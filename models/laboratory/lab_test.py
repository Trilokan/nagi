# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya


# Lab Test
class Test(surya.Sarpam):
    _name = "lab.test"
    _rec_name = "product_id"

    product_id = fields.Many2one(comodel_name="hospital.product", string="Name")
    test_detail = fields.One2many(comodel_name="test.detail", inverse_name="test_id", string="Test Detail")
    report = fields.Html(string="Report")
    price = fields.Float(string="Price")


class TestDetail(surya.Sarpam):
    _name = "test.detail"

    name = fields.Char(string="Name")
    test_id = fields.Many2one(comodel_name="lab.test", string="Test")
