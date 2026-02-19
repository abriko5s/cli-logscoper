from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from math import ceil
from typing import Counter, List, Callable, Any
import re

# REGS FOR LOGS
LOG_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<ts>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<path>.*?)(?:\s+HTTP/\d\.\d)?"\s+'
    r'(?P<status>\d{3})\s+(?P<bytes>\S+)'
    r'(?:\s+"[^"]*"\s+"[^"]*")?'
    r'(?:\s+(?P<rt>\d+\.\d+)|\s+rt=(?P<rt_kv>\d+\.\d+))?'
)

RT_KV_RE = re.compile(r'(?:^|\s)rt=(?P<rt>\d+\.\d+)\b')  # useless chmo

# CONST VALUES
timezone_format: str = "%d/%b/%Y:%H:%M:%S %z"


# METHODS
def make_status(spec: str | None) -> (Callable[[Any], bool] | Callable[[str], bool]):
    if not spec:
        return lambda s: True
    tokens = [t.strip() for t in spec.split(",") if t.strip()]
    exact: set[str] = set()
    mask: list[str] = []
    for t in tokens:
        if re.fullmatch(r"[1-5]xx", t):
            mask.append(t[0])
        elif re.fullmatch(r"\d{3}", t):
            exact.add(t)

    def pred(num: str) -> bool:
        return num in exact or any(num.startswith(m) for m in mask)

    return pred


def percentile(values: list[float], p: int | float) -> float:
    n = len(values)
    values = sorted(values)
    k = ceil(p / 100 * n) - 1
    return values[max(0, min(k, n - 1))]


# CLASSES
@dataclass(frozen=True)
class LogEntry:
    ip: str
    ts: datetime
    method: str
    path: str
    status: int
    bytes_sent: int | None
    request_time_s: float | None


@dataclass
class Stats:
    def __init__(
            self,
            total: int,
            by_status: Counter[int],
            rt_avg_ms: float | None,
            rt_p95_ms: float | None,
            rt_p99_ms: float | None,
            top_paths: List[tuple[str, int]],
            is_json: bool):
        self.total = total
        self.by_status = by_status
        self.rt_avg_ms = rt_avg_ms
        self.rt_p95_ms = rt_p95_ms
        self.rt_p99_ms = rt_p99_ms
        self.top_paths = top_paths
        self.is_json = is_json
