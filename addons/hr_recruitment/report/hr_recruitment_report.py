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
from .. import hr_recruitment
from openerp.addons.decimal_precision import decimal_precision as dp
AVAILABLE_STATES = [('draft', 'New'),
 ('open', 'Open'),
 ('cancel', 'Refused'),
 ('done', 'Hired'),
 ('pending', 'Pending')]

class hr_recruitment_report(osv.osv):
    _name = 'hr.recruitment.report'
    _description = 'Recruitments Statistics'
    _auto = False
    _rec_name = 'date'
    _columns = {'user_id': fields.many2one('res.users', 'User', readonly=True),
     'nbr': fields.integer('# of Applications', readonly=True),
     'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),
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
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'day': fields.char('Day', size=128, readonly=True),
     'year': fields.char('Year', size=4, readonly=True),
     'date': fields.date('Date', readonly=True),
     'date_closed': fields.date('Closed', readonly=True),
     'job_id': fields.many2one('hr.job', 'Applied Job', readonly=True),
     'stage_id': fields.many2one('hr.recruitment.stage', 'Stage'),
     'type_id': fields.many2one('hr.recruitment.degree', 'Degree'),
     'department_id': fields.many2one('hr.department', 'Department', readonly=True),
     'priority': fields.selection(hr_recruitment.AVAILABLE_PRIORITIES, 'Appreciation'),
     'salary_prop': fields.float('Salary Proposed', digits_compute=dp.get_precision('Account')),
     'salary_prop_avg': fields.float('Avg. Proposed Salary', group_operator='avg', digits_compute=dp.get_precision('Account')),
     'salary_exp': fields.float('Salary Expected', digits_compute=dp.get_precision('Account')),
     'salary_exp_avg': fields.float('Avg. Expected Salary', group_operator='avg', digits_compute=dp.get_precision('Account')),
     'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
     'available': fields.float('Availability'),
     'delay_close': fields.float('Avg. Delay to Close', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to close the project issue')}
    _order = 'date desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_recruitment_report')
        cr.execute("\n            create or replace view hr_recruitment_report as (\n                 select\n                     min(s.id) as id,\n                     date_trunc('day',s.create_date) as date,\n                     date_trunc('day',s.date_closed) as date_closed,\n                     to_char(s.create_date, 'YYYY') as year,\n                     to_char(s.create_date, 'MM') as month,\n                     to_char(s.create_date, 'YYYY-MM-DD') as day,\n                     s.state,\n                     s.partner_id,\n                     s.company_id,\n                     s.user_id,\n                     s.job_id,\n                     s.type_id,\n                     sum(s.availability) as available,\n                     s.department_id,\n                     s.priority,\n                     s.stage_id,\n                     sum(salary_proposed) as salary_prop,\n                     (sum(salary_proposed)/count(*)) as salary_prop_avg,\n                     sum(salary_expected) as salary_exp,\n                     (sum(salary_expected)/count(*)) as salary_exp_avg,\n                     extract('epoch' from (s.date_closed-s.create_date))/(3600*24) as  delay_close,\n                     count(*) as nbr\n                 from hr_applicant s\n                 group by\n                     to_char(s.create_date, 'YYYY'),\n                     to_char(s.create_date, 'MM'),\n                     to_char(s.create_date, 'YYYY-MM-DD') ,\n                     date_trunc('day',s.create_date),\n                     date_trunc('day',s.date_closed),\n                     s.date_open,\n                     s.create_date,\n                     s.date_closed,\n                     s.state,\n                     s.partner_id,\n                     s.company_id,\n                     s.user_id,\n                     s.stage_id,\n                     s.type_id,\n                     s.priority,\n                     s.job_id,\n                     s.department_id\n            )\n        ")


hr_recruitment_report()