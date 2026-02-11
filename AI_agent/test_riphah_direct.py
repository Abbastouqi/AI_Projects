"""Direct test of Riphah auto-apply functionality"""
import sys
sys.path.insert(0, '.')

from agent.config import load_config
from agent.controller import AgentController

print("="*70)
print("🎓 Testing Riphah Auto-Apply")
print("="*70)

# Load config
print("\n1. Loading configuration...")
config = load_config()
print(f"   ✅ Config loaded")
print(f"   - Headless: {config.selenium_headless}")
print(f"   - TTS: {config.tts_enabled}")

# Initialize controller
print("\n2. Initializing controller...")
controller = AgentController(config)
print("   ✅ Controller initialized")

# Test the command
print("\n3. Executing 'riphah auto apply' command...")
print("   (Browser should open now...)")
response = controller.handle_text("riphah auto apply", speak_response=False)

print("\n4. Response received:")
print("-"*70)
print(response)
print("-"*70)

print("\n5. Keeping browser open for 10 seconds...")
print("   Check if the browser opened and navigated to Riphah portal!")
import time
time.sleep(10)

print("\n6. Cleaning up...")
controller.shutdown()
print("   ✅ Browser closed")

print("\n" + "="*70)
print("✅ TEST COMPLETE!")
print("="*70)
