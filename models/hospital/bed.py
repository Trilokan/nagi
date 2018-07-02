# -*- coding: utf-8 -*-

from odoo import fields, api, http
from .. import surya
from odoo.http import content_disposition, dispatch_rpc, request, \
                      serialize_exception as _serialize_exception

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
STATUS_INFO = [("vacant", "Vacant"), ("occupied", "Occupied")]


# Bed
class Bed(surya.Sarpam):
    _name = "hos.bed"
    _inherit = "mail.thread"

    name = fields.Char(string="Bed", required=True)
    ward_id = fields.Many2one(comodel_name="hos.ward", string="Ward", required=True)
    patient_id = fields.Many2one(comodel_name="hos.person", string="Patient", compute="_get_patient_id")
    occupied_from = fields.Datetime(string="Occupied From", compute="_get_occupied_from")
    status = fields.Selection(selection=STATUS_INFO, string="Status", compute="_get_occupied_status")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def _get_patient_id(self):
        pass

    def _get_occupied_from(self):
        pass

    def _get_occupied_status(self):
        pass

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Bed Created by {0}".format(self.env.user.name)
        return vals
