# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Ward
class Ward(surya.Sarpam):
    _name = "hos.ward"
    _inherit = "mail.thread"

    name = fields.Char(string="Ward", required=True)
    bed_detail = fields.One2many(comodel_name="hos.bed",
                                 inverse_name="ward_id",
                                 string="Bed Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "State Created by {0}".format(self.env.user.name)
        return vals
