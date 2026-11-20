---
layout: "doc"
origin: "auto-webclient"
language: "release notes"
version: "athena.3"
type: "release notes"
url: "/pages/docs/auto-webclient/athena.3/release-notes.html"
---
## athena.3 (after athena.2)

Changes:
- Derived properties: with advanced features on, the label of a derived number, text, state group or file opens its derivation: the definition as written in the model (with translated names), and a tree with the live values of its paths (amounts for reference sets), the case taken by a switch, and deeplinks to the source properties (click: current window, Ctrl: secondary window, Alt: the property instead of the referenced entry). Hovering the label shows the definition. Aggregates over collections and reference sets are approximated in the client and marked with ≈
- Work lists (work for user, work for all): the columns are the parent headers, the key (unless suppressed), the identifying properties, the actions, the properties of the todo node, and the outlining properties of the rest of the entry; an entry without outlining properties shows all its properties
- Queries follow the graph order of a collection, and entries can be re-ordered in that order
- Actions inside operation parameters
- The show hidden properties setting also shows hidden commands and reference sets
- Planning: move the selected blocks together; the cursor shows what a press would do; end entry creation and fold all, and set query filters for children, at any depth
- Handheld: date and duration widgets for identifying number properties, and the unit in number cells of reference candidates
- Identifying files open their preview on click
- `./alan upgrade` converts an auto-webclient system from athena.2 (besides athena.1, zora.4,
  zora.3, zora.2, zora.1 and partitions-108.1b)

### Before the upgrade

Nothing.

### After the upgrade

From athena.2 the syntax is unchanged. From athena.1 and older, also follow "After the upgrade" of
athena.2 below.

## athena.2 (after athena.1)

Changes:
- Planning: interaction modes (browse, select, create, move) with keyboard shortcuts
- Planning: select blocks and run a command on the selection (`selected items commands`)
- Planning: resize blocks (`resizable`), and drop a block on another item (`drop on item`)
- Planning: child rows nest to any depth
- Planning: the time shows while creating, moving and resizing blocks
- Planning: popups show their properties in one or more columns
- Handheld: the barcode feature on text inputs
- Todos: use the `@label:`, `@description:` and `@style:` annotations of a todo (see [Todo annotations](#todo-annotations))
- `./alan upgrade` converts an auto-webclient system from athena.1 and zora.4 (besides
  partitions-108.1b, zora.1, zora.2 and zora.3)

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

### Todo annotations

A todo state (`has-todo:` in the application model) takes three optional annotations, in any order,
after its requirement:

- `@label:` names the todo in the todo overview and the todo list. Without it, the todo is named
  after the path to its state in the model.
- `@description:` is shown with the todo.
- `@style:` colors the todo: a fixed style (`foreground`, `background`, `brand`, `link`, `accent`,
  `success`, `warning` or `error`), a color from a text property with `to-color`, or a `switch`
  that chooses one of those.

The todo overview is not tied to an entry, so the expressions of `@label:` and `@style:` start at the
root of the dataset:

```
root {
	'todo color': text
	'manual present': stategroup (
		'yes' { }
		'no' { }
	)
	'relations': collection ['relation'] {
		'relation': text
		'bank account': stategroup (
			'yes' {
				'iban': text
			}
			'no'
				has-todo:
					@label: "Relation without a bank account"
					@description: "Add the bank account of the relation"
					@style: switch .'manual present' (
						|'yes' => warning
						|'no'  => error
					)
			{ }
		)
		'checked': stategroup (
			'no'
				has-todo: user .'Type'?'Admin'
					@label: "Unchecked relation"
					@style: to-color .'todo color'
			{ }
			'yes' { }
		)
		'archived': stategroup (
			'no' { }
			'yes'
				has-todo: @description: "Archived relations are removed at the end of the year"
			{ }
		)
	}
}
```

The overview groups the todos on their collection or on their style, or lists them ungrouped. When
the todos have a style, the overview shows a filter for each style, with the amount of todos of that
style.
