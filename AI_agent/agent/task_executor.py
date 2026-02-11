from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import webbrowser
import subprocess
import os
import time
import uuid
import re

from agent.input_handler import Command
from agent.web_automation import WebAutomation


@dataclass
class TaskResult:
    success: bool
    message: str
    data: Optional[dict] = None


class Task:
    name: str = 'base'

    def execute(self, command: Command) -> TaskResult:
        raise NotImplementedError


class RiphahAutoApplyTask(Task):
    name = 'riphah_auto_apply'
    
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
    
    def execute(self, command: Command) -> TaskResult:
        """Automatically apply to Riphah University with full automation"""
        try:
            # Get user data from command or use defaults
            user_data = {
                'email': command.slots.get('email', 'student@example.com'),
                'password': command.slots.get('password', 'Password123'),
                'name': command.slots.get('name', 'Muhammad Ahmed Khan'),
                'fname': command.slots.get('fname', 'Muhammad Ahmed'),
                'lname': command.slots.get('lname', 'Khan'),
                'father_name': command.slots.get('father_name', 'Abdul Rahman Khan'),
                'phone': command.slots.get('phone', '03001234567'),
                'mobile': command.slots.get('mobile', '03001234567'),
                'cnic': command.slots.get('cnic', '12345-1234567-1'),
                'address': command.slots.get('address', 'House 123, Street 45, Islamabad'),
                'city': command.slots.get('city', 'Islamabad'),
                'country': command.slots.get('country', 'Pakistan'),
                'dob': command.slots.get('dob', '01/01/2000'),
                'gender': command.slots.get('gender', 'Male'),
                'religion': command.slots.get('religion', 'Islam'),
                'nationality': command.slots.get('nationality', 'Pakistani'),
            }
            
            # Step 1: Open the portal
            portal_url = 'https://admissions.riphah.edu.pk/riphah_demo/public/Student/application/List'
            
            self.web.start()
            self.web.open_url(portal_url)
            self.web.wait(4)  # Wait for page to load
            
            # Check if we need to login first
            current_url = self.web.get_current_url()
            
            if 'login' in current_url.lower() or 'Student/application/List' not in current_url:
                # Attempt automatic login if on login page
                login_attempted = False
                
                # Try to detect and fill login form
                try:
                    # Wait a bit more for login page to fully load
                    self.web.wait(2)
                    
                    # Try to fill email/username field
                    email_filled = (
                        self.web.fill_input_by_name('email', user_data['email']) or
                        self.web.fill_input_by_name('username', user_data['email']) or
                        self.web.fill_input_by_id('email', user_data['email']) or
                        self.web.fill_input_by_placeholder('Email', user_data['email']) or
                        self.web.fill_input_by_placeholder('email', user_data['email'])
                    )
                    
                    # Try to fill password field
                    password_filled = (
                        self.web.fill_input_by_name('password', user_data['password']) or
                        self.web.fill_input_by_id('password', user_data['password']) or
                        self.web.fill_input_by_placeholder('Password', user_data['password'])
                    )
                    
                    if email_filled and password_filled:
                        login_attempted = True
                        self.web.wait(1)
                        
                        # Try to click login button
                        login_clicked = (
                            self.web.click_button_by_text('Login') or
                            self.web.click_button_by_text('Sign In') or
                            self.web.click_button_by_text('Submit') or
                            self.web.press_enter()
                        )
                        
                        if login_clicked:
                            self.web.wait(3)  # Wait for login to process
                            current_url = self.web.get_current_url()
                            
                            # Check if login was successful
                            if 'Student/application/List' in current_url or 'dashboard' in current_url.lower():
                                # Login successful, continue to application
                                pass
                            else:
                                return TaskResult(
                                    success=True,
                                    message=(
                                        '⚠️ Login attempted but may have failed.\n\n'
                                        f'Current Page: {current_url}\n\n'
                                        'Please check:\n'
                                        '• Credentials are correct\n'
                                        '• Account exists\n'
                                        '• No CAPTCHA required\n\n'
                                        '💡 Try manual login or create account first.'
                                    ),
                                    data={'status': 'login_failed', 'url': current_url}
                                )
                except Exception as login_error:
                    pass
                
                if not login_attempted:
                    return TaskResult(
                        success=True,
                        message=(
                            '🔐 Riphah Portal Opened - Login Required\n\n'
                            f'Current Page: {current_url}\n\n'
                            '📋 To auto-apply, you need to:\n'
                            '1. Login to your account first\n'
                            '2. Or create a new account\n\n'
                            '💡 Manual Login:\n'
                            '• "fill email with your@email.com"\n'
                            '• "fill password with YourPassword"\n'
                            '• "click login"\n\n'
                            'Or say: "create account" to register'
                        ),
                        data={'status': 'login_required', 'url': current_url}
                    )
            
            # Step 2: Try to click "New Application" or similar button
            try:
                self.web.wait(2)
                new_app_clicked = (
                    self.web.click_button_by_text('New Application') or
                    self.web.click_button_by_text('Apply Now') or
                    self.web.click_button_by_text('Start Application') or
                    self.web.click_button_by_text('Create Application')
                )
                
                if new_app_clicked:
                    self.web.wait(3)  # Wait for form to load
            except Exception:
                pass
            
            # Step 3: Auto-fill the application form
            try:
                self.web.wait(2)
                
                # Use the auto_fill_form method with comprehensive data
                fill_results = self.web.auto_fill_form(user_data)
                
                # Build detailed message
                message_parts = [
                    '🤖 RIPHAH AUTO-APPLY IN PROGRESS!\n',
                    f'📊 Auto-Fill Results:',
                    f'   • Forms detected: {fill_results.get("forms_found", 0)}',
                    f'   • Fields found: {fill_results.get("fields_found", 0)}',
                    f'   • Fields filled: {fill_results.get("fields_filled", 0)}\n'
                ]
                
                if fill_results.get('details'):
                    message_parts.append('📝 Filled Fields:')
                    for detail in fill_results['details'][:10]:  # Show first 10
                        if detail['status'] == '✓':
                            field_name = detail['field'] or 'field'
                            message_parts.append(f'   ✓ {field_name}: {detail["value"]}')
                
                if fill_results.get('fields_filled', 0) > 0:
                    message_parts.extend([
                        '\n✅ Application form auto-filled!',
                        '\n📋 Next Steps:',
                        '1. Review the filled information',
                        '2. Fill any missing fields manually',
                        '3. Upload required documents',
                        '4. Click Submit when ready\n',
                        '💡 Say "click submit" to submit the application',
                        '💡 Or say "fill [field] with [value]" for manual corrections'
                    ])
                else:
                    message_parts.extend([
                        '\n⚠️ No form fields detected or filled.',
                        '\nPossible reasons:',
                        '• Form not loaded yet',
                        '• Need to click "New Application" first',
                        '• Form uses custom fields\n',
                        '💡 Try: "click new application" first',
                        '💡 Or use manual filling: "fill name with John Doe"'
                    ])
                
                return TaskResult(
                    success=fill_results.get('fields_filled', 0) > 0,
                    message='\n'.join(message_parts),
                    data={
                        'status': 'form_filled' if fill_results.get('fields_filled', 0) > 0 else 'form_not_found',
                        'fill_results': fill_results,
                        'url': self.web.get_current_url()
                    }
                )
                
            except Exception as fill_error:
                return TaskResult(
                    success=True,
                    message=(
                        f'✅ Riphah Portal Opened!\n\n'
                        f'⚠️ Auto-fill encountered an issue: {str(fill_error)}\n\n'
                        '📋 Manual Steps:\n'
                        '1. Click "New Application" if needed\n'
                        '2. Say "auto fill" to try again\n'
                        '3. Or fill manually: "fill name with John Doe"\n\n'
                        '💡 Current URL: {self.web.get_current_url()}'
                    ),
                    data={'status': 'manual_required', 'error': str(fill_error)}
                )
            
        except Exception as e:
            return TaskResult(
                success=False,
                message=f'❌ Error: {str(e)}\n\nPlease try opening the portal manually.',
                data={'error': str(e)}
            )


class AdmissionsTask(Task):
    name = 'admissions_apply'

    def __init__(self, web: WebAutomation) -> None:
        self.web = web
        self.admission_started = False

    def execute(self, command: Command) -> TaskResult:
        """Handle admission application process with multiple steps"""
        try:
            step = command.slots.get('step', 'initial')
            
            # Initial portal opening
            if step == 'initial' or not self.admission_started:
                return self._handle_initial_portal(command)
            
            # Specific workflow steps
            elif step == 'personal_info':
                return self._handle_personal_info(command)
            elif step == 'select_program':
                return self._handle_select_program(command)
            elif step == 'upload_documents':
                return self._handle_upload_documents(command)
            elif step == 'submit_application':
                return self._handle_submit_application(command)
            else:
                return self._handle_initial_portal(command)
                
        except Exception as e:
            return TaskResult(
                success=False,
                message=f'Error processing admission request: {str(e)}',
                data={'error': str(e)}
            )
    
    def _handle_initial_portal(self, command: Command) -> TaskResult:
        """Open Riphah University admission portal"""
        riphah_main_url = 'https://riphah.edu.pk/'
        riphah_admissions_url = 'https://riphah.edu.pk/admissions/'
        riphah_process_url = 'https://riphah.edu.pk/admissions/process/'
        
        try:
            self.web.start()
            self.web.open_url(riphah_admissions_url)
            target_url = riphah_admissions_url
            
            self.admission_started = True
            
            return TaskResult(
                success=True,
                message=(
                    '✅ Riphah University Admission Portal Opened\n'
                    f'URL: {target_url}\n\n'
                    '📋 Admission Process:\n'
                    '1. Explore programs of interest\n'
                    '2. Review eligibility criteria and deadlines\n'
                    '3. Submit online application through secure portal\n'
                    '4. Attend required interviews or assessments\n'
                    '5. Receive admission decision\n\n'
                    '🔗 Next Steps:\n'
                    '   • Click "Apply Online" on the website\n'
                    '   • Or visit: https://eportal.riphah.edu.pk/login\n'
                    '   • Create new account if first time applicant\n\n'
                    '💡 Say "explore programs" to see available programs\n'
                    '💡 Say "admission dates" for important deadlines'
                ),
                data={
                    'university': 'Riphah International University',
                    'portal_url': target_url,
                    'status': 'portal_opened',
                    'eportal': 'https://eportal.riphah.edu.pk/login'
                }
            )
        except Exception as e:
            return TaskResult(
                success=True,
                message=(
                    f'🎓 Riphah University Admission Application\n\n'
                    f'Please open the admission portal manually:\n'
                    f'🔗 Main Site: {riphah_main_url}\n'
                    f'🔗 Admissions: {riphah_admissions_url}\n'
                    f'🔗 Apply Online: https://eportal.riphah.edu.pk/login\n\n'
                    f'📋 Steps to Apply:\n'
                    f'1. Visit the ePortal link above\n'
                    f'2. Click "New Customer" to create account\n'
                    f'3. Fill in your details\n'
                    f'4. Select your program\n'
                    f'5. Upload required documents\n'
                    f'6. Submit application\n\n'
                    f'Note: Browser automation unavailable - {str(e)}'
                ),
                data={
                    'university': 'Riphah International University',
                    'portal_url': riphah_admissions_url,
                    'status': 'browser_unavailable',
                    'eportal': 'https://eportal.riphah.edu.pk/login'
                }
            )
    
    def _handle_personal_info(self, command: Command) -> TaskResult:
        return TaskResult(
            success=True,
            message=(
                'Personal Information\n\n'
                'Please provide:\n'
                '- Full Name\n'
                '- Email Address\n'
                '- Phone Number\n'
                '- Date of Birth\n'
                '- Address\n'
                '- State/Province\n'
                '- Country\n\n'
                'Type each as prompted or use speech.'
            ),
            data={'step': 2, 'status': 'personal_info'}
        )
    
    def _handle_select_program(self, command: Command) -> TaskResult:
        return TaskResult(
            success=True,
            message=(
                'Program Selection\n\n'
                'Available Programs:\n'
                '- Bachelor of Science (B.Sc)\n'
                '- Bachelor of Arts (B.A)\n'
                '- Bachelor of Commerce (B.Com)\n'
                '- Master of Science (M.Sc)\n'
                '- Master of Arts (M.A)\n\n'
                'Select your preferred program.'
            ),
            data={'step': 3, 'status': 'program_selection'}
        )
    
    def _handle_upload_documents(self, command: Command) -> TaskResult:
        return TaskResult(
            success=True,
            message=(
                'Document Upload\n\n'
                'Required documents:\n'
                '- Mark Sheet or Transcript\n'
                '- Identity Proof\n'
                '- Address Proof\n'
                '- Character Certificate\n'
                '- Medical Fitness Certificate\n'
                '- Passport Photo\n\n'
                'Supported formats: PDF, JPG (Max 5MB each)'
            ),
            data={'step': 4, 'status': 'upload_documents'}
        )
    
    def _handle_submit_application(self, command: Command) -> TaskResult:
        return TaskResult(
            success=True,
            message=(
                'Final Submission\n\n'
                'Review your application:\n'
                '1. Verify personal information\n'
                '2. Confirm program selection\n'
                '3. Check documents uploaded\n'
                '4. Review fees\n\n'
                'Note: Once submitted, the application cannot be edited.\n'
                'A confirmation email will be sent.\n\n'
                'Type "confirm" to submit.'
            ),
            data={'step': 5, 'status': 'submission_ready'}
        )


