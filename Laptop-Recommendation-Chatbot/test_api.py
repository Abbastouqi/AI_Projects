import requests
import json

# Test the chat API
url = "http://localhost:8000/api/chat"
data = {
    "message": "Hi, I'm an FSC student with a budget of 80k PKR",
    "session_id": None
}

print("Testing Chat API...")
print(f"Request: {data['message']}\n")

response = requests.post(url, json=data)
result = response.json()

print(f"Response: {result['response'][:200]}...")
print(f"\nSession ID: {result['session_id']}")

if result.get('recommendations'):
    print(f"\nRecommendations: {len(result['recommendations'])} laptops")
    for laptop in result['recommendations']:
        print(f"  - {laptop['name']}: PKR {laptop['price_pkr']:,}")
