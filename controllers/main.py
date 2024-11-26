from odoo import http
from odoo.http import request

class VisitorRegistration(http.Controller):
    @http.route('/visitor/register', type='http', auth='public', website=True)
    def register_visitor(self, station_id=None, **kwargs):
        station = request.env['visitor.station'].sudo().browse(int(station_id)) if station_id else None
        return request.render('visitor_management.visitor_registration_form', {
            'station': station,
        })

    @http.route('/visitor/register/submit', type='http', auth='public', website=True, csrf=True)
    def submit_visitor_registration(self, **post):
        visitor_data = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'station_id': int(post.get('station_id')),
        }
        request.env['visitor.record'].sudo().create(visitor_data)
        return request.render('visitor_management.registration_success')
