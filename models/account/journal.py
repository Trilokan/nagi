# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Journal
class Journal(surya.Sarpam):
    _name = "hos.journal"

    name = fields.Char(string="Journal", required=True)
    code = fields.Char(string="Code")

    def generate_journal_entries(self, obj):
        category = obj.picking_category

        if category == '':
            pass
