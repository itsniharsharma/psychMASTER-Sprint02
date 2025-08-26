#!/usr/bin/env python3
"""
Comprehensive Backend Testing for psychMASTER Psychological Analysis Features
Tests the new psychological analysis system, session management, and recommendation system.
"""

import requests
import json
import time
import sys
from typing import Dict, List, Optional

# Configuration
BASE_URL = "http://localhost:8001/api"
TIMEOUT = 30

class PsychMASTERTester:
    def __init__(self):
        self.session_id = None
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success:
            self.failed_tests.append(test_name)
    
    def test_health_check(self) -> bool:
        """Test if the backend is running and healthy"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                langchain_init = data.get('langchain_initialized', False)
                
                self.log_test(
                    "Health Check", 
                    True, 
                    f"Status: {data.get('status')}, LangChain: {langchain_init}"
                )
                return True
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_create_session(self) -> bool:
        """Test creating a new chat session"""
        try:
            payload = {"action": "create"}
            response = requests.post(f"{BASE_URL}/chat/session", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get('session_id')
                
                if self.session_id:
                    self.log_test(
                        "Create Session", 
                        True, 
                        f"Session ID: {self.session_id[:8]}..."
                    )
                    return True
                else:
                    self.log_test("Create Session", False, "No session_id in response")
                    return False
            else:
                self.log_test("Create Session", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Create Session", False, f"Error: {str(e)}")
            return False
    
    def send_chat_message(self, message: str, expected_crisis: bool = False) -> Optional[Dict]:
        """Send a chat message and return the response"""
        try:
            payload = {
                "message": message,
                "session_id": self.session_id
            }
            response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                is_crisis = data.get('is_crisis', False)
                
                # Verify crisis detection if expected
                crisis_match = is_crisis == expected_crisis
                
                self.log_test(
                    f"Chat Message: '{message[:30]}...'", 
                    True, 
                    f"Crisis detected: {is_crisis}, Expected: {expected_crisis}, Match: {crisis_match}"
                )
                return data
            else:
                self.log_test(f"Chat Message: '{message[:30]}...'", False, f"Status code: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test(f"Chat Message: '{message[:30]}...'", False, f"Error: {str(e)}")
            return None
    
    def test_conversation_scenarios(self) -> bool:
        """Test different conversation scenarios to build conversation history"""
        scenarios = [
            # Normal conversation
            {
                "message": "Hi, I'm feeling okay today but wanted to chat about managing daily stress at work",
                "expected_crisis": False,
                "type": "normal"
            },
            {
                "message": "I've been having some challenges with work-life balance lately, but I'm managing",
                "expected_crisis": False,
                "type": "normal"
            },
            
            # Anxious conversation
            {
                "message": "I'm really worried about everything lately, can't sleep well, feeling restless and overwhelmed",
                "expected_crisis": False,
                "type": "anxiety"
            },
            {
                "message": "My heart races when I think about upcoming presentations, I feel nervous and panicky",
                "expected_crisis": False,
                "type": "anxiety"
            },
            
            # Depressed conversation
            {
                "message": "I feel so hopeless and empty lately, nothing seems to matter anymore, I'm exhausted all the time",
                "expected_crisis": False,
                "type": "depression"
            },
            {
                "message": "I've been feeling really down and isolated, like I'm worthless and nothing will get better",
                "expected_crisis": False,
                "type": "depression"
            }
        ]
        
        success_count = 0
        for scenario in scenarios:
            result = self.send_chat_message(scenario["message"], scenario["expected_crisis"])
            if result:
                success_count += 1
        
        overall_success = success_count == len(scenarios)
        self.log_test(
            "Conversation Scenarios", 
            overall_success, 
            f"Successful messages: {success_count}/{len(scenarios)}"
        )
        return overall_success
    
    def test_crisis_detection(self) -> bool:
        """Test crisis message detection"""
        crisis_messages = [
            "I don't want to live anymore, everything feels pointless and I'm thinking about ending it all",
            "I want to hurt myself, I can't take this pain anymore",
            "I'm thinking about suicide, I feel like everyone would be better off without me"
        ]
        
        success_count = 0
        for message in crisis_messages:
            result = self.send_chat_message(message, expected_crisis=True)
            if result and result.get('is_crisis'):
                success_count += 1
        
        overall_success = success_count == len(crisis_messages)
        self.log_test(
            "Crisis Detection", 
            overall_success, 
            f"Crisis messages detected: {success_count}/{len(crisis_messages)}"
        )
        return overall_success
    
    def test_end_session_analysis(self) -> bool:
        """Test ending session and getting psychological analysis"""
        try:
            if not self.session_id:
                self.log_test("End Session Analysis", False, "No active session")
                return False
            
            payload = {"session_id": self.session_id}
            response = requests.post(f"{BASE_URL}/chat/end-session", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ['success', 'session_id', 'analysis', 'recommendations', 'session_summary']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "End Session Analysis", 
                        False, 
                        f"Missing fields: {missing_fields}"
                    )
                    return False
                
                # Verify analysis structure
                analysis = data.get('analysis', {})
                analysis_success = self.verify_analysis_structure(analysis)
                
                # Verify recommendations structure
                recommendations = data.get('recommendations', {})
                recommendations_success = self.verify_recommendations_structure(recommendations)
                
                overall_success = analysis_success and recommendations_success
                
                self.log_test(
                    "End Session Analysis", 
                    overall_success, 
                    f"Analysis valid: {analysis_success}, Recommendations valid: {recommendations_success}"
                )
                
                # Print detailed analysis results for verification
                if overall_success:
                    self.print_analysis_details(analysis, recommendations)
                
                return overall_success
            else:
                self.log_test("End Session Analysis", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("End Session Analysis", False, f"Error: {str(e)}")
            return False
    
    def verify_analysis_structure(self, analysis: Dict) -> bool:
        """Verify the psychological analysis structure"""
        required_fields = [
            'predicted_state', 'confidence', 'risk_level', 
            'analysis_timestamp', 'total_messages'
        ]
        
        # Check required fields
        missing_fields = [field for field in required_fields if field not in analysis]
        if missing_fields:
            self.log_test(
                "Analysis Structure", 
                False, 
                f"Missing analysis fields: {missing_fields}"
            )
            return False
        
        # Verify predicted_state is valid
        valid_states = ['Normal', 'Depression', 'Bipolar', 'Anxiety', 'Suicidal']
        predicted_state = analysis.get('predicted_state')
        if predicted_state not in valid_states:
            self.log_test(
                "Analysis Structure", 
                False, 
                f"Invalid predicted_state: {predicted_state}. Must be one of {valid_states}"
            )
            return False
        
        # Verify confidence is between 0-1
        confidence = analysis.get('confidence', 0)
        if not (0 <= confidence <= 1):
            self.log_test(
                "Analysis Structure", 
                False, 
                f"Invalid confidence: {confidence}. Must be between 0-1"
            )
            return False
        
        # Verify risk_level is valid
        valid_risk_levels = ['low', 'medium', 'high']
        risk_level = analysis.get('risk_level')
        if risk_level not in valid_risk_levels:
            self.log_test(
                "Analysis Structure", 
                False, 
                f"Invalid risk_level: {risk_level}. Must be one of {valid_risk_levels}"
            )
            return False
        
        self.log_test(
            "Analysis Structure", 
            True, 
            f"State: {predicted_state}, Confidence: {confidence:.2f}, Risk: {risk_level}"
        )
        return True
    
    def verify_recommendations_structure(self, recommendations: Dict) -> bool:
        """Verify the recommendations structure"""
        required_fields = [
            'primary_concern', 'risk_level', 'youtube_videos', 
            'articles', 'professional_resources', 'personalized_message'
        ]
        
        # Check required fields
        missing_fields = [field for field in required_fields if field not in recommendations]
        if missing_fields:
            self.log_test(
                "Recommendations Structure", 
                False, 
                f"Missing recommendation fields: {missing_fields}"
            )
            return False
        
        # Verify YouTube videos structure
        youtube_videos = recommendations.get('youtube_videos', [])
        if not isinstance(youtube_videos, list) or len(youtube_videos) == 0:
            self.log_test(
                "Recommendations Structure", 
                False, 
                "YouTube videos should be a non-empty list"
            )
            return False
        
        # Verify articles structure
        articles = recommendations.get('articles', [])
        if not isinstance(articles, list) or len(articles) == 0:
            self.log_test(
                "Recommendations Structure", 
                False, 
                "Articles should be a non-empty list"
            )
            return False
        
        # Verify professional resources structure
        professional_resources = recommendations.get('professional_resources', [])
        if not isinstance(professional_resources, list) or len(professional_resources) == 0:
            self.log_test(
                "Recommendations Structure", 
                False, 
                "Professional resources should be a non-empty list"
            )
            return False
        
        # Check if crisis resources are included for high-risk situations
        risk_level = recommendations.get('risk_level', 'low')
        if risk_level == 'high':
            crisis_found = any(
                '988' in resource.get('description', '') or 
                'crisis' in resource.get('title', '').lower() or
                'suicide' in resource.get('title', '').lower()
                for resource in professional_resources
            )
            if not crisis_found:
                self.log_test(
                    "Recommendations Structure", 
                    False, 
                    "High-risk situation should include crisis resources"
                )
                return False
        
        self.log_test(
            "Recommendations Structure", 
            True, 
            f"Videos: {len(youtube_videos)}, Articles: {len(articles)}, Resources: {len(professional_resources)}"
        )
        return True
    
    def print_analysis_details(self, analysis: Dict, recommendations: Dict):
        """Print detailed analysis results for manual verification"""
        print("\n" + "="*60)
        print("PSYCHOLOGICAL ANALYSIS RESULTS")
        print("="*60)
        
        print(f"Predicted State: {analysis.get('predicted_state')}")
        print(f"Confidence: {analysis.get('confidence', 0):.2f}")
        print(f"Risk Level: {analysis.get('risk_level')}")
        print(f"Total Messages: {analysis.get('total_messages')}")
        
        if 'state_probabilities' in analysis:
            print("\nState Probabilities:")
            for state, prob in analysis['state_probabilities'].items():
                print(f"  {state}: {prob:.3f}")
        
        print(f"\nPersonalized Message:")
        print(f"  {recommendations.get('personalized_message', 'N/A')}")
        
        print(f"\nRecommendations Summary:")
        print(f"  YouTube Videos: {len(recommendations.get('youtube_videos', []))}")
        print(f"  Articles: {len(recommendations.get('articles', []))}")
        print(f"  Professional Resources: {len(recommendations.get('professional_resources', []))}")
        
        print("="*60 + "\n")
    
    def test_session_retrieval(self) -> bool:
        """Test retrieving session information"""
        try:
            if not self.session_id:
                self.log_test("Session Retrieval", False, "No session ID available")
                return False
            
            response = requests.get(f"{BASE_URL}/chat/session/{self.session_id}", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                # Should contain session info without full message content
                expected_fields = ['created_at', 'active', 'message_count']
                has_expected = any(field in data for field in expected_fields)
                
                self.log_test(
                    "Session Retrieval", 
                    has_expected, 
                    f"Session data retrieved with fields: {list(data.keys())}"
                )
                return has_expected
            else:
                self.log_test("Session Retrieval", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Session Retrieval", False, f"Error: {str(e)}")
            return False
    
    def test_invalid_session_handling(self) -> bool:
        """Test handling of invalid session IDs"""
        try:
            # Test end session with invalid ID
            payload = {"session_id": "invalid-session-id"}
            response = requests.post(f"{BASE_URL}/chat/end-session", json=payload, timeout=TIMEOUT)
            
            # Should return 400 or appropriate error
            if response.status_code in [400, 404]:
                self.log_test(
                    "Invalid Session Handling", 
                    True, 
                    f"Correctly handled invalid session with status {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    "Invalid Session Handling", 
                    False, 
                    f"Unexpected status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test("Invalid Session Handling", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_test(self) -> Dict:
        """Run all tests in sequence"""
        print("🧠 Starting psychMASTER Backend Testing - Psychological Analysis Features")
        print("="*80)
        
        # Test sequence
        tests = [
            ("Health Check", self.test_health_check),
            ("Create Session", self.test_create_session),
            ("Conversation Scenarios", self.test_conversation_scenarios),
            ("Crisis Detection", self.test_crisis_detection),
            ("End Session Analysis", self.test_end_session_analysis),
            ("Session Retrieval", self.test_session_retrieval),
            ("Invalid Session Handling", self.test_invalid_session_handling)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                success = test_func()
                if success:
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Unexpected error: {str(e)}")
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\nFailed Tests:")
            for test in self.failed_tests:
                print(f"  ❌ {test}")
        
        return {
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'success_rate': (passed/total)*100,
            'failed_tests': self.failed_tests,
            'all_results': self.test_results
        }

def main():
    """Main test execution"""
    tester = PsychMASTERTester()
    results = tester.run_comprehensive_test()
    
    # Exit with appropriate code
    if results['failed'] == 0:
        print("\n🎉 All tests passed! Psychological analysis system is working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()