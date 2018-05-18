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
        'data/base_pack.xml',
        'data/time_management.xml',

        # Account
        # 'views/account/account.xml',

        # Base Pack
        'views/base_pack/company.xml',
        'views/base_pack/users.xml',
        'views/base_pack/year.xml',
        'views/base_pack/period.xml',


        # Person
        'views/person/person.xml',

        # Patient
        'views/patient/patient.xml',


        # Employee
        'views/employee/employee.xml',
        'views/employee/hr_department.xml',
        'views/employee/hr_category.xml',
        'views/employee/hr_designation.xml',
        'views/employee/hr_contact.xml',
        'views/employee/hr_experience.xml',
        'views/employee/hr_qualification.xml',
        'views/employee/hr_leave.xml',

        # Recruitment
        'views/recruitment/vacancy_position.xml',
        'views/recruitment/resume_bank.xml',
        'views/recruitment/interview_schedule.xml',
        'views/recruitment/appointment_order.xml',

        # Leave Managemnet
        'views/leave_management/leave_configuration.xml',
        'views/leave_management/leave.xml',
        'views/leave_management/compoff.xml',
        'views/leave_management/permission.xml',

        # Time Management
        'views/time_management/shift.xml',
        'views/time_management/time_configuration.xml',
        'views/time_management/week_schedule.xml',
        'views/time_management/monthly_attendance.xml',
        'views/time_management/attendance.xml',
        'views/time_management/shift_change.xml',
        'views/time_management/holiday_change.xml',
        'views/time_management/time_sheet.xml',
        'views/time_management/time_sheet_application.xml',

        # Product
        'views/product/product_group.xml',
        'views/product/sub_group.xml',
        'views/product/uom.xml',
        'views/product/location.xml',
        'views/product/warehouse.xml',
        'views/product/product.xml',
        'views/product/stock_picking.xml',
        'views/product/stock_move.xml',
        'views/product/store_request.xml',

        # Menu
        'menu/base_pack.xml',
        'menu/patient.xml',
        'menu/employee.xml',
        'menu/product.xml',


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
