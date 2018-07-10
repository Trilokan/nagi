# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

# Product Sub Group


class ProductSubGroup(surya.Sarpam):
    _name = "product.sub.group"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    account_id = fields.Many2one(comodel_name="hos.account", string="Account", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Sub-Group Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Sub-Group must be unique')]

    def default_vals_creation(self, vals):
        vals["writter"] = "Product Sub-Group Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.code, record.name)
            result.append((record.id, name))
        return result
