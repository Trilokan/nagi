# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave Level
class LeaveLevel(surya.Sarpam):
    _name = "leave.level"
    _inherit = "mail.thread"

    name = fields.Char(string="Level", required=True)
    code = fields.Char(string="Code", required=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Leave level created by {0}".format(self.env.user.name)
        return vals




