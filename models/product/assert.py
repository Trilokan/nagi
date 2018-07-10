# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Assert
class Assert(surya.Sarpam):
    _name = "hos.assert"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

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
    notification_details = fields.One2many(comodel_name="assert.notification",
                                           inverse_name="assert_id",
                                           string="Notification Details")

    # Accounting Details
    account_id = fields.Many2one(comodel_name="hos.account", string="Account")
    depreciation_percentage = fields.Float(string="Depreciation Percentage")
    responsible_id = fields.Many2one(comodel_name="hos.person", string="Responsible Person")
    responsible_details = fields.One2many(comodel_name="hos.person",
                                          inverse_name="assert_id",
                                          string="Responsible Person")
    is_working = fields.Boolean(string="Is Working")
    is_condem = fields.Boolean(string="Is Condemed")
    # attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Group Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Group must be unique')]

    def default_vals_creation(self, vals):
        vals["writter"] = "Product Group Created by {0}".format(self.env.user.name)
        vals["company_id"] = self.env.user.company_id.id
        return vals


class AssertService(surya.Sarpam):
    _name = "assert.service"
    _inherit = "mail.thread"

    assert_id = fields.Many2one(comodel_name="hos.assert", string="Assert")
    person_id = fields.Many2one(comodel_name="hos.person", string="Service")
    date = fields.Date(string="Date")
    description = fields.Text(string="Description")
    comment = fields.Text(string="Comment")


class AssertResponsible(surya.Sarpam):
    _name = "assert.service"
    _inherit = "mail.thread"

    assert_id = fields.Many2one(comodel_name="hos.assert", string="Assert")
    person_id = fields.Many2one(comodel_name="hos.person", string="Service")
    date = fields.Date(string="Date")


class AssertNotification(surya.Sarpam):
    _name = "assert.notification"
    _inherit = "mail.thread"

    assert_id = fields.Many2one(comodel_name="hos.assert", string="Assert")
    person_id = fields.Many2one(comodel_name="hos.person", string="Notify")
    date = fields.Date(string="Date")
    description = fields.Text(string="Description")
    comment = fields.Text(string="Comment")