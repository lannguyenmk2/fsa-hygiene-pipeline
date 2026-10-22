import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "https://api.ratings.food.gov.uk"
HEADERS = {"x-api-version": "2", "accept": "application/json"}

def _session() -> requests.Session:
    """Session that retries on rate limits and server errors."""
    s = requests.Session()
    retry = Retry(
        total=5, 
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update(HEADERS)
    return s

def get_establishments(authority_id: int, page_size: int = 500):
    """Yield every establishment for one local authority, page by page"""
    session = _session()
    page = 1
    while True:
        resp = session.get(
            f"{BASE}/Establishments",
            params={
                "localAuthorityId": authority_id,
                "pageNumber": page,
                "pageSize": page_size,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        rows = data.get("establishments", [])
        if not rows:
            break
        yield from rows
        if page >= data["meta"]["totalPages"]:
            break
        page += 1