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
from openerp.osv import fields, osv
from openerp import tools
from openerp.addons.decimal_precision import decimal_precision as dp

class report_analytic_account_close(osv.osv):
    _name = 'report.analytic.account.close'
    _description = 'Analytic account to close'
    _auto = False
    _columns = {'name': fields.many2one('account.analytic.account', 'Analytic account', readonly=True),
     'state': fields.char('Status', size=32, readonly=True),
     'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
     'quantity': fields.float('Quantity', readonly=True),
     'quantity_max': fields.float('Max. Quantity', readonly=True),
     'balance': fields.float('Balance', readonly=True),
     'date_deadline': fields.date('Deadline', readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_analytic_account_close')
        cr.execute('\n            create or replace view report_analytic_account_close as (\n                select\n                    a.id as id,\n                    a.id as name,\n                    a.state as state,\n                    sum(l.unit_amount) as quantity,\n                    sum(l.amount) as balance,\n                    a.partner_id as partner_id,\n                    a.quantity_max as quantity_max,\n                    a.date as date_deadline\n                from\n                    account_analytic_line l\n                right join\n                    account_analytic_account a on (l.account_id=a.id)\n                group by\n                    a.id,a.state, a.quantity_max,a.date,a.partner_id\n                having\n                    (a.quantity_max>0 and (sum(l.unit_amount)>=a.quantity_max)) or\n                    a.date <= current_date\n            )')


report_analytic_account_close()

class report_account_analytic_line_to_invoice(osv.osv):
    _name = 'report.account.analytic.line.to.invoice'
    _description = 'Analytic lines to invoice report'
    _auto = False
    _columns = {'name': fields.char('Year', size=64, required=False, readonly=True),
     'product_id': fields.many2one('product.product', 'Product', readonly=True),
     'account_id': fields.many2one('account.analytic.account', 'Analytic account', readonly=True),
     'product_uom_id': fields.many2one('product.uom', 'Unit of Measure', readonly=True),
     'unit_amount': fields.float('Units', readonly=True),
     'sale_price': fields.float('Sale price', readonly=True, digits_compute=dp.get_precision('Product Price')),
     'amount': fields.float('Amount', readonly=True, digits_compute=dp.get_precision('Account')),
     'month': fields.selection([('01', 'January'),
               ('02', 'February'),
               ('03', 'March'),
               ('04', 'April'),
               ('05', 'May'),
               ('06', 'June'),
               ('07', 'July'),
               ('08', 'August'),
               ('09', 'September'),
               ('10', 'October'),
               ('11', 'November'),
               ('12', 'December')], 'Month', readonly=True)}
    _order = 'name desc, product_id asc, account_id asc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_account_analytic_line_to_invoice')
        cr.execute("\n            CREATE OR REPLACE VIEW report_account_analytic_line_to_invoice AS (\n                SELECT\n                    DISTINCT(to_char(l.date,'MM')) as month,\n                    to_char(l.date, 'YYYY') as name,\n                    MIN(l.id) AS id,\n                    l.product_id,\n                    l.account_id,\n                    SUM(l.amount) AS amount,\n                    SUM(l.unit_amount*t.list_price) AS sale_price,\n                    SUM(l.unit_amount) AS unit_amount,\n                    l.product_uom_id\n                FROM\n                    account_analytic_line l\n                left join\n                    product_product p on (l.product_id=p.id)\n                left join\n                    product_template t on (p.product_tmpl_id=t.id)\n                WHERE\n                    (invoice_id IS NULL) and (to_invoice IS NOT NULL)\n                GROUP BY\n                    to_char(l.date, 'YYYY'), to_char(l.date,'MM'), product_id, product_uom_id, account_id\n            )\n        ")


report_account_analytic_line_to_invoice()