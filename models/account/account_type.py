# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class AccountType(surya.Sarpam):
    _name = "hos.account.type"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
