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
from openerp.tools.safe_eval import safe_eval

class base_config_settings(osv.TransientModel):
    _inherit = 'base.config.settings'
    _columns = {
         'auth_signup_reset_password': fields.boolean('Enable password reset from Login page', help='This allows users to trigger a password reset from the Login page.'),
         'auth_signup_uninvited': fields.boolean('Allow external users to sign up', help='If unchecked, only invited users may sign up.'),
         'auth_signup_template_user_id': fields.many2one('res.users', string='Template user for new users created through signup')
         }

    def get_default_auth_signup_template_user_id(self, cr, uid, fields, context = None):
        icp = self.pool.get('ir.config_parameter')
        return {
             'auth_signup_reset_password': safe_eval(icp.get_param(cr, uid, 'auth_signup.reset_password', 'False')),
             'auth_signup_uninvited': safe_eval(icp.get_param(cr, uid, 'auth_signup.allow_uninvited', 'False')),
             'auth_signup_template_user_id': safe_eval(icp.get_param(cr, uid, 'auth_signup.template_user_id', 'False'))
             }

    def set_auth_signup_template_user_id(self, cr, uid, ids, context = None):
        config = self.browse(cr, uid, ids[0], context=context)
        icp = self.pool.get('ir.config_parameter')
        icp.set_param(cr, uid, 'auth_signup.reset_password', repr(config.auth_signup_reset_password))
        icp.set_param(cr, uid, 'auth_signup.allow_uninvited', repr(config.auth_signup_uninvited))
        icp.set_param(cr, uid, 'auth_signup.template_user_id', repr(config.auth_signup_template_user_id.id))