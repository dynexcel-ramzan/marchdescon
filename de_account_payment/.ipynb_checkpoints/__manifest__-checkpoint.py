# -*- coding: utf-8 -*-
{
    'name': "Account Payment",

    'summary': """
        Payment Form Check Reference
        """,

    'description': """
        Payment Form Check Reference
        1- Reference1
        2- Reference2
        3- Check Number
    """,

    'author': "company",
    'website': "http://www.comapny.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_payment_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
