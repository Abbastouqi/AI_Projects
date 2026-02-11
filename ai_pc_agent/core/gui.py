"""
GUI for AI Agent using Tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentGUI:
    def __init__(self, agent):
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("🤖 AI PC Agent")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        self.is_listening = False
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="AI PC Agent", font=('Helvetica', 20, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Input
        input_frame = tk.LabelFrame(self.root, text="Command", font=('Helvetica', 12), 
                                   bg='#f0f0f0', padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.input_var = tk.StringVar()
        entry = ttk.Entry(input_frame, textvariable=self.input_var, font=('Helvetica', 11))
        entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        entry.bind('<Return>', lambda e: self.send_command())
        
        ttk.Button(input_frame, text="🎤 Voice", command=self.toggle_voice).pack(side=tk.LEFT, padx=2)
        ttk.Button(input_frame, text="Send", command=self.send_command).pack(side=tk.LEFT, padx=2)
        
        # Log
        log_frame = tk.LabelFrame(self.root, text="Conversation", font=('Helvetica', 12), 
                                 bg='#f0f0f0', padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                 font=('Consolas', 10), bg='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X)
        
        # Quick buttons
        quick = tk.Frame(self.root, bg='#f0f0f0')
        quick.pack(fill=tk.X, padx=20, pady=10)
        
        actions = [
            ("Search", "Search for Python tutorials"),
            ("Chrome", "Open Chrome browser"),
            ("Document", "Create document notes.txt containing Meeting notes"),
            ("Policy", "Search for university admission policy")
        ]
        
        for text, cmd in actions:
            ttk.Button(quick, text=text, command=lambda c=cmd: self.quick_cmd(c)).pack(side=tk.LEFT, padx=5)
    
    def log(self, sender, msg, msg_type="normal"):
        self.log_text.config(state=tk.NORMAL)
        time = datetime.now().strftime("%H:%M:%S")
        
        tag = msg_type
        self.log_text.tag_config("user", foreground="#0066cc")
        self.log_text.tag_config("agent", foreground="#009900")
        self.log_text.tag_config("system", foreground="#666666")
        
        self.log_text.insert(tk.END, f"[{time}] {sender}: {msg}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def send_command(self):
        cmd = self.input_var.get().strip()
        if not cmd:
            return
        self.input_var.set("")
        self.log("You", cmd, "user")
        
        threading.Thread(target=self._process, args=(cmd,), daemon=True).start()
    
    def _process(self, cmd):
        self.status_var.set("Processing...")
        try:
            logger.info(f"GUI Processing command: {cmd}")
            result = self.agent.process_command(cmd)
            logger.info(f"GUI Got result: {result}")
            
            if result['success']:
                response = f"✅ {result['intent']}\n"
                result_text = result.get('result', '')
                if isinstance(result_text, str):
                    response += result_text[:500]
                else:
                    response += str(result_text)[:500]
            else:
                response = f"❌ Error: {result.get('error', 'Unknown')}\n"
                response += str(result.get('suggestion', ''))[:200]
            
            logger.info(f"GUI Display response: {response}")
            self.root.after(0, lambda: self.log("Agent", response, "agent"))
        except Exception as e:
            logger.exception(f"GUI Error: {e}")
            self.root.after(0, lambda: self.log("Agent", f"Error: {str(e)}", "agent"))
        
        self.status_var.set("Ready")
    
    def toggle_voice(self):
        if not self.is_listening:
            self.is_listening = True
            self.log("System", "Voice mode on - Speak now", "system")
            threading.Thread(target=self._voice_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.log("System", "Voice mode off", "system")
    
    def _voice_loop(self):
        while self.is_listening:
            try:
                cmd = self.agent.voice_handler.listen(timeout=5)
                if cmd:
                    self.root.after(0, lambda c=cmd: self.log("You", c, "user"))
                    result = self.agent.process_command(cmd)
                    response = "Done" if result['success'] else "Failed"
                    self.root.after(0, lambda r=response: self.log("Agent", r, "agent"))
                    self.agent.voice_handler.speak(response)
            except:
                pass
    
    def quick_cmd(self, cmd):
        self.input_var.set(cmd)
        self.send_command()
    
    def run(self):
        self.log("System", "Agent ready! Type commands or use voice.", "system")
        self.root.mainloop()

if __name__ == "__main__":
    from core.agent import PCAgent
    agent = PCAgent()
    agent.start()
    gui = AgentGUI(agent)
    gui.run()
