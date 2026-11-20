---
layout: "doc"
origin: "webclient"
language: "release notes"
version: "athena.3.0"
type: "release notes"
url: "/pages/docs/webclient/athena.3.0/release-notes.html"
---
## athena.3.0 (after athena.2.3)

Changes:
- Queries on the entries of a single collection can follow the ordered graphs of that collection: the
  `ordered graph` query binding sorts on a graph order, and entries can be re-ordered in that order
- GUI actions: the view of an `update` on a node and of a `delete` entry is optional and written as
  `view: '<view>'`, so these actions can run inside operation parameters, where no view is available
- Planning: move the selected blocks together; the cursor shows what a press would do; end entry
  creation and fold all, and set query filters for children, at any depth
- Table: subtle text follows the contrasting color on colored rows and cells, and an invisible table
  still builds its rows
- Searchable select: sizes to its content and keeps the last label item when truncating
- Fix: the text input widget stretches while editing
- Fix: the default entries of a collection are kept when the default is applied again
- Fix: subscriptions that were reset are not visited again while reconnecting
- `./alan upgrade` converts a webclient system from athena.2.3 (besides athena.1.0, zora.4.0 and
  zora.3.1)

### Before the upgrade

Nothing.

### After the upgrade

From athena.2.3 the upgrade writes the view of `update` and `delete` GUI actions in the new form:

```
// old
update 'order view' ...
delete 'order view'

// new
update view: 'order view' ...
delete view: 'order view'
```

From athena.1.0 and older, also follow "After the upgrade" of athena.2.0 below.

## athena.2.0 (after athena.1.0)

Changes:
- The planning controls of zora.4: interaction modes (browse, select, create, move) with keyboard
  shortcuts, selecting blocks, resizing blocks, dropping a block on another item, child rows nested to
  any depth, and the time while creating, moving and resizing blocks
- `./alan upgrade` converts a webclient system from athena.1.0, zora.4.0 and zora.3.1

### Before the upgrade

Nothing.

### After the upgrade

- From athena.1.0 the syntax is unchanged.
- From zora.4.0 and zora.3.1 the upgrade converts the query headers in `views/*.alan`. The widget
  changes of athena.1.0 are not converted; change them as described in the release notes of
  athena.1.0, fixing what the build reports, topmost error first:
  - A `query` binding in a widget expression names its query without `candidates`. The build reports
    the old form with
    ``unexpected keyword `candidates` while making a decision for stategroup 'type' of !'widget expression tail'.'type'?'binding'``:

```
// old
'options candidates' = :: query candidates 'choose shift' (

// new
'options candidates' = :: query 'choose shift' (
```

  - Reading the `'todo'` stategroup of the client bindings requires a `'state'` binding. The build
    reports a read on the node with ``'state group' `todo` was not found in 'properties'``:

```
// old, inside a state binding
switch ^ $ [ /'node'.'todo'?'yes'.'active'?'yes'] (

// new
switch ^ $ [ .'todo'?'yes'.'active'?'yes'] (
```
