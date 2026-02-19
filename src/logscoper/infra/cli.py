import argparse
from src.logscoper.adapters.parser import  parse_time
from src.logscoper.adapters.reader import read_logs
from src.logscoper.infra.input_output import print_stats, print_filtered, print_hist
from src.logscoper.commands.filter import apply_filter
from src.logscoper.commands.hist import build_hist
from src.logscoper.commands.stats import compute_stats


# commands
def cmd_stats(args: argparse.Namespace) -> int:
    try:
        logs = read_logs(args.path)
    except FileNotFoundError:
        return 2

    until_dt = parse_time(args.until)
    since_dt = parse_time(args.since)
    stats = compute_stats(logs, args.top, since_dt, until_dt, args.status, args.grep, args.json)
    print_stats(stats)
    return 0


def cmd_filter(args: argparse.Namespace) -> int:
    try:
        logs = read_logs(args.path)
    except FileNotFoundError:
        return 2
    until_dt = parse_time(args.until)
    since_dt = parse_time(args.since)
    filtered_logs = apply_filter(logs, since_dt, until_dt, args.status, args.grep)
    if getattr(args, "out", None):
        with open(args.out, "w") as out:
            print_filtered(filtered_logs, out)
    else:
        print_filtered(filtered_logs)
    return 0


def cmd_hist(args: argparse.Namespace) -> int:
    try:
        logs = read_logs(args.path)
    except FileNotFoundError:
        return 2
    until_dt = parse_time(args.until)
    since_dt = parse_time(args.since)
    bucket_ms = getattr(args, "bucket_ms", 100)
    strict = bool(getattr(args, "strict", False))
    is_json = bool(getattr(args, "json", False))
    hist = build_hist(logs, bucket_ms, strict, since_dt, until_dt, args.status, args.grep)
    if not hist and strict:
        return 2
    print_hist(hist, is_json)
    return 0


# parser
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logscoper",
        description="Simple access log analyzer",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # stats
    ps = sub.add_parser("stats", help="Show aggregated stats")
    ps.add_argument("--path", required=True)
    ps.add_argument("--top", type=int, default=10)
    ps.add_argument("--since")
    ps.add_argument("--until")
    ps.add_argument("--status")
    ps.add_argument("--grep")
    ps.add_argument("--json", action="store_true")
    ps.set_defaults(func=cmd_stats)

    # filter
    pf = sub.add_parser("filter", help="Filter and print normalized lines")
    pf.add_argument("--path", required=True)
    pf.add_argument("--since")
    pf.add_argument("--until")
    pf.add_argument("--status")
    pf.add_argument("--grep")
    pf.add_argument("--out")
    pf.set_defaults(func=cmd_filter)

    # hist
    ph = sub.add_parser("hist", help="Request time histogram")
    ph.add_argument("--path", required=True)
    ph.add_argument("--bucket-ms", type=int, default=100, dest="bucket_ms")
    ph.add_argument("--since")
    ph.add_argument("--until")
    ph.add_argument("--status")
    ph.add_argument("--grep")
    ph.add_argument("--json", action="store_true")
    ph.add_argument("--strict", action="store_true")
    ph.set_defaults(func=cmd_hist)

    return parser
