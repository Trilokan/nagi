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
