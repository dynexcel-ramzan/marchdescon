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
    
    prescrip_line = fields.One2many('medicine.prescrip.line', 'prescrip_id', string='Lines',  copy=True)

    
class MedicinePrescripLine(models.Model):
    _name = 'medicine.prescrip.line'
    _description = 'Medicine Prescrip Line'
    
    product_id = fields.Many2many('product.product', strin='Product', required=True)
    name = fields.Char(string='Description', required=True) 
    amount = fields.Float(string='Amount')
    prescrip_id = fields.Many2one('medicine.prescrip', strin='Prescrip')
    