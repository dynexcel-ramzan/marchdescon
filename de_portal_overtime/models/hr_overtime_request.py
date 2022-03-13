from odoo import api, fields, models, _
from calendar import monthrange

from odoo.exceptions import UserError
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


class HrOvertimeRequest(models.Model):
    _inherit = 'hr.overtime.request'
    

   
#     @api.onchange('overtime_hours')
#     def onchange_overtime_hours(self):
#         for line in self:
#             self.env['hr.overtime.request'].search([('employee_id','=',line.employee_id.id),('date','=',)])
   
    
    
    