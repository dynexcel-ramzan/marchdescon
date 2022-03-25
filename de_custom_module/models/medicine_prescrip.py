# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MedicinePrescrip(models.Model):
    _name = 'medicine.prescrip'
    _description = 'Medicine Prescrip'
    
    
    name = fields.Char(string='Description', required=True) 
    employee_id = fields.Many2one('hr.employee', strin='Employee', required=True)
    employee_ids = fields.Many2many('hr.employee', strin='Employees')
    amount = fields.Float(string='Amount') 
    currency_id = fields.Many2one('res.currency',string='Currency') 
