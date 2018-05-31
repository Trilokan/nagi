# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya


# Schedule Type
class ScheduleType(surya.Sarpam):
    _name = "hos.schedule.type"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
