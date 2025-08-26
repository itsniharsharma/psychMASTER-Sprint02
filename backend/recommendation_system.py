import logging
from typing import Dict, List
import random

logger = logging.getLogger(__name__)

class RecommendationSystem:
    def __init__(self):
        # Define comprehensive recommendations for each psychological state
        self.recommendations = {
            'Normal': {
                'youtube_videos': [
                    {
                        'title': '10 Daily Habits for Mental Wellness',
                        'url': 'https://www.youtube.com/watch?v=3QIfkeA6HBY',
                        'description': 'Simple daily practices to maintain good mental health'
                    },
                    {
                        'title': 'Mindfulness Meditation for Beginners',
                        'url': 'https://www.youtube.com/watch?v=ZToicYcHIOU',
                        'description': '10-minute guided meditation for stress relief'
                    },
                    {
                        'title': 'Building Emotional Resilience',
                        'url': 'https://www.youtube.com/watch?v=NUHsEmlIoE4',
                        'description': 'Techniques to build emotional strength and resilience'
                    }
                ],
                'articles': [
                    {
                        'title': 'The Science of Well-Being',
                        'url': 'https://www.helpguide.org/articles/mental-health/building-better-mental-health.htm',
                        'description': 'Evidence-based strategies for maintaining mental wellness'
                    },
                    {
                        'title': 'Positive Psychology Practices',
                        'url': 'https://positivepsychology.com/positive-psychology-exercises/',
                        'description': 'Research-backed exercises to boost happiness and life satisfaction'
                    }
                ],
                'professional_resources': [
                    {
                        'title': 'Psychology Today - Find a Therapist',
                        'url': 'https://www.psychologytoday.com/us/therapists',
                        'description': 'Find mental health professionals in your area'
                    }
                ]
            },
            
            'Depression': {
                'youtube_videos': [
                    {
                        'title': 'Understanding Depression - Mayo Clinic',
                        'url': 'https://www.youtube.com/watch?v=z-IR48Mb3W0',
                        'description': 'Comprehensive overview of depression symptoms and treatment'
                    },
                    {
                        'title': 'Cognitive Behavioral Therapy for Depression',
                        'url': 'https://www.youtube.com/watch?v=0ViaCs0k2jQ',
                        'description': 'CBT techniques to manage depressive thoughts'
                    },
                    {
                        'title': 'Depression Recovery: Daily Routine That Helps',
                        'url': 'https://www.youtube.com/watch?v=OG6HZMMDEYA',
                        'description': 'Practical daily routines for managing depression'
                    },
                    {
                        'title': 'Guided Meditation for Depression and Anxiety',
                        'url': 'https://www.youtube.com/watch?v=ZToicYcHIOU',
                        'description': 'Calming meditation specifically for depression relief'
                    }
                ],
                'articles': [
                    {
                        'title': 'Depression Treatment and Management',
                        'url': 'https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions/Depression',
                        'description': 'Comprehensive guide to understanding and treating depression'
                    },
                    {
                        'title': 'Coping with Depression - Harvard Health',
                        'url': 'https://www.health.harvard.edu/mind-and-mood/what-causes-depression',
                        'description': 'Evidence-based strategies for managing depression'
                    },
                    {
                        'title': 'Self-Help Strategies for Depression',
                        'url': 'https://www.helpguide.org/articles/depression/coping-with-depression.htm',
                        'description': 'Practical self-help techniques for depression recovery'
                    }
                ],
                'professional_resources': [
                    {
                        'title': 'National Suicide Prevention Lifeline',
                        'url': 'https://suicidepreventionlifeline.org/',
                        'description': 'Crisis support: Call 988 for immediate help'
                    },
                    {
                        'title': 'Depression and Bipolar Support Alliance',
                        'url': 'https://www.dbsalliance.org/',
                        'description': 'Support groups and resources for depression'
                    },
                    {
                        'title': 'SAMHSA National Helpline',
                        'url': 'https://www.samhsa.gov/find-help/national-helpline',
                        'description': '1-800-662-4357 - Free, confidential treatment referral service'
                    }
                ]
            },
            
            'Anxiety': {
                'youtube_videos': [
                    {
                        'title': 'Anxiety Explained - Understanding Your Anxious Mind',
                        'url': 'https://www.youtube.com/watch?v=WWloIAQpMcQ',
                        'description': 'Understanding the science behind anxiety and panic'
                    },
                    {
                        'title': '5-4-3-2-1 Grounding Technique for Anxiety',
                        'url': 'https://www.youtube.com/watch?v=30VMIEmA114',
                        'description': 'Quick technique to manage anxiety attacks'
                    },
                    {
                        'title': 'Breathing Exercises for Anxiety Relief',
                        'url': 'https://www.youtube.com/watch?v=DbDoBzGY3vo',
                        'description': 'Effective breathing techniques to calm anxiety'
                    },
                    {
                        'title': 'Progressive Muscle Relaxation for Anxiety',
                        'url': 'https://www.youtube.com/watch?v=ihO02wUzgkc',
                        'description': 'Guided muscle relaxation to reduce physical anxiety symptoms'
                    }
                ],
                'articles': [
                    {
                        'title': 'Anxiety Disorders - Mayo Clinic',
                        'url': 'https://www.mayoclinic.org/diseases-conditions/anxiety/symptoms-causes/syc-20350961',
                        'description': 'Comprehensive guide to anxiety disorders and treatment'
                    },
                    {
                        'title': 'Managing Anxiety - Practical Tips',
                        'url': 'https://www.anxietyanddepressionassociation.org/tips-managing-anxiety-and-stress',
                        'description': 'Evidence-based tips for managing anxiety in daily life'
                    },
                    {
                        'title': 'Cognitive Techniques for Anxiety',
                        'url': 'https://www.helpguide.org/articles/anxiety/anxiety-disorders-and-anxiety-attacks.htm',
                        'description': 'Cognitive strategies to overcome anxious thoughts'
                    }
                ],
                'professional_resources': [
                    {
                        'title': 'Anxiety and Depression Association of America',
                        'url': 'https://adaa.org/',
                        'description': 'Resources, support groups, and professional help for anxiety'
                    },
                    {
                        'title': 'Crisis Text Line',
                        'url': 'https://www.crisistextline.org/',
                        'description': 'Text HOME to 741741 for free crisis counseling'
                    }
                ]
            },
            
            'Bipolar': {
                'youtube_videos': [
                    {
                        'title': 'Understanding Bipolar Disorder - Mayo Clinic',
                        'url': 'https://www.youtube.com/watch?v=RrWfDgqIbcg',
                        'description': 'Comprehensive overview of bipolar disorder'
                    },
                    {
                        'title': 'Living with Bipolar Disorder - Personal Stories',
                        'url': 'https://www.youtube.com/watch?v=apLGdKKjFNA',
                        'description': 'Real experiences and coping strategies from bipolar individuals'
                    },
                    {
                        'title': 'Mood Tracking for Bipolar Disorder',
                        'url': 'https://www.youtube.com/watch?v=FvnnyY_h0GI',
                        'description': 'How to track mood changes and identify triggers'
                    }
                ],
                'articles': [
                    {
                        'title': 'Bipolar Disorder Guide - NAMI',
                        'url': 'https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions/Bipolar-Disorder',
                        'description': 'Complete guide to understanding bipolar disorder'
                    },
                    {
                        'title': 'Managing Bipolar Disorder',
                        'url': 'https://www.webmd.com/bipolar-disorder/guide/bipolar-disorder-overview',
                        'description': 'Treatment options and management strategies'
                    },
                    {
                        'title': 'Bipolar Self-Care Strategies',
                        'url': 'https://www.helpguide.org/articles/bipolar-disorder/living-with-bipolar-disorder.htm',
                        'description': 'Self-care techniques for managing bipolar symptoms'
                    }
                ],
                'professional_resources': [
                    {
                        'title': 'Depression and Bipolar Support Alliance',
                        'url': 'https://www.dbsalliance.org/',
                        'description': 'Specialized support for bipolar disorder'
                    },
                    {
                        'title': 'International Bipolar Foundation',
                        'url': 'https://ibpf.org/',
                        'description': 'Education and support for bipolar individuals and families'
                    }
                ]
            },
            
            'Suicidal': {
                'youtube_videos': [
                    {
                        'title': 'Suicide Prevention - Warning Signs and How to Help',
                        'url': 'https://www.youtube.com/watch?v=WcSUs9iZv-g',
                        'description': 'Understanding suicidal thoughts and getting help'
                    },
                    {
                        'title': 'Crisis Survival Skills - DBT',
                        'url': 'https://www.youtube.com/watch?v=x3adCjQ_Bfg',
                        'description': 'Dialectical behavior therapy techniques for crisis situations'
                    },
                    {
                        'title': 'Hope and Recovery from Suicidal Thoughts',
                        'url': 'https://www.youtube.com/watch?v=WrqjmxPG1rM',
                        'description': 'Personal stories of recovery and finding hope'
                    }
                ],
                'articles': [
                    {
                        'title': 'Suicide Prevention Resources - CDC',
                        'url': 'https://www.cdc.gov/suicide/resources/index.html',
                        'description': 'Comprehensive suicide prevention resources and strategies'
                    },
                    {
                        'title': 'Coping with Suicidal Thoughts',
                        'url': 'https://www.suicidepreventionlifeline.org/help-yourself/attempt-survivors/',
                        'description': 'Strategies for managing suicidal ideation'
                    }
                ],
                'professional_resources': [
                    {
                        'title': '🚨 IMMEDIATE CRISIS SUPPORT 🚨',
                        'url': 'tel:988',
                        'description': 'Call 988 - National Suicide Prevention Lifeline (Available 24/7)'
                    },
                    {
                        'title': 'Crisis Text Line',
                        'url': 'https://www.crisistextline.org/',
                        'description': 'Text HOME to 741741 for immediate crisis support'
                    },
                    {
                        'title': 'Emergency Services',
                        'url': 'tel:911',
                        'description': 'Call 911 for immediate emergency assistance'
                    },
                    {
                        'title': 'National Suicide Prevention Lifeline',
                        'url': 'https://suicidepreventionlifeline.org/',
                        'description': 'Comprehensive crisis support and resources'
                    }
                ]
            }
        }
        
        # General crisis resources that are always included for high-risk states
        self.crisis_resources = [
            {
                'title': '🚨 National Suicide Prevention Lifeline: 988',
                'url': 'tel:988',
                'description': 'Free, confidential crisis support available 24/7/365'
            },
            {
                'title': 'Crisis Text Line',
                'url': 'https://www.crisistextline.org/',
                'description': 'Text HOME to 741741 for free, 24/7 crisis counseling'
            },
            {
                'title': 'Emergency Services',
                'url': 'tel:911',
                'description': 'Call 911 for immediate medical emergency assistance'
            }
        ]
    
    def get_recommendations(self, analysis_result: Dict) -> Dict:
        """Generate personalized recommendations based on psychological analysis"""
        try:
            predicted_state = analysis_result.get('predicted_state', 'Normal')
            risk_level = analysis_result.get('risk_level', 'low')
            confidence = analysis_result.get('confidence', 0.5)
            
            # Get base recommendations for the predicted state
            base_recommendations = self.recommendations.get(predicted_state, self.recommendations['Normal'])
            
            # Customize recommendations based on risk level and confidence
            recommendations = {
                'primary_concern': predicted_state,
                'risk_level': risk_level,
                'confidence_level': self._get_confidence_description(confidence),
                'youtube_videos': [],
                'articles': [],
                'professional_resources': [],
                'immediate_actions': []
            }
            
            # Add crisis resources for high-risk situations
            if risk_level == 'high' or predicted_state == 'Suicidal':
                recommendations['professional_resources'].extend(self.crisis_resources)
                recommendations['immediate_actions'] = [
                    'If you are in immediate danger, call 911',
                    'Call the National Suicide Prevention Lifeline: 988',
                    'Reach out to a trusted friend, family member, or mental health professional',
                    'Go to your nearest emergency room or urgent care center'
                ]
            
            # Add state-specific recommendations
            recommendations['youtube_videos'] = base_recommendations.get('youtube_videos', [])[:3]
            recommendations['articles'] = base_recommendations.get('articles', [])[:3]
            
            # Add professional resources if not already added (for non-crisis states)
            if risk_level != 'high':
                recommendations['professional_resources'].extend(base_recommendations.get('professional_resources', [])[:2])
            
            # Add general immediate actions based on state
            if not recommendations['immediate_actions']:
                recommendations['immediate_actions'] = self._get_immediate_actions(predicted_state, risk_level)
            
            # Add personalized message
            recommendations['personalized_message'] = self._generate_personalized_message(predicted_state, risk_level, confidence)
            
            # Add follow-up suggestions
            recommendations['follow_up_suggestions'] = self._get_follow_up_suggestions(predicted_state)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations()
    
    def _get_confidence_description(self, confidence: float) -> str:
        """Convert confidence score to human-readable description"""
        if confidence >= 0.8:
            return 'High confidence'
        elif confidence >= 0.6:
            return 'Moderate confidence'
        else:
            return 'Low confidence'
    
    def _get_immediate_actions(self, state: str, risk_level: str) -> List[str]:
        """Get immediate action recommendations based on state and risk"""
        actions = {
            'Normal': [
                'Continue practicing good mental health habits',
                'Consider regular check-ins with yourself about your mental state',
                'Maintain social connections and support networks'
            ],
            'Depression': [
                'Establish a daily routine with small, achievable goals',
                'Try to get some sunlight and fresh air each day',
                'Reach out to a friend or family member for support',
                'Consider scheduling an appointment with a mental health professional'
            ],
            'Anxiety': [
                'Practice deep breathing exercises when feeling anxious',
                'Use grounding techniques like the 5-4-3-2-1 method',
                'Limit caffeine intake which can increase anxiety',
                'Consider talking to a counselor about anxiety management techniques'
            ],
            'Bipolar': [
                'Maintain a consistent sleep schedule',
                'Track your mood changes and identify triggers',
                'Stay connected with your support system',
                'Contact your mental health provider if you notice significant mood changes'
            ]
        }
        
        return actions.get(state, actions['Normal'])
    
    def _generate_personalized_message(self, state: str, risk_level: str, confidence: float) -> str:
        """Generate a personalized supportive message"""
        messages = {
            'Normal': "Your conversation suggests you're managing your mental health well. Keep up the good work with self-care and stay aware of your mental state.",
            
            'Depression': f"Based on our conversation, it appears you may be experiencing symptoms of depression. This is treatable, and you don't have to go through this alone. The resources below can help you take the next steps toward feeling better.",
            
            'Anxiety': f"Your messages indicate you might be dealing with anxiety. Many people experience anxiety, and there are effective techniques and treatments available to help you manage these feelings.",
            
            'Bipolar': f"The patterns in our conversation suggest you may be experiencing symptoms related to bipolar disorder. Professional support can be very helpful in managing mood changes and developing coping strategies.",
            
            'Suicidal': "I'm very concerned about the thoughts and feelings you've shared. Your life has value, and there are people who want to help you through this difficult time. Please reach out for immediate support using the crisis resources below."
        }
        
        base_message = messages.get(state, messages['Normal'])
        
        if risk_level == 'high':
            base_message += " Please prioritize getting professional support as soon as possible."
        
        return base_message
    
    def _get_follow_up_suggestions(self, state: str) -> List[str]:
        """Get follow-up suggestions for continued support"""
        suggestions = {
            'Normal': [
                'Continue regular self-check-ins about your mental health',
                'Maintain healthy lifestyle habits (exercise, sleep, nutrition)',
                'Consider mindfulness or meditation practices'
            ],
            'Depression': [
                'Keep a daily mood journal to track patterns',
                'Set small, achievable daily goals',
                'Consider joining a support group',
                'Schedule regular follow-ups with a mental health professional'
            ],
            'Anxiety': [
                'Practice daily relaxation techniques',
                'Identify and work on managing your anxiety triggers',
                'Consider cognitive behavioral therapy (CBT)',
                'Monitor your progress with anxiety management techniques'
            ],
            'Bipolar': [
                'Maintain consistent daily routines',
                'Keep a detailed mood tracker',
                'Work with a psychiatrist on medication management if appropriate',
                'Build a strong support network of family and friends'
            ],
            'Suicidal': [
                'Follow up with crisis counselors or mental health professionals',
                'Create a safety plan with specific steps for crisis situations',
                'Remove any means of self-harm from your environment',
                'Stay connected with your support network daily'
            ]
        }
        
        return suggestions.get(state, suggestions['Normal'])
    
    def _get_fallback_recommendations(self) -> Dict:
        """Return fallback recommendations when system fails"""
        return {
            'primary_concern': 'General Support',
            'risk_level': 'low',
            'confidence_level': 'Low confidence',
            'youtube_videos': self.recommendations['Normal']['youtube_videos'][:2],
            'articles': self.recommendations['Normal']['articles'][:2],
            'professional_resources': [
                {
                    'title': 'National Suicide Prevention Lifeline',
                    'url': 'tel:988',
                    'description': 'Call 988 for crisis support - available 24/7'
                }
            ],
            'immediate_actions': [
                'If you\'re in crisis, call 988 or 911',
                'Consider talking to a mental health professional',
                'Reach out to trusted friends or family'
            ],
            'personalized_message': 'I want to make sure you have access to mental health resources. If you\'re experiencing any distress, please don\'t hesitate to reach out for professional help.',
            'follow_up_suggestions': [
                'Monitor your mental health regularly',
                'Practice self-care activities',
                'Stay connected with your support network'
            ]
        }


# Global recommendation system instance
recommendation_system = RecommendationSystem()