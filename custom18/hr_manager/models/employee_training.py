from odoo import api, fields, models
import logging

class EmployeeTraining(models.Model):
    _name = 'employee.training'
    _inherit = 'employee.base.info'

    _description = 'Employee Training'

    provider = fields.Char(string='Provider', required = True)
    employee_ids = fields.Many2many('company.employee', string='Attendees')
    