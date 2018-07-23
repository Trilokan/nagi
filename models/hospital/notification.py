# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Notification
class Notification(surya.Sarpam):
    _name = "hos.notification"
    _rec_name = "person_id"
    _inherit =  "mail.thread"

    date = fields.Datetime(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    message = fields.Text(string="Message", required=True)
    comment = fields.Text(string="Comment")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Patient")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Reminder Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals
