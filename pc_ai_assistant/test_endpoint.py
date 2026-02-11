"""Test the application/data endpoint"""
import requests
import json

print("Testing /application/data endpoint...")
try:
    response = requests.get("http://127.0.0.1:5000/application/data")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Application data retrieved:")
        print(json.dumps(data, indent=2))
    else:
        print(f"\n❌ ERROR: {response.text}")
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")

print("\n" + "=" * 60)
print("Testing /validate/application endpoint...")
try:
    test_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'cnic': '3520212345678',
        'dob': '2000-05-15',
        'gender': 'Male',
        'email': 'test@example.com',
        'mobile': '03001234567',
        'address': 'Test Address 123',
        'nationality': 'Pakistan',
        'last_institute': 'Test College',
        'program1': 'BS Computer Science',
        'campus': 'Islamabad',
        'level': 'Undergraduate'
    }
    
    response = requests.post("http://127.0.0.1:5000/validate/application", json=test_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! Validation result:")
        print(f"Valid: {result.get('is_valid')}")
        print(f"Errors: {len(result.get('errors', []))}")
        print(f"Warnings: {len(result.get('warnings', []))}")
    else:
        print(f"\n❌ ERROR: {response.text}")
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
