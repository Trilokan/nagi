# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime

ADMISSION_PROGRESS_INFO = [("draft", "Draft"),
                           ("admitted", "Admitted")]

DISCHARGE_PROGRESS_INFO = [("draft", "Draft"),
                           ("doctor_approved", "Doctor Approved"),
                           ("account_approved", "Account Approve"),
                           ("discharged", "Discharged")]

ADMISSION_STATUS = [("emergency", "Emergency"), ("normal", "Normal")]


# Admission
class Admission(models.Model):
    _name = "hos.admission"
    _inherit = "mail.thread"

    # Admission Detail
    admission_date = fields.Date(string="Admission Date",
                                 default=datetime.now().strftime("%Y-%m-%d"),
                                 required=True)
    admitted_id = fields.Many2one(comodel_name="hos.contact", string="Admitted By")
    admission_status = fields.Selection(selection=ADMISSION_STATUS, string="Admission Status", default="normal")
    admission_progress = fields.Selection(selection=ADMISSION_PROGRESS_INFO,
                                          string="Admission Progress",
                                          default="draft")
    admission_reason = fields.Text(string="Admission Reason")
    admission_attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Admission Attachment")

    # Discharge Detail
    discharge_date = fields.Date(string="Discharge Date")
    discharge_id = fields.Many2one(comodel_name="hos.contact", string="Discharged By")
    discharge_progress = fields.Selection(selection=DISCHARGE_PROGRESS_INFO,
                                          string="Discharge Progress",
                                          default="draft")
    discharge_reason = fields.Text(string="Discharge Reason")
    discharge_attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Discharge Attachment")
    is_doctor_approve = fields.Boolean(string="Doctor Approve")
    is_bill_settled = fields.Boolean(string="Bill Settled")

    # Patient Details
    name = fields.Char(string="Name", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    patient_id = fields.Many2one(comodel_name="hos.patient", string="Patient", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Patient", related="patient_id.person_id")
    patient_uid = fields.Char(string="Patient ID", related="patient_id.patient_uid")

    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile")
    door_no = fields.Char(string="Door No")
    building_name = fields.Char(string="Building Name")
    street_1 = fields.Char(string="Street 1")
    street_2 = fields.Char(string="Street 2")
    locality = fields.Char(string="locality")
    landmark = fields.Char(string="landmark")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State")
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    pin_code = fields.Char(string="Pincode")

    ward_id = fields.Many2one(comodel_name="hos.ward", string="Ward")
    bed_id = fields.Many2one(comodel_name="hos.ward", string="Bed")
    paid_amount = fields.Float(string="Paid Amount")
    others = fields.Text(string="Others")

    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_admitted(self):
        writter = "Admitted by {0}".format(self.env.user.name)
        self.write({"admission_progress": "admitted", "writter": writter})

    def create(self, vals):
        vals["writter"] = "Admission form created by {0}".format(self.env.user.name)
        vals["name"] = self.env['ir.sequence'].next_by_code('hos.ambulance')
        return super(Admission, self).create(vals)

    def reset_to_draft(self, vals):
        writter = "Admission form resetted by {0}".format(self.env.user.name)
        self.write({"admission_progress": "draft", "writter": writter})
        return vals

    def smart_view_patient(self):
        view = self.env.ref('nagi.view_hos_patient_form')

        return {
            'name': 'Patient',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'hos.patient',
            'type': 'ir.actions.act_window',
            'res_id': self.patient_id.id,
            'context': self.env.context
        }

    @api.multi
    def update_patient_info(self):
        if self.patient_id:
            self.email = self.patient_id.email
            self.mobile = self.patient_id.mobile
            self.door_no = self.patient_id.door_no
            self.building_name = self.patient_id.building_name
            self.street_1 = self.patient_id.street_1
            self.street_2 = self.patient_id.street_2
            self.locality = self.patient_id.locality
            self.landmark = self.patient_id.landmark
            self.city = self.patient_id.city
            self.state_id = self.patient_id.state_id.id
            self.country_id = self.patient_id.country_id.id
            self.pin_code = self.patient_id.pin_code
        else:
            raise exceptions.ValidationError("Please select Patient")

    @api.multi
    def trigger_doctor_approve(self):
        writter = "Doctor Approved by {0}".format(self.env.user.name)
        self.write({"discharge_progress": "doctor_approved", "writter": writter})

    @api.multi
    def trigger_account_approve(self):
        writter = "Account approve by {0}".format(self.env.user.name)
        self.write({"discharge_progress": "account_approved", "writter": writter})

    @api.multi
    def trigger_discharge(self):
        writter = "Discharged by {0}".format(self.env.user.name)
        self.write({"discharge_progress": "discharged", "writter": writter})
