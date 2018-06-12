# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


VOUCHER_INFO = [("payment_in", "Payment In"), ("payment_out", "Payment Out")]
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Voucher
class Voucher(surya.Sarpam):
    _name = "hos.voucher"

    person_id = fields.Many2one(comodel_name="hos.person", string="Person")
    admission_id = fields.Many2one(comodel_name="hos.admission", string="Admission")
    name = fields.Char(string="Name", readonly=True)
    amount = fields.Float(string="Amount")
    voucher_type = fields.Selection(selection=VOUCHER_INFO, string="Type")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Type")
