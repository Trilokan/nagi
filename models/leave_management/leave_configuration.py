# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave Configuration

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


class LeaveConfigurationMonth(surya.Sarpam):
    _name = "leave.configuration"
    _inherit = "mail.thread"

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    leave_credit = fields.Float(string="Monthly Leave Credit")
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")
    leave_order = fields.Integer(string="Order Sequence")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Leave Configuration created by {0}".format(self.env.user.name)
        return vals

    @api.multi
    def trigger_confirmed(self):
        data = {"progress": "confirmed",
                "writter": "Permission Confirmed by {0}".format(self.env.user.name)}

        self.write(data)
