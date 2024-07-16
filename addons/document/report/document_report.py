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
from openerp.osv import fields, osv
from openerp import tools

class report_document_user(osv.osv):
    _name = 'report.document.user'
    _description = 'Files details by Users'
    _auto = False
    _columns = {'name': fields.char('Year', size=64, readonly=True),
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
     'user_id': fields.integer('Owner', readonly=True),
     'user': fields.related('user_id', 'name', type='char', size=64, readonly=True),
     'directory': fields.char('Directory', size=64, readonly=True),
     'datas_fname': fields.char('File Name', size=64, readonly=True),
     'create_date': fields.datetime('Date Created', readonly=True),
     'change_date': fields.datetime('Modified Date', readonly=True),
     'file_size': fields.integer('File Size', readonly=True),
     'nbr': fields.integer('# of Files', readonly=True),
     'type': fields.char('Directory Type', size=64, readonly=True)}

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_document_user')
        cr.execute("\n            CREATE OR REPLACE VIEW report_document_user as (\n                 SELECT\n                     min(f.id) as id,\n                     to_char(f.create_date, 'YYYY') as name,\n                     to_char(f.create_date, 'MM') as month,\n                     f.user_id as user_id,\n                     count(*) as nbr,\n                     d.name as directory,\n                     f.datas_fname as datas_fname,\n                     f.create_date as create_date,\n                     f.file_size as file_size,\n                     min(d.type) as type,\n                     f.write_date as change_date\n                 FROM ir_attachment f\n                     left join document_directory d on (f.parent_id=d.id and d.name<>'')\n                 group by to_char(f.create_date, 'YYYY'), to_char(f.create_date, 'MM'),d.name,f.parent_id,d.type,f.create_date,f.user_id,f.file_size,d.type,f.write_date,f.datas_fname\n             )\n        ")


class report_document_file(osv.osv):
    _name = 'report.document.file'
    _description = 'Files details by Directory'
    _auto = False
    _columns = {'file_size': fields.integer('File Size', readonly=True),
     'nbr': fields.integer('# of Files', readonly=True),
     'month': fields.char('Month', size=24, readonly=True)}
    _order = 'month'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_document_file')
        cr.execute("\n            create or replace view report_document_file as (\n                select min(f.id) as id,\n                       count(*) as nbr,\n                       min(EXTRACT(MONTH FROM f.create_date)||'-'||to_char(f.create_date,'Month')) as month,\n                       sum(f.file_size) as file_size\n                from ir_attachment f\n                group by EXTRACT(MONTH FROM f.create_date)\n             )\n        ")