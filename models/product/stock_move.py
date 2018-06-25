# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya, calculation

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Move
class StockMove(surya.Sarpam):
    _name = "stock.move"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=lambda self: self._get_date())
    name = fields.Char(string="Name", readonly=True)
    reference = fields.Char(string="Reference", readonly=True)
    picking_id = fields.Many2one(comodel_name="stock.picking", string="Stock Picking")

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    unit_price = fields.Float(string="Unit Price", required=True)
    requested_quantity = fields.Float(string="Requested Quantity", readonly=True, default=0)
    quantity = fields.Float(string="Approved Quantity", required=True, default=0)
    discount = fields.Float(string="Discount", default=0)
    tax_id = fields.Many2one(comodel_name="hos.tax", string="Tax")
    freight = fields.Float(string="Freight", default=0)
    total_amount = fields.Float(string="Total Amount", readonly=True, default=0)
    cgst = fields.Float(string="CGST", readonly=True, default=0)
    sgst = fields.Float(string="SGST", readonly=True, default=0)
    igst = fields.Float(string="IGST", readonly=True, default=0)
    tax_amount = fields.Float(string="Tax Amount", readonly=True, default=0)
    discount_amount = fields.Float(string="Discount Amount", readonly=True, default=0)
    freight_amount = fields.Float(string="Freight Amount", readonly=True, default=0)
    discounted_amount = fields.Float(string="Discounted Amount", readonly=True, default=0)
    untaxed_amount = fields.Float(string="Untaxed Value", readonly=True, default=0)
    taxed_amount = fields.Float(string="Taxed value", readonly=True, default=0)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    source_location_id = fields.Many2one(comodel_name="hos.location",
                                         string="Source Location",
                                         required=True,
                                         default=lambda self: self._get_source_location_id())
    destination_location_id = fields.Many2one(comodel_name="hos.location",
                                              string="Destination location",
                                              required=True,
                                              default=lambda self: self._get_destination_location_id())
    picking_type = fields.Selection(selection=PICKING_TYPE,
                                    string="Picking Type",
                                    required=True,
                                    default=lambda self: self._get_picking_type())
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    def _get_date(self):
        return self.env.context.get("date")

    def _get_picking_type(self):
        return self.env.context.get("picking_type")

    def _get_source_location_id(self):
        return self.env.context.get("source_location_id")

    def _get_destination_location_id(self):
        return self.env.context.get("destination_location_id")

    @api.multi
    def detail_calculation(self):
        if self.requested_quantity < self.quantity:
            raise exceptions.ValidationError("Error! Approved Quantity is more than requested quantity")

        data = calculation.purchase_calculation(self.unit_price,
                                                self.quantity,
                                                self.discount,
                                                self.tax_id.value,
                                                self.freight,
                                                self.tax_id.state)
        self.write(data)

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
            if quantity < self.quantity:
                raise exceptions.ValidationError("Error! Product {0} has not enough stock to move".
                                                 format(self.product_id.name))

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
        vals["company_id"] = self.env.user.company_id.id
        return vals
