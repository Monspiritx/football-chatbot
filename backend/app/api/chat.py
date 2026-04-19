from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ChatResponse(
        reply=f"รับข้อความแล้ว: {req.message}",
        session_id=req.session_id,
    )