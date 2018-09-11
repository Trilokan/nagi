# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime

# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('approved', 'Approved'),
                 ('cancelled', 'Cancelled')]


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = "mail.thread"

    name = fields.Char(string='Name', readonly=True)
    date = fields.Date(string="Date",
                       default=datetime.now().strftime("%Y-%m-%d"),
                       readonly=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    vendor_id = fields.Many2one(comodel_name="hos.person", string="Vendor", readonly=True)
    vendor_ref = fields.Char(string="Vendor Ref")
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent", readonly=True)
    quote_id = fields.Many2one(comodel_name="purchase.quote", string="Quotation", readonly=True)
    order_detail = fields.One2many(comodel_name='purchase.detail',
                                   inverse_name='order_id',
                                   string='Order Detail')
    amount_detail = fields.One2many(comodel_name='amount.detail',
                                    inverse_name='order_id',
                                    string='Amount Detail')
    total_amount = fields.Float(string="Total Amount")
    comment = fields.Text(string='Comment')
    writter = fields.Text(string="Writter", track_visibility='always')
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')

    @api.multi
    def total_calculation(self):
        recs = self.order_detail

        if not recs:
            raise exceptions.ValidationError("Error! Bill details not found")

        for rec in recs:
            rec.detail_calculation()

        data = {}

        data["discount_amount"] = 0
        data["tax_amount"] = 0
        data["cgst"] = 0
        data["sgst"] = 0
        data["igst"] = 0
        data["total_amount"] = 0
        data["gross_amount"] = 0
        data["round_off_amount"] = 0

        for rec in recs:
            data["discount_amount"] = data["discount_amount"] + rec.discount_amount
            data["tax_amount"] = data["tax_amount"] + rec.tax_amount
            data["cgst"] = data["cgst"] + rec.cgst
            data["sgst"] = data["sgst"] + rec.sgst
            data["igst"] = data["igst"] + rec.igst

            data["total_amount"] = data["total_amount"] + rec.total_amount
            data["gross_amount"] = round(data["total_amount"])
            data["round_off_amount"] = round(data["total_amount"]) - data["total_amount"]

        self.write(data)

    def trigger_grn(self):
        data = {}

        hos_move = []
        recs = self.order_detail
        for rec in recs:
            if (rec.accepted_quantity > 0) and (rec.unit_price > 0):
                hos_move.append((0, 0, {"reference": self.name,
                                        "source_location_id": self.env.user.company_id.purchase_location_id.id,
                                        "destination_location_id": self.env.user.company_id.store_location_id.id,
                                        "picking_type": "in",
                                        "product_id": rec.product_id.id,
                                        "requested_quantity": rec.accepted_quantity}))

        if hos_move:
            data["person_id"] = self.vendor_id.id
            data["reference"] = self.name
            data["picking_detail"] = hos_move
            data["picking_type"] = 'in'
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            data["po_id"] = self.id
            data["source_location_id"] = self.env.user.company_id.purchase_location_id.id
            data["destination_location_id"] = self.env.user.company_id.store_location_id.id
            data["picking_category"] = "po"
            picking_id = self.env["hos.picking"].create(data)
            return True
        return False

    @api.multi
    def trigger_po_approve(self):
        self.total_calculation()

        if not self.trigger_grn():
            raise exceptions.ValidationError("Error! Please check Product lines")

        writter = "PO approved by {0}".format(self.env.user.name)
        self.write({"progress": "approved", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        person_id = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "PO cancelled by {0}".format(person_id.name)

        self.write({"progress": "cancelled", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        return super(PurchaseOrder, self).create(vals)
