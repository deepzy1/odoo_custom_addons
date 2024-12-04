from odoo import http
from odoo.http import request


class VisitorController(http.Controller):

    @http.route('/visitor/list', type='http', auth='public', website=True)
    def visitor_list(self):
        """Fetch visitor records and render the template."""
        # Fetch visitor records
        visitors = request.env['visitor.record'].sudo().search([], order='visit_date desc', limit=10)
        # Render the template and pass visitor data
        return request.render('visitor_management.visitor_list_template', {
            'visitors': visitors
        })
