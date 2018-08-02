# -*- coding: utf-8 -*-

from odoo import fields, exceptions, api, _
from .. import surya
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirm", "Confirm"), ("cancel", "Cancel")]


# Sale order
class SaleOrder(surya.Sarpam):
    _name = "sale.order"
    _inherit = "mail.thread"

    date = fields.Date(srring="Date", required=True, default=datetime.now().strftime("%Y-%m-%d"))
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Partner", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readdonly=True)
    order_detail = fields.One2many(comodel_name="sale.detail",
                                   inverse_name="order_id",
                                   string="Sale detail")

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

    writter = fields.Text(string="Writter", track_visibility='always')

    def default_vals_creation(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["company_id"] = self.env.user.company_id.id
        vals["progress"] = "draft"
        return vals

    @api.multi
    def total_calculation(self):
        recs = self.order_detail

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

    def trigger_gsn(self):
        data = {}

        hos_move = []
        recs = self.order_detail
        for rec in recs:
            if (rec.quantity > 0) and (rec.unit_price > 0):
                hos_move.append((0, 0, {"reference": self.name,
                                        "source_location_id": self.env.user.company_id.purchase_location_id.id,
                                        "destination_location_id": self.env.user.company_id.location_id.id,
                                        "picking_type": "in",
                                        "product_id": rec.product_id.id,
                                        "requested_quantity": rec.quantity}))

        if hos_move:
            data["person_id"] = self.person_id.id
            data["reference"] = self.name
            data["picking_detail"] = hos_move
            data["picking_type"] = 'out'
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            data["so_id"] = self.id
            data["source_location_id"] = self.env.user.company_id.purchase_location_id.id
            data["destination_location_id"] = self.env.user.company_id.location_id.id
            data["picking_category"] = "so"
            picking_id = self.env["hos.picking"].create(data)
            return True
        return False

    def trigger_gsn_direct(self):
        data = {}

        hos_move = []
        recs = self.order_detail
        for rec in recs:
            if (rec.quantity > 0) and (rec.unit_price > 0):
                hos_move.append((0, 0, {"reference": self.name,
                                        "source_location_id": self.env.user.company_id.purchase_location_id.id,
                                        "destination_location_id": self.env.user.company_id.location_id.id,
                                        "picking_type": "in",
                                        "product_id": rec.product_id.id,
                                        "requested_quantity": rec.quantity,
                                        "quantity": rec.quantity}))

        if hos_move:
            data["person_id"] = self.person_id.id
            data["reference"] = self.name
            data["picking_detail"] = hos_move
            data["picking_type"] = 'out'
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            data["so_id"] = self.id
            data["source_location_id"] = self.env.user.company_id.purchase_location_id.id
            data["destination_location_id"] = self.env.user.company_id.location_id.id
            data["picking_category"] = "so"
            picking_id = self.env["hos.picking"].create(data)
            picking_id.trigger_move()

            return True
        return False

    @api.multi
    def trigger_confirm(self):
        self.total_calculation()

        if not self.trigger_gsn():
            raise exceptions.ValidationError("Error! Please check Product lines")

        writter = "SO confirm by {0}".format(self.env.user.name)
        self.write({"progress": "confirm", "writter": writter})

    @api.multi
    def trigger_paid(self):
        self.total_calculation()

        if not self.trigger_gsn_direct():
            raise exceptions.ValidationError("Error! Please check Product lines")

        picking_id = self.env["hos.picking"].search([("so_id", "=", self.id)])
        picking_id.trigger_create_sale_invoice()

        invoice_id = self.env["hos.invoice"].search([("so_id", "=", self.id)])
        invoice_id.trigger_approve()

        writter = "SO Paid by {0}".format(self.env.user.name)
        self.write({"progress": "confirm", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "SO cancel by {0}".format(self.env.user.name)
        self.write({"progress": "cancel", "writter": writter})

