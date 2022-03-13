# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
import cx_Oracle

logger = logging.getLogger(__name__)




class AccountAccount(models.Model):
    _inherit = 'account.move'

    is_posted = fields.Boolean(string="Posted On Oracle")

    def action_delete_ebs_data(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
        cur = conn.cursor()
        statement='delete from XX_ODOO_GL_INTERFACE'
        statementfetch = 'select STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR, REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10, REFERENCE21, GROUP_ID, PERIOD_NAME from XX_ODOO_GL_INTERFACE'
        cur.execute(statement)
        conn.commit()
        cur.execute(statementfetch) 
        attendances = cur.fetchall()
        raise UserError(str(attendances))
    
    def action_view_jv_data_posted(self):
        user_attendance = self.env['hr.user.attendance']
        attendance_ids = []
        conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
        cur = conn.cursor()
        
        statementfetch = 'select STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR, REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10, REFERENCE21, GROUP_ID, PERIOD_NAME from XX_ODOO_GL_INTERFACE'
        cur.execute(statementfetch) 
        attendances = cur.fetchall()
        saatatementfetch = 'select count(*) from XX_ODOO_GL_INTERFACE'
        cur.execute(saatatementfetch) 
        aattendances = cur.fetchall()
        raise UserError('Count '+str(aattendances)+' '+str(attendances))


    def action_posted_on_oracle_payroll(self):
        analytic_account_list = []
        credit_account_list = []
        debit_account_list = []
        final_gl_account_list = []
        move_lines = 0
        total_serial_no = 0
        ledgerna = 0 
        batchid = 0
        batch_name = ''
        for line in self:
            ledgerna = line.company_id.ledger_id
            move_lines = self.env['account.move.line'].search(
                [('company_id', '=', line.company_id.id), ('date', '>=', line.date),('date','<=',line.date),('journal_id.ora_ledger_label','=','Payroll')])
        for jv in move_lines:
            if jv.account_id.ora_credit==True:
                credit_account_list.append(jv.account_id.id)
            if jv.account_id.ora_debit==True:
                debit_account_list.append(jv.account_id.id)
            analytic_account_list.append(jv.analytic_account_id.id)
        uniq_analytic_account_list = set(analytic_account_list)
        uniq_credit_account_list = set(credit_account_list)
        uniq_debit_account_list = set(debit_account_list)
        mv_account_code = 0
        for credit_account in uniq_credit_account_list:
            credit_total = 0
            mv_account_code = 0
             
            for mv_line in move_lines:
                if credit_account == mv_line.account_id.id:
                    code_spliting = mv_line.account_id.code.split('.')
                    inv_name = self.env['account.account'].search([('id', '=', credit_account)], limit=1).name,
                    ledger_id = mv_line.move_id.company_id.ledger_id,
                    currency_code =  mv_line.company_id.currency_id.name,
                    jv_category = 'Odoo ' + str(mv_line.move_id.journal_id.ora_ledger_label),
                    segment1 = mv_line.move_id.company_id.segment1,
                    segment2 = mv_line.analytic_account_id.code if mv_line.analytic_account_id else '000',
                    segment3 = code_spliting[0],
                    segment4 = code_spliting[1],
                    ref1 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label) + ' ' + str(
                        mv_line.move_id.company_id.ledger_id) + '-' + str(
                        mv_line.move_id.date.strftime('%Y')) + '-' + str(
                        mv_line.move_id.date.strftime('%m')) + '-' + str(mv_line.move_id.date.strftime('%d')),
                    ref2 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label) + ' ' + str(
                        mv_line.move_id.company_id.ledger_id) + '-' + str(
                        mv_line.move_id.date.strftime('%Y')) + '-' + str(
                        mv_line.move_id.date.strftime('%m')) + '-' + str(mv_line.move_id.date.strftime('%d')),
                    payslip = self.env['hr.payslip'].search([('move_id', '=', mv_line.move_id.id)], limit=1)
                    batchid = payslip.payslip_run_id.id
                    ref4 = str(payslip.payslip_run_id.id)+' ' +str(payslip.payslip_run_id.name),                        
                    ref5 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label)+' '+ str(payslip.payslip_run_id.id)+' ' +str(payslip.payslip_run_id.name),
                    ref6 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label)+' '+str(mv_line.move_id.journal_id.name),
                    ref10 = str(payslip.payslip_run_id.id) + ' ' + str(payslip.payslip_run_id.name) ,    
                    payslip = self.env['hr.payslip'].search([('move_id', '=', mv_line.move_id.id)], limit=1)
                    batchid = payslip.payslip_run_id.id
                    batch_name = payslip.payslip_run_id.name
                    ref6 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label)+' '+str(mv_line.move_id.journal_id.name),
                    ref10 =  'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label) + ' ' + str(
                        payslip.payslip_run_id.id) + ' ' + str(payslip.payslip_run_id.name) ,
                    ref21= str(mv_line.move_id.company_id.ledger_id) + '-' + str(payslip.payslip_run_id.id) + '-' + str(
                        mv_line.id),
                    group=str(mv_line.move_id.company_id.ledger_id) + str(fields.datetime.now().strftime('%Y%m%d')) + str(
                        payslip.payslip_run_id.id)
                    
                    period = mv_line.date.strftime('%b-%Y')
                    inv_date = mv_line.date.strftime('%d-%b-%Y')
                    credit_total +=  mv_line.credit
                    mv_account_code = mv_line.ora_account_code
            if  credit_total > 0:
                total_serial_no += 1
                final_gl_account_list.append({
                    'total_serial_no': total_serial_no,
                    'inv_name': inv_name,
                    'ledger_id': ledger_id,
                    'currency_code': currency_code,
                    'jv_category': jv_category,
                    'segment1': segment1,
                    'segment2': segment2,
                    'segment3': segment3,
                    'segment4': segment4,
                    'ref1': ref1 ,
                    'ref2': ref2 ,
                    'ref4': ref4 ,
                    'ref5': ref5 ,
                    'ref6': ref6 ,
                    'ref10': str(batchid) + ' '+ str(batch_name) +' ' + str(total_serial_no) ,
                    'ref21': str(ledgerna) + '-' + str(batchid) + '-' + str(total_serial_no) ,
                    'group': group,
                    'period': period,
                    'inv_date': inv_date,
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
                    if debit_account == mv_line.account_id.id and analytic == mv_line.analytic_account_id.id:
                        code_spliting = mv_line.account_id.code.split('.')
                        inv_name = self.env['account.account'].search([('id', '=', debit_account)], limit=1).name,
                        ledger_id = mv_line.move_id.company_id.ledger_id,
                        currency_code = mv_line.company_id.currency_id.name,
                        jv_category = 'Odoo ' + str(mv_line.move_id.journal_id.ora_ledger_label),
                        segment1 = mv_line.move_id.company_id.segment1,
                        segment2 = mv_line.analytic_account_id.code if mv_line.analytic_account_id else '000',
                        segment3 = code_spliting[0],
                        segment4 = code_spliting[1],
                        ref1 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label) + ' ' + str(
                                mv_line.move_id.company_id.ledger_id) + '-' + str(
                                mv_line.move_id.date.strftime('%Y')) + '-' + str(
                                mv_line.move_id.date.strftime('%m')) + '-' + str(mv_line.move_id.date.strftime('%d')),
                        ref2 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label) + ' ' + str(
                                mv_line.move_id.company_id.ledger_id) + '-' + str(
                                mv_line.move_id.date.strftime('%Y')) + '-' + str(
                                mv_line.move_id.date.strftime('%m')) + '-' + str(mv_line.move_id.date.strftime('%d')),

                        payslip = self.env['hr.payslip'].search([('move_id', '=', mv_line.move_id.id)], limit=1)
                        batchid = payslip.payslip_run_id.id
                        ref4 = str(payslip.payslip_run_id.id)+' ' +str(payslip.payslip_run_id.name),                        
                        ref5 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label)+' '+ str(payslip.payslip_run_id.id)+' ' +str(payslip.payslip_run_id.name),
                        
                        batch_name = payslip.payslip_run_id.name
                        ref6 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label)+' '+str(mv_line.move_id.journal_id.name),
                        ref10 = 'Odoo' + ' ' + str(mv_line.move_id.journal_id.ora_ledger_label) + ' ' + str(
                                payslip.payslip_run_id.id) + ' ' + str(payslip.payslip_run_id.name) ,
                        ref21 = str(mv_line.move_id.company_id.ledger_id) + '-' + str(mv_line.move_id.id) + '-' + str(
                                mv_line.id),
                        group = str(mv_line.move_id.company_id.ledger_id) + str(
                                fields.datetime.now().strftime('%Y%m%d')) + str(
                                payslip.payslip_run_id.id)
                        period = mv_line.date.strftime('%b-%Y')
                        inv_date = mv_line.date.strftime('%d-%b-%Y')
                        debit_total += mv_line.debit
                        debit_mv_account_code = mv_line.ora_account_code

                if debit_total > 0:
                    total_serial_no += 1  
                    final_gl_account_list.append({
                        'total_serial_no': total_serial_no,
                        'inv_name': inv_name,
                        'ledger_id': ledger_id,
                        'currency_code': currency_code,
                        'jv_category': jv_category,
                        'segment1': segment1,
                        'segment2': segment2,
                        'segment3': segment3,
                        'segment4': segment4,
                        'ref1': ref1,
                        'ref2': ref2,
                        'ref4': ref4,
                        'ref5': ref5,
                        'ref6': ref6,
                        'ref10': str(batchid) + ' '+ str(batch_name) +' ' + str(total_serial_no) ,
                        'ref21': str(ledgerna) + '-' + str(batchid) + '-' + str(total_serial_no),
                        'group': group,
                        'period': period,
                        'inv_date': inv_date,
                        'account_code': debit_mv_account_code,
                        'account': self.env['account.account'].search([('id', '=', credit_account)], limit=1).name,
                        'debit': debit_total,
                        'credit': 0,
                    })
        for inv in final_gl_account_list:
                #for line in inv:
                #    raise UserError(str(line['inv_name'])+' '+str(line['currency_code'])+' '+str(line['debit']) )
            inv_name = inv['inv_name']
            for inv_n in inv['inv_name']:
                inv_name = inv_n
            ledger = inv['ledger_id']
            for ledid in inv['ledger_id']:
                ledger = ledid
            ledger_id = int(ledger)
            currency_code = inv['currency_code']
            for curr in  inv['currency_code']:
                currency_code = curr
            date_created = fields.date.today().strftime('%d-%b-%Y')
            created_by = -1
            flag = 'A'
            jv_category = inv['jv_category']
            for jv_categ in inv['jv_category']:
                jv_category = jv_categ
            #company code
            segment1 = inv['segment1']
            for seg1 in inv['segment1']:
                segment1 = seg1
            #cost center
            segment2 = inv['segment2']
            for seg2 in inv['segment2']:
                segment2 = seg2
            #control-account
            segment3 = inv['segment3']
            for seg3 in inv['segment3']:
                segment3 = seg3
            #sub account
            segment4 = inv['segment4']
            for seg4 in inv['segment4']:
                segment4 = seg4
            segment5 =  '00'
            segment6 =  '00'
            entered_dr = int(inv['debit'])
            entered_cr = int(inv['credit'])
            accounting_dr = int(inv['debit'])
            accountng_cr = int(inv['credit'])
            ref1 = inv['ref1']
            for re1 in inv['ref1']:
                ref1 =re1
            reference1 = ref1
            ref2 = inv['ref2']
            for re2 in inv['ref2']:
                ref2 =re2
            reference2 = ref2
            ref4 = inv['ref4']
            for re4 in inv['ref4']:
                ref4 =re4
            reference4 = ref4
            ref5 = inv['ref5']
            for re5 in inv['ref5']:
                ref5 =re5
            reference5 = ref5
            reference6 = inv['ref6']
            for re6 in inv['ref6']:
                reference6 =re6
            ref10 = inv['ref10']
            #for re10 in inv['ref10']:
            #    ref10 =re10
            reference10 = ref10
            ref21 = inv['ref21']
            #for re21 in inv['ref21']:
            #    ref21 =re21
            reference21=ref21
            group_uniq_ref = inv['group']
            #for gp in inv['group']:
            #    group_uniq_ref = gp
            group_id = int(group_uniq_ref)
            period_name = inv['period']
            #for pd in inv['period']:
            #    period_name = pd
            inv_date = inv['inv_date']
            #for indate in inv['inv_date']:
            #    inv_date = indate
            conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
            cur = conn.cursor()
            statement = 'insert into XX_ODOO_GL_INTERFACE(STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR,REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10,REFERENCE21, GROUP_ID, PERIOD_NAME) values(: 2,:3,: 4,:5,: 6,:7,: 8,:9,: 10,:11,: 12,:13,: 14,:15,: 16,:17,: 18,:19,: 20,:21,: 22,:23,: 24,:25,:26,:27,:28,:29)'
            cur.execute(statement,('NEW', ledger_id, inv_date, currency_code, date_created, created_by, flag,  jv_category, 'Odoo',segment1, segment2, segment3, segment4, segment5,segment6, entered_cr, entered_dr, accountng_cr, accounting_dr, reference1, reference2, reference4, reference5, reference6, reference10,reference21, group_id, period_name))
            conn.commit()
        #jv.move_id.is_posted = True



  
    def action_posted_on_oracle(self):
        for jv in self:
            if jv.is_posted == False and inv.move_id.journal_id.ora_ledger_label!='Payroll':
                expense_sub_category_name = ' '
                for inv in self.line_ids:
                    if inv.product_id:
                        expense_sub_category_name = inv.product_id.sub_category_id.name
                    inv_name = inv.name
                    ledger_id = int(inv.move_id.company_id.ledger_id)
                    currency_code = inv.company_id.currency_id.name
                    date_created = fields.date.today().strftime('%d-%b-%Y')
                    created_by = -1
                    flag = 'A'
                    jv_category = 'Odoo '+ str(inv.move_id.journal_id.ora_ledger_label)
                    #company code
                    segment1 = inv.move_id.company_id.segment1
                    #cost center
                    segment2 = inv.analytic_account_id.code if inv.analytic_account_id else '000'
                    code_spliting = inv.account_id.code.split('.')
                    #control-account
                    segment3 = code_spliting[0]
                    #sub account
                    segment4 = code_spliting[1]
                    segment5 =  '00'
                    segment6 =  '00'
                    entered_dr = int(inv.debit)
                    entered_cr = int(inv.credit)
                    accounting_dr = int(inv.debit)
                    accountng_cr = int(inv.credit)
                    ref1 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)+ ' '+str(inv.move_id.company_id.ledger_id)+'-'+str(inv.move_id.date.strftime('%Y'))+'-'+str(inv.move_id.date.strftime('%m'))+'-'+str(inv.move_id.date.strftime('%d'))  
                    reference1 = ref1
                    ref2 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)+ ' '+str(inv.move_id.company_id.ledger_id)+'-'+str(inv.move_id.date.strftime('%Y'))+'-'+str(inv.move_id.date.strftime('%m'))+'-'+str(inv.move_id.date.strftime('%d'))  
                    reference2 = ref2
                    ref4 = str(inv.move_id.id)+ ' ' +str(inv.move_id.expense_id.name if inv.move_id.expense_id else inv.move_id.name) 
                    if inv.move_id.journal_id.ora_ledger_label=='Payroll':
                        ref4 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)+ ' '+str(inv.move_id.id)+ ' ' +str(inv.move_id.name)
                    reference4 = ref4
                    ref5 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)+ ' '+str(inv.move_id.id)+ ' ' +str(inv.move_id.expense_id.name if inv.move_id.expense_id else inv.move_id.name) 
                    reference5 = ref5
                    reference6 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)  +' '+ str(expense_sub_category_name)
                    if inv.move_id.journal_id.ora_ledger_label=='Payroll':
                        reference6 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)  +' '+ str(inv.move_id.journal_id.name)    
                    emp_office_id = 0
                    employee_office_id = self.env['hr.employee'].search([('address_home_id','=', inv.partner_id.id)], limit=1)
                    
                    ref10 = str(employee_office_id.name) + ' [' + str(employee_office_id.emp_number) +'] '+str(expense_sub_category_name)+' '+str(inv.move_id.expense_id.name if inv.move_id.expense_id else inv.move_id.name)
                    if inv.move_id.journal_id.type=='bank':
                        ref10 = str(employee_office_id.name) + ' [' + str(employee_office_id.emp_number) +'] '+str(inv.move_id.journal_id.bank_id.name)+' '+str(inv.move_id.journal_id.bank_account_id.acc_number)    
                    if inv.move_id.journal_id.ora_ledger_label=='Payroll':
                        payslip = self.env['hr.payslip'].search([('move_id', '=' , inv.move_id.id)], limit=1)
                        ref10 = 'Odoo' +  ' ' +  str(inv.move_id.journal_id.ora_ledger_label)  +' '+str(payslip.payslip_run_id.id)+' '+str(payslip.payslip_run_id.name)+' '+str(payslip.id)+' '+str(payslip.name)         
                    reference10 = ref10
                    ref21= str(inv.move_id.company_id.ledger_id)+'-'+str(inv.move_id.id)+'-'+str(inv.id)
                    reference21=ref21
                    group_uniq_ref = str(inv.move_id.company_id.ledger_id)+str(fields.datetime.now().strftime('%Y%m%d'))+str(inv.move_id.id)
                    group_id = int(group_uniq_ref)
                    period_name = inv.date.strftime('%b-%y')
                    context = inv.analytic_account_id.name if inv.analytic_account_id.name else 'NULL'
                    attribute1 = inv.analytic_account_id.code if inv.analytic_account_id.code else 'NULL'
                    inv_date = inv.date.strftime('%d-%b-%Y')
                    conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//192.168.65.152:1523/test2')
                    cur = conn.cursor()
                    statement = 'insert into XX_ODOO_GL_INTERFACE(STATUS,LEDGER_ID, ACCOUNTING_DATE, CURRENCY_CODE,DATE_CREATED,CREATED_BY,ACTUAL_FLAG,USER_JE_CATEGORY_NAME,USER_JE_SOURCE_NAME, SEGMENT1, SEGMENT2, SEGMENT3, SEGMENT4, SEGMENT5, SEGMENT6, ENTERED_CR, ENTERED_DR, ACCOUNTED_CR, ACCOUNTED_DR,REFERENCE1, REFERENCE2, REFERENCE4, REFERENCE5, REFERENCE6, REFERENCE10,REFERENCE21, GROUP_ID, PERIOD_NAME) values(: 2,:3,: 4,:5,: 6,:7,: 8,:9,: 10,:11,: 12,:13,: 14,:15,: 16,:17,: 18,:19,: 20,:21,: 22,:23,: 24,:25,:26,:27,:28,:29)'
                    cur.execute(statement,('NEW', ledger_id, inv_date, currency_code, date_created, created_by, flag,  jv_category, 'Odoo',segment1, segment2, segment3, segment4, segment5,segment6, entered_cr, entered_dr, accountng_cr, accounting_dr, reference1, reference2, reference4, reference5, reference6, reference10,reference21, group_id, period_name))
                    conn.commit()
                jv.is_posted = True



















