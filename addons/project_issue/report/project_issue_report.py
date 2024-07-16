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
from openerp.addons.crm import crm
AVAILABLE_STATES = [('draft', 'Draft'),
 ('open', 'Open'),
 ('cancel', 'Cancelled'),
 ('done', 'Closed'),
 ('pending', 'Pending')]

class project_issue_report(osv.osv):
    _name = 'project.issue.report'
    _auto = False
    _columns = {'name': fields.char('Year', size=64, required=False, readonly=True),
     'section_id': fields.many2one('crm.case.section', 'Sale Team', readonly=True),
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
     'opening_date': fields.date('Date of Opening', readonly=True),
     'creation_date': fields.date('Creation Date', readonly=True),
     'date_closed': fields.date('Date of Closing', readonly=True),
     'stage_id': fields.many2one('project.task.type', 'Stage'),
     'nbr': fields.integer('# of Issues', readonly=True),
     'working_hours_open': fields.float('Avg. Working Hours to Open', readonly=True, group_operator='avg'),
     'working_hours_close': fields.float('Avg. Working Hours to Close', readonly=True, group_operator='avg'),
     'delay_open': fields.float('Avg. Delay to Open', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to open the project issue.'),
     'delay_close': fields.float('Avg. Delay to Close', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to close the project issue'),
     'company_id': fields.many2one('res.company', 'Company'),
     'priority': fields.selection(crm.AVAILABLE_PRIORITIES, 'Priority'),
     'project_id': fields.many2one('project.project', 'Project', readonly=True),
     'version_id': fields.many2one('project.issue.version', 'Version'),
     'user_id': fields.many2one('res.users', 'Assigned to', readonly=True),
     'partner_id': fields.many2one('res.partner', 'Contact'),
     'channel_id': fields.many2one('crm.case.channel', 'Channel', readonly=True),
     'task_id': fields.many2one('project.task', 'Task'),
     'email': fields.integer('# Emails', size=128, readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'project_issue_report')
        cr.execute("\n            CREATE OR REPLACE VIEW project_issue_report AS (\n                SELECT\n                    c.id as id,\n                    to_char(c.create_date, 'YYYY') as name,\n                    to_char(c.create_date, 'MM') as month,\n                    to_char(c.create_date, 'YYYY-MM-DD') as day,\n                    to_char(c.date_open, 'YYYY-MM-DD') as opening_date,\n                    to_char(c.create_date, 'YYYY-MM-DD') as creation_date,\n                    c.state,\n                    c.user_id,\n                    c.working_hours_open,\n                    c.working_hours_close,\n                    c.section_id,\n                    c.stage_id,\n                    to_char(c.date_closed, 'YYYY-mm-dd') as date_closed,\n                    c.company_id as company_id,\n                    c.priority as priority,\n                    c.project_id as project_id,\n                    c.version_id as version_id,\n                    1 as nbr,\n                    c.partner_id,\n                    c.channel_id,\n                    c.task_id,\n                    date_trunc('day',c.create_date) as create_date,\n                    c.day_open as delay_open,\n                    c.day_close as delay_close,\n                    (SELECT count(id) FROM mail_message WHERE model='project.issue' AND res_id=c.id) AS email\n\n                FROM\n                    project_issue c\n                WHERE c.active= 'true'\n            )")


project_issue_report()