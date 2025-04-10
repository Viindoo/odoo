# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employee Control',
    'version': '1.0',
    'summary': 'Employee Management Software',
    'sequence': 10,
    'description': """Employee Management Software""",
    'category': 'Human Resources/Employees',
    'website': 'https://www.odoomates.tech',
    'depends': ['base', 'web', 'mail'],
    'assets': {
        'web.assets_backend': [
            'hr_manager/static/src/css/employee_view.css',
            'hr_manager/static/src/js/star_rating.js',
            'hr_manager/static/src/xml/star_rating.xml',
            'hr_manager/static/src/js/emoji.js',
            'hr_manager/static/src/xml/emoji.xml',
            'hr_manager/static/src/js/custom_dashboard.js',
            'hr_manager/static/src/xml/custom_dashboard.xml',
        ],
    },
    'data': [
        'security/hr_group.xml',
        'security/ir.model.access.csv',
        'wizard/absence_request_wizard_view.xml',
        'wizard/performance_review_wizard_view.xml',
        'views/custom.xml',
        'views/employee_view.xml',
        'views/employee_task.xml',
        'views/employee_absence.xml',
        'views/employee_training_view.xml',
        'views/employee_review_view.xml',
        'views/employee.xml',
        'reports/employee_task_report.xml',
        'reports/report.xml'
        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
