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

From athena.2 the syntax is unchanged. 
