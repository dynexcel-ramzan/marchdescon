# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountPayment(http.Controller):
#     @http.route('/de_account_payment/de_account_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_payment/de_account_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_payment.listing', {
#             'root': '/de_account_payment/de_account_payment',
#             'objects': http.request.env['de_account_payment.de_account_payment'].search([]),
#         })

#     @http.route('/de_account_payment/de_account_payment/objects/<model("de_account_payment.de_account_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_payment.object', {
#             'object': obj
#         })
