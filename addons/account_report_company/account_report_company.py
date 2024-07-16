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
from openerp.osv import osv, fields

class res_partner(osv.Model):
    _inherit = 'res.partner'
    _order = 'display_name'

    def _display_name_compute(self, cr, uid, ids, name, args, context = None):
        context = dict(context or {})
        context.pop('show_address', None)
        return dict(self.name_get(cr, uid, ids, context=context))

    _display_name_store_triggers = {'res.partner': (lambda self, cr, uid, ids, context = None: self.search(cr, uid, [('id', 'child_of', ids)]), ['parent_id', 'is_company', 'name'], 10)}
    _display_name = lambda self, *args, **kwargs: self._display_name_compute(*args, **kwargs)
    _columns = {'display_name': fields.function(_display_name, type='char', string='Name', store=_display_name_store_triggers)}


class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    _columns = {'commercial_partner_id': fields.related('partner_id', 'commercial_partner_id', string='Commercial Entity', type='many2one', relation='res.partner', store=True, readonly=True, help='The commercial entity that will be used on Journal Entries for this invoice')}