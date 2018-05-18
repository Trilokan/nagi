# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


# Salary Rule Type
class SalaryRuleCode(surya.Sarpam):
    _name = "salary.rule.code"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    def default_vals_creation(self, vals):
        vals["writter"] = "Salary Rule Code Created by {0}".format(self.env.user.name)
        return vals

    def trigger_confirm(self):
        writter = "Salary Rule Code Confirmed by {0}".format(self.env.user.name)
        self.write({"progress": "confirmed", "writter": writter})
