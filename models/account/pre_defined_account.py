# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Account
class PreDefinedAccount(surya.Sarpam):
    _name = "pre.defined.account"

    name = fields.Char(string="Account", required=True)
    code = fields.Char(string="Code", required=True)
