# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json
TIME_DELAY_HRS = 5
TIME_DELAY_MIN = 30


# Time Sheet

PROGRESS_INFO = [('in', 'In'), ('out', 'Out')]
PROCESS_INFO = [('manual', 'Manual'), ('automatic', 'Automatic')]


class TimeSheet(surya.Sarpam):
    _name = "time.sheet"
    _rec_name = "person_id"

    date = fields.Datetime(string="Date", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", readonly=True)
    progress = fields.Selection(PROGRESS_INFO, string='Progress', readonly=True)
    process = fields.Selection(PROCESS_INFO, string='Process', default="automatic", readonly=True)

    def default_vals_creation(self, vals):
        current_time = datetime.strptime(vals['date'], "%Y-%m-%d %H:%M:%S")
        time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        accepted_in_time = self.env["time.configuration"].search([("name", "=", "IN Grace Time")])
        accepted_out_time = self.env["time.configuration"].search([("name", "=", "OUT Grace Time")])

        recs = self.env["time.attendance.detail"].search([("person_id", "=", vals["person_id"])])

        for rec in recs:
            expected_from_time = datetime.strptime(rec.expected_from_time, "%Y-%m-%d %H:%M:%S")
            expected_till_time = datetime.strptime(rec.expected_till_time, "%Y-%m-%d %H:%M:%S")

            expected_from_time_grace = expected_from_time - timedelta(minutes=accepted_in_time.value)
            expected_till_time_grace = expected_till_time + timedelta(minutes=accepted_out_time.value)

            if 'in' in vals['progress']:
                if expected_from_time_grace <= current_time <= expected_till_time_grace:
                    rec.write({"actual_from_time": time})

            elif 'out' in vals['progress']:
                if expected_from_time_grace <= current_time <= expected_till_time_grace:
                    rec.write({"actual_till_time": time})

        return vals