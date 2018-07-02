# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Notes
class Notes(surya.Sarpam):
    _name = "hos.notes"

    date = fields.Datetime(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    message = fields.Text(string="Message", required=True)

    def default_vals_creation(self, vals):
        vals["person_id"] = self.env.user.person_id.id
        return vals
