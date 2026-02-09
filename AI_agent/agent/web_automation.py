from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    import time
except Exception:  # pragma: no cover - optional dependency
    webdriver = None
    ChromeOptions = None
    ChromeDriverManager = None
    Service = None
    By = None
    Keys = None
    WebDriverWait = None
    EC = None


@dataclass
class WebAutomationConfig:
    driver_path: str = ''
    headless: bool = True


class WebAutomation:
    def __init__(self, config: WebAutomationConfig) -> None:
        self.config = config
        self._driver: Optional[object] = None

    def start(self) -> None:
        if webdriver is None or ChromeOptions is None:
            raise RuntimeError('Selenium is not installed. Please install selenium.')

        options = ChromeOptions()
        if self.config.headless:
            options.add_argument('--headless=new')
        
        # Add options for better automation
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            if self.config.driver_path:
                self._driver = webdriver.Chrome(
                    service=Service(self.config.driver_path),
                    options=options,
                )
            else:
                # Auto-download and manage ChromeDriver via webdriver-manager
                try:
                    driver_path = ChromeDriverManager().install()
                except Exception as manager_error:
                    # If manager fails, try without explicit driver (system PATH)
                    raise RuntimeError(
                        f'Failed to download ChromeDriver: {str(manager_error)}. '
                        f'Trying to use system Chrome...'
                    )
                self._driver = webdriver.Chrome(
                    service=Service(driver_path),
                    options=options,
                )
        except Exception as e:
            # If browser fails to start, we'll handle it in task execution
            raise RuntimeError(f'Failed to start browser: {str(e)}')

    def stop(self) -> None:
        if self._driver:
            self._driver.quit()
            self._driver = None

    def open_url(self, url: str) -> None:
        if not self._driver:
            self.start()
        self._driver.get(url)
    
    def fill_input_by_name(self, name: str, value: str) -> bool:
        """Fill input field by name attribute"""
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            element.clear()
            element.send_keys(value)
            return True
        except Exception:
            return False
    
    def fill_input_by_id(self, element_id: str, value: str) -> bool:
        """Fill input field by id attribute"""
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            element.clear()
            element.send_keys(value)
            return True
        except Exception:
            return False
    
    def fill_input_by_placeholder(self, placeholder: str, value: str) -> bool:
        """Fill input field by placeholder text"""
        try:
            element = self._driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
            element.clear()
            element.send_keys(value)
            return True
        except Exception:
            return False
    
    def fill_input_by_label(self, label_text: str, value: str) -> bool:
        """Fill input field by associated label text"""
        try:
            # Find label containing the text
            label = self._driver.find_element(By.XPATH, f"//label[contains(text(), '{label_text}')]")
            # Get the 'for' attribute or find next input
            input_id = label.get_attribute('for')
            if input_id:
                element = self._driver.find_element(By.ID, input_id)
            else:
                # Try to find input near the label
                element = label.find_element(By.XPATH, ".//following::input[1]")
            element.clear()
            element.send_keys(value)
            return True
        except Exception:
            return False
    
    def click_button_by_text(self, button_text: str) -> bool:
        """Click button by text content"""
        try:
            button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
            )
            button.click()
            return True
        except Exception:
            # Try with input type submit
            try:
                button = self._driver.find_element(By.XPATH, f"//input[@type='submit' and contains(@value, '{button_text}')]")
                button.click()
                return True
            except Exception:
                return False
    
    def click_element_by_id(self, element_id: str) -> bool:
        """Click element by id"""
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            element.click()
            return True
        except Exception:
            return False
    
    def type_in_active_element(self, text: str) -> bool:
        """Type text in currently focused element"""
        try:
            active = self._driver.switch_to.active_element
            active.send_keys(text)
            return True
        except Exception:
            return False
    
    def press_enter(self) -> bool:
        """Press Enter key in active element"""
        try:
            active = self._driver.switch_to.active_element
            active.send_keys(Keys.RETURN)
            return True
        except Exception:
            return False
    
    def get_page_title(self) -> str:
        """Get current page title"""
        try:
            return self._driver.title
        except Exception:
            return ""
    
    def get_current_url(self) -> str:
        """Get current URL"""
        try:
            return self._driver.current_url
        except Exception:
            return ""
    
    def find_and_fill_form(self, form_data: dict) -> dict:
        """Intelligently find and fill form fields"""
        results = {}
        
        for field_name, value in form_data.items():
            filled = False
            
            # Try multiple strategies
            strategies = [
                ('name', lambda: self.fill_input_by_name(field_name, value)),
                ('id', lambda: self.fill_input_by_id(field_name, value)),
                ('placeholder', lambda: self.fill_input_by_placeholder(field_name, value)),
                ('label', lambda: self.fill_input_by_label(field_name, value)),
            ]
            
            for strategy_name, strategy_func in strategies:
                try:
                    if strategy_func():
                        results[field_name] = f'✓ Filled using {strategy_name}'
                        filled = True
                        break
                except Exception:
                    continue
            
            if not filled:
                results[field_name] = '✗ Could not find field'
        
        return results
    
    def wait(self, seconds: float) -> None:
        """Wait for specified seconds"""
        time.sleep(seconds)
    
    def detect_forms(self) -> list:
        """Detect all forms on the current page"""
        try:
            forms = self._driver.find_elements(By.TAG_NAME, 'form')
            return forms
        except Exception:
            return []
    
    def get_form_fields(self, form=None) -> list:
        """Get all input fields from a form or entire page"""
        try:
            if form:
                inputs = form.find_elements(By.TAG_NAME, 'input')
                textareas = form.find_elements(By.TAG_NAME, 'textarea')
                selects = form.find_elements(By.TAG_NAME, 'select')
            else:
                inputs = self._driver.find_elements(By.TAG_NAME, 'input')
                textareas = self._driver.find_elements(By.TAG_NAME, 'textarea')
                selects = self._driver.find_elements(By.TAG_NAME, 'select')
            
            fields = []
            for element in inputs + textareas + selects:
                try:
                    # Skip hidden, submit, button fields
                    input_type = element.get_attribute('type') or 'text'
                    if input_type in ['hidden', 'submit', 'button', 'image', 'reset']:
                        continue
                    
                    # Get field information
                    field_info = {
                        'element': element,
                        'type': input_type,
                        'name': element.get_attribute('name') or '',
                        'id': element.get_attribute('id') or '',
                        'placeholder': element.get_attribute('placeholder') or '',
                        'value': element.get_attribute('value') or '',
                        'required': element.get_attribute('required') is not None,
                        'visible': element.is_displayed()
                    }
                    
                    # Try to find associated label
                    try:
                        if field_info['id']:
                            label = self._driver.find_element(By.XPATH, f"//label[@for='{field_info['id']}']")
                            field_info['label'] = label.text
                        else:
                            # Try to find nearby label
                            parent = element.find_element(By.XPATH, '..')
                            label = parent.find_element(By.TAG_NAME, 'label')
                            field_info['label'] = label.text
                    except Exception:
                        field_info['label'] = ''
                    
                    fields.append(field_info)
                except Exception:
                    continue
            
            return fields
        except Exception:
            return []
    
    def auto_fill_form(self, user_data: dict = None) -> dict:
        """Automatically detect and fill forms with intelligent field matching"""
        if not user_data:
            # Default user data for testing
            user_data = {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '1234567890',
                'address': '123 Main Street',
                'city': 'New York',
                'country': 'USA',
                'message': 'This is an automated form submission.',
                'subject': 'Inquiry',
                'company': 'Example Corp',
                'website': 'https://example.com'
            }
        
        results = {
            'forms_found': 0,
            'fields_found': 0,
            'fields_filled': 0,
            'details': []
        }
        
        try:
            # Detect forms
            forms = self.detect_forms()
            results['forms_found'] = len(forms)
            
            # Get all fields (from forms or entire page)
            fields = self.get_form_fields()
            results['fields_found'] = len(fields)
            
            # Field matching patterns
            field_patterns = {
                'name': ['name', 'full name', 'fullname', 'your name', 'username', 'user name', 'fname', 'first name', 'firstname'],
                'email': ['email', 'e-mail', 'mail', 'your email', 'email address', 'e-mail address'],
                'phone': ['phone', 'telephone', 'mobile', 'cell', 'contact', 'phone number', 'tel'],
                'address': ['address', 'street', 'location', 'your address'],
                'city': ['city', 'town'],
                'country': ['country', 'nation'],
                'message': ['message', 'comment', 'comments', 'description', 'details', 'query', 'your message'],
                'subject': ['subject', 'topic', 'regarding'],
                'company': ['company', 'organization', 'organisation', 'business'],
                'website': ['website', 'site', 'url', 'web']
            }
            
            # Try to fill each field
            for field in fields:
                if not field['visible']:
                    continue
                
                # Skip if already filled
                if field['value']:
                    continue
                
                # Determine what data to fill
                field_identifier = (
                    field['name'].lower() + ' ' +
                    field['id'].lower() + ' ' +
                    field['placeholder'].lower() + ' ' +
                    field['label'].lower()
                )
                
                filled = False
                for data_key, patterns in field_patterns.items():
                    if any(pattern in field_identifier for pattern in patterns):
                        try:
                            element = field['element']
                            element.clear()
                            element.send_keys(user_data.get(data_key, ''))
                            results['fields_filled'] += 1
                            results['details'].append({
                                'field': field['name'] or field['id'] or field['placeholder'],
                                'filled_with': data_key,
                                'value': user_data.get(data_key, ''),
                                'status': '✓'
                            })
                            filled = True
                            break
                        except Exception:
                            continue
                
                if not filled and field['type'] == 'text':
                    # Generic text field - try to fill with something
                    results['details'].append({
                        'field': field['name'] or field['id'] or field['placeholder'],
                        'filled_with': 'skipped',
                        'value': '',
                        'status': '○'
                    })
            
            return results
            
        except Exception as e:
            results['error'] = str(e)
            return results
