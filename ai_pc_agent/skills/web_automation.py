"""
Web Automation Skill - ENHANCED VERSION
Actually performs automation, not just searching
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import logging
from typing import Dict, Any, List
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class FormField:
    name: str
    field_type: str
    element: Any
    label: str = ""

class WebAutomation:
    def __init__(self, headless: bool = False):
        self.driver = None
        self.headless = headless
        self.current_url = ""
        self.form_memory = {}  # Remember how to fill forms
        self._init_driver()
        
    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.implicitly_wait(10)
            logger.info("✅ WebDriver initialized and ready for automation")
        except Exception as e:
            logger.error(f"❌ WebDriver failed: {e}")
            raise
    
    def apply_admission(self, institution: str = "", program: str = "", 
                       applicant_data: Dict = None, **kwargs) -> Dict[str, Any]:
        """
        ACTUALLY automates admission application
        1. Finds the university application portal
        2. Navigates to it
        3. Attempts to fill the form
        """
        try:
            if not institution:
                return {
                    'status': 'error',
                    'message': 'Please specify a university name',
                    'example': 'Apply for admission to Harvard University'
                }
            
            logger.info(f"🎓 Starting REAL admission automation for: {institution}")
            
            # Step 1: Find the official application portal
            portal_info = self._find_university_portal(institution)
            
            if not portal_info['found']:
                return {
                    'status': 'partial',
                    'message': f'Could not find direct portal for {institution}',
                    'action_taken': 'Searched for application information',
                    'search_results': portal_info.get('results', []),
                    'suggestion': 'Please provide the direct application URL'
                }
            
            # Step 2: Navigate to the portal
            apply_url = portal_info['apply_url']
            logger.info(f"🌐 Navigating to: {apply_url}")
            self.driver.get(apply_url)
            time.sleep(3)
            
            # Step 3: Analyze the page and fill forms
            page_analysis = self._analyze_application_page()
            
            # Step 4: Attempt to fill forms if applicant data provided
            filled_forms = []
            if applicant_data:
                filled_forms = self._fill_application_forms(applicant_data)
            
            # Step 5: Take screenshot for verification
            screenshot_path = f"admission_{institution.replace(' ', '_')}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                'status': 'success',
                'message': f'Admission automation initiated for {institution}',
                'institution': institution,
                'program': program,
                'portal_url': apply_url,
                'page_type': page_analysis['page_type'],
                'forms_detected': page_analysis['forms_count'],
                'fields_found': page_analysis['fields_count'],
                'forms_filled': len(filled_forms),
                'filled_sections': filled_forms,
                'screenshot': screenshot_path,
                'next_steps': [
                    'Review the screenshot to verify correct page',
                    'Complete any CAPTCHA if present',
                    'Review auto-filled information',
                    'Submit application manually or provide submit command'
                ],
                'automation_level': 'semi-automated',
                'note': 'Form filling requires applicant_data dict with personal info'
            }
            
        except Exception as e:
            logger.error(f"❌ Admission automation error: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'troubleshooting': [
                    'Check internet connection',
                    'Verify university name is correct',
                    'University may require special login'
                ]
            }
    
    def _find_university_portal(self, institution: str) -> Dict:
        """Find the official application portal for a university"""
        try:
            logger.info(f"🔍 Searching for {institution} application portal...")
            
            # Search for apply portal with better query
            search_query = f"{institution} apply admission online application site:.edu"
            search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            
            logger.info(f"🌐 Searching: {search_url}")
            self.driver.get(search_url)
            time.sleep(3)  # Wait for page to load
            
            # Take screenshot of search results
            self.driver.save_screenshot(f"search_{institution.replace(' ', '_')}.png")
            
            # Look for results - updated selectors for current Google layout
            results = []
            
            # Try multiple possible selectors
            selectors = [
                "div.g",  # Classic result
                "div[data-header-feature]",  # Newer layout
                "div[data-result-index]",  # Another variant
                "div.yuRUbf",  # Link container
                "h3.LC20lb",  # Title directly
            ]
            
            result_elements = []
            for selector in selectors:
                try:
                    elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elems:
                        result_elements = elems
                        logger.info(f"✅ Found results using selector: {selector}")
                        break
                except:
                    continue
            
            logger.info(f"📊 Found {len(result_elements)} result elements")
            
            for elem in result_elements[:5]:
                try:
                    # Try to find link and title
                    link_elem = None
                    title_elem = None
                    
                    # Try different ways to find link
                    try:
                        link_elem = elem.find_element(By.TAG_NAME, "a")
                    except:
                        try:
                            link_elem = elem.find_element(By.XPATH, "..//a")
                        except:
                            link_elem = elem if elem.tag_name == "a" else None
                    
                    if link_elem:
                        url = link_elem.get_attribute("href")
                        title = link_elem.text or ""
                        
                        # Try to get better title
                        if not title:
                            try:
                                title_elem = elem.find_element(By.TAG_NAME, "h3")
                                title = title_elem.text
                            except:
                                title = url
                        
                        if url and url.startswith("http"):
                            results.append({
                                'title': title,
                                'url': url,
                                'is_official': institution.lower() in title.lower() or 
                                              'edu' in url or 
                                              'apply' in url.lower() or 
                                              'admission' in url.lower()
                            })
                            logger.info(f"🔗 Found: {title[:50]}... -> {url[:60]}...")
                            
                except Exception as e:
                    continue
            
            # Prioritize official links
            official_links = [l for l in results if l['is_official']]
            best_link = official_links[0] if official_links else (results[0] if results else None)
            
            if best_link:
                logger.info(f"✅ Best portal found: {best_link['url']}")
                return {
                    'found': True,
                    'apply_url': best_link['url'],
                    'title': best_link['title'],
                    'confidence': 'high' if official_links else 'medium',
                    'all_results': results[:3]
                }
            else:
                logger.warning("⚠️ No portal found in search results")
                return {
                    'found': False,
                    'results': results,
                    'search_url': search_url,
                    'html_sample': self.driver.page_source[:500]  # Debug info
                }
                
        except Exception as e:
            logger.error(f"❌ Error finding portal: {e}")
            return {'found': False, 'error': str(e)}
    
    def _analyze_application_page(self) -> Dict:
        """Analyze what type of application page we're on"""
        try:
            page_source = self.driver.page_source.lower()
            
            # Detect page type
            if 'common app' in page_source or 'commonapp' in page_source:
                page_type = 'Common Application'
            elif 'coalition' in page_source:
                page_type = 'Coalition Application'
            elif 'uc application' in page_source or 'university of california' in page_source:
                page_type = 'UC Application'
            else:
                page_type = 'Institution-Specific Application'
            
            # Count forms and fields
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            
            return {
                'page_type': page_type,
                'forms_count': len(forms),
                'fields_count': len(inputs) + len(selects) + len(textareas),
                'inputs': len(inputs),
                'dropdowns': len(selects),
                'text_areas': len(textareas)
            }
            
        except Exception as e:
            return {
                'page_type': 'Unknown',
                'forms_count': 0,
                'fields_count': 0,
                'error': str(e)
            }
    
    def _fill_application_forms(self, data: Dict) -> List[str]:
        """Intelligently fill application forms"""
        filled_sections = []
        
        try:
            # Map common field names to data keys
            field_mappings = {
                'first name': ['first_name', 'firstname', 'firstName', 'fname'],
                'last name': ['last_name', 'lastname', 'lastName', 'lname'],
                'email': ['email', 'email_address', 'emailAddress'],
                'phone': ['phone', 'telephone', 'mobile', 'cell'],
                'address': ['address', 'street', 'street_address'],
                'city': ['city'],
                'state': ['state', 'province'],
                'zip': ['zip', 'zipcode', 'postal', 'postal_code'],
                'country': ['country'],
                'birthdate': ['dob', 'birthdate', 'date_of_birth', 'birth_date'],
                'gender': ['gender', 'sex'],
                'citizenship': ['citizenship', 'nationality'],
                'high school': ['high_school', 'school', 'current_school']
            }
            
            # Find all input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            
            # Fill text inputs
            for input_field in inputs:
                try:
                    field_type = input_field.get_attribute("type")
                    if field_type in ["hidden", "submit", "button", "image", "file"]:
                        continue
                    
                    # Get field identifier
                    field_id = input_field.get_attribute("id") or ""
                    field_name = input_field.get_attribute("name") or ""
                    placeholder = input_field.get_attribute("placeholder") or ""
                    aria_label = input_field.get_attribute("aria-label") or ""
                    
                    # Try to match with data
                    value_to_fill = None
                    field_text = f"{field_id} {field_name} {placeholder} {aria_label}".lower()
                    
                    for field_pattern, data_keys in field_mappings.items():
                        if field_pattern in field_text:
                            for key in data_keys:
                                if key in data:
                                    value_to_fill = data[key]
                                    break
                            if value_to_fill:
                                break
                    
                    # If no match found, try direct name/id matching
                    if not value_to_fill:
                        for key in data:
                            if key.lower() in field_text or field_text in key.lower():
                                value_to_fill = data[key]
                                break
                    
                    # Fill the field if we found a value
                    if value_to_fill:
                        input_field.clear()
                        input_field.send_keys(str(value_to_fill))
                        filled_sections.append(f"Filled: {field_name or field_id}")
                        
                except Exception as e:
                    continue
            
            # Fill dropdowns
            for select in selects:
                try:
                    select_name = select.get_attribute("name") or ""
                    select_id = select.get_attribute("id") or ""
                    
                    # Try to find matching data
                    for key, value in data.items():
                        if key.lower() in f"{select_name} {select_id}".lower():
                            dropdown = Select(select)
                            try:
                                dropdown.select_by_visible_text(str(value))
                                filled_sections.append(f"Selected: {select_name}")
                            except:
                                try:
                                    dropdown.select_by_value(str(value))
                                except:
                                    pass
                            break
                except:
                    continue
            
            return filled_sections
            
        except Exception as e:
            logger.error(f"Error filling forms: {e}")
            return filled_sections
    
    def fill_form_generic(self, url: str = "", form_data: Dict = None, **kwargs) -> Dict[str, Any]:
        """Enhanced generic form filler with better field detection"""
        try:
            if not url:
                return {'status': 'error', 'message': 'No URL provided'}
            
            logger.info(f"📝 Filling form at: {url}")
            self.driver.get(url)
            time.sleep(2)
            
            filled = self._fill_application_forms(form_data or {})
            
            # Look for submit button
            submit_buttons = self.driver.find_elements(By.XPATH, 
                "//button[@type='submit'] | //input[@type='submit'] | //button[contains(text(), 'Submit')] | //button[contains(text(), 'Continue')]")
            
            return {
                'status': 'success',
                'url': url,
                'fields_filled': len(filled),
                'filled_fields': filled[:10],  # Limit output
                'submit_buttons_found': len(submit_buttons),
                'note': 'Review before submitting. Call submit_form() to finalize.'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def submit_form(self, **kwargs) -> Dict[str, Any]:
        """Submit the current form"""
        try:
            # Find submit button
            submit_btn = self.driver.find_element(By.XPATH, 
                "//button[@type='submit'] | //input[@type='submit'] | //button[contains(text(), 'Submit')]")
            submit_btn.click()
            time.sleep(2)
            
            return {
                'status': 'success',
                'message': 'Form submitted successfully',
                'current_url': self.driver.current_url
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Could not submit: {e}',
                'note': 'Please submit manually after reviewing'
            }
    
    def search_policy(self, topic: str = "", institution: str = "", **kwargs) -> Dict[str, Any]:
        """Search for and extract policy information"""
        try:
            query = f"{institution} {topic} policy site:.edu" if institution else f"{topic} policy guidelines"
            
            # Search Google
            self.driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            time.sleep(2)
            
            # Extract policy snippets
            results = []
            result_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.g")[:5]
            
            for div in result_divs:
                try:
                    title = div.find_element(By.CSS_SELECTOR, "h3").text
                    snippet = div.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                    link = div.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    results.append({
                        'title': title,
                        'summary': snippet[:200] + "..." if len(snippet) > 200 else snippet,
                        'link': link
                    })
                except:
                    continue
            
            # Try to open the first result and extract key policy points
            key_points = []
            if results:
                try:
                    self.driver.get(results[0]['link'])
                    time.sleep(2)
                    
                    # Look for common policy sections
                    content = self.driver.find_elements(By.TAG_NAME, "p")
                    for p in content[:5]:
                        text = p.text
                        if len(text) > 50 and any(keyword in text.lower() for keyword in ['policy', 'requirement', 'must', 'should', 'guideline']):
                            key_points.append(text[:150])
                except:
                    pass
            
            return {
                'status': 'success',
                'topic': topic,
                'institution': institution,
                'search_results': results,
                'key_policy_points': key_points[:3],
                'action': 'Found and analyzed policy information'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def search_information(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search and extract structured information with updated selectors"""
        try:
            logger.info(f"🔍 Searching for: {query}")
            self.driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            time.sleep(2)
            
            # Save screenshot
            self.driver.save_screenshot("search_result.png")
            
            # Extract featured snippet
            featured_snippet = ""
            snippet_selectors = [
                "div.VwiC3b",  # Classic
                "div[data-sokoban-container] span",  # Newer
                "div.yp1CPe",  # Another variant
                "div[data-content-feature]",  # Featured snippet
            ]
            
            for selector in snippet_selectors:
                try:
                    elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elems:
                        featured_snippet = elems[0].text
                        break
                except:
                    continue
            
            # Get top results with flexible selectors
            results = []
            result_selectors = [
                "div.g",
                "div[data-result-index]",
                "div[data-header-feature]",
            ]
            
            result_elements = []
            for selector in result_selectors:
                try:
                    elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elems:
                        result_elements = elems
                        break
                except:
                    continue
            
            for result in result_elements[:5]:
                try:
                    # Try to find title
                    title = ""
                    for title_sel in ["h3", "h3.LC20lb", ".DKV0Md"]:
                        try:
                            title = result.find_element(By.CSS_SELECTOR, title_sel).text
                            break
                        except:
                            continue
                    
                    # Try to find link
                    link = ""
                    try:
                        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    except:
                        try:
                            link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        except:
                            pass
                    
                    if title and link:
                        results.append({'title': title, 'link': link})
                        
                except:
                    continue
            
            return {
                'status': 'success',
                'query': query,
                'results_found': len(results),
                'direct_answer': featured_snippet[:300] if featured_snippet else None,
                'sources': results,
                'screenshot': 'search_result.png',
                'action': 'Searched and extracted information'
            }
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def check_email(self, **kwargs) -> Dict[str, Any]:
        """Navigate to Gmail and check emails"""
        try:
            self.driver.get("https://gmail.com")
            time.sleep(2)
            
            # Check if login page
            if "signin" in self.driver.current_url:
                return {
                    'status': 'requires_auth',
                    'message': 'Please log in to Gmail manually',
                    'url': self.driver.current_url,
                    'automation_possible': False
                }
            
            # If already logged in, count unread emails
            try:
                unread_elements = self.driver.find_elements(By.CSS_SELECTOR, "tr.zA.zE")  # Unread email rows
                return {
                    'status': 'success',
                    'unread_count': len(unread_elements),
                    'message': f'Found {len(unread_elements)} unread emails',
                    'action': 'Gmail opened. Review emails manually.'
                }
            except:
                return {
                    'status': 'unknown',
                    'message': 'Gmail loaded but could not count emails',
                    'current_url': self.driver.current_url
                }
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def cleanup(self):
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed")
            except:
                pass

if __name__ == "__main__":
    # Test the enhanced automation
    web = WebAutomation(headless=False)
    
    # Test admission automation
    result = web.apply_admission(
        institution="Stanford University",
        applicant_data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@email.com'
        }
    )
    print(json.dumps(result, indent=2))
    
    input("Press Enter to close...")
    web.cleanup()