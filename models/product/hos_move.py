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
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="hos.uom", string="UOM", related="product_id.uom_id")
    is_batch = fields.Boolean(string="Batch", related="product_id.is_batch")
    requested_quantity = fields.Float(string="Requested Quantity", readonly=True, default=0)
    quantity = fields.Float(string="Approved Quantity", required=True, default=0)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    source_location_id = fields.Many2one(comodel_name="hos.location",
                                         string="Source Location",
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="hos.location",
                                              string="Destination location",
                                              required=True)
    picking_type = fields.Selection(selection=PICKING_TYPE,
                                    string="Picking Type",
                                    required=True)
    move_detail = fields.One2many(comodel_name="hos.move.line",
                                  inverse_name="move_id",
                                  string="Move Detail")
    is_adjust = fields.Boolean(string="Adjust")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    def get_balance_quantity(self, location):
        model = "hos.move"
        search_criteria = [("product_id", "=", self.product_id.id),
                           ("destination_location_id", "=", location),
                           ("progress", "=", "moved")]

        return self.env["hos.stock"].get_stock(model, search_criteria, search_criteria)

    @api.multi
    def trigger_revert(self):
        self.generate_warehouse()

        writter = "Stock Moved reverted by {0}".format(self.env.user.name)
        location = self.destination_location_id.id
        quantity = self.get_balance_quantity(location)

        if self.picking_type in ["in", "internal"]:
            if quantity < self.quantity:
                raise exceptions.ValidationError("Error! Product {0} has not enough stock to move".
                                                 format(self.product_id.name))

        self.write({"progress": "draft", "writter": writter})

    @api.multi
    def trigger_move(self):
        self.generate_warehouse()
        self.check_batch()

        writter = "Stock Moved by {0}".format(self.env.user.name)
        location = self.source_location_id.id
        quantity = self.get_balance_quantity(location)

        if self.picking_type in ["internal", "out"]:
            if quantity < self.quantity:
                raise exceptions.ValidationError("Error! Product {0} has not enough stock to move".
                                                 format(self.product_id.name))

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

    def check_batch(self):
        if self.product_id.is_batch:
            if not self.move_detail:
                raise exceptions.ValidationError("Error! Product need Batch need")

            move_detail_qty = 0
            for move_detail in self.move_detail:
                move_detail_qty = move_detail_qty + move_detail.quantity

            if move_detail_qty != self.quantity:
                raise exceptions.ValidationError("Error! Batch Quantity must be equal")

    @api.constrains("requested_quantity", "quantity")
    def check_requested_quantity_greater_than_quantity(self):
        for rec in self:
            if rec.picking_id.po_id:
                if rec.requested_quantity < rec.quantity:
                    raise exceptions.ValidationError("Error! Approved Quantity must be lower than requested quantity")

    @api.model
    def create(self, vals):
        code = "{0}.{1}".format(self._name, vals["picking_type"])
        vals["name"] = self.env['ir.sequence'].next_by_code(code)
        vals["writter"] = "Created by {0}".format(self.env.user.name)

        return super(StockMove, self).create(vals)

    @api.multi
    def open_batch_wizard(self):
        view = self.env.ref('nagi.view_hos_batch_form')

        context = self.env.context.copy()
        context.update({"product_id": self.product_id.id,
                        "location_id": self.source_location_id.id})

        return {
            'name': 'Resume',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'hos.batch',
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new'
        }