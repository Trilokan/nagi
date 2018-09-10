# -*- coding: utf-8 -GPK*-

{
    'name': 'Hospital',
    'version': '1.0',
    "author": 'La Mars',
    "website": 'http://',
    'category': 'Hospital Management System',
    'sequence': 1,
    'summary': 'Hospital Management System',
    'description': 'Hospital Management System',
    'depends': ['base', 'mail'],
    'data': [
        'views/assert_backend.xml',
        'menu/web_menu.xml',
        'data/base_pack.xml',
        'data/product.xml',
        'data/hospital.xml',
        'data/employee.xml',
        'data/account.xml',
        'data/asset_account.xml',
        'data/liability_account.xml',
        'data/revenue_account.xml',
        'data/expense_account.xml',
        'data/capital_account.xml',

        'data/employee_cr.xml',

        'data/hos.location.csv',
        'data/hos.uom.csv',
        'data/hos.product.csv',

        'sequence/product.xml',
        'sequence/purchase.xml',
        'sequence/employee.xml',
        'sequence/hospital.xml',


        'security/hospital.xml',
        'security/ir.model.access.csv',

        # Account
        'views/web/account/account.xml',
        'views/web/account/pre_defined_account.xml',
        'views/web/account/journal.xml',
        'views/web/account/journal_entry.xml',
        'views/web/account/journal_item.xml',
        'views/web/account/voucher.xml',
        'views/web/account/tax.xml',
        'views/web/account/leave.xml',

        # Base Pack
        'views/web/base_pack/company.xml',
        'views/web/base_pack/users.xml',
        'views/web/base_pack/year.xml',
        'views/web/base_pack/period.xml',
        'views/web/base_pack/country.xml',
        'views/web/base_pack/state.xml',
        'views/web/base_pack/religion.xml',
        'views/web/base_pack/language.xml',

        # Person
        'views/web/person/person.xml',

        # Patient
        'views/web/patient/patient.xml',
        'views/web/patient/symptoms.xml',
        'views/web/patient/diagnosis.xml',
        'views/web/patient/opt_treatment.xml',
        'views/web/patient/ipt_treatment.xml',
        'views/web/patient/prescription.xml',

        # Hospital
        'views/web/hospital/admission.xml',
        'views/web/hospital/ward.xml',
        'views/web/hospital/bed.xml',
        'views/web/hospital/patient_shifting.xml',
        'views/web/hospital/ambulance.xml',
        'views/web/hospital/discharge.xml',
        'views/web/hospital/ot_booking.xml',
        'views/web/hospital/operation_theater.xml',
        'views/web/hospital/operation.xml',
        'views/web/hospital/notes.xml',
        'views/web/hospital/notification.xml',

        # Employee
        'views/web/employee/employee.xml',
        'views/web/employee/hr_department.xml',
        'views/web/employee/hr_category.xml',
        'views/web/employee/hr_designation.xml',
        'views/web/employee/hr_contact.xml',
        'views/web/employee/hr_experience.xml',
        'views/web/employee/hr_qualification.xml',

        # Recruitment
        'views/web/recruitment/vacancy_position.xml',
        'views/web/recruitment/resume_bank.xml',
        'views/web/recruitment/interview_schedule.xml',
        'views/web/recruitment/appointment_order.xml',

        # Time Management
        'views/web/time_management/shift.xml',
        'views/web/time_management/time_configuration.xml',
        'views/web/time_management/week_schedule.xml',
        'views/web/time_management/monthly_attendance.xml',
        'views/web/time_management/monthly_attendance_wiz.xml',
        'views/web/time_management/attendance.xml',
        'views/web/time_management/shift_change.xml',
        'views/web/time_management/add_employee_to_shift.xml',
        'views/web/time_management/holiday_change.xml',
        'views/web/time_management/time_sheet.xml',
        'views/web/time_management/time_sheet_application.xml',

        # # Leave Management
        'views/web/leave_management/leave_configuration.xml',
        'views/web/leave_management/leave.xml',
        'views/web/leave_management/compoff.xml',
        'views/web/leave_management/permission.xml',
        'views/web/leave_management/leave_journal.xml',
        'views/web/leave_management/leave_voucher.xml',
        'views/web/leave_management/leave_type.xml',
        'views/web/leave_management/leave_level.xml',
        'views/web/leave_management/leave_availability.xml',

        # Payroll
        'views/web/payroll/hr_pay_update_wiz.xml',
        'views/web/payroll/hr_pay.xml',
        'views/web/payroll/payslip.xml',
        'views/web/payroll/payroll_generation.xml',
        'views/web/payroll/salary_structure.xml',
        'views/web/payroll/salary_rule.xml',
        'views/web/payroll/salary_rule_slab.xml',

        # Product
        'views/web/product/product_group.xml',
        'views/web/product/sub_group.xml',
        'views/web/product/uom.xml',
        'views/web/product/product_category.xml',
        'views/web/product/location.xml',
        'views/web/product/warehouse.xml',
        'views/web/product/product.xml',
        'views/web/product/stock_adjustment.xml',
        'views/web/product/hos_move.xml',
        'views/web/product/store_request.xml',
        'views/web/product/store_issue.xml',
        'views/web/product/batch.xml',

        # Purchase
        'views/web/purchase/purchase_indent.xml',
        'views/web/purchase/purchase_quotation.xml',
        'views/web/purchase/purchase_order.xml',
        'views/web/purchase/material_receipt.xml',
        'views/web/purchase/direct_material_receipt.xml',

        # Invoice
        'views/web/bills/purchase_invoice.xml',
        'views/web/bills/sale_invoice.xml',
        'views/web/bills/patient_invoice.xml',

        # Schedule
        'views/web/schedule/schedule.xml',
        'views/web/schedule/schedule_reason.xml',
        'views/web/schedule/schedule_type.xml',
        'views/web/schedule/doctor_availability.xml',

        # Laboratory
        'views/web/laboratory/lab_form.xml',
        'views/web/laboratory/lab_test.xml',

        # Assert
        'views/web/assert/hos_assert.xml',
        'views/web/assert/assert_service.xml',
        'views/web/assert/assert_notification.xml',

        # Pharmacy
        'views/web/pharmacy/sale_order.xml',
        'views/web/pharmacy/sale_detail.xml',
        'views/web/pharmacy/material_delivery.xml',

        # Menu
        'views/web/menu/account.xml',
        # 'views/web/menu/hospital.xml',
        # 'views/web/menu/patient.xml',
        'views/web/menu/employee.xml',
        'views/web/menu/product.xml',
        'views/web/menu/procurement.xml',
        'views/web/menu/base_packs.xml',
        'views/web/menu/pharmacy.xml',
        # 'views/web/menu/laboratory.xml',


    ],
    'demo': [

    ],
    'qweb': [
        'static/src/xml/status_bar.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
