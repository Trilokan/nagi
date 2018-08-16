# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PATIENT_TYPE = [("out_patient", "Out Patient"), ("in_patient", "In Patient")]
PROGRESS_INFO = [("on_process", "Treatment On Going"), ("discharged", "Discharged")]


# Treatment
class Treatment(surya.Sarpam):
    _name = "patient.treatment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    patient_id = fields.Many2one(comodel_name="hos.patient")
    image = fields.Binary(string="Image", related="patient_id.image")
    patient_uid = fields.Char(string="Patient ID", related="patient_id.patient_uid")
    age = fields.Char(string="Age", related="patient_id.age")
    email = fields.Char(string="Email", related="patient_id.mobile")
    mobile = fields.Char(string="Mobile", related="patient_id.mobile")

    # Treatment History
    treatment_history = fields.Html(string="Treatment History")
    report = fields.Html(string="Report")

    symptoms_ids = fields.Many2many(comodel_name="patient.symptoms")
    diagnosis_ids = fields.Many2many(comodel_name="patient.diagnosis")
    symptoms = fields.Text(string="Diagnosis")
    diagnosis = fields.Text(string="Diagnosis")
    is_add_symptoms = fields.Boolean(string="Add Symptoms")
    is_add_diagnosis = fields.Boolean(string="Add Diagnosis")

    prescription_ids = fields.One2many(comodel_name="patient.prescription",
                                       inverse_name="treatment_id",
                                       string="Prescription")
    treatment_ids = fields.One2many(comodel_name="treatment.detail",
                                    inverse_name="treatment_id",
                                    string="Treatment")
    doctor_visit_ids = fields.One2many(comodel_name="doctor.visit",
                                       inverse_name="treatment_id",
                                       string="Doctor Visit")
    ward_id = fields.Many2one(comodel_name="hos.ward", string="Ward")
    bed_id = fields.Many2one(comodel_name="hos.bed", string="Bed")
    notification_ids = fields.One2many(comodel_name="hos.notification",
                                       inverse_name="treatment_id",
                                       string="Notification")

    patient_type = fields.Selection(selection=PATIENT_TYPE, string="Type")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="on_process")


class TreatmentDetail(surya.Sarpam):
    _name = "treatment.detail"

    date = fields.Datetime(string="Date")
    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    comment = fields.Text(string="Comment")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")






