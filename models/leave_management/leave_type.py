# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Leave Type
class LeaveType(surya.Sarpam):
    _name = "leave.type"
    _inherit = "mail.thread"

    name = fields.Char(string="Type", required=True)
    code = fields.Char(string="Code", required=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Leave type created by {0}".format(self.env.user.name)
        return vals
