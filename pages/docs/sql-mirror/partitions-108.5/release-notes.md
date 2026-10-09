---
layout: "doc"
origin: "sql-mirror"
language: "release notes"
version: "partitions-108.5"
type: "release notes"
---
## SQL-mirror 120 (after 119.2)

- sql-mirror mapping language: the `integer`, `decimal`, `date` and `date-time` data type mappings carry a mandatory value range, in raw datastore number values (julian days for `date`, julian seconds for `date-time`, the unscaled integer for `integer` and `decimal`). A value outside its range is written to the mirror as the range maximum, in both directions, and the mirror reports one line per clamped value on the consultant channel (the os-link error channel in engine mode, stderr in map mode) instead of letting the database refuse the statement. Every mapping file has to be regenerated; generated mappings pick the dialect defaults up automatically.
```
// old
data-types
	integer: "BIGINT"
	decimal: "DECIMAL"
	date: "DATE"
	date-time: "DATETIME"

// new (MySQL defaults; SQL Server starts its DATETIME range at 204018912000, 1753-01-01)
data-types
	integer: "BIGINT" [ -9223372036854775807 , 9223372036854775807 ]
	decimal: "DECIMAL" [ -9223372036854775807 , 9223372036854775807 ]
	date: "DATE" [ 2086302 , 5373483 ]
	date-time: "DATETIME" [ 180256492800 , 464269017599 ]
```

  **Upgrading a mapping from 119.1 or 119.2.** `./alan upgrade` runs the transformation for every sql-mirror system; by hand, from the project root:

  ```
  .alan/devenv/system-types/sql-mirror/upgrade/upgrade.sh 119.2 systems/<sys>
  ```

  The script reads the dialect from the mapping's `identifier-delimiter:` line, because the dialect decides the ranges. It rewrites `mapping.alan` in place, keeping the SQL types that are there and adding the widest range the dialect documents; nothing else in the mapping changes. The bounds are raw datastore values, not SQL literals, so a mirror on a `DATETIME2` column, or one that wants a narrower window than its column allows, edits the two numbers afterwards.
