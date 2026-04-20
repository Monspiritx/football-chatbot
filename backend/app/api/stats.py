from fastapi import APIRouter, HTTPException
from app.services.football_api import (
    get_standings,
    get_top_scorers,
    get_fixtures_today,
)

router = APIRouter()

LEAGUES = {"EPL": 39, "LaLiga": 140, "CL": 2, "Serie A": 135, "Bundesliga": 78}

@router.get("/standings/{league}")
async def standings(league: str):
    league_id = LEAGUES.get(league)
    if not league_id:
        raise HTTPException(status_code=404, detail=f"League {league} not found")
    return await get_standings(league_id)

@router.get("/topscorers/{league}")
async def top_scorers(league: str):
    league_id = LEAGUES.get(league)
    if not league_id:
        raise HTTPException(status_code=404, detail=f"League {league} not found")
    return await get_top_scorers(league_id)

@router.get("/fixtures/today")
async def fixtures_today():
    return await get_fixtures_today()