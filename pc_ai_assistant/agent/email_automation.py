"""
Email automation module for Riphah Assistant
Handles automated email sending
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional, List


class EmailAutomation:
    """Handles automated email operations"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_email(
        self,
        from_email: str,
        from_password: str,
        to_email: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html: bool = False
    ) -> dict:
        """
        Send an email with optional attachments
        
        Args:
            from_email: Sender email address
            from_password: Sender email password (or app password)
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            attachments: List of file paths to attach
            html: Whether body is HTML content
            
        Returns:
            dict with status and message
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach body
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type))
            
            # Attach files if provided
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(from_email, from_password)
                server.send_message(msg)
            
            return {
                'status': 'success',
                'message': f'Email sent successfully to {to_email}'
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                'status': 'error',
                'message': 'Authentication failed. Check email and password (use App Password for Gmail)'
            }
        except smtplib.SMTPException as e:
            return {
                'status': 'error',
                'message': f'SMTP error: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error sending email: {str(e)}'
            }
    
    def send_admission_inquiry(
        self,
        from_email: str,
        from_password: str,
        student_name: str,
        program: str,
        query: str
    ) -> dict:
        """
        Send admission inquiry email to Riphah University
        
        Args:
            from_email: Student email
            from_password: Email password
            student_name: Student's full name
            program: Program of interest
            query: Inquiry message
            
        Returns:
            dict with status and message
        """
        to_email = "admissions@riphah.edu.pk"  # Riphah admissions email
        subject = f"Admission Inquiry - {program}"
        
        body = f"""
Dear Admissions Office,

I am writing to inquire about admission to the {program} program at Riphah University.

Student Name: {student_name}
Email: {from_email}
Program of Interest: {program}

Query:
{query}

I would appreciate any information you can provide regarding:
- Admission requirements
- Application deadlines
- Fee structure
- Scholarship opportunities

Thank you for your time and assistance.

Best regards,
{student_name}
"""
        
        return self.send_email(
            from_email=from_email,
            from_password=from_password,
            to_email=to_email,
            subject=subject,
            body=body
        )
    
    def send_application_confirmation(
        self,
        from_email: str,
        from_password: str,
        to_email: str,
        student_name: str,
        application_id: str,
        program: str
    ) -> dict:
        """
        Send application confirmation email
        
        Args:
            from_email: Sender email
            from_password: Email password
            to_email: Recipient email
            student_name: Student's name
            application_id: Application reference ID
            program: Applied program
            
        Returns:
            dict with status and message
        """
        subject = f"Application Confirmation - {application_id}"
        
        body = f"""
Dear {student_name},

This is to confirm that your application has been successfully submitted to Riphah University.

Application Details:
- Application ID: {application_id}
- Program: {program}
- Submission Date: {self._get_current_date()}

Next Steps:
1. Check your email regularly for updates
2. Prepare required documents
3. Wait for admission test schedule (if applicable)
4. Track your application status on the portal

If you have any questions, please contact the admissions office.

Best regards,
Riphah Assistant (Automated System)
"""
        
        return self.send_email(
            from_email=from_email,
            from_password=from_password,
            to_email=to_email,
            subject=subject,
            body=body
        )
    
    def _get_current_date(self) -> str:
        """Get current date in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")


# Convenience function
def send_email_simple(to: str, subject: str, body: str, from_email: str = None, from_password: str = None) -> dict:
    """
    Simple email sending function
    
    Note: For Gmail, you need to:
    1. Enable 2-factor authentication
    2. Generate an App Password
    3. Use the App Password instead of your regular password
    """
    if not from_email or not from_password:
        return {
            'status': 'error',
            'message': 'Email credentials not provided. Set FROM_EMAIL and FROM_PASSWORD in environment or config.'
        }
    
    automation = EmailAutomation()
    return automation.send_email(
        from_email=from_email,
        from_password=from_password,
        to_email=to,
        subject=subject,
        body=body
    )
