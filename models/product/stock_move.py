# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Move
class StockMove(surya.Sarpam):
    _name = "stock.move"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference", readonly=True)
    picking_id = fields.Many2one(comodel_name="stock.picking", string="Stock Picking")
    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", default=0)
    source_location_id = fields.Many2one(comodel_name="hos.location",
                                         string="Source Location",
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="hos.location",
                                              string="Destination location",
                                              required=True)
    picking_type = fields.Selection(selection=PICKING_TYPE, string="Picking Type", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    def get_balance_quantity(self):
        destination_ids = self.env["stock.move"].search([("product_id", "=", self.product_id.id),
                                                         ("destination_location_id", "=", self.source_location_id.id),
                                                         ("progress", "=", "moved")])

        source_ids = self.env["stock.move"].search([("product_id", "=", self.product_id.id),
                                                    ("source_location_id", "=", self.source_location_id.id),
                                                    ("progress", "=", "moved")])
        quantity_in = quantity_out = 0

        for rec in destination_ids:
            quantity_in = quantity_in + rec.quantity

        for rec in source_ids:
            quantity_out = quantity_out + rec.quantity

        balance = quantity_in - quantity_out
        return balance

    @api.multi
    def trigger_move(self):
        writter = "Stock Moved by {0}".format(self.env.user.name)
        quantity = self.get_balance_quantity()

        if self.picking_type in ["internal", "out"]:
            if quantity >= self.quantity:
                self.write({"progress": "moved", "writter": writter})
            else:
                raise exceptions.ValidationError("Error! Product {0} has not enough stock to move".
                                             format(self.product_id.name))
        elif self.picking_type in ["in"]:
            self.write({"progress": "moved", "writter": writter})

    def default_vals_creation(self, vals):
        product_id = vals["product_id"]
        source_location_id = vals["source_location_id"]
        destination_location_id = vals["destination_location_id"]

        warehouse = self.env["hos.warehouse"]
        source = warehouse.search([("product_id", "=", product_id),
                                   ("location_id", "=", source_location_id)])

        destination = warehouse.search([("product_id", "=", product_id),
                                        ("location_id", "=", destination_location_id)])

        if not source:
            warehouse.create({"product_id": product_id,
                              "location_id": source_location_id})

        if not destination:
            warehouse.create({"product_id": product_id,
                              "location_id": destination_location_id})

        return vals
