# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya

PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("completed", "Completed")]

STATUS_INFO = [("draft", "Draft"), ("completed", "Completed")]
BILL_INFO = [("not_paid", "Not Paid"), ("partially_paid", "Partially Paid"), ("fully_paid", "Fully Paid")]


class LabForm(surya.Sarpam):
    _name = "lab.form"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    lab_form_detail = fields.One2many(comodel_name="lab.form.detail",
                                      inverse_name="lab_form_id",
                                      string="Lab Form Detail")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    bill_status = fields.Selection(selection=BILL_INFO, string="Bill Status", default="not_paid", readonly=True)

    report = fields.Html(string="Report")


class LabFormDetail(surya.Sarpam):
    _name = "lab.form.detail"

    test_id = fields.Many2one(comodel_name="lab.test", string="Test", required=True)
    status = fields.Selection(selection=STATUS_INFO, string="Status", default="draft")
    lab_form_id = fields.Many2one(comodel_name="lab.form", string="Lab Form")
    lab_form_test_detail = fields.One2many(comodel_name="lab.form.detail.test",
                                           inverse_name="detail_id",
                                           string="Lab Form Test Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="lab_form_id.progress")
    report = fields.Html(string="Report")


class LabTestFormTestDetail(surya.Sarpam):
    _name = "lab.form.detail.test"

    name = fields.Char(string="Name", readonly=True)
    value = fields.Char(string="Value")
    detail_id = fields.Many2one(comodel_name="lab.form.detail", string="Test Detail")
