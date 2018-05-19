# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]

DAY_TYPE = [('full_day', 'Full Day'), ('half_day', 'Half Day')]


class CompOff(surya.Sarpam):
    _name = "compoff.application"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    co_type = fields.Selection(selection=DAY_TYPE, string="Type", default="full_day", required=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        self.check_month()
        person_id = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        vals["person_id"] = person_id.id
        vals["writter"] = "Comp-Off application created by {0}".format(self.env.user.name)
        return vals

    def check_month(self):
        attendance = self.env["time.attendance.detail"].search([("attendance_id.date", "=", self.date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "closed":
                raise exceptions.ValidationError("Error! Month is already closed")

    @api.multi
    def trigger_confirmed(self):
        self.check_month()
        data = {"progress": "confirmed",
                "writter": "Comp-Off application confirmed by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        self.check_month()
        data = {"progress": "cancelled",
                "writter": "Comp-Off application cancelled by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        self.check_month()
        attendance = self.env["time.attendance.detail"].search([("attendance_id.date", "=", self.date)])

        employee_id = self.env["hr.employee"].search([("person_id", "=", self.person_id.id)])

        hr_leave = {}

        hr_leave["date"] = self.date
        hr_leave["month_id"] = attendance.attendance_id.month_id.id
        hr_leave["employee_id"] = employee_id.id
        hr_leave["leave_type_id"] = self.env.user.company_id.comp_off_id
        hr_leave["credit"] = 1
        hr_leave["leave_order"] = 1
        hr_leave["allocation_type"] = "current_month"

        self.env["hr.leave"].create(hr_leave)

        data = {"progress": "approved",
                "writter": "Comp-Off application approved by {0}".format(self.env.user.name)}

        self.write(data)

