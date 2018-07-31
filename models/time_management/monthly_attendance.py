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

    def generate_header(self, date_list):
        header = ""

        header_list = ["Employee"] + date_list + ["Total Days",
                                                  "Present Days",
                                                  "Absent Days",
                                                  "Holidays",
                                                  "Holidays Present"]

        for rec in header_list:
            header = "{0}\n<th>{1}</th>".format(header, rec)

        header = "<tr>{0}</tr>".format(header)
        return header

    def generate_body(self, date_list, person_list):
        body = ""

        for person in person_list:
            person_id = self.env["hos.person"].search([("id", "=", person)])
            body = "{0}\n<tr><td>{1}</td>".format(body, person_id.name)

            for date in date_list:
                attendance = self.env["time.attendance.detail"].search([("person_id", "=", person),
                                                                        ("attendance_id.date", "=", date)])
                body = "{0}\n<td>{1}</td>".format(body, attendance.availability_progress)

            body = """{0}<td>{1}</td>
                         <td>{2}</td>
                         <td>{3}</td>
                         <td>{4}</td>
                         <td>{5}</td></tr>""".format(body, 0, 0, 0, 0, 0)

        return body

    def trigger_preview(self):
        recs = self.month_detail

        date_list = []
        person_list = []
        for rec in recs:
            date_list.append(rec.date)

        recs = self.env["time.attendance.detail"].search([("attendance_id.month_id", "=", self.id)])

        for rec in recs:
            if rec.person_id.id not in person_list:
                person_list.append(rec.person_id.id)

        header = self.generate_header(date_list)
        body = self.generate_body(date_list, person_list)

        html = self.env.user.company_id.monthly_attendance_report
        report = html.format(header, body)

        view = self.env.ref('nagi.view_month_attendance_wiz_form')

        return {
            'name': 'Monthly Attendance',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'month.attendance.wiz',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'report': report}
        }

    @api.multi
    def trigger_closed(self):
        draft = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "!=", "verified")])

        if draft:
            raise exceptions.ValidationError("Error! Daily attendance report is not verified")

        employees = self.env["hr.employee"].search([])

        for employee in employees:
            total_absent = self.total_absent(employee.person_id)

            voucher = {}
            voucher["period_id"] = self.period_id.id
            voucher["person_id"] = employee.person_id.id
            voucher["count"] = total_absent

            voucher_id = self.env["leave.voucher"].create(voucher)
            voucher_id.get_cr_lines()
            voucher_id.update_count()
            voucher_id.trigger_posting()

        self.write({"progress": "closed"})

    @api.multi
    def trigger_open(self):
        if self.env["month.attendance"].search_count([("progress", "=", "open"), ("id", "!=", self.id)]):
            raise exceptions.ValidationError("Error! Please close all open months before open")

        # Leave Credits from leave configuration
        employees = self.env["hr.employee"].search([])

        for employee in employees:
            leave_item = []
            configs = self.env["leave.configuration"].search([("leave_level_id", "=", employee.leave_level_id.id)])

            # Credit Detail - Employee
            for config in configs:
                journal_detail = {}
                journal_detail["period_id"] = self.period_id.id
                journal_detail["person_id"] = employee.person_id.id
                journal_detail["leave_account_id"] = employee.leave_account_id.id
                journal_detail["description"] = "{0} Leave Credit".format(config.leave_type_id.name)
                journal_detail["debit"] = config.leave_credit
                journal_detail["reference"] = self.period_id.name

                leave_item.append((0, 0, journal_detail))

            # Credit Detail - Monthly
            for config in configs:
                journal_detail = {}
                journal_detail["period_id"] = self.period_id.id
                journal_detail["person_id"] = employee.person_id.id
                journal_detail["leave_account_id"] = self.env.user.company_id.leave_credit_id.id
                journal_detail["description"] = "Leave Credit"
                journal_detail["credit"] = config.leave_credit
                journal_detail["reference"] = self.period_id.name

                leave_item.append((0, 0, journal_detail))

            journal = {}
            journal["period_id"] = self.period_id.id
            journal["person_id"] = employee.person_id.id
            journal["journal_detail"] = leave_item
            journal["progress"] = "posted"
            journal["reference"] = self.period_id.name

            self.env["leave.journal"].create(journal)

        self.write({"progress": "open"})

