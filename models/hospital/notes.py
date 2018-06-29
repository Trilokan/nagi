# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Notes
class Notes(surya.Sarpam):
    _name = "hos.notes"

    date = fields.Datetime(string="Date")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    message = fields.Text(string="Message")

