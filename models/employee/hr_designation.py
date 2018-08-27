# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Designation
class HRDesignation(surya.Sarpam):
    _name = "hr.designation"

    name = fields.Char(string="Designation", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)

