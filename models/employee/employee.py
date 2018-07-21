# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class Employee(surya.Sarpam):
    _name = "hr.employee"
    _inherit = ["hr.account.info", "hr.personal.info", "hos.address", "mail.thread"]

    name = fields.Char(string="Name", required=True)
    employee_uid = fields.Char(string="Employee ID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")

    # Contact
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")

    # HR Details
    doj = fields.Date(string="Date of Joining", required=False)
    date_of_relieving = fields.Date(string="Date of Relieving")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation")
    reporting_to_id = fields.Many2one(comodel_name="hr.employee", string="Reporting To")
    employee_category_id = fields.Many2one(comodel_name="hr.category", string="Employee Category")
    qualification_ids = fields.One2many(comodel_name="hr.qualification",
                                        inverse_name="employee_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="hr.experience",
                                     inverse_name="employee_id",
                                     string="Experience")
    leave_ids = fields.One2many(comodel_name="hr.leave",
                                inverse_name="employee_id",
                                string="Leave")

    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")
    leave_account_id = fields.Many2one(comodel_name="leave.account", string="Leave Account")
    user_id = fields.Many2one(comodel_name="res.users", string="User")

    # Filter Details
    is_doctor = fields.Boolean(string="Doctor")
    is_nurse = fields.Boolean(string="Nurse")
    is_contract = fields.Boolean(string="Contract")
    is_admin_staff = fields.Boolean(string="Admin Staff")
    is_ambulance_driver = fields.Boolean(string="Ambulance Driver")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    person_id = fields.Many2one(comodel_name="hos.person", string="Partner")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)

    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["employee_uid"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["company_id"] = self.env.user.company_id.id

        leave_account = {"name": "{0} leave account".format(self.name),
                         "code": "111"}

        leave_account_id = self.env["leave.account"].create(leave_account)

        data = {"name": vals["name"],
                "mobile": vals["mobile"],
                "email": vals.get("email", None),
                "alternate_contact": vals.get("alternate_contact", None),
                "company_id": vals["company_id"],
                "person_uid": vals["employee_uid"],
                "is_patient": True}

        person_id = self.env["hos.person"].create(data)
        vals["person_id"] = person_id.id
        vals["leave_account_id"] = leave_account_id.id
        vals["writter"] = "Employee record created by {0}".format(self.env.user.name)

        return vals
