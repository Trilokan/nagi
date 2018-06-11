# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("cancelled", "Cancelled"),
                 ("transfer_completed", "Transfer Completed")]
JOURNEY_INFO = [("hospital_transfer", "Hospital Transfer"),
                ("admission", "Admission"),
                ("discharge", "Discharge")]


# Ambulance
class Ambulance(surya.Sarpam):
    _name = "hos.ambulance"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)

    source_location = fields.Text(string="Source Location")
    destination_location = fields.Text(string="Destination Location")

    from_time = fields.Datetime(string="From Time")
    till_time = fields.Datetime(string="Till Time")

    driver_id = fields.Many2one(comodel_name="hos.person", string="Driver")
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    staff_id = fields.Many2one(comodel_name="hos.person", string="Staff")

    driver_mobile = fields.Char(string="Driver Contact")
    patient_mobile = fields.Char(string="Patient Contact")

    journey_type = fields.Selection(selection=JOURNEY_INFO, string="Journey Type")

    distance = fields.Float(string="Distance (KM)")
    time_taken = fields.Float(string="Time Taken (Hrs)", readonly=True)
    total_cost = fields.Float(string="Total Cost")
    is_paid = fields.Boolean(string="Is Paid", readonly=True)

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(strng="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Ambulance confirmed by {0}".format(self.env.user.name)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Ambulance cancelled by {0}".format(self.env.user.name)
        self.write({"progress": "cancelled", "writter": writter})

    @api.multi
    def trigger_transfer_completed(self):
        # create bill in invoice
        writter = "Ambulance transfer verified by {0}".format(self.env.user.name)
        self.write({"progress": "transfer_completed", "writter": writter})

    @api.multi
    def trigger_sms(self):
        # Generate SMS to the driver and staff
        pass

    @api.multi
    def trigger_whatsapp(self):
        # Generate Whatsapp to the driver and staff
        pass


