# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya
from datetime import datetime

RECONCILE_TYPE = [("manual", "Manual"), ("automatic", "Automatic")]


# Leave Reconcile
class LeaveReconcile(surya.Sarpam):
    _name = "leave.reconcile"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    reconcile_type = fields.Selection(selection=RECONCILE_TYPE, string="Type")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["writter"] = "Leave Reconcile By {0}".format(self.env.user.company_id.id)
        return vals


