# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime
from .. import surya, calculation


# Batch
class Batch(models.Model):
    _name = "hos.batch"
    _rec_name = "batch_no"

    """Always shows current stock only 
       Created from stock move line when moved"""

    batch_no = fields.Char(string="Batch", readonly=True)
    manufactured_date = fields.Date(string="Manufacturing Date", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)
    mrp_rate = fields.Float(string="MRP", default=0)
    unit_price = fields.Float(string="Unit Price", default=0)
    quantity = fields.Float(string="Quantity", readonly=True)
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", readonly=True)
    location_id = fields.Many2one(comodel_name="hos.location", string="Location", readonly=True)

