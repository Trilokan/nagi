# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Journal Entry Detail
class JournalItem(surya.Sarpam):
    _name = "journal.item"
    _inherit = "mail.thread"

    date = fields.Date(string="Date",
                       default=datetime.now().strftime("%Y-%m-%d"),
                       readonly=True)
    name = fields.Char(string="Name", readonly=True)
    reference = fields.Char(string="Reference")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile_id = fields.Many2one(comodel_name="hos.reconcile", string="Reconcile Id")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    entry_id = fields.Many2one(comodel_name="journal.entry", string="Journal Entry")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="entry_id.progress")
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["writter"] = "Journal Item Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals
