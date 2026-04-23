from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.core.llm import ask_llm
from app.services.football_api import get_standings, get_top_scorers, get_fixtures_today
from app.services.vector_db import search
import json

router = APIRouter()

async def get_context(message: str) -> str:
    context_parts = []

    # ดึงจาก Vector DB — ใช้ keyword extraction ให้ดีขึ้น
    search_query = message
    msg = message.lower()

    # ถ้าถามเรื่องข่าววันนี้ให้ search คำที่กว้างขึ้น
    if any(w in msg for w in ["วันนี้", "ล่าสุด", "ข่าว", "today", "latest", "news"]):
        search_query = "football news latest transfer injury"

    rag_results = search(search_query, n_results=3)
    if rag_results:
        context_parts.append("ข้อมูลความรู้ที่เกี่ยวข้อง:\n" + "\n".join(f"- {r}" for r in rag_results))

    # ดึงจาก Football API
    try:
        if any(w in msg for w in ["ตาราง", "standings", "คะแนน", "อันดับ"]):
            league = "LaLiga" if any(w in msg for w in ["laliga", "la liga", "สเปน"]) else "EPL"
            data = await get_standings(league)
            context_parts.append(f"ตารางคะแนน {league}:\n{json.dumps(data, ensure_ascii=False)}")

        if any(w in msg for w in ["ดาวซัลโว", "top scorer", "ทำประตู"]):
            league = "LaLiga" if any(w in msg for w in ["laliga", "la liga", "สเปน"]) else "EPL"
            data = await get_top_scorers(league)
            context_parts.append(f"Top Scorers {league}:\n{json.dumps(data, ensure_ascii=False)}")

        if any(w in msg for w in ["วันนี้", "today", "แมตช์", "คืนนี้", "โปรแกรม"]):
            data = await get_fixtures_today()
            context_parts.append(f"แมตช์วันนี้:\n{json.dumps(data, ensure_ascii=False)}")

    except Exception:
        pass

    return "\n\n".join(context_parts)

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        context = await get_context(req.message)
        reply = ask_llm(req.message, context)
        return ChatResponse(reply=reply, session_id=req.session_id)
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))