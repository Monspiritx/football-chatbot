import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

import feedparser
import httpx
import chromadb
import hashlib
from datetime import datetime
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="football_knowledge")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# RSS feeds ข่าวบอล
RSS_FEEDS = [
    {"url": "https://feeds.bbci.co.uk/sport/football/rss.xml", "source": "BBC Sport"},
    {"url": "https://www.theguardian.com/football/rss", "source": "The Guardian"},
    {"url": "https://www.goal.com/feeds/en/news", "source": "Goal.com"},
    
    # บอลเอเชีย
    {"url": "https://www.goal.com/en-sg/feeds/news?fmt=rss", "source": "Goal Asia"},
    {"url": "https://www.afcsiteassets.com/rss/news.xml", "source": "AFC"},
    {"url": "https://www.the-afc.com/rss/news", "source": "AFC News"},
    
    # บอลไทย
    {"url": "https://www.siamsport.co.th/rss.xml", "source": "Siam Sport"},
    {"url": "https://www.thsport.com/feed", "source": "TH Sport"},
    {"url": "https://www.smmsport.com/feed/", "source": "SMM Sport"},
]

def make_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def already_exists(doc_id: str) -> bool:
    try:
        result = collection.get(ids=[doc_id])
        return len(result["ids"]) > 0
    except:
        return False

EXCLUDE_KEYWORDS = [
    "women", "woman", "female", "wsl", "nwsl",
    "women's", "girls", "ladies", "ona batlle",
    "beth mead", "leah williamson", "alexia putellas",
    "sam kerr", "vivianne miedema", "ada hegerberg",
]

THAI_FOOTBALL_KEYWORDS = [
    "ไทย", "ทีมชาติ", "thai", "thailand", "tpl",
    "ไทยลีก", "thai league", "บุรีรัมย์", "ชลบุรี",
    "สมาคมฟุตบอล", "fat", "ชนาธิป", "ธีราทร", "สารัช",
    "aff", "asean", "อาเซียน", "sea games",
]

ASIAN_FOOTBALL_KEYWORDS = [
    "afc", "asian cup", "เอเชีย", "j-league", "k-league",
    "จีน", "ญี่ปุ่น", "เกาหลี", "china", "japan", "korea",
    "saudi", "qatar", "uae", "iran", "australia", "a-league",
]

def is_relevant_football(text: str) -> bool:
    text_lower = text.lower()
    # กรองบอลหญิงออก
    if any(keyword in text_lower for keyword in EXCLUDE_KEYWORDS):
        return False
    return True

def is_mens_football(text: str) -> bool:
    text_lower = text.lower()
    return not any(keyword in text_lower for keyword in EXCLUDE_KEYWORDS)

def ingest_feed(feed_url: str, source: str):
    print(f"กำลังดึงข่าวจาก {source}...")
    try:
        feed = feedparser.parse(feed_url)
        added = 0
        skipped = 0
        for entry in feed.entries[:20]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            published = entry.get("published", "")

            if not title or not summary:
                continue

            text = f"{title}. {summary}"

            # กรองบอลหญิงออก
            if not is_mens_football(text):
                skipped += 1
                continue

            doc_id = make_id(text)
            if already_exists(doc_id):
                continue

            embedding = model.encode([text]).tolist()
            collection.add(
                ids=[doc_id],
                documents=[text],
                embeddings=embedding,
                metadatas=[{
                    "source": source,
                    "link": link,
                    "published": published,
                    "ingested_at": datetime.now().isoformat(),
                    "category": "news",
                    "gender": "mens",
                }]
            )
            added += 1

        print(f"เพิ่มข่าวใหม่ {added} รายการ, ข้ามบอลหญิง {skipped} รายการ จาก {source}")
        return added

    except Exception as e:
        print(f"Error จาก {source}: {e}")
        return 0
    
# ล้าง news เก่าทิ้งก่อน (เฉพาะ category: news)
def clear_news():
    try:
        results = collection.get(where={"category": "news"})
        if results["ids"]:
            collection.delete(ids=results["ids"])
            print(f"ลบข่าวเก่า {len(results['ids'])} รายการแล้ว")
    except Exception as e:
        print(f"ล้างข่าวไม่ได้: {e}")

def run_ingest():
    print(f"\n=== Auto Ingest เริ่มต้น {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    clear_news()  # ล้างข่าวเก่าก่อน
    total = 0
    for feed in RSS_FEEDS:
        total += ingest_feed(feed["url"], feed["source"])
    print(f"=== รวมเพิ่มข่าวใหม่ {total} รายการ ===\n")

if __name__ == "__main__":
    run_ingest()