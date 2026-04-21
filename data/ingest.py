import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.services.vector_db import add_documents

docs = [
    {"text": "Arsenal ภายใต้ Mikel Arteta ใช้ระบบ 4-3-3 ที่ยืดหยุ่น fullback ทั้งสองจะ invert เข้ากลางสนาม สร้าง overload ในพื้นที่แคบ PPDA เฉลี่ยอยู่ที่ 8.2 แสดงถึง high press ที่มีประสิทธิภาพสูง", "metadata": {"team": "Arsenal", "category": "tactics"}},
    {"text": "Manchester City ใช้ระบบ 3-2-4-1 หรือ 4-3-3 ขึ้นอยู่กับคู่แข่ง Pep Guardiola เน้น positional play ครองบอลและสร้างพื้นที่ผ่าน false 9 และ inverted wingers possession เฉลี่ยสูงถึง 65%", "metadata": {"team": "Manchester City", "category": "tactics"}},
    {"text": "Liverpool ภายใต้ Arne Slot สืบทอดแนวคิด gegenpressing จาก Klopp กดดันคู่ต่อสู้ทันทีหลังเสียบอล Mohamed Salah ยังคงเป็นกำลังสำคัญด้าน xG สูงสุดในทีม", "metadata": {"team": "Liverpool", "category": "tactics"}},
    {"text": "Real Madrid ใช้ระบบ 4-3-1-2 หรือ 4-4-2 Vinicius Jr. เป็นตัวแปรสำคัญด้านซ้าย Bellingham ทำหน้าที่ box-to-box midfielder ที่ทั้งรับและบุกได้ดี", "metadata": {"team": "Real Madrid", "category": "tactics"}},
    {"text": "Barcelona ยุค Xavi ใช้ tiki-taka สมัยใหม่ผสม high press Pedri และ Gavi เป็น midfield ที่เชื่อมเกมได้ดีที่สุดในโลก ใช้ระบบ 4-3-3 เน้น possession และ pressing", "metadata": {"team": "Barcelona", "category": "tactics"}},
    {"text": "ทีมชาติไทยใช้ระบบ 4-2-3-1 เป็นหลัก ชนาธิป สรงกระสินธ์ เป็นกัปตันทีมและเพลย์เมคเกอร์หลัก ธีราทร บุญมาทัน รับหน้าที่ fullback ฝั่งขวา สารัช อยู่เย็น เป็นกองหน้าหลัก ทีมมีจุดแข็งด้านความเร็วและการเคลื่อนที่", "metadata": {"team": "Thailand", "category": "national_team"}},
    {"text": "ทีมชาติไทยอยู่ใน FIFA Ranking ประมาณอันดับ 110-120 ของโลก ในอาเซียนถือว่าแข็งแกร่งเป็นอันดับต้น ๆ เคยคว้าแชมป์ AFF Championship หลายสมัย โอกาสไป World Cup ยังต้องพัฒนาอีกมาก", "metadata": {"team": "Thailand", "category": "national_team"}},
    {"text": "xG หรือ Expected Goals คือสถิติที่วัดคุณภาพของโอกาสยิงประตู โดยคำนวณจากตำแหน่ง มุม และสถานการณ์ก่อนยิง ค่า xG สูงหมายถึงมีโอกาสยิงที่ดี ทีมที่ xG สูงกว่าคู่แข่งมักชนะในระยะยาว", "metadata": {"category": "stats_explained"}},
    {"text": "PPDA หรือ Passes Allowed Per Defensive Action วัดความเข้มข้นของ pressing ยิ่งค่าต่ำยิ่ง press หนัก ทีมที่ PPDA ต่ำกว่า 10 ถือว่า press หนักมาก เช่น Liverpool และ Arsenal", "metadata": {"category": "stats_explained"}},
    {"text": "Formation 4-3-3 เหมาะกับทีมที่เน้นครองบอลและ press สูง มี width จาก wingers และ midfield 3 คนช่วยสร้างและทำลายเกม ข้อเสียคือเสี่ยงต่อการถูกโจมตีช่องกลางสนาม", "metadata": {"category": "tactics_explained"}},
]

if __name__ == "__main__":
    add_documents(docs)
    print("Ingest เสร็จแล้วครับ!")