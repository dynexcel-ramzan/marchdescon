# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    
    ref1 = fields.Char(string='Reference1', required=True)
    ref2 = fields.Integer(string='Reference2', copy=True)
    check_number = fields.Char(string='Check Number')
