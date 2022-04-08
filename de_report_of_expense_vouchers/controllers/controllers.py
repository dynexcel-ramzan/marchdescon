# -*- coding: utf-8 -*-
# from odoo import http


# class DeReportOfExpenseVouchers(http.Controller):
#     @http.route('/de_report_of_expense_vouchers/de_report_of_expense_vouchers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_report_of_expense_vouchers/de_report_of_expense_vouchers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_report_of_expense_vouchers.listing', {
#             'root': '/de_report_of_expense_vouchers/de_report_of_expense_vouchers',
#             'objects': http.request.env['de_report_of_expense_vouchers.de_report_of_expense_vouchers'].search([]),
#         })

#     @http.route('/de_report_of_expense_vouchers/de_report_of_expense_vouchers/objects/<model("de_report_of_expense_vouchers.de_report_of_expense_vouchers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_report_of_expense_vouchers.object', {
#             'object': obj
#         })
