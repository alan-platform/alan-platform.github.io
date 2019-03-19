---
layout: page
title: Docs
category: main
permalink: /docs/
---

- An introduction: [Introducing Alan](/pages/tuts/introducing.html).
- A description of the [Alan stack from the bottom up](/pages/tuts/bottom-up.html).

## Languages

### How to read grammars

- Keywords are between `[]`, e.g. `'state group' [ '?' ] reference`.
- `component 'some component'` refers to a different component in the same language.

### Typical quirks of the Alan compiler

- Keywords should be separated by whitespace, so `()` doesn't work but `( )` does.
- Quotes are recognized as something special, so you *can* write `'type':` and `?'state group'|'state'`.
- Single quotes are used for entities (things you can refer to or that refer to something else), double quotes are just strings.
- Only tabs are accepted for indentation.

<a name="languages"></a>
### Important languages

{% include doc-index.html %}
