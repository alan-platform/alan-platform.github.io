---
layout: "doc"
origin: "model"
language: "release notes"
version: "109"
type: "release notes"
---
## Model 109

### Changes

#### `application` language

- Support for partitions on numbers with a derived graph for the order of entries. The period size (`.'Period Size'`), the number the entries are grouped on (`.'Order Date'`) and the number parameter share one numerical type. The partition sets the key, the number, the first-stategroup and the edge reference of a period; any other `= parameter` in the node, such as `'Label': text = parameter`, gives `no valid 'source' found for 'value source' option 'parameter'`, and a `where` rule on a state of the first-stategroup gives `no valid 'value source' found for 'behaviour'`:

```js
'Periods': collection ['Period']
	'Period Order': ordered-graph .'First' ( ?'Yes' || ?'No'>'Predecessor' ) = partition
	= partition .'Period Size' as 'Period Start' in 'Period Order' (
		'1' = .'Orders'* as $ on $ .'Order Date'
	) {
	'Period': text = key
	'Period Start': number 'days' = parameter
	'First': stategroup = parameter (
		'No' {
			'Predecessor': text -> ^ siblings in 'Period Order'[] = parameter
		}
		'Yes' { }
	)
	'Orders': reference-set -> ^ .'Orders'* = branch '1'
}
```

- Support for derived graphs. The key reference of the deriving collection reaches the collection that holds the source graph by parent steps and references, so that every entry of the derived collection refers into the same instance of that collection. A source collection inside the deriving entry itself gives `equality constraint violation for 'unique predefined source graph'`:

```js
'Tasks': collection ['Task']
	'Dependencies': acyclic-graph
{
	'Task': text
	'Predecessor': stategroup (
		'None' { }
		'After' {
			'Task': text -> ^ siblings in 'Dependencies'[]
		}
	)
}
'Milestones': collection ['Task']
	'Milestone Order': acyclic-graph = 'Dependencies'
{
	'Task': text -> ^ .'Tasks'[]
	'Predecessor': stategroup = on >'Task' as $'Step' in 'Dependencies' => switch $'Step'.'Predecessor' (
		|'None'  => 'None' ( )
		|'After' as $ => switch siblings in 'Milestone Order'>[ $ >'Task'] (
			| node  as $ => 'After' ( 'Task' = $ )
			| none  => recurse on $^ $'Step' = $ >'Task'
		)
	) (
		'None' { }
		'After' {
			'Task': text -> ^ siblings in 'Milestone Order'[] = parameter
		}
	)
}
```

- Support for unions that depend on a branch `reference-set` without collection steps. Model 108 rejected the inner union below. 'Shift' and 'Time Slot' are references on the entry that holds 'Available Shifts':

```js
'Available Shifts': collection ['Shift'] = union (
	'1' = as $ on $ >'Shift'
) {
	'Shift': text -> ^ ^ >'Work Center'.'Shifts'[] = key
	'1': reference-set -> ^ = branch '1' // no collection steps, only a parent step
	'Available Slots': collection ['Slot'] = union (
		'1' = <'1'* as $ on $ >'Time Slot' // rejected by model 108
	) {
		'Slot': text -> ^ >'Shift'.'Time Slots'[] = key
	}
}
```

- Containment switch for collections with key references. 'Ordered Products' is keyed by a reference to 'Products', 'Favorite Product' is a reference to 'Products':

```js
'Favorite Product Ordered': stategroup = switch .'Ordered Products'>[ >'Favorite Product'] (
	| node  => 'Yes' ( )
	| none  => 'No' ( )
) ( ... )
```

- A containment `where` rule writes the key node path between `>[` and `]`, like a key reference lookup step in a navigation expression. upgrade/108 converts this:

```js
// old
'Product': text -> ^ .'Products'[] as $
	where 'Ordered' -> ^ .'Ordered Products'[ $ ]

// new
'Product': text -> ^ .'Products'[] as $
	where 'Ordered' -> ^ .'Ordered Products'>[ $ ]
```

