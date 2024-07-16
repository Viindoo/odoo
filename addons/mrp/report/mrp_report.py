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

class report_workcenter_load(osv.osv):
    _name = 'report.workcenter.load'
    _description = 'Work Center Load'
    _auto = False
    _log_access = False
    _columns = {'name': fields.char('Week', size=64, required=True),
     'workcenter_id': fields.many2one('mrp.workcenter', 'Work Center', required=True),
     'cycle': fields.float('Number of Cycles'),
     'hour': fields.float('Number of Hours')}

    def init(self, cr):
        cr.execute("\n            create or replace view report_workcenter_load as (\n                SELECT\n                    min(wl.id) as id,\n                    to_char(p.date_planned,'YYYY:mm:dd') as name,\n                    SUM(wl.hour) AS hour,\n                    SUM(wl.cycle) AS cycle,\n                    wl.workcenter_id as workcenter_id\n                FROM\n                    mrp_production_workcenter_line wl\n                    LEFT JOIN mrp_production p\n                        ON p.id = wl.production_id\n                GROUP BY\n                    wl.workcenter_id,\n                    to_char(p.date_planned,'YYYY:mm:dd')\n            )")


report_workcenter_load()

class report_mrp_inout(osv.osv):
    _name = 'report.mrp.inout'
    _description = 'Stock value variation'
    _auto = False
    _log_access = False
    _rec_name = 'date'
    _columns = {'date': fields.char('Week', size=64, required=True),
     'value': fields.float('Stock value', required=True, digits=(16, 2))}

    def init(self, cr):
        cr.execute("\n            create or replace view report_mrp_inout as (\n                select\n                    min(sm.id) as id,\n                    to_char(sm.date,'YYYY:IW') as date,\n                    sum(case when (sl.usage='internal') then\n                        pt.standard_price * sm.product_qty\n                    else\n                        0.0\n                    end - case when (sl2.usage='internal') then\n                        pt.standard_price * sm.product_qty\n                    else\n                        0.0\n                    end) as value\n                from\n                    stock_move sm\n                left join product_product pp\n                    on (pp.id = sm.product_id)\n                left join product_template pt\n                    on (pt.id = pp.product_tmpl_id)\n                left join stock_location sl\n                    on ( sl.id = sm.location_id)\n                left join stock_location sl2\n                    on ( sl2.id = sm.location_dest_id)\n                where\n                    sm.state in ('waiting','confirmed','assigned')\n                group by\n                    to_char(sm.date,'YYYY:IW')\n            )")


report_mrp_inout()