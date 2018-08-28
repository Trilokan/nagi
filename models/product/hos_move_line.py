# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime
from .. import surya, calculation


# Stock Move Line
class StockMoveLine(models.Model):
    _name = "hos.move.line"

    batch_no = fields.Char(string="Batch No")
    manufactured_date = fields.Date(string="Manufacturing Date")
    expiry_date = fields.Date(string="Expiry Date")
    mrp_rate = fields.Float(string="MRP")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity", default=0)
    move_id = fields.Many2one(comodel_name="hos.move", string="Move Lines")

    @api.model
    def create(self, vals):
        if "quantity" in vals:
            if vals["quantity"] > 0:
                return super(StockMoveLine, self).create(vals)

