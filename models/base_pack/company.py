# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class HospitalCompany(surya.Sarpam):
    _name = "res.company"
    _inherit = ["res.company", "mail.thread"]

    location_id = fields.Many2one(comodel_name="hos.location", string="Location")
    purchase_location_id = fields.Many2one(comodel_name="hos.location", string="Purchase Location")
    virtual_location_right = fields.Integer(string="Virtual Location Right")
    virtual_location_left = fields.Integer(string="Virtual Location Left")

    default_product_in = fields.Integer(string="default IN")
    default_product_out = fields.Integer(string="default OUT")

    name = fields.Char(string="Name", required=True)
    company_uid = fields.Char(string="Company ID", readonly=True)
    email = fields.Char(string="E-mail")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")
    person_id = fields.Many2one(comodel_name="hos.person")
    lop_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    appointment_order_template = fields.Html(string="Appointment Order Template")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["company_uid"] = self.env['ir.sequence'].next_by_code(self._name)

        data = {"name": vals["name"],
                "mobile": vals["mobile"],
                "email": vals.get("email", None),
                "alternate_contact": vals.get("alternate_contact", None),
                "person_uid": vals["company_uid"],
                "is_company": True}

        person_id = self.env["hos.person"].create(data)

        vals["person_id"] = person_id.id
        vals["writter"] = "{0} is created by {1}".format(vals["name"], self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals
