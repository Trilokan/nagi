# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

# Product UOM
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class UOM(surya.Sarpam):
    _name = "product.uom"
    _rec_name = "code"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! UOM Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! UOM must be unique')]

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Product UOM Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals

