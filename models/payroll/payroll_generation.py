# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya

# payroll Generation
PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]


class PayrollGeneration(surya.Sarpam):
    _name = "payroll.generation"
    _inherit = "mail.thread"
    _rec_name = "month_id"

    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", required=True)
    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employee")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    @api.multi
    def trigger_generate(self):
        if not self.employee_ids:
            raise exceptions.ValidationError("Error! No Employees found")

        recs = self.employee_ids

        for rec in recs:
            data = {"employee_id": rec.id,
                    "month_id": self.month_id.id,
                    "progress": "draft"}

            payslip = self.env["pay.slip"].create(data)
            payslip.generate_payslip()

        self.write({"progress": "generated"})
