# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]


# Sale order
class SaleOrder(surya.Sarpam):
    _name = "sale.order"

    date = fields.Date(srring="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Partner", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readdonly=True)

    writter = fields.Text(string="Writter", track_visibility='always')
    invoice_detail = fields.One2many(comodel_name="invoice.detail",
                                     inverse_name="invoice_id",
                                     string="Invoice detail")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
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
