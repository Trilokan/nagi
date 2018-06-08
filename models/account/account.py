# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class Account(surya.Sarpam):
    _name = "hos.account"

    name = fields.Char(string="Account", required=True)
    code = fields.Char(string="Code", required=True)
    parent_left = fields.Integer(string="Parent Left")
    parent_right = fields.Integer(string="Parent Right")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    is_company = fields.Boolean(string="Is Company")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    parent_id = fields.Many2one(comodel_name="hos.account", string="Parent")
    account_type = fields.Many2one(comodel_name="hos.account.type", string="Account Type")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    balance = fields.Float(string="Balance")

    def default_vals_creation(self, vals):
        vals["parent_id"] = 0