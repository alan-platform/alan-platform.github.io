---
layout: "doc"
origin: "model"
language: "release notes"
version: "partitions-108.5"
type: "release notes"
---
## Model 109 (after 108)

### Changes

#### `application` language

- Support for partitions on numbers with a derived graph for the order of entries:
```js
'Orders': collection ['Order'] {
	'Order': text
	'Order Date': number 'date'
}
'Period Size': number positive 'days'
'Periods': collection ['Period']
	'Period Order': ordered-graph .'First' ( ?'Yes' || ?'No'>'Predecessor' ) = partition
	= partition .'Period Size' as 'Period Start' in 'Period Order' (
		'1' = .'Orders'* .'Order Date'
	) {
	'Period': text = key
	'Period Start': number 'date' = parameter
	'First': stategroup = parameter (
		'No' {
			'Predecessor': text -> ^ sibling in ( 'Period Order' ) = parameter
		}
		'Yes' { }
	)
	'Orders': reference-set -> ^ .'Orders'* = branch '1'
}
```

- Support for derived graphs:
```js
'Tasks': collection ['Task']
	'Dependencies': acyclic-graph
{
	'Task': text
	'Predecessor': stategroup (
		'None' { }
		'After' {
			'Task': text -> ^ sibling in ( 'Dependencies' )
		}
	)
}
'Milestones': collection ['Task']
	'Milestone Order': acyclic-graph = 'Dependencies'
{
	'Task': text -> ^ .'Tasks'[]
	'Predecessor': stategroup = on >'Task' as $'Step' in 'Dependencies' => switch $'Step'.'Predecessor' (
		|'None' => 'None' ( )
		|'After' as $ => switch sibling in ( 'Milestone Order' ) [ $ >'Task'] (
			| node as $ => 'After' ( 'Task' = $ )
			| none => recurse on $^ $'Step' = $ >'Task'
		)
	) (
		'None' { }
		'After' {
			'Task': text -> ^ sibling in ( 'Milestone Order' ) = parameter
		}
	)
}
```

- Readd support for unions that depend on a branch `reference-set` without collection steps:
```js
'Work Centers': collection ['Center'] {
	'Center': text
	'Shifts': collection ['Shift'] {
		'Shift': text
		'Time Slots': collection ['Slot'] {
			'Slot': text
		}
	}
}
'Work Center': text -> .'Work Centers'[]
'Assignments': collection ['Assignment'] {
	'Assignment': text
	'Shift': text -> ^ >'Work Center'.'Shifts'[]
	'Time Slot': text -> >'Shift'.'Time Slots'[]
	'Available Shifts': collection ['Shift'] = union (
		'1' = >'Shift'
	) {
		'Shift': text -> ^ ^ >'Work Center'.'Shifts'[] = key
		'1': reference-set -> ^ = branch '1' // NOTE: no collection steps, only a parent step
		'Available Slots': collection ['Slot'] = union (
			'1' = <'1'* >'Time Slot' // not supported in model 108
		) {
			'Slot': text -> ^ >'Shift'.'Time Slots'[] = key
		}
	}
}
```

- Containment switch for collections with key references:
```js
'Favorite Product Ordered': stategroup = switch .'Ordered Products'>[ >'Favorite Product' ] (
	| node => 'Yes' ( )
	| none => 'No' ( )
) ( ... )
```

- Containment `where` rules use `>[` and `]` around the key node path, in line with key reference lookup steps in navigation expressions. Previously the path was written between `[` and `]`:
```js
'Product': text -> ^ .'Products'[] as $
	where 'Ordered' -> ^ .'Ordered Products'>[ $ ]
```

- Aggregates take a parenthesized expression list, and `std` joins `min`, `max`, `sum` and `count`:
```js
// old
'Parts Cost': number 'euro' = sum .'Parts'* .'Part Price'
'# Products': number 'items' = count .'Products'*

// new
'Parts Cost': number 'euro' = sum ( .'Parts'* .'Part Price' )
'# Products': number 'items' = count ( .'Products'* )
```

- Sibling access is a navigation step `siblings`, so it can be taken within a path. An entry reference to a sibling ends in `[]`:
```js
// old
'Previous Year': text -> ^ sibling in ( 'Ordered Years' )
'Self or Sibling': text -> ^ sibling || self

// new
'Previous Year': text -> ^ siblings in 'Ordered Years' []
'Self or Sibling': text -> ^ siblings || self []
'Weeks': reference-set -> ^ siblings * .'Weeks'*
```

