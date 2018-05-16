# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Contacts

class AppointmentContact(surya.Sarpam):
    _name = "appointment.contact"
    _inherit = "hos.address"

    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")


# Experience
class AppointmentExperience(surya.Sarpam):
    _name = "appointment.experience"

    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")
    name = fields.Char(string="Name", required=True)
    position = fields.Char(string="Position", required=True)
    total_years = fields.Float(string="Total Years", required=True)
    relieving_reason = fields.Text(string="Relieving Reason", required=True)


RESULT_INFO = [("pass", "Pass"), ("fail", "Fail"), ("discontinued", "Discontinued")]


# Qualification
class AppointmentQualification(surya.Sarpam):
    _name = "appointment.qualification"

    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")
    name = fields.Char(string="Name", required=True)
    institution = fields.Char(string="Institution", required=True)
    result = fields.Selection(selection=RESULT_INFO, string='Pass/Fail', required=True)
    enrollment_year = fields.Integer(string="Enrollment Year", required=True)
    completed_year = fields.Integer(string="Completed Year")