- Aggregates take their argument between parentheses: `count` takes one plural path, `sum`, `min`, `max` and `std` take an expression list. upgrade/108 converts this:

```js
// old
'Parts Cost': number 'euro' = sum .'Parts'* .'Part Price'
'# Products': number 'items' = count .'Products'*

// new
'Parts Cost': number 'euro' = sum ( .'Parts'* .'Part Price' )
'# Products': number 'items' = count ( .'Products'* )
```

- Sibling access is a navigation step `siblings`. An entry reference to a sibling ends in `[]`. The signature of a reference set and a subset path take the step followed by `*`, and the signature may continue below it. A value path, such as the argument of `count`, may not iterate `siblings`. upgrade/108 converts the three forms; in a subset path it takes the graph from the signature of the reference set. The first two lines below sit in a state of the year, the others on the year itself:

```js
// old
'Previous Year': text -> ^ sibling in ( 'Ordered Years' )
'Self or Sibling': text -> ^ sibling || self
'Other Year': text -> sibling
'Next Years': reference-set -> sibling in ( inverse 'Ordered Years' ) * .'First'?'No' = inverse >'Previous Year'
'Weeks of other years': reference-set -> sibling * .'Weeks'* = inverse >'Linked Year'
'Later Years': collection ['Year'] = union (
	'this' = <'Next Years'[ sibling * ]
) { ... }

// new
'Previous Year': text -> ^ siblings in 'Ordered Years'[]
'Self or Sibling': text -> ^ siblings || self []
'Other Year': text -> siblings []
'Next Years': reference-set -> siblings in inverse 'Ordered Years'* .'First'?'No' = inverse >'Previous Year'
'Weeks of other years': reference-set -> siblings * .'Weeks'* = inverse >'Linked Year'
'Later Years': collection ['Year'] = union (
	'this' = <'Next Years'[ siblings in inverse 'Ordered Years'* ]
) { ... }
```

- In derivations, one `switch` handles node paths and sets. Its path is a plural path. `| none` is required when the path can produce no node, and `| nodes` when it can produce several; `| node` may be left out when `| nodes` is present. A case that can never match is an error: `| none` on a path that always produces a node, such as a mandatory reference, and `| nodes` on a path that produces at most one node. The set that `| nodes as $` binds can be iterated. A `switch` in a command or action keeps both its cases:

```js
'Open Orders': stategroup = switch .'Orders'* .'Status'?'Open' (
	| nodes as $ => 'Several' ( '# Orders' = count ( $ * ) )
	| node  => 'One' ( )
	| none  => 'None' ( )
) ( ... )
```
Without `| nodes`, this switch reports `no valid 'upper bound cardinality for set' found for 'match nodes' option 'no'`; without `| none`, `no valid 'lower bound cardinality for set' found for 'match none' option 'no'`. The old `switch` on a node path in a derivation always had a `| none` case. upgrade/108 drops that case from an existence switch on a path that always produces a node. A `switch ... is ( ... )` keeps its `| none` case, which is valid there, and a switch on a set keeps every case it had:

```js
// old
'Price': number 'cents' = switch >'Product' (
	| none => 0
	| node as $ => $ .'Price'
)

// new
'Price': number 'cents' = switch >'Product' ( | node  as $ => $ .'Price' )
```

- Plural paths chain collection steps and reference set subsets, and reference set signatures are plural paths as well, so a signature may take a key reference lookup. 'Lines' below sits on a contact of a customer; 'Orders' is keyed by a reference to 'Customers':

```js
'Lines': reference-set -> downstream ^ ^ .'Orders'>[ ^ ] .'Lines'* = inverse >'Contact'
'# Deliveries': number 'items' = count ( .'Orders'* .'Lines'* >'Product'.'Deliveries'* )
```

