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
from openerp import tools
import openerp.addons.decimal_precision as dp

class mrp_workorder(osv.osv):
    _name = 'mrp.workorder'
    _description = 'Work Order Report'
    _auto = False
    _columns = {'year': fields.char('Year', size=64, readonly=True),
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
     'day': fields.char('Day', size=64, readonly=True),
     'nbr': fields.integer('# of Lines', readonly=True),
     'date': fields.date('Date', readonly=True),
     'product_id': fields.many2one('product.product', 'Product', readonly=True),
     'product_qty': fields.float('Product Qty', digits_compute=dp.get_precision('Product Unit of Measure'), readonly=True),
     'state': fields.selection([('draft', 'Draft'),
               ('startworking', 'In Progress'),
               ('pause', 'Pause'),
               ('cancel', 'Cancelled'),
               ('done', 'Finished')], 'Status', readonly=True),
     'total_hours': fields.float('Total Hours', readonly=True),
     'total_cycles': fields.float('Total Cycles', readonly=True),
     'delay': fields.float('Delay', readonly=True),
     'production_id': fields.many2one('mrp.production', 'Production', readonly=True),
     'workcenter_id': fields.many2one('mrp.workcenter', 'Work Center', readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'mrp_workorder')
        cr.execute("\n            create or replace view mrp_workorder as (\n                select\n                    to_date(to_char(wl.date_planned, 'MM-dd-YYYY'),'MM-dd-YYYY') as date,\n                    to_char(wl.date_planned, 'YYYY') as year,\n                    to_char(wl.date_planned, 'MM') as month,\n                    to_char(wl.date_planned, 'YYYY-MM-DD') as day,\n                    min(wl.id) as id,\n                    mp.product_id as product_id,\n                    sum(wl.hour) as total_hours,\n                    avg(wl.delay) as delay,\n                    (w.costs_hour*sum(wl.hour)) as total_cost,\n                    wl.production_id as production_id,\n                    wl.workcenter_id as workcenter_id,\n                    sum(wl.cycle) as total_cycles,\n                    count(*) as nbr,\n                    sum(mp.product_qty) as product_qty,\n                    wl.state as state\n                from mrp_production_workcenter_line wl\n                    left join mrp_workcenter w on (w.id = wl.workcenter_id)\n                    left join mrp_production mp on (mp.id = wl.production_id)\n                group by\n                    w.costs_hour, mp.product_id, mp.name, wl.state, wl.date_planned, wl.production_id, wl.workcenter_id\n        )")


mrp_workorder()