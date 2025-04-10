from odoo import api, fields, models
from odoo.exceptions import ValidationError
from openai import OpenAI


class EmployeeTask(models.Model):
    _name = "employee.task"
    _inherit = ['employee.base.info', 'mail.thread', 'mail.activity.mixin']
    _order = "priority desc"
    
    _description = "Employee Task"
    
    difficulty = fields.Selection([
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
        ], string='Difficulty', required=True, tracking=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('urgent', 'Urgent'),
        ], string='Priority', required=True, tracking=True)
    status = fields.Selection(tracking=True)
    user_image = fields.Binary(related='employee_id.user_id.image_1920', string="User Image", store=False)
    subtask_suggestions = fields.Text(string='AI Suggested Subtasks')
    manager = fields.Boolean(string="Manager")
    
    employee_id = fields.Many2one('company.employee', string='Employee', required=True, tracking=True)
    
    employee_user_id = fields.Many2one(related='employee_id.user_id', string='Employee(User)', readonly=True, store=True)
    active = fields.Boolean(string='Active', default=True)
    
    # tự follow user trong chat khi được tạo task
    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
    
        if record.employee_id and record.employee_id.user_id:
            partner = record.employee_id.user_id.partner_id
            record.message_subscribe(partner_ids=[partner.id])
    
        return record

    def action_confirm(self):
        self.status = 'completed'
        
    def unlink(self):
        if self.status == "completed":
            raise ValidationError("Task Completed cannot be delete")
        return super(EmployeeTask, self).unlink()

    def get_manger_group(self):
        is_manager = self.env.user.has_group('hr_manager.group_employee_manager')
        for i in is_manager:
            i.manager = is_manager
    
    def action_generate_subtasks(self):
        for task in self:
            api_key = self.env['ir.config_parameter'].sudo().get_param('openai.api_key')
            if not api_key:
                task.subtask_suggestions = "OpenAI API key is missing."
                continue
    
            try:
                client = OpenAI(api_key=api_key)
    
                prompt = (
                    f"You are a productivity assistant. Brainstorm and break following task into small task so user can work efficiently. "
                    f"Each subtask should have a brief description and a due date.\n\n"
                    f"Task title: {task.name or 'Untitled'}\n"
                    f"Notes: {task.notes or 'No additional notes'}\n"
                    f"Start date: {task.start_date.strftime('%Y-%m-%d')} (YYYY-MM-DD format)\n"
                    f"End date: {task.end_date.strftime('%Y-%m-%d')} (YYYY-MM-DD format)\n\n"
                    f"Spread the subtask due dates logically between the start and end dates. "
                    f"Due <= End date "
                    f"⚠️ IMPORTANT: Each subtask MUST include a time (e.g., 09:00 or 14:30) in the format YYYY-MM-DD HH:MM. Do not skip the time.\n\n"
                    f"Distribute the deadlines evenly between the start and end date. Assume 8:00–18:00 working hours.\n\n"
                    f"Make sure they are evenly spaced and in chronological order.\n\n"
                    f"Example format:\n"
                    f"Task title: {task.name or 'Untitled'}\n"
                    f"---------------------------------------"
                    f"- Subtask 1: [Action]\n (Due: YYYY-MM-DD HH:MM)\n"
                    f"- Subtask 2: ...\n\n"
                    f"Example:\n"
                    f"Task title: Build module\n"
                    f"---------------------------------------"
                    f"- Subtask 1: Design the product form\n (Due: 2025-03-05 09:00)\n"
                    f"- Subtask 2: Build the model and backend logic\n (Due: 2025-03-07 14:00)\n"
                    f"- Subtask 3: Test and deploy\n (Due: 2025-03-09 10:00)\n"
                    f"Respond only with the list. No extra explanation."
                    f"Keep your output clear, use bullet points"
                )
    
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=200,
                )
    
                suggestion = response.choices[0].message.content.strip()
                task.subtask_suggestions = suggestion
    
            except Exception as e:
                task.subtask_suggestions = f"Error: {str(e)}"

