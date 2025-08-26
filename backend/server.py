from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from langchain_service import mental_health_service


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Chat Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_crisis: bool = False

# Session and Analysis Models
class SessionRequest(BaseModel):
    action: str = "create"  # create or get

class SessionResponse(BaseModel):
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EndSessionRequest(BaseModel):
    session_id: str

class AnalysisResult(BaseModel):
    predicted_state: str
    confidence: float
    risk_level: str
    analysis_timestamp: str
    total_messages: int

class SessionEndResponse(BaseModel):
    success: bool
    session_id: str
    analysis: Optional[dict] = None
    recommendations: Optional[dict] = None
    session_summary: Optional[dict] = None
    error: Optional[str] = None

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Chat endpoints
@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """Send a message to the AI and get a response"""
    try:
        result = mental_health_service.get_response(
            message=request.message,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=result['response'],
            session_id=result['session_id'],
            is_crisis=result.get('is_crisis', False)
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during chat processing")

@api_router.post("/chat/session", response_model=SessionResponse)
async def manage_session(request: SessionRequest):
    """Create or manage chat sessions"""
    try:
        if request.action == "create":
            session_id = mental_health_service.create_session()
            return SessionResponse(session_id=session_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
    except Exception as e:
        logger.error(f"Session error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during session management")

@api_router.post("/chat/end-session", response_model=SessionEndResponse)
async def end_chat_session(request: EndSessionRequest):
    """End a chat session and perform psychological analysis"""
    try:
        result = mental_health_service.end_session(request.session_id)
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('error', 'Failed to end session'))
        
        return SessionEndResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"End session error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during session analysis")

@api_router.get("/chat/session/{session_id}")
async def get_session_info(session_id: str):
    """Get session information and analysis if available"""
    try:
        session_data = mental_health_service.get_session_data(session_id)
        
        if 'error' in session_data:
            raise HTTPException(status_code=404, detail=session_data['error'])
        
        return session_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get session error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving session data")

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "psychMASTER API",
        "langchain_initialized": mental_health_service.qa_chain is not None
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
