import json
from typing import List, TextIO, Dict

from src.logscoper.adapters.presenters import render_stats, render_filter, render_hist
from src.logscoper.models.domain import Stats, LogEntry


def print_stats(stats: Stats) -> None:
    print(render_stats(stats))


def print_filtered(logs: List[LogEntry], out: TextIO | None = None) -> None:
    str_logs = render_filter(logs)
    for log in str_logs:
        print(log, file=out)


def print_hist(hist: Dict[str, int], is_json: bool = False) -> None:
    if is_json:
        print(json.dumps(hist))
    else:
        print(render_hist(hist))
