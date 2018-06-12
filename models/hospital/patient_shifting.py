# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("shifted", "Shifted")]


class PatientShift(surya.Sarpam):
    _name = "patient.shifting"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date")
    name = fields.Char(string="Name", readonly=True)
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Treatment")
    source_id = fields.Many2one(comodel_name="hos.bed", string="From Location")
    destination_id = fields.Many2one(comodel_name="hos.bed", string="Destination Location")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_shifting(self):
        writter = "Patient Shifting by {0}".format(self.env.user.name)
        self.write({"progress": "shifted", "writter": writter})

    def default_vals_creation(self, vals):
        vals["writter"] = "Patient Shifting request Created by {0}".format(self.env.user.name)
        vals["name"] = self.env['ir.sequence'].next_by_code('patient.shifting')
        return vals

