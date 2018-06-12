# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


# Operation
class Operation(surya.Sarpam):
    _name = "hos.operation"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
