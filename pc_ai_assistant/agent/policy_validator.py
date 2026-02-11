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
        
        # Run all validations
        self.validate_personal_info(application_data)
        self.validate_contact_info(application_data)
        self.validate_academic_info(application_data)
        self.validate_eligibility(application_data)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings, self.info
    
    def validate_personal_info(self, data: Dict):
        """Validate personal information against policies"""
        
        # Name validation
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        if not first_name:
            self.errors.append("❌ First name is required (Policy: Personal Information)")
        elif len(first_name) < 2:
            self.errors.append("❌ First name must be at least 2 characters")
        
        if not last_name:
            self.warnings.append("⚠️ Last name is recommended for official records")
        
        # CNIC validation (Pakistan)
        cnic = data.get('cnic', '').strip()
        if cnic:
            # Remove dashes and spaces
            cnic_clean = re.sub(r'[-\s]', '', cnic)
            if not re.match(r'^\d{13}$', cnic_clean):
                self.errors.append("❌ CNIC must be 13 digits (Policy: Identification)")
            else:
                self.info.append("✅ CNIC format valid")
        else:
            self.errors.append("❌ CNIC is required for Pakistani nationals")
        
        # Date of Birth validation
        dob = data.get('dob', '')
        if dob:
            try:
                dob_date = datetime.strptime(dob, '%Y-%m-%d')
                age = (datetime.now() - dob_date).days // 365
                
                if age < 16:
                    self.errors.append("❌ Minimum age requirement: 16 years (Policy: Admission)")
                elif age > 35:
                    self.warnings.append("⚠️ Age above typical range. Special consideration may be needed")
                else:
                    self.info.append(f"✅ Age: {age} years - Eligible")
            except:
                self.errors.append("❌ Invalid date of birth format (use YYYY-MM-DD)")
        else:
            self.errors.append("❌ Date of birth is required")
        
        # Gender validation
        gender = data.get('gender', '')
        if gender not in ['Male', 'Female', 'Other']:
            self.errors.append("❌ Gender must be specified (Policy: Personal Information)")
    
    def validate_contact_info(self, data: Dict):
        """Validate contact information"""
        
        # Email validation
        email = data.get('email', '').strip()
        if not email:
            self.errors.append("❌ Email is required (Policy: Communication)")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.errors.append("❌ Invalid email format")
        else:
            self.info.append("✅ Email format valid")
        
        # Mobile validation (Pakistan format)
        mobile = data.get('mobile', '').strip()
        if not mobile:
            self.errors.append("❌ Mobile number is required (Policy: Communication)")
        else:
            mobile_clean = re.sub(r'[-\s+]', '', mobile)
            # Pakistan mobile: 03XXXXXXXXX (11 digits) or 923XXXXXXXXX (12 digits with country code)
            if not re.match(r'^(92)?0?3\d{9}$', mobile_clean):
                self.errors.append("❌ Invalid Pakistan mobile format (03XXXXXXXXX)")
            else:
                self.info.append("✅ Mobile number format valid")
        
        # Address validation
        address = data.get('address', '').strip()
        if not address or len(address) < 10:
            self.errors.append("❌ Complete address is required (Policy: Contact Information)")
    
    def validate_academic_info(self, data: Dict):
        """Validate academic information"""
        
        # Last institute
        last_institute = data.get('last_institute', '').strip()
        if not last_institute:
            self.warnings.append("⚠️ Last institute name is recommended")
        
        # Program selection
        program = data.get('program1', '').strip()
        if not program:
            self.errors.append("❌ Program selection is required (Policy: Admission)")
        else:
            self.info.append(f"✅ Selected program: {program}")
        
        # Campus selection
        campus = data.get('campus', '').strip()
        if not campus:
            self.errors.append("❌ Campus selection is required")
        
        # Level selection
        level = data.get('level', '').strip()
        if not level:
            self.errors.append("❌ Program level is required (Undergraduate/Graduate)")
    
    def validate_eligibility(self, data: Dict):
        """Validate eligibility criteria"""
        
        # Nationality check
        nationality = data.get('nationality', '').strip()
        if not nationality:
            self.errors.append("❌ Nationality is required (Policy: Eligibility)")
        
        # Check for required documents (informational)
        self.info.append("📋 Required Documents:")
        self.info.append("   - CNIC/B-Form copy")
        self.info.append("   - Educational certificates")
        self.info.append("   - Passport size photographs")
        
        # Policy reminders
        self.info.append("📖 Policy Reminders:")
        self.info.append("   - Attendance: Minimum 75% required")
        self.info.append("   - Medium: English language proficiency needed")
        self.info.append("   - Merit-based: Selection is purely merit-based")
    
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
