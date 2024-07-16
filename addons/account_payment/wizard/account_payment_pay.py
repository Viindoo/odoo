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
from openerp.osv import osv

class account_payment_make_payment(osv.osv_memory):
    _name = 'account.payment.make.payment'
    _description = 'Account make payment'

    def launch_wizard(self, cr, uid, ids, context = None):
        """
        Search for a wizard to launch according to the type.
        If type is manual. just confirm the order.
        """
        obj_payment_order = self.pool.get('payment.order')
        if context is None:
            context = {}
        obj_payment_order.set_done(cr, uid, [context['active_id']], context)
        return {'type': 'ir.actions.act_window_close'}


account_payment_make_payment()