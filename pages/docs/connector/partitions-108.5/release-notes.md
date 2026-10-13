---
layout: "doc"
origin: "connector"
language: "release notes"
version: "partitions-108.5"
type: "release notes"
---
## 40 (after 39)
Upgrade instructions:

Version 40 introduces no language changes at all beyond an updated model dependency.
It does include a breaking change to the `'network'` stdlib that needs to be manually resolved.
`./alan upgrade` runs the transformation from 39 (`upgrade/39`) on every connector system; it does not cover the `'network'` change. The build reports each entry that a processor creates in a `'key value list'` and each lookup by key in one.

In `'network'`, the type `'key value list'` is no longer an indexed collection as its usages have no concept of key uniqueness. This was a long standing bug.
To obtain a value by key from a `'key value list'`, either use the provided `'network'::'key value find'` — which returns a list of all values, possibly empty — or `'network'::'key value shared'` — which returns a single value if, and only if, there are 1..N entries with identical values.

```js
// 39
'headers' = create [ "content-type" ] "application/json"
'content type' = $'response'.'headers'[ "content-type" ] || "application/octet-stream"

// 40
'headers' = create (
	'name' = "content-type"
	'value' = "application/json"
)
'content type' = call 'network'::'key value shared' (
	$'response'.'headers'
	$'key' = "content-type"
) || "application/octet-stream"
```
Neither function is a drop-in replacement for the 39 lookup `X[ "name" ]`, so choose per lookup:

| Name in the list | 39 `X[ "name" ]` | `'key value shared'` | `'key value find'` |
|---|---|---|---|
| absent | fails | fails | an empty list |
| once | its value | its value | a list with its value |
| more than once, all the same value | that value | that value | all of them |
| more than once, different values | one of them | fails | all of them |

All three compare the name with case folding. A response can carry a header more than once (`Set-Cookie`, for one); there `'key value shared'` with `|| <value>`, as in the example above, gives the fallback where the 39 lookup gave a value.
