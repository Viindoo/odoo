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
import functools
import logging
import simplejson
import werkzeug.utils
from werkzeug.exceptions import BadRequest
import openerp
from openerp import SUPERUSER_ID
import openerp.addons.web.http as oeweb
from openerp.addons.web.controllers.main import db_monodb, set_cookie_and_redirect, login_and_redirect
from openerp.modules.registry import RegistryManager
_logger = logging.getLogger(__name__)

def fragment_to_query_string(func):

    @functools.wraps(func)
    def wrapper(self, req, **kw):
        if not kw:
            return "<html><head><script>\n                var l = window.location;\n                var q = l.hash.substring(1);\n                var r = '/' + l.search;\n                if(q.length !== 0) {\n                    var s = l.search ? (l.search === '?' ? '' : '&') : '?';\n                    r = l.pathname + l.search + s + q;\n                }\n                window.location = r;\n            </script></head><body></body></html>"
        return func(self, req, **kw)

    return wrapper


class OAuthController(oeweb.Controller):
    _cp_path = '/auth_oauth'

    @oeweb.jsonrequest
    def list_providers(self, req, dbname):
        try:
            registry = RegistryManager.get(dbname)
            with registry.cursor() as cr:
                providers = registry.get('auth.oauth.provider')
                l = providers.read(cr, SUPERUSER_ID, providers.search(cr, SUPERUSER_ID, [('enabled', '=', True)]))
        except Exception:
            l = []

        return l

    @oeweb.httprequest
    @fragment_to_query_string
    def signin(self, req, **kw):
        state = simplejson.loads(kw['state'])
        dbname = state['d']
        provider = state['p']
        context = state.get('c', {})
        registry = RegistryManager.get(dbname)
        with registry.cursor() as cr:
            try:
                u = registry.get('res.users')
                credentials = u.auth_oauth(cr, SUPERUSER_ID, provider, kw, context=context)
                cr.commit()
                action = state.get('a')
                menu = state.get('m')
                url = '/'
                if action:
                    url = '/#action=%s' % action
                elif menu:
                    url = '/#menu_id=%s' % menu
                return login_and_redirect(req, redirect_url=url, *credentials)
            except AttributeError:
                _logger.error('auth_signup not installed on database %s: oauth sign up cancelled.' % (dbname,))
                url = '/#action=login&oauth_error=1'
            except openerp.exceptions.AccessDenied:
                _logger.info('OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies')
                url = '/#action=login&oauth_error=3'
                redirect = werkzeug.utils.redirect(url, 303)
                redirect.autocorrect_location_header = False
                return redirect
            except Exception as e:
                _logger.exception('OAuth2: %s' % str(e))
                url = '/#action=login&oauth_error=2'

        return set_cookie_and_redirect(req, url)

    @oeweb.httprequest
    def oea(self, req, **kw):
        """login user via OpenERP Account provider"""
        dbname = kw.pop('db', None)
        if not dbname:
            dbname = db_monodb(req)
        if not dbname:
            return BadRequest()
        else:
            registry = RegistryManager.get(dbname)
            with registry.cursor() as cr:
                IMD = registry['ir.model.data']
                try:
                    model, provider_id = IMD.get_object_reference(cr, SUPERUSER_ID, 'auth_oauth', 'provider_openerp')
                except ValueError:
                    return set_cookie_and_redirect(req, '/?db=%s' % dbname)

                raise model == 'auth.oauth.provider' or AssertionError
            state = {'d': dbname,
             'p': provider_id,
             'c': {'no_user_creation': True}}
            kw['state'] = simplejson.dumps(state)
            return self.signin(req, **kw)