---
layout: "doc"
origin: "connector"
language: "release notes"
version: "partitions-108.4.2"
type: "release notes"
---
## 40 (after 39)
Upgrade instructions:

Version 40 introduces no language changes at all beyond an updated model dependency.
It does include a breaking change to the `'network'` stdlib that needs to be manually resolved.
`./alan upgrade` runs the transformation from 39 (`upgrade/39`) on every connector system; it does not cover the `'network'` change.

In `'network'`, the type `'key value list'` is no longer an indexed collection as its usages have no concept of key uniqueness. This was a long standing bug.
To obtain a value by key from a `'key value list'`, either use the provided `'network'::'key value find'` — which returns a list of all values, possibly empty — or `'network'::'key value shared'` — which returns a single value if, and only if, there are 1..N entries with identical values.
