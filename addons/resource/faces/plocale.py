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
import gettext
import os.path
import locale
import sys

def _get_translation():
    try:
        return gettext.translation('faces')
    except:
        try:
            if sys.frozen:
                path = os.path.dirname(sys.argv[0])
                path = os.path.join(path, 'resources', 'faces', 'locale')
            else:
                path = os.path.split(__file__)[0]
                path = os.path.join(path, 'locale')
            return gettext.translation('faces', path)
        except Exception as e:
            return None

    return None


def get_gettext():
    trans = _get_translation()
    if trans:
        return trans.ugettext
    return lambda msg: msg


def get_encoding():
    trans = _get_translation()
    if trans:
        return trans.charset()
    return locale.getpreferredencoding()