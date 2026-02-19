import json
from ..models.domain import Stats

# STATS STUFF
def stats_text_render(stats: Stats) -> str:
    lines: list[str] = [f'Total: {stats.total}']
    lines.append("By status:")
    for (num, cnt) in sorted(stats.by_status.items()):
        lines.append(f'{num}: {cnt}')
    lines.append(
        f'Avg RT (ms): {stats.rt_avg_ms:.2f}'
        if stats.rt_avg_ms else
        'Avg RT (ms): n/a'
    )
    lines.append(
        f'P95 RT (ms): {stats.rt_p95_ms:.2f}'
        if stats.rt_p95_ms else
        'P95 RT (ms): n/a'
    )
    lines.append(
        f'P99 RT (ms): {stats.rt_p99_ms:.2f}'
        if stats.rt_p99_ms else
        'P99 RT (ms): n/a'
    )
    lines.append("Top paths:")
    for path, cnt in stats.top_paths:
        lines.append(f'{cnt} {path}')
    return "\n".join(lines)


def stats_json_render(stats: Stats) -> str:
    data = {
        'total': stats.total,
        'status': stats.by_status,
        'rt_avg_ms': stats.rt_avg_ms,
        'rt_p95_ms': stats.rt_p95_ms,
        'rt_p99_ms': stats.rt_p99_ms,
        'top_paths': [[p, c] for p, c in stats.top_paths]
    }
    return json.dumps(data)
