# Embedded file name: /opt/lamthao/server/openerp/addons/decimal_precision/decimal_precision.py
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields

class decimal_precision(osv.osv):
    _name = 'decimal.precision'
    _columns = {'name': fields.char('Usage', size=50, select=True, required=True),
     'digits': fields.integer('Digits', required=True)}
    _defaults = {'digits': 4}
    _sql_constraints = [('name_uniq', 'unique (name)', 'Only one value can be defined for each given usage!')]

    @tools.ormcache(skiparg=3)
    def precision_get(self, cr, uid, application):
        cr.execute('select digits from decimal_precision where name=%s', (application,))
        res = cr.fetchone()
        if res:
            return res[0]
        return 4

    def create(self, cr, uid, data, context = None):
        res = super(decimal_precision, self).create(cr, uid, data, context=context)
        self.precision_get.clear_cache(self)
        return res

    def unlink(self, cr, uid, ids, context = None):
        res = super(decimal_precision, self).unlink(cr, uid, ids, context=context)
        self.precision_get.clear_cache(self)
        return res

    def write(self, cr, uid, ids, data, *args, **argv):
        res = super(decimal_precision, self).write(cr, uid, ids, data, *args, **argv)
        self.precision_get.clear_cache(self)
        for obj in self.pool.obj_list():
            for colname, col in self.pool.get(obj)._columns.items():
                if isinstance(col, (fields.float, fields.function)):
                    col.digits_change(cr)

        return res


decimal_precision()

def get_precision(application):

    def change_digit(cr):
        res = pooler.get_pool(cr.dbname).get('decimal.precision').precision_get(cr, SUPERUSER_ID, application)
        return (16, res)

    return change_digit