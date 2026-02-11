"""
AI PC Agent - ENHANCED Main Controller
Better integration between voice/text and automation
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any
import threading
import queue
import os

from core.voice_handler import VoiceHandler
from core.intent_parser import IntentParser
from skills.web_automation import WebAutomation
from skills.system_control import SystemControl
from skills.document_handler import DocumentHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PCAgent:
    def __init__(self):
        self.voice_handler = VoiceHandler()
        self.intent_parser = IntentParser()
        self._web_auto = None  # Lazy initialization
        self.system = SystemControl()
        self.documents = DocumentHandler()
        
        self.command_queue = queue.Queue()
        self.is_running = False
        self.applicant_profile = {}  # Store user info for forms
        
        # Enhanced skills registry
        self.skills = {
            'apply_admission': self._handle_admission,
            'search_policy': self._handle_policy_search,
            'open_application': self.system.open_application,
            'create_document': self.documents.create_document,
            'read_email': self._handle_read_email,
            'schedule_task': self.system.schedule_task,
            'search_web': self._handle_search_web,
            'fill_form': self._handle_form_filling,
            'submit_form': self._handle_submit_form,
            'set_profile': self._set_applicant_profile,
            'show_profile': self._show_profile
        }
    
    @property
    def web_auto(self):
        """Lazy initialization of WebAutomation"""
        if self._web_auto is None:
            logger.info("Initializing WebAutomation...")
            self._web_auto = WebAutomation(headless=False)
        return self._web_auto
    
    def start(self):
        """Start the agent"""
        self.is_running = True
        logger.info("🤖 AI Agent started with FULL AUTOMATION")
        print("\n" + "="*50)
        print("🎯 AI PC Agent Ready!")
        print("="*50)
        print("Available commands:")
        print("  • 'Apply for admission to [University]' - Auto-fills application")
        print("  • 'Set my profile' - Save your info for auto-fill")
        print("  • 'Search policy for [topic]' - Find university policies")
        print("  • 'Fill form at [URL]' - Auto-fill any form")
        print("  • 'Open [application]' - Open desktop apps")
        print("  • 'voice' | 'text' | 'quit'")
        print("="*50)
    
    def _handle_admission(self, **params):
        """Handle admission with profile data"""
        # Merge saved profile with current params
        full_data = {**self.applicant_profile, **params}
        return self.web_auto.apply_admission(**full_data, applicant_data=full_data)
    
    def _handle_policy_search(self, **params):
        """Enhanced policy search"""
        return self.web_auto.search_policy(**params)
    
    def _handle_form_filling(self, **params):
        """Handle form filling with profile"""
        full_data = {**self.applicant_profile, **params.get('form_data', {})}
        return self.web_auto.fill_form_generic(form_data=full_data, **params)
    
    def _handle_read_email(self, **params):
        """Handle email reading"""
        return self.web_auto.check_email(**params)
    
    def _handle_search_web(self, **params):
        """Handle web search"""
        return self.web_auto.search_information(**params)
    
    def _handle_submit_form(self, **params):
        """Handle form submission"""
        return self.web_auto.submit_form(**params)
    
    def _set_applicant_profile(self, **kwargs):
        """Interactive profile setup"""
        print("\n📝 Setting up your applicant profile...")
        print("(This information will be used to auto-fill applications)")
        
        fields = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Street Address',
            'city': 'City',
            'state': 'State/Province',
            'zip': 'ZIP/Postal Code',
            'country': 'Country',
            'high_school': 'Current School',
            'graduation_year': 'Expected Graduation Year'
        }
        
        for key, label in fields.items():
            if key not in self.applicant_profile:
                value = input(f"{label}: ").strip()
                if value:
                    self.applicant_profile[key] = value
        
        # Save to file
        profile_path = "config/applicant_profile.json"
        os.makedirs("config", exist_ok=True)
        with open(profile_path, 'w') as f:
            json.dump(self.applicant_profile, f, indent=2)
        
        return {
            'status': 'success',
            'message': 'Profile saved successfully',
            'fields_saved': len(self.applicant_profile),
            'path': profile_path
        }
    
    def _show_profile(self, **kwargs):
        """Display current profile"""
        if not self.applicant_profile:
            return {
                'status': 'info',
                'message': 'No profile set. Say "Set my profile" to add your information.'
            }
        return {
            'status': 'success',
            'profile': self.applicant_profile,
            'message': f'Profile has {len(self.applicant_profile)} fields'
        }
    
    def process_command(self, command: str, input_type: str = "text") -> Dict[str, Any]:
        """Process a command with better error handling"""
        try:
            # Parse intent
            intent_data = self.intent_parser.parse(command)
            logger.info(f"🎯 Intent detected: {intent_data['intent']} (confidence: {intent_data['confidence']:.2f})")
            
            skill_name = intent_data.get('intent')
            parameters = intent_data.get('parameters', {})
            
            # Special handling for profile setup
            if 'profile' in command.lower() and 'set' in command.lower():
                skill_name = 'set_profile'
            
            if skill_name in self.skills:
                print(f"⚙️  Executing: {skill_name}")
                result = self.skills[skill_name](**parameters)
                
                # Format result for display
                formatted_result = self._format_result(result)
                
                return {
                    'success': True,
                    'intent': skill_name,
                    'result': formatted_result,
                    'raw_result': result,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f"I don't know how to: {skill_name}",
                    'suggestion': "Try: 'Apply for admission', 'Search policy', 'Open Chrome', 'Set my profile'",
                    'available_commands': list(self.skills.keys())
                }
                
        except Exception as e:
            logger.error(f"❌ Error processing command: {e}")
            return {
                'success': False,
                'error': str(e),
                'troubleshooting': 'Check internet connection and try again'
            }
    
    def _format_result(self, result: Dict) -> str:
        """Format automation result for user-friendly display"""
        if isinstance(result, dict):
            lines = []
            for key, value in result.items():
                if key == 'status':
                    emoji = '✅' if value == 'success' else '⚠️' if value == 'partial' else '❌'
                    lines.append(f"{emoji} Status: {value.upper()}")
                elif isinstance(value, list):
                    lines.append(f"📋 {key.replace('_', ' ').title()}: {len(value)} items")
                    for item in value[:5]:  # Show max 5
                        lines.append(f"   • {str(item)[:80]}")
                elif isinstance(value, dict):
                    lines.append(f"📊 {key.replace('_', ' ').title()}:")
                    for k, v in value.items():
                        lines.append(f"   • {k}: {str(v)[:60]}")
                else:
                    lines.append(f"📌 {key.replace('_', ' ').title()}: {str(value)[:100]}")
            return "\n".join(lines)
        return str(result)
    
    def listen_and_execute(self):
        """Voice command loop with feedback"""
        print("\n🎤 Voice Mode Active - Speak clearly...")
        print("Say 'stop' to end, 'help' for commands")
        
        while self.is_running:
            try:
                command = self.voice_handler.listen(timeout=6)
                if command:
                    if 'stop' in command.lower():
                        self.voice_handler.speak("Voice mode deactivated")
                        break
                    if 'help' in command.lower():
                        help_text = "Available commands: apply for admission, search policy, open application, set profile, fill form"
                        self.voice_handler.speak(help_text)
                        continue
                    
                    print(f"📢 Heard: {command}")
                    result = self.process_command(command, "voice")
                    
                    if result['success']:
                        response = f"Task completed: {result['intent']}. {result['result'][:100]}"
                    else:
                        response = f"Error: {result.get('error', 'Unknown error')}"
                    
                    print(f"🗣️  Response: {response}")
                    self.voice_handler.speak(response)
                    
            except Exception as e:
                print(f"❌ Voice error: {e}")
    
    def stop(self):
        """Cleanup and stop"""
        self.is_running = False
        self.web_auto.cleanup()
        logger.info("Agent stopped")

if __name__ == "__main__":
    agent = PCAgent()
    agent.start()
    
    while True:
        try:
            mode = input("\nMode (voice/text/quit): ").lower().strip()
            if mode == "quit":
                agent.stop()
                break
            elif mode == "voice":
                agent.listen_and_execute()
            elif mode == "text":
                cmd = input("Command: ")
                result = agent.process_command(cmd)
                print("\n" + "="*50)
                print("RESULT:")
                print("="*50)
                print(json.dumps(result, indent=2, default=str))
            else:
                print("Invalid mode. Use: voice, text, quit")
        except KeyboardInterrupt:
            print("\n\nStopping agent...")
            agent.stop()
            break