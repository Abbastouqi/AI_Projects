"""
Intent Parser - Natural Language Understanding
Maps user commands to structured intents using keyword matching
"""

import re
from typing import Dict, Any
import json

class IntentParser:
    def __init__(self):
        self.intent_patterns = {
            'show_profile': {
                'keywords': ['show profile', 'display profile', 'my profile', 'view profile'],
                'parameters': [],
                'description': 'Display current user profile'
            },
            'set_profile': {
                'keywords': ['set profile', 'save profile', 'update profile', 'my info'],
                'parameters': [],
                'description': 'Set up and save your profile information'
            },
            'apply_admission': {
                'keywords': ['apply', 'admission', 'university', 'college', 'register', 'enroll'],
                'parameters': ['institution', 'program', 'name', 'email'],
                'description': 'Apply for admission to educational institutions'
            },
            'search_policy': {
                'keywords': ['policy', 'find policy', 'search policy', 'university policy', 'rules'],
                'parameters': ['topic', 'institution'],
                'description': 'Search for university or organizational policies'
            },
            'fill_form': {
                'keywords': ['fill form', 'complete form', 'submit form', 'enter data'],
                'parameters': ['form_type', 'url', 'data'],
                'description': 'Fill out online forms automatically'
            },
            'open_application': {
                'keywords': ['open', 'launch', 'start', 'run', 'application', 'program'],
                'parameters': ['app_name'],
                'description': 'Open desktop applications'
            },
            'search_web': {
                'keywords': ['search', 'google', 'find', 'look up', 'information about'],
                'parameters': ['query'],
                'description': 'Search the web for information'
            },
            'create_document': {
                'keywords': ['create document', 'write file', 'save document', 'new file'],
                'parameters': ['filename', 'content'],
                'description': 'Create and save documents'
            },
            'schedule_task': {
                'keywords': ['schedule', 'remind me', 'set reminder', 'calendar'],
                'parameters': ['task', 'time', 'date'],
                'description': 'Schedule tasks and reminders'
            },
            'read_email': {
                'keywords': ['check email', 'read mail', 'emails', 'inbox'],
                'parameters': ['filter'],
                'description': 'Check and read emails'
            }
        }
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse natural language command into structured intent"""
        text_lower = text.lower()
        
        # Score each intent based on keyword matches
        intent_scores = {}
        for intent_name, pattern in self.intent_patterns.items():
            score = 0
            for keyword in pattern['keywords']:
                if keyword in text_lower:
                    score += len(keyword.split())
            
            if score > 0:
                intent_scores[intent_name] = score
        
        if not intent_scores:
            return {
                'intent': 'unknown',
                'original_text': text,
                'parameters': {},
                'confidence': 0
            }
        
        # Select best matching intent
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 3, 1.0)
        
        # Extract parameters
        parameters = self._extract_parameters(best_intent, text)
        
        return {
            'intent': best_intent,
            'original_text': text,
            'parameters': parameters,
            'confidence': confidence,
            'description': self.intent_patterns[best_intent]['description']
        }
    
    def _extract_parameters(self, intent: str, text: str) -> Dict[str, Any]:
        """Extract parameters from text based on intent type"""
        params = {}
        text_lower = text.lower()
        
        if intent == 'apply_admission':
            # Extract university name - try multiple patterns
            # Pattern 1: "to/in/at [University/College Name] university/college"
            match = re.search(r'(?:to|for|at|in)\s+([a-zA-Z\s]+?)(?:\s+university|\s+college|$)', text, re.IGNORECASE)
            if match:
                uni_name = match.group(1).strip().title()
                if uni_name and len(uni_name) > 2:  # Ensure it's not too short
                    params['institution'] = uni_name
            
            # Pattern 2: If no match, try to get the last capitalized words
            if 'institution' not in params:
                match = re.search(r'(?:apply|admission|enroll|register).*?(?:to|in|at)\s+(.+?)$', text, re.IGNORECASE)
                if match:
                    uni_name = match.group(1).strip().title()
                    if 'university' in uni_name.lower() or 'college' in uni_name.lower():
                        params['institution'] = uni_name
                    elif len(uni_name) > 2:
                        params['institution'] = uni_name + ' University'
            
            # Extract program
            match = re.search(r'(?:for|in)\s+(\w+)\s+(?:program|degree|major)', text, re.IGNORECASE)
            if match:
                params['program'] = match.group(1)
                
        elif intent == 'search_policy':
            match = re.search(r'(?:about|regarding|for|on)\s+(\w+(?:\s+\w+){0,3})', text_lower)
            if match:
                params['topic'] = match.group(1)
                
        elif intent == 'open_application':
            apps = ['chrome', 'firefox', 'word', 'excel', 'notepad', 'calculator', 'outlook', 'powershell']
            for app in apps:
                if app in text_lower:
                    params['app_name'] = app
                    break
            if 'app_name' not in params:
                match = re.search(r'(?:open|launch|start)\s+(\w+)', text_lower)
                if match:
                    params['app_name'] = match.group(1)
                    
        elif intent == 'search_web':
            match = re.search(r'(?:search (?:web )?for|google|find|look up)\s+(.+?)(?:\s+please|$)', text_lower)
            if match:
                params['query'] = match.group(1).strip()
            else:
                # Fallback: take everything after the intent keyword
                match = re.search(r'(?:search|find|look)\s+(.+)', text_lower)
                if match:
                    params['query'] = match.group(1).strip()
                
        elif intent == 'create_document':
            match = re.search(r'(?:named|called|file)\s+([\w\.]+)', text_lower)
            if match:
                params['filename'] = match.group(1)
            else:
                params['filename'] = 'document.txt'
            
            match = re.search(r'(?:saying|with content|containing)\s+(.+)', text_lower)
            if match:
                params['content'] = match.group(1)
            else:
                params['content'] = 'Document created by AI Agent'
        
        return params

if __name__ == "__main__":
    parser = IntentParser()
    test = "Apply for admission to Harvard University for Computer Science"
    print(json.dumps(parser.parse(test), indent=2))
