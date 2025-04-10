from odoo import api, fields, models

class EmployeeCertification(models.Model):
    _name = 'employee.certification'
    _description = 'Employee Certification'
    
    name = fields.Char(string='Certification Name', required = True)
    issuer = fields.Char(string = 'Issuer')
    date_obtained = fields.Date(string = 'Date Obtained', default=fields.Date.today)
    valid_until = fields.Date(string = 'Expired Date', default=fields.Date.today)
    attachment = fields.Binary(string = 'Attachment')
    file_name = fields.Char(string = 'Filename')
    
    employee_id = fields.Many2one('company.employee', string = 'employee_id')