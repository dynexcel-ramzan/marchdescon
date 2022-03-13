from odoo import api, fields, models, _
from calendar import monthrange

from odoo.exceptions import UserError
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


class HrOvertimeLock(models.Model):
    _name = 'hr.overtime.lock'
    _description = 'Overtime Approval Lock'
    _rec_name = 'date'

   
    date = fields.Date(string='Date', required=True)  
   
    
    
    