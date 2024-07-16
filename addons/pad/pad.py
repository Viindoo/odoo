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
from openerp.osv import fields, osv
import random
import re
import string
import urllib2
import logging
from openerp.tools.translate import _
from openerp.tools import html2plaintext
from py_etherpad import EtherpadLiteClient
_logger = logging.getLogger(__name__)

class pad_common(osv.osv_memory):
    _name = 'pad.common'

    def pad_generate_url(self, cr, uid, context = None):
        company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id
        pad = {'server': company.pad_server,
         'key': company.pad_key}
        if not pad['server']:
            return pad
        if not pad['server'].startswith('http'):
            pad['server'] = 'http://' + pad['server']
        pad['server'] = pad['server'].rstrip('/')
        s = string.ascii_uppercase + string.digits
        salt = ''.join([ s[random.randint(0, len(s) - 1)] for i in range(10) ])
        path = '%s-%s-%s' % (cr.dbname.replace('_', '-'), self._name, salt)
        url = '%s/p/%s' % (pad['server'], path)
        if 'field_name' in context and 'model' in context and 'object_id' in context:
            myPad = EtherpadLiteClient(pad['key'], pad['server'] + '/api')
            myPad.createPad(path)
            model = self.pool.get(context['model'])
            field = model._all_columns[context['field_name']]
            real_field = field.column.pad_content_field
            for record in model.browse(cr, uid, [context['object_id']]):
                if record[real_field]:
                    myPad.setText(path, html2plaintext(record[real_field]))

        return {'server': pad['server'],
         'path': path,
         'url': url}

    def pad_get_content(self, cr, uid, url, context = None):
        content = ''
        if url:
            try:
                page = urllib2.urlopen('%s/export/html' % url).read()
                mo = re.search('<body>(.*)</body>', page)
                if mo:
                    content = mo.group(1)
            except:
                _logger.warning("No url found '%s'.", url)

        return content

    def write(self, cr, uid, ids, vals, context = None):
        self._set_pad_value(cr, uid, vals, context)
        return super(pad_common, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context = None):
        self._set_pad_value(cr, uid, vals, context)
        return super(pad_common, self).create(cr, uid, vals, context=context)

    def _set_pad_value(self, cr, uid, vals, context = None):
        for k, v in vals.items():
            field = self._all_columns[k].column
            if hasattr(field, 'pad_content_field'):
                vals[field.pad_content_field] = self.pad_get_content(cr, uid, v, context=context)

    def copy(self, cr, uid, id, default = None, context = None):
        if not default:
            default = {}
        for k, v in self._all_columns.iteritems():
            field = v.column
            if hasattr(field, 'pad_content_field'):
                pad = self.pad_generate_url(cr, uid, context)
                default[k] = pad.get('url')

        return super(pad_common, self).copy(cr, uid, id, default, context)