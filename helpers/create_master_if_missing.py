import csv
from pathlib import Path

MASTER = Path("storage/cuotapro_historial_master.csv")
MASTER.parent.mkdir(parents=True, exist_ok=True)

HEADERS = ["block_id","date","sport","competition","home","away","market","odds","prob_p","ev","kelly_cap","status","verification_sources","correlation_flag","result_final","hit","notes","discard_reason","source_url","scrape_time"]

def ensure_master():
    if not MASTER.exists():
        with open(MASTER, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        print("Created master file:", MASTER)
    else:
        print("Master file exists:", MASTER)

if __name__ == "__main__":
    ensure_master()