- One `switch` for node paths and sets. `| none`, `| node` and `| nodes` are each optional, and the set that `| nodes as $` binds can be iterated:
```js
'Open Orders': stategroup = switch .'Orders'* .'Status'?'Open' (
	| nodes as $ => 'Several' ( '# Orders' = count ( $ * ) )
	| node       => 'One' ( )
	| none       => 'None' ( )
) ( ... )
```

- Plural paths chain collection steps and reference set subsets, and reference set signatures are plural paths as well, so a signature may take a key reference lookup:
```js
'# Deliveries': number 'items' = count ( .'Orders'* .'Lines'* >'Product'.'Deliveries'* )
'Lines': reference-set -> downstream ^ ^ .'Orders'>[ ^ ] .'Lines'* = inverse >'Order'
```

- Reference set subsets take a complete plural path between `[` and `]`, with the `*` inside it. Only the head of that path may filter; the tail restates the levels of the reference set signature, including the state filters it declares:
```js
'# Members': number 'items' = count ( >'Region' <'Customers'[ >'Country' .'Cities'* .'Customers'* ] )
'# In Graph': number 'items' = count ( <'Slots'[ siblings in 'Slot Order' * ] )

// ERROR: a filter that the signature of 'Customers' does not declare
'# Active': number 'items' = count ( >'Region' <'Customers'[ >'Country' .'Cities'* .'Customers'* .'Status'?'Active' ] )
```
A level of a subset path may not be a reference set or a matched set, and a sibling or graph step is allowed
only where the signature has the same location. Below a level that the path pins, the filters of the signature
may be left out. A subset step produces every node once, also when several members of the set lead to it.

- The cardinality of a reference set subset is computed per level: pinning the parent level of a set that inverts a key reference yields at most one node, so a `switch` without `| nodes` is accepted:
```js
'Line found': stategroup = switch <'Lines'[ ^ >'Order'.'Lines'* ] ( // 'Line' is the key of 'Lines'
	| node => 'Yes' ( )
	| none => 'No' ( )
) ( ... )
```

- Union branches are plural paths. A branch merges its results one-to-one, or groups them with `as $ on`:
```js
'Debtors': collection ['Debtor'] = union (
	'' = .'Orders'* as $ on $ >'Debtor' // group: one entry per debtor
) { ... }

'Slots': collection ['Slot'] = union (
	'this' = <'Shifts'[ ^ .'Time Slots'* ] // merge: one entry per node the path produces
) { ... }
```

- A containment `where` rule whose lookup value is unique per entry re-roots the scope of the steps after it, like a key reference step does, so a branch path may continue over it:
```js
'Orders': collection ['Order'] {
	'Order': text -> ^ .'Order Numbers'[] as $
		where 'Invoice' -> ^ .'Invoices'>[ $ ] // unique lookup value: distinct orders reach distinct invoices
}
'Debtors': collection ['Debtor'] = union (
	'this' = .'Orders'* as $ on $ .'Order'&'Invoice'>'Debtor' // accepted
) { ... }
```
The lookup value decides, not whether the property holding the rule is the key of its collection. A lookup on a value that repeats, or into a collection that lives inside the entry itself, does not re-root the scope.

- State filters are part of the dependency chain of a path and are checked (see `design/ADR-003`). A reference that demands a state now forces every path that feeds it to take the same filter:
```js
'Key B': text -> ^ >'Ref A' .'Status'?'Open' ^ .'B'[] = key

'ok'  = .'Items'* as $ on $ >'Ref B'  // >'Ref B' takes the same filter
'bad' = .'Items'* as $ on $ >'Ref B2' // ERROR: the filter ?'Open' is missing
```
The reverse is allowed: a value path may filter where the reference does not.

- A `where` rule may supply the state filter that a reference target or a union key demands, and a `flatten` branch pops the filter together with the collection step it leaves:
```js
'Ref': text -> siblings [] as $
	where 'in S' -> $ .'Status'?'Open'
'Ref in S': text -> siblings [] .'Status'?'Open' = .'Ref'&'in S' // accepted

'Lines': collection ['Line'] = flatten (
	'open' = .'Orders'* .'Status'?'Open' as $ ( 'Debtor' = $ ^ ^ >'Debtor' )
) join - { ... }
```

