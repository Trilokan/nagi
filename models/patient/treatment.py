# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Treatment
class Treatment(surya.Sarpam):
    _name = "patient.treatment"
    _inherit = "mail.thread"

    patient_id = fields.Many2one(comodel_name="patient.patient")
    patient_uid = ""
    age = ""
    treatment_history = ""
    report = ""
    date = ""

    symptoms_id = fields.Many2many(comodel_name="patient.symptoms")
    diagnosis_id = fields.Many2many(comodel_name="patient.diagnosis")
    opt_treatment_id = fields.One2many(comodel_name="product.product", string="Medicine")

