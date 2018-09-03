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

    def get_batch_quantity(self, product_id, location_id, batch_no):
        model = "hos.move.line"
        source = [("move_id.product_id", "=", product_id),
                  ("move_id.source_location_id", "=", location_id),
                  ("move_id.progress", "=", "moved"),
                  ("batch_no", "=", batch_no)]

        destination = [("move_id.product_id", "=", product_id),
                       ("move_id.destination_location_id", "=", location_id),
                       ("move_id.progress", "=", "moved"),
                       ("batch_no", "=", batch_no)]

        quantity = self.env["hos.stock"].get_stock(model, source, destination)
        return quantity

    def get_batch(self):

        batch_list = []
        batch_detail = []

        product_id = self.env.context.get("product_id", False)
        location_id = self.env.context.get("location_id", False)

        if product_id and location_id:

            batch_ids = self.env["hos.move.line"].search([("move_id.product_id", "=", product_id),
                                                          ("move_id.destination_location_id", "=", location_id),
                                                          ("move_id.progress", "=", "moved")])

            for rec in batch_ids:
                if rec.batch_no not in batch_list:
                    batch_list.append(rec.batch_no)

            for batch_no in batch_list:
                quantity = self.get_batch_quantity(product_id, location_id, batch_no)
                if quantity > 0:
                    move_id = self.env["hos.move.line"].search([("batch_no", "=", batch_no)], limit=1)

                    data = {"batch_no": move_id.batch_no,
                            "manufactured_date": move_id.manufactured_date,
                            "expiry_date": move_id.expiry_date,
                            "mrp_rate": move_id.mrp_rate,
                            "unit_price": move_id.unit_price,
                            "quantity": quantity}

                    batch_detail.append((0, 0, data))

        return batch_detail

    def trigger_update(self):
        model = self.env.context.get("active_model", False)
        move_id = self.env.context.get("active_id", False)
        move_detail = []

        if model and move_id:
            move_obj = self.env[model].search([("id", "=", move_id)])

            recs = self.batch_detail

            for rec in recs:
                if rec.check:

                    data = {"batch_no": rec.batch_no,
                            "manufactured_date": rec.manufactured_date,
                            "expiry_date": rec.expiry_date,
                            "mrp_rate": rec.mrp_rate,
                            "unit_price": rec.unit_price,
                            "quantity": rec.quantity}

                    move_detail.append((0, 0, data))

            move_obj.move_detail = move_detail


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
