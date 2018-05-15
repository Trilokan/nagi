# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class HospitalCompany(surya.Sarpam):
    _name = "res.company"
    _inherit = "res.company"

    # location_id = fields.Many2one(comodel_name="hos.location", string="Location")
    # virtual_location_ids = fields.One2many(comodel_name="hos.location", string="Virtual Location")
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="E-mail")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")
    person_id = fields.Many2one(comodel_name="hos.person")

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
