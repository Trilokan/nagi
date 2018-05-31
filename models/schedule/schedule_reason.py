# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


# Schedule Reason
class ScheduleReason(surya.Sarpam):
    _name = "hos.schedule.reason"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
