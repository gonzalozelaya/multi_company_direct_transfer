# -*- coding: utf-8 -*-
{
    'name': "Multicompany direct transfer",

    'summary': """
        This module allows """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/direct_transfer_views.xml',
        'data/stock_picking_transfer_sequence.xml',
        'reports/report_tranfers.xml',
   ],
}