"""
Simple test to check if Chrome browser automation works
"""
import sys
import os

# Add agent to path
sys.path.insert(0, os.path.dirname(__file__))

from agent.browser import run_browser_persistent

def test_browser():
    print("=" * 60)
    print("TESTING CHROME BROWSER AUTOMATION")
    print("=" * 60)
    print()
    
    try:
        print("🔄 Attempting to launch Chrome...")
        driver = run_browser_persistent(
            user_data_dir="./test_browser_profile",
            headless=False
        )
        
        print("✅ Chrome launched successfully!")
        print(f"✅ Browser title: {driver.title}")
        
        print("\n🔄 Testing navigation to Google...")
        driver.get("https://www.google.com")
        print(f"✅ Navigated to: {driver.current_url}")
        print(f"✅ Page title: {driver.title}")
        
        print("\n🔄 Waiting 3 seconds...")
        import time
        time.sleep(3)
        
        print("🔄 Closing browser...")
        driver.quit()
        print("✅ Browser closed successfully!")
        
        print("\n" + "=" * 60)
        print("✅ BROWSER AUTOMATION TEST PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Browser test failed: {e}")
        print("\n" + "=" * 60)
        print("❌ BROWSER AUTOMATION TEST FAILED")
        print("=" * 60)
        print("\nPossible solutions:")
        print("1. Update Chrome: https://www.google.com/chrome/")
        print("2. Close all Chrome windows and try again")
        print("3. Delete browser profile: rmdir /s /q test_browser_profile")
        return False

if __name__ == "__main__":
    success = test_browser()
    sys.exit(0 if success else 1)
