import json
from odoo import models
from odoo.exceptions import UserError


class TaxEpaymentReport(models.AbstractModel):
    _name = 'report.de_payroll_tax_reports.epayment_report'
    _description = 'Epayment report'
    _inherit = 'report.report_xlsx.abstract'
    
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        data = self.env['tax.epayment.wizard'].browse(self.env.context.get('active_ids'))
        format1 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': False,'border': True})
        format2 = workbook.add_format({'font_size': '12', 'align': 'center', 'bold': False,'border': True})
        sheet = workbook.add_worksheet('Tax Epayment Report')
        bold = workbook. add_format({'bold': True, 'align': 'center','border': True})
        
        sheet.set_column('A:A', 5,)
        sheet.set_column('B:B', 10,)
        sheet.set_column('C:C', 20,)
        sheet.set_column('D:D', 20,)
        sheet.set_column('E:E', 30,)
        sheet.set_column('F:F', 20,)
        sheet.set_column('G:G', 40,)
        sheet.set_column('H:H', 20,)
        sheet.set_column('I:I', 20,)
        sheet.set_column('J:J', 20,)
        sheet.set_column('K:K', 20,)
        
        sheet.write(1,0, 'Sr No',bold)
        sheet.write(1,1, 'Payment Section' ,bold)
        sheet.write(1,2, 'TaxPayer NTN' ,bold) 
        sheet.write(1,3, 'TaxPayer CNIC' ,bold)
        sheet.write(1,4, 'TaxPayer Name' ,bold)
        sheet.write(1,5, 'TaxPayer City',bold)
        sheet.write(1,6, 'TaxPayer Address',bold)
        sheet.write(1,7, 'TaxPayer Status',bold)
        sheet.write(1,8, 'TaxPayer Business Name',bold)
        sheet.write(1,9, 'Taxable Amount',bold)
        sheet.write(1,10, 'Tax Amount',bold)
        row = 3
        serial_count = 0
        payslips = self.env['hr.payslip'].search([('company_id','=',data.company_id.id),('fiscal_month','=',data.date.month),('tax_year','=',data.date.year),('state','=','done')])
        for slip in payslips:  
            serial_count += 1
            current_tax_amount = 0 
            for rule in slip.line_ids:
                if rule.code=='INC01': 
                    current_tax_amount = rule.amount
            if current_tax_amount > 0:              
                sheet.write(row, 0, serial_count, format1)
                sheet.write(row, 1, 149, format1)
                sheet.write(row, 2, str(slip.employee_id.ntn if slip.employee_id.ntn else '-'), format1)
                sheet.write(row, 3, str(slip.employee_id.cnic if slip.employee_id.cnic else '-'), format1)
                sheet.write(row, 4, str(slip.employee_id.name), format1)
                sheet.write(row, 5, str(slip.employee_id.address_home_id.city if slip.employee_id.address_home_id.city else '-'), format1)  
                sheet.write(row, 6, str(slip.employee_id.address_home_id.street if slip.employee_id.address_home_id.street else '-'), format2)
                sheet.write(row, 7, 'INDIVIDUAL', format1) 
                sheet.write(row, 8, 'Salaried Person', format1) 
                sheet.write(row, 9, str('{0:,}'.format(int(round(slip.current_taxable_amount)))), format1)  
                sheet.write(row, 10, str('{0:,}'.format(int(round(current_tax_amount)))), format1)
                row += 1           