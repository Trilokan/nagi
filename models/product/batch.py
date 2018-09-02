# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime
from .. import surya, calculation


# Batch
class Batch(models.TransientModel):
    _name = "hos.batch"

    product_id = fields.Many2one(comodel_name="hos.product",
                                 string="Product",
                                 readonly=True,
                                 default=lambda self: self.env.context.get("product_id", False))
    location_id = fields.Many2one(comodel_name="hos.location",
                                  string="Location",
                                  readonly=True,
                                  default=lambda self: self.env.context.get("location_id", False))
    batch_detail = fields.One2many(comodel_name="hos.batch.detail",
                                   inverse_name="batch_id",
                                   string="Batch Detail",
                                   default=lambda self: self.get_batch())

    def get_batch(self):
        # model = "hos.move.line"
        # source = [("move_id.product_id", "=", self.product_id.id),
        #           ("move_id.source_location_id", "=", self.location_id.id),
        #           ("move_id.progress", "=", "moved")]
        #
        # destination = [("move_id.product_id", "=", self.product_id.id),
        #                ("move_id.destination_location_id", "=", self.location_id.id),
        #                ("move_id.progress", "=", "moved")]
        #
        # record.quantity = self.env["hos.stock"].get_stock(model, source, destination)
        return [(0, 0, {"batch_no": "op",
                                     "manufactured_date": datetime.now().strftime("%Y-%m-%d"),
                                     "expiry_date": datetime.now().strftime("%Y-%m-%d")})]

    def trigger_update(self):
        id = self.env.context.get("active_id", False)
        move_id = self.env["hos.move"].search([("id", "=", id)])

        recs = self.batch_detail

        for rec in recs:
            if rec.check:
                move_id.move_detail.create({"batch_no": rec.batch_no,
                                            "manufactured_date": rec.manufactured_date,
                                            "expiry_date": rec.expiry_date,
                                            "mrp_rate": rec.mrp_rate,
                                            "unit_price": rec.unit_price,
                                            "quantity": rec.quantity})


class BatchDetail(models.TransientModel):
    _name = "hos.batch.detail"

    check = fields.Boolean(string="Check")
    batch_no = fields.Char(string="Batch", readonly=True)
    manufactured_date = fields.Date(string="Manufacturing Date", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)
    mrp_rate = fields.Float(string="MRP", default=0)
    unit_price = fields.Float(string="Unit Price", default=0)
    quantity = fields.Float(string="Quantity", readonly=True)
    batch_id = fields.Many2one(comodel_name="hos.batch", string="Batch")
