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
import time
from openerp import netsvc
from openerp import tools

class report_transaction_pos(osv.osv):
    _name = 'report.transaction.pos'
    _description = 'transaction for the pos'
    _auto = False
    _columns = {'date_create': fields.char('Date', size=16, readonly=True),
     'journal_id': fields.many2one('account.journal', 'Sales Journal', readonly=True),
     'jl_id': fields.many2one('account.journal', 'Cash Journals', readonly=True),
     'user_id': fields.many2one('res.users', 'User', readonly=True),
     'no_trans': fields.float('Number of Transaction', readonly=True),
     'amount': fields.float('Amount', readonly=True),
     'invoice_id': fields.float('Nbr Invoice', readonly=True),
     'invoice_am': fields.float('Invoice Amount', readonly=True),
     'product_nb': fields.float('Product Nb.', readonly=True),
     'disc': fields.float('Disc.', readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_transaction_pos')
        cr.execute("\n            create or replace view report_transaction_pos as (\n               select\n                    min(absl.id) as id,\n                    count(absl.id) as no_trans,\n                    sum(absl.amount) as amount,\n                    sum((100.0-line.discount) * line.price_unit * line.qty / 100.0) as disc,\n                    to_char(date_trunc('day',absl.create_date),'YYYY-MM-DD')::text as date_create,\n                    po.user_id as user_id,\n                    po.sale_journal as journal_id,\n                    abs.journal_id as jl_id,\n                    count(po.invoice_id) as invoice_id,\n                    count(p.id) as product_nb\n                from\n                    account_bank_statement_line as absl,\n                    account_bank_statement as abs,\n                    product_product as p,\n                    pos_order_line as line,\n                    pos_order as po\n                where\n                    absl.pos_statement_id = po.id and\n                    line.order_id=po.id and\n                    line.product_id=p.id and\n                    absl.statement_id=abs.id\n\n                group by\n                    po.user_id,po.sale_journal, abs.journal_id,\n                    to_char(date_trunc('day',absl.create_date),'YYYY-MM-DD')::text\n                )\n        ")


report_transaction_pos()

class report_sales_by_user_pos(osv.osv):
    _name = 'report.sales.by.user.pos'
    _description = 'Sales by user'
    _auto = False
    _columns = {'date_order': fields.date('Order Date', required=True, select=True),
     'amount': fields.float('Total', readonly=True, select=True),
     'qty': fields.float('Quantity', readonly=True, select=True),
     'user_id': fields.many2one('res.users', 'User', readonly=True, select=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_sales_by_user_pos')
        cr.execute("\n            create or replace view report_sales_by_user_pos as (\n                select\n                    min(po.id) as id,\n                    to_char(date_trunc('day',po.date_order),'YYYY-MM-DD')::text as date_order,\n                    po.user_id as user_id,\n                    sum(pol.qty)as qty,\n                    sum((pol.price_unit * pol.qty * (1 - (pol.discount) / 100.0))) as amount\n                from\n                    pos_order as po,pos_order_line as pol,product_product as pp,product_template as pt\n                where\n                    pt.id=pp.product_tmpl_id and pp.id=pol.product_id and po.id = pol.order_id\n               group by\n                    to_char(date_trunc('day',po.date_order),'YYYY-MM-DD')::text,\n                    po.user_id\n\n                )\n        ")


report_sales_by_user_pos()

class report_sales_by_user_pos_month(osv.osv):
    _name = 'report.sales.by.user.pos.month'
    _description = 'Sales by user monthly'
    _auto = False
    _columns = {'date_order': fields.date('Order Date', required=True, select=True),
     'amount': fields.float('Total', readonly=True, select=True),
     'qty': fields.float('Quantity', readonly=True, select=True),
     'user_id': fields.many2one('res.users', 'User', readonly=True, select=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_sales_by_user_pos_month')
        cr.execute("\n            create or replace view report_sales_by_user_pos_month as (\n                select\n                    min(po.id) as id,\n                    to_char(date_trunc('month',po.date_order),'YYYY-MM-DD')::text as date_order,\n                    po.user_id as user_id,\n                    sum(pol.qty)as qty,\n                    sum((pol.price_unit * pol.qty * (1 - (pol.discount) / 100.0))) as amount\n                from\n                    pos_order as po,pos_order_line as pol,product_product as pp,product_template as pt\n                where\n                    pt.id=pp.product_tmpl_id and pp.id=pol.product_id and po.id = pol.order_id\n               group by\n                    to_char(date_trunc('month',po.date_order),'YYYY-MM-DD')::text,\n                    po.user_id\n\n                )\n        ")


report_sales_by_user_pos_month()

class report_sales_by_margin_pos(osv.osv):
    _name = 'report.sales.by.margin.pos'
    _description = 'Sales by margin'
    _auto = False
    _columns = {'product_name': fields.char('Product Name', size=64, readonly=True),
     'date_order': fields.date('Order Date', required=True, select=True),
     'user_id': fields.many2one('res.users', 'User', readonly=True, select=True),
     'qty': fields.float('Qty', readonly=True, select=True),
     'net_margin_per_qty': fields.float('Net margin per Qty', readonly=True, select=True),
     'total': fields.float('Margin', readonly=True, select=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_sales_by_margin_pos')
        cr.execute("\n            create or replace view report_sales_by_margin_pos as (\n                select\n                    min(pol.id) as id,\n                    po.user_id as user_id,\n                    pt.name as product_name,\n                    to_char(date_trunc('day',po.date_order),'YYYY-MM-DD')::text as date_order,\n                    sum(pol.qty) as qty,\n                    pt.list_price-pt.standard_price as net_margin_per_qty,\n                    (pt.list_price-pt.standard_price) *sum(pol.qty) as total\n                from\n                    product_template as pt,\n                    product_product as pp,\n                    pos_order_line as pol,\n                    pos_order as po\n                where\n                    pol.product_id = pp.product_tmpl_id and\n                    pp.product_tmpl_id = pt.id and\n                    po.id = pol.order_id\n\n                group by\n                    pt.name,\n                    pt.list_price,\n                    pt.standard_price,\n                    po.user_id,\n                    to_char(date_trunc('day',po.date_order),'YYYY-MM-DD')::text\n\n                )\n        ")


report_sales_by_margin_pos()

class report_sales_by_margin_pos_month(osv.osv):
    _name = 'report.sales.by.margin.pos.month'
    _description = 'Sales by margin monthly'
    _auto = False
    _columns = {'product_name': fields.char('Product Name', size=64, readonly=True),
     'date_order': fields.date('Order Date', required=True, select=True),
     'user_id': fields.many2one('res.users', 'User', readonly=True, select=True),
     'qty': fields.float('Qty', readonly=True, select=True),
     'net_margin_per_qty': fields.float('Net margin per Qty', readonly=True, select=True),
     'total': fields.float('Margin', readonly=True, select=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_sales_by_margin_pos_month')
        cr.execute("\n            create or replace view report_sales_by_margin_pos_month as (\n                select\n                    min(pol.id) as id,\n                    po.user_id as user_id,\n                    pt.name as product_name,\n                    to_char(date_trunc('month',po.date_order),'YYYY-MM-DD')::text as date_order,\n                    sum(pol.qty) as qty,\n                    pt.list_price-pt.standard_price as net_margin_per_qty,\n                    (pt.list_price-pt.standard_price) *sum(pol.qty) as total\n                from\n                    product_template as pt,\n                    product_product as pp,\n                    pos_order_line as pol,\n                    pos_order as po\n                where\n                    pol.product_id = pp.product_tmpl_id and\n                    pp.product_tmpl_id = pt.id and\n                    po.id = pol.order_id\n\n                group by\n                    pt.name,\n                    pt.list_price,\n                    pt.standard_price,\n                    po.user_id,\n                    to_char(date_trunc('month',po.date_order),'YYYY-MM-DD')::text\n\n                )\n        ")


report_sales_by_margin_pos_month()