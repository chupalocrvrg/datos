import time, yaml, logging
from pathlib import Path
from scraper.fetcher import try_fetch_sequence
from scraper.parser import parse_page_for_fixtures
from scraper.utils import append_master_row, now_iso, make_event_id
from helpers.create_master_if_missing import ensure_master

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=LOG_DIR/"scraper.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

with open("config.yml","r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

RATE = cfg.get("rate_limit_seconds", 3)

with open("urls_list.txt","r", encoding="utf-8") as f:
    URLS = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

ensure_master()

block_id = now_iso().split("T")[0]

def normalize_and_store(fixt, src_url):
    home = fixt.get("home") or fixt.get("team1") or ""
    away = fixt.get("away") or fixt.get("team2") or ""
    dt = fixt.get("time_local") or fixt.get("raw_time") or ""
    event_id = make_event_id(home, away, dt or now_iso())
    row = {
        "block_id": block_id,
        "date": dt or "",
        "sport":"football",
        "competition":"",
        "home": home,
        "away": away,
        "market":"",
        "odds":"",
        "prob_p":"",
        "ev":"",
        "kelly_cap":"",
        "status":"parsed",
        "verification_sources":"",
        "correlation_flag":"",
        "result_final":"",
        "hit":"",
        "notes":"parsed from " + src_url,
        "discard_reason":"",
        "source_url": src_url,
        "scrape_time": now_iso()
    }
    append_master_row(row)
    return row

def process_url(url):
    logging.info(f"Processing URL {url}")
    r = try_fetch_sequence(url)
    if r.get("method") == "requests":
        html = r.get("content")
        fixtures = parse_page_for_fixtures(html, url)
        if fixtures:
            for f in fixtures:
                normalize_and_store(f, url)
            logging.info(f"Parsed {len(fixtures)} fixtures for {url}")
            return True
        else:
            logging.warning(f"No fixtures found by parser for {url}")
            return False
    else:
        logging.error(f"Requests failed for {url}: {r}")
        return False

def main():
    for url in URLS:
        tries = 0
        max_tries = 5
        backoff = 2
        success = False
        while tries < max_tries and not success:
            try:
                success = process_url(url)
                if not success:
                    tries += 1
                    logging.warning(f"Attempt {tries} failed for {url}, backing off {backoff}s")
                    time.sleep(backoff)
                    backoff *= 2
            except Exception as e:
                logging.exception("Unhandled error processing %s: %s", url, e)
                tries += 1
                time.sleep(backoff)
                backoff *= 2
        if not success:
            logging.error(f"All attempts failed for {url} after {max_tries} tries")
        time.sleep(RATE)

if __name__ == "__main__":
    main()
