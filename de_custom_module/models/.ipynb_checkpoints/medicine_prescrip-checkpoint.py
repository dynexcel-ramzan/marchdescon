# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MedicinePrescrip(models.Model):
    _name = 'medicine.prescrip'
    _description = 'Medicine Prescrip'
    
    
    name = fields.Char(string='Description') 
    employee_id = fields.Many2one('hr.employee', strin='Employee')
    employee_ids = fields.Many2many('hr.employee', strin='Employees')

