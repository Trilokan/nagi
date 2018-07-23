# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


# Operation
class Operation(surya.Sarpam):
    _name = "hos.operation"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Operation Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals
