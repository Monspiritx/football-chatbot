from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.core.llm import ask_llm

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = ask_llm(req.message)
        return ChatResponse(reply=reply, session_id=req.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))