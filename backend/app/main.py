from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.api.stats import router as stats_router

app = FastAPI(title="Football Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Football Chatbot API"}