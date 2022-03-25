# -*- coding: utf-8 -*-
# from odoo import http


# class DeCustomModule(http.Controller):
#     @http.route('/de_custom_module/de_custom_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_custom_module/de_custom_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_custom_module.listing', {
#             'root': '/de_custom_module/de_custom_module',
#             'objects': http.request.env['de_custom_module.de_custom_module'].search([]),
#         })

#     @http.route('/de_custom_module/de_custom_module/objects/<model("de_custom_module.de_custom_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_custom_module.object', {
#             'object': obj
#         })
