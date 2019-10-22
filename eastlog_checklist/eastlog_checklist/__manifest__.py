# -*- coding: utf-8 -*-
{
    'name': "eastlog_checklist",

    'summary': """
        This module is used for Eastlog Checklist project""",

    'description': """
        It helps Admin follows Site Supervisors activities,
        and collect data from Site Supervisors.
    """,

    'author': "Appex",
    'website': "http://appex.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_rest', 'component', 'project', 'mail', 'eastlog_job_request'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/activity_type_data.xml',
        'views/checklist_menu.xml',
        # 'views/job_request_view.xml',
        'views/checklist_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'external_dependencies': {
        'python': [
            'jsondiff'
        ],
    },
}