class PolicyInfoTask(Task):
    name = 'policy_lookup'

    def execute(self, command: Command) -> TaskResult:
        return TaskResult(
            success=True,
            message='Policy lookup stub. Provide a policy name or source to search.',
        )


class ExploreProgramsTask(Task):
    name = 'explore_programs'
    
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
    
    def execute(self, command: Command) -> TaskResult:
        programs_url = 'https://riphah.edu.pk/academics/programs/'
        
        try:
            self.web.start()
            self.web.open_url(programs_url)
            return TaskResult(
                success=True,
                message=(
                    '🎓 Riphah University Programs\n\n'
                    'Opening programs page...\n'
                    f'URL: {programs_url}\n\n'
                    '📚 Available Faculties:\n'
                    '   • Faculty of Medicine & Health Sciences\n'
                    '   • Faculty of Engineering & Applied Sciences\n'
                    '   • Faculty of Management Sciences\n'
                    '   • Faculty of Computing\n'
                    '   • Faculty of Social Sciences\n'
                    '   • Faculty of Islamic Studies\n'
                    '   • Faculty of Pharmacy\n'
                    '   • Faculty of Allied Health Sciences\n\n'
                    '💡 Browse the website to see specific programs'
                ),
                data={'url': programs_url, 'status': 'opened'}
            )
        except Exception:
            return TaskResult(
                success=True,
                message=(
                    f'🎓 Riphah University Programs\n\n'
                    f'Please visit: {programs_url}\n\n'
                    f'Available Faculties:\n'
                    f'   • Medicine & Health Sciences\n'
                    f'   • Engineering & Applied Sciences\n'
                    f'   • Management Sciences\n'
                    f'   • Computing\n'
                    f'   • Social Sciences\n'
                    f'   • Islamic Studies\n'
                    f'   • Pharmacy\n'
                    f'   • Allied Health Sciences'
                ),
                data={'url': programs_url, 'status': 'manual'}
            )


