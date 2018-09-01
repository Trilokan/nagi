# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _

END_INFO = [('current_day', 'Current Day'), ('next_day', 'Next Day')]


# Shift Master
class Shift(models.Model):
    _name = "time.shift"
    _inherit = "mail.thread"

    name = fields.Char(string="Shift", required=True)
    total_hours = fields.Float(string="Total Hours", readonly=True)
    end_day = fields.Selection(selection=END_INFO, string="Ends On", default="current_day")
    from_hours = fields.Integer(string="From Hours")
    from_minutes = fields.Integer(string="From Minutes")
    till_hours = fields.Integer(string="Till Hours")
    till_minutes = fields.Integer(string="Till Minutes")
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    @api.multi
    def trigger_calculate(self):
        total_from_hours = (self.from_hours * 60) + self.from_minutes
        total_till_hours = (self.till_hours * 60) + self.till_minutes
        if self.end_day == 'current_day':
            self.total_hours = float(total_till_hours - total_from_hours) / 60
        elif self.end_day == 'next_day':
            self.total_hours = 24 - (float(total_from_hours - total_till_hours) / 60)
