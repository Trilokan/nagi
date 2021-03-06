# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


PERSON_TYPE = [("patient", "Patient"),
               ("doctor", "Doctor"),
               ("staff", "Staff"),
               ("driver", "Driver"),
               ("supplier", "Supplier"),
               ("customer", "Customer"),
               ("service", "Service")]


class HospitalPerson(surya.Sarpam):
    _name = "hos.person"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    person_uid = fields.Char(string="Person UID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")

    is_company = fields.Boolean(string="Is Company")
    is_user = fields.Boolean(string="Is User")
    is_employee = fields.Boolean(string="Is Employee")

    person_type = fields.Selection(selection=PERSON_TYPE, string="Person Type")

    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")

    contact_person = fields.Char(sring="Contact Person")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    state_id = fields.Many2one(comodel_name="res.country.state", string="State", required=True,
                               default=lambda self: self.env.user.company_id.state_id.id)

    payable_id = fields.Many2one(comodel_name="hos.account", string="Accounts Payable")
    receivable_id = fields.Many2one(comodel_name="hos.account", string="Accounts Receivable")

    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        if "person_uid" not in vals:
            vals["person_uid"] = self.env["ir.sequence"].next_by_code(self._name)

        account = {}
        account["name"] = vals["name"]
        account["code"] = self.env['ir.sequence'].next_by_code("hos.account")
        account["company_id"] = self.env.user.company_id.id

        # Sundry Creditor
        account["parent_id"] = self.env.user.company_id.sundry_creditor_id.id
        payable_id = self.env["hos.account"].create(account)

        # Sundry Debitor
        account["parent_id"] = self.env.user.company_id.sundry_debitor_id.id
        receivable_id = self.env["hos.account"].create(account)

        vals["payable_id"] = payable_id.id
        vals["receivable_id"] = receivable_id.id

        return vals
