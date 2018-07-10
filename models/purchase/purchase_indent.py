# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("approved", "Approved"),
                 ("cancelled", "Cancelled")]


class PurchaseIndent(surya.Sarpam):
    _name = "purchase.indent"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", readonly=True)
    requested_by = fields.Many2one(comodel_name="hos.person", string="Requested By", readonly=True)
    approved_by = fields.Many2one(comodel_name="hos.person", string="Approved By", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    indent_detail = fields.One2many(comodel_name="purchase.indent.detail",
                                    inverse_name="indent_id",
                                    string="Indent Detail")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    writter = fields.Text(string="Writter", track_visibility='always')

    def default_vals_creation(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")

        requested_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        employee_id = self.env["hr.employee"].search([("person_id", "=", self.env.user.person_id.id)])

        vals["requested_by"] = requested_by.id
        vals["department_id"] = employee_id.department_id.id
        vals["company_id"] = self.env.user.company_id.id
        return vals

    @api.multi
    def check_quantity(self):
        recs = self.indent_detail

        quantity = 0
        for rec in recs:
            quantity = quantity + rec.quantity

        if quantity <= 0:
            raise exceptions.ValidationError("Error! No Products Found")

    @api.multi
    def trigger_confirm(self):
        self.check_quantity()

        requested_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        employee_id = self.env["hr.employee"].search([("person_id", "=", self.env.user.person_id.id)])
        writter = "Purchase Indent by {0} on {1}".format(requested_by.name,
                                                         datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.write({"progress": "confirmed",
                    "requested_by": requested_by.id,
                    "department_id": employee_id.department_id.id,
                    "writter": writter})

    @api.multi
    def trigger_cancel(self):
        cancelled_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "Purchase Indent cancelled by {0} on {1}".format(cancelled_by.name,
                                                                   datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.write({"progress": "cancelled",
                    "writter": writter})

    @api.multi
    def create_quote(self, writter):

        quote_detail = []
        recs = self.indent_detail

        for rec in recs:
            if rec.quantity > 0:
                quote_detail.append((0, 0, {"product_id": rec.product_id.id,
                                            "quantity": rec.quantity}))

        data = {"indent_id": self.id,
                "quote_detail": quote_detail,
                "writter": writter}

        self.env["purchase.quote"].create(data)

    @api.multi
    def trigger_approve(self):
        self.check_quantity()

        approved_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "Purchase indent approved by {0} on {1}".format(approved_by.name,
                                                                  datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.create_quote(writter)
        self.write({"progress": "approved",
                    "approved_by": approved_by.id,
                    "writter": writter})


class PurchaseIndentDetail(surya.Sarpam):
    _name = "purchase.indent.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="hos.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity")
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="indent_id.progress")

    _sql_constraints = [('unique_indent_detail', 'unique (product_id, indent_id)',
                         'Error! Product should not be repeated')]
