# agent/admissions_riphah.py
import os
import time
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from agent.browser import run_browser_persistent
from agent.credentials import prompt_registration, prompt_login


def _save_registration_to_yaml(reg_data: dict):
    """Save registration data to data/application.yaml"""
    try:
        yaml_path = "data/application.yaml"

        if os.path.exists(yaml_path):
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}

        name_parts = reg_data.get("name", "").strip().split()
        if len(name_parts) >= 2:
            data["first_name"] = name_parts[0]
            data["last_name"] = " ".join(name_parts[1:])
        elif len(name_parts) == 1:
            data["first_name"] = name_parts[0]
            data["last_name"] = ""

        data["email"] = reg_data.get("email", "")
        data["mobile"] = reg_data.get("mobile", "")

        os.makedirs("data", exist_ok=True)
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)
        print(f"✅ Registration data saved to {yaml_path}")
    except Exception as e:
        print(f"⚠️  Could not save registration data: {e}")


def _safe_screenshot(driver, name: str):
    try:
        driver.save_screenshot(f"{name}.png")
        print(f"[Saved screenshot] {name}.png")
    except Exception:
        pass


def _click_login_button(driver):
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
        btn.click()
        return True
    except Exception:
        try:
            btn = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'Login')]")
            btn.click()
            return True
        except Exception:
            return False


def register_then_login(config: dict):
    reg_url = config["admissions"]["registration_url"]
    base_url = config["admissions"]["base_url"]
    headless = bool(config["admissions"].get("headless", False))
    user_data_dir = config["admissions"].get("user_data_dir", "./browser_profile")

    reg = prompt_registration()
    driver = run_browser_persistent(user_data_dir=user_data_dir, headless=headless)

    try:
        driver.get(reg_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "firstname")))

        # Clear all fields first to avoid duplicate values
        firstname_field = driver.find_element(By.NAME, "firstname")
        firstname_field.clear()
        firstname_field.send_keys(reg["name"])
        
        mobile_field = driver.find_element(By.NAME, "mobile")
        mobile_field.clear()
        mobile_field.send_keys(reg["mobile"])
        
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(reg["email"])
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(reg["password"])
        
        rpassword_field = driver.find_element(By.NAME, "rpassword")
        rpassword_field.clear()
        rpassword_field.send_keys(reg["password"])

        driver.find_element(By.ID, "register-submit-btn").click()

        try:
            WebDriverWait(driver, 20).until(lambda d: d.current_url != reg_url)
        except TimeoutException:
            pass

        time.sleep(1.5)
        print("Registration submitted. Current URL:", driver.current_url)
        _save_registration_to_yaml(reg)

        driver.get(base_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))

        # Clear fields first to avoid duplicate values from cached form data
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(reg["email"])
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(reg["password"])
        
        _click_login_button(driver)

        try:
            WebDriverWait(driver, 20).until(lambda d: "login" not in d.current_url.lower())
        except TimeoutException:
            pass

        time.sleep(1.5)
        print("Login submitted. Current URL:", driver.current_url)
        _safe_screenshot(driver, "after_login")
        time.sleep(3)
    finally:
        driver.quit()


def login_only(config: dict):
    base_url = config["admissions"]["base_url"]
    headless = bool(config["admissions"].get("headless", False))
    user_data_dir = config["admissions"].get("user_data_dir", "./browser_profile")

    creds = prompt_login()
    driver = run_browser_persistent(user_data_dir=user_data_dir, headless=headless)

    try:
        driver.get(base_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))

        # Clear fields first to avoid duplicate values from cached form data
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(creds["email"])
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(creds["password"])
        
        _click_login_button(driver)

        try:
            WebDriverWait(driver, 20).until(lambda d: "login" not in d.current_url.lower())
        except TimeoutException:
            pass

        time.sleep(1.5)
        print("Login submitted. Current URL:", driver.current_url)
        _safe_screenshot(driver, "after_login")
        time.sleep(3)
    finally:
        driver.quit()
