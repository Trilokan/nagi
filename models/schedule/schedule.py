# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancel")]


# Schedule
class HospitalSchedule(surya.Sarpam):
    _name = "hos.schedule"
    _inherit = "mail.thread"

    employee_id = fields.Many2one(comodel_name="hos.person", string="Scheduler", required=True)
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    time = fields.Datetime(string="Time", required=True)
    reason = fields.Many2one(comodel_name="hos.schedule.reason", string="Reason")
    comment = fields.Text(string="Comment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter")
    schedule_type_id = fields.Many2one(comodel_name="hos.schedule.type", string="Schedule Type")
    notify_employee = fields.Boolean(string="Notify Scheduler")
    notify_patient = fields.Boolean(string="Notify Receiver")

    reference = fields.Char(string="Reference")

    def default_vals_creation(self, vals):
        writter = "Schedule By {0}".format(self.env.user.name)
        vals["progress"] = "confirmed"
        return vals

    @api.multi
    def trigger_cancel(self):
        writter = "Schedule Cancel By {0}".format(self.env.user.name)
        self.write({"progress": "cancel", "writter": writter})
