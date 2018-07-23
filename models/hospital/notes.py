# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Notes
class Notes(surya.Sarpam):
    _name = "hos.notes"
    _rec_name = "person_id"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    message = fields.Text(string="Message", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Reminder Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        vals["person_id"] = self.env.user.person_id.id
        return vals
