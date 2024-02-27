from serpapi import GoogleSearch
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY","")

def product_search(image_url: str):
    params = {
        "engine": "google_lens",
        "url": image_url,
        "hl": "ja",
        "country": "jp",
        "api_key": SERPAPI_KEY,
    }
    search = GoogleSearch(params)
    search_results = search.get_dict()
    matches = search_results.get("visual_matches", [])
    return matches[:5]
