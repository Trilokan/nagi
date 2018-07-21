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
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    journal_detail = fields.One2many(comodel_name="leave.item",
                                     inverse_name="journal_id",
                                     string="Journal Entry Detail")

    def default_vals_creation(self, vals):

        print vals
        vals["company_id"] = self.env.user.company_id.id

        person_id = self.env["hos.person"].search([("id", "=", vals["person_id"])])
        employee_id = self.env["hr.employee"].search([("person_id", "=", person_id.id)])

        credit = debit = 0
        recs = vals["journal_detail"]

        for rec in recs:
            if rec["credit"] > 0:
                credit = credit + rec["credit"]

            if rec["debit"] > 0:
                debit = debit + rec["debit"]

        data = {"period_id": vals["period_id"],
                "company_id": self.env.user.company_id.id,
                "person_id": person_id.id,
                "description": "Monthly Leave Credit",
                "leave_account_id": employee_id.leave_account_id.id}

        if credit > debit:
            credit_dict = {"credit": credit}
            credit_dict.update(data)
            vals["journal_detail"].append(credit_dict)

        if debit > credit:
            debit_dict = {"debit": debit}
            debit_dict.update(data)
            vals["journal_detail"].append(debit_dict)

        return vals