# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employee Payroll',
    'version': '1.0',
    'summary': 'Employee Payroll Software',
    'sequence': 10,
    'description': """Employee Payroll Software""",
    'category': 'Accounting/Accounting',
    'website': '',
    'depends': ['base', 'web', 'mail', 'hr_manager'],
    'data': [
        'security/ir.model.access.csv',
        'data/payslip_deduction_type_data.xml',
        'views/payslip_deduction_type.xml',
        'views/payslip_view.xml',
        'views/bonus_tag.xml',
        'views/payslip_menu.xml',
        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
