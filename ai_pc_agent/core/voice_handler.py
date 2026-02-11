"""
Voice Input/Output Handler
Handles speech recognition and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Calibrate for ambient noise
        with self.microphone as source:
            print("🎙️ Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Calibration complete")
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("👂 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
            print("🧠 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"🚨 Speech recognition error: {e}")
            return None
    
    def speak(self, text: str):
        """Convert text to speech"""
        try:
            print(f"🗣️ Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"[AGENT]: {text}")

if __name__ == "__main__":
    vh = VoiceHandler()
    print("Say something...")
    text = vh.listen()
    if text:
        vh.speak(f"You said: {text}")
