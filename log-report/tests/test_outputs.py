import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")
REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS)\s+(\S+)\s+HTTP/[^"]+"')


def _expected_report():
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

    return {
        "total_requests": total_requests,
        "unique_ips": len(ips),
        "top_path": top_path,
    }


def _read_report():
    try:
        return json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as exc:
        raise AssertionError(f"/app/report.json is not valid JSON: {exc}") from exc


def test_success_criterion_1_report_exists_and_is_valid_json():
    assert REPORT_PATH.exists(), "missing /app/report.json"
    report = _read_report()
    assert isinstance(report, dict), "report.json must contain a JSON object"


def test_success_criterion_2_report_has_exact_schema():
    assert set(_read_report()) == {"total_requests", "unique_ips", "top_path"}


def test_success_criterion_3_total_requests_is_correct():
    assert _read_report()["total_requests"] == _expected_report()["total_requests"]


def test_success_criterion_4_unique_ips_is_correct():
    assert _read_report()["unique_ips"] == _expected_report()["unique_ips"]


def test_success_criterion_5_top_path_is_correct():
    assert _read_report()["top_path"] == _expected_report()["top_path"]
