
import re
import json
import os
from typing import Dict, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_tags():
    import pandas as pd
    return pd.read_csv(os.path.join(DATA_DIR, "tags.csv"))

def load_templates():
    with open(os.path.join(DATA_DIR, "templates.json"), encoding="utf-8") as f:
        return json.load(f)

TEMPLATES = load_templates()

def classify(text: str, market: str = "JP") -> str:
    """Simple keyword matching; return first matching tag."""
    tags_df = load_tags()
    field = "jp_keywords" if market == "JP" else "us_keywords"
    for _, row in tags_df.iterrows():
        kws = str(row[field]).split("|")
        if any(kw.strip() and kw.strip().lower() in text.lower() for kw in kws):
            return row["tag"]
    return "材料未確認"

def extract_fields(text: str) -> Dict[str, str]:
    # Simple regexes; tune later
    pct = re.findall(r'([+\-]?\d+(?:\.\d+)?)\s*%?', text)
    money = re.findall(r'([0-9]+(?:\.[0-9]+)?\s*(?:億円|万円|B\$|M\$|億円相当|円))', text, flags=re.I)
    ratio = re.search(r'(\d+)\s*[対xX]\s*(\d+)', text)
    fields = {}
    if len(pct) >= 2:
        fields["rev_pct"] = pct[0]
        fields["op_pct"] = pct[1]
    elif len(pct) == 1:
        fields["rev_pct"] = pct[0]
    if money:
        fields["op_amount"] = money[0]
        fields["bb_amount"] = money[0]
        fields["award_amount"] = money[0]
        fields["deal_amount"] = money[0]
        fields["div_amount"] = money[0]
    if ratio:
        fields["split_ratio"] = f"{ratio.group(1)}対{ratio.group(2)}"
    # Fallbacks
    fields.setdefault("rev_pct", "—")
    fields.setdefault("op_pct", "—")
    fields.setdefault("op_amount", "—")
    fields.setdefault("bb_amount", "—")
    fields.setdefault("award_amount", "—")
    fields.setdefault("deal_amount", "—")
    fields.setdefault("div_amount", "—")
    fields.setdefault("bb_period", "—")
    fields.setdefault("product", "製品")
    return fields

def truncate_ja(s: str, limit: int = 80) -> str:
    # naive truncation; ensure <= limit chars
    return s if len(s) <= limit else s[:limit-1] + "…"

def render(tag: str, source_label: str, fields: Dict[str, str], limit: int = 80) -> str:
    tpl = TEMPLATES.get(tag, "{source}")
    txt = tpl.format(source=source_label, **fields)
    return truncate_ja(txt, limit)
