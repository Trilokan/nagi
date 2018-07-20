# -*- coding: utf-8 -*-

from odoo import fields, api
from .. import surya
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
VOUCHER_INFO = [("credit", "Credit"), ("debit", "Debit")]


# Leave Voucher
class LeaveVoucher(surya.Sarpam):
    _name = "leave.voucher"

    date = fields.Date(string="Date", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    count = fields.Float(string="Count")
    difference = fields.Float(string="Difference")
    debit_lines = fields.One2many(comodel_name="leave.voucher.line",
                                  inverse_name="debit_id",
                                  string="Leave Voucher Line")

    credit_lines = fields.One2many(comodel_name="leave.voucher.line",
                                   inverse_name="credit_id",
                                   string="Leave Voucher Line")

    is_manual = fields.Boolean(string="Is Manual")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.onchange("count")
    def update_count(self):
        # Reset all reconcile
        for rec in self.debit_lines:
            rec.leave_reconcile = 0

        for rec in self.credit_lines:
            rec.leave_reconcile = 0

        # Credit Reconcilation
        leave_days = self.count

        for rec in self.debit_lines:
            rec.reconcile = True
            leave_days = leave_days + rec.debit

        for rec in self.credit_lines:
            value = rec.credit - rec.leave_reconcile
            total = value - leave_days

            if (total >= 0) and (value > 0):
                rec.reconcile = True
                rec.leave_reconcile = rec.leave_reconcile + leave_days
                leave_days = 0

            elif (total < 0) and (value > 0):
                rec.reconcile = True
                rec.leave_reconcile = rec.leave_reconcile + value
                leave_days = leave_days - value

        # Debit reconcilation
        credit_reconciled = 0

        for rec in self.credit_lines:
            if rec.reconcile:
                credit_reconciled = credit_reconciled + rec.leave_reconcile

        debit = credit_reconciled - self.count

        for rec in self.debit_lines:
            rec.reconcile = False
            value = rec.debit - debit

            if value >= 0:
                rec.reconcile = True
                rec.leave_reconcile = debit
                debit = 0
            else:
                rec.reconcile = True
                rec.leave_reconcile = rec.debit
                debit = debit - rec.debit

        self.difference = leave_days

    @api.onchange("person_id")
    def get_cr_dr_lines(self):
        if self.person_id:
            self.credit_lines.unlink()
            res_cr = []

            recs_cr = self.env["leave.item"].search([("person_id", "=", self.person_id.id),
                                                     ("credit", ">", 0),
                                                     ("reconcile_id", "=", False),
                                                     ("reconcile_partial_id", "=", False)])
            for rec in recs_cr:
                data = {}

                data["date"] = rec.date
                data["name"] = rec.name
                data["person_id"] = rec.person_id.id
                data["description"] = rec.description
                data["credit"] = rec.credit
                data["journal_id"] = rec.id
                data["voucher_type"] = "credit"
                res_cr.append(data)

            self.credit_lines = res_cr

            self.debit_lines.unlink()
            res_dr = []
            recs_dr = self.env["leave.item"].search([("person_id", "=", self.person_id.id),
                                                     ("debit", ">", 0),
                                                     ("reconcile_id", "=", False),
                                                     ("reconcile_partial_id", "=", False)])
            for rec in recs_dr:
                data = {}

                data["date"] = rec.date
                data["name"] = rec.name
                data["person_id"] = rec.person_id.id
                data["description"] = rec.description
                data["debit"] = rec.debit
                data["journal_id"] = rec.id
                data["voucher_type"] = "debit"
                res_dr.append(data)

            self.debit_lines = res_dr

    def generate_journal(self):
        # Create leave days

        reconcile_data = {"date": self.date,
                          "name": "",
                          "reconcile_type": "manual" if self.is_manual else "automatic"}

        reconcile_id = self.env["leave.reconcile"].create(reconcile_data)

        detail = []

        data = {}

        data["date"] = self.date
        data["period_id"] = ""
        data["reference"] = self.name
        data["company_id"] = self.env.user.company_id.id
        data["person_id"] = self.person_id.id
        data["description"] = ""
        data["credit"] = ""
        data["debit"] = ""
        data["reconcile_id"] = ""
        data["reconcile_partial_id"] = ""
        data["leave_id"] = ""
        data["leave_id"] = ""
        data["journal_id"] = ""
        data["progress"] = ""

    @api.multi
    def trigger_posting(self):

        data = {"progress": "posted",
                "writter": "Leave Voucher posted by {0}".format(self.env.user.name)}

        self.write(data)

    def default_vals_creation(self, vals):
        vals["company_id"] = self.env.user.company_id.id
        vals["writter"] = "Leave Voucher created by {0}".format(self.env.user.name)

        return vals


class LeaveVoucherLine(surya.Sarpam):
    _name = "leave.voucher.line"

    date = fields.Date(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    credit_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher")
    debit_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher")
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    reconcile = fields.Boolean(string="Reconcile")
    journal_id = fields.Many2one(comodel_name="leave.item", string="Journal Item")
    leave_reconcile = fields.Float(string="Leave Reconcile")




