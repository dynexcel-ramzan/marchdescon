# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta


class ReconciliationWizard(models.Model):
    _name = 'reconciliation.wizard'
    _description = 'Reconciliation Wizard'

    company_id = fields.Many2one('res.company',  string='Company', required=True)
    company_number = fields.Integer(string='Company Code')
    date_from =  fields.Date(string='Previous Month')
    date_to =  fields.Date(string='Current Month', required=True)
    
       
    @api.onchange('date_to')
    def onchange_date_to(self):
        for line in self:
            if line.date_to:
                line.date_from =line.date_to - timedelta(31)
                
    def check_report(self):
        data = {}
        data['form'] = self.read(['company_id','date_from', 'date_to'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['company_id','date_from', 'date_to'])[0])
        return self.env.ref('de_payroll_reconcilation_report.open_payroll_reconciliation_action').report_action(self, data=data, config=False)
