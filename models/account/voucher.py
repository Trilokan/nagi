# -*- coding: utf-8 -*-

from odoo import fields, api
from .. import surya

PAYMENT_TYPE = [("payment_in", "Payment In"), ("payment_out", "Payment Out")]
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("posted", "Posted")]


# Voucher
class Voucher(surya.Sarpam):
    _name = "hos.voucher"

    date = fields.Date(string="Date")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    journal_id = fields.Many2one(comodel_name="hos.journal", string="Journal")
    name = fields.Char(string="Name", readonly=True)
    amount = fields.Float(string="Amount", default=0)
    difference = fields.Float(string="Difference", default=0)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Type", default="draft")
    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type", default="payment_in")
    credit_detail = fields.One2many(comodel_name="hos.voucher.credit",
                                    inverse_name="voucher_id",
                                    string="Credit Detail")
    debit_detail = fields.One2many(comodel_name="hos.voucher.debit",
                                   inverse_name="voucher_id",
                                   string="Debit Detail")

    @api.onchange('person_id')
    def get_cr_dr_lines(self):
        if (self.payment_type == "payment_in") and self.person_id:

            res_cr = []
            recs_cr = self.env["journal.item"].search([("account_id", "=", self.person_id.payable_id.id),
                                                       ("credit", ">", 0),
                                                       ("reconcile_id", "=", False)])

            for rec in recs_cr:
                data = {}

                data["date"] = rec.date
                data["person_id"] = rec.person_id.id
                data["company_id"] = rec.company_id.id
                data["account_id"] = rec.account_id.id
                data["description"] = rec.description
                data["credit"] = rec.credit
                data["amount_allocated"] = 0
                data["voucher_id"] = self.id
                data["item_id"] = rec.id
                res_cr.append(data)

            res_dr = []
            recs_dr = self.env["journal.item"].search([("account_id", "=", self.person_id.payable_id.id),
                                                       ("debit", ">", 0),
                                                       ("reconcile_id", "=", False)])

            for rec in recs_dr:
                data = {}

                data["date"] = rec.date
                data["person_id"] = rec.person_id.id
                data["company_id"] = rec.company_id.id
                data["account_id"] = rec.account_id.id
                data["description"] = rec.description
                data["debit"] = rec.debit
                data["amount_allocated"] = 0
                data["voucher_id"] = self.id
                data["item_id"] = rec.id
                res_dr.append(data)

            self.credit_detail = res_cr
            self.debit_detail = res_dr

    @api.onchange("amount")
    def update_count(self):
        cr_line = self.credit_detail
        dr_line = self.debit_detail

        amount = self.amount

        for rec in cr_line:
            rec.reconcile = False
            rec.amount_allocated = 0

        for rec in dr_line:
            rec.reconcile = False
            rec.amount_allocated = 0

        for cr in cr_line:
            cr_diff = cr.credit - cr.amount_allocated
            if cr_diff > 0:
                if cr_diff >= amount:
                    cr.amount_allocated = cr.amount_allocated + amount
                    cr.reconcile = True

                elif cr_diff < amount:
                    cr.reconcile = True
                    cr.amount_allocated = cr.amount_allocated + cr_diff

        for dr in dr_line:
            for cr in cr_line:
                cr_diff = cr.credit - cr.amount_allocated
                dr_diff = dr.debit - dr.amount_allocated
                if cr_diff > 0:
                    if cr_diff >= dr_diff:
                        cr.amount_allocated = cr.amount_allocated + dr_diff
                        dr.amount_allocated = dr.amount_allocated + dr_diff
                        cr.reconcile = True
                        dr.reconcile = True

                    elif cr_diff < dr_diff:
                        cr.reconcile = True
                        dr.reconcile = True
                        dr.amount_allocated = dr.amount_allocated + cr_diff
                        cr.amount_allocated = cr.amount_allocated + cr_diff

        # Get Difference
        for rec in cr_line:
            if rec.reconcile:
                amount = amount - rec.credit

        for rec in dr_line:
            if rec.reconcile:
                amount = amount + rec.debit

        self.difference = amount


class VoucherCreditLine(surya.Sarpam):
    _name = "hos.voucher.credit"

    date = fields.Date(string="Date")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    description = fields.Text(string="Description")
    credit = fields.Float(string="Credit", default=0)
    amount_allocated = fields.Float(string="Amount Allocated", default=0)
    voucher_id = fields.Many2one(comodel_name="hos.voucher", string="Voucher")
    reconcile = fields.Boolean(string="Reconcile")
    item_id = fields.Many2one(comodel_name="journal.item", string="Journal Item")


class VoucherDebitLine(surya.Sarpam):
    _name = "hos.voucher.debit"

    date = fields.Date(string="Date")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    description = fields.Text(string="Description")
    debit = fields.Float(string="Debit", default=0)
    amount_allocated = fields.Float(string="Amount Allocated", default=0)
    voucher_id = fields.Many2one(comodel_name="hos.voucher", string="Voucher")
    reconcile = fields.Boolean(string="Reconcile")
    item_id = fields.Many2one(comodel_name="journal.item", string="Journal Item")
