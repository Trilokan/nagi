# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Journal Reconcile
class JournalReconcile(surya.Sarpam):
    _name = "journal.reconcile"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    is_auto = fields.Boolean(string="Is Auto Reconcile")
    amount = fields.Float(string="Amount")
