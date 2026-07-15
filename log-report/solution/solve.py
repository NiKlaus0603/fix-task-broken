import json
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS)\s+(\S+)\s+HTTP/[^"]+"')


total_requests = 0
ips = set()
paths = Counter()
first_reached_best_order = {}
current_best = 0
reach_order = 0

for line in LOG_PATH.read_text().splitlines():
    if not line.strip():
        continue

    total_requests += 1
    parts = line.split()
    if parts:
        ips.add(parts[0])

    match = REQUEST_RE.search(line)
    if match:
        path = match.group(1)
        paths[path] += 1

        if paths[path] > current_best:
            current_best = paths[path]
            reach_order += 1
            first_reached_best_order[path] = reach_order
        elif paths[path] == current_best and path not in first_reached_best_order:
            reach_order += 1
            first_reached_best_order[path] = reach_order

if not paths:
    top_path = None
else:
    top_count = max(paths.values())
    top_path = min(
        (path for path, count in paths.items() if count == top_count),
        key=lambda path: first_reached_best_order[path],
    )

REPORT_PATH.write_text(json.dumps({
    "total_requests": total_requests,
    "unique_ips": len(ips),
    "top_path": top_path,
}, sort_keys=True))
