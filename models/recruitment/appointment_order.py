# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
MARITAL_INFO = [('male', 'Male'), ('female', 'Female')]
GENDER_INFO = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


# Appointment Order
class AppointmentOrder(surya.Sarpam):
    _name = "appointment.order"
    _inherit = "mail.thread"
    _rec_name = "sequence"

    # Resume Details
    resume_id = fields.Many2one(comodel_name="resume.bank", string="Resume", required=True)
    sequence = fields.Char(string="Sequence", readonly=True)

    date = fields.Date(string="Date", required=True)
    image = fields.Binary(string="Image", related="resume_id.image")
    name = fields.Char(string="Name", readonly=True)
    candidate_uid = fields.Char(string="Candidate ID", related="resume_id.candidate_uid")

    # Contact Detail
    email = fields.Char(string="Email", related="resume_id.email")
    mobile = fields.Char(string="Mobile", related="resume_id.mobile")

    # Order Detail
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)
    order_preview = fields.Html(string="Order Preview", readonly=1)
    order = fields.Binary(string="Appointment Order", readonly=1)

    # Salary Details
    salary_detail = fields.One2many(comodel_name="appointment.order.salary",
                                    inverse_name="appointment_id",
                                    string="Salary Detail")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft", track_visibility='always')
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.multi
    def trigger_confirmed(self):
        self.generate_appointment_order()
        writter = "Appointment Order Confirmed by {0}".format(self.env.user.name)
        data = {"progress": "confirmed",
                "writter": writter}

        self.write(data)

    @api.multi
    def view_resume_bank(self):
        view = self.env.ref('nagi.view_resume_bank_form')

        return {
            'name': 'Resume',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'resume.bank',
            'type': 'ir.actions.act_window',
            'res_id': self.resume_id.id,
            'context': self.env.context
        }

    def default_vals_creation(self, vals):
        vals["sequence"] = self.env['ir.sequence'].sudo().next_by_code(self._name)
        vals["writter"] = "Appointment Order generated by {0}".format(self.env.user.name)
        return vals

    def get_address(self):
        address = []

        if self.resume_id.name:
            address.append(self.resume_id.name)
        if self.resume_id.door_no:
            address.append(self.resume_id.door_no)
        if self.resume_id.building_name:
            address.append(self.resume_id.building_name)
        if self.resume_id.street_1:
            address.append(self.resume_id.street_1)
        if self.resume_id.street_2:
            address.append(self.resume_id.street_2)
        if self.resume_id.locality:
            address.append(self.resume_id.locality)
        if self.resume_id.landmark:
            address.append(self.resume_id.landmark)
        if self.resume_id.city:
            address.append(self.resume_id.city)
        if self.resume_id.state_id:
            address.append(self.resume_id.state_id.name)
        if self.resume_id.country_id:
            address.append(self.resume_id.country_id.name)
        if self.resume_id.pin_code:
            address.append(self.resume_id.pin_code)

        address = "<br>".join(address)

        return address

    @api.multi
    def generate_appointment_order(self):
        template = self.env.user.company_id.appointment_order_template

        data = template.format(self.date,
                               self.get_address(),
                               self.position_id.name,
                               self.department_id.name)

        self.order_preview = data


class AppointmentOrderSalary(surya.Sarpam):
    _name = "appointment.order.salary"

    name = fields.Char(string="Name")
    amount = fields.Float(string="Amount")
    appointment_id = fields.Many2one(comodel_name="appointment.order",
                                     string="Appointment Order")

