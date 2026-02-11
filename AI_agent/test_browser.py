"""Test script to verify browser automation works"""
import sys
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    print("="*70)
    print("🧪 Testing Browser Automation")
    print("="*70)
    
    # Setup Chrome options
    options = ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    print("\n1. Setting up ChromeDriver...")
    
    try:
        # Try with webdriver-manager
        driver_path = ChromeDriverManager().install()
        print(f"   ✅ ChromeDriver installed at: {driver_path}")
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
    except Exception as e:
        print(f"   ⚠️ ChromeDriver manager failed: {e}")
        print("   Trying system Chrome...")
        driver = webdriver.Chrome(options=options)
    
    print("   ✅ Browser opened successfully!")
    
    print("\n2. Testing navigation...")
    driver.get("https://www.google.com")
    print(f"   ✅ Navigated to: {driver.current_url}")
    print(f"   ✅ Page title: {driver.title}")
    
    print("\n3. Waiting 3 seconds...")
    time.sleep(3)
    
    print("\n4. Testing Riphah portal...")
    driver.get("https://admissions.riphah.edu.pk/riphah_demo/public/Student/application/List")
    print(f"   ✅ Navigated to: {driver.current_url}")
    print(f"   ✅ Page title: {driver.title}")
    
    print("\n5. Waiting 5 seconds for you to see the browser...")
    time.sleep(5)
    
    print("\n6. Closing browser...")
    driver.quit()
    print("   ✅ Browser closed")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\nBrowser automation is working correctly!")
    print("The Riphah Auto-Apply feature should work now.")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Make sure Chrome is installed")
    print("2. Install dependencies: pip install selenium webdriver-manager")
    print("3. Check if Chrome is in PATH")
    sys.exit(1)
