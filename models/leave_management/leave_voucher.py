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
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
    count = fields.Float(string="Count")
    difference = fields.Float(string="Difference")
    credit_lines = fields.One2many(comodel_name="leave.voucher.line",
                                   inverse_name="voucher_id",
                                   string="Leave Voucher Line")

    is_manual = fields.Boolean(string="Is Manual")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.onchange("count")
    def update_count(self):
        cr_line = self.credit_lines

        count = self.count

        for rec in cr_line:
            rec.reconcile = False
            rec.leave_reconcile = 0

        for cr in cr_line:
            cr_diff = cr.credit - cr.leave_reconcile
            if (cr_diff > 0) and (count > 0):
                if cr_diff >= count:
                    cr.leave_reconcile = cr.leave_reconcile + count
                    count = 0
                    cr.reconcile = True

                elif cr_diff < count:
                    cr.reconcile = True
                    cr.leave_reconcile = cr.leave_reconcile + cr_diff
                    count = count - cr_diff

        self.difference = count

    @api.onchange("employee_id")
    def get_cr_lines(self):
        if self.employee_id:
            self.credit_lines.unlink()
            res_cr = []

            leave_account_id = self.employee_id.leave_account_id.id

            recs_cr = self.env["leave.item"].search([("leave_account_id", "=", leave_account_id),
                                                     ("credit", ">", 0),
                                                     ("reconcile_id", "=", False)])

            for rec in recs_cr:
                data = {}

                print rec.id

                data["date"] = rec.date
                data["name"] = rec.name
                data["employee_id"] = self.employee_id.id
                data["description"] = rec.description
                data["credit"] = rec.credit
                data["item_id"] = rec.id
                data["voucher_type"] = "credit"
                res_cr.append(data)

            self.credit_lines = res_cr

    @api.multi
    def generate_journal(self):
        # Create Journal for leave Taken

        reconcile_id = self.env["leave.reconcile"].create({})

        leave_item = []

        journal_detail = {}
        journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
        journal_detail["period_id"] = self.period_id.id
        journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
        journal_detail["company_id"] = self.env.user.company_id.id
        journal_detail["person_id"] = self.employee_id.person_id.id
        journal_detail["description"] = "Leave Debit"
        journal_detail["credit"] = self.count
        journal_detail["leave_account_id"] = self.env.user.company_id.leave_debit_id.id

        leave_item.append((0, 0, journal_detail))

        journal_detail = {}
        journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
        journal_detail["period_id"] = self.period_id.id
        journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
        journal_detail["company_id"] = self.env.user.company_id.id
        journal_detail["person_id"] = self.employee_id.person_id.id
        journal_detail["description"] = "Leave Debit"
        journal_detail["debit"] = self.difference
        journal_detail["leave_account_id"] = self.env.user.company_id.leave_lop_id.id

        leave_item.append((0, 0, journal_detail))

        # Create Journal for reconcillation
        recs = self.credit_lines

        for rec in recs:
            if rec.leave_reconcile > 0:
                rec.item_id.write({"reconcile_id": reconcile_id.id})

                journal_detail = {}
                journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
                journal_detail["period_id"] = self.period_id.id
                journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
                journal_detail["company_id"] = self.env.user.company_id.id
                journal_detail["person_id"] = self.employee_id.person_id.id
                journal_detail["description"] = "Leave Debit"
                journal_detail["debit"] = rec.leave_reconcile
                journal_detail["leave_account_id"] = self.employee_id.leave_account_id.id
                journal_detail["reconcile_id"] = reconcile_id.id

                leave_item.append((0, 0, journal_detail))

                if (rec.credit - rec.leave_reconcile) > 0:
                    journal_detail = {}
                    journal_detail["date"] = datetime.now().strftime("%Y-%m-%d")
                    journal_detail["period_id"] = self.period_id.id
                    journal_detail["name"] = self.env['ir.sequence'].next_by_code("leave.item")
                    journal_detail["company_id"] = self.env.user.company_id.id
                    journal_detail["person_id"] = self.employee_id.person_id.id
                    journal_detail["description"] = "Leave Debit"
                    journal_detail["credit"] = rec.credit - rec.leave_reconcile
                    journal_detail["leave_account_id"] = self.employee_id.leave_account_id.id

                    leave_item.append((0, 0, journal_detail))

        journal = {}

        journal["date"] = datetime.now().strftime("%Y-%m-%d")
        journal["period_id"] = self.period_id.id
        journal["name"] = self.env['ir.sequence'].next_by_code("leave.journal")
        journal["company_id"] = self.env.user.company_id.id
        journal["person_id"] = self.employee_id.person_id.id
        journal["journal_detail"] = leave_item
        journal["progress"] = "posted"

        self.env["leave.journal"].create(journal)

    @api.multi
    def trigger_posting(self):
        self.generate_journal()
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
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    voucher_id = fields.Many2one(comodel_name="leave.voucher", string="Leave Voucher")
    credit = fields.Float(string="Credit")
    reconcile = fields.Boolean(string="Reconcile")
    item_id = fields.Many2one(comodel_name="leave.item", string="Journal Item")
    leave_reconcile = fields.Float(string="Leave Reconcile")
