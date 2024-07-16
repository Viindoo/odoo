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
from osv import osv, fields
AVAILABLE_STATES = [('draft', 'New'),
 ('cancel', 'Cancelled'),
 ('open', 'In Progress'),
 ('pending', 'Pending'),
 ('done', 'Closed')]

class lead_test(osv.Model):
    _name = 'base.action.rule.lead.test'
    _columns = {'name': fields.char('Subject', size=64, required=True, select=1),
     'user_id': fields.many2one('res.users', 'Responsible'),
     'state': fields.selection(AVAILABLE_STATES, string='Status', readonly=True),
     'active': fields.boolean('Active', required=False),
     'partner_id': fields.many2one('res.partner', 'Partner', ondelete='set null'),
     'date_action_last': fields.datetime('Last Action', readonly=1)}
    _defaults = {'state': 'draft',
     'active': True}

    def message_post(self, cr, uid, thread_id, body = '', subject = None, type = 'notification', subtype = None, parent_id = False, attachments = None, context = None, **kwargs):
        pass

    def message_subscribe(self, cr, uid, ids, partner_ids, subtype_ids = None, context = None):
        pass