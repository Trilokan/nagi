# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _, models
from datetime import datetime, timedelta
from .. import surya
from .. import calculation


PROGRESS_INFO = [('draft', 'Draft'), ('approved', 'approved'), ('cancel', 'Cancel')]
INVOICE_TYPE = [("dpo", "Direct Purchase Bill"),
                ("po", "Purchase Bill"),
                ("por", "Purchase Return Bill"),
                ("so", "Sale Bill"),
                ("sor", "Sale Return Bill")]


# Bills
class HospitalInvoice(surya.Sarpam):
    _name = "hos.invoice"
    _inherit = "mail.thread"

    date = fields.Date(srring="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Partner", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readdonly=True)

    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    quote_id = fields.Many2one(comodel_name="purchase.quote", string="Quotation")
    po_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")
    so_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    picking_id = fields.Many2one(comodel_name="hos.picking", string="Material Receipt")
    reference = fields.Char(string="Reference")

    writter = fields.Text(string="Writter", track_visibility='always')
    invoice_detail = fields.One2many(comodel_name="invoice.detail",
                                     inverse_name="invoice_id",
                                     string="Invoice detail")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    invoice_type = fields.Selection(selection=INVOICE_TYPE, string="Invoice Type", required=True)
    discount_amount = fields.Float(string="Discount Amount", readonly=True)
    discounted_amount = fields.Float(string="Discounted Amount", readonly=True)
    tax_amount = fields.Float(string="Tax Amount", readonly=True)
    untaxed_amount = fields.Float(string="Untaxed Amount", readonly=True)
    taxed_amount = fields.Float(string="Taxed Amount", readonly=True)
    cgst = fields.Float(string="CGST", readonly=True)
    sgst = fields.Float(string="SGST", readonly=True)
    igst = fields.Float(string="IGST", readonly=True)
    freight_amount = fields.Float(string="Freight Amount", readonly=True)
    total_amount = fields.Float(string="Total Amount", readonly=True)
    round_off_amount = fields.Float(string="Round-Off", readonly=True)
    gross_amount = fields.Float(stringt="Gross Amount", readonly=True)

    # payment_detail = fields.One2many(comodel_name="invoice.detail",
    #                                  inverse_name="invoice_id",
    #                                  string="Invoice detail")
    # Account_detail

    def default_vals_creation(self, vals):
        code = "{0}.{1}".format("hos.invoice", vals["invoice_type"])
        vals['name'] = self.env['ir.sequence'].next_by_code("hos.purchase.invoice")
        vals['company_id'] = self.env.user.company_id.id
        vals['writter'] = self.env.user.name
        if vals.get('date', True):
            vals['date'] = datetime.now().strftime("%Y-%m-%d")
        return vals

    @api.multi
    def trigger_approve(self):
        self.total_calculation()

        writter = "Invoice approved by {0}".format(self.env.user.name)
        self.write({"progress": "approved", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        self.total_calculation()

        writter = "Invoice cancel by {0}".format(self.env.user.name)
        self.write({"progress": "cancel", "writter": writter})

    @api.multi
    def total_calculation(self):
        recs = self.invoice_detail

        if not recs:
            raise exceptions.ValidationError("Error! Bill details not found")

        for rec in recs:
            rec.detail_calculation()

        discount_amount = discounted_amount = tax_amount = untaxed_amount = taxed_amount\
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


class InvoiceDetail(surya.Sarpam):
    _name = "invoice.detail"

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

    invoice_id = fields.Many2one(comodel_name="hos.invoice", string="Hospital Invoice")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="invoice_id.progress")

    @api.multi
    def detail_calculation(self):
        data = calculation.purchase_calculation(self.unit_price,
                                                self.quantity,
                                                self.discount,
                                                self.tax_id.value,
                                                self.freight,
                                                self.tax_id.state)
        self.write(data)
