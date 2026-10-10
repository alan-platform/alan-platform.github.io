---
layout: "doc"
origin: "auto-webclient"
language: "release notes"
version: "partitions-108.5.1"
type: "release notes"
---
## partitions-108.5.1 (after zora.3)

Changes:
- Support model language 109 (partitions)
- auto-webclient: reference sets of partition aggregate branches
- Views language: a query binds with `binds:` and takes node, number and text parameters; client side `repetition` and `condition` filters
- Binary client protocol on new webserver endpoints; the webserver runs on an event loop and uses session cookies
- Login and logout follow the flow of the session manager
- Builds for darwin-arm64 instead of darwin-x64; the generator and annotator also build for Windows
- The packages ship an agent guide (AGENTS.md)

### Views language

The header of a query changed: `from` became `binds:` followed by the query binding context, and
the query path follows `path:`. A binding context that started with `@root` starts with `root`,
and a filter compares with the binding context through `= query context` instead of
`= view context`.

```
// old
query 'usages query'
	from root path +'usages'.'on entries'

// new
query 'usages query'
	binds: path: root +'usages'.'on entries'
```

New in a query:
- `node parameter`, `number parameter` and `text parameter`, taken from the query binding context
  (`query context <path>`). A text filter compares with a parameter through `text $'p'`; a number
  criterium adds parameters: `$'a' + $'b' + 5`.
- `repetition <path> .'start' every .'interval' until .'end' in $'block start' + $'block length'`,
  applied by the client to the result.
- `condition $'p'`: the query has no entries when the node parameter is not resolved.

### Upgrade

- The project needs model language 109; see the model release notes.
- webclient: rewrite the query headers in `views.alan` as shown above; no transformation ships.
- auto-webclient: `annotations.alan` and `settings.alan` keep their syntax.
