# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime
from .. import surya, calculation


# Stock Move Line
class StockMoveLine(models.Model):
    _name = "hos.move.line"

    batch_no = fields.Char(string="Batch No", required=True)
    manufactured_date = fields.Date(string="Manufacturing Date", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)
    mrp_rate = fields.Float(string="MRP", default=0)
    unit_price = fields.Float(string="Unit Price", default=0)
    quantity = fields.Float(string="Quantity", default=0, required=True)
    move_id = fields.Many2one(comodel_name="hos.move", string="Move Lines")

    @api.model
    def create(self, vals):
        if vals["quantity"] > 0:
            return super(StockMoveLine, self).create(vals)

