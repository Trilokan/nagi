# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")]


# Schedule
class HospitalSchedule(surya.Sarpam):
    _name = "hos.schedule"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    scheduler_id = fields.Many2one(comodel_name="hos.person", string="Scheduler", required=True)
    receiver_id = fields.Many2many(comodel_name="hos.person", string="Receiver")
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient")
    from_time = fields.Datetime(string="From Time", required=True)
    till_time = fields.Datetime(string="Till Time", required=True)
    reason = fields.Many2one(comodel_name="hos.schedule.reason", string="Reason")
    comment = fields.Text(string="Comment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter")
    schedule_type_id = fields.Many2one(comodel_name="hos.schedule.type", string="Schedule")
    notify_scheduler = fields.Boolean(string="Notify Scheduler")
    notify_receiver = fields.Boolean(string="Notify Receiver")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        return vals

    @api.multi
    def trigger_cancel(self):
        writter = "Schedule By {0}".format(self.env.user.name)
        self.write({"progress": "cancelled", "writter": writter})
