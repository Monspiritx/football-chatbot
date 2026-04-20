from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.core.llm import ask_llm
from app.services.football_api import get_standings, get_top_scorers, get_fixtures_today
import json

router = APIRouter()

async def get_context(message: str) -> str:
    msg = message.lower()
    try:
        if any(w in msg for w in ["ตาราง", "standings", "คะแนน", "อันดับ"]):
            league = "LaLiga" if any(w in msg for w in ["laliga", "la liga", "สเปน"]) else "EPL"
            data = await get_standings(league)
            return f"ตารางคะแนน {league}:\n{json.dumps(data, ensure_ascii=False)}"

        if any(w in msg for w in ["ดาวซัลโว", "top scorer", "goldenboot", "ทำประตู"]):
            league = "LaLiga" if any(w in msg for w in ["laliga", "la liga", "สเปน"]) else "EPL"
            data = await get_top_scorers(league)
            return f"Top Scorers {league}:\n{json.dumps(data, ensure_ascii=False)}"

        if any(w in msg for w in ["วันนี้", "today", "แมตช์", "คืนนี้"]):
            data = await get_fixtures_today()
            return f"แมตช์วันนี้:\n{json.dumps(data, ensure_ascii=False)}"

    except Exception:
        return ""
    return ""

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        context = await get_context(req.message)
        reply = ask_llm(req.message, context)
        return ChatResponse(reply=reply, session_id=req.session_id)
    except Exception as e:
        print(f"ERROR: {e}")  # เพิ่มบรรทัดนี้
        raise HTTPException(status_code=500, detail=str(e))