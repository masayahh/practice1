
from fastapi import FastAPI, Query
from typing import List, Literal
from datetime import date, timedelta
import json
import os
from .reason import render

app = FastAPI(title="今日一番熱い株 - MVP API")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SAMPLE_DIR = os.path.join(BASE_DIR, "sample_output")

def load_sample(date_str: str, market: str):
    path = os.path.join(SAMPLE_DIR, f"{market.lower()}_{date_str}.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

@app.get("/v1/highlights")
def highlights(date_str: str = Query(None), market: Literal["JP","US"] = "JP"):
    if not date_str:
        date_str = (date.today() - timedelta(days=1)).isoformat()
    data = load_sample(date_str, market)
    return data
