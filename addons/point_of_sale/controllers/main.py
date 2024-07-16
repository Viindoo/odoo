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
import logging
import simplejson
import os
import openerp
from openerp.addons.web.controllers.main import manifest_list, module_boot, html_template

class PointOfSaleController(openerp.addons.web.http.Controller):
    _cp_path = '/pos'

    @openerp.addons.web.http.httprequest
    def app(self, req, s_action = None, **kw):
        js = '\n        '.join(('<script type="text/javascript" src="%s"></script>' % i for i in manifest_list(req, None, 'js')))
        css = '\n        '.join(('<link rel="stylesheet" href="%s">' % i for i in manifest_list(req, None, 'css')))
        cookie = req.httprequest.cookies.get('instance0|session_id')
        session_id = cookie.replace('%22', '')
        template = html_template.replace('<html', '<html manifest="/pos/manifest?session_id=%s"' % session_id)
        r = template % {'js': js,
         'css': css,
         'modules': simplejson.dumps(module_boot(req)),
         'init': 'var wc = new s.web.WebClient();wc.appendTo($(document.body));'}
        return r

    @openerp.addons.web.http.httprequest
    def manifest(self, req, **kwargs):
        """ This generates a HTML5 cache manifest files that preloads the categories and products thumbnails 
        and other ressources necessary for the point of sale to work offline """
        ml = ['CACHE MANIFEST']

        def load_css_img(srcdir, dstdir):
            for f in os.listdir(srcdir):
                path = os.path.join(srcdir, f)
                dstpath = os.path.join(dstdir, f)
                if os.path.isdir(path):
                    load_css_img(path, dstpath)
                elif f.endswith(('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG', '.gif', '.GIF')):
                    ml.append(dstpath)

        imgdir = openerp.modules.get_module_resource('point_of_sale', 'static/src/img')
        load_css_img(imgdir, '/point_of_sale/static/src/img')
        products = req.session.model('product.product')
        for p in products.search_read([('pos_categ_id', '!=', False)], ['name']):
            product_id = p['id']
            url = '/web/binary/image?session_id=%s&model=product.product&field=image&id=%s' % (req.session_id, product_id)
            ml.append(url)

        categories = req.session.model('pos.category')
        for c in categories.search_read([], ['name']):
            category_id = c['id']
            url = '/web/binary/image?session_id=%s&model=pos.category&field=image&id=%s' % (req.session_id, category_id)
            ml.append(url)

        ml += ['NETWORK:', '*']
        m = '\n'.join(ml)
        return m

    @openerp.addons.web.http.jsonrequest
    def dispatch(self, request, iface, **kwargs):
        method = 'iface_%s' % iface
        return getattr(self, method)(request, **kwargs)

    @openerp.addons.web.http.jsonrequest
    def scan_item_success(self, request, ean):
        """
        A product has been scanned with success
        """
        print 'scan_item_success: ' + str(ean)

    @openerp.addons.web.http.jsonrequest
    def scan_item_error_unrecognized(self, request, ean):
        """
        A product has been scanned without success
        """
        print 'scan_item_error_unrecognized: ' + str(ean)

    @openerp.addons.web.http.jsonrequest
    def help_needed(self, request):
        """
        The user wants an help (ex: light is on)
        """
        print 'help_needed'

    @openerp.addons.web.http.jsonrequest
    def help_canceled(self, request):
        """
        The user stops the help request
        """
        print 'help_canceled'

    @openerp.addons.web.http.jsonrequest
    def weighting_start(self, request):
        print 'weighting_start'

    @openerp.addons.web.http.jsonrequest
    def weighting_read_kg(self, request):
        print 'weighting_read_kg'
        return 0.0

    @openerp.addons.web.http.jsonrequest
    def weighting_end(self, request):
        print 'weighting_end'

    @openerp.addons.web.http.jsonrequest
    def payment_request(self, request, price):
        """
        The PoS will activate the method payment 
        """
        print 'payment_request: price:' + str(price)
        return 'ok'

    @openerp.addons.web.http.jsonrequest
    def payment_status(self, request):
        print 'payment_status'
        return {'status': 'waiting'}

    @openerp.addons.web.http.jsonrequest
    def payment_cancel(self, request):
        print 'payment_cancel'

    @openerp.addons.web.http.jsonrequest
    def transaction_start(self, request):
        print 'transaction_start'

    @openerp.addons.web.http.jsonrequest
    def transaction_end(self, request):
        print 'transaction_end'

    @openerp.addons.web.http.jsonrequest
    def cashier_mode_activated(self, request):
        print 'cashier_mode_activated'

    @openerp.addons.web.http.jsonrequest
    def cashier_mode_deactivated(self, request):
        print 'cashier_mode_deactivated'

    @openerp.addons.web.http.jsonrequest
    def open_cashbox(self, request):
        print 'open_cashbox'

    @openerp.addons.web.http.jsonrequest
    def print_receipt(self, request, receipt):
        print 'print_receipt' + str(receipt)

    @openerp.addons.web.http.jsonrequest
    def print_pdf_invoice(self, request, pdfinvoice):
        print 'print_pdf_invoice' + str(pdfinvoice)