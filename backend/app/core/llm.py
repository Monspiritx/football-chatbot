from dotenv import load_dotenv
import google.genai as genai
import os
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """คุณคือ FootballBot ผู้เชี่ยวชาญวิเคราะห์ฟุตบอล
คุณมีความรู้เรื่อง Premier League, La Liga, Champions League
ตอบเป็นภาษาไทย กระชับ ชัดเจน อ้างอิงสถิติเมื่อวิเคราะห์
ห้ามแนะนำการพนันทุกกรณี"""

def ask_llm(message: str) -> str:
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=SYSTEM_PROMPT + "\n\n" + message,
            )
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                time.sleep(15)
                continue
            raise e