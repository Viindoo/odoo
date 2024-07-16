# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
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
"""
This module contains the base class for all observer objects
"""
_is_source_ = True

class Observer(object):
    """
    Base Class for all charts and reports.
    
    @var visible: Specifies if the observer is visible
           at the navigation bar inside the gui.
    
    @var link_view: syncronizes the marked objects in all views.
    
    """
    __type_name__ = None
    __type_image__ = None
    visible = True
    link_view = True
    __attrib_completions__ = {'visible': 'visible = False',
     'link_view': 'link_view = False'}

    def register_editors(cls, registry):
        pass

    register_editors = classmethod(register_editors)


factories = {}
clear_cache_funcs = {}