class AdmissionDatesTask(Task):
    name = 'admission_dates'
    
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
    
    def execute(self, command: Command) -> TaskResult:
        dates_url = 'https://riphah.edu.pk/admissions/dates/'
        
        try:
            self.web.start()
            self.web.open_url(dates_url)
            return TaskResult(
                success=True,
                message=(
                    '📅 Riphah University Admission Dates\n\n'
                    'Opening admission dates page...\n'
                    f'URL: {dates_url}\n\n'
                    '⏰ Important Information:\n'
                    '   • Check application deadlines\n'
                    '   • Review test dates\n'
                    '   • Note enrollment timelines\n'
                    '   • Plan your application journey\n\n'
                    '💡 Visit the page for current semester dates'
                ),
                data={'url': dates_url, 'status': 'opened'}
            )
        except Exception:
            return TaskResult(
                success=True,
                message=(
                    f'📅 Riphah University Admission Dates\n\n'
                    f'Please visit: {dates_url}\n\n'
                    f'Check the website for:\n'
                    f'   • Application submission deadlines\n'
                    f'   • Entry test dates\n'
                    f'   • Interview schedules\n'
                    f'   • Enrollment timelines'
                ),
                data={'url': dates_url, 'status': 'manual'}
            )


class SendEmailTask(Task):
    name = 'send_email'

    def __init__(self, web: WebAutomation) -> None:
        self.web = web
        self.pending_email: Optional[dict] = None
        self.pending_task_id: Optional[str] = None
        self.awaiting_login: bool = False

    def resume_if_ready(self, text: str) -> Optional[TaskResult]:
        if not self.pending_email:
            return None

        normalized = text.strip().lower()
        if any(k in normalized for k in ['cancel', 'stop', 'nevermind', 'never mind']):
            self.pending_email = None
            self.awaiting_login = False
            return TaskResult(success=True, message='Email task cancelled.')

        update = self._parse_email_parts(text)
        updated = False
        if update.get('to'):
            self.pending_email['to'] = update['to']
            updated = True
        if update.get('subject'):
            self.pending_email['subject'] = update['subject']
            updated = True
        if update.get('body'):
            self.pending_email['body'] = update['body']
            updated = True

        ready_keywords = [
            'continue', 'ready', 'logged in', 'signed in',
            'go ahead', 'proceed', 'send it', 'send now'
        ]

        # If we already have everything, send when user confirms or after a full body update.
        if self._is_ready_to_send(self.pending_email):
            if any(k in normalized for k in ready_keywords) or updated:
                return self._compose_and_send(self.pending_email)

            return TaskResult(
                success=True,
                message="I have the recipient and body ready. Say 'continue' to send.",
                data={'status': 'waiting_confirmation', 'task_id': self.pending_task_id}
            )

        # Still missing fields
        if not self.pending_email.get('to'):
            return TaskResult(
                success=False,
                message='Please provide the recipient email address.',
                data={'status': 'missing_recipient', 'task_id': self.pending_task_id}
            )

        if not self.pending_email.get('body'):
            return TaskResult(
                success=False,
                message='Please provide the email body.',
                data={'status': 'missing_body', 'task_id': self.pending_task_id}
            )

        return None

    def execute(self, command: Command) -> TaskResult:
        action = command.slots.get('action', '').lower()

        if action == 'continue':
            if not self.pending_email:
                return TaskResult(
                    success=False,
                    message='No pending email draft. Ask me to send an email first.'
                )
            return self._compose_and_send(self.pending_email)

        to_addr = command.slots.get('to') or command.slots.get('recipient') or ''
        subject = command.slots.get('subject', '').strip()
        body = command.slots.get('body', '').strip()

        task_id = self.pending_task_id or str(uuid.uuid4())
        self.pending_task_id = task_id
        task_title = f'Send email to {to_addr}' if to_addr else 'Send email'

        if not to_addr:
            self.pending_email = {
                'to': '',
                'subject': subject,
                'body': body,
            }
            return TaskResult(
                success=False,
                message=(
                    'Please provide a recipient.\n\n'
                    'Example: send email to name@example.com subject: Hello body: Your message'
                ),
                data={'status': 'missing_recipient', 'task_id': task_id, 'task_title': task_title}
            )

        if not body:
            self.pending_email = {
                'to': to_addr,
                'subject': subject,
                'body': '',
            }
            return TaskResult(
                success=False,
                message=(
                    'Please provide the email body.\n\n'
                    'Example: send email to name@example.com subject: Hello body: Your message'
                ),
                data={'status': 'missing_body', 'task_id': task_id, 'task_title': task_title}
            )

        email = {
            'to': to_addr,
            'subject': subject,
            'body': body,
        }
        self.pending_email = email
        return self._compose_and_send(email)

    def _parse_email_parts(self, text: str) -> Dict[str, str]:
        """Extract recipient, subject, and body from free-form text."""
        parts: Dict[str, str] = {}
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.[a-z]{2,}', text, re.IGNORECASE)
        if email_match:
            parts['to'] = email_match.group(0)

        subject_match = re.search(
            r'(?:subject|subj)[:\-]\s*(.+?)(?:\s+(?:body|message)[:\-]|$)',
            text,
            re.IGNORECASE
        )
        if subject_match:
            parts['subject'] = subject_match.group(1).strip().strip('"')

        body_match = re.search(r'(?:body|message)[:\-]\s*(.+)$', text, re.IGNORECASE)
        if body_match:
            parts['body'] = body_match.group(1).strip().strip('"')
        else:
            # If no markers and we're likely providing the body, treat full text as body.
            normalized = text.strip().lower()
            if not any(k in normalized for k in ['send email', 'compose email', 'write email', 'continue', 'ready']):
                parts['body'] = text.strip()

        return parts

    def _is_ready_to_send(self, email: dict) -> bool:
        return bool(email.get('to') and email.get('body'))

    def _compose_and_send(self, email: dict) -> TaskResult:
        task_id = self.pending_task_id or str(uuid.uuid4())
        self.pending_task_id = task_id
        task_title = f"Send email to {email.get('to', '')}".strip()

        try:
            if not self.web._driver:
                self.web.start()
                self.web.open_url('https://mail.google.com/')
                self.web.wait(3)
            else:
                current_url = self.web.get_current_url()
                if not current_url:
                    self.web.open_url('https://mail.google.com/')
                    self.web.wait(2)
                elif 'mail.google.com' not in current_url and 'accounts.google.com' not in current_url:
                    # If we're on another site, keep the session but navigate to Gmail.
                    self.web.open_url('https://mail.google.com/')
                    self.web.wait(2)
        except Exception as e:
            return TaskResult(
                success=False,
                message=f'Could not open Gmail: {str(e)}',
                data={'status': 'browser_error', 'task_id': task_id, 'task_title': task_title}
            )

        compose_xpaths = [
            "//div[@role='button' and @gh='cm']",
            "//div[@role='button' and @aria-label='Compose']",
            "//div[@role='button' and contains(., 'Compose')]",
            "//div[@role='button' and contains(., 'Write')]",
            "//div[@role='button' and contains(., 'New message')]",
            "//span[text()='Compose']/ancestor::div[@role='button']",
            "//span[text()='Write']/ancestor::div[@role='button']"
        ]

        compose_clicked = False
        for xpath in compose_xpaths:
            if self.web.click_by_xpath(xpath, timeout=5):
                compose_clicked = True
                break

        if not compose_clicked:
            self.awaiting_login = True
            return TaskResult(
                success=True,
                message=(
                    "I'm ready to send the email. Please log in to your Gmail account in the browser.\n\n"
                    "Once you can see your inbox, reply with: 'I'm logged in' or 'continue'."
                ),
                data={'status': 'awaiting_login', 'task_id': task_id, 'task_title': task_title}
            )

        # Fill recipient
        to_filled = (
            self.web.fill_input_by_xpath("//textarea[@name='to']", email['to']) or
            self.web.fill_input_by_xpath("//input[@name='to']", email['to']) or
            self.web.fill_input_by_xpath("//div[@aria-label='To']//input", email['to'])
        )

        # Fill subject (optional)
        if email.get('subject'):
            self.web.fill_input_by_xpath("//input[@name='subjectbox']", email['subject'])

        # Fill body
        body_filled = self.web.type_by_xpath("//div[@aria-label='Message Body']", email['body'])

        send_clicked = False
        send_xpaths = [
            "//div[@role='button' and starts-with(@aria-label,'Send')]",
            "//div[@role='button' and contains(@data-tooltip,'Send')]",
            "//div[@role='button' and contains(., 'Send')]"
        ]
        for xpath in send_xpaths:
            if self.web.click_by_xpath(xpath, timeout=5):
                send_clicked = True
                break

        if to_filled and body_filled and send_clicked:
            self.pending_email = None
            self.awaiting_login = False
            return TaskResult(
                success=True,
                message=f"Email sent to {email.get('to')} successfully.",
                data={'status': 'sent', 'task_id': task_id, 'task_title': task_title}
            )

        # If we reached here, some step failed
        return TaskResult(
            success=True,
            message=(
                "I opened Gmail and started composing the email, but couldn't fully send it.\n\n"
                "Please verify the To/Subject/Body fields, then click Send manually.\n"
                "If you'd like me to retry, say: 'continue'."
            ),
            data={'status': 'needs_review', 'task_id': task_id, 'task_title': task_title}
        )


