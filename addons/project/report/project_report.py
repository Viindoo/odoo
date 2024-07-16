# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
from openerp import tools

class report_project_task_user(osv.osv):
    _name = 'report.project.task.user'
    _description = 'Tasks by user and project'
    _auto = False
    _columns = {'name': fields.char('Task Summary', size=128, readonly=True),
     'day': fields.char('Day', size=128, readonly=True),
     'year': fields.char('Year', size=64, required=False, readonly=True),
     'user_id': fields.many2one('res.users', 'Assigned To', readonly=True),
     'date_start': fields.date('Starting Date', readonly=True),
     'no_of_days': fields.integer('# of Days', size=128, readonly=True),
     'date_end': fields.date('Ending Date', readonly=True),
     'date_deadline': fields.date('Deadline', readonly=True),
     'project_id': fields.many2one('project.project', 'Project', readonly=True),
     'hours_planned': fields.float('Planned Hours', readonly=True),
     'hours_effective': fields.float('Effective Hours', readonly=True),
     'hours_delay': fields.float('Avg. Plan.-Eff.', readonly=True),
     'remaining_hours': fields.float('Remaining Hours', readonly=True),
     'progress': fields.float('Progress', readonly=True, group_operator='avg'),
     'total_hours': fields.float('Total Hours', readonly=True),
     'closing_days': fields.float('Days to Close', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to close the task'),
     'opening_days': fields.float('Days to Open', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to Open the task'),
     'delay_endings_days': fields.float('Overpassed Deadline', digits=(16, 2), readonly=True),
     'nbr': fields.integer('# of tasks', readonly=True),
     'priority': fields.selection([('4', 'Very Low'),
                  ('3', 'Low'),
                  ('2', 'Medium'),
                  ('1', 'Urgent'),
                  ('0', 'Very urgent')], 'Priority', readonly=True),
     'month': fields.selection([('01', 'January'),
               ('02', 'February'),
               ('03', 'March'),
               ('04', 'April'),
               ('05', 'May'),
               ('06', 'June'),
               ('07', 'July'),
               ('08', 'August'),
               ('09', 'September'),
               ('10', 'October'),
               ('11', 'November'),
               ('12', 'December')], 'Month', readonly=True),
     'state': fields.selection([('draft', 'Draft'),
               ('open', 'In Progress'),
               ('pending', 'Pending'),
               ('cancelled', 'Cancelled'),
               ('done', 'Done')], 'Status', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'partner_id': fields.many2one('res.partner', 'Contact', readonly=True)}
    _order = 'name desc, project_id'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'report_project_task_user')
        cr.execute("\n            CREATE view report_project_task_user as\n              SELECT\n                    (select 1 ) AS nbr,\n                    t.id as id,\n                    to_char(date_start, 'YYYY') as year,\n                    to_char(date_start, 'MM') as month,\n                    to_char(date_start, 'YYYY-MM-DD') as day,\n                    date_trunc('day',t.date_start) as date_start,\n                    date_trunc('day',t.date_end) as date_end,\n                    to_date(to_char(t.date_deadline, 'dd-MM-YYYY'),'dd-MM-YYYY') as date_deadline,\n--                    sum(cast(to_char(date_trunc('day',t.date_end) - date_trunc('day',t.date_start),'DD') as int)) as no_of_days,\n                    abs((extract('epoch' from (t.date_end-t.date_start)))/(3600*24))  as no_of_days,\n                    t.user_id,\n                    progress as progress,\n                    t.project_id,\n                    t.state,\n                    t.effective_hours as hours_effective,\n                    t.priority,\n                    t.name as name,\n                    t.company_id,\n                    t.partner_id,\n                    t.stage_id,\n                    remaining_hours as remaining_hours,\n                    total_hours as total_hours,\n                    t.delay_hours as hours_delay,\n                    planned_hours as hours_planned,\n                    (extract('epoch' from (t.date_end-t.create_date)))/(3600*24)  as closing_days,\n                    (extract('epoch' from (t.date_start-t.create_date)))/(3600*24)  as opening_days,\n                    abs((extract('epoch' from (t.date_deadline-t.date_end)))/(3600*24))  as delay_endings_days\n              FROM project_task t\n                WHERE t.active = 'true'\n                GROUP BY\n                    t.id,\n                    remaining_hours,\n                    t.effective_hours,\n                    progress,\n                    total_hours,\n                    planned_hours,\n                    hours_delay,\n                    year,\n                    month,\n                    day,\n                    create_date,\n                    date_start,\n                    date_end,\n                    date_deadline,\n                    t.user_id,\n                    t.project_id,\n                    t.state,\n                    t.priority,\n                    name,\n                    t.company_id,\n                    t.partner_id,\n                    t.stage_id\n\n        ")


report_project_task_user()