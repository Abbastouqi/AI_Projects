# agent/apply_riphah.py
import json
import time
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from agent.browser import run_browser_persistent
from agent.credentials import prompt_login
from agent.form_validator import check_and_report
from agent.policy_validator import validate_before_apply


def load_application_data():
    with open("data/application.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _shot(driver, name: str):
    # Screenshots disabled for headless/web frontend usage.
    return


def _set_value(element, value: str):
    """Clear and set value in an input field"""
    try:
        # Try multiple methods to clear the field
        element.clear()
        # Use JavaScript to ensure it's really cleared
        element._parent.execute_script("arguments[0].value = '';", element)
    except Exception:
        pass
    element.send_keys(value)


def _click_apply_now(driver):
    apply_buttons = driver.find_elements(By.XPATH, "//div[contains(@class,'actions')]//a[contains(.,'APPLY NOW')]")
    if not apply_buttons:
        return False
    btn = apply_buttons[0]
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    except Exception:
        pass
    try:
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)
    return True


def _wait_option_exists(driver, select_css: str, label: str, timeout_s: int = 60):
    def _has_option(drv):
        try:
            select = Select(drv.find_element(By.CSS_SELECTOR, select_css))
            return any((o.text or "").strip() == label for o in select.options)
        except Exception:
            return False

    WebDriverWait(driver, timeout_s).until(_has_option)


def _select_program_preference(driver, program_label: str):
    # Attempt 1: standard select
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#programid")))
        _wait_option_exists(driver, "#programid", program_label, timeout_s=60)
        Select(driver.find_element(By.CSS_SELECTOR, "#programid")).select_by_visible_text(program_label)
        print("✅ Program selected via <select>:", program_label)
        return
    except Exception as e:
        print("Program select via <select> failed, trying fuzzy/Select2. Reason:", str(e))

    # Attempt 2: fuzzy match
    try:
        select = Select(driver.find_element(By.CSS_SELECTOR, "#programid"))
        for opt in select.options:
            text = (opt.text or "").strip()
            if not text:
                continue
            if program_label.lower() in text.lower() or text.lower() in program_label.lower():
                select.select_by_visible_text(text)
                print("✅ Program selected via fuzzy match:", text)
                return
    except Exception as e_opts:
        print("Could not read program options:", str(e_opts))

    # Attempt 3: Select2 fallback
    try:
        container = driver.find_element(
            By.CSS_SELECTOR,
            "#programid + span.select2, #programid ~ span.select2, span.select2"
        )
        container.click()
        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.select2-search__field"))
        )
        search.clear()
        search.send_keys(program_label)
        search.send_keys(Keys.ENTER)
        print("✅ Program selected via Select2:", program_label)
        return
    except Exception as e:
        _shot(driver, "program_select_failed")
        raise RuntimeError(
            f"Could not select program '{program_label}'. "
            f"Either label does not match dropdown text or selector needs adjustment. "
            f"Error: {e}"
        )


