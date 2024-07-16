# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
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

class purchase_report(osv.osv):
    _name = 'purchase.report'
    _description = 'Purchases Orders'
    _auto = False
    _columns = {'date': fields.date('Order Date', readonly=True, help='Date on which this document has been created'),
     'name': fields.char('Year', size=64, required=False, readonly=True),
     'day': fields.char('Day', size=128, readonly=True),
     'state': fields.selection([('draft', 'Request for Quotation'),
               ('confirmed', 'Waiting Supplier Ack'),
               ('approved', 'Approved'),
               ('except_picking', 'Shipping Exception'),
               ('except_invoice', 'Invoice Exception'),
               ('done', 'Done'),
               ('cancel', 'Cancelled')], 'Order Status', readonly=True),
     'product_id': fields.many2one('product.product', 'Product', readonly=True),
     'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse', readonly=True),
     'location_id': fields.many2one('stock.location', 'Destination', readonly=True),
     'partner_id': fields.many2one('res.partner', 'Supplier', readonly=True),
     'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', readonly=True),
     'date_approve': fields.date('Date Approved', readonly=True),
     'expected_date': fields.date('Expected Date', readonly=True),
     'validator': fields.many2one('res.users', 'Validated By', readonly=True),
     'product_uom': fields.many2one('product.uom', 'Reference Unit of Measure', required=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
     'delay': fields.float('Days to Validate', digits=(16, 2), readonly=True),
     'delay_pass': fields.float('Days to Deliver', digits=(16, 2), readonly=True),
     'quantity': fields.float('Quantity', readonly=True),
     'price_total': fields.float('Total Price', readonly=True),
     'price_average': fields.float('Average Price', readonly=True, group_operator='avg'),
     'negociation': fields.float('Purchase-Standard Price', readonly=True, group_operator='avg'),
     'price_standard': fields.float('Products Value', readonly=True, group_operator='sum'),
     'nbr': fields.integer('# of Lines', readonly=True),
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
               ('12', 'December')], 'Month', readonly=True),
     'category_id': fields.many2one('product.category', 'Category', readonly=True)}
    _order = 'name desc,price_total desc'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'purchase_report')
        cr.execute("\n            create or replace view purchase_report as (\n                select\n                    min(l.id) as id,\n                    s.date_order as date,\n                    to_char(s.date_order, 'YYYY') as name,\n                    to_char(s.date_order, 'MM') as month,\n                    to_char(s.date_order, 'YYYY-MM-DD') as day,\n                    s.state,\n                    s.date_approve,\n                    s.minimum_planned_date as expected_date,\n                    s.dest_address_id,\n                    s.pricelist_id,\n                    s.validator,\n                    s.warehouse_id as warehouse_id,\n                    s.partner_id as partner_id,\n                    s.create_uid as user_id,\n                    s.company_id as company_id,\n                    l.product_id,\n                    t.categ_id as category_id,\n                    t.uom_id as product_uom,\n                    s.location_id as location_id,\n                    sum(l.product_qty/u.factor*u2.factor) as quantity,\n                    extract(epoch from age(s.date_approve,s.date_order))/(24*60*60)::decimal(16,2) as delay,\n                    extract(epoch from age(l.date_planned,s.date_order))/(24*60*60)::decimal(16,2) as delay_pass,\n                    count(*) as nbr,\n                    (l.price_unit*l.product_qty)::decimal(16,2) as price_total,\n                    avg(100.0 * (l.price_unit*l.product_qty) / NULLIF(t.standard_price*l.product_qty/u.factor*u2.factor, 0.0))::decimal(16,2) as negociation,\n\n                    sum(t.standard_price*l.product_qty/u.factor*u2.factor)::decimal(16,2) as price_standard,\n                    (sum(l.product_qty*l.price_unit)/NULLIF(sum(l.product_qty/u.factor*u2.factor),0.0))::decimal(16,2) as price_average\n                from purchase_order s\n                    left join purchase_order_line l on (s.id=l.order_id)\n                        left join product_product p on (l.product_id=p.id)\n                            left join product_template t on (p.product_tmpl_id=t.id)\n                    left join product_uom u on (u.id=l.product_uom)\n                    left join product_uom u2 on (u2.id=t.uom_id)\n                where l.product_id is not null\n                group by\n                    s.company_id,\n                    s.create_uid,\n                    s.partner_id,\n                    l.product_qty,\n                    u.factor,\n                    s.location_id,\n                    l.price_unit,\n                    s.date_approve,\n                    l.date_planned,\n                    l.product_uom,\n                    s.minimum_planned_date,\n                    s.pricelist_id,\n                    s.validator,\n                    s.dest_address_id,\n                    l.product_id,\n                    t.categ_id,\n                    s.date_order,\n                    to_char(s.date_order, 'YYYY'),\n                    to_char(s.date_order, 'MM'),\n                    to_char(s.date_order, 'YYYY-MM-DD'),\n                    s.state,\n                    s.warehouse_id,\n                    u.uom_type,\n                    u.category_id,\n                    t.uom_id,\n                    u.id,\n                    u2.factor\n            )\n        ")


purchase_report()