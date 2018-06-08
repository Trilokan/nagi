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

    name = fields.Char(string="Name")
    patient_id = fields.Many2one(comodel_name="hos.patient")
    image = fields.Binary(string="Image", related="patient_id.image")
    patient_uid = fields.Char(string="Patient ID", related="patient_id.patient_uid")
    age = fields.Char(string="Age", related="patient_id.age")
    email = fields.Char(string="Email", related="patient_id.mobile")
    mobile = fields.Char(string="Mobile", related="patient_id.mobile")
    treatment_history = fields.Html(string="Treatment History")
    report = fields.Html(string="Report")
    date = fields.Date(string="Date")
    symptoms_ids = fields.Many2many(comodel_name="patient.symptoms")
    diagnosis_ids = fields.Many2many(comodel_name="patient.diagnosis")
    diagnosis = fields.Text(string="Diagnosis")
    days = fields.Integer(string="Days")
    medicine_suggestion_ids = fields.One2many(comodel_name="prescription.suggestion",
                                              inverse_name="treatment_id",
                                              string="Medicine")
    lab_suggestion_ids = fields.Many2many(comodel_name="hos.product",
                                          string="Lab Report Required")
    opt_prescription_ids = fields.One2many(comodel_name="opt.prescription",
                                           inverse_name="treatment_id",
                                           string="Prescription")
    ipt_prescription_ids = fields.One2many(comodel_name="ipt.prescription",
                                           inverse_name="treatment_id",
                                           string="Prescription")
    ipt_treatment_ids = fields.One2many(comodel_name="treatment.detail",
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

    @api.multi
    def trigger_add_prescription(self):
        self.opt_prescription_ids.unlink()
        recs = self.medicine_suggestion_ids

        for rec in recs:
            if rec.mark:
                self.env["opt.prescription"].create({"product_id": rec.product_id.id,
                                                     "treatment_id": self.id})

    @api.onchange("diagnosis_ids")
    def get_medicine(self):
        recs = self.diagnosis_ids
        if recs:
            records = []
            record_detail = []

            for rec in recs:
                medicine_ids = rec.medicine_ids
                for medicine_id in medicine_ids:
                    if medicine_id.id not in records:
                        records.append(medicine_id.id)
                        record_detail.append((0, 0, {"product_id": medicine_id.id, "treatment_id": self.id}))
            return {'value': {'medicine_suggestion_ids': record_detail}}
        else:
            return {'value': {'medicine_suggestion_ids': []}}

    @api.multi
    def trigger_report(self):
        pass

    @api.multi
    def trigger_prescription(self):
        view = self.env.ref('nagi.view_ipt_prescription_tree')

        return {
            'name': 'Prescription',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(False, 'tree')],
            'view_id': view.id,
            'res_model': 'ipt.prescription',
            'type': 'ir.actions.act_window',
            'context': self.env.context
        }

    @api.multi
    def trigger_patient_history(self):
        pass


class TreatmentDetail(surya.Sarpam):
    _name = "treatment.detail"

    date = fields.Datetime(string="Date")
    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    description = fields.Text(string="Description")
    comment = fields.Text(string="Comment")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")






