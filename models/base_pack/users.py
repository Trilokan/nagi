# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class HospitalUsers(surya.Sarpam):
    _name = "res.users"
    _inherit = "res.users"

    location_id = fields.Many2one(comodel_name="hos.location", string="Location")
    name = fields.Char(string="Name", readonly=True)
    email = fields.Char(string="E-mail", readonly=True)
    mobile = fields.Char(string="Mobile", readonly=True)
    alternate_contact = fields.Char(string="Alternate Contact", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)

    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        person_id = self.env["hos.person"].search([("id", "=", vals["person_id"])])

        vals["name"] = person_id.name
        vals["email"] = person_id.email
        vals["mobile"] = person_id.mobile

        person_id.write({"is_user": True})

        return vals
