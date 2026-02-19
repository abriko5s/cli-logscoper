from __future__ import annotations
from typing import List
from src.logscoper.adapters.parser import parse_line
from src.logscoper.models.domain import LogEntry


def read_logs(path: str) -> List[LogEntry]:
    logs: List[LogEntry] = []
    with open(path) as f:
        for line in f:
            log = parse_line(line)
            if isinstance(log, LogEntry):
                logs.append(log)
    return logs