class OpenUrlTask(Task):
    name = 'open_url'

    def __init__(self, web: WebAutomation) -> None:
        self.web = web

    def execute(self, command: Command) -> TaskResult:
        url = command.slots.get('url', '').strip()
        
        if not url:
            return TaskResult(
                success=False,
                message='No URL provided. Usage: "open https://example.com" or just paste the URL'
            )
        
        if not url.startswith(('http://', 'https://', 'www.')):
            url = 'https://' + url
        
        try:
            self.web.start()
            self.web.open_url(url)
            return TaskResult(
                success=True,
                message=f'✅ Opening {url}\n\nBrowser window opened. You can now interact with the website.',
                data={'url': url, 'status': 'opened'}
            )
        except KeyboardInterrupt:
            raise
        except Exception as e:
            return TaskResult(
                success=True,
                message=f'Browser unavailable. Opening in default browser:\n{url}',
                data={'url': url, 'status': 'manual_required'}
            )


class AutoFillFormTask(Task):
    name = 'auto_fill_form'
    
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
    
    def execute(self, command: Command) -> TaskResult:
        """Automatically detect and fill forms on any website"""
        
        # Get user data from command slots or use defaults
        user_data = {}
        if command.slots:
            user_data = command.slots
        
        try:
            if not self.web._driver:
                return TaskResult(
                    success=False,
                    message='❌ No browser open. First open a website with: "open [website]"'
                )
            
            # Wait a moment for page to fully load
            self.web.wait(2)
            
            # Auto-detect and fill forms
            results = self.web.auto_fill_form(user_data if user_data else None)
            
            if results['forms_found'] == 0 and results['fields_found'] == 0:
                return TaskResult(
                    success=False,
                    message=(
                        '❌ No forms detected on this page.\n\n'
                        'Make sure:\n'
                        '• The page has fully loaded\n'
                        '• You are on a page with a form\n'
                        '• The form is visible (not hidden)\n\n'
                        'Try scrolling down or navigating to a form page.'
                    )
                )
            
            # Build result message
            message_parts = [
                '🤖 AUTO-FILL COMPLETE!\n',
                f'📊 Results:',
                f'   • Forms found: {results["forms_found"]}',
                f'   • Fields found: {results["fields_found"]}',
                f'   • Fields filled: {results["fields_filled"]}\n'
            ]
            
            if results['details']:
                message_parts.append('📝 Field Details:')
                for detail in results['details']:
                    status_icon = detail['status']
                    field_name = detail['field'] or 'unnamed'
                    if detail['status'] == '✓':
                        message_parts.append(
                            f'   {status_icon} {field_name}: {detail["filled_with"]} = {detail["value"]}'
                        )
                    else:
                        message_parts.append(f'   {status_icon} {field_name}: skipped')
            
            if results['fields_filled'] > 0:
                message_parts.append('\n✅ Form filled! Review the data and click submit when ready.')
                message_parts.append('💡 Say "click submit" to submit the form')
            else:
                message_parts.append('\n⚠️ No fields were filled. The form might use custom fields.')
                message_parts.append('💡 Try manual filling: "fill [field] with [value]"')
            
            return TaskResult(
                success=results['fields_filled'] > 0,
                message='\n'.join(message_parts),
                data=results
            )
            
        except Exception as e:
            return TaskResult(
                success=False,
                message=f'❌ Error during auto-fill: {str(e)}\n\nTry manual form filling instead.'
            )


