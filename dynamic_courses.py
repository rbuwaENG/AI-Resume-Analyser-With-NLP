import os
import json
import time
import re
from datetime import datetime, timedelta
from typing import List, Tuple
import requests
import xml.etree.ElementTree as ET

CACHE_FILE = os.path.join(os.path.dirname(__file__), "courses_cache.json")
CACHE_TTL_DAYS = 7

YOUTUBE_FEED_BY_CHANNEL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

CHANNELS = {
    "ds": [
        # freeCodeCamp.org
        "UC8butISFwT-Wl7EV0hUK0BQ",
        # Google Developers
        "UC_x5XG1OV2P6uZZ5FSM9Ttw",
    ],
    "web": [
        # freeCodeCamp.org
        "UC8butISFwT-Wl7EV0hUK0BQ",
        # The Net Ninja
        "UCW5YeuERMmlnqo4oq8vwUpg",
    ],
    "android": [
        # Android Developers
        "UCVHFbqXqoYvEWM1Ddxl0QDg",
    ],
    "ios": [
        # Apple Developer
        "UCE_M8A5yxnLfW0KghEeajjw",
    ],
    "uiux": [
        # DesignCourse
        "UCVyRiMvfUNMA1UPlDPzG5Ow",
        # Figma (community)
        "UCQs5NiuR2M4Ww6U8L1lb2XQ",
    ],
}

KEYWORDS = {
    "ds": ["data", "machine learning", "ml", "deep learning", "pandas", "numpy", "scikit", "tensorflow", "pytorch"],
    "web": ["react", "next.js", "node", "django", "angular", "vue", "javascript", "typescript", "flask", "web"],
    "android": ["android", "kotlin", "jetpack", "compose", "java"],
    "ios": ["ios", "swift", "xcode", "swiftui"],
    "uiux": ["ui", "ux", "figma", "design", "prototype", "wireframe"],
}


def _normalize_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    return title


def _fetch_channel_feed(channel_id: str) -> List[Tuple[str, str]]:
    url = YOUTUBE_FEED_BY_CHANNEL.format(channel_id=channel_id)
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    ns = {"yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    entries = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title_el = entry.find("{http://www.w3.org/2005/Atom}title")
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        if title_el is None or link_el is None:
            continue
        title = _normalize_title(title_el.text)
        url = link_el.attrib.get("href", "")
        if title and url:
            entries.append((title, url))
    return entries


def _filter_by_keywords(items: List[Tuple[str, str]], keywords: List[str]) -> List[Tuple[str, str]]:
    if not keywords:
        return items
    result = []
    for title, url in items:
        lt = title.lower()
        if any(k in lt for k in keywords):
            result.append((title, url))
    return result


def _dedupe(items: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    seen = set()
    deduped = []
    for title, url in items:
        if url in seen:
            continue
        seen.add(url)
        deduped.append((title, url))
    return deduped


def _load_cache() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(data: dict) -> None:
    tmp = CACHE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, CACHE_FILE)


def _is_fresh(ts: float) -> bool:
    try:
        return (datetime.utcnow() - datetime.utcfromtimestamp(ts)) < timedelta(days=CACHE_TTL_DAYS)
    except Exception:
        return False


def fetch_latest_courses(category: str, limit: int = 10) -> List[Tuple[str, str]]:
    category = category.lower()
    channel_ids = CHANNELS.get(category, [])
    keywords = KEYWORDS.get(category, [])
    all_items: List[Tuple[str, str]] = []
    for cid in channel_ids:
        try:
            items = _fetch_channel_feed(cid)
            all_items.extend(items)
        except Exception:
            continue
    filtered = _filter_by_keywords(all_items, keywords)
    deduped = _dedupe(filtered)
    return deduped[:limit]


def get_dynamic_courses(category: str, limit: int = 10) -> List[Tuple[str, str]]:
    cache = _load_cache()
    key = f"{category}:{limit}"
    entry = cache.get(key)
    if entry and _is_fresh(entry.get("ts", 0)):
        return entry.get("items", [])
    items = fetch_latest_courses(category, limit=limit)
    if items:
        cache[key] = {"ts": time.time(), "items": items}
        _save_cache(cache)
    return items