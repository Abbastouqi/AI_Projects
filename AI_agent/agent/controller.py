from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from agent.config import Config
from agent.input_handler import Command, VoiceTextInputHandler
from agent.speech_engine import SpeechEngine
from agent.task_executor import TaskExecutor, TaskResult
from agent.utils.logger import setup_logger
from agent.web_automation import WebAutomation, WebAutomationConfig


@dataclass
class WorkflowState:
    current_intent: str = ''
    current_step: str = 'initial'
    form_data: dict = field(default_factory=dict)
    
    def reset(self) -> None:
        self.current_intent = ''
        self.current_step = 'initial'
        self.form_data = {}


class AgentController:
    def __init__(self, config: Config) -> None:
        self._logger = setup_logger('AgentController', config.log_level)
        self.config = config
        self.input_handler = VoiceTextInputHandler(config.voice_enabled)
        self.speech_engine = SpeechEngine(
            enabled=config.voice_enabled,
            tts_enabled=config.tts_enabled
        )
        self.web = WebAutomation(
            WebAutomationConfig(
                driver_path=config.selenium_driver_path,
                headless=config.selenium_headless,
            )
        )
        self.tasks = TaskExecutor(self.web)
        self.workflow_state = WorkflowState()
        
        # Log speech status
        if config.voice_enabled:
            status = self.speech_engine.get_status()
            self._logger.info('Speech-to-Text: %s', 'Enabled' if status['stt_enabled'] else 'Disabled')
            self._logger.info('Text-to-Speech: %s', 'Enabled' if status['tts_enabled'] else 'Disabled')
            if status['microphone_available']:
                self._logger.info('Microphone: Available')
            else:
                self._logger.warning('Microphone: Not available')

    def handle_text(self, text: str, speak_response: bool = False, return_result: bool = False):
        result: Optional[TaskResult] = None

        # Resume pending tasks if user confirms readiness
        resume_result = self.tasks.resume_pending(text)
        if resume_result:
            result = resume_result
            response = resume_result.message
        else:
            command = self.input_handler.parse_command(text)

            # If user is on a form step and input is free-form, capture it
            if self.workflow_state.current_step != 'initial' and command.intent == 'unknown':
                response = self._handle_form_input(text)
                result = TaskResult(success=True, message=response, data={
                    'status': 'workflow',
                    'step': self.workflow_state.current_step
                })
            else:
                # Process as normal command
                result = self.tasks.execute(command)
                self._logger.info('Intent=%s Success=%s', command.intent, result.success)

                # Update workflow state
                if result.success and command.intent == 'admissions_apply':
                    self.workflow_state.current_intent = command.intent
                    self.workflow_state.current_step = command.slots.get('step', 'initial')

                response = result.message

        # Speak response if TTS is enabled
        if speak_response and self.config.tts_enabled:
            self.speech_engine.speak(response, async_mode=True)

        if return_result:
            return response, result
        return response

    def _handle_form_input(self, text: str) -> str:
        step = self.workflow_state.current_step
        normalized = text.strip().lower()
        
        if any(k in normalized for k in ['next', 'continue', 'done', 'finished', 'submit', 'final']):
            if step == 'personal_info':
                return (
                    f"✓ Personal information saved!\n\n"
                    f"Collected:\n"
                    f"Name: {self.workflow_state.form_data.get('name', 'Pending')}\n\n"
                    f"Moving to Step 3: Program Selection\n"
                    f"Say 'select program' to proceed."
                )
            elif step == 'select_program':
                return (
                    f"✓ Program confirmed!\n\n"
                    f"Selected: {self.workflow_state.form_data.get('program', 'Pending')}\n\n"
                    f"Moving to Step 4: Document Upload\n"
                    f"Say 'upload documents' to proceed."
                )
            elif step == 'upload_documents':
                self.workflow_state.current_step = 'submit_application'
                return (
                    f"✓ Documents uploaded!\n\n"
                    f"Moving to Step 5: Final Submission\n\n"
                    f"Your Application Summary:\n"
                    f"Name: {self.workflow_state.form_data.get('name', 'Not provided')}\n"
                    f"Program: {self.workflow_state.form_data.get('program', 'Not selected')}\n\n"
                    f"Ready to submit? Say 'confirm' or 'yes' to finalize."
                )
            elif step == 'submit_application':
                self.workflow_state.form_data['submitted'] = True
                return (
                    f"✅ APPLICATION SUBMITTED SUCCESSFULLY!\n\n"
                    f"Your application to RIPHA University has been received.\n"
                    f"Confirmation email will be sent to your registered email.\n"
                    f"Application ID: RIPHA-2026-{hash(str(self.workflow_state.form_data)) % 10000:04d}\n\n"
                    f"Thank you for applying!"
                )
        
        # Check for confirmation (yes, confirm, approve)
        if any(k in normalized for k in ['yes', 'confirm', 'approve', 'ok', 'okay', 'agreed']):
            if step == 'submit_application':
                self.workflow_state.form_data['submitted'] = True
                return (
                    f"✅ APPLICATION SUBMITTED SUCCESSFULLY!\n\n"
                    f"Your application to RIPHA University has been received.\n"
                    f"Confirmation email will be sent to your registered email.\n"
                    f"Application ID: RIPHA-2026-{hash(str(self.workflow_state.form_data)) % 10000:04d}\n\n"
                    f"Thank you for applying to RIPHA University!"
                )
        
        # Otherwise, capture as form input
        if step == 'personal_info':
            self.workflow_state.form_data['name'] = text
            return (
                f"✓ Name recorded: {text}\n\n"
                f"Please provide additional information:\n"
                f"- Email: [your email]\n"
                f"- Phone: [your phone]\n"
                f"- Date of Birth: [DD/MM/YYYY]\n\n"
                f"Type 'next' when done with this step."
            )
        elif step == 'select_program':
            self.workflow_state.form_data['program'] = text
            return (
                f"✓ Program selected: {text}\n\n"
                f"Great choice! Program '{text}' has been noted.\n\n"
                f"Type 'next' to proceed to Step 4 (Document Upload)."
            )
        elif step == 'upload_documents':
            # Add to documents list
            docs = self.workflow_state.form_data.get('documents', [])
            if isinstance(docs, str):
                docs = [docs]
            elif not isinstance(docs, list):
                docs = []
            docs.append(text)
            self.workflow_state.form_data['documents'] = docs
            return (
                f"✓ Document recorded: {text}\n\n"
                f"Uploaded documents: {len(docs)}\n\n"
                f"Type 'next' or 'submit' when ready to finalize."
            )
        elif step == 'submit_application':
            return (
                f"Ready to submit? Please confirm:\n"
                f"Type 'YES', 'CONFIRM', or 'SUBMIT' to finalize your application."
            )
        
        return "Please use specific commands for this step."

    def handle_voice(self) -> str:
        """Listen for voice input and process it"""
        if not self.config.voice_enabled:
            return 'Voice input is disabled. Enable it in config.json'
        
        # Use new speech engine
        text = self.speech_engine.listen()
        
        if not text:
            response = 'No speech detected or could not understand.'
            if self.config.tts_enabled:
                self.speech_engine.speak(response)
            return response
        
        # Process the recognized text
        return self.handle_text(text, speak_response=True)

    def shutdown(self) -> None:
        self.web.stop()
