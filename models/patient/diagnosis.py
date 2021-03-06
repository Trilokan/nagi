# -*- coding: utf-8 -*-

from odoo import fields, models


# Diagnosis
class Diagnosis(models.Model):
    _name = "patient.diagnosis"
    _inherit = "mail.thread"

    name = fields.Char(string="Diagnosis")
    code = fields.Char(string="Code")
    medicine_ids = fields.Many2many(comodel_name="hos.product")
