from odoo import api, fields, models

class EmployeeExpertise(models.Model):
    _name = 'employee.expertise'
    _description = 'Employee Expertise'
    
    name = fields.Char(string = 'Skill', required = True)
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
        ], string = 'Level', required = True)
    years_of_experience = fields.Integer(string = 'Year of Experience', required = True)
    
    employee_id = fields.Many2one('company.employee', string = 'Employee')