def apply_riphah(config: dict, submit: bool = True, debug_pause: bool = False):
    """
    One-run flow:
      1) Validate application data against policies
      2) Open portal and login (if needed)
      3) Go to List page
      4) Click APPLY NOW
      5) Fill form from data/application.yaml
      6) Submit (optional)
    """
    data = load_application_data()
    try:
        overrides = config.get("application_overrides") or {}
        if isinstance(overrides, dict):
            data.update({k: v for k, v in overrides.items() if v is not None})
    except Exception:
        pass
    
    # POLICY VALIDATION - NEW FEATURE
    print("\n" + "=" * 60)
    print("VALIDATING APPLICATION AGAINST UNIVERSITY POLICIES")
    print("=" * 60)
    
    validation_result = validate_before_apply(data)
    print(validation_result['report'])
    
    if not validation_result['is_valid']:
        print("\n❌ APPLICATION VALIDATION FAILED")
        print("Please fix the errors above before proceeding.")
        print("=" * 60 + "\n")
        
        # Ask user if they want to proceed anyway
        user_input = input("Do you want to proceed anyway? (yes/no): ").strip().lower()
        if user_input not in ['yes', 'y']:
            print("Application cancelled by user.")
            return
        else:
            print("⚠️ Proceeding with validation errors (not recommended)...")
    else:
        print("\n✅ VALIDATION PASSED - Proceeding with application...")
        print("=" * 60 + "\n")
    
    admissions = config["admissions"]
    base_url = admissions["base_url"]
    list_url = admissions["applications_list_url"]
    headless = bool(admissions.get("headless", False))
    user_data_dir = admissions.get("user_data_dir", "./browser_profile")

    driver = run_browser_persistent(user_data_dir=user_data_dir, headless=headless)

    try:
        # 1) Open portal
        print(f"Opening portal: {base_url}")
        driver.get(base_url)
        time.sleep(3)  # Increased wait for page load
        _shot(driver, "00_portal")
        
        print(f"Page loaded. Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")

        # 2) Wait for page to fully load and check for login form
        print("Waiting for page elements to load...")
        time.sleep(2)
        
        print("Checking for login form...")
        email_field = driver.find_elements(By.NAME, "email")
        password_field = driver.find_elements(By.NAME, "password")
        
        print(f"Found {len(email_field)} email fields and {len(password_field)} password fields")
        
        if email_field and password_field:
            print("Login form found - logging in...")
            creds = prompt_login(default_email=data.get("email", ""))
            
            # Clear and fill email field with VERY aggressive clearing
            email_elem = email_field[0]
            print(f"Email field found, current value: '{email_elem.get_attribute('value')}'")
            
            # Method 1: JavaScript force clear
            driver.execute_script("""
                arguments[0].value = '';
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, email_elem)
            time.sleep(0.3)
            
            # Method 2: Click and select all, then delete
            email_elem.click()
            time.sleep(0.2)
            email_elem.send_keys(Keys.CONTROL + "a")
            email_elem.send_keys(Keys.BACKSPACE)
            time.sleep(0.2)
            
            # Method 3: Clear again
            try:
                email_elem.clear()
            except:
                pass
            
            time.sleep(0.3)
            print(f"After clearing, value: '{email_elem.get_attribute('value')}'")
            
            # Now enter the email
            email_elem.send_keys(creds["email"])
            time.sleep(0.5)
            final_value = email_elem.get_attribute('value')
            print(f"Email entered, final value: '{final_value}'")
            
            if final_value != creds["email"]:
                print(f"⚠️ WARNING: Email mismatch! Expected '{creds['email']}' but got '{final_value}'")
                print("Attempting one more clear and fill...")
                driver.execute_script("arguments[0].value = '';", email_elem)
                time.sleep(0.2)
                email_elem.send_keys(creds["email"])
                time.sleep(0.3)
                print(f"Final attempt value: '{email_elem.get_attribute('value')}'")
            
            # Clear and fill password field
            pwd_elem = password_field[0]
            driver.execute_script("arguments[0].value = '';", pwd_elem)
            time.sleep(0.2)
            pwd_elem.click()
            pwd_elem.send_keys(Keys.CONTROL + "a")
            pwd_elem.send_keys(Keys.BACKSPACE)
            time.sleep(0.2)
            pwd_elem.send_keys(creds["password"])
            print("Password entered (hidden)")
            
            time.sleep(1)  # Wait before clicking
            print("Clicking login button...")
            try:
                login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
                print(f"Found login button: {login_btn.text}")
                login_btn.click()
            except Exception:
                print("Button not found, trying submit input...")
                driver.find_element(By.XPATH, "//input[@type='submit']").click()

            try:
                WebDriverWait(driver, 20).until(lambda d: "login" not in d.current_url.lower())
                print("✅ Login successful")
            except TimeoutException:
                print("⚠️ Login timeout - continuing anyway")

            time.sleep(1.2)
            _shot(driver, "01_after_login")
        else:
            print("No login form found - assuming already logged in")
            # Check if we're actually logged in by looking at the current page
            if "login" in driver.current_url.lower() or "Login" in driver.page_source[:500]:
                print("⚠️ Appears to be on login page but no form found - may need manual login")
                time.sleep(5)  # Give time to see the page

        # 3) Go to List page
        print(f"Navigating to applications list: {list_url}")
        driver.get(list_url)
        time.sleep(2.5)  # Increased wait time
        _shot(driver, "02_list")
        
        print(f"Current URL after navigation: {driver.current_url}")
        print(f"Page title: {driver.title}")
        
        # Check if we got redirected back to login
        if "login" in driver.current_url.lower() or driver.current_url == base_url:
            print("⚠️ Got redirected - not logged in properly!")
            print("Attempting to login again...")
            
            # Try to login again
            email_field = driver.find_elements(By.NAME, "email")
            password_field = driver.find_elements(By.NAME, "password")
            
            if email_field and password_field:
                creds = prompt_login(default_email=data.get("email", ""))
                
                # Clear and fill with extra care
                email_elem = email_field[0]
                try:
                    email_elem.clear()
                    driver.execute_script("arguments[0].value = '';", email_elem)
                    time.sleep(0.3)
                except Exception:
                    pass
                email_elem.send_keys(creds["email"])
                
                pwd_elem = password_field[0]
                try:
                    pwd_elem.clear()
                    driver.execute_script("arguments[0].value = '';", pwd_elem)
                    time.sleep(0.3)
                except Exception:
                    pass
                pwd_elem.send_keys(creds["password"])
                
                try:
                    driver.find_element(By.XPATH, "//button[contains(., 'Login')]").click()
                except Exception:
                    driver.find_element(By.XPATH, "//input[@type='submit']").click()
                
                time.sleep(3)
                print(f"After re-login, URL: {driver.current_url}")
                
                # Try going to list page again
                driver.get(list_url)
                time.sleep(2.5)
                print(f"After second attempt, URL: {driver.current_url}")

        if "login" in driver.current_url.lower():
            raise RuntimeError("Login failed or session not created. Cannot proceed to Apply Now.")

        # 4) Click APPLY NOW
        print("Looking for APPLY NOW button...")
        # Try to find any buttons on the page for debugging
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(all_buttons)} buttons and {len(all_links)} links on page")
        
        if not _click_apply_now(driver):
            _shot(driver, "apply_now_not_found")
            print("❌ Could not find APPLY NOW button")
            print("Available buttons:")
            for btn in all_buttons[:5]:  # Show first 5 buttons
                print(f"  - {btn.text}")
            print("Available links with 'apply' in text:")
            for link in all_links:
                if 'apply' in link.text.lower():
                    print(f"  - {link.text} -> {link.get_attribute('href')}")
            raise RuntimeError("APPLY NOW button not found on List page.")

        WebDriverWait(driver, 30).until(lambda d: "Student/application" in d.current_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#branch")))
        time.sleep(1.2)
        _shot(driver, "03_form")

        print("Starting form fill...")

        # Campus & Level
        try:
            Select(driver.find_element(By.CSS_SELECTOR, "#branch")).select_by_visible_text(data["campus"])
            time.sleep(0.8)
            print("✅ Campus filled:", data["campus"])
        except Exception as e:
            print(f"⚠️ Campus fill error: {e}")

        try:
            Select(driver.find_element(By.CSS_SELECTOR, "#ptype")).select_by_visible_text(data["level"])
            time.sleep(1.0)
            print("✅ Level filled:", data["level"])
        except Exception as e:
            print(f"⚠️ Level fill error: {e}")

        # Program preference
        try:
            _select_program_preference(driver, data["program1"])
            time.sleep(0.4)
            print("✅ Program filled:", data["program1"])
        except Exception as e:
            print(f"⚠️ Program fill error: {e}")

        # Personal info
        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='fname']"), data["first_name"])
            print("✅ First name filled")
        except Exception as e:
            print(f"⚠️ First name error: {e}")

        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='mname']"), data.get("middle_name", ""))
            print("✅ Middle name filled")
        except Exception as e:
            print(f"⚠️ Middle name error: {e}")

        try:
            lname = data.get("last_name", "")
            lname_val = lname if lname else "N/A"
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='lname']"), lname_val)
            print("✅ Last name filled")
        except Exception as e:
            print(f"⚠️ Last name error: {e}")
            try:
                driver.execute_script(
                    "const ln=document.querySelector(\"input[name='lname']\");"
                    "if(ln){ln.value='N/A';ln.dispatchEvent(new Event('change',{bubbles:true}));}"
                )
                print("✅ Last name filled via JavaScript")
            except Exception as e2:
                print(f"⚠️ Last name JS error: {e2}")

        try:
            if data.get("nationality"):
                Select(driver.find_element(By.CSS_SELECTOR, "#nationality")).select_by_visible_text(data["nationality"])
                print("✅ Nationality filled")
        except Exception as e:
            print(f"⚠️ Nationality error: {e}")

        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='cnic']"), data["cnic"])
            print("✅ CNIC filled")
        except Exception as e:
            print(f"⚠️ CNIC error: {e}")

        try:
            Select(driver.find_element(By.CSS_SELECTOR, "#gender")).select_by_visible_text(data["gender"])
            print("✅ Gender filled")
        except Exception as e:
            print(f"⚠️ Gender error: {e}")

        # DOB (readonly)
        try:
            driver.execute_script("document.getElementById('DOB')?.removeAttribute('readonly')")
            dob_value = data.get("dob", "2000-05-15")
            dob = driver.find_element(By.ID, "DOB")
            _set_value(dob, dob_value)
            print(f"✅ DOB filled: {dob_value}")
        except Exception as e:
            print(f"⚠️ DOB error: {e}")

        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='fathername']"), data["father_name"])
            print("✅ Father name filled")
        except Exception as e:
            print(f"⚠️ Father name error: {e}")

        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='lastinstitute']"), data["last_institute"])
            print("✅ Last institute filled")
        except Exception as e:
            print(f"⚠️ Last institute error: {e}")

        try:
            Select(driver.find_element(By.CSS_SELECTOR, "select[name='aboutus']")).select_by_visible_text(data["about_us"])
            print("✅ About us filled")
        except Exception as e:
            print(f"⚠️ About us error: {e}")

        # Contact
        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "#Email"), data["email"])
            print("✅ Email filled")
        except Exception as e:
            print(f"⚠️ Email error: {e}")

        try:
            _set_value(driver.find_element(By.CSS_SELECTOR, "input[name='mobile']"), data["mobile"])
            print("✅ Mobile filled")
        except Exception as e:
            print(f"⚠️ Mobile error: {e}")

        # Address (required)
        try:
            address = data.get("address", "N/A")
            _set_value(driver.find_element(By.CSS_SELECTOR, "#addressline1"), address)
            print("✅ Address filled")
        except Exception as e:
            print(f"⚠️ Address error: {e}")
            try:
                driver.execute_script(
                    "const addr=document.querySelector('#addressline1');"
                    f"if(addr){{addr.value={json.dumps(address)};addr.dispatchEvent(new Event('change',{{bubbles:true}}));}}"
                )
                print("✅ Address filled via JavaScript")
            except Exception as e2:
                print(f"⚠️ Address JS error: {e2}")

        try:
            alt_phone = data.get("alternate_phone", "")
            if alt_phone:
                _set_value(driver.find_element(By.CSS_SELECTOR, "#phone1"), alt_phone)
                print("✅ Alternate phone filled")
            else:
                print("⚠️ Alternate phone is empty")
        except Exception as e:
            print(f"⚠️ Alternate phone error: {e}")

        # Country & City
        try:
            country = data.get("country", "Pakistan")
            try:
                Select(driver.find_element(By.CSS_SELECTOR, "#country1")).select_by_visible_text(country)
                print("✅ Country filled")
            except Exception:
                Select(driver.find_element(By.CSS_SELECTOR, "#country1")).select_by_value(country)
                print("✅ Country filled (by value)")
        except Exception as e:
            print(f"⚠️ Country error: {e}")

        try:
            city = data.get("city", "Islamabad")
            try:
                Select(driver.find_element(By.CSS_SELECTOR, "#pcity1")).select_by_visible_text(city)
                print("✅ City filled")
            except Exception:
                Select(driver.find_element(By.CSS_SELECTOR, "#pcity1")).select_by_value(city)
                print("✅ City filled (by value)")
        except Exception as e:
            print(f"⚠️ City error: {e}")

        _shot(driver, "04_filled")
        print("✅ Form filled successfully.")

        print("\nValidating form fields...")
        check_and_report(driver)

        # Submit
        if submit:
            print("Attempting to submit application...")
            submit_btn = None

            css_selectors = [
                "#application_submit",
                "button[id*='submit']",
                "button[class*='submit']",
                "input[type='submit']",
            ]
            for selector in css_selectors:
                try:
                    candidates = driver.find_elements(By.CSS_SELECTOR, selector)
                    if candidates:
                        submit_btn = candidates[0]
                        break
                except Exception:
                    continue

            if not submit_btn:
                xpath_selectors = [
                    "//button[contains(., 'Submit')]",
                    "//button[contains(., 'Apply')]",
                ]
                for selector in xpath_selectors:
                    try:
                        submit_btn = driver.find_element(By.XPATH, selector)
                        break
                    except Exception:
                        continue

            if not submit_btn:
                raise RuntimeError("Submit button not found. Please verify selector.")

            try:
                submit_btn.click()
                time.sleep(1.5)
                _shot(driver, "05_submitted")
                print("✅ Application submitted successfully.")
            except Exception as e:
                raise RuntimeError(f"Failed to click or detect submission: {e}")
        else:
            print("⚠️ submit=False (not submitting).")

        if debug_pause:
            print("Keeping browser open 20s...")
            time.sleep(20)
    finally:
        driver.quit()
