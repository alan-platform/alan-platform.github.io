---
layout: "doc"
origin: "auto-webclient"
language: "release notes"
version: "athena.2"
type: "release notes"
url: "/pages/docs/auto-webclient/athena.2/release-notes.html"
---
## athena.2 (after athena.1)

Changes:
- Planning: interaction modes (browse, select, create, move) with keyboard shortcuts
- Planning: select blocks and run a command on the selection (`selected items commands`)
- Planning: resize blocks (`resizable`), and drop a block on another item (`drop on item`)
- Planning: child rows nest to any depth
- Planning: the time shows while creating, moving and resizing blocks
- Planning: popups show their properties in one or more columns
- Handheld: the barcode feature on text inputs
- `./alan upgrade` converts an auto-webclient system from athena.1 and zora.4 (besides
  partitions-108.1a, zora.1, zora.2 and zora.3)

### Before the upgrade

Nothing.

### After the upgrade

From zora.4 the syntax is unchanged. From athena.1, zora.3 and older, the upgrade copies the planning
annotations unchanged; change them by hand. The build reports each one, fix them topmost error first.

- Each entry of a planning `rows` list (the `rows` of a window and `children`) is a group that holds
  the rows and, optionally, the `selected items commands`. Wrap the rows in `( 'rows' = ... )`. The
  build reports an entry that is not wrapped with
  ``no valid 'nodes' found for 'type' option 'nodes'. Unexpected 'strategy'``, defined by `.'planning row group'`:

```
// old
'rows' = [
	on .'rows'* (
		'label' = [ .'key' ( ) ]
	)
]

// new
'rows' = [
	( 'rows' = on .'rows'* (
		'label' = [ .'key' ( ) ]
	) )
]
```

- In `draggable`, `move` becomes `drop on row` and `alternative move command` becomes
  `alternative drop on row`. In a drop on row command, `can switch row` becomes `row scope`:
  `'yes'.'<row>'` becomes `'reference'.'<row>'`; drop `'can switch row' = 'no'`, as `'self'` is the
  default. The build reports the old names with ``entry `move` was not found in 'properties'`` and
  ``entry `can switch row` was not found in 'properties'``:

```
// old
'draggable' = (
	'move' = .'move' (
		'start' = .'start' ( )
		'can switch row' = 'yes'.'row' ( )
		'snap' = 'minute' 60
	)
)

// new
'draggable' = (
	'drop on row' = .'move' (
		'start' = .'start' ( )
		'row scope' = 'reference'.'row' ( )
		'snap' = 'minute' 60
	)
)
```

- A planning `popup` shows its properties in columns: its `node` moves into `'columns' = ( 'node' = ... )`
  and its `label` is removed; a column can take a `'header'` instead. The build reports the old popup
  with ``entry `label` was not found in 'properties'`` and ``entry `node` was not found in 'properties'``:

```
// old
'popup' = (
	'label' = [ .'key' ( ) ]
	'node' = [ 'text' .'key' ( ) ]
)

// new
'popup' = (
	'columns' = ( 'node' = [ 'text' .'key' ( ) ] )
)
```
