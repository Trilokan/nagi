# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave Configuration
class LeaveConfigurationMonth(surya.Sarpam):
    _name = "leave.configuration"
    _inherit = "mail.thread"
    _rec_name = "leave_type_id"

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    leave_credit = fields.Float(string="Credit Days", required=True)
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level", required=True)
    leave_order = fields.Integer(string="Order Sequence", required=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Leave Configuration created by {0}".format(self.env.user.name)
        return vals



