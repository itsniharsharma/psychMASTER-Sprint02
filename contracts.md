# API Contracts & Integration Plan for psychMASTER

## Current State
- ✅ Frontend: Complete with mock chat functionality
- ✅ Mock Data: Located in `/frontend/src/mock/chatMockData.js` 
- ✅ UI/UX: Black & white theme, responsive design, smooth interactions
- 🔄 Backend: Ready to integrate user's LangChain + Groq setup

## API Contracts

### 1. Chat Endpoint
**POST /api/chat**

Request:
```json
{
  "message": "string",
  "session_id": "string (uuid)"
}
```

Response:
```json
{
  "response": "string",
  "session_id": "string",
  "timestamp": "ISO string",
  "message_id": "string"
}
```

### 2. Session Management
**POST /api/chat/session**

Request:
```json
{
  "action": "create" | "get"
}
```

Response:
```json
{
  "session_id": "string",
  "created_at": "ISO string"
}
```

## Backend Implementation Plan

### Phase 1: Dependencies Installation
```bash
# Install LangChain dependencies
pip install langchain
pip install langchain-groq
pip install chromadb
pip install sentence-transformers
pip install huggingface-hub
```

### Phase 2: LangChain Integration
1. **Vector Database Setup**: Create persistent Chroma DB directory
2. **LLM Integration**: Use provided Groq configuration
3. **Document Processing**: Set up PDF loading and text splitting
4. **QA Chain**: Implement retrieval-augmented generation

### Phase 3: API Endpoints
1. **Chat Handler**: Process user messages through LangChain pipeline
2. **Session Management**: Track conversation context
3. **Error Handling**: Graceful fallback for API failures

### Phase 4: Frontend Integration
1. **Remove Mock Data**: Replace `getRandomResponse()` calls
2. **API Integration**: Connect to `/api/chat` endpoint
3. **Session Handling**: Implement session persistence
4. **Error States**: Handle loading, errors, and timeouts

## Mock Data to Replace

### Current Frontend Mock Usage:
- `chatMockData.js` - Contains predefined responses
- `ChatSection.jsx` - Uses `getRandomResponse()` function
- Local state management for messages

### Will Be Replaced With:
- Real-time API calls to `/api/chat`
- Session-based conversation management
- Actual LangChain + Groq responses
- Error handling for network/API issues

## Environment Variables Needed
```bash
# Backend .env additions
GROQ_API_KEY=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
CHROMA_DB_PATH=./chroma_db
PDF_DOCS_PATH=./docs
```

## Integration Steps

1. **Install Dependencies** - Add LangChain packages to requirements.txt
2. **Setup Vector DB** - Initialize Chroma database with mental health documents
3. **Create API Endpoints** - Implement chat and session endpoints
4. **Update Frontend** - Replace mock calls with real API integration
5. **Test Integration** - Verify end-to-end functionality

## Expected User Flow
1. User opens psychMASTER website
2. Clicks "Start Chatting" or navigates to chat section
3. Types message in chat input
4. Frontend sends POST to `/api/chat` with message and session_id
5. Backend processes through LangChain → Groq → Vector DB
6. Returns empathetic, contextual response
7. Frontend displays response in chat UI
8. Conversation continues with session context

## Files to Modify

### Backend Files:
- `server.py` - Add chat endpoints
- `requirements.txt` - Add LangChain dependencies
- `.env` - Add Groq API key

### Frontend Files:  
- `ChatSection.jsx` - Replace mock with API calls
- Remove: `mock/chatMockData.js` (after integration)

## Success Criteria
- ✅ Real-time chat with Groq LLM responses
- ✅ Session persistence across conversation
- ✅ Vector database integration for context
- ✅ Error handling for API failures
- ✅ Smooth UI experience matching current design