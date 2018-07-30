# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
from lxml import etree


# Week Schedule

PROGRESS_INFO = [('draft', 'draft'), ('open', 'Open'), ('closed', 'Closed')]


class MonthAttendance(surya.Sarpam):
    _name = "month.attendance"
    _rec_name = "period_id"

    period_id = fields.Many2one(comodel_name="period.period", string="Month", required=True)
    month_detail = fields.One2many(comodel_name="time.attendance",
                                   inverse_name="month_id",
                                   string="Month Detail")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")

    _sql_constraints = [('unique_period_id', 'unique (period_id)', 'Error! Month must be unique')]

    def calc_total_days(self):
        from_date = datetime.strptime(self.period_id.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.period_id.till_date, "%Y-%m-%d")

        return (till_date - from_date).days

    def calc_total_present(self, person):
        full_day = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("availability_progress", "=", "full_day")])
        half_day = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("availability_progress", "=", "half_day")])

        return full_day + (0.5 * half_day)

    def calc_total_absent(self, person):
        absent = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                  ("attendance_id.month_id", "=", self.id),
                                                                  ("day_progress", "=", "working_day"),
                                                                  ("availability_progress", "=", "absent")])

        return absent

    def calc_total_working_days(self, person):
        working_days = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                        ("attendance_id.month_id", "=", self.id),
                                                                        ("day_progress", "=", "working_day")])

        return working_days

    def calc_total_holidays(self, person):
        holidays = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("day_progress", "=", "holiday")])

        return holidays

    @api.multi
    def trigger_closed(self):
        draft = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "!=", "verified")])

        if draft:
            raise exceptions.ValidationError("Error! Daily attendance report is not verified")

        person_ids = self.env["hos.person"].search([])

        total_days = self.calc_total_days()

        for person in person_ids:
            total_present = self.calc_total_present(person)
            total_absent = self.calc_total_absent(person)
            total_working_days = self.calc_total_working_days(person)
            total_holidays = self.calc_total_holidays(person)

            debit = (total_holidays + total_working_days) - (total_present + total_absent)

            employee_id = self.env["hr.employee"].search([("person_id", "=", person.id)])

            credit_recs = self.env["hr.leave"].search([("employee_id", "=", employee_id.id),
                                                       ("month_id", "=", self.id),
                                                       ("credit", ">", 0)])
            credit = 0
            for rec in credit_recs:
                credit = credit + rec.credit

            credit_data = {"employee_id": employee_id.id,
                           "month_id": self.id,
                           "date": datetime.now().strftime("%Y-%m-%d"),
                           "leave_type_id": self.env.user.company_id.lop_id.id}

            if debit > credit:
                credit_data["credit"] = debit - credit

            else:
                credit_data["debit"] = 0

                self.env["hr.leave"].create(credit_data)

            debit_date = {"employee_id": employee_id.id,
                          "month_id": self.id,
                          "debit": debit,
                          "date": datetime.now().strftime("%Y-%m-%d")}

            self.env["hr.leave"].create(debit_date)

        self.write({"progress": "closed"})

    @api.multi
    def trigger_open(self):
        if self.env["month.attendance"].search_count([("progress", "=", "open"), ("id", "!=", self.id)]):
            raise exceptions.ValidationError("Error! Please close all open months before open")

        self.update_last_month_opening()
        configs = self.env["leave.configuration"].search([])

        for config in configs:
            person_ids = self.env["hos.person"].search([])

            for person in person_ids:
                employee_id = self.env["hr.employee"].search([("person_id", "=", person.id)])

                hr_leave = {"employee_id": employee_id.id,
                            "month_id": self.id,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "leave_type_id": config.leave_type_id.id,
                            "credit": config.leave_credit,
                            "leave_order": config.leave_order}

                self.env["hr.leave"].create(hr_leave)

        self.write({"progress": "open"})

    @api.multi
    def update_last_month_opening(self):
        from_date_obj = datetime.strptime(self.period_id.from_date, "%Y-%m-%d")
        previous_day = from_date_obj - timedelta(days=1)
        previous_month = self.env["period.period"].search([("from_date", ">=", previous_day.strftime("%Y-%m-%d")),
                                                           ("till_date", "<=", previous_day.strftime("%Y-%m-%d"))])

        if previous_month:
            employees = self.env["hr.employee"].search([])

            for employee in employees:
                credit_records = self.env["hr.leave"].search([("employee_id", "=", employee.id),
                                                              ("month_id", "=", previous_month.id),
                                                              ("credit", ">", 0)])

                debit_records = self.env["hr.leave"].search([("employee_id", "=", employee.id),
                                                             ("month_id", "=", previous_month.id),
                                                             ("debit", ">", 0)])

                debit = 0
                for record in debit_records:
                    debit = debit + record.debit

                credit_records = credit_records.sorted(key=lambda r: r.leave_order)

                for record in credit_records:
                    debit = debit - record.credit

                    if debit < 0:
                        self.env["hr.leave"].create({"employee_id": employee.id,
                                                     "month_id": self.id,
                                                     "allocation_type": "carry_forward",
                                                     "date": datetime.now().strftime("%Y-%m-%d"),
                                                     "leave_type_id": record.leave_type_id.id,
                                                     "credit": - debit,
                                                     "leave_order": record.leave_order})

                        debit = 0

    # Update as per accounting
    @api.multi
    def trigger_month_open(self):
        # Leave Credits from leave configuration
        employees = self.env["hr.employee"].search([])

        leave_item = []
        for employee in employees:
            configs = self.env["leave.configuration"].search([("leave_level_id", "=", employee.leave_level_id.id)])

            for config in configs:
                journal_detail = {}
                journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
                journal_detail["period_id"] = self.period_id.id
                journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
                journal_detail["company_id"] = self.env.user.company_id.id
                journal_detail["person_id"] = employee.person_id.id
                journal_detail["description"] = "{0} Leave Credit".format(config.leave_type_id.name)
                journal_detail["credit"] = config.leave_credit
                journal_detail["leave_account_id"] = employee.leave_account_id.id

                leave_item.append((0, 0, journal_detail))

            for config in configs:
                journal_detail = {}
                journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
                journal_detail["period_id"] = self.period_id.id
                journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
                journal_detail["company_id"] = self.env.user.company_id.id
                journal_detail["person_id"] = employee.person_id.id
                journal_detail["description"] = "Leave Credit"
                journal_detail["debit"] = config.leave_credit
                journal_detail["leave_account_id"] = self.env.user.company_id.leave_credit_id.id

                leave_item.append((0, 0, journal_detail))

            journal = {}

            journal["date"] = datetime.now().strftime("%Y-%m-%d")
            journal["period_id"] = self.period_id.id
            journal["name"] = self.env['ir.sequence'].next_by_code("leave.journal")
            journal["company_id"] = self.env.user.company_id.id
            journal["person_id"] = employee.person_id.id
            journal["journal_detail"] = leave_item
            journal["progress"] = "posted"

            self.env["leave.journal"].create(journal)

