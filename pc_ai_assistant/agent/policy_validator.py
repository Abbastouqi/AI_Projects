"""
Policy Validator for Application Automation
Validates application data against university policies
"""
from datetime import datetime
from typing import Dict, List, Tuple
import re

class PolicyValidator:
    """Validates application data against university policies"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate_all(self, application_data: Dict) -> Tuple[bool, List[str], List[str], List[str]]:
        """
        Validate all application data against policies
        Returns: (is_valid, errors, warnings, info)
        """
        self.errors = []
        self.warnings = []
        self.info = []
        
        print("\n" + "=" * 70)
        print("🔍 POLICY VALIDATION STARTED")
        print("=" * 70)
        
        # Run all validations
        self.validate_personal_info(application_data)
        self.validate_contact_info(application_data)
        self.validate_academic_info(application_data)
        self.validate_eligibility(application_data)
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        
        is_valid = len(self.errors) == 0
        
        if is_valid:
            print("✅ ALL POLICIES PASSED")
            print(f"   • Errors: {len(self.errors)}")
            print(f"   • Warnings: {len(self.warnings)}")
            print(f"   • Info: {len(self.info)}")
            print("\n✅ APPLICATION IS READY FOR SUBMISSION")
        else:
            print("❌ VALIDATION FAILED")
            print(f"   • Errors: {len(self.errors)} (must fix)")
            print(f"   • Warnings: {len(self.warnings)} (review recommended)")
            print(f"   • Info: {len(self.info)}")
            print("\n❌ PLEASE FIX ERRORS BEFORE SUBMISSION")
        
        print("=" * 70 + "\n")
        
        return is_valid, self.errors, self.warnings, self.info
    
    def validate_personal_info(self, data: Dict):
        """Validate personal information against policies"""
        
        print("\n📋 Checking Personal Information Policies...")
        
        # Name validation
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        print("   → Policy: Personal Information - Name Requirements")
        if not first_name:
            self.errors.append("❌ First name is required (Policy: Personal Information)")
            print("      ❌ FAILED: First name missing")
        elif len(first_name) < 2:
            self.errors.append("❌ First name must be at least 2 characters")
            print("      ❌ FAILED: First name too short")
        else:
            print(f"      ✅ PASSED: First name valid ({first_name})")
        
        if not last_name:
            self.warnings.append("⚠️ Last name is recommended for official records")
            print("      ⚠️  WARNING: Last name missing (recommended)")
        else:
            print(f"      ✅ PASSED: Last name provided ({last_name})")
        
        # CNIC validation (Pakistan)
        cnic = data.get('cnic', '').strip()
        print("   → Policy: Identification - CNIC Requirements")
        if cnic:
            # Remove dashes and spaces
            cnic_clean = re.sub(r'[-\s]', '', cnic)
            if not re.match(r'^\d{13}$', cnic_clean):
                self.errors.append("❌ CNIC must be 13 digits (Policy: Identification)")
                print(f"      ❌ FAILED: CNIC format invalid ({cnic})")
            else:
                self.info.append("✅ CNIC format valid")
                print(f"      ✅ PASSED: CNIC format valid ({cnic})")
        else:
            self.errors.append("❌ CNIC is required for Pakistani nationals")
            print("      ❌ FAILED: CNIC missing")
        
        # Date of Birth validation
        dob = data.get('dob', '')
        print("   → Policy: Admission - Age Requirements (16-35 years)")
        if dob:
            try:
                dob_date = datetime.strptime(dob, '%Y-%m-%d')
                age = (datetime.now() - dob_date).days // 365
                
                if age < 16:
                    self.errors.append("❌ Minimum age requirement: 16 years (Policy: Admission)")
                    print(f"      ❌ FAILED: Age {age} below minimum (16)")
                elif age > 35:
                    self.warnings.append("⚠️ Age above typical range. Special consideration may be needed")
                    print(f"      ⚠️  WARNING: Age {age} above typical range")
                else:
                    self.info.append(f"✅ Age: {age} years - Eligible")
                    print(f"      ✅ PASSED: Age {age} within eligible range")
            except:
                self.errors.append("❌ Invalid date of birth format (use YYYY-MM-DD)")
                print(f"      ❌ FAILED: Invalid DOB format ({dob})")
        else:
            self.errors.append("❌ Date of birth is required")
            print("      ❌ FAILED: DOB missing")
        
        # Gender validation
        gender = data.get('gender', '')
        print("   → Policy: Personal Information - Gender")
        if gender not in ['Male', 'Female', 'Other']:
            self.errors.append("❌ Gender must be specified (Policy: Personal Information)")
            print("      ❌ FAILED: Gender not specified")
        else:
            print(f"      ✅ PASSED: Gender specified ({gender})")
    
    def validate_contact_info(self, data: Dict):
        """Validate contact information"""
        
        print("\n📋 Checking Contact Information Policies...")
        
        # Email validation
        email = data.get('email', '').strip()
        print("   → Policy: Communication - Email Requirements")
        if not email:
            self.errors.append("❌ Email is required (Policy: Communication)")
            print("      ❌ FAILED: Email missing")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.errors.append("❌ Invalid email format")
            print(f"      ❌ FAILED: Invalid email format ({email})")
        else:
            self.info.append("✅ Email format valid")
            print(f"      ✅ PASSED: Email format valid ({email})")
        
        # Mobile validation (Pakistan format)
        mobile = data.get('mobile', '').strip()
        print("   → Policy: Communication - Mobile Number Requirements")
        if not mobile:
            self.errors.append("❌ Mobile number is required (Policy: Communication)")
            print("      ❌ FAILED: Mobile number missing")
        else:
            mobile_clean = re.sub(r'[-\s+]', '', mobile)
            # Pakistan mobile: 03XXXXXXXXX (11 digits) or 923XXXXXXXXX (12 digits with country code)
            if not re.match(r'^(92)?0?3\d{9}$', mobile_clean):
                self.errors.append("❌ Invalid Pakistan mobile format (03XXXXXXXXX)")
                print(f"      ❌ FAILED: Invalid mobile format ({mobile})")
            else:
                self.info.append("✅ Mobile number format valid")
                print(f"      ✅ PASSED: Mobile format valid ({mobile})")
        
        # Address validation
        address = data.get('address', '').strip()
        print("   → Policy: Contact Information - Address Requirements")
        if not address or len(address) < 10:
            self.errors.append("❌ Complete address is required (Policy: Contact Information)")
            print("      ❌ FAILED: Address missing or incomplete")
        else:
            print(f"      ✅ PASSED: Address provided ({len(address)} chars)")
    
    def validate_academic_info(self, data: Dict):
        """Validate academic information"""
        
        print("\n📋 Checking Academic Information Policies...")
        
        # Last institute
        last_institute = data.get('last_institute', '').strip()
        print("   → Policy: Academic History - Last Institute")
        if not last_institute:
            self.warnings.append("⚠️ Last institute name is recommended")
            print("      ⚠️  WARNING: Last institute not provided (recommended)")
        else:
            print(f"      ✅ PASSED: Last institute provided ({last_institute})")
        
        # Program selection
        program = data.get('program1', '').strip()
        print("   → Policy: Admission - Program Selection")
        if not program:
            self.errors.append("❌ Program selection is required (Policy: Admission)")
            print("      ❌ FAILED: Program not selected")
        else:
            self.info.append(f"✅ Selected program: {program}")
            print(f"      ✅ PASSED: Program selected ({program})")
        
        # Campus selection
        campus = data.get('campus', '').strip()
        print("   → Policy: Admission - Campus Selection")
        if not campus:
            self.errors.append("❌ Campus selection is required")
            print("      ❌ FAILED: Campus not selected")
        else:
            print(f"      ✅ PASSED: Campus selected ({campus})")
        
        # Level selection
        level = data.get('level', '').strip()
        print("   → Policy: Admission - Program Level")
        if not level:
            self.errors.append("❌ Program level is required (Undergraduate/Graduate)")
            print("      ❌ FAILED: Program level not selected")
        else:
            print(f"      ✅ PASSED: Program level selected ({level})")
    
    def validate_eligibility(self, data: Dict):
        """Validate eligibility criteria"""
        
        print("\n📋 Checking Eligibility Policies...")
        
        # Nationality check
        nationality = data.get('nationality', '').strip()
        print("   → Policy: Eligibility - Nationality Requirements")
        if not nationality:
            self.errors.append("❌ Nationality is required (Policy: Eligibility)")
            print("      ❌ FAILED: Nationality not specified")
        else:
            print(f"      ✅ PASSED: Nationality specified ({nationality})")
        
        # Check for required documents (informational)
        print("\n   → Policy: Documentation Requirements")
        self.info.append("📋 Required Documents:")
        self.info.append("   - CNIC/B-Form copy")
        self.info.append("   - Educational certificates")
        self.info.append("   - Passport size photographs")
        print("      ℹ️  Required: CNIC/B-Form copy")
        print("      ℹ️  Required: Educational certificates")
        print("      ℹ️  Required: Passport size photographs")
        
        # Policy reminders
        print("\n   → University Policies - Important Reminders")
        self.info.append("📖 Policy Reminders:")
        self.info.append("   - Attendance: Minimum 75% required")
        self.info.append("   - Medium: English language proficiency needed")
        self.info.append("   - Merit-based: Selection is purely merit-based")
        print("      ℹ️  Attendance Policy: Minimum 75% required")
        print("      ℹ️  Medium of Instruction: English proficiency needed")
        print("      ℹ️  Selection Policy: Purely merit-based")
    
    def get_validation_report(self) -> str:
        """Get formatted validation report"""
        report = "=" * 60 + "\n"
        report += "APPLICATION VALIDATION REPORT\n"
        report += "=" * 60 + "\n\n"
        
        if self.errors:
            report += "❌ ERRORS (Must Fix):\n"
            for error in self.errors:
                report += f"   {error}\n"
            report += "\n"
        
        if self.warnings:
            report += "⚠️  WARNINGS (Review Recommended):\n"
            for warning in self.warnings:
                report += f"   {warning}\n"
            report += "\n"
        
        if self.info:
            report += "ℹ️  INFORMATION:\n"
            for info in self.info:
                report += f"   {info}\n"
            report += "\n"
        
        if not self.errors:
            report += "✅ APPLICATION READY FOR SUBMISSION\n"
            report += "All required fields validated successfully.\n"
        else:
            report += "❌ APPLICATION NOT READY\n"
            report += f"Please fix {len(self.errors)} error(s) before submission.\n"
        
        report += "\n" + "=" * 60
        return report


def validate_before_apply(application_data: Dict) -> Dict:
    """
    Validate application data before automation
    Returns validation results
    """
    validator = PolicyValidator()
    is_valid, errors, warnings, info = validator.validate_all(application_data)
    
    return {
        'is_valid': is_valid,
        'can_proceed': is_valid,
        'errors': errors,
        'warnings': warnings,
        'info': info,
        'report': validator.get_validation_report()
    }


def check_policy_compliance(field_name: str, field_value: str) -> Dict:
    """
    Check if a specific field complies with policies
    Returns compliance status and message
    """
    compliance = {
        'compliant': True,
        'message': '',
        'policy': ''
    }
    
    # Field-specific policy checks
    if field_name == 'email':
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', field_value):
            compliance['compliant'] = False
            compliance['message'] = 'Invalid email format'
            compliance['policy'] = 'Communication Policy'
    
    elif field_name == 'mobile':
        mobile_clean = re.sub(r'[-\s+]', '', field_value)
        # Pakistan mobile: 03XXXXXXXXX (11 digits) or 923XXXXXXXXX (12 digits with country code)
        if not re.match(r'^(92)?0?3\d{9}$', mobile_clean):
            compliance['compliant'] = False
            compliance['message'] = 'Invalid Pakistan mobile format'
            compliance['policy'] = 'Contact Information Policy'
    
    elif field_name == 'cnic':
        cnic_clean = re.sub(r'[-\s]', '', field_value)
        if not re.match(r'^\d{13}$', cnic_clean):
            compliance['compliant'] = False
            compliance['message'] = 'CNIC must be 13 digits'
            compliance['policy'] = 'Identification Policy'
    
    elif field_name == 'age':
        try:
            age = int(field_value)
            if age < 16:
                compliance['compliant'] = False
                compliance['message'] = 'Minimum age requirement: 16 years'
                compliance['policy'] = 'Admission Policy'
        except:
            compliance['compliant'] = False
            compliance['message'] = 'Invalid age value'
    
    return compliance


if __name__ == "__main__":
    # Test validation
    test_data = {
        'first_name': 'Touqeer',
        'last_name': 'Abbas',
        'cnic': '3520212345678',
        'dob': '2000-05-15',
        'gender': 'Male',
        'email': 'test@example.com',
        'mobile': '03022994771',
        'address': 'House 12 Street 5 Islamabad',
        'nationality': 'Pakistan',
        'last_institute': 'Punjab College',
        'program1': 'BS Computer Science',
        'campus': 'Islamabad/Rawalpindi',
        'level': 'Undergraduate'
    }
    
    result = validate_before_apply(test_data)
    print(result['report'])
