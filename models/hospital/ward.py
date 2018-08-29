# -*- coding: utf-8 -*-

from odoo import fields, models
from .. import surya


# Ward
class Ward(models.Model):
    _name = "hos.ward"

    name = fields.Char(string="Ward", required=True)
    bed_detail = fields.One2many(comodel_name="hos.bed",
                                 inverse_name="ward_id",
                                 string="Bed Detail")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
