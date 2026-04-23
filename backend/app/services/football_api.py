import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": os.getenv("FOOTBALL_API_KEY")}

LEAGUES = {
    "EPL": "PL",
    "LaLiga": "PD",
    "CL": "CL",
    "Serie A": "SA",
    "Bundesliga": "BL1",
}

async def get_standings(league: str):
    code = LEAGUES.get(league, "PL")
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/competitions/{code}/standings",
            headers=HEADERS,
        )
        data = res.json()
        table = data["standings"][0]["table"]
        return [
            {
                "rank": t["position"],
                "team": t["team"]["name"],
                "played": t["playedGames"],
                "won": t["won"],
                "drawn": t["draw"],
                "lost": t["lost"],
                "goals_for": t["goalsFor"],
                "goals_against": t["goalsAgainst"],
                "points": t["points"],
            }
            for t in table[:10]
        ]

async def get_top_scorers(league: str):
    code = LEAGUES.get(league, "PL")
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/competitions/{code}/scorers",
            headers=HEADERS,
        )
        data = res.json()
        return [
            {
                "name": p["player"]["name"],
                "team": p["team"]["name"],
                "goals": p["goals"],
                "assists": p.get("assists") or 0,
            }
            for p in data["scorers"][:5]
        ]

async def get_fixtures_today():
    from datetime import date
    today = date.today().isoformat()
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/matches",
            headers=HEADERS,
            params={"dateFrom": today, "dateTo": today},
        )
        data = res.json()
        matches = data.get("matches", [])
        if not matches:
            return []
        return [
            {
                "home": m["homeTeam"].get("name", "Unknown"),
                "away": m["awayTeam"].get("name", "Unknown"),
                "league": m["competition"].get("name", "Unknown"),
                "status": m.get("status", ""),
                "score": f"{m['score']['fullTime'].get('home', '-')} - {m['score']['fullTime'].get('away', '-')}",
            }
            for m in matches[:10]
            if m.get("homeTeam") and m.get("awayTeam")
        ]