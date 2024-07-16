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

class asset_asset_report(osv.osv):
    _name = 'asset.asset.report'
    _description = 'Assets Analysis'
    _auto = False
    _columns = {'name': fields.char('Year', size=16, required=False, readonly=True),
     'purchase_date': fields.date('Purchase Date', readonly=True),
     'depreciation_date': fields.date('Depreciation Date', readonly=True),
     'asset_id': fields.many2one('account.asset.asset', string='Asset', readonly=True),
     'asset_category_id': fields.many2one('account.asset.category', string='Asset category'),
     'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
     'state': fields.selection([('draft', 'Draft'), ('open', 'Running'), ('close', 'Close')], 'Status', readonly=True),
     'depreciation_value': fields.float('Amount of Depreciation Lines', readonly=True),
     'move_check': fields.boolean('Posted', readonly=True),
     'nbr': fields.integer('# of Depreciation Lines', readonly=True),
     'gross_value': fields.float('Gross Amount', readonly=True),
     'posted_value': fields.float('Posted Amount', readonly=True),
     'unposted_value': fields.float('Unposted Amount', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'asset_asset_report')
        cr.execute('\n    \t    create or replace view asset_asset_report as (\n                select \n                    min(dl.id) as id,\n                    dl.name as name,\n                    dl.depreciation_date as depreciation_date,\n                    a.purchase_date as purchase_date,\n                    (CASE WHEN (select min(d.id) from account_asset_depreciation_line as d\n                                left join account_asset_asset as ac ON (ac.id=d.asset_id)\n                                where a.id=ac.id) = min(dl.id)\n                      THEN a.purchase_value\n                      ELSE 0\n                      END) as gross_value,\n                    dl.amount as depreciation_value, \n                    (CASE WHEN dl.move_check\n                      THEN dl.amount\n                      ELSE 0\n                      END) as posted_value,\n                    (CASE WHEN NOT dl.move_check\n                      THEN dl.amount\n                      ELSE 0\n                      END) as unposted_value,\n                    dl.asset_id as asset_id,\n                    dl.move_check as move_check,\n                    a.category_id as asset_category_id,\n                    a.partner_id as partner_id,\n                    a.state as state,\n                    count(dl.*) as nbr,\n                    a.company_id as company_id\n                from account_asset_depreciation_line dl\n                    left join account_asset_asset a on (dl.asset_id=a.id)\n                group by \n                    dl.amount,dl.asset_id,dl.depreciation_date,dl.name,\n                    a.purchase_date, dl.move_check, a.state, a.category_id, a.partner_id, a.company_id,\n                    a.purchase_value, a.id, a.salvage_value\n        )')


asset_asset_report()