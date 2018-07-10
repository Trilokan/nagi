# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class PreDefinedAccount(surya.Sarpam):
    _name = "pre.defined.account"

    name = fields.Char(string="Account", required=True)
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