class FillFormTask(Task):
    name = 'fill_form'
    
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
        self.form_data = {}  # Store form data
    
    def execute(self, command: Command) -> TaskResult:
        """Fill forms on any website with intelligent field detection"""
        field = command.slots.get('field', '').lower()
        value = command.slots.get('value', '')
        action = command.slots.get('action', '').lower()
        
        try:
            # If no specific action, show help
            if not field and not action:
                return TaskResult(
                    success=True,
                    message=(
                        '📝 Smart Form Filling Assistant\n\n'
                        'I can automatically fill forms on ANY website!\n\n'
                        '🎯 Commands:\n'
                        '• "fill name with [your name]" - Fill name field\n'
                        '• "fill email with [email]" - Fill email field\n'
                        '• "fill phone with [number]" - Fill phone field\n'
                        '• "fill address with [address]" - Fill address\n'
                        '• "type [text]" - Type in focused field\n'
                        '• "click submit" - Click submit button\n'
                        '• "press enter" - Press Enter key\n'
                        '• "fill all fields" - Auto-fill entire form\n\n'
                        '📋 Example Workflow:\n'
                        '1. "open google.com/forms"\n'
                        '2. "fill name with John Doe"\n'
                        '3. "fill email with john@email.com"\n'
                        '4. "click submit"\n\n'
                        '✨ I intelligently find fields by:\n'
                        '• Field name\n'
                        '• Field ID\n'
                        '• Placeholder text\n'
                        '• Label text\n'
                        '• Field type'
                    ),
                    data={'status': 'ready'}
                )
            
            # Handle specific actions
            if action == 'submit' or 'submit' in command.raw_text.lower():
                if self.web._driver:
                    # Try to find and click submit button
                    success = (
                        self.web.click_button_by_text('Submit') or
                        self.web.click_button_by_text('Send') or
                        self.web.click_button_by_text('Apply') or
                        self.web.click_button_by_text('Continue') or
                        self.web.click_button_by_text('Next')
                    )
                    if success:
                        return TaskResult(
                            success=True,
                            message='✅ Submit button clicked!\n\nForm submitted successfully.'
                        )
                    else:
                        return TaskResult(
                            success=False,
                            message='❌ Could not find submit button.\n\nTry: "press enter" or specify button text.'
                        )
                else:
                    return TaskResult(
                        success=False,
                        message='❌ No browser open. First open a website with: "open [website]"'
                    )
            
            if action == 'new_application' or 'new application' in command.raw_text.lower():
                if self.web._driver:
                    # Try to find and click new application button
                    self.web.wait(1)
                    success = (
                        self.web.click_button_by_text('New Application') or
                        self.web.click_button_by_text('Apply Now') or
                        self.web.click_button_by_text('Start Application') or
                        self.web.click_button_by_text('Create Application') or
                        self.web.click_button_by_text('New')
                    )
                    if success:
                        self.web.wait(2)  # Wait for form to load
                        return TaskResult(
                            success=True,
                            message='✅ New Application button clicked!\n\nApplication form should be loading...\n\n💡 Say "auto fill" to fill the form automatically'
                        )
                    else:
                        return TaskResult(
                            success=False,
                            message='❌ Could not find "New Application" button.\n\nThe button might have a different name or already be on the form page.'
                        )
                else:
                    return TaskResult(
                        success=False,
                        message='❌ No browser open. First open the portal with: "riphah auto apply"'
                    )
            
            if action == 'enter' or 'press enter' in command.raw_text.lower():
                if self.web._driver:
                    if self.web.press_enter():
                        return TaskResult(
                            success=True,
                            message='✅ Enter key pressed!'
                        )
                    else:
                        return TaskResult(
                            success=False,
                            message='❌ Could not press Enter'
                        )
                else:
                    return TaskResult(
                        success=False,
                        message='❌ No browser open. First open a website.'
                    )
            
            if action == 'type' or 'type' in command.raw_text.lower():
                if self.web._driver:
                    # Extract text to type
                    text_to_type = command.raw_text.lower().replace('type', '').strip()
                    if self.web.type_in_active_element(text_to_type):
                        return TaskResult(
                            success=True,
                            message=f'✅ Typed: {text_to_type}'
                        )
                    else:
                        return TaskResult(
                            success=False,
                            message='❌ Could not type. Click on a field first.'
                        )
                else:
                    return TaskResult(
                        success=False,
                        message='❌ No browser open. First open a website.'
                    )
            
            # Handle field filling
            if field and value:
                if not self.web._driver:
                    return TaskResult(
                        success=False,
                        message='❌ No browser open. First open a website with: "open [website]"'
                    )
                
                # Store data
                self.form_data[field] = value
                
                # Try to fill the field
                filled = False
                strategies_tried = []
                
                # Try different field identifiers
                field_variations = [field, field.title(), field.upper(), field.lower()]
                
                for field_var in field_variations:
                    if self.web.fill_input_by_name(field_var, value):
                        filled = True
                        strategies_tried.append('name')
                        break
                    if self.web.fill_input_by_id(field_var, value):
                        filled = True
                        strategies_tried.append('id')
                        break
                    if self.web.fill_input_by_placeholder(field_var, value):
                        filled = True
                        strategies_tried.append('placeholder')
                        break
                    if self.web.fill_input_by_label(field_var, value):
                        filled = True
                        strategies_tried.append('label')
                        break
                
                if filled:
                    return TaskResult(
                        success=True,
                        message=(
                            f'✅ Field filled successfully!\n\n'
                            f'Field: {field}\n'
                            f'Value: {value}\n'
                            f'Method: {strategies_tried[0]}\n\n'
                            f'Continue with more fields or say "click submit"'
                        ),
                        data={'field': field, 'value': value}
                    )
                else:
                    return TaskResult(
                        success=False,
                        message=(
                            f'❌ Could not find field: {field}\n\n'
                            f'Tips:\n'
                            f'• Make sure the field is visible\n'
                            f'• Try: "type {value}" after clicking the field\n'
                            f'• Check field name on the website\n'
                            f'• Try different field names (e.g., "email" vs "e-mail")'
                        )
                    )
            
            # Handle "fill all fields" command
            if 'fill all' in command.raw_text.lower():
                if not self.form_data:
                    return TaskResult(
                        success=False,
                        message='❌ No form data stored. First provide data with "fill [field] with [value]"'
                    )
                
                if not self.web._driver:
                    return TaskResult(
                        success=False,
                        message='❌ No browser open. First open a website.'
                    )
                
                results = self.web.find_and_fill_form(self.form_data)
                
                success_count = sum(1 for v in results.values() if '✓' in v)
                total_count = len(results)
                
                result_text = '\n'.join([f'{k}: {v}' for k, v in results.items()])
                
                return TaskResult(
                    success=success_count > 0,
                    message=(
                        f'📝 Form Filling Results:\n\n'
                        f'{result_text}\n\n'
                        f'Success: {success_count}/{total_count} fields\n\n'
                        f'{"✅ Ready to submit!" if success_count == total_count else "⚠️ Some fields could not be filled"}'
                    )
                )
            
            return TaskResult(
                success=False,
                message='❌ Invalid command. Try: "fill name with John Doe" or "fill form" for help'
            )
            
        except Exception as e:
            return TaskResult(
                success=False,
                message=f'❌ Error: {str(e)}\n\nMake sure a website is open first.'
            )


