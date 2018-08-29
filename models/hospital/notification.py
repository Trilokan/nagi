# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime


# Notification
class Notification(models.Model):
    _name = "hos.notification"
    _rec_name = "person_id"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date",
                           default=datetime.now().strftime("%Y-%m-%d"),
                           required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    message = fields.Text(string="Message", required=True)
    comment = fields.Text(string="Comment")
    treatment_id = fields.Many2one(comodel_name="patient.treatment", string="Patient")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

