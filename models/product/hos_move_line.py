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
    quantity = fields.Float(string="Quantity", default=0)
    move_id = fields.Many2one(comodel_name="hos.move", string="Move Lines")

    def update_destination_batch(self):
        batch = self.env["hos.batch"]
        product_id = self.move_id.product_id.id
        destination_id = self.move_id.destination_location_id.id

        destination_batch = batch.search([("product_id", "=", product_id),
                                          ("location_id", "=", destination_id),
                                          ("batch_no", "=", self.batch_no)])

        if destination_batch:
            destination_batch.quantity = destination_batch.quantity + self.quantity
        else:
            batch.create({"product_id": product_id,
                          "batch_no": self.batch_no,
                          "manufactured_date": self.manufactured_date,
                          "expiry_date": self.expiry_date,
                          "mrp_rate": self.mrp_rate,
                          "unit_price": self.unit_price,
                          "quantity": self.quantity})

    def update_source_batch(self):
        batch = self.env["hos.batch"]
        product_id = self.move_id.product_id.id
        source_id = self.move_id.source_location_id.id

        source_batch = batch.search([("product_id", "=", product_id),
                                     ("location_id", "=", source_id),
                                     ("batch_no", "=", self.batch_no)])

        if source_batch:
            if source_batch.quantity < self.quantity:
                raise exceptions.ValidationError("Error! Batch stock not available")
            else:
                source_batch.quantity = source_batch.quantity - self.quantity
        else:
            raise exceptions.ValidationError("Error! Batch stock not available")

    @api.model
    def create(self, vals):
        if "quantity" in vals:
            if vals["quantity"] > 0:
                return super(StockMoveLine, self).create(vals)

