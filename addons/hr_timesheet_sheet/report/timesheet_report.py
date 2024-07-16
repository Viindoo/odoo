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

class timesheet_report(osv.osv):
    _name = 'timesheet.report'
    _description = 'Timesheet'
    _auto = False
    _columns = {'year': fields.char('Year', size=64, required=False, readonly=True),
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
     'date': fields.date('Date', readonly=True),
     'name': fields.char('Description', size=64, readonly=True),
     'product_id': fields.many2one('product.product', 'Product'),
     'general_account_id': fields.many2one('account.account', 'General Account', readonly=True),
     'user_id': fields.many2one('res.users', 'User', readonly=True),
     'to_invoice': fields.many2one('hr_timesheet_invoice.factor', 'Type of Invoicing', readonly=True),
     'account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
     'nbr': fields.integer('#Nbr', readonly=True),
     'total_diff': fields.float('#Total Diff', readonly=True),
     'total_timesheet': fields.float('#Total Timesheet', readonly=True),
     'total_attendance': fields.float('#Total Attendance', readonly=True),
     'company_id': fields.many2one('res.company', 'Company', readonly=True),
     'department_id': fields.many2one('hr.department', 'Department', readonly=True),
     'date_from': fields.date('Date from', readonly=True),
     'date_to': fields.date('Date to', readonly=True),
     'date_current': fields.date('Current date', required=True),
     'state': fields.selection([('new', 'New'),
               ('draft', 'Draft'),
               ('confirm', 'Confirmed'),
               ('done', 'Done')], 'Status', readonly=True),
     'quantity': fields.float('Time', readonly=True),
     'cost': fields.float('#Cost', readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'timesheet_report')
        cr.execute("\n            create or replace view timesheet_report as (\n                    select\n                        min(aal.id) as id,\n                        htss.name,\n                        aal.date as date,\n                        htss.date_from,\n                        htss.date_to,\n                        to_char(htss.date_from, 'YYYY-MM-DD') as day,\n                        to_char(htss.date_from, 'YYYY') as year,\n                        to_char(htss.date_from, 'MM') as month,\n                        count(*) as nbr,\n                        aal.unit_amount as quantity,\n                        aal.amount as cost,\n                        aal.account_id,\n                        aal.product_id,\n                        (SELECT   sum(day.total_difference)\n                            FROM hr_timesheet_sheet_sheet AS sheet \n                            LEFT JOIN hr_timesheet_sheet_sheet_day AS day \n                            ON (sheet.id = day.sheet_id) where sheet.id=htss.id) as total_diff,\n                        (SELECT sum(day.total_timesheet)\n                            FROM hr_timesheet_sheet_sheet AS sheet \n                            LEFT JOIN hr_timesheet_sheet_sheet_day AS day \n                            ON (sheet.id = day.sheet_id) where sheet.id=htss.id) as total_timesheet,\n                        (SELECT sum(day.total_attendance)\n                            FROM hr_timesheet_sheet_sheet AS sheet \n                            LEFT JOIN hr_timesheet_sheet_sheet_day AS day \n                            ON (sheet.id = day.sheet_id) where sheet.id=htss.id) as total_attendance,\n                        aal.to_invoice,\n                        aal.general_account_id,\n                        htss.user_id,\n                        htss.company_id,\n                        htss.department_id,\n                        htss.state\n                    from account_analytic_line as aal\n                    left join hr_analytic_timesheet as hat ON (hat.line_id=aal.id)\n                    left join hr_timesheet_sheet_sheet as htss ON (hat.line_id=htss.id)\n                    group by\n                        aal.account_id,\n                        aal.date,\n                        htss.date_from,\n                        htss.date_to,\n                        aal.unit_amount,\n                        aal.amount,\n                        aal.to_invoice,\n                        aal.product_id,\n                        aal.general_account_id,\n                        htss.name,\n                        htss.company_id,\n                        htss.state,\n                        htss.id,\n                        htss.department_id,\n                        htss.user_id\n            )\n        ")


timesheet_report()