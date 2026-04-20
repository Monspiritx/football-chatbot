from dotenv import load_dotenv
import google.genai as genai
import os
import time
from datetime import datetime, timedelta
from collections import deque

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """คุณคือ FootballBot ผู้เชี่ยวชาญวิเคราะห์ฟุตบอล
คุณมีความรู้เรื่อง Premier League, La Liga, Champions League
ตอบเป็นภาษาไทย กระชับ ชัดเจน อ้างอิงสถิติเมื่อวิเคราะห์
ถ้ามีข้อมูลสถิติแนบมาให้ใช้ข้อมูลนั้นในการตอบ
ห้ามแนะนำการพนันทุกกรณี"""

# Rate limiter — max 2 requests ต่อนาที
REQUEST_TIMES: deque = deque()
MAX_REQUESTS_PER_MINUTE = 2
MIN_INTERVAL_SECONDS = 35

def _wait_if_needed():
    now = datetime.now()
    window = now - timedelta(minutes=1)

    # ลบ request เก่าที่เกิน 1 นาทีออก
    while REQUEST_TIMES and REQUEST_TIMES[0] < window:
        REQUEST_TIMES.popleft()

    # ถ้า request ใน 1 นาทีเต็มแล้ว ให้รอ
    if len(REQUEST_TIMES) >= MAX_REQUESTS_PER_MINUTE:
        oldest = REQUEST_TIMES[0]
        wait_seconds = (oldest + timedelta(minutes=1) - now).total_seconds()
        if wait_seconds > 0:
            print(f"Rate limit: รอ {wait_seconds:.1f} วินาที...")
            time.sleep(wait_seconds + 1)

    # ถ้า request ล่าสุดเพิ่งส่งไปไม่นาน ให้รอก่อน
    if REQUEST_TIMES:
        last = REQUEST_TIMES[-1]
        elapsed = (now - last).total_seconds()
        if elapsed < MIN_INTERVAL_SECONDS:
            wait = MIN_INTERVAL_SECONDS - elapsed
            print(f"Rate limit: รอ {wait:.1f} วินาที...")
            time.sleep(wait)

    REQUEST_TIMES.append(datetime.now())

def ask_llm(message: str, context: str = "") -> str:
    full_prompt = message
    if context:
        full_prompt = f"ข้อมูลสถิติล่าสุด:\n{context}\n\nคำถาม: {message}"

    _wait_if_needed()

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=SYSTEM_PROMPT + "\n\n" + full_prompt,
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                wait = 45 * (attempt + 1)
                print(f"429 error: รอ {wait} วินาที... (attempt {attempt + 1}/3)")
                time.sleep(wait)
                continue
            raise e

    return "ขออภัยครับ ระบบยุ่งมาก กรุณารอสักครู่แล้วลองใหม่"