from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestIbanCountry(TransactionCase):

    def test_company_in_non_iban_country_does_not_use_iban(self):
        self.env.company.country_id = self.env.ref('base.vn')
        self.assertFalse(self.env['res.partner.bank'].check_company_uses_iban())

    def test_company_in_iban_country_uses_iban(self):
        for country in ('base.be', 'base.de'):
            self.env.company.country_id = self.env.ref(country)
            self.assertTrue(self.env['res.partner.bank'].check_company_uses_iban(), country)

    def test_company_in_territory_banking_with_another_country_iban_uses_iban(self):
        for country in ('base.re', 'base.ax', 'base.je'):
            self.env.company.country_id = self.env.ref(country)
            self.assertTrue(self.env['res.partner.bank'].check_company_uses_iban(), country)

    def test_company_without_country_keeps_iban_check(self):
        self.env.company.country_id = False
        self.assertTrue(self.env['res.partner.bank'].check_company_uses_iban())
