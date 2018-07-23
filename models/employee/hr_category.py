# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Category
class HRCategory(surya.Sarpam):
    _name = "hr.category"

    name = fields.Char(string="Category", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Employee Category Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals
