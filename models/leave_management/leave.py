# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave
PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('approved', 'Approved')]


class Leave(surya.Sarpam):
    _name = "leave.application"
    _inherit = "mail.thread"

    from_date = fields.Date(string="From Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        person_id = self.env["hos.person"].search([("person_id", "=", self.env.user.person_id.id)])
        vals["person_id"] = person_id.id
        vals["writter"] = "Leave Application Created by {0}".format(self.env.user.name)
        return vals

    @api.multi
    def trigger_confirmed(self):
        data = {"progress": "confirmed",
                "writter": "Leave Application Confirmed by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        data = {"progress": "cancelled",
                "writter": "Leave Application Cancelled by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        data = {"progress": "approved",
                "writter": "Leave Application Approved by {0}".format(self.env.user.name)}

        self.write(data)
