# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions


# Leave Level
class LeaveLevel(models.Model):
    _name = "leave.level"

    name = fields.Char(string="Level", required=True)
    code = fields.Char(string="Code", required=True)
