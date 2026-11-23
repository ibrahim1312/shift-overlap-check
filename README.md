# Shift Overlap Check

Check a staff or resource schedule CSV for overlapping bookings across time zones.

## Quick start

Requires Python 3.11 or later. Uses the standard library and runs locally.

```bash
python3 tool.py shifts.csv
```

Output is formatted JSON on standard output. Invalid inputs report an error on standard error and exit with status 1. Run the tool with --help for all arguments.

Use ISO 8601 timestamps with offsets, such as +01:00 or Z. Adjacent shifts do not conflict. Resource matching is case sensitive.

## Example input

**shifts.csv**

```
resource,start,end
Room A,2026-01-01T09:00:00+01:00,2026-01-01T11:00:00+01:00
Room A,2026-01-01T09:30:00Z,2026-01-01T11:00:00Z
Room A,2026-01-01T11:00:00Z,2026-01-01T12:00:00Z
```

## Example output

```json
{
  "conflicts": [
    {
      "resource": "Room A",
      "rows": [
        2,
        3
      ]
    }
  ]
}
```

## License

[MIT](LICENSE).
