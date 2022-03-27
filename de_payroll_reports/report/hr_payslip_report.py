# -*- coding: utf-8 -*-
import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class HrPayslipReport(models.AbstractModel):
    _name = 'report.de_payroll_reports.slip_portal_report'
    _description = 'Slip Report'
    
    '''Find payroll Slip Report for selected Record'''
    @api.model
    def _get_report_values(self, docids, data=None): 
        slip = self.env['hr.payslip'].sudo().search( [('id','=', data['id'])] )
        return {
                'docs': slip,
        }