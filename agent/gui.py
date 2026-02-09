from __future__ import annotations

import threading
import tkinter as tk
from tkinter import scrolledtext

from agent.controller import AgentController


class AgentGUI:
    def __init__(self, controller: AgentController) -> None:
        self.controller = controller
        self.root = tk.Tk()
        self.root.title('AI Assistant Agent')
        self.root.geometry('720x420')

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Status bar at top
        status_frame = tk.Frame(frame)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        status = self.controller.speech_engine.get_status()
        status_text = []
        if status['stt_enabled']:
            status_text.append('🎤 Voice Input: ON')
        if status['tts_enabled']:
            status_text.append('🔊 Voice Output: ON')
        if not status_text:
            status_text.append('⌨️ Text Mode Only')
        
        self.status_label = tk.Label(
            status_frame, 
            text=' | '.join(status_text),
            fg='green' if status_text else 'gray'
        )
        self.status_label.pack(side=tk.LEFT)

        self.log = scrolledtext.ScrolledText(frame, height=18)
        self.log.pack(fill=tk.BOTH, expand=True)

        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill=tk.X, pady=8)

        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self._on_send)

        send_btn = tk.Button(entry_frame, text='Send', command=self._on_send)
        send_btn.pack(side=tk.LEFT, padx=6)

        voice_btn = tk.Button(
            entry_frame, 
            text='🎤 Voice', 
            command=self._on_voice,
            state=tk.NORMAL if self.controller.config.voice_enabled else tk.DISABLED
        )
        voice_btn.pack(side=tk.LEFT, padx=2)
        
        # Test speech button
        if self.controller.config.tts_enabled:
            test_btn = tk.Button(
                entry_frame,
                text='🔊 Test',
                command=self._on_test_speech
            )
            test_btn.pack(side=tk.LEFT, padx=2)

    def _append_log(self, message: str) -> None:
        self.log.insert(tk.END, message + '\n')
        self.log.see(tk.END)

    def _on_send(self, _event=None) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self._append_log(f'You: {text}')
        
        # Check if user wants speech output
        speak = self.controller.config.tts_enabled
        response = self.controller.handle_text(text, speak_response=speak)
        self._append_log(f'Agent: {response}')

    def _on_voice(self) -> None:
        def worker() -> None:
            self._append_log('🎤 Listening...')
            response = self.controller.handle_voice()
            self._append_log(f'Agent: {response}')

        threading.Thread(target=worker, daemon=True).start()
    
    def _on_test_speech(self) -> None:
        """Test text-to-speech functionality"""
        test_message = "Hello! I am your Riphah University admission assistant. Speech is working correctly."
        self._append_log('🔊 Testing speech output...')
        self.controller.speech_engine.speak(test_message)
        self._append_log('Agent: ' + test_message)

    def run(self) -> None:
        self.root.mainloop()
