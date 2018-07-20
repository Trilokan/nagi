# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class HosLeave(surya.Sarpam):
    _name = "hos.leave"

    name = fields.Char(string="Account", required=True)
    code = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
