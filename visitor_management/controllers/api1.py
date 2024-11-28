# visitor_management/controllers/main.py
from odoo import http
from odoo.http import request

class VisitorManagementController(http.Controller):
    @http.route('/visitor/create', type='json', auth='user')
    def create_visitor(self, **kwargs):
        # Logic to create a visitor record
        visitor = request.env['visitor.management'].create({
            'name': kwargs.get('name'),
            'email': kwargs.get('email')
        })
        return {'status': 'success', 'visitor_id': visitor.id}
