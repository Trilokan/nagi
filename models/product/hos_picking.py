# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Picking
class HosPicking(surya.Sarpam):
    _name = "hos.picking"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Partner", readonly=True)
    reference = fields.Char(string="Reference", readonly=True)
    reason = fields.Text(string="Reason")
    picking_detail = fields.One2many(comodel_name="hos.move",
                                     inverse_name="picking_id",
                                     string="Stock Move")
    picking_type = fields.Selection(selection=PICKING_TYPE, string="Picking Type", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    source_location_id = fields.Many2one(comodel_name="hos.location",
                                         string="Source Location",
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="hos.location",
                                              string="Destination location",
                                              required=True)
    writter = fields.Text(string="Writter", track_visibility='always')
    po_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")

    @api.multi
    def trigger_move(self):
        writter = "Stock Picked by {0}".format(self.env.user.name)
        recs = self.picking_detail

        for rec in recs:
            rec.trigger_move()

        self.write({"progress": "moved", "writter": writter})

    def default_vals_creation(self, vals):
        code = "{0}.{1}".format(self._name, vals["picking_type"])
        vals["name"] = self.env['ir.sequence'].next_by_code(code)
        vals["company_id"] = self.env.user.company_id.id
        vals["writter"] = "Created by {0}".format(self.env.user.name)
        return vals

    @api.multi
    def trigger_create_invoice(self):
        data = {}

        invoice_detail = []
        recs = self.picking_detail
        for rec in recs:
            if rec.quantity > 0:

                order_detail = self.env["order.detail"].search([("product_id", "=", rec.product_id.id),
                                                                ("order_id", "=", self.po_id.id)])

                invoice_detail.append((0, 0, {"product_id": rec.product_id.id,
                                              "quantity": rec.quantity,
                                              "unit_price": order_detail.unit_price,
                                              "discount": order_detail.discount,
                                              "tax_id": order_detail.tax_id.id,
                                              "freight": order_detail.freight}))

        if invoice_detail:
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            data["person_id"] = self.person_id.id
            data["reference"] = self.name
            data["invoice_detail"] = invoice_detail
            data["invoice_type"] = 'purchase_bill'
            data["indent_id"] = self.po_id.indent_id.id
            data["quote_id"] = self.po_id.quote_id.id
            data["order_id"] = self.po_id.id
            data["picking_id"] = self.id

            invoice_id = self.env["hos.invoice"].create(data)
            invoice_id.total_calculation()

    @api.multi
    def trigger_create_direct_invoice(self):
        data = {}

        invoice_detail = []
        recs = self.picking_detail
        for rec in recs:
            if rec.quantity > 0:
                invoice_detail.append((0, 0, {"product_id": rec.product_id.id,
                                              "quantity": rec.quantity}))

        if invoice_detail:
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            data["person_id"] = self.person_id.id
            data["reference"] = self.name
            data["invoice_detail"] = invoice_detail
            data["invoice_type"] = 'direct_purchase_bill'
            data["picking_id"] = self.id

            invoice_id = self.env["hos.invoice"].create(data)
            invoice_id.total_calculation()


