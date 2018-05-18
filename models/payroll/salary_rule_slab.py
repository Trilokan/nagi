# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Salary Rule Slab
SLAB_TYPE = [('fixed', 'Fixed'), ('formula', 'Formula')]


class SalaryRuleSlab(surya.Sarpam):
    _name = "salary.rule.slab"
    _inherit = "mail.thread"

    range_from = fields.Float(string="Range From", required=True)
    range_till = fields.Float(string="Range Till", required=True)
    slab_input = fields.Text(string="Slab Input")
    slab_type = fields.Selection(selection=SLAB_TYPE, string="Slab Type")
    fixed = fields.Float(string="Fixed Amount")
    formula = fields.Text(string="Formula")
    rule_id = fields.Many2one(comodel_name="salary.rule", string="Salary Rule")
    writter = fields.Text(string="Writter", track_visibility='always')