- A reference set subset takes a complete plural path between `[` and `]`. Model 108 already placed the `*` inside the brackets, in a union branch over a reference set; model 109 accepts a complete plural path there, and the subset step in every plural path. The part of the path before its first `*` is the head: it selects one node, and the members of the set are matched against that node. The rest of the path walks the levels of the reference set signature again, down to the level of the nodes wanted. The head selects its node freely: it may reach the level by a reference or a lookup that the signature does not use. Below the head, the path takes only the levels that the signature walks: a reference set step or a set bound by `| nodes as $` is an error there, and a state filter is accepted only where the signature declares the same filter. The filters of the signature may be left out. A subset step produces every node once, also when several members of the set lead to it. A rejected path is fixed by hand. 'Customers' below has the signature `^ .'Countries'* .'Cities'* .'Customers'*`:

```js
'# Members': number 'items' = count ( >'Region'<'Customers'[ >'Country'.'Cities'* .'Customers'* ] )
// ERROR: equality constraint violation for 'subset of reference set': the signature of 'Customers' declares no filter on 'Status'
'# Active': number 'items' = count ( >'Region'<'Customers'[ >'Country'.'Cities'* .'Customers'* .'Status'?'Active'] )
// accepted: the filter follows the subset step
'# Active': number 'items' = count ( >'Region'<'Customers'[ >'Country'.'Cities'* .'Customers'* ] .'Status'?'Active' )
```
A `siblings` step after the head walks from the node that the head selects, while the signature walks its siblings from the entry itself; the two do not match, so this is an error. Without a head, a `siblings` step walks from the entry itself, like the signature. It is accepted where the signature walks the same siblings or the same graph, and also where the signature walks a graph and the path takes all siblings. A `siblings || self` step walks the whole collection and may follow a head. 'Taken over next year' below sits on a supplier of a year; 'Other Year' is `-> siblings []` on the year:

```js
'Taken over next year': reference-set -> ^ siblings in inverse 'Ordered Years'* .'Suppliers'* .'Taken Over'?'Yes' = inverse >'Supplier Last Year'
// the head `^ >'Other Year'` selects the year by a plain sibling reference: accepted
'# Taken over by other year': number 'items' = count ( <'Taken over next year'[ ^ >'Other Year'.'Suppliers'* ] )
// ERROR: equality constraint violation for 'subset of reference set': the graph step after the head walks from the other year
'# Taken over after other year': number 'items' = count (
	<'Taken over next year'[ ^ >'Other Year' siblings in inverse 'Ordered Years'* .'Suppliers'* ]
)
```

- The cardinality of a reference set subset is computed per level: a head that selects the parent level of a set that inverts a key reference yields at most one node, so a `switch` without `| nodes` is accepted. 'Line' is the key of 'Lines', 'Order' a reference to 'Orders':

```js
'Lines': reference-set -> ^ .'Orders'* .'Lines'* = inverse >'Line'
'Line found': stategroup = switch <'Lines'[ >'Order'.'Lines'* ] (
	| node  => 'Yes' ( )
	| none  => 'No' ( )
) ( ... )
```

- Union branches are plural paths. A branch merges its results one-to-one, or groups them with `as $ on`. upgrade/108 converts a branch that ended in a reference step into a grouping branch; a branch over a reference set is a merging branch and keeps its form:

```js
// old
'' = .'Orders'* >'Debtor'

// new
'' = .'Orders'* as $ on $ >'Debtor' // group: one entry per debtor
'this' = <'Shifts'[ >'Work Center'.'Shifts'* ] // merge: one entry per node the path produces
```

- A containment `where` rule finds one entry of a collection. In a plural path, a reference step after the rule is accepted only when distinct entries of the iterated collection find distinct entries: the lookup value is unique per entry (its key, or a reference that is its key), or the collection looked up lives inside the entry itself. A grouping path of a union branch may continue over the rule under the same condition. The rules below sit on an order; 'Invoices' and 'Contracts' are keyed by references to 'Order Numbers' and 'Suppliers' and hold a reference 'Debtor':

