# agent/form_validator.py
"""Validate that all required form fields are filled before submission."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def validate_form(driver):
    """Check if all required fields are filled."""
    errors = []

    required_inputs = {
        "input[name='fname']": "First Name",
        "input[name='lname']": "Last Name",
        "input[name='cnic']": "CNIC",
        "#addressline1": "Address",
        "#Email": "Email",
        "input[name='mobile']": "Mobile",
        "#phone1": "Alternate Phone",
        "#DOB": "Date of Birth",
    }

    for selector, label in required_inputs.items():
        try:
            value = driver.find_element(By.CSS_SELECTOR, selector).get_attribute("value") or ""
            value = value.strip()
            if not value:
                errors.append(f"❌ {label} is empty")
            else:
                print(f"✅ {label}: {value[:30]}")
        except Exception as e:
            errors.append(f"❌ {label} not found or error: {e}")

    required_selects = {
        "#branch": "Campus",
        "#ptype": "Level",
        "#programid": "Program",
        "#gender": "Gender",
        "#country1": "Country",
        "#pcity1": "City",
        "select[name='aboutus']": "How did you know about us",
        "#nationality": "Nationality",
    }

    for selector, label in required_selects.items():
        try:
            elem = driver.find_element(By.CSS_SELECTOR, selector)
            if elem.tag_name.lower() == "select":
                selected = Select(elem).first_selected_option.get_attribute("value") or ""
            else:
                selected = driver.execute_script(
                    "const e=arguments[0]; return e.getAttribute('value') || e.textContent || '';",
                    elem,
                )
            if selected and str(selected).strip():
                print(f"✅ {label}: {str(selected).strip()[:30]}")
            else:
                errors.append(f"❌ {label} is not selected")
        except Exception as e:
            errors.append(f"❌ {label} not found or error: {e}")

    return errors


def check_and_report(driver):
    """Validate form and print results."""
    errors = validate_form(driver)

    if errors:
        print("\n" + "=" * 60)
        print("FORM VALIDATION ERRORS:")
        print("=" * 60)
        for error in errors:
            print(error)
        print("=" * 60)
        raise RuntimeError(f"Form validation failed: {len(errors)} field(s) not filled")
    else:
        print("\n✅ All required fields are filled correctly!")
