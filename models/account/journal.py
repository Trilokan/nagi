# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Journal
class Journal(surya.Sarpam):
    _name = "hos.journal"

    name = fields.Char(string="Journal", required=True)
    code = fields.Char(string="Code")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")
