from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EmployeePerformanceReview(models.Model):
    _name = 'employee.performance.review'

    _description = 'Employee Performance Review'
    
    review_date = fields.Date(string='Review Date', default=fields.Date.today, required=True)
    score = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Score')
    status = fields.Selection([
        ('on wait', 'On Wait'),
        ('finished', 'Finished'),
    ], string='Status', default='on wait')
    notes = fields.Text(string = 'Notes')
    display_name = fields.Char(compute='_compute_display_name')
    
    employee_id = fields.Many2one('company.employee', string='Employee', required = True)
    reviewer_id = fields.Many2one('company.employee', string='Supervisor', required = True)

    employee_user_id = fields.Many2one(related='employee_id.user_id', string='Employee(User)', readonly=True, store=True)
    reviewer_user_id = fields.Many2one(related='reviewer_id.user_id', string='Supervisor(User)', readonly=True, store=True)

    @api.constrains('employee_user_id', 'reviewer_user_id')
    def check_review_self(self):
        for record in self:
            if record.employee_user_id == record.reviewer_user_id:
                raise ValidationError("An employee cannot review themselves.")
            
    @api.depends('employee_id', 'reviewer_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.employee_id.user_id.name} - {rec.reviewer_id.user_id.name}"