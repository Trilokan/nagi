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

        'menu/main_menu.xml',
        'data/base_pack.xml',

        # Account
        # 'views/account/account.xml',

        # Base Pack
        'views/base_pack/company.xml',
        'views/base_pack/users.xml',


        # Person
        'views/person/person.xml',

        # Patient
        'views/patient/patient.xml',


        # Employee
        'views/employee/employee.xml',

        'menu/base_pack.xml',
        'menu/patient.xml',
        'menu/employee.xml',

    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
