# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Category
class ProductCategory(surya.Sarpam):
    _name = "product.category"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Group Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Group must be unique')]

    def default_vals_creation(self, vals):
        vals["writter"] = "Product Group Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals