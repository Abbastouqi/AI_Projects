"""Full end-to-end test of all features"""
import sys
import time
sys.path.insert(0, '.')

from agent.config import load_config
from agent.controller import AgentController

print("="*70)
print("🧪 FULL FEATURE TEST")
print("="*70)

# Load config
config = load_config()
print(f"\n✅ Config: headless={config.selenium_headless}, tts={config.tts_enabled}")

# Initialize
controller = AgentController(config)
print("✅ Controller initialized\n")

# Test 1: Open Calculator
print("TEST 1: Open Calculator")
print("-"*70)
response = controller.handle_text("open calculator")
print(f"Response: {response[:100]}...")
time.sleep(2)

# Test 2: Search Google
print("\nTEST 2: Search Google")
print("-"*70)
response = controller.handle_text("search python tutorial")
print(f"Response: {response[:100]}...")
print("⏳ Browser should open now... waiting 5 seconds")
time.sleep(5)

# Test 3: Riphah Auto Apply
print("\nTEST 3: Riphah Auto Apply")
print("-"*70)
print("⏳ This will open browser and navigate to Riphah portal...")
response = controller.handle_text("riphah auto apply")
print(f"\nResponse:\n{response}")
print("\n⏳ Browser should be open now... waiting 10 seconds")
print("   Check if you can see Chrome window with Riphah portal!")
time.sleep(10)

# Test 4: Auto Fill (if form is open)
print("\nTEST 4: Auto Fill")
print("-"*70)
response = controller.handle_text("auto fill")
print(f"Response: {response[:200]}...")
time.sleep(3)

print("\n" + "="*70)
print("✅ ALL TESTS COMPLETE!")
print("="*70)
print("\nDid you see:")
print("  1. Calculator open? (should have opened)")
print("  2. Chrome browser open? (should have opened)")
print("  3. Riphah portal loaded? (should be visible)")
print("  4. Form fields filled? (if form was present)")

# Cleanup
print("\n⏳ Cleaning up in 5 seconds...")
time.sleep(5)
controller.shutdown()
print("✅ Done!")
