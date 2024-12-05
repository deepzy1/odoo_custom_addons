from odoo import http

class SlideshowPage(http.Controller):
    @http.route('/custom_slideshow', type='http', auth='public', website=True)
    def custom_slideshow(self):
        return http.request.render('visitor_management.custom_slideshow_template', {})
