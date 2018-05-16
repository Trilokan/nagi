# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Picking
class StockPicking(surya.Sarpam):
    _name = "stock.picking"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference", readonly=True)
    picking_detail = fields.One2many(comodel_name="stock.move",
                                     inverse_name="picking_id",
                                     string="Stock Move")
    picking_type = fields.Selection(selection=PICKING_TYPE, string="Picking Type", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.multi
    def trigger_move(self):
        writter = "Stock Picked by {0}".format(self.env.user.name)
        recs = self.picking_detail

        for rec in recs:
            rec.trigger_move()

        self.write({"progress": "moved", "writter": writter})
