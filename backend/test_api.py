import urllib.request
import json

endpoints = [
    "/api/jobs",
    "/api/skills",
    "/api/skills/trends",
    "/api/skills/categories",
    "/api/skills/top-emerging",
    "/api/skills/regional-demand",
    "/api/users/1",
    "/api/analysis/1/gap",
    "/api/analysis/1/match-score",
    "/api/analysis/dashboard-stats",
    "/api/recommendations/1",
    "/api/jobs/1/extract-skills",
]

for ep in endpoints:
    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:8000{ep}")
        data = json.loads(r.read())
        if isinstance(data, list):
            print(f"OK  {ep}  ->  {len(data)} items")
        elif isinstance(data, dict):
            keys = list(data.keys())[:5]
            print(f"OK  {ep}  ->  {keys}")
    except Exception as e:
        print(f"FAIL {ep}  ->  {e}")
