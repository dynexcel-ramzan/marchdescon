import json
from odoo import models
from odoo.exceptions import UserError


class ORAGLaccount(models.AbstractModel):
    _name = 'report.de_payroll_reconcilation_report.gl_report'
    _description = 'GL Account Report'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, lines):
        data = self.env['ora.account.wizard'].browse(self.env.context.get('active_ids'))
        format1 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': False})
        sheet = workbook.add_worksheet('GL Account report')
        bold = workbook. add_format({'bold': True, 'align': 'center','border': True})        
        sheet.set_column('A:A', 5,)
        sheet.set_column('B:B', 30,)
        sheet.set_column('C:D', 20,)
        sheet.set_column('E:F', 50,)
        sheet.set_column('G:H', 20,)
        sheet.set_column('I:J', 20,)
        sheet.set_column('K:L', 20,)        
        sheet.write(1,0, 'Sr#',bold)
        sheet.write(1,1, 'Account' ,bold)
        sheet.write(1,2, 'Debit' , bold)   
        sheet.write(1,3, 'Credit' , bold)
        sheet.write(1,4, 'Description', bold)
        analytic_account_list = []
        credit_account_list = []
        debit_account_list = []
        final_gl_account_list = []        
        move_lines = self.env['account.move.line'].sudo().search([('company_id','=',data.company_id.id),('date','>=', data.date),('date','<=', data.date)]) 
        for mv in move_lines:
            if mv.account_id.ora_credit==True:  
                credit_account_list.append(mv.account_id.id)
            if mv.account_id.ora_debit==True:  
                debit_account_list.append(mv.account_id.id)                
            analytic_account_list.append(mv.analytic_account_id.id) 
                
        uniq_analytic_account_list = set(analytic_account_list)
        uniq_credit_account_list = set(credit_account_list)
        uniq_debit_account_list = set(debit_account_list)
        mv_account_code = 0
        for credit_account in uniq_credit_account_list:
            credit_total = 0
            mv_account_code = 0
            for mv_line in move_lines:
                if credit_account == mv_line.account_id.id:
                    credit_total +=  mv_line.credit
                    mv_account_code = mv_line.ora_account_code
            if  credit_total > 0:       
                final_gl_account_list.append({
                    'account_code': mv_account_code,
                    'account':  self.env['account.account'].search([('id','=',credit_account)], limit=1).name ,
                    'debit': 0,
                    'credit': credit_total,
                })
        debit_mv_account_code = 0        
        for analytic in uniq_analytic_account_list:            
            for debit_account in uniq_debit_account_list:
                debit_total = 0 
                debit_mv_account_code = 0
                for mv_line in move_lines:
                    if analytic == mv_line.analytic_account_id.id and debit_account == mv_line.account_id.id:
                        debit_total +=  mv_line.debit
                        debit_mv_account_code = mv_line.ora_account_code
                if  debit_total > 0:       
                    final_gl_account_list.append({
                           'account_code': debit_mv_account_code ,
                           'account': self.env['account.account'].search([('id','=',debit_account)], limit=1).name ,
                           'debit': debit_total ,
                           'credit':  0,
                    }) 
        serial_account=1
        row = 2                   
        for uniq_gl_account in final_gl_account_list:               
            sheet.write(row, 0, serial_account, format1)
            sheet.write(row, 1, uniq_gl_account['account_code'], format1)
            sheet.write(row, 2, '{0:,}'.format(int(round(uniq_gl_account['debit']))), format1)
            sheet.write(row, 3, '{0:,}'.format(int(round(uniq_gl_account['credit']))), format1)
            sheet.write(row, 4, uniq_gl_account['account'], format1)
            serial_account += 1
            row += 1           