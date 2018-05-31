# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya

RELATION_INFO = [('father', 'Father'),
                 ('mother', 'Mother'),
                 ('wife', 'Wife'),
                 ('brother', 'Brother'),
                 ('sister', 'Sister'),
                 ('uncle', 'Uncle'),
                 ('aunt', 'Aunt'),
                 ('grand_father', 'Grand Father'),
                 ('grand_mother', 'Grand Mother'),
                 ('son', 'Son'),
                 ('daughter', 'Daughter')]


# Contacts
class HospitalContact(surya.Sarpam):
    _name = "hos.contact"
    _inherit = "hos.address"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    patient_id = fields.Many2one(comodel_name="hos.patient", string="Patient")
    name = fields.Char(string="Name")
    relation = fields.Selection(selection=RELATION_INFO, string="Relation")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="E-mail")