```js
'Order': text -> ^ .'Order Numbers'[] as $
	where 'Invoice' -> ^ .'Invoices'>[ $ ] // unique: 'Order' is the key
'Supplier': text -> ^ .'Suppliers'[] as $
	where 'Contract' -> ^ .'Contracts'>[ $ ] // repeats: two orders can find the same contract
	where 'Line' -> .'Lines'>[ $ ] // repeats, but every order looks up in its own lines
'# Invoice debtors': number 'items' = count ( .'Orders'* .'Order'&'Invoice'>'Debtor' ) // accepted
// ERROR: no valid 'reference navigation support' found for 'type' option 'dependency'
'# Contract debtors': number 'items' = count ( .'Orders'* .'Supplier'&'Contract'>'Debtor' )
'# Line debtors': number 'items' = count ( .'Orders'* .'Supplier'&'Line'>'Debtor' ) // accepted
```

- State filters are part of the path that a reference walks, and they are checked. A reference that demands a state forces every path that feeds it to take the same filter. A model that skipped the filter is fixed by hand. 'Address' and 'Any Address' below sit on a line of an order, 'Customer' on the order:

```js
'Address': text ~> ^ >'Customer'.'Status'?'Active' ^ .'Addresses'[] // takes the filter of the key below
'Any Address': text -> ^ >'Customer'.'Addresses'[] // skips it
'Delivery Addresses': collection ['Address'] = union (
	'ok' = .'Lines'* as $ on $ >'Address' // accepted
	'bad' = .'Lines'* as $ on $ >'Any Address' // ERROR: equality constraint violation for 'key reference dependency'
) {
	'Address': text -> ^ >'Customer'.'Status'?'Active' ^ .'Addresses'[] = key
}
```
The reverse is allowed: a value path may filter where the reference does not.

- A `where` rule may supply the state filter that a reference target or a union key demands, and a `flatten` branch pops the filter together with the collection step it leaves:

```js
'Ref': text -> siblings [] as $
	where 'in S' -> $ .'Status'?'Open'
'Ref in S': text -> siblings [] .'Status'?'Open' = .'Ref'&'in S' // accepted

'Lines': collection ['Line'] = flatten (
	'open' = .'Orders'* .'Status'?'Open' as $ ( 'Debtor' = $ ^ ^ >'Debtor' )
) join - {
	'Line': text = key
	'Debtor': text -> ^ .'Debtors'[] = parameter
}
```

- The parameters of a command or action are an entity of their own, so a parent step after a state step may not leave them, just as it may not leave a collection entry. A `where` rule that tests a parameter state and then steps out of the parameters fails with `equality constraint violation for 'context entity'`; the upgrade leaves it as it is. Fix it by hand: split the rule into a rule that tests the state and a rule that steps out of the parameters. The rule that steps out of the parameters has one `^` fewer than the old rule: the `^` right after the state step only left the state node. Where the rule selects collection candidates, take one as the source and add the other with `where`, which keeps the "and". A migration's source model holds the same rule and gets the same fix. 'Lines' below sits on the item that holds the command:

```js
'Bundle': command {
	'Selection': stategroup ( ... )
	'Picks': collection ['Line'] @default: candidates &'Open' where 'Selected' {
		'Line': text -> ^ ^ .'Lines'[]
			where 'Old' ~> ^ .'Selection'?'All' ^ ^ .'Lines'[] .'Done'?'No' // ERROR: equality constraint violation for 'context entity'
			where 'Selected' ~> ^ .'Selection'?'All' // accepted
			where 'Open' ~> ^ ^ .'Lines'[] .'Done'?'No' // accepted
	}
} => update .'Item' = "bundled"
```

- A base ordered graph takes a base ordering stategroup and a base edge reference; a derived ordered graph, written `= 'Order'` after its definition, takes derived ones. A base graph that names a derived reference as its edge is fixed by hand:

```js
'Order Copy': ordered-graph .'First' ( ?'Yes' || ?'No'>'Previous Copy' ) // ERROR: no valid 'value source' found for 'edge reference'
'Order Copy': ordered-graph .'First' ( ?'Yes' || ?'No'>'Previous Base' ) // accepted

'Previous Base': text -> ^ siblings in 'Order Copy'[]
'Previous Copy': text -> ^ siblings in 'Order Copy'[] = >'Previous Base'
```

