# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


# Leave Availability
class LeaveAvailability(models.TransientModel):
    _name = "leave.availability"

    person_id = fields.Many2one(comodel_name="hos.person", string="Person", required=True)
    leave_available = fields.Float(string="Leave Available", default=0)

    @api.onchange("person_id")
    def get_report(self):
        if self.person_id:
            self.leave_available = self.env["month.attendance"].get_leave_available(self.person_id)


