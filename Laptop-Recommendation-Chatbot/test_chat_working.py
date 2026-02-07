"""
Test script to verify the chatbot is working correctly
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{API_URL}/api/health")
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    try:
        payload = {
            "message": "Hi, I need a laptop for programming under 80,000 PKR",
            "session_id": "test_session_123"
        }
        
        response = requests.post(
            f"{API_URL}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Chat endpoint is working!")
            print(f"\n🤖 Bot Response:\n{data['response'][:200]}...")
            
            if data.get('recommendations'):
                print(f"\n💻 Recommendations: {len(data['recommendations'])} laptops found")
                for laptop in data['recommendations'][:2]:
                    print(f"  - {laptop['name']} - PKR {laptop['price_pkr']:,}")
            
            return True
        else:
            print(f"❌ Chat endpoint returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_laptops():
    """Test laptops endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/laptops")
        
        if response.status_code == 200:
            laptops = response.json()
            print(f"\n✅ Laptops endpoint working! Found {len(laptops)} laptops in database")
            return True
        else:
            print(f"❌ Laptops endpoint returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Laptops test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTING LAPTOP CHATBOT")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n[Test 1] Checking backend health...")
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ Backend is not running!")
        print("Please start it with: python backend/main.py")
        exit(1)
    
    # Test 2: Chat endpoint
    print("\n[Test 2] Testing chat endpoint...")
    chat_ok = test_chat()
    
    # Test 3: Laptops endpoint
    print("\n[Test 3] Testing laptops endpoint...")
    laptops_ok = test_laptops()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Chat Endpoint: {'✅ PASS' if chat_ok else '❌ FAIL'}")
    print(f"Laptops Endpoint: {'✅ PASS' if laptops_ok else '❌ FAIL'}")
    
    if health_ok and chat_ok and laptops_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n📝 Next Steps:")
        print("1. Open 'simple-chat.html' in your browser")
        print("2. Start chatting with the bot!")
        print("3. Try: 'I need a laptop for programming under 80,000 PKR'")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    print("=" * 60)
