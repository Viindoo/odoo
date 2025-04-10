from odoo import api, fields, models

class PayslipDeductionType(models.Model):
    _name = "payslip.deduction.type"
    _description = 'Payslip Deduction Type'

    name = fields.Char(string='Deduction Name', required=True)
    default_amount = fields.Float(string='Default Amount', required=True)
    active = fields.Boolean(default=True)
    auto_apply = fields.Boolean(string='Apply by Default', default=True)