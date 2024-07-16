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
import openerp.addons.decimal_precision as dp

class account_entries_report(osv.osv):
    _name = 'account.entries.report'
    _description = 'Journal Items Analysis'
    _auto = False
    _rec_name = 'date'
    _columns = {'date': fields.date('Effective Date', readonly=True),
     'date_created': fields.date('Date Created', readonly=True),
     'date_maturity': fields.date('Date Maturity', readonly=True),
     'ref': fields.char('Reference', size=64, readonly=True),
     'nbr': fields.integer('# of Items', readonly=True),
     'debit': fields.float('Debit', readonly=True),
     'credit': fields.float('Credit', readonly=True),
     'balance': fields.float('Balance', readonly=True),
     'day': fields.char('Day', size=128, readonly=True),
     'year': fields.char('Year', size=4, readonly=True),
     'date': fields.date('Date', size=128, readonly=True),
     'currency_id': fields.many2one('res.currency', 'Currency', readonly=True),
     'amount_currency': fields.float('Amount Currency', digits_compute=dp.get_precision('Account'), readonly=True),
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
     'period_id': fields.many2one('account.period', 'Period', readonly=True),
     'account_id': fields.many2one('account.account', 'Account', readonly=True),
     'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
     'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', readonly=True),
     'product_id': fields.many2one('product.product', 'Product', readonly=True),
     'product_uom_id': fields.many2one('product.uom', 'Product Unit of Measure', readonly=True),
     'move_state': fields.selection([('draft', 'Unposted'), ('posted', 'Posted')], 'Status', readonly=True),
     'move_line_state': fields.selection([('draft', 'Unbalanced'), ('valid', 'Valid')], 'State of Move Line', readonly=True),
     'reconcile_id': fields.many2one('account.move.reconcile', readonly=True),
     'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
     'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
     'quantity': fields.float('Products Quantity', digits=(16, 2), readonly=True),
     'user_type': fields.many2one('account.account.type', 'Account Type', readonly=True),
     'type': fields.selection([('receivable', 'Receivable'),
              ('payable', 'Payable'),
              ('cash', 'Cash'),
              ('view', 'View'),
              ('consolidation', 'Consolidation'),
              ('other', 'Regular'),
              ('closed', 'Closed')], 'Internal Type', readonly=True, help='This type is used to differentiate types with special effects in OpenERP: view can not have entries, consolidation are accounts that can have children accounts for multi-company consolidations, payable/receivable are for partners accounts (for debit/credit computations), closed for depreciated accounts.'),
     'company_id': fields.many2one('res.company', 'Company', readonly=True)}
    _order = 'date desc'

    def search(self, cr, uid, args, offset = 0, limit = None, order = None, context = None, count = False):
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        for arg in args:
            if arg[0] == 'period_id' and arg[2] == 'current_period':
                ctx = dict(context or {}, account_period_prefer_normal=True)
                current_period = period_obj.find(cr, uid, context=ctx)[0]
                args.append(['period_id', 'in', [current_period]])
                break
            elif arg[0] == 'period_id' and arg[2] == 'current_year':
                current_year = fiscalyear_obj.find(cr, uid)
                ids = fiscalyear_obj.read(cr, uid, [current_year], ['period_ids'])[0]['period_ids']
                args.append(['period_id', 'in', ids])

        for a in [['period_id', 'in', 'current_year'], ['period_id', 'in', 'current_period']]:
            if a in args:
                args.remove(a)

        return super(account_entries_report, self).search(cr, uid, args=args, offset=offset, limit=limit, order=order, context=context, count=count)

    def read_group(self, cr, uid, domain, fields, groupby, offset = 0, limit = None, context = None, orderby = False):
        if context is None:
            context = {}
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        if context.get('period', False) == 'current_period':
            ctx = dict(context, account_period_prefer_normal=True)
            current_period = period_obj.find(cr, uid, context=ctx)[0]
            domain.append(['period_id', 'in', [current_period]])
        elif context.get('year', False) == 'current_year':
            current_year = fiscalyear_obj.find(cr, uid)
            ids = fiscalyear_obj.read(cr, uid, [current_year], ['period_ids'])[0]['period_ids']
            domain.append(['period_id', 'in', ids])
        else:
            domain = domain
        return super(account_entries_report, self).read_group(cr, uid, domain, fields, groupby, offset, limit, context, orderby)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_entries_report')
        cr.execute("\n            create or replace view account_entries_report as (\n            select\n                l.id as id,\n                am.date as date,\n                l.date_maturity as date_maturity,\n                l.date_created as date_created,\n                am.ref as ref,\n                am.state as move_state,\n                l.state as move_line_state,\n                l.reconcile_id as reconcile_id,\n                to_char(am.date, 'YYYY') as year,\n                to_char(am.date, 'MM') as month,\n                to_char(am.date, 'YYYY-MM-DD') as day,\n                l.partner_id as partner_id,\n                l.product_id as product_id,\n                l.product_uom_id as product_uom_id,\n                am.company_id as company_id,\n                am.journal_id as journal_id,\n                p.fiscalyear_id as fiscalyear_id,\n                am.period_id as period_id,\n                l.account_id as account_id,\n                l.analytic_account_id as analytic_account_id,\n                a.type as type,\n                a.user_type as user_type,\n                1 as nbr,\n                l.quantity as quantity,\n                l.currency_id as currency_id,\n                l.amount_currency as amount_currency,\n                l.debit as debit,\n                l.credit as credit,\n                l.debit-l.credit as balance\n            from\n                account_move_line l\n                left join account_account a on (l.account_id = a.id)\n                left join account_move am on (am.id=l.move_id)\n                left join account_period p on (am.period_id=p.id)\n                where l.state != 'draft'\n            )\n        ")


account_entries_report()