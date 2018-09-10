# -*- coding: utf-8 -*-

from odoo import fields, api, models


# Tax
class Tax(models.Model):
    _name = "hos.tax"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    rate = fields.Float(string="rate", required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Tax Code must be unique')]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{0} - {1}".format(record.name, record.rate)
            result.append((record.id, name))
        return result
