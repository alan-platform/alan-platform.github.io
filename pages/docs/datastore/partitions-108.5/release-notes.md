---
layout: "doc"
origin: "datastore"
language: "release notes"
version: "partitions-108.5"
type: "release notes"
---
## Datastore 120 (after 119.2)

- model 109 implementation

- provided interface implementation language: a state filter `?'s'` in a collection expression is part of the dependency chain of that collection, so a reference into the collection must reach the node through the same filter:
```
'C of A in s': collection = (
	'' = root .'R-A in s'&'in s' .'C'* as $ ( ) // chain: context >'R-A' ?'s' .'C'*
)

// old (accepted: the filter was dropped from the chain):
'ref-c-s': text -> .'C of A in s'[] = from '' [ root >'R-A' >'R-C' ]

// new (the expression takes the same filter):
'ref-c-s': text -> .'C of A in s'[] = from '' [ root .'R-A in s'&'in s' >'R-C' ]
```

- provided interface implementation language: a state rule (`.'sg'?'s'.&'rule'`) and a reference whose target path ends in a filter (`'R-A-s': text -> .'A'[] .'sg'?'s'`) contribute that same state step, so a reference expression may not route around them:
```
'D via R-A-s': collection = (
	'' = root >'R-A-s'.&'c'.'D'* as $ ( ) // chain: context >'R-A-s' ?'s' >'R-C' .'D'*
)

// old (accepted): an unfiltered reference to some 'A'
'ref-d': text -> .'D via R-A-s'[] = from '' [ root >'R-A'>'R-C'>'R-D' ]

// new:
'ref-d': text -> .'D via R-A-s'[] = from '' [ root >'R-A-s'.&'c'>'R-D' ]
```

- provided interface implementation language: a matrix collection applies the state filters of the collection it is keyed by:
```
'C of A in s': collection = (
	'' = root .'R-A in s'&'in s' .'C'* as $ ( )
)
'mat': collection -> .'C of A in s' = (
	'' = root >'R-A'.'C'* as $ ( )                // old
	'' = root .'R-A in s'&'in s' .'C'* as $ ( )   // new
)
```

- provided interface implementation language: the entries of a collection must be distinct nodes. This is now a rule on the branch expression as a whole instead of a rule on its last step, so the same implementations are rejected with a different message:
```
'c2': collection -> .'c1' = (
	'' = $ .'c2'* >'r1' as $ ( ) // two 'c2' entries may point at one 'c1'
)

// old: no valid 'unique result nodes' found for 'dependency' ( at >'r1' )
// new: no valid 'unique entries' found for 'expression' ( at the branch expression )
```
For a collection with a key constraint (`collection -> .'Source'`) the step that breaks the uniqueness is marked as well, so the error points at the navigation that has to change.

- provided interface implementation language: the check covers every branch expression, including entry lookups after a collection step. A lookup whose value is not the key of the entry the expression iterates is rejected:
```
/* application model: 'X': collection ['k'] { 'k': text  'r': text -> ^ .'C0'[]
**   'rb': text -> ^ .'C0'[] where 'C1 of r' -> ^ .'C1'>[ >'r' ] } */

'E after collection': collection = join - (
	// ERROR: 'r' is not the key of 'X', so two 'X' entries reach the same 'C1' and the 'E' entries repeat
	'' = root .'X'* .'rb'&'C1 of r' .'E'* as $ ( )
)
```

- provided interface implementation language: a containment rule or a node path lookup after a collection step is now accepted when it produces distinct entries. Previously every lookup after a collection step was rejected ("only reference steps are supported after a collection step"):
```
/* application model: 'Y': collection ['k'] { 'k': text -> ^ .'C0'[]
**   'rb': text -> ^ .'C0'[] where 'C1 of k' -> ^ .'C1'>[ >'k' ] } */

'E after collection by key': collection = join - (
	'' = root .'Y'* .'rb'&'C1 of k' .'E'* as $ ( ) // distinct 'Y' entries find distinct 'C1' entries
)
'D via key': collection = join - (
	'' = root .'Y'* >'k'.'D'[ root >'R-Z' ] as $ ( ) // each 'Y' entry looks up in its own 'D'
)
```

- provided interface implementation language: a graph step after a collection step is accepted. An ordered graph maps distinct entries onto distinct predecessors, so the result nodes stay distinct. Repeated steps in the same graph are fine; a plain sibling step and steps in two different graphs are rejected:
```
/* application model: 'A': collection ['k'] 'G': ordered-graph .'first' ( ?'yes' || ?'no'>'prev' ) */

'A via prev': collection -> .'A' = (
	'' = $'r'.'A'* .'first'?'no'>'prev' as $ ( )                       // accepted
)
'A via sib': collection -> .'A' = (
	'' = $'r'.'A'* >'sib' as $ ( )                                     // ERROR: two 'A' entries can have the same sibling
)
```

- provided interface implementation language: a `where` rule that only takes parent steps after a collection step is rejected under the name `context within child scope` (was `unique result nodes after parent steps`):
```
'' = $ .'c1a'* .'c1b'* .'kb'&'root' ( ) // ERROR: the rule climbs out of the last collection step
```

- provided interface implementation language: in a collection expression, a binding followed by more steps ends the line, so `as $'order'` followed by `.'Documents'` is no longer read as the variable step `$'order'.'Documents'`. When the chain splits, it starts on the line after the `=`. A chain that fits on one line and only binds at its end keeps its layout. A chain followed by `where` rules, or longer than 132 columns, also starts on the line after the `=`. The meaning of an implementation does not change and existing files still compile; `./alan upgrade` reformats every system, and by hand `.alan/devenv/platform/project-compiler/tools/pretty-printer .alan/devenv/system-types/datastore/language --allow-unresolved -C systems/<sys>` does.
```
// old
'Documents' = root .'Orders'* as $'order'.'Documents'* as $'document' (

// new
'Documents' =
	root .'Orders'* as $'order'
	.'Documents'* as $'document'
(
```
