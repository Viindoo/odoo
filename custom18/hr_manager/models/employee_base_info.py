from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EmployeeBaseInfo(models.AbstractModel):
    _name = 'employee.base.info'
    _description = 'Base Info for Employee Models'
    _abstract = True

    name = fields.Char(string='Name')
    start_date = fields.Datetime(string='Start Date', required = True, default=fields.Date.today)
    end_date = fields.Datetime(string='End Date', required = True, default=fields.Date.today)
    status = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], string='Status', default='ongoing', store = True)
    notes = fields.Text(string='Notes')
    

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError("End date cannot be earlier than start date.")
    
