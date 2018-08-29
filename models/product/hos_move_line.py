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

    def check_batch(self, vals):
        warehouse = self.env["hos.warehouse"]
        batch = self.env["hos.batch"]

        move_id = self.env["hos.move"].search([("id", "=", vals["move_id"])])
        source = warehouse.search([("product_id", "=", move_id.product_id.id),
                                   ("location_id", "=", move_id.source_location_id.id)])

        source_batch = batch.search([("warehouse_id", "=", source.id),
                                     ("batch_no", "=", vals["batch_no"])])

        if not source_batch:
            batch.create({"warehouse_id": source.id,
                          "batch_no": vals["batch_no"]})

        destination = warehouse.search([("product_id", "=", move_id.product_id.id),
                                        ("location_id", "=", move_id.destination_location_id.id)])

        destination_batch = batch.search([("warehouse_id", "=", destination.id),
                                          ("batch_no", "=", vals["batch_no"])])

        if not destination_batch:
            batch.create({"warehouse_id": destination.id,
                          "batch_no": vals["batch_no"]})

    @api.model
    def create(self, vals):
        if "quantity" in vals:
            if vals["quantity"] > 0:
                self.check_batch(vals)
                return super(StockMoveLine, self).create(vals)

