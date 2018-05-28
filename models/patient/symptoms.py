# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Symptoms
class Symptoms(surya.Sarpam):
    _name = "patient.symptoms"
    _inherit = "mail.thread"

    name = fields.Char(string="Symptoms")
    code = fields.Char(string="Code")
