from odoo import api, fields, models


class BonusTag(models.Model):
    _name = 'bonus.tag'
    
    _description = 'Bonus'
    
    name = fields.Char(string='Bonus', required=True)
    amount = fields.Float(string='Amount', required=True)
