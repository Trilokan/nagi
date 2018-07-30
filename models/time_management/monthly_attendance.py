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

    def total_days(self):
        from_date = datetime.strptime(self.period_id.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.period_id.till_date, "%Y-%m-%d")

        return (till_date - from_date).days

    def total_absent(self, person):
        absent = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                  ("attendance_id.month_id", "=", self.id),
                                                                  ("day_progress", "=", "working_day"),
                                                                  ("availability_progress", "=", "absent")])
        half_day = self.env["time.attendance.detail"].search_count([("person_id", "=", person.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("day_progress", "=", "working_day"),
                                                                    ("availability_progress", "=", "half_day")])

        return absent + (0.5 * half_day)

    @api.multi
    def trigger_closed(self):
        draft = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "!=", "verified")])

        if draft:
            raise exceptions.ValidationError("Error! Daily attendance report is not verified")

        person_ids = self.env["hos.person"].search([])

        total_days = self.calc_total_days()

        for person in person_ids:
            total_absent = self.total_absent(person)


            # Generate Voucher






        self.write({"progress": "closed"})

    # Update as per accounting
    @api.multi
    def trigger_open(self):
        if self.env["month.attendance"].search_count([("progress", "=", "open"), ("id", "!=", self.id)]):
            raise exceptions.ValidationError("Error! Please close all open months before open")

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
                journal_detail["employee_id"] = employee.id
                journal_detail["description"] = "{0} Leave Credit".format(config.leave_type_id.name)
                journal_detail["debit"] = config.leave_credit
                journal_detail["leave_account_id"] = employee.leave_account_id.id

                leave_item.append((0, 0, journal_detail))

            for config in configs:
                journal_detail = {}
                journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
                journal_detail["period_id"] = self.period_id.id
                journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
                journal_detail["company_id"] = self.env.user.company_id.id
                journal_detail["employee_id"] = employee.id
                journal_detail["description"] = "Leave Credit"
                journal_detail["credit"] = config.leave_credit
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

        self.write({"progress": "open"})

