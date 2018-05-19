# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class HospitalCompany(surya.Sarpam):
    _name = "res.company"
    _inherit = "res.company"

    location_id = fields.Many2one(comodel_name="hos.location", string="Location")
    virtual_location_right = fields.Integer(string="Virtual Location Right")
    virtual_location_left = fields.Integer(string="Virtual Location Left")

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="E-mail")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")
    person_id = fields.Many2one(comodel_name="hos.person")
    lop_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    appointment_order_template = fields.Html(string="Appointment Order Template")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        data = {"name": vals["name"],
                "mobile": vals["mobile"],
                "email": vals.get("email", None),
                "alternate_contact": vals.get("alternate_contact", None),
                "is_company": True}
        person_id = self.env["hos.person"].create(data)
        vals["person_id"] = person_id.id

        return vals
