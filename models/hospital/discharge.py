# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"),
                 ("doctor_approved", "Doctor Approve"),
                 ("account_approved", "Account Approve"),
                 ("discharged", "Discharged")]


# Discharge
class Discharge(surya.Sarpam):
    _name = "hos.discharge"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    person_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    patient_id = fields.Many2one(comodel_name="hos.patient", string="Patient")
    patient_uid = fields.Char(string="Patient ID", related="patient_id.patient_uid")
    reason = fields.Text(string="Reason")
    discharge_date = fields.Date(string="Discharge Date")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    email = fields.Char(string="Email", related="patient_id.email")
    mobile = fields.Char(string="Mobile", related="patient_id.mobile")
    door_no = fields.Char(string="Door No", related="patient_id.door_no")
    building_name = fields.Char(string="Building Name", related="patient_id.building_name")
    street_1 = fields.Char(string="Street 1", related="patient_id.street_1")
    street_2 = fields.Char(string="Street 2", related="patient_id.street_2")
    locality = fields.Char(string="locality", related="patient_id.locality")
    landmark = fields.Char(string="landmark", related="patient_id.landmark")
    city = fields.Char(string="City", related="patient_id.city")
    state_id = fields.Many2one(comodel_name="hos.state", string="State", related="patient_id.state_id")
    country_id = fields.Many2one(comodel_name="res.country", string="Country", related="patient_id.country_id")
    pin_code = fields.Char(string="Pincode", related="patient_id.pin_code")

    is_bill_settled = fields.Boolean(string="Bill Settled")
    is_doctor_approve = fields.Boolean(string="Doctor Approve")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_doctor_approve(self):
        writter = "Doctor Approved by {0}".format(self.env.user.name)
        self.write({"progress": "doctor_approved", "writter": writter})

    @api.multi
    def trigger_account_approve(self):
        writter = "Account approve by {0}".format(self.env.user.name)
        self.write({"progress": "account_approved", "writter": writter})

    @api.multi
    def trigger_discharge(self):
        writter = "Discharged by {0}".format(self.env.user.name)
        self.write({"progress": "discharged", "writter": writter})

    def default_vals_creation(self, vals):
        vals["writter"] = "Discharged Form created by {0}".format(self.env.user.name)
        vals["name"] = self.env['ir.sequence'].next_by_code('hos.discharge')
        return vals



