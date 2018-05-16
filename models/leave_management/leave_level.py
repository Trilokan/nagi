# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave Leavel

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


class LeaveLevel(surya.Sarpam):
    _name = "leave.level"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")



