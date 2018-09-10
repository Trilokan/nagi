# -*- coding: utf-8 -*-

from odoo import fields, models


# Category
class ProductCategory(models.Model):
    _name = "hos.product.category"
    _description = "Lab-test/Product/Ambulance/Treatment"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Product Category Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Product Category must be unique')]
