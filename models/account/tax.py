# -*- coding: utf-8 -*-

from odoo import fields, api
from .. import surya


STATE_INFO = [("inter_state", "Inter state"), ("outer_state", "Outer State")]


# Tax
class Tax(surya.Sarpam):
    _name = "hos.tax"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    state = fields.Selection(selection=STATE_INFO, string="State", required=True)
    value = fields.Float(string="Value", required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Tax Code must be unique')]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{0} - {1}".format(record.name, record.value)
            result.append((record.id, name))
        return result
