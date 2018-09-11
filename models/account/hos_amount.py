# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _


class Amount(models.Model):
    _name = 'hos.amount'

    name = fields.Char(string="List", required=True)
    sequence = fields.Integer(string="Sequence", required=True)
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
