# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]


# Permission
class Permission(models.Model):
    _name = "permission.application"
    _inherit = "mail.thread"

    from_time = fields.Datetime(string="From", required=True)
    till_time = fields.Datetime(string="Till", required=True)
    person_id = fields.Many2one(comodel_name="hos.person", string="Employee", readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirmed(self):
        data = {"progress": "confirmed",
                "writter": "Permission confirmed by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        data = {"progress": "cancelled",
                "writter": "Permission cancelled by {0}".format(self.env.user.name)}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        data = {"progress": "approved",
                "writter": "Permission approved by {0}".format(self.env.user.name)}

        self.write(data)

    @api.model
    def create(self, vals):
        person_id = self.env["hos.person"].search([("id", "=", self.env.user.person_id.id)])
        vals["person_id"] = person_id.id
        vals["writter"] = "Permission created by {0}".format(self.env.user.name)
        return super(Permission, self).create(vals)
