from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PerformanceReviewRequestWizard(models.TransientModel):
    _name = 'performance.review.request.wizard'
    _description = 'Request an Performance Review'


    review_date = fields.Date(required=True, default=fields.Date.today)
    
    employee_id = fields.Many2one('company.employee', string='Employee', required = True)
    reviewer_id = fields.Many2one('company.employee', string='Supervisor', required = True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        return res


    def action_submit(self):
        self.env['employee.performance.review'].create({
            'employee_id': self.employee_id.id,
            'reviewer_id': self.reviewer_id.id,
            'review_date': self.review_date,
        })
