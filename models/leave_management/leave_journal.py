# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Journal Entry
class LeaveJournal(surya.Sarpam):
    _name = "leave.journal"

    date = fields.Date(string="Date", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    journal_detail = fields.One2many(comodel_name="leave.item",
                                     inverse_name="journal_id",
                                     string="Journal Entry Detail")

    def default_vals_creation(self, vals):
        vals["company_id"] = self.env.user.company_id.id
        return vals