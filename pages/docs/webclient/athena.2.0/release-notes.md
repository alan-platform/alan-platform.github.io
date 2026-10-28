---
layout: "doc"
origin: "webclient"
language: "release notes"
version: "athena.2.0"
type: "release notes"
url: "/pages/docs/webclient/athena.2.0/release-notes.html"
---
## athena.2.0 (after athena.1.0)

Changes:
- The planning controls of zora.4: interaction modes (browse, select, create, move) with keyboard
  shortcuts, selecting blocks, resizing blocks, dropping a block on another item, child rows nested to
  any depth, and the time while creating, moving and resizing blocks
- `./alan upgrade` converts a webclient system from athena.1.0, zora.4.0 and zora.3.0

### Before the upgrade

Nothing.

### After the upgrade

- From athena.1.0 the syntax is unchanged.
- From zora.4.0 and zora.3.0 the upgrade converts the query headers in `views/*.alan`. The widget
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
