# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

RECONCILE_TYPE = [("manual", "Manual"), ("automatic", "Automatic")]


# Leave Reconcile
class LeaveReconcile(surya.Sarpam):
    _name = "leave.reconcile"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    reconcile_type = fields.Selection(selection=RECONCILE_TYPE, string="Type")


