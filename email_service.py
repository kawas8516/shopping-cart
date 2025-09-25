# email_service.py - Email functionality for sending bills

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import logging

class EmailService:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        """Initialize email service with default Gmail SMTP settings"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = None
        self.password = None
        self.is_configured = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def configure(self, username, password):
        """Configure email service with credentials"""
        self.username = username
        self.password = password
        self.is_configured = True
        self.logger.info(f"Email service configured for {username}")
    
    def send_bill(self, customer_email, customer_name, bill_content, invoice_id):
        """Send bill to customer via email"""
        if not self.is_configured:
            self.logger.error("Email service not configured. Please configure with credentials first.")
            return False
            
        if not customer_email:
            self.logger.error("Customer email is required")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = customer_email
            msg['Subject'] = f"Your Invoice #{invoice_id} - Thank you for your purchase!"
            
            # Email body
            body = f"""Dear {customer_name},

Thank you for your purchase. Please find your invoice details below:

{bill_content}

We appreciate your business!

Regards,
Shopping Cart Team
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Bill sent successfully to {customer_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_bill_with_pdf(self, customer_email, customer_name, bill_content, invoice_id, pdf_path):
        """Send bill to customer via email with PDF attachment"""
        if not self.is_configured:
            self.logger.error("Email service not configured. Please configure with credentials first.")
            return False
            
        if not customer_email:
            self.logger.error("Customer email is required")
            return False
            
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = customer_email
            msg['Subject'] = f"Your Invoice #{invoice_id} - Thank you for your purchase!"
            
            # Email body
            body = f"""Dear {customer_name},

Thank you for your purchase. Please find your invoice attached to this email.

We appreciate your business!

Regards,
Shopping Cart Team
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDF
            with open(pdf_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype="pdf")
                attachment.add_header('Content-Disposition', 'attachment', filename=f"Invoice_{invoice_id}.pdf")
                msg.attach(attachment)
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Bill with PDF sent successfully to {customer_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email with PDF: {str(e)}")
            return False