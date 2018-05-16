# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class HospitalLocation(surya.Sarpam):
    _name = "hos.location"
    _inherit = "mail.thread"
    _rec_name = "code"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", compute="_get_code")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)

    location_right = fields.Integer(string="Parent Right", required=True)
    location_left = fields.Integer(string="Parent Left", required=True)

    progress = fields.Selection(selection=PROGRESS_INFO, string="progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Group Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Group must be unique')]

    def _get_code(self):
        for record in self:
            recs = self.env["hos.location"].search([("location_left", "<=", record.location_left),
                                                    ("location_right", ">=", record.location_right)])

            recs = recs.sorted(key=lambda r: r.location_left)

            name = ""
            for rec in recs:
                name = "{0}{1}/".format(name, rec.name)

            record.code = name

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Product Location Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals