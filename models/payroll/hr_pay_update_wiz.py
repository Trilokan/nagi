# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, models
from datetime import datetime, timedelta
from .. import surya


# Payslip

PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]
PAY_TYPE = [('allowance', 'Allowance'), ('deduction', 'Deduction')]


class HRPayWiz(models.TransientModel):
    _name = "hr.pay.wizard"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    basic = fields.Float(string="Basic")
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")

    def trigger_pay_update(self):
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        record = self.env["hr.pay"].search([("employee_id", "=", self.employee_id.id)])
        record.write({"basic": self.basic,
                      "structure_id": self.structure_id.id,
                      "writter": writter.id})
