from __future__ import annotations
import re
from datetime import datetime
from typing import List, Counter

from src.logscoper.models.domain import make_status, percentile, Stats, LogEntry

def compute_stats(logs: List[LogEntry],
                  top: int,
                  since_dt: datetime | None,
                  until_dt: datetime | None,
                  requested_status: str | None,
                  grep: str | None,
                  is_json: bool = False,
                  ) -> Stats:
    total: int = 0
    by_status: Counter[int] = Counter()
    path_counts: Counter[str] = Counter()
    rt_ms: List[float] = []
    status_filter = make_status(requested_status)
    grep_re = re.compile(grep) if grep else None
    for log in logs:
        if (since_dt and log.ts < since_dt) or (until_dt and log.ts >= until_dt):
            continue
        if not status_filter(str(log.status)):
            continue
        if grep_re and not grep_re.match(str(log.path)):
            continue

        total += 1
        by_status[log.status] += 1
        if log.request_time_s:
            rt_ms.append(log.request_time_s * 1000.0)
        path_counts[str(log.path)] += 1

    avg_ms = round(sum(rt_ms) / len(rt_ms)) if rt_ms else None
    p95_ms = percentile(rt_ms, 95) if rt_ms else None
    p99_ms = percentile(rt_ms, 99) if rt_ms else None
    top_paths = path_counts.most_common(top)

    stats = Stats(
        total=total,
        by_status=by_status,
        rt_avg_ms=avg_ms,
        rt_p95_ms=p95_ms,
        rt_p99_ms=p99_ms,
        top_paths=top_paths,
        is_json=is_json,
    )
    return stats