- The key property of a derived collection requires `= key`. A `flatten` builds its key by joining the branch name and the keys of the entries the branch walks with the separator. Model 108 and partitions-108.1 accepted `= parameter` on the key property of a `flatten`, with an argument for the key in each branch initializer. That argument never set the key, so the keys stay the same. upgrade/108 and upgrade/partitions-108.1 write `= key` and remove the argument:

```js
// old
'Lines': collection ['Line'] = flatten (
	'Order' = .'Orders'* as $'o' (
		'Line' = $'o'.'Number'
		'Amount' = $'o'.'Amount'
	)
) join - {
	'Line': text = parameter
	'Amount': number 'euro' = parameter
}

// new
'Lines': collection ['Line'] = flatten (
	'Order' = .'Orders'* as $'o' ( 'Amount' = $'o'.'Amount' )
) join - {
	'Line': text = key
	'Amount': number 'euro' = parameter
}
```

- The cyclic dependency error at a derivation names the value the compiler resolves: `cyclic dependency detected for 'type'?>'value use of recursion'` replaces `cyclic dependency detected for 'type'?>'value computation phase'`. The meaning is unchanged: the compiler found a dependency cycle through the derivation that its recursion annotations do not cover.

- A todo item takes a `@label:`, the text that names it in the list of todo items, and a `@style:`, like a state or a property does. The webclient lists todo items in a section of their own, away from the node that carries them, so both expressions start at the **root** of the dataset and not at that node. The three annotations of a todo item may be written in any order. 'Number' below is the key of the orders that hold the stategroup:

```js
'Open'
	has-todo: user
		@label: concat ( "Open order of ", .'Company' ) // accepted: 'Company' is a property of the root
		@description: "Handle this order"
		@style: switch .'Mode' ( // accepted: 'Mode' is a stategroup of the root
			|'Normal' => foreground
			|'Urgent' => error
		)
{ }
'Closed'
	has-todo: user @label: .'Number' // ERROR: 'property' `Number` was not found in 'attributes'
{ }
```

- A todo item is declared on a **state**, written after the state name and before the state's node body. In model 108 it was written at the start of the node body of any node: a state, the root, a group, a collection entry or the parameters of a command or action. No other kind of node than a state carries one now: to keep a todo that sat on a root, group or collection node, give that node a stategroup and declare the todo on the state that asks for the action. A derived collection takes a derived stategroup for this, because a derived entry holds no base data. The requirement expression still starts at the node of the state, so `^` counts from there as it did before. upgrade/108 carries a todo that sat on a state to its new place:

```js
// old
'No' {
	has-todo: user @description: "Solve this problem in its module."
}

// new
'No'
	has-todo: user @description: "Solve this problem in its module."
{ }

'Open Problems': collection ['Problem'] = .'Problems'* .'Handled'?'No' {
	'Problem': text -> ^ .'Problems'[] .'Handled'?'No' = key
	'Reported': stategroup = 'No' ( ) (
		'No'
			has-todo: user @description: "Report this problem."
		{ }
		'Yes' { }
	)
}
```
A todo on a root, group or collection node is moved by upgrade/108 to the one state of a new derived stategroup `'Todo item'`, the node's last property, hidden from the views. Its requirement gets a leading `^` on every path that started at the node, because it now starts at the state's node:

```js
// old
'Problems': collection ['Problem'] {
	has-todo: user where ( .'Status'?'Open' ) @description: "Solve this problem in its module."
	'Problem': text
	'Status': stategroup ( ... )
}

// new
'Problems': collection ['Problem'] {
	'Problem': text
	'Status': stategroup ( ... )
	'Todo item': stategroup = 'Yes' ( ) @hidden (
		'Yes'
			has-todo: user where ( ^ .'Status'?'Open' ) @description: "Solve this problem in its module."
		{ }
	)
}
```
The requirement still controls when the todo applies. Replace the generated stategroup by one of your own when you want an explicit state, as 'Handled' above. A todo on the parameters of a command or action has no derived stategroup to carry it and is dropped. A node that already has a property `'Todo item'` cannot take the new one: rename that property before you upgrade.

