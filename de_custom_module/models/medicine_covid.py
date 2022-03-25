# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MedicineCovid(models.Model):
    _name = 'medicine.covid'
    _description = 'Medicine Covid'
    
    
    name = fields.Char(string='Description') 
    employee_id = fields.Many2one('hr.employee', strin='Employee')
    employee_ids = fields.Many2many('hr.employee', strin='Employees')

