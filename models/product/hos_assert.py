# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


# Assert
class Assert(surya.Sarpam):
    _name = "hos.assert"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)

    # Manufacturing Details
    product_id = fields.Many2one(comodel_name="hos.product", string="Product", required=True)
    manufacturer = fields.Char(string="Manufacturer")
    manufactured_date = fields.Date(string="Date of Manufactured")
    expiry_date = fields.Date(string="Date of Expiry")
    serial_no = fields.Char(string="Serial No")
    model_no = fields.Char(string="Manufacturer")
    warranty_date = fields.Date(string="Warranty Date")

    # Seller Details
    vendor_id = fields.Many2one(comodel_name="hos.person", string="Vendor")
    purchase_date = fields.Date(string="Date of Purchase")
    # vendor_contact = ""
    # vendor_address = ""

    # Service Details
    service_id = fields.Many2one(comodel_name="hos.person", string="Service")
    # service_contact = ""
    # service_address = ""
    service_details = fields.One2many(comodel_name="assert.service",
                                      inverse_name="assert_id",
                                      string="Service Details")
    notification_details = fields.One2many(comodel_name="assert.reminder",
                                           inverse_name="assert_id",
                                           string="Notification Details")

    # Accounting Details
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    depreciation_percentage = fields.Float(string="Depreciation Percentage")
    responsible_id = fields.Many2one(comodel_name="hos.person", string="Responsible Person")
    is_working = fields.Boolean(string="Is Working")
    is_condem = fields.Boolean(string="Is Condemed")
    # attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_name', 'unique (name)', 'Error! Assert must be unique')]

    def default_vals_creation(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        vals["company_id"] = self.env.user.company_id.id
        vals["writter"] = "Assert Created by {0}".format(self.env.user.name)
        return vals


class AssertService(surya.Sarpam):
    _name = "assert.service"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    assert_id = fields.Many2one(comodel_name="hos.assert", string="Assert")
    person_id = fields.Many2one(comodel_name="hos.person", string="Service")
    description = fields.Text(string="Description")
    attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Assert Service Created by {0}".format(self.env.user.name)
        return vals


class AssertNotification(surya.Sarpam):
    _name = "assert.reminder"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    assert_id = fields.Many2one(comodel_name="hos.assert", string="Assert")
    person_id = fields.Many2one(comodel_name="hos.person", string="Notify")
    description = fields.Text(string="Description")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["writter"] = "Assert reminder Created by {0}".format(self.env.user.name)
        return vals
