from __future__ import annotations

import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_browser_persistent(user_data_dir: str, headless: bool = False):
    """
    Launch a persistent Chrome session using Selenium.
    This keeps cookies/session across runs.
    """
    profile_dir = os.path.abspath(user_data_dir or "./browser_profile")
    
    # Create fresh profile directory
    os.makedirs(profile_dir, exist_ok=True)
    
    # Clean up any lock files that might cause issues
    lock_file = os.path.join(profile_dir, "SingletonLock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except Exception:
            pass

    options = ChromeOptions()
    
    # Basic Chrome options
    if headless:
        options.add_argument("--headless=new")
    
    # Profile and window settings
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument("--start-maximized")
    
    # Stability options
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    
    # Anti-detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Prevent crashes
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-in-process-stack-traces")
    options.add_argument("--log-level=3")
    
    # Set user agent to avoid detection
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

    try:
        # Try to get ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"⚠️ ChromeDriver error: {e}")
        print("Trying alternative approach...")
        
        # Try without service specification
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e2:
            print(f"❌ Failed to start Chrome: {e2}")
            raise RuntimeError(
                f"Could not start Chrome browser. Please ensure:\n"
                f"1. Chrome is installed and up to date\n"
                f"2. ChromeDriver is compatible with your Chrome version\n"
                f"3. No other Chrome instances are using the profile\n"
                f"Original error: {e}"
            )
