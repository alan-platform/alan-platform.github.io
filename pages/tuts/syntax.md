---
layout: page
title: "Alan grammar syntax"
category: docs
---


# Syntax

## How to read grammars

### Keywords
- Literals between square brackets indicate required keywords, where a comma indicates if keywords go before or after a property. For example:
  - `'name' [ '#' ] text` implies a hashtag *before* a name-text: `#"Alice"`
  - `'name' [ '*' , '*' ] text` implies a star *before* and a star *after* a name-text: `* "Alice" *`
  - `'name' [ , '?' ] text` implies a question mark *after* a name-text: `"Alice"?`

### Properties
- `text` properties require a double quoted string: `"Alice"`
- `reference` properties require a single quoted string: `'reference to Bob'`
- `number` properties require a numerical value: `10`
- `stategroup` properties indicate a choice between different states, such as allowing or disallowing `anonymous` users
- `collection` properties require key-value pairs, where keys are single-quoted strings. For example, a `collection` of `properties` is written like this, depending on the required keywords and properties for the value:

> ```js
'First Name': text = "Alice"
'Last Name': text = "Ecila"
```

- `component` properties reference a rule in the grammar, to be instantiated at that point: `component 'abc'` references rule `'abc'`
- `group` properties just group properties that belong together

In the grammars, `indent` is an instruction for the deparser/pretty-printer; you can ignore it.
Furthermore, properties that are marked `implicit` exist for type checking purposes only.

## Typical quirks of the Alan compiler

- Keywords should be separated by whitespace, so `()` doesn't work but `( )` does.
- Quotes are recognized as something special, so you *can* write `'type':` and `?'state group'|'state'`.
- Only *tabs* are accepted for indentation.
