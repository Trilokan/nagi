# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class HospitalCompany(surya.Sarpam):
    _name = "res.company"
    _inherit = "res.company"

    name = fields.Char(string="Name", required=True)
    company_uid = fields.Char(string="Company ID", readonly=True)
    email = fields.Char(string="E-mail")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")
    person_id = fields.Many2one(comodel_name="hos.person")
    writter = fields.Text(string="Writter", track_visibility="always")

    # Tax
    tax_default_id = fields.Many2one(comodel_name="hos.tax", string="Default Tax")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State")

    # Leave
    leave_lop_id = fields.Many2one(comodel_name="leave.account", string="Loss Of Pay")
    leave_credit_id = fields.Many2one(comodel_name="leave.account", string="Leave Credit")
    leave_debit_id = fields.Many2one(comodel_name="leave.account", string="Leave Debit")

    # Stock
    store_location_id = fields.Many2one(comodel_name="hos.location", string="Location",
                                        help="Default Stores Location; \
                                              Product on creation create a location in warehouse")
    purchase_location_id = fields.Many2one(comodel_name="hos.location", string="Purchase Location",
                                           help="Virtual Purchase location of product")
    pharmacy_location_id = fields.Many2one(comodel_name="hos.location", string="Pharmacy Location",
                                           help="Virtual Pharmacy location of product")
    virtual_location_right = fields.Integer(string="Virtual Location Right",
                                            help="Filter the location in report stock to remove in view")
    virtual_location_left = fields.Integer(string="Virtual Location Left",
                                           help="Filter the location in report stock to remove in view")

    # Account
    sundry_creditor_id = fields.Many2one(comodel_name="hos.account", string="Sundry Creditor")
    sundry_debitor_id = fields.Many2one(comodel_name="hos.account", string="Sundry Debitor")

    # Template
    appointment_order_template = fields.Html(string="Appointment Order Template")
    monthly_attendance_report = fields.Html(string="Monthly Attendance Report")

    def default_vals_creation(self, vals):
        vals["company_uid"] = self.env['ir.sequence'].next_by_code(self._name)

        data = {"name": vals["name"],
                "mobile": vals["mobile"],
                "email": vals.get("email", None),
                "alternate_contact": vals.get("alternate_contact", None),
                "is_company": True,
                "person_uid": vals["company_uid"]}

        person_id = self.env["hos.person"].create(data)

        vals["person_id"] = person_id.id
        vals["writter"] = "{0} is created by {1}".format(vals["name"], self.env.user.name)
        return vals
