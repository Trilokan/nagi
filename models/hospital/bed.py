# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Bed
class Bed(surya.Sarpam):
    _name = "hos.bed"
    _inherit = "mail.thread"

    name = fields.Char(string="Bed", required=True)
    ward_id = fields.Many2one(comodel_name="hos.ward", string="Ward", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "State Created by {0}".format(self.env.user.name)
        return vals
