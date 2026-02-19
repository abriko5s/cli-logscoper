from __future__ import annotations
from datetime import datetime, timezone
from src.logscoper.models.domain import LogEntry, LOG_RE, timezone_format


def parse_line(line: str) -> LogEntry | None:
    m = LOG_RE.search(line)
    if not m:
        return None
    ts = datetime.strptime(m.group("ts"), timezone_format)
    rt = m.group("rt") or m.group("rt_kv")
    bytes_cnt = None if m.group("bytes") == "-" else int(m.group("bytes"))
    return LogEntry(
        ip=m.group("ip"),
        ts=ts,
        method=m.group("method"),
        path=m.group("path").strip(),
        status=int(m.group("status")),
        bytes_sent=bytes_cnt,
        request_time_s=(float(rt) if rt else None))


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.strip())
    except ValueError:
        raise SystemExit(2)
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
