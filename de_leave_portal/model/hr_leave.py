# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'      
    
    
    #def action_check_write_date(self):
    #    for line in self:
    #        if line.request_date_from:        
    #            if str(line.request_date_from ) < '2022-02-16':
    #                raise UserError('Payroll Workdays Deadline Expire.Please contact HR Department!')
        
    
    #def create(self, values):
    #    result = super(HrLeave, self).create(values)
    #    result.action_check_write_date()
    #    
    #    return result


    #def action_check_write_date_write(self):
    #    for line in self:
    #        if str(line.request_date_from ) < '2022-02-16':
    #            raise UserError('Payroll Workdays Deadline Expire.Please contact HR Department!')
        
    
    #def write(self, values):
    #    result = super(HrLeave, self).write(values)
    #    self.action_check_write_date_write()        
    #    return result
    
    

    


    
class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'      
    
    
    is_publish = fields.Boolean(string="Publish At Website")
    

class HrLeave(models.Model):
    _inherit = 'hr.leave'          
    

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'
    

class ResourceCalanderLeaves(models.Model):
    _inherit = 'resource.calendar.leaves'    


    

    

class ResourceCalanderAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'  
            

class ResourceResource(models.Model):
    _inherit = 'resource.resource' 
    
class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'  
                
            


    