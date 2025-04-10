from odoo import api, fields, models


class EmployeePayslip(models.Model):
    _name = "employee.payslip"
    
    _description = "Employee Payslip"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Text(string='Payslip Title', required=True)
    employee_id = fields.Many2one('company.employee', string='Employee', required=True)
    employee_user_id = fields.Many2one(related='employee_id.user_id', string='User', readonly=True, store=True)
    period_start = fields.Date(string='Period Start', default=fields.Date.today, required=True)
    period_end = fields.Date(string='Period End', default=fields.Date.today, required=True)
    base_salary = fields.Float(related='employee_id.base_salary', string='Base salary', readonly=True)
    bonus = fields.Float(string='Total Bonus', compute='_compute_bonus_tag', store=True)
    bonus_tag_ids = fields.Many2many('bonus.tag', string="Bonuses")
    deduction_ids = fields.One2many('payslip.deduction', 'payslip_id', string='Deductions')
    total_deduction = fields.Float(string='Total Deduction', compute='_compute_net_salary', store=True)
    net_salary = fields.Float(string='Net Salary', compute='_compute_net_salary', store=True)
    day_off = fields.Integer(string='Day off', compute='_compute_attendance', store=True)
    total_days = fields.Integer(string='Total days', compute='_compute_attendance', store=True)
    work_days = fields.Integer(string='Work Days', compute='_compute_attendance', store=True)
    work_hours = fields.Integer(string='Work Hours', compute='_compute_attendance', store=True)
    expected_hours = fields.Float(string='Expected Hours', compute='_compute_attendance', store=True)
    task_completed = fields.Integer(string='Task Completed', compute='_compute_attendance', store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('done', 'Done'),
        ('rejected', 'Rejected')
        ], string='Status', default='draft', tracking=True)
    
    @api.depends('bonus_tag_ids')
    def _compute_bonus_tag(self):
        for bonus in self:
            bonus.bonus = sum(bonus.bonus_tag_ids.mapped('amount'))

    @api.depends('base_salary', 'bonus', 'deduction_ids', 'work_hours', 'expected_hours', 'task_completed')
    def _compute_net_salary(self):
        for emp in self:
            hourly_rate = (emp.base_salary / emp.expected_hours) if emp.expected_hours else 0
            earned_salary = emp.work_hours * hourly_rate
            
            salary_per_day = hourly_rate * 8
            bonus_task = salary_per_day * int(10 / emp.task_completed) if emp.task_completed else 0
            
            total_deduction = sum(line.amount for line in emp.deduction_ids)
            
            emp.total_deduction = total_deduction
            
            emp.net_salary = earned_salary + emp.bonus + bonus_task - total_deduction
            
    @api.depends('employee_id', 'period_start', 'period_end')
    def _compute_attendance(self):
        for emp in self:
            total_days = (emp.period_end - emp.period_start).days + 1
            expected = 30 * 8
            
            day_off_count = self.env['employee.absence'].search_count([
                ('employee_id', '=', emp.employee_id.id),
                ('start_date', '>=', emp.period_start),
                ('start_date', '<=', emp.period_end),
                ])
            
            task_completed_count = self.env['employee.task'].search_count([
                ('employee_id', '=', emp.employee_id.id),
                ('status', '=', 'completed'),
                ('start_date', '>=', emp.period_start),
                ('start_date', '<=', emp.period_end),
                ])
            
            work_days = total_days - day_off_count
            
            emp.expected_hours = expected
            emp.task_completed = task_completed_count
            emp.day_off = day_off_count
            emp.work_days = work_days
            emp.work_hours = work_days * 8
            emp.total_days = total_days

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if not self.deduction_ids:
            default_deductions = self.env['payslip.deduction.type'].search([('auto_apply', '=', True)])
            lines = []
            
            for type in default_deductions:
                lines.append((0, 0, {
                    'type_id': type.id,
                    'amount': type.default_amount,
                    }))
                
            self.deduction_ids = lines
