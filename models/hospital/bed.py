# -*- coding: utf-8 -*-

from odoo import fields, models

STATUS_INFO = [("vacant", "Vacant"), ("occupied", "Occupied")]


# Bed
class Bed(models.Model):
    _name = "hos.bed"

    name = fields.Char(string="Bed", required=True)
    ward_id = fields.Many2one(comodel_name="hos.ward", string="Ward", required=True)
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient", compute="_get_patient_id")
    occupied_from = fields.Datetime(string="Occupied From", compute="_get_occupied_from")
    status = fields.Selection(selection=STATUS_INFO, string="Status", compute="_get_occupied_status")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    def _get_patient_id(self):
        pass

    def _get_occupied_from(self):
        pass

    def _get_occupied_status(self):
        pass
