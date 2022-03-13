from odoo import api, fields, models, _
from calendar import monthrange

from odoo.exceptions import UserError
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


class HrOvertimeApproval(models.Model):
    _name = 'hr.overtime.approval'
    _description = 'Overtime Approval'
    _rec_name = 'incharge_id'

   
    incharge_id = fields.Many2one('hr.employee', string='Overtime Incharge')  
    approval_request_id = fields.Many2one('approval.request', string="Approval")
    category_id = fields.Many2one('approval.category', string='Approval Category')
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'To Approve'), ('approved', 'Approved'),('refused', 'Refused')], string='Status', default='draft')    
    overtime_line_ids = fields.One2many('hr.overtime.approval.line', 'site_ot_id', string="Overtime Lines")
    
    work_location_id = fields.Many2one('hr.work.location', string="Work Location", compute='_compute_employee_location')
    workf_location_id = fields.Many2one('hr.work.location', string="Work Location")

    @api.depends('incharge_id')
    def _compute_employee_location(self):
        for line in self:
            line.update({
               'work_location_id': line.incharge_id.work_location_id.id,
               'workf_location_id': line.incharge_id.work_location_id.id,
                })
    
    
    @api.constrains('employee_id')
    def _check_incharge(self):
        for line in self:
            if line.incharge_id.user_id.id != self.env.uid:                   
                raise UserError('Only Employee Site Incharge can Approve Overtime!')

                    
    @api.model
    def create(self, vals):
        sheet = super(HrOvertimeApproval, self.with_context(mail_create_nosubscribe=True, mail_auto_subscribe_no_notify=True)).create(vals)
        
        return sheet
    
    
    def _action_send_overtime_for_approval(self):
        employee_list=self.env['hr.employee'].sudo().search([('company_id','=', 5)])
        subordinates_overtime_list=[]
        for employee in employee_list:
            normal_overtime_total = 0
            rest_overtime_total = 0
            gazetted_overtime_total=0
            evertime_type_list = []
            overtime_reconcile=self.env['hr.overtime.request'].sudo().search([('employee_id','=',employee.id),('date','>=','2022-01-16'),('date','<=','2022-02-16'),('state','=','to_approve')])
            for ovt in overtime_reconcile:
                evertime_type_list.append(ovt.overtime_type_id.id) 
            uniq_overtime_type_list = set(evertime_type_list) 
            for uniq_ovt in uniq_overtime_type_list:
                total_ot_hours = 0
                overtime_entry_list=self.env['hr.overtime.request'].sudo().search([('employee_id','=',employee.id),('date','>=','2022-01-16'),('date','<=','2022-02-16'),('overtime_type_id','=',uniq_ovt),('state','=','to_approve')])  
                for ot in overtime_entry_list:
                    if ot.overtime_type_id.type=='normal':
                        normal_overtime_total += ot.overtime_hours
                    if ot.overtime_type_id.type=='rest_day':
                        rest_overtime_total += ot.overtime_hours
                    if ot.overtime_type_id.type=='gazetted':
                        gazetted_overtime_total += ot.overtime_hours
                    ot.update({
                          'state':  'approved',
                    }) 
            if  normal_overtime_total > 0 or rest_overtime_total > 0 or gazetted_overtime_total > 0:    
                subordinates_overtime_list.append({
                  'employee':  employee.id,
                  'normal_overtime': normal_overtime_total,
                  'rest_day_overtime': rest_overtime_total,
                  'gazetted_overtime': gazetted_overtime_total,
                })        
        overtime_vals={
            'incharge_id': 3630,
            'date_from': '2022-01-16',
            'date_to': '2022-02-15',
            'state': 'draft',
        }  
        ot_approval=self.env['hr.overtime.approval'].sudo().create(overtime_vals)
        for line in subordinates_overtime_list:
            line_vals = {
                'employee_id': line['employee'],
                'site_ot_id':  ot_approval.id,
                'normal_ot':  line['normal_overtime'],
                'rest_day_ot': line['rest_day_overtime'],
                'gazetted_ot':  line['gazetted_overtime'],
            }
            overtime_line=self.env['hr.overtime.approval.line'].create(line_vals)


    def action_create_approval_request_site_attendance(self):
        approver_ids  = []       
        request_list = []
        for line in self:
            approval_categ=self.env['approval.category'].search([('name','=','Overtime'),('company_id','=', line.incharge_id.company_id.id)], limit=1)
            if not approval_categ:
                category = {
                    'name': 'Overtime',
                    'company_id': line.incharge_id.company_id.id,
                    'is_parent_approver': False,
                }
                approval_categ = self.env['approval.category'].sudo().create(category)
            line.category_id=approval_categ.id  
            if approval_categ:
                request_list.append({
                        'name': 'Overtime Approval' + ' Date From ' + str(line.date_from.strftime('%d-%b-%Y'))+' '+' Date To '+str(line.date_to.strftime('%d-%b-%Y')),
                        'request_owner_id': line.incharge_id.user_id.id,
                        'category_id': approval_categ.id,
                        'site_ot_id': line.id,
                        'reason': 'Overtime Approval' + ' Date From ' + str(line.date_from.strftime('%d-%b-%Y'))+' '+' Date To '+str(line.date_to.strftime('%d-%b-%Y')),
                        'request_status': 'new',
                })
                approval_request_id = self.env['approval.request'].sudo().create(request_list)
                vals ={
                    'user_id': line.incharge_id.user_id.id,
                    'request_id': approval_request_id.id,
                    'status': 'new',
                }
                approvers=self.env['approval.approver'].sudo().create(vals)
                approval_request_id._onchange_category_id()
                approval_request_id.action_confirm()
                line.approval_request_id = approval_request_id.id
                
            
    def unlink(self):
        for line in self:
            if line.state in ('submitted','approved'):
                raise UserError('Not Allow to delete  Document!')
        return super(HrOvertimeApproval, self).unlink()
    
    
    def action_approve(self):
        self.state = 'approved'  

    def action_submit(self):
        self.action_create_approval_request_site_attendance()
        self.state = 'submitted'       
            
    def action_refuse(self):
        self.state = 'refused'
                
    def action_reset(self):
        self.state = 'draft'


    def generate_normal_overtime_compansation(self):
        """
         Generate Overtime Entries 
         1- By Normal Overtime type
        """
        for line in self.overtime_line_ids:
            ot_amount = 0.0
            nrate = 0
            overtime_type=self.env['hr.overtime.type'].search([('company_id','=',self.incharge_id.company_id.id),('type','=','normal')], limit=1) 
            for compansation in overtime_type.type_line_ids:
                if line.normal_ot >= compansation.ot_hours:
                    if compansation.compansation == 'payroll':
                        if compansation.rate_type == 'fix_amount':
                            ot_amount = compansation.rate * line.normal_ot 
                        elif compansation.rate_type == 'percent':
                            contract = self.env['hr.contract'].search([('employee_id','=',line.employee_id.id),('state','=','open')], limit=1)   
                            ot_hour_amount = (((contract.wage/100) * compansation.percent_salary) * compansation.rate_percent ) /(compansation.hours_per_day * compansation.month_day)
                            nrate = compansation.rate_percent
                            ot_amount = ot_hour_amount * line.normal_ot
            total_amount = ot_amount
            if  line.overtime_type_id.type == 'normal': 
                if total_amount > 0:
                    entry_vals = {
                            'employee_id': line.employee_id.id,
                            'date': line.date,
                            'amount': total_amount ,
                            'company_id':  line.company_id.id,
                            'overtime_hours': line.normal_ot,
                            'overtime_type_id': line.overtime_type.id,
                            'remarks': '@rate '+ str(nrate)
                    }
                    overtime_entry = self.env['hr.overtime.entry'].create(entry_vals)
                


                
    def generate_overtime_compansation_rest_day(self):
        """
         Generate Overtime Entries 
         1- By Using Overtime type
         2- Rest Day
        """
        for line in self.overtime_line_ids:
            if line.employee_id:
                single_ot_amount = 0
                double_ot_amount = 0
                single_hour_limit = 0
                double_rate_ot_hours = 0
                single_ot_hour_amount = 0
                double_ot_hour_amount = 0
                grate2 = ' '
                grate = ' '
                overtime_type=self.env['hr.overtime.type'].search([('company_id','=',self.incharge_id.company_id.id),('type','=','rest_day')], limit=1) 
                double_rate_line=self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.rest_day_ot),('entry_type_id','=','double'),('rate_type','=','percent')], order='ot_hours desc', limit=1)
                single_rate_line=self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.rest_day_ot),('entry_type_id','=','single'),('rate_type','=','percent')], order='ot_hours desc', limit=1)    
                contract = self.env['hr.contract'].search([('employee_id','=',line.employee_id.id),('state','=','open')], limit=1)
                single_fixed_amount =self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.rest_day_ot),('entry_type_id','=','single'),('rate_type','=','fix_amount')], order='ot_hours desc', limit=1)
                double_fixed_amount =self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.rest_day_ot),('entry_type_id','=','double'),('rate_type','=','fix_amount')], order='ot_hours desc', limit=1)
                if double_rate_line and single_rate_line:
                    single_hour_limit =  single_rate_line.ot_hours
                    double_rate_ot_hours = line.rest_day_ot - single_rate_line.ot_hours
                    double_ot_hour_amount = (((contract.wage/100) * double_rate_line.percent_salary) * double_rate_line.rate_percent ) /(double_rate_line.hours_per_day * double_rate_line.month_day)
                    single_ot_hour_amount = (((contract.wage/100) * double_rate_line.percent_salary) * single_rate_line.rate_percent ) /(single_rate_line.hours_per_day * single_rate_line.month_day)
                    grate2 = double_rate_line.rate_percent
                    grate  = single_rate_line.rate_percent
                elif  single_rate_line:
                    single_hour_limit =  line.rest_day_ot
                    single_ot_hour_amount = (((contract.wage/100) * double_rate_line.percent_salary) * single_rate_line.rate_percent ) /(single_rate_line.hours_per_day * single_rate_line.month_day)
                    grate  = single_rate_line.rate_percent
                else:
                    if single_fixed_amount and double_fixed_amount:
                        single_hour_limit =  single_fixed_amount.ot_hours
                        double_rate_ot_hours = line.rest_day_ot - single_fixed_amount.ot_hours 
                        single_ot_hour_amount = single_fixed_amount.rate
                        double_ot_hour_amount = double_fixed_amount.rate
                    elif single_fixed_amount:
                        single_hour_limit =  line.rest_day_ot 
                        single_ot_hour_amount = single_fixed_amount.rate                    

                single_ot_amount =  single_ot_hour_amount * single_hour_limit
                double_ot_amount =  double_ot_hour_amount * double_rate_ot_hours
                if single_ot_amount > 0:
                    if line.employee_id:
                        entry_vals = {
                                'employee_id': line.employee_id.id,
                                'date': '2022-02-02',
                                'amount': round(single_ot_amount) ,
                                'company_id':  line.employee_id.company_id.id,
                                'overtime_hours': single_hour_limit,
                                'overtime_type_id': overtime_type.id,
                                'remarks': '@rate '+str(grate)                                    
                                              }
                        overtime_entry_single = self.env['hr.overtime.entry'].create(entry_vals)
                if double_ot_amount > 0:
                    if line.employee_id:
                        entry_vals = {
                                'employee_id': line.employee_id.id,
                                'date': '2022-02-02',
                                'amount': round(double_ot_amount) ,
                                'company_id':  line.employee_id.company_id.id,
                                'overtime_hours': double_rate_ot_hours,
                                'overtime_type_id': overtime_type.id,
                                'remarks': '@rate '+str(grate2) ,
                                                }
                        overtime_entry_double = self.env['hr.overtime.entry'].create(entry_vals)


    def generate_overtime_compansation_gazetted(self):
        """
         Generate Overtime Entries 
         1- By Using Overtime type
         2- Rest Day
        """
        for line in self.overtime_line_ids:
            if line.employee_id:
                single_ot_amount = 0
                double_ot_amount = 0
                single_hour_limit = 0
                double_rate_ot_hours = 0
                single_ot_hour_amount = 0
                double_ot_hour_amount = 0
                grate2 = ' '
                grate = ' '
                overtime_type=self.env['hr.overtime.type'].search([('company_id','=',self.incharge_id.company_id.id),('type','=','gazetted')], limit=1) 
                double_rate_line=self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.gazetted_ot),('entry_type_id','=','double'),('rate_type','=','percent')], order='ot_hours desc', limit=1)
                single_rate_line=self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.gazetted_ot),('entry_type_id','=','single'),('rate_type','=','percent')], order='ot_hours desc', limit=1)    
                contract = self.env['hr.contract'].search([('employee_id','=',line.employee_id.id),('state','=','open')], limit=1)
                single_fixed_amount =self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.gazetted_ot),('entry_type_id','=','single'),('rate_type','=','fix_amount')], order='ot_hours desc', limit=1)
                double_fixed_amount =self.env['hr.overtime.type.line'].search([('overtime_type_id','=',overtime_type.id),('compansation','=', 'payroll'),('ot_hours','<=', line.gazetted_ot),('entry_type_id','=','double'),('rate_type','=','fix_amount')], order='ot_hours desc', limit=1)
                if double_rate_line and single_rate_line:
                    single_hour_limit =  single_rate_line.ot_hours
                    double_rate_ot_hours = line.gazetted_ot - single_rate_line.ot_hours
                    double_ot_hour_amount = (((contract.wage/100) * double_rate_line.percent_salary) * double_rate_line.rate_percent ) /(double_rate_line.hours_per_day * double_rate_line.month_day)
                    single_ot_hour_amount = (((contract.wage/100) * double_rate_line.percent_salary) * single_rate_line.rate_percent ) /(single_rate_line.hours_per_day * single_rate_line.month_day)
                    grate2 = double_rate_line.rate_percent
                    grate  = single_rate_line.rate_percent
                elif  single_rate_line:
                    single_hour_limit =  line.gazetted_ot
                    single_ot_hour_amount = (((contract.wage/100) * double_rate_line.percent_salary) * single_rate_line.rate_percent ) /(single_rate_line.hours_per_day * single_rate_line.month_day)
                    grate  = single_rate_line.rate_percent
                else:
                    if single_fixed_amount and double_fixed_amount:
                        single_hour_limit =  single_fixed_amount.ot_hours
                        double_rate_ot_hours = line.gazetted_ot - single_fixed_amount.ot_hours 
                        single_ot_hour_amount = single_fixed_amount.rate
                        double_ot_hour_amount = double_fixed_amount.rate
                    elif single_fixed_amount:
                        single_hour_limit =  line.gazetted_ot
                        single_ot_hour_amount = single_fixed_amount.rate                    

                single_ot_amount =  single_ot_hour_amount * single_hour_limit
                double_ot_amount =  double_ot_hour_amount * double_rate_ot_hours
                if single_ot_amount > 0:
                    if line.employee_id:
                        entry_vals = {
                                'employee_id': line.employee_id.id,
                                'date': '2022-02-02',
                                'amount': round(single_ot_amount) ,
                                'company_id':  line.employee_id.company_id.id,
                                'overtime_hours': single_hour_limit,
                                'overtime_type_id': overtime_type.id,
                                'remarks': '@rate '+str(grate)                                    
                                              }
                        overtime_entry_single = self.env['hr.overtime.entry'].create(entry_vals)
                if double_ot_amount > 0:
                    if line.employee_id:
                        entry_vals = {
                                'employee_id': line.employee_id.id,
                                'date': '2022-02-02',
                                'amount': round(double_ot_amount) ,
                                'company_id':  line.employee_id.company_id.id,
                                'overtime_hours': double_rate_ot_hours,
                                'overtime_type_id': overtime_type.id,
                                'remarks': '@rate '+str(grate2) ,
                                                }
                        overtime_entry_double = self.env['hr.overtime.entry'].create(entry_vals)






    def action_approve_line(self):
        for line in self.overtime_line_ids:
            if line.state == 'to_approve' and line.employee_id:
                ot_amount = 0
                gazetted_hours = 0
                nrate = 0
                leave_period = ' '
                leave_type = 0
                if line.normal_ot > 0:
                    line.generate_normal_overtime_compansation()    
                if line.rest_day_ot > 0:
                    line.generate_overtime_compansation_rest_day()                                    
                if  line.gazetted_ot > 0:
                    line.generate_overtime_compansation_gazetted() 
                
                      
        
   
class HrOvertimeLine(models.Model):
    _name = 'hr.overtime.approval.line'
    _description = 'Overtime Line'
    _rec_name = 'employee_id'

    site_ot_id = fields.Many2one('hr.overtime.approval', string='Site OT')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=False)
    normal_ot = fields.Float(string='Normal OT')
    rest_day_ot = fields.Float(string="Rest Day OT")
    gazetted_ot = fields.Float(string="Gazetted OT")
    work_location_id = fields.Many2one('hr.work.location', string="Work Location", compute='_compute_employee_location')
    workf_location_id = fields.Many2one('hr.work.location', string="Work Location")
    remarks = fields.Char(string='Remarks')
    @api.depends('employee_id')
    def _compute_employee_location(self):
        for line in self:
            line.update({
               'work_location_id': line.employee_id.work_location_id.id,
               'workf_location_id': line.employee_id.work_location_id.id,
                })
    
    
    def unlink(self):
        for line in self:
            if line.state != 'draft':
                raise UserError('A record in Submitted or Approved state can`t be deleted!')
        return super(HrOvertimeLine, self).unlink()


    
    
    