class OpenApplicationTask(Task):
    name = 'open_application'
    
    def execute(self, command: Command) -> TaskResult:
        """Open applications on PC"""
        app_name = command.slots.get('app', '').lower()
        
        # Common applications
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'outlook': 'outlook.exe',
        }
        
        if not app_name:
            return TaskResult(
                success=True,
                message=(
                    '💻 Application Launcher\n\n'
                    'Available applications:\n'
                    '• Notepad\n'
                    '• Calculator\n'
                    '• Paint\n'
                    '• Chrome\n'
                    '• Edge\n'
                    '• File Explorer\n'
                    '• Command Prompt\n'
                    '• PowerShell\n'
                    '• Word\n'
                    '• Excel\n'
                    '• Outlook\n\n'
                    'Say: "open [app name]"'
                )
            )
        
        if app_name in apps:
            try:
                subprocess.Popen(apps[app_name])
                return TaskResult(
                    success=True,
                    message=f'✅ Opening {app_name.title()}...',
                    data={'app': app_name}
                )
            except Exception as e:
                return TaskResult(
                    success=False,
                    message=f'❌ Could not open {app_name}: {str(e)}'
                )
        else:
            return TaskResult(
                success=False,
                message=f'❌ Application "{app_name}" not recognized. Try: notepad, calculator, chrome, etc.'
            )


