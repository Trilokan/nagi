# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class PatientShift(surya.Sarpam):
    _name = "patient.shifting"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date")
    name = fields.Char(string="Name")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")
    source_id = fields.Many2one(comodel_name="hos.bed", string="From Location")
    destination_id = fields.Many2one(comodel_name="hos.bed", string="Destination Location")

