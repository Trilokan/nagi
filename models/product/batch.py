# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime
from .. import surya, calculation


# Batch
class Batch(models.Model):
    _name = "hos.batch"

    batch_no = fields.Char(string="Batch", readonly=True)
    warehouse_id = fields.Many2one(comodel_name="hos.warehouse", string="Warehouse")
    quantity = fields.Float(string="Quantity", compute="_get_stock")

    def _get_stock(self):
        for record in self:
            model = "hos.move.line"
            source = [("batch_no", "=", record.batch_no),
                      ("move_id.product_id", "=", record.warehouse_id.product_id.id),
                      ("move_id.source_location_id", "=", record.warehouse_id.location_id.id),
                      ("move_id.progress", "=", "moved")]

            destination = [("batch_no", "=", record.batch_no),
                           ("move_id.product_id", "=", record.warehouse_id.product_id.id),
                           ("move_id.destination_location_id", "=", record.warehouse_id.location_id.id),
                           ("move_id.progress", "=", "moved")]

            record.quantity = self.env["hos.stock"].get_stock(model, source, destination)

