from odoo import api, fields, models

class EmployeeExperience(models.Model):
    _name = 'employee.experience'
    _inherit = 'employee.base.info'

    _description = 'Employee Experience'

    job_title = fields.Char(string='Job Title')
    employee_id = fields.Many2one('company.employee', string='Employee')
