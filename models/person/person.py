# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


class HospitalPerson(surya.Sarpam):
    _name = "hos.person"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", readonly=True)
    name = fields.Char(string="Name", required=True)
    partner_uid = fields.Char(string="Partner UID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")

    is_company = fields.Boolean(string="Is Company", store=True, compute='_get_company_filter')
    is_user = fields.Boolean(string="Is User", store=True, compute='_get_user_filter')
    is_employee = fields.Boolean(string="Is Employee", store=True, compute='_get_employee_filter')
    is_patient = fields.Boolean(string="Is Patient", store=True, compute='_get_patient_filter')
    is_supplier = fields.Boolean(string="Is Supplier")
    is_service = fields.Boolean(string="Is Service")

    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")

    contact_person = fields.Char(sring="Contact Person")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)

    writter = fields.Text(string="Writter", track_visibility="always")

    def _get_company_filter(self):
        for rec in self:
            if self.env["res.company"].search_count([("person_id", "=", rec.id)]):
                rec.is_company = True

    def _get_user_filter(self):
        for rec in self:
            if self.env["res.users"].search_count([("person_id", "=", rec.id)]):
                rec.is_user = True

    def _get_employee_filter(self):
        for rec in self:
            if self.env["hr.employee"].search_count([("person_id", "=", rec.id)]):
                rec.is_employee = True

    def _get_patient_filter(self):
        for rec in self:
            if self.env["hos.patient"].search_count([("person_id", "=", rec.id)]):
                rec.is_patient = True

    @api.model
    def create(self, vals):
        vals["date"] = datetime.now().strftime("%Y-%m-%d"),
        vals["partner_uid"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(HospitalPerson, self).create(vals)

