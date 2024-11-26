from odoo import models, fields, api
from datetime import datetime

class VisitorTodayRecord(models.Model):
    _name = 'visitor.today.record'
    _description = 'Visitor Today Record'

    visitor_name = fields.Char(string="Visitor Name", related="visitor_id.visitor_name", store=True)
    visit_date = fields.Datetime(string="Visit Date", related="visitor_id.visit_date", store=True)
    visit_purpose = fields.Char(string="Visit Purpose")
    visitor_id = fields.Many2one('visitor.record', string="Visitor", required=True)

    @api.model
    def create(self, vals):
        # Automatically populate visit_date and visitor_name from the related visitor_id
        visitor = self.env['visitor.record'].browse(vals['visitor_id'])
        vals['visit_date'] = visitor.visit_date  # Get visit_date from visitor record
        vals['visitor_name'] = visitor.visitor_name  # Get visitor_name from visitor record
        return super(VisitorTodayRecord, self).create(vals)

    @api.depends('visitor_id')
    def _compute_visitor_today(self):
        today = datetime.now().date()
        for record in self:
            record.visitor_today_count = len(
                self.env['visitor.record'].search([
                    ('visit_date', '>=', f'{today} 00:00:00'),
                    ('visit_date', '<', f'{today} 23:59:59')
                ])
            )

    visitor_today_count = fields.Integer(string="Today's Visitor Count", compute="_compute_visitor_today")
