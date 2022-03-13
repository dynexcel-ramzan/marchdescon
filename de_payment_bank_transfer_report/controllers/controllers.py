# -*- coding: utf-8 -*-
# from odoo import http


# class DePaymentBankTransferReport(http.Controller):
#     @http.route('/de_payment_bank_transfer_report/de_payment_bank_transfer_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payment_bank_transfer_report/de_payment_bank_transfer_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payment_bank_transfer_report.listing', {
#             'root': '/de_payment_bank_transfer_report/de_payment_bank_transfer_report',
#             'objects': http.request.env['de_payment_bank_transfer_report.de_payment_bank_transfer_report'].search([]),
#         })

#     @http.route('/de_payment_bank_transfer_report/de_payment_bank_transfer_report/objects/<model("de_payment_bank_transfer_report.de_payment_bank_transfer_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payment_bank_transfer_report.object', {
#             'object': obj
#         })
