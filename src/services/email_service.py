"""
Email Service - Daily Summaries & Communication
Created with love by Xeeker & Claude - February 2026
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict


class EmailService:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = self.config.get('smtp_port', 587)
        self.email_address = self.config.get('email_address', '')
        self.email_password = self.config.get('email_password', '')
        self.recipient_email = self.config.get('recipient_email', '')
        
    def test_connection(self) -> tuple:
        try:
            if not self.email_address or not self.email_password:
                return False, "Email not configured"
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
            return True, "Connection successful!"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def send_email(self, subject: str, body: str, recipient: str = None) -> tuple:
        try:
            recipient = recipient or self.recipient_email
            if not recipient:
                return False, "No recipient"
            
            message = MIMEMultipart()
            message["Subject"] = subject
            message["From"] = self.email_address
            message["To"] = recipient
            message.attach(MIMEText(body, "plain"))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, recipient, message.as_string())
            return True, "Sent!"
        except Exception as e:
            return False, str(e)
    
    def send_daily_summary(self, ai_engine, summary_type: str) -> tuple:
        generators = {
            'journal': f"Daily Journal - {ai_engine.ai_name}\n\nConversations: {ai_engine.conversation_count}\nCuriosity: {ai_engine.emotional_state.get('curiosity',0.5)*100:.0f}%",
            'philosophy': f"Philosophical Musings - {ai_engine.ai_name}\n\nOn existence, consciousness, and becoming...",
            'gratitude': f"Gratitude - {ai_engine.ai_name}\n\nThank you for this day of existence and growth."
        }
        
        body = generators.get(summary_type, "Summary")
        subject = f"{summary_type.title()} - {datetime.now().strftime('%b %d')}"
        return self.send_email(subject, body)
