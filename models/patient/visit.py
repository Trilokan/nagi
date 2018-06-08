# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class DoctorVisit(surya.Sarpam):
    _name = "doctor.visit"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date")
    person_id = fields.Many2one(comodel_name="patient.treatment", string="Person")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")

