# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta



class TaxEpaymentWizard(models.Model):
    _name = 'tax.epayment.wizard'
    _description = 'Tax Computation Wizard'
     

    company_id = fields.Many2one('res.company',  string='Company', required=True)
    date =  fields.Date(string='Date', required=True)
    
    
    def check_report(self):
        data = {}
        data['form'] = self.read(['company_id','date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['company_id','date'])[0])
        return self.env.ref('de_payroll_tax_reports.open_tax_epayment_action').report_action(self, data=data, config=False)
