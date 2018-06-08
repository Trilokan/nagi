# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Prescription
class OPTPrescription(surya.Sarpam):
    _name = "opt.prescription"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    days = fields.Integer(string="Days")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")


class IPTPrescription(surya.Sarpam):
    _name = "ipt.prescription"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    prescription_ids = fields.One2many(comodel_name="ipt.prescription.suggestion",
                                       inverse_name="ipt_treatment_id",
                                       string="Prescription")
    progress = fields.Selection(selection=[("draft", "Draft"), ("confirmed", "Confirmed")],
                                string="Progress",
                                default="draft")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")


class IPTPrescriptionSuggestion(surya.Sarpam):
    _name = "ipt.prescription.suggestion"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    days = fields.Integer(string="Days")
    ipt_treatment_id = fields.Many2one(comodel_name="ipt.prescription", string="Prescription")


class PrescriptionSuggestion(surya.Sarpam):
    _name = "prescription.suggestion"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")
    mark = fields.Boolean(string="Select")








