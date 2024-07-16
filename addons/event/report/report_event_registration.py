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

class report_event_registration(osv.osv):
    _name = 'report.event.registration'
    _description = 'Events Analysis'
    _auto = False
    _columns = {'event_date': fields.char('Event Start Date', size=64, readonly=True),
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
     'event_id': fields.many2one('event.event', 'Event', required=True),
     'draft_state': fields.integer(' # No of Draft Registrations', size=20),
     'confirm_state': fields.integer(' # No of Confirmed Registrations', size=20),
     'register_max': fields.integer('Maximum Registrations'),
     'nbevent': fields.integer('Number Of Events'),
     'event_type': fields.many2one('event.type', 'Event Type'),
     'registration_state': fields.selection([('draft', 'Draft'),
                            ('confirm', 'Confirmed'),
                            ('done', 'Attended'),
                            ('cancel', 'Cancelled')], 'Registration State', readonly=True, required=True),
     'event_state': fields.selection([('draft', 'Draft'),
                     ('confirm', 'Confirmed'),
                     ('done', 'Done'),
                     ('cancel', 'Cancelled')], 'Event State', readonly=True, required=True),
     'user_id': fields.many2one('res.users', 'Event Responsible', readonly=True),
     'user_id_registration': fields.many2one('res.users', 'Register', readonly=True),
     'name_registration': fields.char('Participant / Contact Name', size=45, readonly=True),
     'speaker_id': fields.many2one('res.partner', 'Speaker', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True)}
    _order = 'event_date desc'

    def init(self, cr):
        """
        Initialize the sql view for the event registration
        """
        tools.drop_view_if_exists(cr, 'report_event_registration')
        cr.execute(" CREATE VIEW report_event_registration AS (\n            SELECT\n                e.id::char || '/' || coalesce(r.id::char,'') AS id,\n                e.id AS event_id,\n                e.user_id AS user_id,\n                r.user_id AS user_id_registration,\n                r.name AS name_registration,\n                e.company_id AS company_id,\n                e.main_speaker_id AS speaker_id,\n                to_char(e.date_begin, 'YYYY-MM-DD') AS event_date,\n                to_char(e.date_begin, 'YYYY') AS year,\n                to_char(e.date_begin, 'MM') AS month,\n                count(e.id) AS nbevent,\n                CASE WHEN r.state IN ('draft') THEN r.nb_register ELSE 0 END AS draft_state,\n                CASE WHEN r.state IN ('open','done') THEN r.nb_register ELSE 0 END AS confirm_state,\n                e.type AS event_type,\n                e.register_max AS register_max,\n                e.state AS event_state,\n                r.state AS registration_state\n            FROM\n                event_event e\n                LEFT JOIN event_registration r ON (e.id=r.event_id)\n\n            GROUP BY\n                event_id,\n                user_id_registration,\n                r.id,\n                registration_state,\n                r.nb_register,\n                event_type,\n                e.id,\n                e.date_begin,\n                e.user_id,\n                event_state,\n                e.company_id,\n                e.main_speaker_id,\n                year,\n                month,\n                e.register_max,\n                name_registration\n        )\n        ")


report_event_registration()