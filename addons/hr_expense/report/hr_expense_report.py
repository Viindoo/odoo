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
from openerp import tools
from openerp.osv import fields, osv
from openerp.addons.decimal_precision import decimal_precision as dp

class hr_expense_report(osv.osv):
    _name = 'hr.expense.report'
    _description = 'Expenses Statistics'
    _auto = False
    _rec_name = 'date'
    _columns = {'date': fields.date('Date ', readonly=True),
     'year': fields.char('Year', size=4, readonly=True),
     'day': fields.char('Day', size=128, readonly=True),
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
     'product_id': fields.many2one('product.product', 'Product', readonly=True),
     'journal_id': fields.many2one('account.journal', 'Force Journal', readonly=True),
     'product_qty': fields.float('Qty', readonly=True),
     'employee_id': fields.many2one('hr.employee', "Employee's Name", readonly=True),
     'date_confirm': fields.date('Confirmation Date', readonly=True),
     'date_valid': fields.date('Validation Date', readonly=True),
     'voucher_id': fields.many2one('account.voucher', 'Receipt', readonly=True),
     'department_id': fields.many2one('hr.department', 'Department', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'user_id': fields.many2one('res.users', 'Validation User', readonly=True),
     'currency_id': fields.many2one('res.currency', 'Currency', readonly=True),
     'price_total': fields.float('Total Price', readonly=True, digits_compute=dp.get_precision('Account')),
     'delay_valid': fields.float('Delay to Valid', readonly=True),
     'delay_confirm': fields.float('Delay to Confirm', readonly=True),
     'analytic_account': fields.many2one('account.analytic.account', 'Analytic account', readonly=True),
     'price_average': fields.float('Average Price', readonly=True, digits_compute=dp.get_precision('Account')),
     'nbr': fields.integer('# of Lines', readonly=True),
     'no_of_products': fields.integer('# of Products', readonly=True),
     'no_of_account': fields.integer('# of Accounts', readonly=True),
     'state': fields.selection([('draft', 'Draft'),
               ('confirm', 'Waiting confirmation'),
               ('accepted', 'Accepted'),
               ('done', 'Done'),
               ('cancelled', 'Cancelled')], 'Status', readonly=True)}
    _order = 'date desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_expense_report')
        cr.execute("\n            create or replace view hr_expense_report as (\n                 select\n                     min(l.id) as id,\n                     date_trunc('day',s.date) as date,\n                     s.employee_id,\n                     s.journal_id,\n                     s.currency_id,\n                     to_date(to_char(s.date_confirm, 'dd-MM-YYYY'),'dd-MM-YYYY') as date_confirm,\n                     to_date(to_char(s.date_valid, 'dd-MM-YYYY'),'dd-MM-YYYY') as date_valid,\n                     s.voucher_id,\n                     s.user_valid as user_id,\n                     s.department_id,\n                     to_char(date_trunc('day',s.create_date), 'YYYY') as year,\n                     to_char(date_trunc('day',s.create_date), 'MM') as month,\n                     to_char(date_trunc('day',s.create_date), 'YYYY-MM-DD') as day,\n                     avg(extract('epoch' from age(s.date_valid,s.date)))/(3600*24) as  delay_valid,\n                     avg(extract('epoch' from age(s.date_valid,s.date_confirm)))/(3600*24) as  delay_confirm,\n                     l.product_id as product_id,\n                     l.analytic_account as analytic_account,\n                     sum(l.unit_quantity * u.factor) as product_qty,\n                     s.company_id as company_id,\n                     sum(l.unit_quantity*l.unit_amount) as price_total,\n                     (sum(l.unit_quantity*l.unit_amount)/sum(case when l.unit_quantity=0 or u.factor=0 then 1 else l.unit_quantity * u.factor end))::decimal(16,2) as price_average,\n                     count(*) as nbr,\n                     (select unit_quantity from hr_expense_line where id=l.id and product_id is not null) as no_of_products,\n                     (select analytic_account from hr_expense_line where id=l.id and analytic_account is not null) as no_of_account,\n                     s.state\n                 from hr_expense_line l\n                 left join hr_expense_expense s on (s.id=l.expense_id)\n                 left join product_uom u on (u.id=l.uom_id)\n                 group by\n                     date_trunc('day',s.date),\n                     to_char(date_trunc('day',s.create_date), 'YYYY'),\n                     to_char(date_trunc('day',s.create_date), 'MM'),\n                     to_char(date_trunc('day',s.create_date), 'YYYY-MM-DD'),\n                     to_date(to_char(s.date_confirm, 'dd-MM-YYYY'),'dd-MM-YYYY'),\n                     to_date(to_char(s.date_valid, 'dd-MM-YYYY'),'dd-MM-YYYY'),\n                     l.product_id,\n                     l.analytic_account,\n                     s.voucher_id,\n                     s.currency_id,\n                     s.user_valid,\n                     s.department_id,\n                     l.uom_id,\n                     l.id,\n                     s.state,\n                     s.journal_id,\n                     s.company_id,\n                     s.employee_id\n            )\n        ")


hr_expense_report()