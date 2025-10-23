import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from requests.exceptions import RequestException

HEADERS = {"User-Agent":"CuotaProScraper/1.0 (+https://example.com) Python/requests"}

@retry(reraise=True, stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=20), retry=retry_if_exception_type(RequestException))
def fetch_requests(url, timeout=15):
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text

def try_fetch_sequence(url):
    try:
        html = fetch_requests(url)
        return {"method":"requests", "content":html}
    except Exception as e:
        return {"method":"requests_failed", "error": str(e)}
