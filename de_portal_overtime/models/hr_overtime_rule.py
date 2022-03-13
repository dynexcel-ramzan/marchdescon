# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrOvertimeRule(models.Model):
    _inherit = 'hr.overtime.rule'
    
    exceeding_limit = fields.Many2one(string='Exceeding limit')
    
    