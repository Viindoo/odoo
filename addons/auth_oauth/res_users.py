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
import logging
import urllib
import urlparse
import urllib2
import simplejson
import openerp
from openerp.osv import osv, fields
from openerp import SUPERUSER_ID
_logger = logging.getLogger(__name__)

class res_users(osv.Model):
    _inherit = 'res.users'
    _columns = {'oauth_provider_id': fields.many2one('auth.oauth.provider', 'OAuth Provider'),
     'oauth_uid': fields.char('OAuth User ID', help='Oauth Provider user_id'),
     'oauth_access_token': fields.char('OAuth Access Token', readonly=True)}
    _sql_constraints = [('uniq_users_oauth_provider_oauth_uid', 'unique(oauth_provider_id, oauth_uid)', 'OAuth UID must be unique per provider')]

    def _auth_oauth_rpc(self, cr, uid, endpoint, access_token, context = None):
        params = urllib.urlencode({'access_token': access_token})
        if urlparse.urlparse(endpoint)[4]:
            url = endpoint + '&' + params
        else:
            url = endpoint + '?' + params
        f = urllib2.urlopen(url)
        response = f.read()
        return simplejson.loads(response)

    def _auth_oauth_validate(self, cr, uid, provider, access_token, context = None):
        """ return the validation data corresponding to the access token """
        p = self.pool.get('auth.oauth.provider').browse(cr, uid, provider, context=context)
        validation = self._auth_oauth_rpc(cr, uid, p.validation_endpoint, access_token)
        if validation.get('error'):
            raise Exception(validation['error'])
        if p.data_endpoint:
            data = self._auth_oauth_rpc(cr, uid, p.data_endpoint, access_token)
            validation.update(data)
        return validation

    def _auth_oauth_signin(self, cr, uid, provider, validation, params, context = None):
        """ retrieve and sign in the user corresponding to provider and validated access token
            :param provider: oauth provider id (int)
            :param validation: result of validation of access token (dict)
            :param params: oauth parameters (dict)
            :return: user login (str)
            :raise: openerp.exceptions.AccessDenied if signin failed
        
            This method can be overridden to add alternative signin methods.
        """
        oauth_uid = validation['user_id']
        user_ids = self.search(cr, uid, [('oauth_uid', '=', oauth_uid), ('oauth_provider_id', '=', provider)])
        if not user_ids:
            raise openerp.exceptions.AccessDenied()
        raise len(user_ids) == 1 or AssertionError
        user = self.browse(cr, uid, user_ids[0], context=context)
        user.write({'oauth_access_token': params['access_token']})
        return user.login

    def auth_oauth(self, cr, uid, provider, params, context = None):
        access_token = params.get('access_token')
        validation = self._auth_oauth_validate(cr, uid, provider, access_token)
        if not validation.get('user_id'):
            raise openerp.exceptions.AccessDenied()
        login = self._auth_oauth_signin(cr, uid, provider, validation, params, context=context)
        if not login:
            raise openerp.exceptions.AccessDenied()
        return (cr.dbname, login, access_token)

    def check_credentials(self, cr, uid, password):
        try:
            return super(res_users, self).check_credentials(cr, uid, password)
        except openerp.exceptions.AccessDenied:
            res = self.search(cr, SUPERUSER_ID, [('id', '=', uid), ('oauth_access_token', '=', password)])
            if not res:
                raise