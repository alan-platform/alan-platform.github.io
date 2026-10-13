---
layout: "doc"
origin: "webclient"
language: "release notes"
version: "partitions-108.6.0"
type: "release notes"
---
## partitions-108.6

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
- auto-webclient: `./alan upgrade` converts `annotations.alan` and `settings.alan` from zora.1, zora.2,
  zora.3 and partitions-108.1a. From zora.2 and zora.3 the syntax is unchanged. partitions-108.1a has the
  syntax of zora.1 and gets the same conversion. From zora.1 an entry of the `filters` and
  `properties` features starts with its property binding, which holds the `'label'` and the `'show'`,
  and a number criteria takes its value directly:

```
// zora.1
(
	'label' = "Number"
	'property' = .'number' (
		'filter' = 'yes' (
			'operator' = 'greater' ( )
			'criteria' = 'static' (
				'value' = 0
			)
		)
	)
	'show' = 'no' ( )
)

// now
.'number' (
	'label' = "Number"
	'filter' = 'yes' (
		'operator' = 'greater' ( )
		'criteria' = 'static' 0
	)
	'show' = 'no' ( )
)
```

  The transformation recognises an entry by its shape. Fix by hand what the build reports after it:
  - `'filter' = 'no' ( )` in `properties` becomes `'filter' =` (no filter), or `'filter' = 'none'` on a
    stategroup property.
  - A chart line with only a `'name'`, a `'y'` and at most one stategroup has the shape of an entry and
    is converted too (its name becomes `'label'`, its stategroup `'show'`); write it back as it was.
  - `'criteria' = 'now' 0` may be written as `'criteria' = 'now' ( )`.
  - From partitions-108.1a: the handheld `'string'` is no longer a node annotation (it had no effect
    there); remove it.

  Check by hand, as the build does not report it. When auto-webclient was zora.1 or partitions-108.1a
  before the upgrade (the conversion of `filters` and `properties` ran):
  - Every converted `filters` and `properties` entry against the file before the upgrade: its label,
    property path, show, filter and criteria values are under the right keys, nothing is added and
    nothing is missing.
  - Every converted node outside `filters` and `properties`: a node of another feature with the shape
    of an entry is converted too, and the build reports it only where that feature has no `'label'` or
    `'show'`.
  - Comments of a converted entry: a comment on its own line directly before its `'label'`,
    `'property'` or `'show'`, or before the `'value'` or `'offset'` of a number criteria, moves to the
    end of the converted entry, for example between its closing `)` and the `,`; other comments can
    move too, for example a comment before the entry to after it. Put them back where a reader expects
    them, next to the commented-out code they describe.
  - From zora.1: a text filter in `filters` without a `'filter'` was `'simple'` and is `auto` now,
    which filters a text with a reference by containment; write `'filter' = 'simple' ( )` to keep the
    old behaviour.

  From zora.1, a numerical type conversion evaluated by the client rounds to nearest since zora.2.
