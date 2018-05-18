# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

ALLOCATION_TYPE = [("current_month", "Current Month"), ("carry_forward", "Carry Forward")]


# Leave
class HRLeave(surya.Sarpam):
    _name = "hr.leave"

    date = fields.Date(string="Date")
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    leave_level_id = fields.Many2one(comodel_name="leave.level",
                                     string="Leave Level",
                                     related="employee_id.leave_level_id")

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    debit = fields.Float(string="Leave Debit")
    credit = fields.Float(string="Leave Credit")
    leave_order = fields.Integer(string="Order Sequence")
    allocation_type = fields.Selection(selection=ALLOCATION_TYPE,
                                       default="current_month",
                                       string="Allocation Type")









