#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI PC Agent - Entry Point
Run this file to start the agent
"""

import sys
import os

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import argparse
from core.agent import PCAgent
from core.gui import AgentGUI

def main():
    parser = argparse.ArgumentParser(description='AI PC Agent')
    parser.add_argument('--mode', choices=['cli', 'gui'], default='gui',
                       help='Run mode: cli (command line) or gui (graphical)')
    parser.add_argument('--voice', action='store_true', 
                       help='Start in voice mode (CLI only)')
    args = parser.parse_args()
    
    print("🤖 AI PC Agent Starting...")
    
    agent = PCAgent()
    agent.start()
    
    if args.mode == 'gui':
        print("🖥️  Launching GUI...")
        gui = AgentGUI(agent)
        gui.run()
    else:
        # CLI Mode
        if args.voice:
            agent.listen_and_execute()
        else:
            print("\nType 'voice' for voice input, 'quit' to exit")
            while True:
                mode = input("\nMode (text/voice/quit): ").lower().strip()
                if mode == "quit":
                    agent.stop()
                    break
                elif mode == "voice":
                    agent.listen_and_execute()
                elif mode == "text":
                    cmd = input("Command: ")
                    result = agent.process_command(cmd)
                    print(f"Result: {result}")
                else:
                    print("Invalid mode. Use: text, voice, quit")

if __name__ == "__main__":
    main()
