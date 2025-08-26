#!/usr/bin/env python3
"""
Quick test to verify crisis detection keywords
"""

import requests

BASE_URL = "http://localhost:8001/api"

def test_crisis_message(message):
    # Create session
    session_response = requests.post(f"{BASE_URL}/chat/session", json={"action": "create"})
    session_id = session_response.json()['session_id']
    
    # Send message
    payload = {"message": message, "session_id": session_id}
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    data = response.json()
    
    print(f"Message: {message}")
    print(f"Crisis detected: {data.get('is_crisis', False)}")
    print(f"Response preview: {data.get('response', '')[:100]}...")
    print("-" * 50)

# Test messages
messages = [
    "I don't want to live anymore, everything feels pointless",
    "I want to die, I can't take this anymore", 
    "I'm thinking about suicide",
    "I want to hurt myself",
    "I'm going to kill myself"
]

for msg in messages:
    test_crisis_message(msg)