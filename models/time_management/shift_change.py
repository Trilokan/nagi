# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya
TIME_DELAY_HRS = 5
TIME_DELAY_MIN = 30


# Week Schedule

PROGRESS_INFO = [('draft', 'Draft'), ('shift_changed', 'Shift Changed')]


class ShiftChange(surya.Sarpam):
    _name = "shift.change"
    _inherit = "mail.thread"
    _rec_name = "person_id"

    date = fields.Date(string="Date", required=True)
    shift_id = fields.Many2one(comodel_name="time.shift", string="Shift", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", required=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft", track_visibility='always')

    def update_attendance(self):
        current_date_obj = datetime.strptime(self.date, "%Y-%m-%d")
        next_date_obj = current_date_obj + timedelta(days=1)
        next_date = next_date_obj.strftime("%Y-%m-%d")

        attendance = self.env["time.attendance.detail"].search([("person_id", "=", self.person_id.id),
                                                                ("attendance_id.date", "=", self.date)])

        if attendance:
            if attendance.attendance_id.month_id.progress == "verified":
                raise exceptions.ValidationError("Error! Month is already closed")

            expected_from_time = "{0} {1}:{2}:00".format(self.date,
                                                         self.shift_id.from_hours,
                                                         self.shift_id.from_minutes)
            if self.shift_id.end_day == 'current_day':
                expected_till_time = "{0} {1}:{2}:00".format(self.date,
                                                             self.shift_id.till_hours,
                                                             self.shift_id.till_minutes)
            elif self.shift_id.end_day == 'next_day':
                expected_till_time = "{0} {1}:{2}:00".format(self.date,
                                                             self.shift_id.till_hours,
                                                             self.shift_id.till_minutes)

            new_from_time_obj = datetime.strptime(expected_from_time, "%Y-%m-%d %H:%M:%S") - timedelta(
                minutes=(TIME_DELAY_HRS * 60) + TIME_DELAY_MIN)
            new_till_time_obj = datetime.strptime(expected_till_time, "%Y-%m-%d %H:%M:%S") - timedelta(
                minutes=(TIME_DELAY_HRS * 60) + TIME_DELAY_MIN)

            attendance.write({"shift_id": self.shift_id.id,
                              "expected_from_time": new_from_time_obj,
                              "expected_till_time": new_till_time_obj})
        else:
            raise exceptions.ValidationError("Error! please check")

    @api.multi
    def trigger_approve(self):
        self.update_attendance()
        self.write({'progress': 'shift_changed'})


