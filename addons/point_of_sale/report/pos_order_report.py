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
from openerp import tools
from openerp.osv import fields, osv

class pos_order_report(osv.osv):
    _name = 'report.pos.order'
    _description = 'Point of Sale Orders Statistics'
    _auto = False
    _columns = {'date': fields.date('Date Order', readonly=True),
     'year': fields.char('Year', size=4, readonly=True),
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
     'day': fields.char('Day', size=128, readonly=True),
     'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
     'product_id': fields.many2one('product.product', 'Product', readonly=True),
     'state': fields.selection([('draft', 'New'),
               ('paid', 'Closed'),
               ('done', 'Synchronized'),
               ('invoiced', 'Invoiced'),
               ('cancel', 'Cancelled')], 'Status'),
     'user_id': fields.many2one('res.users', 'Salesperson', readonly=True),
     'price_total': fields.float('Total Price', readonly=True),
     'total_discount': fields.float('Total Discount', readonly=True),
     'average_price': fields.float('Average Price', readonly=True, group_operator='avg'),
     'shop_id': fields.many2one('sale.shop', 'Shop', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'nbr': fields.integer('# of Lines', readonly=True),
     'product_qty': fields.integer('# of Qty', readonly=True),
     'journal_id': fields.many2one('account.journal', 'Journal'),
     'delay_validation': fields.integer('Delay Validation')}
    _order = 'date desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_pos_order')
        cr.execute("\n            create or replace view report_pos_order as (\n                select\n                    min(l.id) as id,\n                    count(*) as nbr,\n                    to_date(to_char(s.date_order, 'dd-MM-YYYY'),'dd-MM-YYYY') as date,\n                    sum(l.qty * u.factor) as product_qty,\n                    sum(l.qty * l.price_unit) as price_total,\n                    sum((l.qty * l.price_unit) * (l.discount / 100)) as total_discount,\n                    (sum(l.qty*l.price_unit)/sum(l.qty * u.factor))::decimal(16,2) as average_price,\n                    sum(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') as int)) as delay_validation,\n                    to_char(s.date_order, 'YYYY') as year,\n                    to_char(s.date_order, 'MM') as month,\n                    to_char(s.date_order, 'YYYY-MM-DD') as day,\n                    s.partner_id as partner_id,\n                    s.state as state,\n                    s.user_id as user_id,\n                    s.shop_id as shop_id,\n                    s.company_id as company_id,\n                    s.sale_journal as journal_id,\n                    l.product_id as product_id\n                from pos_order_line as l\n                    left join pos_order s on (s.id=l.order_id)\n                    left join product_template pt on (pt.id=l.product_id)\n                    left join product_uom u on (u.id=pt.uom_id)\n                group by\n                    to_char(s.date_order, 'dd-MM-YYYY'),to_char(s.date_order, 'YYYY'),to_char(s.date_order, 'MM'),\n                    to_char(s.date_order, 'YYYY-MM-DD'), s.partner_id,s.state,\n                    s.user_id,s.shop_id,s.company_id,s.sale_journal,l.product_id,s.create_date\n                having\n                    sum(l.qty * u.factor) != 0)")


pos_order_report()