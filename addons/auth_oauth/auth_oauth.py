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

class auth_oauth_provider(osv.osv):
    """Class defining the configuration values of an OAuth2 provider"""
    _name = 'auth.oauth.provider'
    _description = 'OAuth2 provider'
    _order = 'name'
    _columns = {'name': fields.char('Provider name'),
     'client_id': fields.char('Client ID'),
     'auth_endpoint': fields.char('Authentication URL'),
     'scope': fields.char('Scope'),
     'validation_endpoint': fields.char('Validation URL'),
     'data_endpoint': fields.char('Data URL'),
     'enabled': fields.boolean('Allowed'),
     'css_class': fields.char('CSS class'),
     'body': fields.char('Body'),
     'sequence': fields.integer()}
    _defaults = {'enabled': False}