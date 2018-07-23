# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Today Menu
class TodayMenu(surya.Sarpam):
    _name = "hos.today.menu"
    _inherit = "mail.thread"

    name = fields.Char(string="Ward", required=True)
    menu = ""
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Ward Created by {0}".format(self.env.user.name)
        return vals
