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
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.account.wizard.pos_box import CashBox

class PosBox(CashBox):
    _register = False

    def run(self, cr, uid, ids, context = None):
        if not context:
            context = dict()
        active_model = context.get('active_model', False) or False
        active_ids = context.get('active_ids', []) or []
        if active_model == 'pos.session':
            records = self.pool.get(active_model).browse(cr, uid, active_ids, context=context)
            bank_statements = [ record.cash_register_id for record in records if record.cash_register_id ]
            if not bank_statements:
                raise osv.except_osv(_('Error!'), _('There is no cash register for this PoS Session'))
            return self._run(cr, uid, ids, bank_statements, context=context)
        else:
            return super(PosBox, self).run(cr, uid, ids, context=context)


class PosBoxIn(PosBox):
    _inherit = 'cash.box.in'

    def _compute_values_for_statement_line(self, cr, uid, box, record, context = None):
        if context is None:
            context = {}
        values = super(PosBoxIn, self)._compute_values_for_statement_line(cr, uid, box, record, context=context)
        active_model = context.get('active_model', False) or False
        active_ids = context.get('active_ids', []) or []
        if active_model == 'pos.session':
            session = self.pool.get(active_model).browse(cr, uid, active_ids, context=context)[0]
            values['ref'] = session.name
        return values


class PosBoxOut(PosBox):
    _inherit = 'cash.box.out'

    def _compute_values_for_statement_line(self, cr, uid, box, record, context = None):
        values = super(PosBoxOut, self)._compute_values_for_statement_line(cr, uid, box, record, context=context)
        active_model = context.get('active_model', False) or False
        active_ids = context.get('active_ids', []) or []
        if active_model == 'pos.session':
            session = self.pool.get(active_model).browse(cr, uid, active_ids, context=context)[0]
            values['ref'] = session.name
        return values