# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import OrderedDict
from operator import itemgetter
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR
import ast

def overtime_approval_lines_content(): 
    overtime = request.env['hr.overtime.approval'].sudo().search([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
    return {
        'overtime': overtime,
    }


class CreateAttendance(http.Controller):

    @http.route('/overtime/approval/line/save',type="http", website=True, auth='user')
    def action_approve_overtime_template(self, **kw):
        count = 0
        record_id = 0
        if kw.get('line_overtime_vals'):
            line_ovt_vals_list = ast.literal_eval(kw.get('line_overtime_vals'))
        for siteworker in line_ovt_vals_list:
            count += 1
            if count > 1:
                overtime_line=request.env['hr.overtime.approval.line'].sudo().search([('id','=', int(siteworker['col6']) )])
                record_id =  overtime_line.site_ot_id.id
                overtime_line.update({
                        'normal_ot': float(siteworker['col2']) if siteworker['col2'] != '' else 0,
                        'rest_day_ot': float(siteworker['col3']) if siteworker['col3'] != '' else 0,
                        'gazetted_ot':  float(siteworker['col4']) if siteworker['col4'] != '' else 0,
                        'remarks': siteworker['col5'],
                        })
        overtime_approval=request.env['hr.overtime.approval'].sudo().search([('id','=',record_id)]) 
        overtime_approval.action_approve()
        return request.render("de_portal_overtime.overtime_approve_submited", {})
      
class CustomerPortal(CustomerPortal):


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'overtime_count' in counters:
            values['overtime_count'] = request.env['hr.overtime.approval'].sudo().search_count([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
        return values
  
    def _overtime_get_page_view_values(self,overtime, access_token = None, **kwargs):
        
        exist_employee=request.env['hr.employee'].sudo().search([('user_id','=',http.request.env.context.get('uid'))])
        values = {
            'page_name' : 'Overtime',
            'overtime' : overtime,
            'date_from': overtime.date_from,
            'date_to': overtime.date_to,
        }
        return self._get_page_view_values(overtime, access_token, values, 'my_overtime_history', False, **kwargs)

    @http.route(['/overtime/approvals', '/overtime/approvals/page/<int:page>'], type='http', auth="user", website=True)
    def portal_overtime_approvals(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                         search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'id': {'label': _('Default'), 'order': 'id asc'},
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'incharge_id desc' },
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }                                       
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state','=','submitted')]},
        }  
        searchbar_inputs = {
            'id': {'input': 'id', 'label': _('Search in No#')},
            'incharge_id.name': {'input': 'incharge_id.name', 'label': _('Search in Incharge')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }
        project_groups = request.env['hr.overtime.approval'].sudo().search([('incharge_id.user_id','=',http.request.env.context.get('uid'))])
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
#         domain = []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]       
        # search
        if search and search_in:
            search_domain = []
            if search_in in ('id', 'ID'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('incharge_id.name', 'Incharge'):
                search_domain = OR([search_domain, [('incharge_id.name', 'ilike', search)]])
            domain += search_domain
            
        domain += [('incharge_id.user_id', '=',http.request.env.context.get('uid'))]
        ot_amount_count = request.env['hr.overtime.approval'].sudo().search_count(domain)
        pager = portal_pager(
            url="/overtime/approvals",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'search_in': search_in, 'search': search},
            total=ot_amount_count,
            page=page,
            step=self._items_per_page
        )
        _overtimes = request.env['hr.overtime.approval'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_overtime_history'] = _overtimes.ids[:100]
        grouped_overtime = [_overtimes]              
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_overtime': grouped_overtime,
            'page_name': 'overtime',
            'default_url': '/overtime/approvals',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        })
        return request.render("de_portal_overtime.portal_hr_overtime_req", values)   


    @http.route(['/overtime/approval/<int:overtime_id>'], type='http', auth="user", website=True)
    def portal_overtime_request_approval(self, overtime_id, access_token=None, **kw):
        values = []
        id = overtime_id
        try:
            overtime_sudo = request.env['hr.overtime.approval'].sudo().search([('id','=',overtime_id)], limit=1)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._overtime_get_page_view_values(overtime_sudo, access_token, **kw) 
        return request.render("de_portal_overtime.portal_overtime_lines", values)


    