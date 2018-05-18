# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya

PROGRESS_INFO = [('draft', 'draft'), ('confirmed', 'Confirmed')]


# Time Configuration
class TimeConfiguration(surya.Sarpam):
    _name = "time.configuration"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    value = fields.Float(string="Value", required=True)
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Time Configuration Created by {0}".format(self.env.user.name)
        return vals
