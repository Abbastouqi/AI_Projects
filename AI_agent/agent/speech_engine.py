"""Enhanced speech engine with speech-to-text and text-to-speech"""
from __future__ import annotations

import threading
from typing import Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class SpeechEngine:
    """Handles both speech recognition (STT) and text-to-speech (TTS)"""
    
    def __init__(self, enabled: bool = False, tts_enabled: bool = False) -> None:
        self.stt_enabled = enabled and sr is not None
        self.tts_enabled = tts_enabled and pyttsx3 is not None
        
        # Initialize speech recognizer
        self._recognizer = sr.Recognizer() if self.stt_enabled else None
        
        # Initialize text-to-speech engine
        self._tts_engine = None
        if self.tts_enabled:
            try:
                self._tts_engine = pyttsx3.init()
                self._configure_tts()
            except Exception:
                self.tts_enabled = False
                self._tts_engine = None
    
    def _configure_tts(self) -> None:
        """Configure text-to-speech settings"""
        if not self._tts_engine:
            return
        
        # Set properties
        self._tts_engine.setProperty('rate', 175)  # Speed (words per minute)
        self._tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Try to set a good voice
        voices = self._tts_engine.getProperty('voices')
        if voices:
            # Prefer female voice if available, otherwise use first voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self._tts_engine.setProperty('voice', voice.id)
                    break
            else:
                self._tts_engine.setProperty('voice', voices[0].id)
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for speech input and convert to text
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Recognized text or None if failed
        """
        if not self.stt_enabled or sr is None:
            return None
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (speak now)")
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing speech...")
            # Use Google's free speech recognition API
            text = self._recognizer.recognize_google(audio)
            print(f"✓ Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected (timeout)")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def speak(self, text: str, async_mode: bool = False) -> None:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            async_mode: If True, speak in background thread
        """
        if not self.tts_enabled or not self._tts_engine:
            return
        
        if async_mode:
            threading.Thread(target=self._speak_sync, args=(text,), daemon=True).start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str) -> None:
        """Synchronous speech (internal use)"""
        try:
            # Clean text for better speech
            clean_text = self._clean_text_for_speech(text)
            self._tts_engine.say(clean_text)
            self._tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text to make it more speech-friendly"""
        # Remove emojis and special characters that don't speak well
        import re
        
        # Remove URLs
        text = re.sub(r'https?://\S+', 'website link', text)
        
        # Remove emojis (basic cleanup)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", 
            flags=re.UNICODE
        )
        text = emoji_pattern.sub('', text)
        
        # Replace common symbols
        replacements = {
            '✓': 'check',
            '✅': 'success',
            '❌': 'error',
            '🎓': '',
            '📋': '',
            '📚': '',
            '📅': '',
            '🔗': '',
            '💡': '',
            '•': '',
            '→': 'then',
            '&': 'and',
        }
        
        for symbol, replacement in replacements.items():
            text = text.replace(symbol, replacement)
        
        # Clean up extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def test_microphone(self) -> bool:
        """Test if microphone is available"""
        if not self.stt_enabled or sr is None:
            return False
        
        try:
            with sr.Microphone() as source:
                return True
        except Exception:
            return False
    
    def list_microphones(self) -> list:
        """List available microphones"""
        if not sr:
            return []
        
        try:
            return sr.Microphone.list_microphone_names()
        except Exception:
            return []
    
    def get_status(self) -> dict:
        """Get status of speech engine"""
        return {
            'stt_enabled': self.stt_enabled,
            'tts_enabled': self.tts_enabled,
            'microphone_available': self.test_microphone() if self.stt_enabled else False,
            'available_microphones': self.list_microphones() if self.stt_enabled else []
        }
