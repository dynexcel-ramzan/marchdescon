# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
class HrWorkLocation(models.Model):
    _inherit = 'hr.work.location'    
    
class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    

class HrPayslipStructure(models.Model):
    
    _inherit = 'hr.payroll.structure'  
    
    
class HrPayslipLines(models.Model):
    _inherit = 'hr.payslip.line'    