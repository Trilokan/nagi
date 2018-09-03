# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

MEDICINE_TYPE = [("after_food", "After Food"), ("before_food", "Before Food")]


# Prescription
class PatientPrescription(surya.Sarpam):
    _name = "patient.prescription"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    days = fields.Integer(string="Days")
    prescription_ids = fields.One2many(comodel_name="prescription.detail",
                                       inverse_name="prescription_id",
                                       string="Prescription")
    progress = fields.Selection(selection=[("draft", "Draft"), ("confirmed", "Confirmed")],
                                string="Progress",
                                default="draft")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")


class PrescriptionDetail(surya.Sarpam):
    _name = "prescription.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    medicine_type = fields.Selection(selection=MEDICINE_TYPE, string="Medicine Type")
    prescription_id = fields.Many2one(comodel_name="prescription.detail", string="Prescription")
    days = fields.Integer(string="Days")








