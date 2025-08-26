import os
from pathlib import Path
from typing import Optional, Dict, List
import uuid
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
from psychological_analysis import psychological_analyzer
from recommendation_system import recommendation_system

logger = logging.getLogger(__name__)

class MentalHealthChatService:
    def __init__(self):
        self.llm = None
        self.qa_chain = None
        self.vector_db = None
        self.sessions = {}  # Store session contexts
        self.initialize_service()
    
    def initialize_llm(self):
        """Initialize the Groq LLM"""
        try:
            # Load environment variables explicitly with correct path
            from dotenv import load_dotenv
            from pathlib import Path
            
            # Load .env from the backend directory
            env_path = Path(__file__).parent / '.env'
            load_dotenv(env_path)
            
            groq_api_key = os.environ.get('GROQ_API_KEY')
            if not groq_api_key:
                raise ValueError(f"GROQ_API_KEY not found. Env file path: {env_path}")
            
            self.llm = ChatGroq(
                temperature=0,
                groq_api_key=groq_api_key,
                model_name="llama-3.3-70b-versatile"
            )
            logger.info("✅ Groq LLM initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq LLM: {str(e)}")
            return False
    
    def create_vector_db(self):
        """Create or load the vector database"""
        try:
            docs_path = Path("./docs")
            db_path = os.environ.get('CHROMA_DB_PATH', './chroma_db')
            
            # Check if vector DB already exists
            if os.path.exists(db_path):
                logger.info("📁 Loading existing vector database...")
                embeddings = HuggingFaceBgeEmbeddings(
                    model_name='sentence-transformers/all-MiniLM-L6-v2'
                )
                self.vector_db = Chroma(
                    persist_directory=db_path, 
                    embedding_function=embeddings
                )
                logger.info("✅ Vector database loaded successfully")
                return True
            
            # Create new vector DB if it doesn't exist
            logger.info("🔧 Creating new vector database...")
            
            # Load documents
            if docs_path.exists():
                loader = DirectoryLoader(str(docs_path), glob="*.txt", loader_cls=TextLoader)
                documents = loader.load()
                
                if documents:
                    # Split documents
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=500, 
                        chunk_overlap=50
                    )
                    texts = text_splitter.split_documents(documents)
                    
                    # Create embeddings and vector store
                    embeddings = HuggingFaceBgeEmbeddings(
                        model_name='sentence-transformers/all-MiniLM-L6-v2'
                    )
                    
                    self.vector_db = Chroma.from_documents(
                        texts, 
                        embeddings, 
                        persist_directory=db_path
                    )
                    self.vector_db.persist()
                    
                    logger.info(f"✅ Vector database created with {len(texts)} document chunks")
                    return True
                else:
                    logger.warning("⚠️ No PDF documents found in docs directory")
                    return self._create_empty_vector_db(db_path)
            else:
                logger.warning("⚠️ Docs directory not found, creating empty vector DB")
                return self._create_empty_vector_db(db_path)
                
        except Exception as e:
            logger.error(f"❌ Failed to create vector database: {str(e)}")
            return False
    
    def _create_empty_vector_db(self, db_path: str):
        """Create an empty vector database for fallback"""
        try:
            embeddings = HuggingFaceBgeEmbeddings(
                model_name='sentence-transformers/all-MiniLM-L6-v2'
            )
            # Create with empty documents
            from langchain.schema import Document
            dummy_docs = [Document(page_content="Mental health support and guidance.", metadata={"source": "default"})]
            
            self.vector_db = Chroma.from_documents(
                dummy_docs,
                embeddings, 
                persist_directory=db_path
            )
            self.vector_db.persist()
            logger.info("✅ Empty vector database created as fallback")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create empty vector database: {str(e)}")
            return False
    
    def setup_qa_chain(self):
        """Set up the QA chain with retrieval"""
        try:
            if not self.vector_db or not self.llm:
                logger.error("❌ Vector DB or LLM not initialized")
                return False
            
            retriever = self.vector_db.as_retriever()
            
            prompt_template = """You are psychMASTER, a compassionate and empathetic AI mental health companion. Your role is to provide supportive, understanding, and helpful responses to users seeking mental health guidance.

Guidelines for your responses:
- Always be empathetic, non-judgmental, and supportive
- Acknowledge the user's feelings and validate their experiences
- Provide practical advice when appropriate
- Encourage professional help when needed
- Keep responses conversational and warm
- Use the context below to provide informed guidance
- If the user expresses thoughts of self-harm, immediately provide crisis resources

Context from mental health resources:
{context}

User: {question}

psychMASTER Response:"""

            PROMPT = PromptTemplate(
                template=prompt_template, 
                input_variables=['context', 'question']
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": PROMPT}
            )
            
            logger.info("✅ QA chain setup completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup QA chain: {str(e)}")
            return False
    
    def initialize_service(self):
        """Initialize the complete service"""
        logger.info("🚀 Initializing Mental Health Chat Service...")
        
        success = True
        success &= self.initialize_llm()
        success &= self.create_vector_db()
        success &= self.setup_qa_chain()
        
        if success:
            logger.info("✅ Mental Health Chat Service initialized successfully!")
        else:
            logger.error("❌ Failed to initialize Mental Health Chat Service")
    
    def create_session(self) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'messages': [],
            'created_at': datetime.utcnow().isoformat(),
            'active': True
        }
        return session_id
    
    def get_response(self, message: str, session_id: Optional[str] = None) -> dict:
        """Get AI response for a user message"""
        try:
            # Create session if not provided
            if not session_id:
                session_id = self.create_session()
            elif session_id not in self.sessions:
                self.sessions[session_id] = {'messages': [], 'created_at': str(uuid.uuid4())}
            
            # Check for crisis keywords
            crisis_keywords = [
                'suicide', 'kill myself', 'end my life', 'hurt myself', 
                'want to die', 'better off dead', 'self harm'
            ]
            
            if any(keyword in message.lower() for keyword in crisis_keywords):
                crisis_response = """I'm very concerned about what you've shared. Your life has value, and there are people who want to help you through this difficult time.

Please reach out for immediate support:
• National Suicide Prevention Lifeline: 988 (available 24/7)
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

You don't have to go through this alone. Professional counselors are available right now to talk with you. Would you like me to help you find local mental health resources?"""
                
                return {
                    'response': crisis_response,
                    'session_id': session_id,
                    'is_crisis': True
                }
            
            # Get AI response
            if self.qa_chain:
                ai_response = self.qa_chain.run(message)
            else:
                # Fallback response if QA chain fails
                ai_response = self._get_fallback_response(message)
            
            # Store conversation in session
            self.sessions[session_id]['messages'].extend([
                {'role': 'user', 'content': message},
                {'role': 'assistant', 'content': ai_response}
            ])
            
            return {
                'response': ai_response,
                'session_id': session_id,
                'is_crisis': False
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting AI response: {str(e)}")
            return {
                'response': self._get_error_response(),
                'session_id': session_id or self.create_session(),
                'is_crisis': False,
                'error': str(e)
            }
    
    def end_session(self, session_id: str) -> Dict:
        """End a chat session and perform psychological analysis"""
        try:
            if session_id not in self.sessions:
                logger.error(f"Session {session_id} not found")
                return {
                    'success': False,
                    'error': 'Session not found'
                }
            
            session_data = self.sessions[session_id]
            messages = session_data.get('messages', [])
            
            if not messages:
                logger.warning(f"No messages found in session {session_id}")
                return {
                    'success': False,
                    'error': 'No conversation data to analyze'
                }
            
            # Perform psychological analysis
            logger.info(f"Performing psychological analysis for session {session_id}")
            analysis_result = psychological_analyzer.analyze_conversation(messages)
            
            # Generate personalized recommendations
            logger.info(f"Generating recommendations for session {session_id}")
            recommendations = recommendation_system.get_recommendations(analysis_result)
            
            # Mark session as ended
            session_data['active'] = False
            session_data['ended_at'] = datetime.utcnow().isoformat()
            session_data['analysis'] = analysis_result
            session_data['recommendations'] = recommendations
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis': analysis_result,
                'recommendations': recommendations,
                'session_summary': {
                    'total_messages': len(messages),
                    'user_messages': len([m for m in messages if m.get('role') == 'user']),
                    'conversation_duration': session_data.get('ended_at'),
                    'started_at': session_data.get('created_at')
                }
            }
            
        except Exception as e:
            logger.error(f"Error ending session {session_id}: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to analyze session: {str(e)}'
            }
    
    def get_session_data(self, session_id: str) -> Dict:
        """Get session data including analysis if session has ended"""
        try:
            if session_id not in self.sessions:
                return {'error': 'Session not found'}
            
            session_data = self.sessions[session_id].copy()
            
            # Don't return all message content for privacy
            if 'messages' in session_data:
                session_data['message_count'] = len(session_data['messages'])
                del session_data['messages']
            
            return session_data
            
        except Exception as e:
            logger.error(f"Error getting session data for {session_id}: {str(e)}")
            return {'error': str(e)}
    
    def _get_fallback_response(self, message: str) -> str:
        """Provide fallback responses when AI is unavailable"""
        fallback_responses = [
            "I hear you, and I want you to know that your feelings are valid. Can you tell me more about what you're experiencing?",
            "Thank you for sharing that with me. It sounds like you're going through a challenging time. How can I best support you right now?",
            "I'm here to listen and support you. What's been weighing on your mind lately?",
            "It takes courage to reach out. I'm glad you're here. What would be most helpful for you today?",
        ]
        
        import random
        return random.choice(fallback_responses)
    
    def _get_error_response(self) -> str:
        """Response when there's a technical error"""
        return """I'm experiencing some technical difficulties right now, but I'm still here to support you. 

If you're in crisis, please don't wait:
• Call 988 (Suicide & Crisis Lifeline)
• Text HOME to 741741 (Crisis Text Line)
• Call 911 for emergencies

I'll be back online shortly to continue our conversation."""

# Global service instance
mental_health_service = MentalHealthChatService()