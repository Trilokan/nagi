# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api, _
from .. import calculation

PROGRESS_INFO = [("draft", "Draft"), ("confirm", "Confirm"), ("cancel", "Cancel")]


# Sale order
class SaleOrderDetail(models.Model):
    _name = "sale.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Item", required=True)
    uom_id = fields.Many2one(comodel_name="hos.uom", string="UOM", related="product_id.uom_id")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity", required=True)
    discount = fields.Float(string="Discount")
    tax_id = fields.Many2one(comodel_name="hos.tax", string="Tax")
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
    batch_detail = fields.One2many(comodel_name="sale.batch",
                                   inverse_name="sale_detail_id",
                                   string="Batch")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    @api.multi
    def detail_calculation(self):
        if self.quantity < 0:
            raise exceptions.ValidationError("Error! please check quantity")

        data = calculation.purchase_calculation(self.unit_price,
                                                self.quantity,
                                                self.discount,
                                                self.tax_id.value,
                                                self.tax_id.state)
        self.write(data)

    @api.multi
    def open_batch_wizard(self):
        view = self.env.ref('nagi.view_hos_batch_form')

        context = self.env.context.copy()
        context.update({"product_id": self.product_id.id,
                        "location_id": self.env.user.company_id.pharmacy_location_id.id})

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


class SaleOrderBatch(models.Model):
    _name = "sale.batch"

    batch_no = fields.Char(string="Batch No", required=True)
    manufactured_date = fields.Date(string="Manufacturing Date", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)
    mrp_rate = fields.Float(string="MRP", default=0)
    unit_price = fields.Float(string="Unit Price", default=0)
    quantity = fields.Float(string="Quantity", default=0, required=True)
    sale_detail_id = fields.Many2one(comodel_name="sale.detail", string="Batch")

    @api.model
    def create(self, vals):
        if vals["quantity"] > 0:
            return super(SaleOrderBatch, self).create(vals)