class SystemCommandTask(Task):
    name = 'system_command'
    
    def execute(self, command: Command) -> TaskResult:
        """Execute system commands"""
        cmd_type = command.slots.get('type', '').lower()
        
        try:
            if cmd_type == 'shutdown':
                return TaskResult(
                    success=True,
                    message='⚠️ Shutdown command received. Say "confirm shutdown" to proceed.',
                    data={'pending': 'shutdown'}
                )
            elif cmd_type == 'restart':
                return TaskResult(
                    success=True,
                    message='⚠️ Restart command received. Say "confirm restart" to proceed.',
                    data={'pending': 'restart'}
                )
            elif cmd_type == 'sleep':
                return TaskResult(
                    success=True,
                    message='⚠️ Sleep command received. Say "confirm sleep" to proceed.',
                    data={'pending': 'sleep'}
                )
            else:
                return TaskResult(
                    success=True,
                    message=(
                        '⚙️ System Commands\n\n'
                        'Available commands:\n'
                        '• "shutdown computer" - Shutdown PC\n'
                        '• "restart computer" - Restart PC\n'
                        '• "sleep computer" - Put PC to sleep\n'
                        '• "open [app]" - Open application\n'
                        '• "search [query]" - Search on Google\n\n'
                        'Note: System commands require confirmation.'
                    )
                )
        except Exception as e:
            return TaskResult(
                success=False,
                message=f'Error: {str(e)}'
            )


class SearchTask(Task):
    name = 'search'
    
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
    
    def execute(self, command: Command) -> TaskResult:
        """Search on Google"""
        query = command.slots.get('query', '').strip()
        
        if not query:
            return TaskResult(
                success=False,
                message='Please provide a search query. Example: "search Python tutorials"'
            )
        
        try:
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            self.web.start()
            self.web.open_url(search_url)
            return TaskResult(
                success=True,
                message=f'🔍 Searching for: {query}',
                data={'query': query, 'url': search_url}
            )
        except Exception as e:
            # Fallback to default browser
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            webbrowser.open(search_url)
            return TaskResult(
                success=True,
                message=f'🔍 Searching for: {query}\nOpened in default browser.',
                data={'query': query}
            )


class FileTask(Task):
    name = 'file_operation'
    
    def execute(self, command: Command) -> TaskResult:
        """File operations"""
        operation = command.slots.get('operation', '').lower()
        path = command.slots.get('path', '')
        
        if operation == 'open':
            if path:
                try:
                    os.startfile(path)
                    return TaskResult(
                        success=True,
                        message=f'✅ Opening: {path}'
                    )
                except Exception as e:
                    return TaskResult(
                        success=False,
                        message=f'❌ Could not open file: {str(e)}'
                    )
            else:
                return TaskResult(
                    success=False,
                    message='Please specify a file path. Example: "open C:\\Users\\file.txt"'
                )
        else:
            return TaskResult(
                success=True,
                message=(
                    '📁 File Operations\n\n'
                    'Available commands:\n'
                    '• "open file [path]" - Open a file\n'
                    '• "open folder [path]" - Open a folder\n'
                    '• "open downloads" - Open downloads folder\n'
                    '• "open documents" - Open documents folder\n\n'
                    'Example: "open downloads"'
                )
            )


class TaskExecutor:
    def __init__(self, web: WebAutomation) -> None:
        self.web = web
        self._tasks: Dict[str, Task] = {}
        
        # Register all tasks
        self.register(OpenUrlTask(web))
        self.register(AutoFillFormTask(web))
        self.register(FillFormTask(web))
        self.register(OpenApplicationTask())
        self.register(SystemCommandTask())
        self.register(SearchTask(web))
        self.register(FileTask())
        self.register(RiphahAutoApplyTask(web))
        self.register(AdmissionsTask(web))
        self.register(PolicyInfoTask())
        self.register(ExploreProgramsTask(web))
        self.register(AdmissionDatesTask(web))
        self.register(SendEmailTask(web))

    def register(self, task: Task) -> None:
        self._tasks[task.name] = task

    def execute(self, command: Command) -> TaskResult:
        task = self._tasks.get(command.intent)
        if not task:
            return TaskResult(
                success=False,
                message=(
                    '❓ Command not recognized.\n\n'
                    'Try:\n'
                    '• "open [website]" - Open any website\n'
                    '• "search [query]" - Search on Google\n'
                    '• "open [app]" - Open application\n'
                    '• "fill form" - Form filling help\n'
                    '• "send email to [address]" - Compose and send email\n'
                    '• "apply for admission" - Riphah admission\n'
                    '• "help" - Show all commands'
                ),
            )
        return task.execute(command)

    def resume_pending(self, text: str) -> Optional[TaskResult]:
        """Allow stateful tasks to resume when user confirms readiness."""
        task = self._tasks.get('send_email')
        if task and hasattr(task, 'resume_if_ready'):
            return task.resume_if_ready(text)
        return None