- A derived graph takes its order from one graph that is predefined at or above the collection deriving it, the edge reference of a graph must be base data, and a node that a `partition` constructs takes no further constructor input:
```js
'Steps': collection ['Step']
	'Order': acyclic-graph = 'Deps' // ERROR when 'Deps' is defined on a nested collection

'Periods': collection ['Period'] = partition ... {
	'First': stategroup = parameter (
		'No' {
			'Predecessor': text -> ^ siblings in 'Period Order' [] = parameter // ERROR: the partition initializes the entry
		}
		'Yes' { }
	)
}
```

- `source-of` and `sink-of` take the first or last entry of one whole collection, so the path handed to them may not filter or iterate:
```js
'First Activity': text -> downstream ^ .'Activities'[] = sink-of ^ .'Activities'* in 'Order' // accepted

// ERROR: a state filter in the collection path
'First Open': text -> downstream ^ .'Activities'[] = sink-of ^ .'Activities'* .'Status'?'Open' in 'Order'

// ERROR: a reference set holds some entries, not a whole collection
'First Member': text -> downstream ^ .'Activities'[] = sink-of <'Members'* in 'Order'
```

- The cyclic dependency error at a derivation names the value the compiler resolves: `cyclic dependency detected for 'type'?>'value use of recursion'` replaces `cyclic dependency detected for 'type'?>'value computation phase'`. The meaning is unchanged: the derivation depends on itself without a recursion annotation.

- A todo item takes a `@style:`, like a state or a property does. The webclient lists todo items in a section of their own, away from the node that carries them, so the style expression starts at the **root** of the dataset and not at that node:
```js
'Mode': stategroup (
	'Normal' { }
	'Urgent' { }
)
'Theme color': text
'Orders': collection ['Number'] {
	'Number': text
	'Colour': text
	'Status': stategroup (
		'Open'
			has-todo: user
				@description: "Handle this order"
				@style: switch .'Mode' ( // accepted: 'Mode' is a property of the root
					|'Normal' => foreground
					|'Urgent' => error
				)
		{ }
		'Closed'
			has-todo: user @style: to-color .'Theme color' // accepted: 'Theme color' is a property of the root
		{ }
	)
}
'Deliveries': collection ['Number'] {
	'Number': text
	'Colour': text
	'Status': stategroup (
		'Open'
			has-todo: user
				@style: to-color .'Colour' // ERROR: 'property' `Colour` was not found in 'attributes'
		{ }
		'Closed' { }
	)
}
```

- A todo item takes a `@label:`, the text that names it in the list of todo items. Its expression starts at the **root** of the dataset, for the same reason the `@style:` expression does. The three annotations of a todo item may be written in any order:
```js
'Company': text
'Orders': collection ['Number'] {
	'Number': text
	'Status': stategroup (
		'Open'
			has-todo: user
				@label: concat ( "Open order of ", .'Company' ) // accepted: 'Company' is a property of the root
				@description: "Handle this order"
				@style: warning
		{ }
		'Closed' { }
	)
}
'Deliveries': collection ['Number'] {
	'Number': text
	'Status': stategroup (
		'Open'
			has-todo: user
				@label: .'Number' // ERROR: 'property' `Number` was not found in 'attributes'
		{ }
		'Closed' { }
	)
}
```

- A todo item is declared on a **state**, written after the state name and before the state's node body. No other kind of node carries one: to keep a todo that sat on a root, group or collection node, give that node a stategroup and declare the todo on the state that asks for the action. A derived collection takes a derived stategroup for this, because a derived entry holds no base data. The requirement expression still starts at the node of the state, so `^` counts from there as it did before:
```js
'Problemen': collection ['Probleem'] {
	'Probleem': text
	'Afgehandeld': stategroup (
		'Nee'
			has-todo: user @description: "Probleem: los dit op in de betreffende module."
		{ }
		'Ja' { }
	)
}
'Openstaande problemen': collection ['Probleem'] = .'Problemen'* .'Afgehandeld'?'Nee' {
	'Probleem': text -> ^ .'Problemen'[] .'Afgehandeld'?'Nee' = key
	'Gemeld': stategroup = 'Nee' ( ) (
		'Nee'
			has-todo: user @description: "Taak: meld dit probleem."
		{ }
		'Ja' { }
	)
}
```
A `has-todo:` inside a node body no longer parses. The upgrade transformations carry a todo that already sat on a state to its new place; a todo on any other node has no target to move to and is dropped, so remodel those before upgrading.
