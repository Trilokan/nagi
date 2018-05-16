# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('approved', 'Approved')]
DAY_TYPE = [('full_day', 'Full Day'), ('half_day', 'Half Day')]


class CompOff(surya.Sarpam):
    _name = "compoff.application"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    co_type = fields.Selection(selection=DAY_TYPE, string="Progress", default="full_day")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        person_id = self.env["hos.person"].search([("person_id", "=", self.env.user.person_id.id)])
        vals["person_id"] = person_id.id
        vals["writter"] = "Leave Application Created by {0}".format(self.env.user.name)
        return vals

    @api.multi
    def trigger_confirmed(self):
        data = {"progress": "confirmed",
                "writter": "Comp-Off Application Confirmed by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        data = {"progress": "cancelled",
                "writter": "Comp-Off Application Cancelled by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        data = {"progress": "approved",
                "writter": "Comp-Off Application approved by {0}".format(self.env.user.name)}

        self.write(data)
