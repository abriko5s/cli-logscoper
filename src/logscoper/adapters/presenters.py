from typing import List, Dict
from ..models.domain import Stats, LogEntry
from src.logscoper.adapters.renders import stats_json_render
from src.logscoper.adapters.renders import stats_text_render


def render_stats(stats: Stats) -> str:
    if stats.is_json:
        return stats_json_render(stats)
    else:
        return stats_text_render(stats)


# FILTER STUFF
def render_filter(logs: List[LogEntry]) -> List[str]:
    str_logs: List[str] = []
    for log in logs:
        ts = log.ts
        bytes_out = log.bytes_sent if log.bytes_sent else "-"
        rt = log.request_time_s
        str_logs.append(
            f"{ts.isoformat()} {log.ip} {log.method} {log.path} "
            f"{log.status} {bytes_out}"
            f"{(' rt=' + str(rt)) if rt else ''}"
        )
    return str_logs


# HIST STUFF
def render_hist(hist: Dict[str, int]) -> List[str]:
    str_hist: List[str] = []
    for k, v in hist.items():
        str_hist.append(f"{k}: {'#' * v} {v}")
    return str_hist
