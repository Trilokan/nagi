# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('invoice_generated', 'Invoice Generated'),
                 ('cancelled', 'Cancelled')]


class Quotation(surya.Sarpam):
    _name = "purchase.quotation"
    _inherit = "mail.thread"

    name = fields.Char(string='Name', readonly=True)
    date = fields.Date(string="Date", readonly=True)
    vendor_id = fields.Many2one(comodel_name="hos.person", string="Vendor", readonly=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent", readonly=True)
    vs_id = fields.Many2one(comodel_name="purchase.vs", string="Vendor Selection", readonly=True)
    vendor_ref = fields.Char(string="Vendor Ref")
    processed_by = fields.Many2one(comodel_name="hos.person", string="Processed By", readonly=True)
    processed_on = fields.Date(string='Processed On', readonly=True)
    quotation_detail = fields.One2many(comodel_name='vs.quote.detail',
                                       inverse_name='quotation_id',
                                       string='Quotation Detail')
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')
    comment = fields.Text(string='Comment')

    freight_amount = fields.Float(string="Freight Amount", readonly=True,)
    discount_amount = fields.Float(string='Discount Amount', readonly=True, help='Discount value')
    discounted_amount = fields.Float(string='Discounted Amount', readonly=True, help='Amount after discount')
    tax_amount = fields.Float(string='Tax Amount', readonly=True, help='Tax value')
    taxed_amount = fields.Float(string='Taxed Amount', readonly=True, help='Tax after discounted amount')
    untaxed_amount = fields.Float(string='Untaxed Amount', readonly=True)
    sgst = fields.Float(string='SGST', readonly=True)
    cgst = fields.Float(string='CGST', readonly=True)
    igst = fields.Float(string='IGST', readonly=True)
    gross_amount = fields.Float(string='Gross Amount', readonly=True)
    round_off_amount = fields.Float(string='Round-Off', readonly=True)
    writter = fields.Text(string="Writter", track_visibility='always')

    def default_vals_creation(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")

        return vals

    @api.multi
    def total_calculation(self):
        recs = self.quotation_detail

        if not recs:
            raise exceptions.ValidationError("Error! Bill details not found")

        for rec in recs:
            rec.detail_calculation()

        discount_amount = discounted_amount = tax_amount = untaxed_amount = taxed_amount \
            = cgst = sgst = igst = freight_amount = total_amount = 0
        for rec in recs:
            discount_amount = discount_amount + rec.discount_amount
            discounted_amount = discounted_amount + rec.discounted_amount
            tax_amount = tax_amount + rec.tax_amount
            untaxed_amount = untaxed_amount + rec.untaxed_amount
            taxed_amount = taxed_amount + rec.taxed_amount
            cgst = cgst + rec.cgst
            sgst = sgst + rec.sgst
            igst = igst + rec.igst

            freight_amount = freight_amount + rec.freight_amount
            total_amount = total_amount + rec.total_amount
        gross_amount = round(total_amount)
        round_off_amount = round(total_amount) - total_amount

        self.write({"discount_amount": discount_amount,
                    "discounted_amount": discounted_amount,
                    "tax_amount": tax_amount,
                    "untaxed_amount": untaxed_amount,
                    "taxed_amount": taxed_amount,
                    "cgst": cgst,
                    "sgst": sgst,
                    "igst": igst,
                    "freight_amount": freight_amount,
                    "total_amount": total_amount,
                    "gross_amount": gross_amount,
                    "round_off_amount": round_off_amount})

    def trigger_invoice_generation(self):
        data = {}

        invoice_detail = []
        recs = self.quotation_detail
        for rec in recs:
            if (rec.accepted_quantity > 0) and (rec.unit_price > 0):
                invoice_detail.append((0, 0, {"product_id": rec.product_id.id,
                                              "unit_price": rec.unit_price,
                                              "quantity": rec.accepted_quantity,
                                              "discount": rec.discount,
                                              "tax_id": rec.tax_id.id,
                                              "freight": rec.freight,}))

        if invoice_detail:
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            data["person_id"] = self.vendor_id.id
            data["invoice_detail"] = invoice_detail
            data["invoice_type"] = 'purchase_bill'
            data["reference"] = self.name

            invoice_id = self.env["hos.invoice"].create(data)
            invoice_id.total_calculation()
            return True
        return False

    @api.multi
    def trigger_quote_approve(self):
        self.total_calculation()

        if not self.trigger_invoice_generation():
            raise exceptions.ValidationError("Error! Please check Product lines")

        writter = "Invoice generated by {0}".format(self.env.user.name)
        self.write({"progress": "invoice_generated", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        person_id = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "Quotation cancelled by {0}".format(person_id.name)

        self.write({"progress": "cancelled", "writter": writter})

