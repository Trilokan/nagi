# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime
from .. import surya


# Notes
class Notes(models.Model):
    _name = "hos.notes"
    _rec_name = "person_id"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date",
                           default=datetime.now().strftime("%Y-%m-%d"),
                           required=True)
    person_id = fields.Many2one(comodel_name="hos.person",
                                default=lambda self: self.env.user.person_id.id,
                                string="Person",
                                readonly=True)
    message = fields.Text(string="Message", required=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
