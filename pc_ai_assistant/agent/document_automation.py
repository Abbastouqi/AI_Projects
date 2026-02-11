"""
Document Automation Module
Automates Google Docs and PowerPoint creation
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_google_doc(driver, title, content):
    """
    Create a new Google Doc with specified title and content
    
    Args:
        driver: Selenium WebDriver instance
        title: Document title
        content: Document content (can be string or list of paragraphs)
    """
    print(f"Creating Google Doc: {title}")
    
    # Navigate to Google Docs
    print("Opening Google Docs...")
    driver.get("https://docs.google.com/document/create")
    
    # Wait for document to load - increased timeout and better detection
    print("Waiting for document to load...")
    time.sleep(8)  # Give more time for page to load
    
    try:
        # Try multiple selectors for the document
        print("Looking for document editor...")
        
        # Check if we need to login
        if "accounts.google.com" in driver.current_url:
            print("⚠️ Google login required!")
            print("Please login to Google in the browser window")
            print("Waiting 30 seconds for manual login...")
            time.sleep(30)
            driver.get("https://docs.google.com/document/create")
            time.sleep(8)
        
        # Try to find the document canvas with multiple attempts
        doc_found = False
        for attempt in range(3):
            try:
                # Try different selectors
                if driver.find_elements(By.CLASS_NAME, "kix-page"):
                    doc_found = True
                    print("✅ Document loaded (kix-page found)")
                    break
                elif driver.find_elements(By.CSS_SELECTOR, ".docs-texteventtarget-iframe"):
                    doc_found = True
                    print("✅ Document loaded (iframe found)")
                    break
                elif driver.find_elements(By.ID, "docs-editor"):
                    doc_found = True
                    print("✅ Document loaded (editor found)")
                    break
                else:
                    print(f"Attempt {attempt + 1}: Document not ready, waiting...")
                    time.sleep(5)
            except Exception as e:
                print(f"Attempt {attempt + 1} error: {e}")
                time.sleep(5)
        
        if not doc_found:
            print("❌ Could not find document editor")
            print(f"Current URL: {driver.current_url}")
            print("Taking screenshot for debugging...")
            driver.save_screenshot("doc_error.png")
            raise Exception("Document editor not found. You may need to login to Google first.")
        
        # Set document title
        try:
            print("Setting document title...")
            title_elem = driver.find_element(By.CSS_SELECTOR, "input.docs-title-input")
            title_elem.click()
            time.sleep(0.5)
            title_elem.send_keys(Keys.CONTROL + "a")
            title_elem.send_keys(title)
            print(f"✅ Title set: {title}")
        except Exception as e:
            print(f"⚠️ Could not set title: {e}")
        
        time.sleep(1)
        
        # Click in the document body and add content
        print("Adding content to document...")
        try:
            # Try clicking on the page
            doc_body = driver.find_element(By.CLASS_NAME, "kix-page")
            doc_body.click()
            time.sleep(1)
        except:
            # Alternative: just start typing
            print("Using alternative method to add content...")
        
        # Type the content
        if isinstance(content, list):
            for i, paragraph in enumerate(content):
                print(f"Adding paragraph {i+1}/{len(content)}")
                driver.switch_to.active_element.send_keys(paragraph)
                driver.switch_to.active_element.send_keys(Keys.ENTER)
                driver.switch_to.active_element.send_keys(Keys.ENTER)
                time.sleep(0.3)
        else:
            driver.switch_to.active_element.send_keys(content)
        
        print("✅ Content added to document")
        print(f"✅ Google Doc created successfully: {title}")
        print(f"Document URL: {driver.current_url}")
        
        return driver.current_url
        
    except Exception as e:
        print(f"❌ Error creating Google Doc: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        raise


def create_google_slides(driver, title, slides_content):
    """
    Create a new Google Slides presentation
    
    Args:
        driver: Selenium WebDriver instance
        title: Presentation title
        slides_content: List of dicts with 'title' and 'content' for each slide
    """
    print(f"Creating Google Slides: {title}")
    
    # Navigate to Google Slides
    driver.get("https://docs.google.com/presentation/create")
    
    # Wait for presentation to load
    print("Waiting for presentation to load...")
    time.sleep(5)
    
    try:
        # Wait for the first slide
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "punch-viewer-container"))
        )
        print("✅ Presentation loaded")
        
        # Rename presentation
        try:
            title_elem = driver.find_element(By.CSS_SELECTOR, "input.docs-title-input")
            title_elem.click()
            title_elem.send_keys(Keys.CONTROL + "a")
            title_elem.send_keys(title)
            print(f"✅ Title set: {title}")
        except Exception as e:
            print(f"⚠️ Could not set title: {e}")
        
        time.sleep(1)
        
        # Add content to slides
        for i, slide in enumerate(slides_content):
            print(f"Adding content to slide {i+1}...")
            
            if i > 0:
                # Add new slide (Ctrl+M)
                driver.switch_to.active_element.send_keys(Keys.CONTROL + "m")
                time.sleep(2)
            
            # Click on the slide canvas
            try:
                canvas = driver.find_element(By.CLASS_NAME, "punch-viewer-container")
                canvas.click()
                time.sleep(0.5)
                
                # Add title
                if 'title' in slide:
                    driver.switch_to.active_element.send_keys(slide['title'])
                    driver.switch_to.active_element.send_keys(Keys.TAB)
                    time.sleep(0.3)
                
                # Add content
                if 'content' in slide:
                    if isinstance(slide['content'], list):
                        for point in slide['content']:
                            driver.switch_to.active_element.send_keys(point)
                            driver.switch_to.active_element.send_keys(Keys.ENTER)
                            time.sleep(0.2)
                    else:
                        driver.switch_to.active_element.send_keys(slide['content'])
                
                print(f"✅ Slide {i+1} completed")
                
            except Exception as e:
                print(f"⚠️ Error adding content to slide {i+1}: {e}")
        
        print(f"✅ Google Slides created successfully: {title}")
        return driver.current_url
        
    except Exception as e:
        print(f"❌ Error creating Google Slides: {e}")
        raise


def open_word_online(driver):
    """Open Microsoft Word Online"""
    print("Opening Microsoft Word Online...")
    driver.get("https://www.office.com/launch/word")
    time.sleep(5)
    print("✅ Word Online opened")


def create_powerpoint_online(driver, title, slides_content):
    """Create PowerPoint presentation online"""
    print(f"Creating PowerPoint Online: {title}")
    driver.get("https://www.office.com/launch/powerpoint")
    time.sleep(5)
    print("✅ PowerPoint Online opened")
    # Similar implementation to Google Slides


# Example usage templates
SAMPLE_DOC_CONTENT = [
    "Introduction",
    "This is a sample document created by PC AI Assistant.",
    "",
    "Main Content",
    "Here you can add your main content with multiple paragraphs.",
    "Each paragraph will be separated by a blank line.",
    "",
    "Conclusion",
    "This document was created automatically using browser automation."
]

SAMPLE_SLIDES_CONTENT = [
    {
        "title": "Welcome",
        "content": ["Introduction to the presentation", "Created by PC AI Assistant"]
    },
    {
        "title": "Main Points",
        "content": ["Point 1: First important topic", "Point 2: Second important topic", "Point 3: Third important topic"]
    },
    {
        "title": "Conclusion",
        "content": ["Summary of key points", "Thank you for your attention"]
    }
]
