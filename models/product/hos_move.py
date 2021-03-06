# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime


PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Move
class StockMove(models.Model):
    _name = "hos.move"
    _inherit = "mail.thread"

    date = fields.Date(string="Date",
                       default=datetime.now().strftime("%Y-%m-%d"),
                       required=True)
    name = fields.Char(string="Name", readonly=True)
    reference = fields.Char(string="Reference", readonly=True)
    picking_id = fields.Many2one(comodel_name="hos.picking", string="Stock Picking")
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True,
                                 default=lambda self: self.env.context.get("product_id", False))
    uom_id = fields.Many2one(comodel_name="hos.uom", string="UOM", related="product_id.uom_id")
    is_batch = fields.Boolean(string="Batch", related="product_id.is_batch")
    requested_quantity = fields.Float(string="Requested Quantity", readonly=True,
                                      default=0)
    quantity = fields.Float(string="Approved Quantity", required=True, default=0)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    source_location_id = fields.Many2one(comodel_name="hos.location",
                                         string="Source Location",
                                         default=lambda self: self.env.context.get("source_location_id", False),
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="hos.location",
                                              string="Destination location",
                                              default=lambda self: self.env.context.get("destination_location_id", False),
                                              required=True)
    picking_type = fields.Selection(selection=PICKING_TYPE,
                                    string="Picking Type",
                                    default=lambda self: self.env.context.get("picking_type", False),
                                    required=True)
    move_split = fields.One2many(comodel_name="hos.move",
                                 inverse_name="split_id",
                                 string="Move Split")
    batch_split = fields.One2many(comodel_name="dum.batch",
                                  inverse_name="move_id",
                                  string="Batch Split")
    assert_split = fields.One2many(comodel_name="hos.assert",
                                   inverse_name="move_id",
                                   string="Assert Split")
    split_id = fields.Many2one(comodel_name="hos.move", string="Move")
    batch_id = fields.Many2one(comodel_name="hos.batch", string="Batch")
    manufactured_date = fields.Date(string="Manufacturing Date", related="batch_id.manufactured_date")
    expiry_date = fields.Date(string="Expiry Date", related="batch_id.expiry_date")
    mrp_rate = fields.Float(string="MRP", related="batch_id.mrp_rate")
    unit_price = fields.Float(string="Unit Price", related="batch_id.unit_price")

    is_adjust = fields.Boolean(string="Adjust", related="picking_id.is_adjust")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    def get_balance_quantity(self, location, batch=False):

        source = [("product_id", "=", self.product_id.id),
                  ("source_location_id", "=", location),
                  ("progress", "=", "moved"),
                  ("batch_id", "=", batch)]

        destination = [("product_id", "=", self.product_id.id),
                       ("destination_location_id", "=", location),
                       ("progress", "=", "moved"),
                       ("batch_id", "=", batch)]

        return self.env["hos.stock"].get_stock(source, destination)

    def generate_batch(self):
        for rec in self.batch_split:
            batch = {"product_id": self.product_id.id,
                     "batch_no": rec.batch_no,
                     "manufactured_date": rec.manufactured_date,
                     "expiry_date": rec.expiry_date,
                     "mrp_rate": rec.mrp_rate,
                     "unit_price": rec.unit_price}

            batch_id = self.env["hos.batch"].search([("batch_no", "=", rec.batch_no)])

            if not batch_id.id:
                batch_id = self.env["hos.batch"].create(batch)

            move = {"product_id": self.product_id.id,
                    "source_location_id": self.source_location_id.id,
                    "destination_location_id": self.destination_location_id.id,
                    "picking_type": self.picking_type,
                    "batch_id": batch_id.id,
                    "date": self.date,
                    "reference": self.reference,
                    "quantity": rec.quantity,
                    "split_id": self.id,
                    "progress": "moved"}

            self.env["hos.move"].create(move)

        for rec in self.move_split:
            rec.write({"progress": "moved"})

    @api.multi
    def trigger_move(self):
        self.generate_warehouse()

        writter = "Stock Moved by {0}".format(self.env.user.name)
        location = self.source_location_id.id
        quantity = self.get_balance_quantity(location)

        if self.picking_type in ["internal", "out"]:
            if quantity < self.quantity:
                raise exceptions.ValidationError("Error! Product {0} has not enough stock to move".
                                                 format(self.product_id.name))

            batch_total = 0
            for rec in self.move_split:
                batch_quantity = self.get_balance_quantity(location, rec.batch_id.id)
                batch_total = batch_total + batch_quantity

                if batch_quantity < rec.quantity:
                    raise exceptions.ValidationError("Error! Product {0} with {1} has not enough stock to move".
                                                     format(self.product_id.name, rec.batch_id.batch_no))

        self.generate_batch()

        if self.is_batch and self.quantity:
            if not self.move_split:
                raise exceptions.ValidationError("Error! Product needs batch")

        self.write({"progress": "moved", "writter": writter})

    def generate_warehouse(self):
        warehouse = self.env["hos.warehouse"]
        source = warehouse.search([("product_id", "=", self.product_id.id),
                                   ("location_id", "=", self.source_location_id.id)])

        if not source:
            warehouse.create({"product_id": self.product_id.id,
                              "location_id": self.source_location_id.id})

        destination = warehouse.search([("product_id", "=", self.product_id.id),
                                        ("location_id", "=", self.destination_location_id.id)])

        if not destination:
            warehouse.create({"product_id": self.product_id.id,
                              "location_id": self.destination_location_id.id})

    @api.constrains("requested_quantity", "quantity")
    def check_requested_quantity(self):
        if self.picking_id.picking_category in ["si", "po"]:
            if self.requested_quantity < self.quantity:
                error_msg = "Error! Approved/Store Quantity must be lower than requested quantity"
                raise exceptions.ValidationError(error_msg)

    @api.model
    def create(self, vals):
        code = "{0}.{1}".format(self._name, vals["picking_type"])
        vals["name"] = self.env['ir.sequence'].next_by_code(code)
        vals["writter"] = "Created by {0}".format(self.env.user.name)

        return super(StockMove, self).create(vals)
