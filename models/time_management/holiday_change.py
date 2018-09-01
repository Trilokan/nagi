# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta

TIME_DELAY_HRS = 5
TIME_DELAY_MIN = 30

PROGRESS_INFO = [('draft', 'Draft'), ('holiday_changed', 'Holiday Changed')]
DAY_PROGRESS = [('holiday', 'Holiday'), ('working_day', 'Working Day')]


# Week Schedule
class HolidayChange(models.Model):
    _name = "holiday.change"
    _inherit = "mail.thread"
    _rec_name = "person_id"

    date = fields.Date(string="Date", required=True, default=datetime.now().strftime("%Y-%m-%d"))
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)
    day_progress = fields.Selection(DAY_PROGRESS, string='Day Status', required=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft", track_visibility='always')
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    def update_attendance(self):
        current_date_obj = datetime.strptime(self.date, "%Y-%m-%d")
        next_date_obj = current_date_obj + timedelta(days=1)
        next_date = next_date_obj.strftime("%Y-%m-%d")

        attendance = self.env["time.attendance.detail"].search([("person_id", "=", self.person_id.id),
                                                                ("attendance_id.date", "=", self.date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "closed":
                raise exceptions.ValidationError("Error! Month is already closed")

            attendance.write({"day_progress": self.day_progress})
        else:
            raise exceptions.ValidationError("Error! please check")

    @api.multi
    def trigger_approve(self):
        self.update_attendance()
        self.write({'progress': 'holiday_changed'})
