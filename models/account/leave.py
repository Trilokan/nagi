# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class LeaveAccount(surya.Sarpam):
    _name = "leave.account"

    name = fields.Char(string="Account", required=True)
    code = fields.Char(string="Code", readonly=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")

    def default_vals_creation(self, vals):
        vals["company_id"] = self.env.user.company_id.id
        return vals

