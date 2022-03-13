# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrWorkLocation(models.Model):
    _inherit = 'hr.work.location'
    
    ot_approver_id = fields.Many2one('hr.employee', string='OT Approver')
    
  