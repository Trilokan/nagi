# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancel")]


# Doctor Availability
class DoctorAvailability(surya.Sarpam):
    _name = "hos.doctor.availability"
    _inherit = "mail.thread"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(comodel_name="hos.person", string="Doctor", required=True)
    from_time = fields.Datetime(string="From Time")
    till_time = fields.Datetime(string="Till Time")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter")

    def default_vals_creation(self, vals):
        writter = "Availability created By {0}".format(self.env.user.name)
        vals["progress"] = "confirmed"
        return vals

    @api.multi
    def trigger_cancel(self):
        writter = "Availability Cancel By {0}".format(self.env.user.name)
        self.write({"progress": "cancel", "writter": writter})
