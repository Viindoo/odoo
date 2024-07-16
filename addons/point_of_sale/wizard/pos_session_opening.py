# -*- coding: utf-8 -*-
##############################################################################
#    
#    VNC Developments (India) Pvt. Ltd.
#    Copyright (C) 2004-TODAY VNC (<http://www.vnc.biz>).
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
from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.point_of_sale.point_of_sale import pos_session

class pos_session_opening(osv.osv_memory):
    _name = 'pos.session.opening'
    _columns = {'pos_config_id': fields.many2one('pos.config', 'Point of Sale', required=True),
     'pos_session_id': fields.many2one('pos.session', 'PoS Session'),
     'pos_state': fields.related('pos_session_id', 'state', type='selection', selection=pos_session.POS_SESSION_STATE, string='Session Status', readonly=True),
     'pos_state_str': fields.char('Status', 32, readonly=True),
     'show_config': fields.boolean('Show Config', readonly=True),
     'pos_session_name': fields.related('pos_session_id', 'name', type='char', size=64, readonly=True),
     'pos_session_username': fields.related('pos_session_id', 'user_id', 'name', type='char', size=64, readonly=True)}

    def open_ui(self, cr, uid, ids, context = None):
        context = context or {}
        data = self.browse(cr, uid, ids[0], context=context)
        context['active_id'] = data.pos_session_id.id
        return {'type': 'ir.actions.client',
         'name': _('Start Point Of Sale'),
         'tag': 'pos.ui',
         'context': context}

    def open_existing_session_cb_close(self, cr, uid, ids, context = None):
        wf_service = netsvc.LocalService('workflow')
        wizard = self.browse(cr, uid, ids[0], context=context)
        wf_service.trg_validate(uid, 'pos.session', wizard.pos_session_id.id, 'cashbox_control', cr)
        return self.open_session_cb(cr, uid, ids, context)

    def open_session_cb(self, cr, uid, ids, context = None):
        if not len(ids) == 1:
            raise AssertionError('you can open only one session at a time')
            proxy = self.pool.get('pos.session')
            wizard = self.browse(cr, uid, ids[0], context=context)
            if not wizard.pos_session_id:
                values = {'user_id': uid,
                 'config_id': wizard.pos_config_id.id}
                session_id = proxy.create(cr, uid, values, context=context)
                s = proxy.browse(cr, uid, session_id, context=context)
                return s.state == 'opened' and self.open_ui(cr, uid, ids, context=context)
            return self._open_session(session_id)
        return self._open_session(wizard.pos_session_id.id)

    def open_existing_session_cb(self, cr, uid, ids, context = None):
        raise len(ids) == 1 or AssertionError
        wizard = self.browse(cr, uid, ids[0], context=context)
        return self._open_session(wizard.pos_session_id.id)

    def _open_session(self, session_id):
        return {'name': _('Session'),
         'view_type': 'form',
         'view_mode': 'form,tree',
         'res_model': 'pos.session',
         'res_id': session_id,
         'view_id': False,
         'type': 'ir.actions.act_window'}

    def on_change_config(self, cr, uid, ids, config_id, context = None):
        result = {'pos_session_id': False,
         'pos_state': False,
         'pos_state_str': '',
         'pos_session_username': False,
         'pos_session_name': False}
        if not config_id:
            return {'value': result}
        proxy = self.pool.get('pos.session')
        session_ids = proxy.search(cr, uid, [('state', '!=', 'closed'), ('config_id', '=', config_id), ('user_id', '=', uid)], context=context)
        if session_ids:
            session = proxy.browse(cr, uid, session_ids[0], context=context)
            result['pos_state'] = str(session.state)
            result['pos_state_str'] = dict(pos_session.POS_SESSION_STATE).get(session.state, '')
            result['pos_session_id'] = session.id
            result['pos_session_name'] = session.name
            result['pos_session_username'] = session.user_id.name
        return {'value': result}

    def default_get(self, cr, uid, fieldnames, context = None):
        so = self.pool.get('pos.session')
        session_ids = so.search(cr, uid, [('state', '<>', 'closed'), ('user_id', '=', uid)], context=context)
        if session_ids:
            result = so.browse(cr, uid, session_ids[0], context=context).config_id.id
        else:
            current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            result = current_user.pos_config and current_user.pos_config.id or False
        if not result:
            r = self.pool.get('pos.config').search(cr, uid, [], context=context)
            result = r and r[0] or False
        count = self.pool.get('pos.config').search_count(cr, uid, [('state', '=', 'active')], context=context)
        show_config = bool(count > 1)
        return {'pos_config_id': result,
         'show_config': show_config}


pos_session_opening()