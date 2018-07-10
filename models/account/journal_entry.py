# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Journal Entry
class JournalEntry(surya.Sarpam):
    _name = "journal.entry"

    date = fields.Date(string="Date", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference")
    journal_id = fields.Many2one(comodel_name="hos.journal", string="Journal", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    entry_detail = fields.One2many(comodel_name="journal.item",
                                   inverse_name="entry_id",
                                   string="Journal Entry Detail")

