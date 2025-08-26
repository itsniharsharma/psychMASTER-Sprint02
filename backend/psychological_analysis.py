import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pickle
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class PsychologicalAnalyzer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.model_path = Path("./models/psychological_model.pkl")
        self.vectorizer_path = Path("./models/vectorizer.pkl")
        self.label_encoder_path = Path("./models/label_encoder.pkl")
        self.dataset_path = Path("./datasets/Combined Data.csv")
        
        # Create models directory
        os.makedirs("./models", exist_ok=True)
        
        # Target psychological states
        self.target_states = ['Normal', 'Depression', 'Bipolar', 'Anxiety', 'Suicidal']
        
        # Initialize the analyzer
        self.initialize_analyzer()
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep some punctuation
        text = re.sub(r'[^a-zA-Z\s\.\!\?\,]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def load_and_prepare_dataset(self) -> pd.DataFrame:
        """Load and prepare the mental health dataset"""
        try:
            logger.info("Loading mental health dataset...")
            df = pd.read_csv(self.dataset_path)
            
            # Filter for target states only
            df = df[df['status'].isin(self.target_states)].copy()
            
            # Clean the data
            df = df.dropna(subset=['statement', 'status'])
            df['statement'] = df['statement'].astype(str)
            
            # Preprocess text
            df['processed_statement'] = df['statement'].apply(self.preprocess_text)
            
            # Remove empty statements after preprocessing
            df = df[df['processed_statement'].str.strip() != '']
            
            logger.info(f"Dataset loaded successfully with {len(df)} samples")
            logger.info(f"State distribution:\n{df['status'].value_counts()}")
            
            return df
        
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            return pd.DataFrame()
    
    def train_model(self, force_retrain: bool = False) -> bool:
        """Train the psychological analysis model"""
        try:
            # Check if model already exists and is recent
            if not force_retrain and all([
                self.model_path.exists(),
                self.vectorizer_path.exists(), 
                self.label_encoder_path.exists()
            ]):
                logger.info("Using existing trained model...")
                return self.load_model()
            
            logger.info("Training psychological analysis model...")
            
            # Load dataset
            df = self.load_and_prepare_dataset()
            if df.empty:
                logger.error("No data available for training")
                return False
            
            # Prepare features and labels
            X = df['processed_statement']
            y = df['status']
            
            # Initialize vectorizer with optimized parameters
            self.vectorizer = TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 2),
                stop_words='english',
                min_df=2,
                max_df=0.95
            )
            
            # Fit vectorizer and transform text
            X_vectorized = self.vectorizer.fit_transform(X)
            
            # Initialize label encoder
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_vectorized, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
            )
            
            # Train model with balanced class weights
            self.model = LogisticRegression(
                max_iter=1000,
                class_weight='balanced',
                random_state=42
            )
            
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Model trained with accuracy: {accuracy:.3f}")
            logger.info(f"Classification report:\n{classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)}")
            
            # Save model components
            self.save_model()
            
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def save_model(self):
        """Save the trained model components"""
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(self.vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            with open(self.label_encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            
            logger.info("Model saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self) -> bool:
        """Load the trained model components"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            with open(self.label_encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def initialize_analyzer(self):
        """Initialize the psychological analyzer"""
        try:
            # Try to load existing model first
            if not self.load_model():
                logger.info("No existing model found, training new model...")
                if not self.train_model():
                    logger.error("Failed to train model")
                    return False
            
            logger.info("Psychological analyzer initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing analyzer: {str(e)}")
            return False
    
    def analyze_conversation(self, messages: List[Dict]) -> Dict:
        """Analyze a conversation and predict psychological state"""
        try:
            if not self.model or not self.vectorizer or not self.label_encoder:
                logger.error("Model not initialized")
                return self._get_fallback_analysis()
            
            # Extract user messages
            user_messages = [
                msg['content'] for msg in messages 
                if msg.get('role') == 'user' and msg.get('content')
            ]
            
            if not user_messages:
                return self._get_fallback_analysis()
            
            # Combine all user messages
            full_conversation = ' '.join(user_messages)
            
            # Preprocess the conversation
            processed_text = self.preprocess_text(full_conversation)
            
            if not processed_text:
                return self._get_fallback_analysis()
            
            # Vectorize the text
            text_vectorized = self.vectorizer.transform([processed_text])
            
            # Get predictions with probabilities
            prediction_proba = self.model.predict_proba(text_vectorized)[0]
            predicted_class = self.model.predict(text_vectorized)[0]
            
            # Get the predicted state
            predicted_state = self.label_encoder.inverse_transform([predicted_class])[0]
            confidence = float(prediction_proba.max())
            
            # Get probabilities for all states
            state_probabilities = {}
            for i, state in enumerate(self.label_encoder.classes_):
                state_probabilities[state] = float(prediction_proba[i])
            
            # Analyze conversation patterns
            conversation_insights = self._analyze_conversation_patterns(user_messages)
            
            # Generate risk assessment
            risk_level = self._assess_risk_level(predicted_state, confidence, conversation_insights)
            
            return {
                'predicted_state': predicted_state,
                'confidence': confidence,
                'state_probabilities': state_probabilities,
                'risk_level': risk_level,
                'conversation_insights': conversation_insights,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'total_messages': len(user_messages),
                'conversation_length': len(full_conversation)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing conversation: {str(e)}")
            return self._get_fallback_analysis()
    
    def _analyze_conversation_patterns(self, messages: List[str]) -> Dict:
        """Analyze patterns in the conversation"""
        try:
            full_text = ' '.join(messages).lower()
            
            # Crisis indicators
            crisis_keywords = [
                'suicide', 'kill myself', 'end my life', 'hurt myself',
                'want to die', 'better off dead', 'self harm', 'no point living'
            ]
            
            # Emotional indicators
            depression_keywords = [
                'sad', 'hopeless', 'empty', 'worthless', 'tired', 'exhausted',
                'lonely', 'isolated', 'depressed', 'down', 'low'
            ]
            
            anxiety_keywords = [
                'anxious', 'worried', 'nervous', 'panic', 'scared', 'afraid',
                'restless', 'overwhelmed', 'stress', 'tension'
            ]
            
            # Count occurrences
            crisis_count = sum(1 for keyword in crisis_keywords if keyword in full_text)
            depression_count = sum(1 for keyword in depression_keywords if keyword in full_text)
            anxiety_count = sum(1 for keyword in anxiety_keywords if keyword in full_text)
            
            return {
                'crisis_indicators': crisis_count,
                'depression_indicators': depression_count,
                'anxiety_indicators': anxiety_count,
                'avg_message_length': np.mean([len(msg) for msg in messages]) if messages else 0,
                'total_words': len(full_text.split()),
                'unique_concerns': len(set(messages)) / len(messages) if messages else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing conversation patterns: {str(e)}")
            return {}
    
    def _assess_risk_level(self, predicted_state: str, confidence: float, insights: Dict) -> str:
        """Assess the risk level based on analysis"""
        try:
            # High risk conditions
            if predicted_state == 'Suicidal':
                return 'high'
            
            if insights.get('crisis_indicators', 0) > 0:
                return 'high'
            
            # Medium risk conditions
            if predicted_state in ['Depression', 'Bipolar'] and confidence > 0.7:
                return 'medium'
            
            if predicted_state == 'Anxiety' and confidence > 0.8:
                return 'medium'
            
            # Low risk or normal
            if predicted_state == 'Normal':
                return 'low'
            
            return 'medium'
            
        except Exception as e:
            logger.error(f"Error assessing risk level: {str(e)}")
            return 'low'
    
    def _get_fallback_analysis(self) -> Dict:
        """Return fallback analysis when model fails"""
        return {
            'predicted_state': 'Normal',
            'confidence': 0.5,
            'state_probabilities': {
                'Normal': 0.5,
                'Depression': 0.2,
                'Anxiety': 0.2,
                'Bipolar': 0.05,
                'Suicidal': 0.05
            },
            'risk_level': 'low',
            'conversation_insights': {},
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'total_messages': 0,
            'conversation_length': 0,
            'fallback': True
        }


# Global analyzer instance
psychological_analyzer = PsychologicalAnalyzer()