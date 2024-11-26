from odoo import http
from odoo.http import request

class VisitorController(http.Controller):

    @http.route('/visitor/register', type='http', auth='public', website=True)
    def visitor_register_form(self, **kwargs):
        station_id = kwargs.get('station_id')
        if not station_id:
            return request.render('visitor_management.error_page', {
                'error_message': 'No station ID provided.'
            })

        station = request.env['visitor.station'].sudo().browse(int(station_id))
        if not station.exists():
            return request.render('visitor_management.error_page', {
                'error_message': 'Invalid station ID.'
            })

        employees = request.env['hr.employee'].sudo().search([])
        return request.render('visitor_management.visitor_register_template', {
            'station': station,
            'employees': employees,
        })

    @http.route('/visitor/submit', type='http', auth='public', website=True, methods=['POST'])
    def visitor_submit(self, **post):
        visitor_vals = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'station_id': int(post.get('station_id')),
            'purpose': post.get('purpose'),
            'host': int(post.get('host')),
            'aadhar_id': post.get('aadhar_id'),
            'place': post.get('place'),
        }
        visitor = request.env['visitor.record'].sudo().create(visitor_vals)
        visitor.send_visitor_notification()
        return request.render('visitor_management.thank_you_page', {
            'visitor': visitor,
        })