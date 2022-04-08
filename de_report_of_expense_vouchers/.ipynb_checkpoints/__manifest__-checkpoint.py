# -*- coding: utf-8 -*-
{
    'name': "de_report_of_expense_vouchers",

    'summary': """Making reports for expense""",

    'description': """
    """,

    'author': "dynexcel.co",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/sbase/data/ir_module_category_data.xml
    # for the full list
    'category': 'Reporting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',	'hr_expense'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/report_expense_views.xml',
        'views/templates.xml',
        'reports/report_of_expense.xml',
        'reports/report.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
