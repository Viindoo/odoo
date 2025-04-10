from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AbsenceRequestWizard(models.TransientModel):
    _name = 'absence.request.wizard'
    _description = 'Request an Absence'

    absence_type = fields.Selection([
        ('annual', 'Annual'),
        ('sick', 'Sick'),
        ('family issue', 'Family Issue'),
        ('unpaid', 'Unpaid'),
        ('other', 'Other'),
    ], required=True)

    start_date = fields.Date(required=True, default=fields.Date.today)
    end_date = fields.Date(required=True, default=fields.Date.today)
    notes = fields.Text()

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        return res

    def action_submit(self):
        employee = self.env['company.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not employee:
            raise ValidationError("You must be linked to an employee to submit an absence.")
        
        self.env['employee.absence'].create({
            'employee_id': employee.id,
            'absence_type': self.absence_type,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'notes': self.notes,
        })
    
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Absences',
            'res_model': 'employee.absence',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('employee_id.user_id', '=', self.env.user.id)],
        }
