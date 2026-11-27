import { models } from "@web/../tests/web_test_helpers";

export class ResPartnerBank extends models.ServerModel {
    _name = "res.partner.bank";

    check_company_uses_iban() {
        return true;
    }
}
