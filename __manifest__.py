# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name':
    'Pricelist by Zoning',
    'description':
    'Pricelist by Zoning',
    'category':
    'Sales',
    'version':
    '10.0.1.0.1',
    'author':
    'Shepilov Vladislav <shepilov.v@protonmail.com>',
    'data': [
        # Data
        'data/product_zone1_code_data.xml',
        'data/product_zone2_code_data.xml',
        'data/product_zone3_code_data.xml',
        'data/product_zone4_code_data.xml',
        'data/product_zone5_code_data.xml',
        'data/product_zone_data.xml',
        # Views
        'views/product_zone_code_views.xml',
        'views/product_zone_views.xml',
        'views/product_pricelist_zoning_item_views.xml',
        'views/product_pricelist_zoning_views.xml',
        'views/menu_view.xml',
        'views/product_view.xml',
        # Templates
        'views/templates.xml',
    ],
    'demo': [],
    'depends': [
        'base',
        'product',
        'delivery',
        'sales_team',
        'multiple_signup',
        'edulux_upgrade',
    ],
    'license':
    'OPL-1',
}
