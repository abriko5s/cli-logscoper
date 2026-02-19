import re
from datetime import datetime
from typing import List, Dict

from src.logscoper.models.domain import make_status, LogEntry


def build_hist(logs: List[LogEntry],
               bucket_ms: int,
               strict: bool,
               since_dt: datetime | None,
               until_dt: datetime | None,
               requested_status: str | None,
               grep: str | None,
               ) -> Dict[str, int] | None:
    strict_cond: bool = False
    buckets: dict[int, int] = {}
    status_filter = make_status(requested_status)
    grep_re = re.compile(grep) if grep else None

    for log in logs:
        if (since_dt and log.ts < since_dt) or (until_dt and log.ts >= until_dt):
            continue
        if not status_filter(str(log.status)):
            continue
        if grep_re and not grep_re.search(log.path):
            continue
        if log.request_time_s:
            strict_cond = True
            rt_ms = log.request_time_s * 1000.0
            start = int(rt_ms) // bucket_ms * bucket_ms
            buckets[start] = buckets.get(start, 0) + 1
    if strict and not strict_cond:  # broken in this function => return 2 in main
        return None

    hist = {f"{start}-{start + bucket_ms}": cnt
            for start, cnt in sorted(buckets.items())}
    return hist
