# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("opened", "Position Opened"),
                 ("closed", "Position Closed")]


# Vacancy Position
class VacancyPosition(surya.Sarpam):
    _name = "vacancy.position"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    roles = fields.Html(string="Roles & Responsibility")
    experience = fields.Html(string="Experience")
    preference = fields.Html(string="Preference")
    qualification = fields.Html(string="Qualification")
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_open(self):
        data = {"writter": "Vacancy position opened by {0}".format(self.env.user.name),
                "progress": "opened"}

        self.write(data)

    @api.multi
    def trigger_close(self):
        data = {"writter": "Vacancy position closed by {0}".format(self.env.user.name),
                "progress": "closed"}

        self.write(data)

    def default_vals_creation(self, vals):
        if not "date" in vals:
            vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["writter"] = "Vacancy position created by {0}".format(self.env.user.name)

        return vals