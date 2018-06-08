# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Journal Entry Detail
class JournalEntryDetail(surya.Sarpam):
    _name = "journal.entry.detail"

    date = fields.Date(string="Date", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
    journal_id = fields.Many2one(comodel_name="hos.journal", string="Journal", required=True)

    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile_amount = fields.Float(string="Reconcile Amount")
    balance_amount = fields.Float(string="Balance Amount")
    reconcile_id = fields.Many2one(comodel_name="journal.entry.detail", string="Reconcile Id")
    partial_reconcile_id = fields.Many2one(comodel_name="journal.entry.detail", string="Partial Reconcile Id")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    entry_id = fields.Many2one(comodel_name="entry.detail", string="Journal Entry")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="entry_id.progress")

