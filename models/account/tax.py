# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


STATE_INFO = [("inter_state", "Inter state"), ("outer_state", "Outer State")]


# Tax
class Tax(surya.Sarpam):
    _name = "hos.tax"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(selection=STATE_INFO, string="State")
    value = fields.Char(string="Value", required=True)
