"""Quick test - just open browser and Google"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🧪 Quick Browser Test")
print("="*50)

# Setup
options = ChromeOptions()
options.add_argument('--start-maximized')

# Open browser
print("Opening Chrome...")
driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# Go to Google
print("Going to Google...")
driver.get("https://www.google.com")
print(f"✅ Success! Page title: {driver.title}")

# Wait
print("Browser will stay open for 5 seconds...")
time.sleep(5)

# Close
print("Closing browser...")
driver.quit()
print("✅ Test complete!")
