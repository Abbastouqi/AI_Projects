from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.schemas import ChatMessage, ChatResponse
from models.database import get_db, UserSession
from services.conversation_manager import ConversationFlowManager
import uuid

chat_router = APIRouter()

@chat_router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    try:
        session_id = message.session_id or str(uuid.uuid4())
        
        # Ensure session exists
        session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
        if not session:
            session = UserSession(
                session_id=session_id,
                conversation_history=[],
                preferences={}
            )
            db.add(session)
            db.commit()
        
        # Use conversation manager
        conversation_manager = ConversationFlowManager(db)
        response, recommendations = conversation_manager.generate_response(
            session_id,
            message.message
        )
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chat_router.get("/health")
async def health():
    return {"status": "healthy"}

@chat_router.get("/session/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get session conversation history"""
    session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "conversation_history": session.conversation_history,
        "preferences": session.preferences,
        "created_at": session.created_at
    }
