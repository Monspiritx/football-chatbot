import schedule
import time
from news_ingest import run_ingest

# รันทันทีตอนเปิด
run_ingest()

# รันทุกวัน 6 โมงเช้า
schedule.every().day.at("06:00").do(run_ingest)

# รันทุก 6 ชั่วโมง
schedule.every(6).hours.do(run_ingest)

print("Scheduler รันอยู่ครับ กด Ctrl+C เพื่อหยุด")
print("อัปเดตข่าวทุก 6 ชั่วโมง และทุกวัน 06:00")

while True:
    schedule.run_pending()
    time.sleep(60)