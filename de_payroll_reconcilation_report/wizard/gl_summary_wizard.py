# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta


class ORAAccountWizard(models.Model):
    _name = 'ora.account.wizard'
    _description = 'ORA Account Wizard'

    company_id = fields.Many2one('res.company',  string='Company', required=True)
    date =  fields.Date(string='Month', required=True, default='2022-02-15')
                   
    def check_report(self):
        data = {}
        data['form'] = self.read(['company_id','date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['company_id','date'])[0])
        return self.env.ref('de_payroll_reconcilation_report.open_ora_account_wizard_action').report_action(self, data=data, config=False)
