from odoo import api, fields, models


class PayslipDeduction(models.Model):
    _name = 'payslip.deduction'
    _description = 'Payslip Deduction Line'

    payslip_id = fields.Many2one('employee.payslip', string='Payslip', ondelete='cascade')
    type_id = fields.Many2one('payslip.deduction.type', string='Deduction Type')
    amount = fields.Float(string='Amount', required=True)
    note = fields.Text(string='Description')
    
    @api.onchange('type_id')
    def _onchange_type_id(self):
        for line in self:
            if line.type_id:
                line.amount = line.type_id.default_amount
