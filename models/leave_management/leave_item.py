# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Journal Entry Detail
class LeaveItem(surya.Sarpam):
    _name = "leave.item"

    date = fields.Date(string="Date", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    name = fields.Char(string="Name")
    reference = fields.Char(string="Reference")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile_id = fields.Many2one(comodel_name="leave.reconcile", string="Reconcile Id")
    leave_account_id = fields.Many2one(comodel_name="leave.account", string="Account")
    journal_id = fields.Many2one(comodel_name="leave.journal", string="Journal Entry")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="journal_id.progress")
    comment = fields.Text(string="Comment")

    def default_vals_creation(self, vals):

        print vals
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        return vals