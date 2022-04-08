# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReportExpense(models.Model):
    _inherit = 'hr.expense.sheet'
    
    
    approve_date = fields.Date(string="Approve Date")
    post_date = fields.Date(string="Post Date")
    payment_date = fields.Date(string="Payment Date")
    doc_received  = fields.Date(string="Document Received Date")
    

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
