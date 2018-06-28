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

        'menu/main_menu.xml',
        # 'data/base_pack.xml',
        # 'data/time_management.xml',
        'data/purchase.xml',
        'data/hospital.xml',
        'data/employee.xml',

        # # Account
        # # 'views/account/account.xml',
        #
        # # Base Pack
        # 'views/base_pack/company.xml',
        # 'views/base_pack/users.xml',
        # 'views/base_pack/year.xml',
        # 'views/base_pack/period.xml',
        #
        # # Person
        # 'views/person/person.xml',
        #
        # Patient
        # 'views/web/patient/patient.xml',
        # 'views/patient/opt_treatment.xml',
        # 'views/patient/ipt_treatment.xml',
        # 'views/patient/ipt_prescription.xml',
        #
        # # Hospital
        # 'views/hospital/admission.xml',
        # 'views/hospital/ward.xml',
        # 'views/hospital/bed.xml',
        # 'views/hospital/patient_shifting.xml',
        # 'views/hospital/ambulance.xml',
        # 'views/hospital/discharge.xml',
        # 'views/hospital/ot_booking.xml',
        # 'views/hospital/operation_theater.xml',
        # 'views/hospital/operation.xml',
        #
        # 'views/web/hospital/admission.xml',
        #
        # Employee
        'views/web/employee/employee.xml',
        # 'views/employee/hr_department.xml',
        # 'views/employee/hr_category.xml',
        # 'views/employee/hr_designation.xml',
        # 'views/employee/hr_contact.xml',
        # 'views/employee/hr_experience.xml',
        # 'views/employee/hr_qualification.xml',
        # 'views/employee/hr_leave.xml',

        # Recruitment
        'views/web/recruitment/vacancy_position.xml',
        'views/web/recruitment/resume_bank.xml',
        'views/web/recruitment/interview_schedule.xml',
        'views/web/recruitment/appointment_order.xml',
        #
        # # Leave Management
        # 'views/leave_management/leave_configuration.xml',
        # 'views/leave_management/leave.xml',
        # 'views/leave_management/compoff.xml',
        # 'views/leave_management/permission.xml',

        # Time Management
        'views/web/time_management/shift.xml',
        'views/web/time_management/time_configuration.xml',
        'views/web/time_management/week_schedule.xml',
        # 'views/time_management/monthly_attendance.xml',
        # 'views/time_management/attendance.xml',
        # 'views/time_management/shift_change.xml',
        # 'views/time_management/holiday_change.xml',
        # 'views/time_management/time_sheet.xml',
        # 'views/time_management/time_sheet_application.xml',
        #
        # # Payroll
        # 'views/payroll/hr_pay_update_wiz.xml',
        # 'views/payroll/hr_pay.xml',
        # 'views/payroll/payslip.xml',
        # 'views/payroll/payroll_generation.xml',
        # 'views/payroll/salary_structure.xml',
        # 'views/payroll/salary_rule.xml',
        # 'views/payroll/salary_rule_slab.xml',

        # Product
        'views/web/product/product_group.xml',
        'views/web/product/sub_group.xml',
        'views/web/product/uom.xml',
        'views/web/product/tax.xml',
        'views/web/product/product_category.xml',
        'views/web/product/product_type.xml',
        'views/web/product/location.xml',
        'views/web/product/warehouse.xml',
        'views/web/product/product.xml',
        'views/web/product/stock_adjustment.xml',
        'views/web/product/stock_move.xml',
        'views/web/product/store_request.xml',
        'views/web/product/store_issue.xml',

        # Purchase
        'views/web/purchase/purchase_indent.xml',
        'views/web/purchase/purchase_quotation.xml',
        'views/web/purchase/purchase_order.xml',
        'views/web/purchase/material_receipt.xml',
        'views/web/purchase/direct_material_receipt.xml',

        # Invoice
        'views/web/bills/purchase_invoice.xml',
        #
        # # Schedule
        # 'views/schedule/schedule.xml',
        # 'views/schedule/schedule_reason.xml',
        # 'views/schedule/schedule_type.xml',
        #
        # Laboratory
        # 'views/web/laboratory/lab_form.xml',
        # 'views/web/laboratory/lab_test.xml',

        # # Menu
        # 'menu/base_pack.xml',
        # 'menu/patient.xml',
        # 'menu/employee.xml',
        'views/web/menu/product.xml',
        'views/web/menu/employee.xml',
        # 'menu/purchase.xml',
        # 'menu/hospital.xml',
        # 'menu/reception.xml',


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
