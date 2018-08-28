# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _


# Product
class Product(models.Model):
    _name = "hos.product"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", readonly=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    uom_id = fields.Many2one(comodel_name="hos.uom", string="UOM", required=True)
    category_id = fields.Many2one(comodel_name="hos.product.category", string="Category", required=True)
    warehouse_ids = fields.One2many(comodel_name="hos.warehouse",
                                    inverse_name="product_id",
                                    string="Warehouse",
                                    domain=lambda self: self._get_warehouse_ids(),
                                    readonly=True)
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    min_stock = fields.Integer(string="Min Stock")
    max_stock = fields.Integer(string="Max Stock")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Product Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Product must be unique')]

    def _get_warehouse_ids(self):
        location_left = self.env.user.company_id.virtual_location_left
        location_right = self.env.user.company_id.virtual_location_right

        domain = [('location_id.location_left', '>=', location_left),
                  ('location_id.location_right', '<=', location_right)]

        virtual_location = self.env["hos.warehouse"].search(domain)

        return [("id", "not in", virtual_location.ids)]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(['|', ('name', '=', name), ('code', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search(['|', ('name', operator, name), ('code', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.code, record.name)
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        group_id = self.env["product.group"].search([("id", "=", vals["group_id"])])
        sub_group_id = self.env["product.sub.group"].search([("id", "=", vals["sub_group_id"])])
        code = "{0}/{1}/{2}".format(group_id.code,
                                    sub_group_id.code,
                                    self.env["ir.sequence"].next_by_code(self._name))

        vals["code"] = code
        rec = super(Product, self).create(vals)

        # Warehouse Creation
        store_location_id = self.env.user.company_id.store_location_id

        if not store_location_id:
            raise exceptions.ValidationError("Default Product Location is not set")

        self.env["hos.warehouse"].create({"product_id": rec.id,
                                          "location_id": store_location_id.id})

        return rec

