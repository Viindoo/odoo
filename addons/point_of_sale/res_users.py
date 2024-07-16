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
import math
from openerp.osv import osv, fields
import openerp.addons.product.product

class res_users(osv.osv):
    _inherit = 'res.users'
    _columns = {'ean13': fields.char('EAN13', size=13, help='BarCode'),
     'pos_config': fields.many2one('pos.config', 'Default Point of Sale', domain=[('state', '=', 'active')])}

    def _check_ean(self, cr, uid, ids, context = None):
        return all((openerp.addons.product.product.check_ean(user.ean13) == True for user in self.browse(cr, uid, ids, context=context)))

    def edit_ean(self, cr, uid, ids, context):
        return {'name': 'Edit EAN',
         'type': 'ir.actions.act_window',
         'view_type': 'form',
         'view_mode': 'form',
         'res_model': 'pos.ean_wizard',
         'target': 'new',
         'view_id': False,
         'context': context}

    _constraints = [(_check_ean, 'Error: Invalid ean code', ['ean13'])]