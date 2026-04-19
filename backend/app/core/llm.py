import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""คุณคือ FootballBot ผู้เชี่ยวชาญวิเคราะห์ฟุตบอล
คุณมีความรู้เรื่อง Premier League, La Liga, Champions League, ฟุตบอลทีมชาติ, บอลโลก รวมถึงการวิเคราะห์เรื่อง Tactic
ตอบเป็นภาษาไทย กระชับ ชัดเจน อ้างอิงสถิติเมื่อวิเคราะห์
ห้ามแนะนำการพนันทุกกรณี"""
)

def ask_llm(message: str) -> str:
    response = model.generate_content(message)
    return response.text