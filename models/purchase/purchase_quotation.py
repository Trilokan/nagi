
# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class PurchaseQuote(surya.Sarpam):
    _name = "purchase.quote"
    _rec_name = "indent_id"
    _inherit = "mail.thread"

    date = fields.Date(string='Date', readonly=True)
    indent_id = fields.Many2one(comodel_name='purchase.indent',
                                string='Purchase Indent',
                                readonly=True)
    quote_comparision = fields.Binary(string="Quote Comparision", readonly=True)
    quote_detail = fields.One2many(comodel_name='quote.detail',
                                   inverse_name='quote_id',
                                   string='Quotation Details')
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility='always')

    _sql_constraints = [('unique_indent', 'unique (indent_id)',
                         'Error! indent should not be repeated')]

    def default_vals_creation(self, vals):
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["company_id"] = self.env.user.company_id.id
        return vals

    @api.multi
    def trigger_order_creation(self):
        recs = self.quote_detail

        for rec in recs:
            rec.order_detail_creation()

        person_id = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "Order generated by {0}".format(person_id.name)

        self.write({"writter": writter})


class QuoteDetail(surya.Sarpam):
    _name = 'quote.detail'
    _description = 'Quotation Details'

    product_id = fields.Many2one(comodel_name='hos.product', string='Product', readonly=True)
    uom_id = fields.Many2one(comodel_name='product.uom', string='UOM', related="product_id.uom_id")
    quantity = fields.Float(string='Quantity', readonly=True)
    vendor_ids = fields.Many2many(comodel_name='hos.person', string='Vendors')
    po_detail = fields.One2many(comodel_name='order.detail',
                                inverse_name='quote_detail_id',
                                string='Purchase Order Detail')
    comment = fields.Text(string='Comment')
    quote_id = fields.Many2one(comodel_name='purchase.quote', string='Quotation')

    @api.multi
    def order_detail_creation(self):
        for vendor in self.vendor_ids:
            order = self.env["purchase.order"].search([("indent_id", "=", self.quote_id.indent_id.id),
                                                       ("vendor_id", "=", vendor.id)])

            if order:
                order_detail = self.env["order.detail"].search([("product_id", "=", self.product_id.id),
                                                                ("order_id", "=", order.id)])

                if not order_detail:
                    self.env["order.detail"].create({"vendor_id": vendor.id,
                                                     "product_id": self.product_id.id,
                                                     "uom_id": self.uom_id.id,
                                                     "requested_quantity": self.quantity,
                                                     "quote_detail_id": self.id,
                                                     "tax_id": self.env.user.company_id.tax_default_id.id,
                                                     "order_id": order.id})

            else:
                order_detail = [(0, 0, {"vendor_id": vendor.id,
                                        "product_id": self.product_id.id,
                                        "uom_id": self.uom_id.id,
                                        "quote_detail_id": self.id,
                                        "requested_quantity": self.quantity})]

                data = {"indent_id": self.quote_id.indent_id.id,
                        "vendor_id": vendor.id,
                        "quote_id": self.quote_id.id,
                        "order_detail": order_detail}

                self.env["purchase.order"].create(data)
