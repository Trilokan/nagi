# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Journal Entry
class LeaveJournal(surya.Sarpam):
    _name = "leave.journal"

    date = fields.Date(string="Date", required=True, default=datetime.now().strftime("%Y-%m-%d"))
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    name = fields.Char(string="Name", readonly=True)
    reference = fields.Char(string="Reference")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    journal_detail = fields.One2many(comodel_name="leave.item",
                                     inverse_name="journal_id",
                                     string="Journal Entry Detail")

    def default_vals_creation(self, vals):
        vals["company_id"] = self.env.user.company_id.id
        vals["name"] = self.env['ir.sequence'].next_by_code("leave.journal")
        return vals
