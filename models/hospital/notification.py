# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Notification
class Notification(surya.Sarpam):
    _name = "hos.notification"

    date = fields.Datetime(string="Date")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    message = fields.Text(string="Message")
    comment = fields.Text(string="Comment")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")
