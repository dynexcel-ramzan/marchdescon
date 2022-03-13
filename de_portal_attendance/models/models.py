# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'  

    
    #def action_check_write_date(self):
    #    for line in self:
    #        if line.att_date: 
    #            if str(line.att_date ) < '2022-02-16' and self.env.user!=2:
    #                raise UserError('Payroll Workdays Deadline Expire.Please contact HR Department!')
        
    
   # def write(self, values):
   #     result = super(HrAttendance, self).write(values) 
   #     self.action_check_write_date()
   #     return result


    #def action_check_date_create(self):
    #    for line in self:
    #        if line.att_date: 
    #            if str(line.att_date ) < '2022-02-16' and self.env.user!=2:
    #                raise UserError('Payroll Workdays Deadline Expire.Please contact HR Department!')
        
    
    #def create(self, values):
    #    result = super(HrAttendance, self).create(values) 
    #    result.action_check_date_create()
    #    return result
    
    


    

    
    
    

    
