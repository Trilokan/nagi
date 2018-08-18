# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

# Product UOM


class UOM(surya.Sarpam):
    _name = "hos.uom"
    _rec_name = "code"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! UOM Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! UOM must be unique')]
