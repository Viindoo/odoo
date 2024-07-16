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
import openerp

class ImportController(openerp.addons.web.http.Controller):
    _cp_path = '/base_import'

    @openerp.addons.web.http.httprequest
    def set_file(self, req, file, import_id, jsonp = 'callback'):
        import_id = int(import_id)
        written = req.session.model('base_import.import').write(import_id, {'file': file.read(),
         'file_name': file.filename,
         'file_type': file.content_type}, req.context)
        return 'window.top.%s(%s)' % (jsonp, simplejson.dumps({'result': written}))