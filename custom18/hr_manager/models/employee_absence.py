from odoo import api, fields, models

class EmployeeAbsence(models.Model):
    _name = "employee.absence"
    _inherit = ['employee.base.info', 'mail.thread', 'mail.activity.mixin']
    
    _description = "Employee Absence"
    
    
    display_name = fields.Char(compute='_compute_display_name')
    absence_type = fields.Selection([
        ('annual', 'Annual'), 
        ('sick', 'Sick'), 
        ('family issue', 'family issue'),
        ('other', 'Other'),
        ('unpaid', 'Unpaid'),
        ], string='Absence Type', required = True)
    absence_status = fields.Selection([('draft', 'Draft'), 
                              ('refused', 'Refused'),
                              ('approved', 'Approved'), ], default='draft', tracking = True)
    
    employee_id = fields.Many2one('company.employee', string='Employee', required=True)
    
    employee_user_id = fields.Many2one(related='employee_id.user_id', string='Employee(User)', readonly=True, store=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
    
        # Example logic for each created record
        manager_group = self.env.ref('hr_manager.group_employee_manager')
        manager_users = manager_group.users
        partner_ids = manager_users.mapped('partner_id').ids
    
        for record in records:
            if partner_ids:
                record.message_subscribe(partner_ids=partner_ids)
    
        return records

    def action_confirm(self):
        self.absence_status = "approved"
    def action_refuse(self):
        self.absence_status = "refused"
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        user = self.env.user
        employee = self.env['company.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee:
            res['employee_id'] = employee.id
        return res  
    @api.depends('employee_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.employee_id.user_id.name}"