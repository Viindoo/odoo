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
from openerp.osv import orm, fields

def name(n):
    return 'base_import.tests.models.%s' % n


class char(orm.Model):
    _name = name('char')
    _columns = {'value': fields.char('unknown', size=None)}


class char_required(orm.Model):
    _name = name('char.required')
    _columns = {'value': fields.char('unknown', size=None, required=True)}


class char_readonly(orm.Model):
    _name = name('char.readonly')
    _columns = {'value': fields.char('unknown', size=None, readonly=True)}


class char_states(orm.Model):
    _name = name('char.states')
    _columns = {'value': fields.char('unknown', size=None, readonly=True, states={'draft': [('readonly', False)]})}


class char_noreadonly(orm.Model):
    _name = name('char.noreadonly')
    _columns = {'value': fields.char('unknown', size=None, readonly=True, states={'draft': [('invisible', True)]})}


class char_stillreadonly(orm.Model):
    _name = name('char.stillreadonly')
    _columns = {'value': fields.char('unknown', size=None, readonly=True, states={'draft': [('readonly', True)]})}


class m2o(orm.Model):
    _name = name('m2o')
    _columns = {'value': fields.many2one(name('m2o.related'))}


class m2o_related(orm.Model):
    _name = name('m2o.related')
    _columns = {'value': fields.integer()}
    _defaults = {'value': 42}


class m2o_required(orm.Model):
    _name = name('m2o.required')
    _columns = {'value': fields.many2one(name('m2o.required.related'), required=True)}


class m2o_required_related(orm.Model):
    _name = name('m2o.required.related')
    _columns = {'value': fields.integer()}
    _defaults = {'value': 42}


class o2m(orm.Model):
    _name = name('o2m')
    _columns = {'value': fields.one2many(name('o2m.child'), 'parent_id')}


class o2m_child(orm.Model):
    _name = name('o2m.child')
    _columns = {'parent_id': fields.many2one(name('o2m')),
     'value': fields.integer()}


class preview_model(orm.Model):
    _name = name('preview')
    _columns = {'name': fields.char('Name', size=None),
     'somevalue': fields.integer('Some Value', required=True),
     'othervalue': fields.integer('Other Variable')}