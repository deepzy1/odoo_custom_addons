from odoo import models, fields, api
from email.message import EmailMessage
import smtplib
import os
from datetime import datetime, timedelta


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    user_id = fields.Many2one('res.users', string="Related User", required=True)


class VisitorRecord(models.Model):
    _name = 'visitor.record'
    _description = 'Visitor Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'host'

    name = fields.Char(string="Visitor Name", required=True)
    email = fields.Char(string="Email",required=True)
    phone = fields.Integer(string="Phone",max_digit=10)
    station_id = fields.Many2one('visitor.station', string="Station", required=True)
    visit_date = fields.Datetime(string="Visit Date", default=fields.Datetime.now)
    purpose = fields.Char(string="Purpose")
    host = fields.Many2one('hr.employee', string="To Meet", required=True)
    aadhar_id = fields.Char(string="Aadhar ID")
    place = fields.Char(string="Place")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('notified', 'Notified'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out')
    ], string="Status", default='draft', tracking=True)

    check_in_time = fields.Datetime(string="Check-In Time", readonly=True)
    check_out_time = fields.Datetime(string="Check-Out Time", readonly=True)

    @api.model
    def get_todays_visitors(self):
        """Return visitor records for today's date."""
        today = datetime.today().date()  # Get today's date
        return self.search([('visit_date', '>=', f'{today} 00:00:00'),
                            ('visit_date', '<=', f'{today} 23:59:59')])




    def action_approve(self):
        """Approve the visitor record."""
        for record in self:
            if record.state == 'notified':
                record.state = 'approved'

    def action_refuse(self):
        """Refuse the visitor record."""
        for record in self:
            if record.state == 'notified':
                record.state = 'refused'

    def action_check_in(self):
        """Set Check-In Time and notify host."""
        for record in self:
            if record.state == 'approved' and not record.check_in_time:
                record.check_in_time = datetime.now()
                record.state = 'checked_in'

    def action_check_out(self):
        """Set Check-Out Time."""
        for record in self:
            if record.state == 'checked_in' and not record.check_out_time:
                record.check_out_time = datetime.now()
                record.state = 'checked_out'

    def send_visitor_notification(self):
        """Send an email to the host when the visitor is approved or checked in."""

        # Log file path for notifications
        log_file_path = '/home/user/odoo18/visitor_notifications.log'

        # Ensure the log directory exists
        log_directory = os.path.dirname(log_file_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Open log file in append mode
        with open(log_file_path, 'a') as log_file:
            if self.host.work_email:  # Ensure host has an email address
                # Handle 'purpose' to make sure it's a string before slicing
                if not isinstance(self.purpose, str):
                    self.purpose = str(self.purpose) if self.purpose else "(No purpose provided)"

                # Compose email content
                email_content = f"Visitor Details:\n"
                email_content += f"Name: {self.name}\n"
                email_content += f"Phone: {self.phone}\n"
                email_content += f"Purpose: {self.purpose}\n"
                email_content += f"Visit Date: {self.visit_date}\n"
                email_content += f"Visitor's Email: {self.email}\n"
                email_content += f"Host's Email: {self.host.work_email}\n"
                # email_content += f"Host:{self.host}\n"
                # if self.email:
                #     email_content += f"Visitor's Email: {self.email}\n"
                #     email_content += f"Host's Email: {self.host.work_email }\n"

                # Compose the email
                email = EmailMessage()
                email['From'] = 'admin@company.com'  # Replace with an actual sender email address
                email['To'] = self.host.work_email  # Host's email
                email['Subject'] = f"Visitor Notification: {self.name} visiting at {self.visit_date}"
                email.set_content(email_content)

                try:
                    # Simulate sending the email (using local SMTP for testing)
                    smtp_host = 'localhost'  # Local SMTP server address
                    smtp_port = 1025  # Local SMTP server port (adjust for your server)

                    with smtplib.SMTP(smtp_host, smtp_port) as server:
                        server.send_message(email)

                    # Log success
                    log_message = f"{datetime.now()} - SUCCESS: Email sent to {self.host.work_email} for visitor '{self.name}'\n"
                    log_message += f"Visitor Details - Name: {self.name}, Phone: {self.phone}, Purpose: {self.purpose}... Visit Date: {self.visit_date} \n"
                    log_file.write(log_message)

                    # Update state to 'notified' after sending the email
                    self.state = 'notified'

                except Exception as e:
                    # Log failure
                    log_message = f"{datetime.now()} - ERROR: Failed to send email to {self.host.work_email} for visitor '{self.name}'. Error: {str(e)}\n"
                    log_message += f"Visitor Details - Name: {self.name}, Phone: {self.phone}, Purpose: {self.purpose}... Visit Date: {self.visit_date}\n"
                    log_file.write(log_message)