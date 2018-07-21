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
    debit_lines = fields.One2many(comodel_name="leave.voucher.debit.line",
                                  inverse_name="voucher_id",
                                  string="Leave Voucher Line")

    credit_lines = fields.One2many(comodel_name="leave.voucher.credit.line",
                                   inverse_name="voucher_id",
                                   string="Leave Voucher Line")

    is_manual = fields.Boolean(string="Is Manual")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.onchange("count")
    def update_count(self):
        cr_line = self.credit_lines
        dr_line = self.debit_lines

        count = self.count

        for rec in cr_line:
            rec.reconcile = False
            rec.leave_reconcile = 0

        for rec in dr_line:
            rec.reconcile = False
            rec.leave_reconcile = 0

        for cr in cr_line:
            cr_diff = cr.credit - cr.leave_reconcile
            if cr_diff > 0:
                if cr_diff >= count:
                    cr.leave_reconcile = cr.leave_reconcile + count
                    cr.reconcile = True

                elif cr_diff < count:
                    cr.reconcile = True
                    cr.leave_reconcile = cr.leave_reconcile + cr_diff

        for dr in dr_line:
            for cr in cr_line:
                cr_diff = cr.credit - cr.leave_reconcile
                dr_diff = dr.debit - dr.leave_reconcile
                if cr_diff > 0:
                    if cr_diff >= dr_diff:
                        cr.leave_reconcile = cr.leave_reconcile + dr_diff
                        dr.leave_reconcile = dr.leave_reconcile + dr_diff
                        cr.reconcile = True
                        dr.reconcile = True

                    elif cr_diff < dr_diff:
                        cr.reconcile = True
                        dr.reconcile = True
                        dr.leave_reconcile = dr.leave_reconcile + cr_diff
                        cr.leave_reconcile = cr.leave_reconcile + cr_diff

        # Get Difference
        for rec in cr_line:
            if rec.reconcile:
                count = count - rec.credit

        for rec in dr_line:
            if rec.reconcile:
                count = count + rec.debit

        self.difference = count

    @api.onchange("person_id")
    def get_cr_dr_lines(self):
        if self.person_id:
            self.credit_lines.unlink()
            res_cr = []

            recs_cr = self.env["leave.item"].search([("person_id", "=", self.person_id.id),
                                                     ("credit", ">", 0),
                                                     ("reconcile_id", "=", False)])
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
                                                     ("reconcile_id", "=", False)])
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
        pass

    @api.multi
    def trigger_posting(self):

        data = {"progress": "posted",
                "writter": "Leave Voucher posted by {0}".format(self.env.user.name)}

        self.write(data)

    def default_vals_creation(self, vals):
        vals["company_id"] = self.env.user.company_id.id
        vals["writter"] = "Leave Voucher created by {0}".format(self.env.user.name)

        return vals


class LeaveVoucherCreditLine(surya.Sarpam):
    _name = "leave.voucher.credit.line"

    date = fields.Date(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    voucher_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher")
    credit = fields.Float(string="Credit")
    reconcile = fields.Boolean(string="Reconcile")
    journal_id = fields.Many2one(comodel_name="leave.item", string="Journal Item")
    leave_reconcile = fields.Float(string="Leave Reconcile")
    difference = fields.Float(string="Difference")



class LeaveVoucherDebitLine(surya.Sarpam):
    _name = "leave.voucher.debit.line"

    date = fields.Date(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    voucher_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher")
    debit = fields.Float(string="Debit")
    reconcile = fields.Boolean(string="Reconcile")
    journal_id = fields.Many2one(comodel_name="leave.item", string="Journal Item")
    leave_reconcile = fields.Float(string="Leave Reconcile")
    difference = fields.Float(string="Difference")

