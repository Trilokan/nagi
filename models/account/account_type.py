# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account Type
class AccountType(surya.Sarpam):
    _name = "hos.account.type"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")
