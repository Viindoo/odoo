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
import simplejson
import urllib
import openerp.addons.web.http as openerpweb
import openerp.addons.web.controllers.main as webmain

class EDI(openerpweb.Controller):
    _cp_path = '/edi'

    @openerpweb.httprequest
    def import_url(self, req, url):
        modules = webmain.module_boot(req) + ['edi']
        modules_str = ','.join(modules)
        modules_json = simplejson.dumps(modules)
        js = '\n        '.join(('<script type="text/javascript" src="%s"></script>' % i for i in webmain.manifest_list(req, modules_str, 'js')))
        css = '\n        '.join(('<link rel="stylesheet" href="%s">' % i for i in webmain.manifest_list(req, modules_str, 'css')))
        safe_url = urllib.quote_plus(url, ':/?&;=')
        return webmain.html_template % {'js': js,
         'css': css,
         'modules': modules_json,
         'init': 's.edi.edi_import("%s");' % safe_url}

    @openerpweb.jsonrequest
    def import_edi_url(self, req, url):
        result = req.session.proxy('edi').import_edi_url(req.session._db, req.session._uid, req.session._password, url)
        if len(result) == 1:
            return {'action': webmain.clean_action(req, result[0][2])}
        return True