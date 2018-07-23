# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"),
                 ("booked", "Booked"),
                 ("cancel", "Cancel"),
                 ("done", "Done")]


# OT Booking
class OTBooking(surya.Sarpam):
    _name = "hos.operation.theater"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date")
    name = fields.Char(string="Name", readonly=True)
    image = fields.Binary(string="Iamge")
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    patient_id = fields.Many2one(comodel_name="hos.patient", string="Patient")
    patient_uid = fields.Char(string="Patient UID", related="patient_id.patient_uid")
    doctor_detail = fields.Many2many(comodel_name="hos.person", string="Doctor Detail")
    operation_id = fields.Many2one(comodel_name="hos.operation", string="Operation", required=True)
    duration = fields.Float(string="Duration")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_book(self):
        writter = "OT Booked by {0}".format(self.env.user.name)
        self.write({"progress": "booked", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        # Cancel Appointment
        self.cancel_appointment()
        writter = "OT Cancel by {0}".format(self.env.user.name)
        self.write({"progress": "cancel", "writter": writter})

    @api.multi
    def trigger_book(self):
        # Create appointment
        self.create_appointment()
        writter = "OT Form Completed by {0}".format(self.env.user.name)
        self.write({"progress": "done", "writter": writter})

    def default_vals_creation(self, vals):
        vals["writter"] = "OT Form created by {0}".format(self.env.user.name)
        vals["name"] = self.env['ir.sequence'].next_by_code('hos.operation.theater')
        return vals

    def create_appointment(self):
        schedule_type_id = self.env["hos.schedule.type"].search([("name", "=", "Operation")])
        recs = self.doctor_detail

        for rec in recs:
            data = {"employee_id": rec.id,
                    "patient_id": self.person_id.id,
                    "time": self.date,
                    "reason": self.operation_id.name,
                    "schedule_type_id": schedule_type_id.id,
                    "reference": self.name}

            self.env["hos.schedule"].create(data)

    def cancel_appointment(self):
        recs = self.env["hos.schedule"].search([("reference", "=", self.name)])
        recs.trigger_cancel()
