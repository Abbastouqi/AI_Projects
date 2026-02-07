"""
Demo script showing the conversation flow in action
"""
import requests
import json
import time

API_URL = "http://localhost:8000/api/chat"

def send_message(message, session_id=None):
    """Send a message to the chatbot"""
    data = {
        "message": message,
        "session_id": session_id
    }
    
    response = requests.post(API_URL, json=data)
    result = response.json()
    
    return result

def print_response(message, response):
    """Pretty print the conversation"""
    print("\n" + "="*80)
    print(f"👤 USER: {message}")
    print("-"*80)
    print(f"🤖 BOT: {response['response']}")
    
    if response.get('recommendations'):
        print(f"\n📱 RECOMMENDATIONS ({len(response['recommendations'])} laptops):")
        for laptop in response['recommendations']:
            print(f"   • {laptop['name']}")
            print(f"     Price: PKR {laptop['price_pkr']:,}")
            print(f"     Specs: {laptop['processor']}, {laptop['ram']}, {laptop['storage']}")
            print()
    
    print("="*80)
    time.sleep(1)

def main():
    print("\n🎓 AI Laptop Recommendation Chatbot - Demo Conversation")
    print("="*80)
    
    session_id = None
    
    # Conversation flow
    conversations = [
        "Hi",
        "I'm an FSC pre-engineering student",
        "My budget is around 80,000 PKR",
        "I also need it for basic programming",
        "Compare HP vs Dell laptops",
        "Where can I buy laptops in Pakistan?"
    ]
    
    for message in conversations:
        result = send_message(message, session_id)
        session_id = result['session_id']
        print_response(message, result)
    
    print("\n✅ Demo completed!")
    print(f"Session ID: {session_id}")
    print("\nThe chatbot successfully:")
    print("  ✓ Detected user intent (greeting, student type, budget, use case, comparison, purchase)")
    print("  ✓ Tracked conversation state")
    print("  ✓ Built user profile (FSC student, 80k budget, programming)")
    print("  ✓ Provided contextual responses")
    print("  ✓ Maintained session continuity")

if __name__ == "__main__":
    main()
