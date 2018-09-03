# -*- coding: utf-8 -*-

from odoo import fields, models


# Symptoms
class Symptoms(models.Model):
    _name = "patient.symptoms"
    _inherit = "mail.thread"

    name = fields.Char(string="Symptoms")
    code = fields.Char(string="Code")
