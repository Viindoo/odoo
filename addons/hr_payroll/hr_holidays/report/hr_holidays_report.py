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

class hr_holidays_remaining_leaves_user(osv.osv):
    _name = 'hr.holidays.remaining.leaves.user'
    _description = 'Total holidays by type'
    _auto = False
    _columns = {'name': fields.char('Employee', size=64),
     'no_of_leaves': fields.integer('Remaining leaves'),
     'user_id': fields.many2one('res.users', 'User'),
     'leave_type': fields.char('Leave Type', size=64)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_holidays_remaining_leaves_user')
        cr.execute('\n            CREATE or REPLACE view hr_holidays_remaining_leaves_user as (\n                 SELECT\n                    min(hrs.id) as id,\n                    rr.name as name,\n                    sum(hrs.number_of_days) as no_of_leaves,\n                    rr.user_id as user_id,\n                    hhs.name as leave_type\n                FROM\n                    hr_holidays as hrs, hr_employee as hre,\n                    resource_resource as rr,hr_holidays_status as hhs\n                WHERE\n                    hrs.employee_id = hre.id and\n                    hre.resource_id =  rr.id and\n                    hhs.id = hrs.holiday_status_id\n                GROUP BY\n                    rr.name,rr.user_id,hhs.name\n            )\n        ')


hr_holidays_remaining_leaves_user()