### After the upgrade

`./alan upgrade` runs `upgrade/108` on every model 108 (platform before-partitions.1) and migration source model. The transformation converts what it can, and the build that follows reports what is left: that is the work by hand. These are the errors it reports for the changes above, each with its cause and the change that shows the fix.

Errors that converted code can report:

- `no valid 'lower bound cardinality for set' found for 'match none' option 'no'`: a `switch` in a derivation without `| none` on a path that can produce no node, such as a collection or a state filter. Add the case, as 'Open Orders' has it (see "In derivations, one `switch`").
- `no valid 'upper bound cardinality for set' found for 'match nodes' option 'no'`: a `switch` in a derivation without `| nodes` on a path that can produce several nodes, such as a branch reference set with several members per entry. Add the case, as 'Open Orders' has it (same change).
- `no valid 'lower bound cardinality for set' found for 'match none' option 'yes'`: a `| none` case on a path that always produces a node, such as a mandatory reference. The transformation drops it from an existence switch; it stays in a switch on a set and in code that was not converted. Remove the case, as the old and new 'Price' show (same change).
- `no valid 'upper bound cardinality for set' found for 'match nodes' option 'yes'`: a `| nodes` case on a path that produces at most one node, such as a subset whose head selects the parent of a set that inverts a key reference. Remove the case (see "The cardinality of a reference set subset is computed per level").
- `equality constraint violation for 'key reference dependency'`: a grouping path or a derived key skips a state filter that the reference it ends in demands. Take the reference that walks the same filter, as 'ok' does next to 'bad', or supply the filter with a `where` rule (see "State filters are part of the path that a reference walks" and "A `where` rule may supply the state filter").
- `equality constraint violation for 'subset of reference set'`: a subset path filters on a state that the signature of the reference set does not declare, iterates a reference set level, or selects a node in its head and then iterates a `siblings` or graph level. Move the filter out of the brackets, as the two '# Active' lines show, or select the level with a reference instead of iterating it (see "A reference set subset takes a complete plural path").
- `equality constraint violation for 'context entity'`: a parent step after a state step leaves the entity of that state, for example the parameters of a command or action. Split the rule, in the model and in each migration's source model (see "The parameters of a command or action are an entity of their own").
- `no valid 'value source' found for 'edge reference'`: a base ordered graph names a derived reference as its edge. Name the base reference, as the second 'Order Copy' does, or derive the graph (see "A base ordered graph takes a base ordering stategroup").

Errors in code that was not converted, such as a model upgraded by hand:

- ``unexpected keyword `sibling` while making a decision for stategroup 'has steps' of !'object path tail'``: the old sibling syntax. Write `siblings`, and end an entry reference with `[]` (see "Sibling access is a navigation step").
- ``expected keyword `(` but saw keyword `.` ``: an aggregate without parentheses, such as `count .'Products'*`. Write `count ( .'Products'* )` (see "Aggregates take their argument between parentheses").
- ``unexpected keyword `[` while making a decision for stategroup 'type' of !'where rules definition'.'rules'``: a containment rule written `[ $ ]`. Write `>[ $ ]` (see "A containment `where` rule writes the key node path").
- `no valid 'inverse reference step' found for 'type' option 'merge'. Unexpected 'dependency entity step'`: a union branch that ends in a reference step, such as `.'Orders'* >'Debtor'`. Write `.'Orders'* as $ on $ >'Debtor'` (see "Union branches are plural paths").
- ``unexpected keyword `has-todo:` while making a decision for !'permissions definition'``: a `has-todo:` inside a node body. Move it to the state, after the state name (see "A todo item is declared on a **state**").
- `no valid 'is simple member' found for 'value source' option 'parameter'`: the key property of a derived collection written `= parameter`. Write `= key`. For a `flatten`, remove its argument from each branch initializer (see "The key property of a derived collection requires `= key`").
