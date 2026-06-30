"""
Proves the critical path: execute a *parameterized* saved Dune query via the
free-tier API and read results back. Run once before trusting Week 2 onward.
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv() # reads .env from the repo root into the environment

API_KEY = os.environ["DUNE_API_KEY"]   # never hardcode
QUERY_ID = 7836510                       # <-- one of YOUR saved queries
PARAMS = {}               # <-- match your query's params (or {})

BASE = "https://api.dune.com/api/v1"
HEADERS = {"X-Dune-API-Key": API_KEY}

# 1) execute (this is the call that spends an execution credit)
r = requests.post(f"{BASE}/query/{QUERY_ID}/execute",
                  headers=HEADERS, json={"query_parameters": PARAMS})
r.raise_for_status()
execution_id = r.json()["execution_id"]
print("execution_id:", execution_id)

# 2) poll status until done (this is why execution is async)
while True:
    s = requests.get(f"{BASE}/execution/{execution_id}/status", headers=HEADERS)
    s.raise_for_status()
    state = s.json()["state"]
    print("state:", state)
    if state == "QUERY_STATE_COMPLETED":
        break
    if state in ("QUERY_STATE_FAILED", "QUERY_STATE_CANCELLED"):
        raise SystemExit(f"execution did not complete: {state}")
    time.sleep(2)

# 3) fetch results
res = requests.get(f"{BASE}/execution/{execution_id}/results", headers=HEADERS)
res.raise_for_status()
rows = res.json()["result"]["rows"]
print(f"got {len(rows)} rows; first row: {rows[0] if rows else 'none'}")
