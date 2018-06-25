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


class StoreRequest(surya.Sarpam):
    _name = "store.request"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", readonly=True)
    requested_by = fields.Many2one(comodel_name="hos.person", string="Requested By", readonly=True)
    approved_by = fields.Many2one(comodel_name="hos.person", string="Approved By", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    request_detail = fields.One2many(comodel_name="store.request.detail",
                                     inverse_name="request_id",
                                     string="Request Detail")
    writter = fields.Text(string="Writter", track_visibility='always')

    def default_vals_creation(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")

        requested_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        employee_id = self.env["hr.employee"].search([("person_id", "=", self.env.user.person_id.id)])

        vals["requested_by"] = requested_by.id
        vals["department_id"] = employee_id.department_id.id
        return vals

    @api.multi
    def check_quantity(self):
        recs = self.request_detail

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

        writter = "Store Requested by {0} on {1}".format(requested_by.name,
                                                         datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.write({"progress": "confirmed",
                    "requested_by": requested_by.id,
                    "department_id": employee_id.department_id.id,
                    "writter": writter})

    @api.multi
    def trigger_cancel(self):
        cancelled_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "Store Request cancelled by {0} on {1}".format(cancelled_by.name,
                                                                 datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.write({"progress": "cancelled",
                    "writter": writter})

    @api.multi
    def create_issue(self, writter):

        picking_detail = []
        recs = self.request_detail

        for rec in recs:
            if rec.quantity > 0:
                picking_detail.append((0, 0, {"date": datetime.now().strftime("%Y-%m-%d"),
                                              "name": self.env["ir.sequence"].next_by_code("stock.move.internal"),
                                              "reference": self.name,
                                              "product_id": rec.product_id.id,
                                              "requested_quantity": rec.quantity,
                                              "picking_type": "internal",
                                              "unit_price": 0,
                                              "source_location_id": self.env.user.company_id.location_id.id,
                                              "destination_location_id": self.env.user.location_id.id}))

        data = {"date": datetime.now().strftime("%Y-%m-%d"),
                "name": self.env['ir.sequence'].next_by_code("store.issue"),
                "reference": self.name,
                "picking_type": "internal",
                "picking_detail": picking_detail,
                "source_location_id": self.env.user.company_id.location_id.id,
                "destination_location_id": self.env.user.location_id.id,
                "writter": writter}

        self.env["stock.picking"].create(data)

    @api.multi
    def trigger_approve(self):
        self.check_quantity()

        approved_by = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        writter = "Store Request approved by {0} on {1}".format(approved_by.name,
                                                                datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.create_issue(writter)
        self.write({"progress": "approved",
                    "approved_by": approved_by.id,
                    "writter": writter})


class StoreRequestDetail(surya.Sarpam):
    _name = "store.request.detail"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity")
    request_id = fields.Many2one(comodel_name="store.request", string="Store Request")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="request_id.progress")

    _sql_constraints = [('unique_request_detail', 'unique (product_id, request_id)',
                         'Error! Product should not be repeated')]