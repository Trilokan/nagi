# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya, calculation


PROGRESS_INFO = [('draft', 'Draft'),
                 ('qa', 'Quotation Approved'),
                 ('cancel', 'Cancel')]


class PurchaseDetail(surya.Sarpam):
    _name = 'purchase.detail'
    _description = 'Purchase Order Detail'

    vendor_id = fields.Many2one(comodel_name='hos.person', string='Vendor', readonly=True)
    product_id = fields.Many2one(comodel_name='hos.product', string='Product', related='quote_detail_id.product_id')
    uom_id = fields.Many2one(comodel_name='hos.uom', string='UOM', related='quote_detail_id.uom_id')
    requested_quantity = fields.Float(string='Requested Quantity', default=0, readonly=True)
    accepted_quantity = fields.Float(string='Accepted Quantity', default=0)
    unit_price = fields.Float(string='Unit Price', default=0)

    discount = fields.Float(string='Discount', default=0)
    freight = fields.Float(string='Freight', default=0)
    discount_amount = fields.Float(string='Discount Amount', default=0, readonly=True)
    discounted_amount = fields.Float(string='Discounted Amount', readonly=True, help='Amount after discount')
    tax_id = fields.Many2one(comodel_name='hos.tax', string='Tax', required=True)
    igst = fields.Float(string='IGST', default=0, readonly=True)
    cgst = fields.Float(string='CGST', default=0, readonly=True)
    sgst = fields.Float(string='SGST', default=0, readonly=True)
    tax_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount', default=0, readonly=True)
    untaxed_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    freight_amount = fields.Float(string='Freight Amount', default=0, readonly=True)
    total_amount = fields.Float(string='Total', default=0, readonly=True)
    quote_detail_id = fields.Many2one(comodel_name='quote.detail', string='Quotation')
    order_id = fields.Many2one(comodel_name='purchase.order', string='Purchase Order')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='order_id.progress')

    @api.multi
    def detail_calculation(self):
        if self.requested_quantity < self.accepted_quantity:
            raise exceptions.ValidationError("Error! Approved Quantity is more than requested quantity")

        data = calculation.purchase_calculation(self.unit_price,
                                                self.accepted_quantity,
                                                self.discount,
                                                self.tax_id.value,
                                                self.freight,
                                                self.tax_id.state)
        self.write(data)
