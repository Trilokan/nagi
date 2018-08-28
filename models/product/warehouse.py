# -*- coding: utf-8 -*-

from odoo import fields, models


# Warehouse
class HospitalWarehouse(models.Model):
    _name = "hos.warehouse"
    _rec_name = "location_id"

    product_id = fields.Many2one(comodel_name="hos.product", string="Product", readonly=True)
    location_id = fields.Many2one(comodel_name="hos.location", string="Location", readonly=True)
    quantity = fields.Float(string="Quantity", compute="_get_stock")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    _sql_constraints = [('unique_product_location', 'unique (product_id, location_id)',
                         'Error! Product location must be unique')]

    def _get_stock(self):
        for record in self:
            destination_ids = self.env["hos.move"].search([("product_id", "=", record.product_id.id),
                                                           ("destination_location_id", "=", record.location_id.id),
                                                           ("progress", "=", "moved")])

            source_ids = self.env["hos.move"].search([("product_id", "=", record.product_id.id),
                                                      ("source_location_id", "=", record.location_id.id),
                                                      ("progress", "=", "moved")])
            quantity_in = quantity_out = 0

            for rec in destination_ids:
                quantity_in = quantity_in + rec.quantity

            for rec in source_ids:
                quantity_out = quantity_out + rec.quantity

            record.quantity = quantity_in - quantity_out
