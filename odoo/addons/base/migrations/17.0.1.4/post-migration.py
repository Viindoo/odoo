from odoo import api, SUPERUSER_ID


def _update_currency_rate_access_rule(env):
    currency_rate_rule = env.ref('base.res_currency_rate_rule')
    currency_rate_rule.domain_force = '''
        ['|', ('company_id', 'parent_of', company_ids), ('company_id', '=', False)]
    '''

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _update_currency_rate_access_rule(env)
