---
layout: "doc"
origin: "webclient"
language: "release notes"
version: "athena.3.1"
type: "release notes"
url: "/pages/docs/webclient/athena.3.1/release-notes.html"
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
