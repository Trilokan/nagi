# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancel")]


# Doctor Availability
class DoctorAvailability(models.Model):
    _name = "hos.doctor.availability"
    _inherit = "mail.thread"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(comodel_name="hos.person",
                                  string="Doctor",
                                  required=True)
    from_time = fields.Datetime(string="From Time",
                                default=datetime.now().strftime("%Y-%m-%d"),
                                required=True)
    till_time = fields.Datetime(string="Till Time",
                                default=datetime.now().strftime("%Y-%m-%d"),
                                required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter")

    def trigger_confirm(self):
        writter = "Availability Cancel By {0}".format(self.env.user.name)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Availability Cancel By {0}".format(self.env.user.name)
        self.write({"progress": "cancel", "writter": writter})

    @api.model
    def create(self, vals):
        vals["writter"] = "Availability created By {0}".format(self.env.user.name)
        return vals
