# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Picking
class StockPicking(surya.Sarpam):
    _name = "stock.picking"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Partner", readonly=True)
    reference = fields.Char(string="Reference", readonly=True)
    reason = fields.Text(string="Reason")
    picking_detail = fields.One2many(comodel_name="stock.move",
                                     inverse_name="picking_id",
                                     string="Stock Move")
    picking_type = fields.Selection(selection=PICKING_TYPE, string="Picking Type", required=True)
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

    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    source_location_id = fields.Many2one(comodel_name="hos.location",
                                         string="Source Location",
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="hos.location",
                                              string="Destination location",
                                              required=True)
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.multi
    def trigger_move(self):
        self.total_calculation()
        writter = "Stock Picked by {0}".format(self.env.user.name)
        recs = self.picking_detail

        for rec in recs:
            rec.trigger_move()

        self.write({"progress": "moved", "writter": writter})

    @api.multi
    def total_calculation(self):
        recs = self.picking_detail

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

    def trigger_adjust(self):
        recs = self.picking_detail
        for rec in recs:
            rec.trigger_move()

        writter = "Stock Adjusted by {0}".format(self.env.user.name)
        self.write({"progress": "moved", "writter": writter})

    def default_vals_creation(self, vals):
        vals["company_id"] = self.env.user.company_id.id
        vals["writter"] = "Created by {0}".format(self.env.user.name)
        return vals
