# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Shift Master

PROGRESS_INFO = [('draft', 'draft'), ('confirmed', 'Confirmed')]
END_INFO = [('current_day', 'Current Day'), ('next_day', 'Next Day')]


class Shift(surya.Sarpam):
    _name = "time.shift"
    _inherit = "mail.thread"

    name = fields.Char(string="Shift", required=True)
    total_hours = fields.Float(string="Total Hours", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    end_day = fields.Selection(selection=END_INFO, string="Ends On", default="current_day")
    from_hours = fields.Integer(string="From Hours")
    from_minutes = fields.Integer(string="From Minutes")
    till_hours = fields.Integer(string="Till Hours")
    till_minutes = fields.Integer(string="Till Minutes")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Shift Created by {0}".format(self.env.user.name)
        return vals

    @api.multi
    def trigger_calculate(self):
        total_from_hours = (self.from_hours * 60) + self.from_minutes
        total_till_hours = (self.till_hours * 60) + self.till_minutes
        if self.end_day == 'current_day':
            self.total_hours = float(total_till_hours - total_from_hours) / 60
        elif self.end_day == 'next_day':
            self.total_hours = 24 - (float(total_from_hours - total_till_hours) / 60)

    @api.multi
    def trigger_confirm(self):
        self.trigger_calculate()
        self.write({"progress": "confirmed",
                    "writter": "Shift Created by {0}".format(self.env.user.name)})
