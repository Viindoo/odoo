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
from openerp.osv import fields, osv
from openerp import tools
from .. import crm
AVAILABLE_STATES = [('draft', 'Draft'),
 ('open', 'Open'),
 ('cancel', 'Cancelled'),
 ('done', 'Closed'),
 ('pending', 'Pending')]
MONTHS = [('01', 'January'),
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
 ('12', 'December')]

class crm_lead_report(osv.osv):
    """ CRM Lead Analysis """
    _name = 'crm.lead.report'
    _auto = False
    _description = 'CRM Lead Analysis'
    _rec_name = 'deadline_day'
    _columns = {'deadline_year': fields.char('Ex. Closing Year', size=10, readonly=True, help='Expected closing year'),
     'deadline_month': fields.selection(MONTHS, 'Exp. Closing Month', readonly=True, help='Expected closing month'),
     'deadline_day': fields.char('Exp. Closing Day', size=10, readonly=True, help='Expected closing day'),
     'creation_year': fields.char('Creation Year', size=10, readonly=True, help='Creation year'),
     'creation_month': fields.selection(MONTHS, 'Creation Month', readonly=True, help='Creation month'),
     'creation_day': fields.char('Creation Day', size=10, readonly=True, help='Creation day'),
     'create_date': fields.datetime('Create Date', readonly=True),
     'opening_date': fields.date('Opening Date', readonly=True),
     'date_closed': fields.date('Close Date', readonly=True),
     'delay_open': fields.float('Delay to Open', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to open the case'),
     'delay_close': fields.float('Delay to Close', digits=(16, 2), readonly=True, group_operator='avg', help='Number of Days to close the case'),
     'delay_expected': fields.float('Overpassed Deadline', digits=(16, 2), readonly=True, group_operator='avg'),
     'user_id': fields.many2one('res.users', 'User', readonly=True),
     'country_id': fields.many2one('res.country', 'Country', readonly=True),
     'section_id': fields.many2one('crm.case.section', 'Sales Team', readonly=True),
     'channel_id': fields.many2one('crm.case.channel', 'Channel', readonly=True),
     'type_id': fields.many2one('crm.case.resource.type', 'Campaign', readonly=True),
     'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'probability': fields.float('Probability', digits=(16, 2), readonly=True, group_operator='avg'),
     'planned_revenue': fields.float('Planned Revenue', digits=(16, 2), readonly=True),
     'probable_revenue': fields.float('Probable Revenue', digits=(16, 2), readonly=True),
     'stage_id': fields.many2one('crm.case.stage', 'Stage', readonly=True, domain="[('section_ids', '=', section_id)]"),
     'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
     'nbr': fields.integer('# of Cases', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'priority': fields.selection(crm.AVAILABLE_PRIORITIES, 'Priority'),
     'type': fields.selection([('lead', 'Lead'), ('opportunity', 'Opportunity')], 'Type', help='Type is used to separate Leads and Opportunities')}

    def init(self, cr):
        """
            CRM Lead Report
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'crm_lead_report')
        cr.execute("\n            CREATE OR REPLACE VIEW crm_lead_report AS (\n                SELECT\n                    id,\n\n                    to_char(c.date_deadline, 'YYYY') as deadline_year,\n                    to_char(c.date_deadline, 'MM') as deadline_month,\n                    to_char(c.date_deadline, 'YYYY-MM-DD') as deadline_day,\n\n                    to_char(c.create_date, 'YYYY') as creation_year,\n                    to_char(c.create_date, 'MM') as creation_month,\n                    to_char(c.create_date, 'YYYY-MM-DD') as creation_day,\n\n                    to_char(c.date_open, 'YYYY-MM-DD') as opening_date,\n                    to_char(c.date_closed, 'YYYY-mm-dd') as date_closed,\n\n                    c.state,\n                    c.user_id,\n                    c.probability,\n                    c.stage_id,\n                    c.type,\n                    c.company_id,\n                    c.priority,\n                    c.section_id,\n                    c.channel_id,\n                    c.type_id,\n                    c.partner_id,\n                    c.country_id,\n                    c.planned_revenue,\n                    c.planned_revenue*(c.probability/100) as probable_revenue,\n                    1 as nbr,\n                    date_trunc('day',c.create_date) as create_date,\n                    extract('epoch' from (c.date_closed-c.create_date))/(3600*24) as  delay_close,\n                    abs(extract('epoch' from (c.date_deadline - c.date_closed))/(3600*24)) as  delay_expected,\n                    extract('epoch' from (c.date_open-c.create_date))/(3600*24) as  delay_open\n                FROM\n                    crm_lead c\n                WHERE c.active = 'true'\n            )")


crm_lead_report()