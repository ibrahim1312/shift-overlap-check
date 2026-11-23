"""Check a staff or resource schedule CSV for overlapping bookings across time zones."""

import argparse
import json
from decimal import InvalidOperation
from pathlib import Path
import csv
from collections import defaultdict
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description='Check a staff or resource schedule CSV for overlapping bookings across time zones.')
    parser.add_argument("schedule", type=Path)
    args = parser.parse_args()

    def parse_time(value):
        result = datetime.fromisoformat(value)
        if result.utcoffset() is None:
            raise ValueError("Timestamps require an explicit UTC offset")
        return result.astimezone(timezone.utc)

    rows = defaultdict(list)
    with args.schedule.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not {"resource", "start", "end"} <= set(reader.fieldnames or []):
            raise ValueError("Required columns: resource, start, end")
        for row in reader:
            resource = row["resource"].strip()
            start, end = parse_time(row["start"]), parse_time(row["end"])
            if not resource or end <= start:
                raise ValueError(f"Row {reader.line_num}: resource required and end must follow start")
            rows[resource].append((start, end, reader.line_num))

    conflicts = []
    for resource, shifts in sorted(rows.items()):
        active = []
        for start, end, row in sorted(shifts):
            active = [(finish, earlier_row) for finish, earlier_row in active if finish > start]
            for _, earlier_row in active:
                conflicts.append({"resource": resource, "rows": sorted([row, earlier_row])})
            active.append((end, row))
    report = {"conflicts": conflicts}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, OverflowError, InvalidOperation, TypeError, csv.Error) as error:
        raise SystemExit(f"Error: {error}") from None
