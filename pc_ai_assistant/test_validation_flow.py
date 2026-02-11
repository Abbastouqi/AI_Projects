"""
Test the complete validation flow
"""
import yaml
from agent.policy_validator import validate_before_apply

# Load application data
with open("data/application.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print("=" * 60)
print("TESTING POLICY VALIDATION FLOW")
print("=" * 60)
print("\nApplication Data:")
print(f"  Name: {data.get('first_name')} {data.get('last_name')}")
print(f"  Email: {data.get('email')}")
print(f"  CNIC: {data.get('cnic')}")
print(f"  DOB: {data.get('dob')}")
print(f"  Mobile: {data.get('mobile')}")
print(f"  Program: {data.get('program1')}")
print(f"  Campus: {data.get('campus')}")

print("\n" + "=" * 60)
print("RUNNING VALIDATION")
print("=" * 60)

# Validate
result = validate_before_apply(data)

# Print report
print(result['report'])

# Print summary
print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)
print(f"Valid: {result['is_valid']}")
print(f"Errors: {len(result['errors'])}")
print(f"Warnings: {len(result['warnings'])}")
print(f"Info: {len(result['info'])}")

if result['errors']:
    print("\nErrors:")
    for error in result['errors']:
        print(f"  - {error}")

if result['warnings']:
    print("\nWarnings:")
    for warning in result['warnings']:
        print(f"  - {warning}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
