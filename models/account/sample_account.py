# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class SampleAccount(surya.Sarpam):
    _name = "hos.account.sample"

    name = fields.Char(string="Account", required=True)
    code = fields.Char(string="Code", required=True)
    parent_left = fields.Integer(string="Parent Left")
    parent_right = fields.Integer(string="Parent Right")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    is_company = fields.Boolean(string="Is Company")
    parent_id = fields.Many2one(comodel_name="hos.account", string="Parent")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    balance = fields.Float(string="Balance")
