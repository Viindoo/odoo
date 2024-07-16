# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp import tools
from openerp.osv import fields, osv

class hr_evaluation_report(osv.osv):
    _name = 'hr.evaluation.report'
    _description = 'Evaluations Statistics'
    _auto = False
    _columns = {'create_date': fields.date('Create Date', readonly=True),
     'delay_date': fields.float('Delay to Start', digits=(16, 2), readonly=True),
     'overpass_delay': fields.float('Overpassed Deadline', digits=(16, 2), readonly=True),
     'day': fields.char('Day', size=128, readonly=True),
     'deadline': fields.date('Deadline', readonly=True),
     'request_id': fields.many2one('survey.request', 'Request_id', readonly=True),
     'closed': fields.date('closed', readonly=True),
     'year': fields.char('Year', size=4, readonly=True),
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
     'plan_id': fields.many2one('hr_evaluation.plan', 'Plan', readonly=True),
     'employee_id': fields.many2one('hr.employee', 'Employee', readonly=True),
     'rating': fields.selection([('0', 'Significantly bellow expectations'),
                ('1', 'Did not meet expectations'),
                ('2', 'Meet expectations'),
                ('3', 'Exceeds expectations'),
                ('4', 'Significantly exceeds expectations')], 'Overall Rating', readonly=True),
     'nbr': fields.integer('# of Requests', readonly=True),
     'state': fields.selection([('draft', 'Draft'),
               ('wait', 'Plan In Progress'),
               ('progress', 'Final Validation'),
               ('done', 'Done'),
               ('cancel', 'Cancelled')], 'Status', readonly=True)}
    _order = 'create_date desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_evaluation_report')
        cr.execute("\n            create or replace view hr_evaluation_report as (\n                 select\n                     min(l.id) as id,\n                     date_trunc('day',s.create_date) as create_date,\n                     to_char(s.create_date, 'YYYY-MM-DD') as day,\n                     s.employee_id,\n                     l.request_id,\n                     s.plan_id,\n                     s.rating,\n                     s.date as deadline,\n                     s.date_close as closed,\n                     to_char(s.create_date, 'YYYY') as year,\n                     to_char(s.create_date, 'MM') as month,\n                     count(l.*) as nbr,\n                     s.state,\n                     avg(extract('epoch' from age(s.create_date,CURRENT_DATE)))/(3600*24) as  delay_date,\n                     avg(extract('epoch' from age(s.date,CURRENT_DATE)))/(3600*24) as overpass_delay\n                     from\n                 hr_evaluation_interview l\n                LEFT JOIN\n                     hr_evaluation_evaluation s on (s.id=l.evaluation_id)\n                 GROUP BY\n                     s.create_date,\n                     date_trunc('day',s.create_date),\n                     to_char(s.create_date, 'YYYY-MM-DD'),\n                     to_char(s.create_date, 'YYYY'),\n                     to_char(s.create_date, 'MM'),\n                     s.state,\n                     s.employee_id,\n                     s.date,\n                     s.date_close,\n                     l.request_id,\n                     s.rating,\n                     s.plan_id\n            )\n        ")


hr_evaluation_report()