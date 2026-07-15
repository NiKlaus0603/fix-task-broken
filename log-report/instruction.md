There is an Apache-style access log at `/app/access.log`. Write a JSON summary report to `/app/report.json`.

Success criteria:
1. Create `/app/report.json` as a valid JSON object.
2. The JSON object must contain exactly these keys: `total_requests`, `unique_ips`, and `top_path`.
3. `total_requests` must equal the number of non-empty log lines in `/app/access.log`.
4. `unique_ips` must equal the number of distinct client IP addresses, using the first whitespace-separated field from each non-empty log line.
5. `top_path` must be the request path that appears most often inside the quoted HTTP request. If more than one path has the same highest count, choose the path that reached that count first while reading the file from top to bottom.
