import re
from datetime import datetime
from typing import List

from src.logscoper.models.domain import make_status, LogEntry


def apply_filter(logs: List[LogEntry],
                 since_dt: datetime | None,
                 until_dt: datetime | None,
                 requested_status: str | None,
                 grep: str | None,
                 ) -> List[LogEntry]:
    filtered_logs: List[LogEntry] = []
    status_filter = make_status(requested_status)
    grep_re = re.compile(grep) if grep else None
    for log in logs:
        if (since_dt and log.ts < since_dt) or (until_dt and log.ts >= until_dt):
            continue
        if not status_filter(str(log.status)):
            continue
        if grep_re and not grep_re.search(log.path):
            continue
        filtered_logs.append(log)

    return filtered_logs
