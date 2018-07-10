# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Sale order
class SaleOrderDetail(surya.Sarpam):
    _name = "sale.order.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Description", required=True)
    uom_id = fields.Many2one(comodel_name="hos.uom", string="UOM", related="product_id.uom_id")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity", required=True)
    discount = fields.Float(string="Discount")
    tax_id = fields.Many2one(comodel_name="hos.tax", string="Tax")
    freight = fields.Float(string="Freight")
    total_amount = fields.Float(string="Total Amount", readonly=True)
    cgst = fields.Float(string="CGST", readonly=True)
    sgst = fields.Float(string="SGST", readonly=True)
    igst = fields.Float(string="IGST", readonly=True)
    tax_amount = fields.Float(string="Tax Amount", readonly=True)
    discount_amount = fields.Float(string="Discount Amount", readonly=True)
    freight_amount = fields.Float(string="Freight Amount", readonly=True)
    discounted_amount = fields.Float(string="Discounted Amount", readonly=True)
    untaxed_amount = fields.Float(string="Untaxed Value", readonly=True)
    taxed_amount = fields.Float(string="Taxed value", readonly=True)
    order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="invoice_id.progress")
