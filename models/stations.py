from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO
from datetime import datetime

class VisitorStation(models.Model):
    _name = 'visitor.station'
    _description = 'Visitor Station'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    security_name = fields.Many2one('hr.employee',string="Security Guard")
    name = fields.Char(string="Station Name", required=True)
    kiosk_url = fields.Char(string="Registration URL", readonly=True)
    qr_code = fields.Binary(string="QR Code", readonly=True)
    branches = fields.Selection(
        selection=[
            ('koramangala', 'Koramangala'),
            ('bommasandra', 'Bommasandra'),
        ],
        string="Branch Name"
    )
    location=fields.Char(string="Location")
    visitor_count = fields.Integer(string="Total Visitors", compute="_compute_visitor_count", store=True)
    visitor_count_today = fields.Integer(string="Today's Visitors", compute="_compute_visitor_count_today", store=False)
    visitor_ids = fields.One2many('visitor.record', 'station_id', string="Visitors")
    visitor_ids_today = fields.One2many('visitor.record', 'station_id', string="Today's Visitors",
                                        compute="_compute_visitor_ids_today")

    @api.depends('visitor_ids')
    def _compute_visitor_count(self):
        for station in self:
            station.visitor_count = len(station.visitor_ids)

    def _compute_visitor_count_today(self):
        today = datetime.now().date()
        for station in self:
            station.visitor_count_today = len(
                station.visitor_ids.filtered(lambda v: v.visit_date.date() == today)
            )

    def _compute_visitor_ids_today(self):
        today = datetime.now().date()
        for station in self:
            station.visitor_ids_today = station.visitor_ids.filtered(lambda v: v.visit_date.date() == today)




    @api.model
    def create(self, vals):
        record = super(VisitorStation, self).create(vals)
        record.kiosk_url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/visitor/register?station_id={record.id}"
        record._generate_qr_code()
        return record

    def write(self, vals):
        result = super(VisitorStation, self).write(vals)
        for station in self:
            if 'name' in vals:
                station.kiosk_url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/visitor/register?station_id={station.id}"
                station._generate_qr_code()
        return result

    def _generate_qr_code(self):
        for station in self:
            if station.kiosk_url:
                qr = qrcode.QRCode()
                qr.add_data(station.kiosk_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                station.qr_code = base64.b64encode(buffer.getvalue())
