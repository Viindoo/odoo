from odoo import api, fields, models
from datetime import datetime
import string


class CompanyEmployee(models.Model):
    _name = 'company.employee'
    _description = 'Company Employee'
    _rec_name = 'user_id'
    
    _sql_constraints = [(
        'unique_user_id',
        'UNIQUE(user_id)',
        'Employee is already created!'
    )]
    age = fields.Char(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Char(string='Address', required=True)
    phone = fields.Char(string='Phone No.', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    image = fields.Binary(string='Profile Picture', attachment=True)
    job_title = fields.Selection([
        ('intern', 'Intern'),
        ('fresher', 'Fresher'),
        ('junior', 'Junior Developer'),
        ('mid', 'Mid-level Developer'),
        ('senior', 'Senior Developer'),
        ('lead', 'Team Lead'),
        ('manager', 'Manager')
    ], string='Job Title', required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.ref('base.VND'))
    base_salary = fields.Float(string='Base Salary', default='25805000')
    salary = fields.Monetary(string='Salary', compute='_compute_salary', store=True, currency_field='currency_id')
    active = fields.Boolean(string="Active", default=True)
    notes = fields.Text(string='Description')
    attitude = fields.Char(string='Satisfaction')
    rating = fields.Float(string='Rating')
    task_count = fields.Integer(string='Task Count', compute="_compute_task")
    training_count = fields.Integer(string='Training Count', compute="_compute_training")
    review_count = fields.Integer(string='Review Count', compute="_compute_review")
    
    user_image = fields.Binary(related='user_id.image_1920', string="User Image", readonly=True)
    
    user_id = fields.Many2one('res.users', string='User')
    expertise_id = fields.One2many('employee.expertise', 'employee_id', string='Expertise')
    certification_id = fields.One2many('employee.certification', 'employee_id', string='Certification')
    training_id = fields.One2many('employee.training', 'employee_ids', string='Training')
    experience_id = fields.One2many('employee.experience', 'employee_id', string='Experience')
    task_id = fields.One2many('employee.task', 'employee_id', string='Task')
    absence_id = fields.One2many('employee.absence', 'employee_id', string='Absence')
    performance_review_id = fields.One2many('employee.performance.review', 'employee_id', string='Employee')
    reviewer_id = fields.One2many('employee.performance.review', 'reviewer_id', string='Supervisor')
    
    def _compute_task(self):
        for employee in self:
            employee.task_count = self.env['employee.task'].search_count([
                ('employee_id', '=', employee.id)
            ])

    def _compute_training(self):
        for employee in self:
            employee.training_count = self.env['employee.training'].search_count([
                ('employee_ids', '=', employee.id)
            ])

    def _compute_review(self):
        for employee in self:
            employee.review_count = self.env['employee.performance.review'].search_count([
                ('employee_id', '=', employee.id)
            ])
    
    def action_open_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'employee.task',
            'view_mode': 'list,form,calendar',
            'target': 'current',
            'domain': [('employee_id', '=', self.id)],
        }

    def action_open_training(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Training',
            'res_model': 'employee.training',
            'domain': [('employee_ids', '=', self.id)],
            'view_mode': 'list,form,calendar',
            'target': 'current',
            }

    def action_open_review(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Performance Review',
            'res_model': 'employee.performance.review',
            'domain': [('employee_id', '=', self.id)],
            'view_mode': 'list,form,calendar',
            'target': 'current',
            }

    @api.depends('job_title')
    def _compute_salary(self):
        multiplier_map = {
            'intern': 0.5,
            'fresher': 1.0,
            'junior': 1.5,
            'mid': 2.0,
            'senior': 2.5,
            'lead': 3.0,
            'manager': 4.0
            }
        for employee in self:
            multiplier = multiplier_map.get(employee.job_title, 0.5)
            employee.salary = employee.base_salary * multiplier

    @api.depends('date_of_birth')
    def _compute_age(self):
        for employee in self:
            current = datetime.today()
            current_year = current.year
            if employee.date_of_birth:
               employee.age = current_year - employee.date_of_birth.year
            else:
               employee.age = 0   
