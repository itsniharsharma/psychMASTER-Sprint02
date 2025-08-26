#!/usr/bin/env python3
"""
Comprehensive End-to-End Test for Different Psychological States
"""

import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_conversation_type(conversation_type, messages):
    print(f"\n🧠 Testing {conversation_type.upper()} Conversation")
    print("=" * 50)
    
    # Create session
    session_response = requests.post(f"{BASE_URL}/chat/session", json={"action": "create"})
    session_id = session_response.json()['session_id']
    print(f"Session created: {session_id[:8]}...")
    
    # Send messages
    for i, message in enumerate(messages, 1):
        payload = {"message": message, "session_id": session_id}
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        data = response.json()
        print(f"Message {i}: Crisis detected: {data.get('is_crisis', False)}")
    
    # End session and get analysis
    end_payload = {"session_id": session_id}
    end_response = requests.post(f"{BASE_URL}/chat/end-session", json=end_payload)
    
    if end_response.status_code == 200:
        result = end_response.json()
        analysis = result.get('analysis', {})
        recommendations = result.get('recommendations', {})
        
        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"Predicted State: {analysis.get('predicted_state')}")
        print(f"Confidence: {analysis.get('confidence', 0):.2f}")
        print(f"Risk Level: {analysis.get('risk_level')}")
        print(f"Total Messages: {analysis.get('total_messages')}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"YouTube Videos: {len(recommendations.get('youtube_videos', []))}")
        print(f"Articles: {len(recommendations.get('articles', []))}")
        print(f"Professional Resources: {len(recommendations.get('professional_resources', []))}")
        
        # Show personalized message
        print(f"\n📝 Personalized Message:")
        print(f"{recommendations.get('personalized_message', 'N/A')}")
        
        return True
    else:
        print(f"❌ Failed to end session: {end_response.status_code}")
        return False

# Test scenarios
scenarios = {
    "Normal": [
        "Hi, I'm doing pretty well today, just wanted to chat about general wellness",
        "I've been maintaining good habits like exercise and sleep",
        "Sometimes I feel stressed but I manage it well with meditation"
    ],
    
    "Anxiety": [
        "I'm feeling really anxious and worried about everything lately",
        "My heart races and I feel restless, especially about work presentations",
        "I can't stop overthinking and it's affecting my sleep",
        "I feel overwhelmed and nervous about the future"
    ],
    
    "Depression": [
        "I feel so hopeless and empty, like nothing matters anymore",
        "I'm exhausted all the time and have no motivation",
        "I feel worthless and isolated from everyone",
        "Everything feels pointless and I can't find joy in anything"
    ],
    
    "Crisis": [
        "I feel like I want to die, everything is too much",
        "I'm thinking about suicide because I can't handle this pain",
        "I want to hurt myself, nothing seems worth living for",
        "Life feels meaningless and I don't want to be here anymore"
    ]
}

# Run tests
print("🧠 psychMASTER Comprehensive Psychological Analysis Testing")
print("=" * 60)

results = {}
for conv_type, messages in scenarios.items():
    success = test_conversation_type(conv_type, messages)
    results[conv_type] = success

# Summary
print("\n" + "=" * 60)
print("COMPREHENSIVE TEST SUMMARY")
print("=" * 60)
for conv_type, success in results.items():
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {conv_type} conversation analysis")

total_passed = sum(results.values())
print(f"\nOverall: {total_passed}/{len(results)} conversation types analyzed successfully")