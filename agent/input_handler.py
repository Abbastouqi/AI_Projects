from __future__ import annotations

import re
import os
from dataclasses import dataclass
from typing import Dict, Optional

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover - optional dependency
    sr = None


@dataclass
class Command:
    intent: str
    raw_text: str
    slots: Dict[str, str]


class VoiceTextInputHandler:
    def __init__(self, voice_enabled: bool = False) -> None:
        self.voice_enabled = voice_enabled and sr is not None
        self._recognizer = sr.Recognizer() if self.voice_enabled else None

    def listen_for_voice(self) -> Optional[str]:
        if not self.voice_enabled or sr is None:
            return None

        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self._recognizer.listen(source)

        try:
            return self._recognizer.recognize_google(audio)
        except Exception:
            return None

    def _extract_url(self, text: str) -> Optional[str]:
        url_pattern = r'https?://[^\s]+'
        match = re.search(url_pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).rstrip('.,;:!?)')
        
        www_pattern = r'www\.[^\s]+'
        match = re.search(www_pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).rstrip('.,;:!?)')
        
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
        match = re.search(domain_pattern, text, re.IGNORECASE)
        if match:
            domain = match.group(0)
            if '.' in domain:
                return domain
        
        return None

    def parse_command(self, text: str) -> Command:
        normalized = text.strip().lower()
        slots: Dict[str, str] = {}

        # System commands
        if any(k in normalized for k in ['shutdown', 'turn off', 'power off']):
            intent = 'system_command'
            slots['type'] = 'shutdown'
        elif any(k in normalized for k in ['restart', 'reboot']):
            intent = 'system_command'
            slots['type'] = 'restart'
        elif any(k in normalized for k in ['sleep', 'hibernate']):
            intent = 'system_command'
            slots['type'] = 'sleep'
        
        # Open applications
        elif 'open notepad' in normalized or 'notepad' in normalized:
            intent = 'open_application'
            slots['app'] = 'notepad'
        elif 'open calculator' in normalized or 'calculator' in normalized or 'calc' in normalized:
            intent = 'open_application'
            slots['app'] = 'calculator'
        elif 'open paint' in normalized:
            intent = 'open_application'
            slots['app'] = 'paint'
        elif 'open chrome' in normalized:
            intent = 'open_application'
            slots['app'] = 'chrome'
        elif 'open edge' in normalized:
            intent = 'open_application'
            slots['app'] = 'edge'
        elif 'open explorer' in normalized or 'file explorer' in normalized:
            intent = 'open_application'
            slots['app'] = 'explorer'
        elif 'open cmd' in normalized or 'command prompt' in normalized:
            intent = 'open_application'
            slots['app'] = 'cmd'
        elif 'open powershell' in normalized:
            intent = 'open_application'
            slots['app'] = 'powershell'
        elif 'open word' in normalized:
            intent = 'open_application'
            slots['app'] = 'word'
        elif 'open excel' in normalized:
            intent = 'open_application'
            slots['app'] = 'excel'
        
        # Search
        elif any(k in normalized for k in ['search for', 'search', 'google', 'find']) and not self._extract_url(text):
            intent = 'search'
            # Extract search query
            for prefix in ['search for ', 'search ', 'google ', 'find ']:
                if prefix in normalized:
                    slots['query'] = text[text.lower().find(prefix) + len(prefix):].strip()
                    break
        
        # Auto-fill form (automatic detection)
        elif any(k in normalized for k in ['auto fill', 'autofill', 'fill this form', 'fill the form', 'detect form', 'smart fill']):
            intent = 'auto_fill_form'
        # Fill form - specific field with value
        elif 'fill' in normalized and 'with' in normalized:
            intent = 'fill_form'
            # Extract field and value from "fill [field] with [value]" - preserve original case for value
            match = re.search(r'fill\s+(.+?)\s+with\s+(.+)', text, re.IGNORECASE)
            if match:
                slots['field'] = match.group(1).strip().lower()
                slots['value'] = match.group(2).strip()  # Keep original case
        # Fill form - general
        elif any(k in normalized for k in ['fill form', 'fill out', 'complete form', 'enter data', 'fill all']):
            intent = 'fill_form'
            if 'fill all' in normalized:
                slots['action'] = 'fill_all'
        # Click submit button
        elif any(k in normalized for k in ['click submit', 'submit form', 'send form', 'submit']):
            intent = 'fill_form'
            slots['action'] = 'submit'
        # Press enter
        elif 'press enter' in normalized or 'hit enter' in normalized:
            intent = 'fill_form'
            slots['action'] = 'enter'
        # Type text
        elif normalized.startswith('type '):
            intent = 'fill_form'
            slots['action'] = 'type'
            slots['value'] = text[5:].strip()  # Get text after "type "
        
        # File operations
        elif 'open file' in normalized or 'open folder' in normalized:
            intent = 'file_operation'
            slots['operation'] = 'open'
        elif 'open downloads' in normalized:
            intent = 'file_operation'
            slots['operation'] = 'open'
            slots['path'] = os.path.expanduser('~/Downloads')
        elif 'open documents' in normalized:
            intent = 'file_operation'
            slots['operation'] = 'open'
            slots['path'] = os.path.expanduser('~/Documents')
        
        # Riphah-specific commands (keep existing)
        elif any(k in normalized for k in ['explore program', 'show program', 'available program', 'list program', 'what program', 'which program', 'programs offered', 'courses offered']):
            intent = 'explore_programs'
        elif any(k in normalized for k in ['admission date', 'deadline', 'important date', 'when to apply', 'application date', 'test date', 'enrollment date']):
            intent = 'admission_dates'
        elif any(k in normalized for k in ['personal', 'information', 'name', 'email', 'phone', 'date of birth', 'address', 'enter info', 'sign up', 'signup', 'new applicant', 'register', 'create account']):
            intent = 'admissions_apply'
            slots['step'] = 'personal_info'
        elif any(k in normalized for k in ['program', 'course', 'degree', 'select', 'choose']):
            intent = 'admissions_apply'
            slots['step'] = 'select_program'
        elif any(k in normalized for k in ['document', 'upload', 'file', 'mark sheet', 'certificate', 'proof']):
            intent = 'admissions_apply'
            slots['step'] = 'upload_documents'
        elif any(k in normalized for k in ['submit application', 'confirm', 'send application', 'final step', 'finalize', 'complete']):
            intent = 'admissions_apply'
            slots['step'] = 'submit_application'
        elif any(k in normalized for k in ['admission', 'apply', 'application', 'applicant', 'enroll', 'riphah']):
            intent = 'admissions_apply'
        elif any(k in normalized for k in ['policy', 'policies', 'rules', 'guideline']):
            intent = 'policy_lookup'
        
        # URL opening (keep at end as fallback)
        elif any(k in normalized for k in ['open', 'website', 'browser', 'go to', 'navigate', 'visit']):
            intent = 'open_url'
            url = self._extract_url(text)
            if url:
                slots['url'] = url
        else:
            intent = 'unknown'
            url = self._extract_url(text)
            if url:
                intent = 'open_url'
                slots['url'] = url

        return Command(intent=intent, raw_text=text, slots=slots)
