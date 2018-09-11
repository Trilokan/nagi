# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _

PROGRESS_INFO = [('draft', 'Draft'),
                 ('approved', 'Approved'),
                 ('cancelled', 'Cancelled')]


class AmountDetail(models.Model):
    _name = 'amount.detail'
    _order = "sequence"

    amount_id = fields.Many2one(comodel_name="hos.amount", string="Amount")
    sequence = fields.Integer(string="Sequence", related="amount_id.sequence")
    amount = fields.Float(string="Amount")
    order_id = fields.Many2one(comodel_name='purchase.order', string='Purchase Order')
    purchase_progress = fields.Selection(PROGRESS_INFO, string='Progress', related='order_id.progress')
