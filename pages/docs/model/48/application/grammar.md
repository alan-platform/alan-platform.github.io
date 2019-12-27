---
layout: doc
origin: model
language: application
version: 48
type: grammar
---

1. TOC
{:toc}
## The *minimal model*
---
Every valid Alan model instantiates the [`root` rule](#the-root-rule).
We can use that rule for extracting a minimal model.
For the `application` language, the minimal model is

> ```js
users
interfaces
root { }
numerical-types
```

Thus, every `application` model defines `users` for access control, `interfaces` specifying operations and data from external systems, a `root` type, and `numerical-types`.
The next section explains the minimal model in more detail.
## Data model structure
---
### The `root` rule
##### Application users
The language supports two classes of users: `anonymous` users and `dynamic` users.
Anonymous users do not require login; dynamic users do.

The keyword `anonymous` enables `anonymous` user access to your application.
If you do not plan to support anonymous users, you just leave it out: the `'no'` state for `'allow anonymous user'` is the default, requiring no code at all.

User authentication can either be application-specific, or it can be done via a separate module for single sign-on.
If you want user authentication to be application-specific, you need to specify which text property holds (hashed) user passwords.
In addition, you have to specify states for the 'active' and 'reset' status of the password.

```js
'user' ['users'] component 'modifier'
```

```js
'allow anonymous user' stategroup (
	'no'
	'yes' [ 'anonymous' ]
)
```

```js
'has dynamic users' stategroup (
	'no'
	'yes'
		'context node path' [ 'dynamic' ':' ] component 'node content path'
		'users collection' [ '.' ] reference
		'has user authentication' stategroup (
			'yes'
				'password node' ['password' ':'] component 'node content path'
				'password property' [ '.' ] reference
				'password status' ['password-status' ':'] group (
					'state group' ['?'] reference
					'active state' ['active' ':']  group (
						'state' reference
						'initializer' component 'parametrized initialize node'
					)
					'reset state' ['reset' ':'] group (
						'state' reference
						'initializer' component 'parametrized initialize node'
					)
				)
			'no'
		)
		'has external authentication' stategroup (
			'yes'
				'authorities node' ['external' 'authentication' ':'] component 'node content path'
				'authorities collection' ['.'] reference
				'identities node' component 'node content path'
				'identities collection' ['.'] reference
				'user reference' [':'] reference
			'no'
		)
)
```
##### Interfaces
If your application consumes data from external sources, you will have defined an Alan `interface`.
In order to consume an `interface`, you mention it in a list of `interfaces`, so that you can reference the `interface` when configuring [permissions](#permissions-and-todos).
The `path` is a navigation path that produces a context node on which interface conformant data will be imported at runtime.
The `node type` specifying the context node, requires a permission definition to satisfy the modifier constraint: `can-update: interface '<imported interfaces id>'`.

```js
'imported interfaces' ['interfaces'] collection indent (
	'modifier' component 'modifier'
	'path' ['='] component 'group node selection' //'singular node path tail'
	'constraint: path result node has interface modifier' component 'EQ modifier'
)
```
##### The `root` node type
Alan models are hierarchical models specifying hierarchical data.
An Alan model is a hierarchy of nested types with a single root type:
> ```js
root { }
```

The `root` type (short for node type) is a complex type that nests other (complex) types. Types are surrounded by
curly braces, and their identification is a path which starts from the root type. We refer to
an instance of a type as a node. The rule for defining a type carries the same name: `node`; it should be read as the `node type` rule,
as we define `node types` in a model (for legacy reasons it is called the `'node'` rule).

{::comment}
##### Type checker annotations
The properties below are instantiated automatically as they do not require keywords. The type checker uses them for, well, type checking.

```js
'source base' group (
	'elementary' component 'value source base'
	'derived' component 'value source base'
)
```

```js
'source' group (
	'user'			component 'value source'
	'meta'			component 'value source'
	'inference'		component 'value source'
	'calculation'	component 'value source'
)
```

```js
'direction' group (
	'backward' component 'direction type'
	'forward' component 'direction type'
)
```

```js
'undefined output parameters' component 'output parameters'
```

```js
'undefined direction' component 'direction type'
```

```js
'undefined link' component 'link'
```

```js
'undefined reference' component 'reference'
```

```js
'unassigned variable' component 'variable'
```

```js
'undefined parameter' component 'parameter'
```

```js
'undefined member' component 'member'
```

```js
'integer' component 'integer'
```

```js
'natural' component 'natural'
```

```js
'type' component 'type'
```

```js
'dependable' component 'dependency'
```

```js
'entity' component 'entity'
```

```js
'root member' component 'member'
```
{:/comment}

```js
'root' [ 'root' ] component 'node'
```
##### Numerical types
Numbers in an application model require a numerical type. Also, computations with numbers of different numerical types require conversion rules.
Divisions require a division conversion rule, products require a product conversion rule, and so on. Some examples of numerical types, with conversion rules are
> ```js
'date' in 'days' @date
'date and time' in 'seconds' @date-time
'days'
'milliseconds'
    = 'seconds' * 1 * 10 ^ 3 // rule for converting 'seconds' to milliseconds
    @factor: 10^ 3
    @label: "sec"
'minutes' @duration: minutes
'seconds'
    = 'seconds' * 'factor' // 'seconds' times a 'factor' produces 'seconds'
    = 'seconds' / 'factor'
    = 'milliseconds' * 1 * 10 ^ -3
    = 'minutes' * 60 * 10 ^ 0
    @duration: seconds
'factor'
    = 'factor' * 'factor'
    = 'seconds' / 'seconds'
```

Annotations like `@date` map numerical types to formats for easy modification in the GUI.
With `@factor` you can present 1000 milliseconds as 1 second to the application user.<br>
If you do so, be sure to set `@label:` to `"sec"` as well!

```js
'numerical types' [ 'numerical-types' ] collection indent (
	'type' stategroup (
		'relative'
			'timer resolution' stategroup (
				'undefined'
				'seconds' [':' 'time-in-seconds']
			)
			'range type' ['in'] reference
		'absolute'
			'product conversions' collection indent ( ['=']
				'right' ['*'] reference
			)
			'division conversions' collection indent ( ['=']
				'denominator' ['/'] reference
			)
	)
	'singular conversions' collection indent ( ['=']
		'type' stategroup (
			'factor'
				'invert' stategroup (
					'no' ['*']
					'yes' ['/']
				)
				'factor' number
				'base' ['*'] number
				'exponent' ['^'] number
			'base'
				'offset' ['+'] number
				'base' ['*'] number
				'exponent' ['^'] number
				'unit conversion' stategroup (
					'no'
						'constraint' component 'numerical type constraint'
					'yes'
						'conversion rule' ['in'] reference
				)
		)
	)
	'ui' component 'ui numerical type'
)
```
### Node types
Node types contain a `permissions definition` for controlling read and update permissions,
 a `todo definition` to mark a node as a `todo`-item,
 and `attributes`.
An attribute is of type `property`, `reference-set`, or `command`.

##### Property attributes
A `property` specifies a part of the data structure.
Alan supports six different property types:
`text`, `file`, `number` (with subtypes `integer` and `natural`), `collection`, `stategroup`, and `group`.

*Text*, *file*, and *number* are primitive property types. Text properties hold an unbounded
string value. File properties hold two unbounded string values: a file token and a file extension.
Integer number properties hold an integer value, and natural number properties hold an integer
value greater than zero.
For ensuring that number values have a predefined accuracy, Alan does not support number values with a fractional component.
For expressing the accuracy of a number, number properties reference a [`numerical type`](#numerical-types).

> ```js
'Name'        : text
'Price'       : integer 'euro'
'Release Date': natural 'date and time'
```

A *collection* property holds a map of key-value pairs. Keys are text values that have
to be unique such that we can reference them unambiguously.
A key field has to be specified explicitly, after the keyword `collection`; values are nodes of an inline defined type that specifies the key field:

> ```js
Customers : collection ['Customer ID'] {
    'Customer ID': text
    ... /* other attributes of this type */ ...
}
```

A *state group* property holds a value indicating a state. States are the alternatives to an aspect
that a state group property indicates. For example, `red`, `orange`, or `green` for a `color` property of a traffic light. The type of the property value corresponds to one out of multiple
predefined state types, such as `simple` or `assembled`:
> ```js
'Product Type': stategroup (
    'Simple' -> { ... /* attributes of this type */ ... }
    'Assembled' -> { ... /* attributes of this type */ ... }
)
```

A *group* property groups related property values, which is useful for presentational purposes:
> ```js
'Address': group {
    'City': text
    'State': text
    'Zip Code': text
}
```

___Derived values.___ Properties of the different types hold either *elementary* values or *derived* values (derivations).
*Derived* values are computed from elementary values and other derived values.
Application users cannot modify derived values.
Properties holding *derived* values require an expression for computing their values at runtime:
> ```js
'City': text                    // elementary value property
'copy of City':= text = .'City' // derived value property with expression
```

The [derivations](#derivations) section provides the grammar for derivation expressions,
detailing the different computations that the language supports.

___Presentation options.___ The `ui` component properties reference [GUI annotation rules](#gui-annotations) for tweaking and tuning the behaviour and presentation of properties in the generated GUI.
Some examples of GUI annotations are
- `@hidden`: hides a derived property from the UI.
- `@description: "a description"`: describes the property in more detail to the user.
  Useful in combination with validation rules!
- `@validate: "[a-b]+"`: sets a regex for text properties that defines what values are acceptable.
- `@min:` and `@max:`: limits number values.
- `@identifying`: marks a property to always be displayed in addition to an collection entry's key.
- `@default: 'Assembled'`: specifies a default state for a state group property.
- `@default: today|now`: sets date or date-time number value to the current time.
- `@default: guid`: initializes a text property with a generated unique id string.
- `@small`: displays (small) collections inline, and includes them when pressing 'Duplicate'.
- `@multi-line`: presents a multi-line text area for a text property.

##### Reference set attributes
A `reference-set` is a special property that holds a set of inverse references created by reference [constraints](#constraints).
Derivation expressions use them for computations (e.g. [derived numbers](#derived-numbers)).

##### Command attributes
A `command` is a complex parametrized atomic operation on the dataset; a `command` is executed in a single transaction.
A `command` attribute on a `node type` consists of a `parameter definition` and an [implementation](#commands-and-timers).

```js
'node' [ '{' , '}' ]
	'permissions definition' component 'node permissions definition'
	'todo definition' component 'todo definition'
	'has attributes' stategroup has 'attributes' first 'first' 'yes' 'no'
	'attributes' collection (
		'preceding siblings' collection predecessors
		'type' stategroup (
			'referencer anchor'[':' 'reference-set']
				'node type path' ['->'] component 'node path'
				'EQ node type' component 'EQ node type'
				'text' ['=>' 'inverse' '>' ] reference
				'referencer is bidirectional' stategroup ( 'is bidirectional' )
			'log' [ ':' 'log' ] // NOT SUPPORTED!
				'root' component 'log node'
			'command' [ ':' 'command' ]
				'type' stategroup (
					'global'
						'ui' component 'ui command attribute'
					'component' [ 'component' ]
				)
				'parameters root entity' component 'entity'
				'parameters' component 'parameter definition'
				'implementation' stategroup (
					'external' [ 'external' ]
					'internal'
						'implementation' component 'command implementation'
				)
			'property'
				'data type' stategroup (
					'elementary' [ ':' ]
					'derived' [ ':=' ]
				)
				'type' stategroup (
					'group' [ 'group' ]
						'type' stategroup (
							'elementary'
							'derived' ['=']
						)
						'ui' component 'ui group property'
						'node' component 'node'
					'collection' [ 'collection' ]
						'key property' ['[',']'] reference
						'type' stategroup (
							'elementary'
								'graph constraints' component 'graph constraints definition'
							'derived'
								'key constraint' stategroup (
									'no' [ '=' 'flatten' ]
										'branches' ['(', ')'] collection (
											'expression' [ '=' ] component 'flatten expression'
										)
										'separator' ['join'] stategroup (
											'dot' ['.']
											'dash' ['-']
											'colon' [':']
											'greater than' ['>']
											'space' ['space']
										)
									'yes' [ '=' ]
										'expression' component 'plural reference expression'
								)
						)
						'entity' component 'entity'
						'permissions' component 'item permissions definition'
						'ui' component 'ui collection property'
						'node' component 'node'
					'number'
						'type' stategroup (
							'elementary'
								'set' stategroup (
									'integer' [ 'integer' ]
									'natural' [ 'natural' ]
								)
								'numerical type' reference
								'type' stategroup (
									'causal'
										'type' stategroup (
											'mutation' [ '=' 'mutation-time' ]
												'watched property' stategroup (
													'number' [ '#' ]
														'number' reference
													'text' [ '.' ]
														'text' reference
												)
											'creation' [ '=' 'creation-time' ]
											'destruction'
												'destruction operation' stategroup (
													'set to lifetime' [ '=' 'life-time' ]
													'add lifetime' [ 'add' 'life-time' ]
													'subtract lifetime' [ 'subtract' 'life-time' ]
												)
												'watched stategroup' ['?'] reference
												'watched state' ['|'] reference
										)
									'simple'
										'record mutation time' stategroup (
											'yes' ['mutation-time']
												'meta property' ['=' '#'] reference
											'no'
										)
								)
							'derived'
								'type' stategroup (
									'integer' [ 'integer' ]
										'numerical type' reference
										'conversion' [ '=' ] stategroup (
											'none'
											'singular'
												'conversion rule' ['from'] reference
										)
										'expression' component 'integer expression'
									'natural' [ 'natural' ]
										'numerical type' reference
										'conversion' [ '=' ] stategroup (
											'none'
											'singular'
												'conversion rule' ['from'] reference
										)
										'expression' component 'natural expression'
								)
						)
						'behaviour' stategroup (
							'none'
							'timer' [ 'timer' 'ontimeout']
								'implementation' component 'command implementation'
						)
						'ui' component 'ui number property'
					'file' ['file']
						'type' stategroup (
							'elementary'
							'derived' [ '=' ]
								'type' stategroup (
									'singular'
										'type' stategroup (
											'property'
												'context selection' component 'ancestor property path'
												'file' [ '/' ] reference
											'node'
												'selection' component 'calculated node selection starting from property'
												'file' [ '/' ] reference
										)
									'conditional' ['switch']
										'state group selection' ['(',')'] component 'calculated state group selection starting from property'
										'states' [ '(' , ')' ] collection ( ['|']
											'expression' [ '=' ] component 'conditional file expression'
										)
								)
						)
						'ui' component 'ui file property'
					'text' ['text']
						'type' stategroup (
							'elementary'
								'has constraint' stategroup (
									'no'
									'yes' ['->']
										'expression' component 'reference constraint expression'
										'output parameters' component 'output parameters definition'
										'referencer' component 'referencer'
								)
								'record mutation time' stategroup (
									'yes' ['mutation-time']
										'meta property' ['=' '#'] reference
									'no'
								)
							'derived'
								'has constraint' stategroup (
									'no' ['=']
										'value source' stategroup (
											'key' ['$']
												'is collection key' component 'EQ member'
											'expression'
												'not collection key' component 'EQ member'
												'expression' component 'text expression'
										)
									'yes' ['=>']
										'expression' component 'derived reference constraint expression'
										'output parameters' component 'output parameters definition'
										'value provision' ['='] stategroup (
											'key' ['$']
												'is collection key' component 'EQ member'
											'expression'
												'not collection key' component 'EQ member'
												'expression' component 'singular reference expression'
										)
										'referencer' component 'referencer'
								)
						)
						'value type' stategroup (
							'link' [ '~>' ]
								'selection' component 'link text expression'
								'linker' component 'linker'
							'simple'
						)
						'ui' component 'ui text property'
					'state group' [ 'stategroup' ]
						'type' stategroup (
							'elementary'
							'derived' ['=']
								'expression' component 'state expression'
						)
						'ui' component 'ui state group property'
						'output parameters' collection ( [ '(' , ')' ]
							'dependable' component 'dependency'
							'type' stategroup (
								'elementary' [ '->' ]
								'derived' [ '=>' ]
							)
							'node selection' component 'node path'
						)
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' [ '(' , ')' ] collection order 'view order' indent (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'record lifetime' stategroup (
								'yes' ['life-time']
									'meta property' ['=' '#'] reference
									'creation timestamp' ['from'] reference
								'no'
								)
							'input parameters' collection ( [ '(' , ')' ]
								'type' stategroup (
									'node'
										'type' stategroup (
											'elementary' ['->']
												'selection' component 'resolved state group selection starting from property'
												'state' [ '|' ] reference
												'tail' component 'node content path'
											'derived' [':']
												'node selection' component 'node path'
										)
									'number'
										'set' [':'] stategroup (
											'integer' ['integer']
											'natural' ['natural']
										)
										'numerical type' reference
								)
							)
							'output arguments' [ '->' ] collection ( [ '(' , ')' ]
								'type' stategroup (
									'elementary' [ '->' ]
										'type' stategroup (
											'descendant'
												'type' stategroup (
													'input parameter' ['&']
														'input parameter' reference
													'this'
												)
												'selection' component 'resolved node descendant selection starting from node'
											'ancestor' [ '^' ]
												'selection' component 'resolved node selection starting from property'
										)
									'derived' [ '=>' ]
										'type' stategroup (
											'descendant'
												'type' stategroup (
													'input parameter' ['&']
														'input parameter' reference
													'this'
												)
												'selection' component 'calculated descendant node selection starting from node'
											'ancestor' [ '^' ]
												'selection' component 'calculated node selection starting from property'
										)
								)
							)
							'permissions' component 'item permissions definition'
							'ui' component 'ui state'
							'node' component 'node'
						)
				)
		)
		'attribute' component 'member'
	)
```
## Constraints
---
The `application` language supports two types of constraints on data: *reference constraints* and *graph constraints*.

___Reference constraints___ ensure that text properties hold a key value that uniquely identifies an item in a single specific `collection`.
This ensures that derived value computations and command invocations can safely use references.
In the GUI, reference constraints translate to a select list from which the application user has to choose an item.

Reference constraint expressions exist in two different flavours:
(1) `backward` reference expressions that use earlier defined attributes and (2)
`forward` reference expressions that freely use earlier and later defined attributes.
We recommend limiting the use of `forward` references, as their use in computations is restricted for ensuring terminating computations.

References can be unidirectional or bidirectional. For bidirectional references, you specify a reference-set:
> ```js
'Products': collection ['Name']
    'assembly': acyclic-graph
{
    'Name': text
      // reference-set holding Orders added by Product references:
    'Orders': reference-set -> .'Orders' => inverse >'Product'
}
'Orders': collection ['ID'] {
    'ID': text
      // a (bidirectional) backward reference:
    'Product': text -> ^ .'Products' -<'Orders'
}
```

The expression `^ .'Products'` is a navigation expression that produces exactly one collection at runtime.
The Alan runtime interpretes such [navigation expressions](#navigation) as follows:
starting from the `Orders` node, go to the parent node (as expressed by the navigation step `^`);
then select the `Products` collection found on that node.
Thus, at runtime, navigation expressions are executed relative to the context node for which the expression should be evaluated.

___Graph constraints___ ensure termination for recursive computations traversing a graph.
Graph constraints constrain that a set of references (edges) together form a graph satisfying a specific property.
For example, an `acyclic-graph` constraint ensures that references that partake in the graph, form a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph).
For a detailed explanation, see [AlanLight](http://resolver.tudelft.nl/uuid:3eedbb63-29ea-4671-a016-4c037eec94cd).

The code sample below presents a graph constraint `assembly`.
`Product` references of `Parts` partake in the acyclic `assembly` graph.
The constraint ensures that `Product Price` computations terminate:
> ```js
'Products': collection ['Name']
    'assembly': acyclic-graph
{
    'Name': text
    'Parts': collection ['Product'] {
         // a 'forward' (self) reference that partakes in a graph constraint:
        'Product': text -> forward ^ ^ .'Products' / ^ 'assembly'
        'Part Price': integer 'euro' = >'Product'#'Product Price'
    }
    'Product Price': integer 'euro' = sum .'Parts'#'Part Price' // recursion!
}
```

```js
'reference constraint expression'
	'type' stategroup (
		'backward'
			'selection' component 'resolved collection selection starting from property'
		'forward' [ 'forward' ]
			'head' component 'unresolved node selection'
			'collection' ['.'] reference
			'constrain' stategroup (
				'no'
				'yes' ['/']
					'ancestor' component 'ancestor node path'
					'collection constraint' reference // reference to a 'graph constraint'
			)
	)
	'tail' component 'node content path'
	'EQ modifier' component 'EQ modifier'
	'bidirectional' stategroup (
		'no'
		'yes' [ '-<' ]
			'anchor' reference
	)
```

```js
'derived reference constraint expression'
	'type' stategroup (
		'backward'
			'selection' component 'calculated collection selection starting from property'
		'self'
			'selection' component 'ancestor node path'
			'collection' [ '.self' ] stategroup ( 'collection' )
	)
	'tail' component 'derivation node content path'
```

```js
'graph constraints definition'
	'constraints' collection (
		'type' [':'] stategroup (
			'acyclic' [ 'acyclic-graph' ]
			'linear' [ 'ordered-graph' ]
		)
	)
```
## Links
---
Links mark relations between nodes that are not, or cannot be enforced by the runtime.
Similar to constraints, they also feature select lists in the generated GUI.

Links are especially useful when importing data from external systems via an Alan `interface`.
An Alan `application` requires that imports via an Alan `interface` always succeed.
Therefore, `application` data cannot put constraints on imported data; that is, unless the `interface` specifies them.
To exemplify this, suppose that order management application imports `Products` from a `Catalog Provider`.
As `Catalog Provider` can remove `Products` at any given time, we cannot put constraints on them.
`Orders` have to *link* to `Products` instead:
> ```js
'Catalog': group { can-update: interface 'Catalog Provider'
    'Products': collection ['Name'] {
        'Name': text
    }
}
'Orders': collection ['ID'] {
    'ID': text
     // a link to a 'Products' item from the catalog provider:
    'Product': text ~> ^ +'Catalog' .'Products'
}
```

```js
'link text expression'
	'dependency' stategroup (
		'link'
			'context selection' component 'ancestor property path'
			'text' [ '.' ] reference //TODO: should be > (ambiguous right now)
			'group selection' component 'group node selection'
			'collection' ['.'] reference
		'node'
			'collection selection' component 'calculated collection selection starting from property'
	)
	'tail' component 'derivation node content path'
```

```js
'link text expression context path'
	'has steps' stategroup (
		'no' [ '$' ]
		'yes' [ '$^' ]
			'tail' component 'link text expression context path'
	)
```
## Derivations
---
Derivation expressions use earlier defined properties for deriving values for ensuring terminating computations of derived values (derivations).
After a navigation step for following a reference, derivation expressions can use later defined properties as well.
Please note that some work remains to be done on the `application` language to fully ensure safe computations.
For more details on this, see [AlanLight](http://resolver.tudelft.nl/uuid:3eedbb63-29ea-4671-a016-4c037eec94cd).

### Derived texts without constraint
A derived text property holds a (sequence of) static text values and text values from other properties:

> ```js
'Address': group {
    'Street'       : text // e.g. "Huntington Rd"
    'Street number': text // e.g. "12B"
}
 // label for an external billing system:
'Address label':= text
    = +'Address'.'Street' " " +'Address'.'Street number' // "Huntington Rd 12B"
```

```js
'text expression'
	'type' stategroup (
		'singular'
			'selection' component 'text selection starting from property'
		'conditional' ['switch' ]
			'state group selection' ['(', ')'] component 'calculated state group selection starting from property'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional text expression'
			)
	)
	'has successor' stategroup (
		'no'
		'yes'
			'tail' component 'text expression'
	)
```

```js
'text selection starting from property'
	'type' stategroup (
		'value'
			'value' text
		'text'
			'type' stategroup (
				'text'
					'context selection' component 'ancestor property path'
					'text' [ '.' ] reference
				'node'
					'selection' component 'calculated node selection starting from property'
					'text' [ '.' ] reference
			)
	)
```

```js
'conditional text expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional text expression context path'
	)
```

```js
'conditional text expression'
	'has steps' stategroup (
		'no'
			'type' stategroup (
				'value'
					'value' text
				'text'
					'expression context' component 'conditional text expression context path'
					'context' stategroup (
						'target context' [ '$^' ]
							'selection' component 'text selection starting from property'
						'expression result' [ '$' ]
							'context type' stategroup (
								'input parameter'
									'input parameter' [ '&' ] reference
								'this state'
							)
							'selection' component 'calculated descendant node selection starting from node'
							'text' [ '.' ] reference
					)
			)
		'yes' ['switch' '(']
			'expression context' component 'conditional text expression context path'
			'type' stategroup (
				'merge' [ '$^' ]
					'state group selection' component 'calculated state group selection starting from property'
				'flatten' ['$']
					'context type' stategroup (
						'input parameter'
							'input parameter' [ '&' ] reference
						'this state'
					)
					'selection' component 'calculated descendant node selection starting from node'
					'state group' [ '?' ] reference
			)
			'KEYWORD' [')'] component 'KEYWORD'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional text expression'
			)
	)
```
### Derived texts with constraint (derived references)
The `application` language supports two types of derived references: `singular` and `branch`.
The `singular` type creates a direct relation between nodes using other relations.
The `branch` type is required for creating derived references to items in derived collections merge nodes of different types (see [node type rule](#node-types)).
The example below shows a property ` for deriving a (`singular`) direct reference from an `Orders` item to a `Manufacturers` item.
The expression for the `Manufacturer` reference an `Orders` item requires specifying an [`output parameter`](#output-parameters-legacy)
after the constraint expression for the `Product` property.

> ```js
'Manufacturers': collection ['Name'] { 'Name': text }
'Products': collection ['Name'] {
    'Name': text
    'Manufacturer': text -> ^ .'Manufacturers'
}
'Orders': collection ['ID'] {
    'ID': text
    'Product': text -> ^ .'Products' ( 'Manufacturer' => >'Manufacturer' )
    'Manufacturer':= text => ^ .'Manufacturers' = >'Product'$'Manufacturer'
}
```

```js
'singular reference expression'
	'type' stategroup (
		'branch' // branch of derived collection constructed using flatten expressions
			'branch' [ 'from' ] reference
			'root entity constraint' stategroup ( 'root' )
			'expression' [ '[', ']' ] component 'calculated node selection starting from property'
		'singular'
			'expression' component 'calculated node selection starting from property'
	)
```
### Derived files
An example of a derived file property `Contract`.
The property holds the value of a `Default Contract` in case of a `Standard` `Agreement`, and a `Custom` `Contract` in case of a `Custom` `Agreement`:
> ```js
'Default Contract': file
'Agreement': stategroup (
    'Standard' -> { }
    'Custom' -> {
        'Contract': file
    }
)
'Contract':= file = switch ( ?'Agreement' ) (
    |'Default' = $^ /'Default Contract'
    |'Custom' = $ /'Contract'
)
```

```js
'conditional file expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional file expression context path'
	)
```

```js
'conditional file expression'
	'has steps' stategroup (
		'no'
			'expression context' component 'conditional file expression context path'
			'context' stategroup (
				'target context' [ '$^' ]
					'type' stategroup (
						'property'
							'context selection' component 'ancestor property path'
							'file' [ '/' ] reference
						'node'
							'selection' component 'calculated node selection starting from property'
							'file' [ '/' ] reference
					)
				'expression result' [ '$' ]
					'context type' stategroup (
						'input parameter'
							'input parameter' [ '&' ] reference
						'this state'
					)
					'selection' component 'calculated descendant node selection starting from node'
					'file' [ '/' ] reference
			)
		'yes' ['switch' '(']
			'expression context' component 'conditional file expression context path'
			'type' stategroup (
				'merge' [ '$^' ]
					'state group selection' component 'calculated state group selection starting from property'
				'flatten' ['$']
					'context type' stategroup (
						'input parameter'
							'input parameter' [ '&' ] reference
						'this state'
					)
					'selection' component 'calculated descendant node selection starting from node'
					'state group' [ '?' ] reference
			)
			'KEYWORD' [')'] component 'KEYWORD'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional file expression'
			)
	)
```
### Derived numbers
Examples of derived number properties, including required conversion rules:

> ```js
root {
    'Tax Percentage': natural 'percent'
    'Products': collection ['Name'] {
        'Name': text
        'Price': integer 'eurocent'
        'Price (euro)':= integer 'euro' = from 'eurocent' #'Price'
        'Order Unit Quantity': natural 'items per unit'
        'Orders': reference-set -> .'Orders' => inverse >'Product'
        'Sales Value':= integer 'eurocent' = sum <'Orders'#'Price'
        'Items Sold':= integer 'items' = count <'Orders'
    }
    'Total Sales Value':= integer 'eurocent' = sum .'Products'#'Sales Value'
    'Number of Products':= integer 'items' = count .'Products'
    'Orders': collection ['ID'] {
        'ID': text
        'Product': text -> ^ .'Products' -<'Orders'
        'Quantity': natural 'items'
        'Loss':= integer 'items' = remainder ( #'Quantity' as 'items', >'Product' #'Order Unit Quantity' )
        'Price':= integer 'eurocent' = product ( >'Product'#'Price' as 'eurocent' , #'Quantity' )
        'Order Units':= natural 'units' = division ceil ( #'Quantity' as 'items' , >'Product'#'Order Unit Quantity' )
        'Tax': integer 'eurocent'
        'Gross Price':= integer 'eurocent' = sumlist ( #'Price', #'Tax' )
        'Creation Time': integer 'date and time'
        'Estimated Lead Time': integer 'seconds'
        'Estimated Delivery Time':= integer 'date and time' = add ( #'Creation Time', #'Estimated Lead Time' )
        'Delivered': stategroup (
            'No' -> { }
            'Yes' -> {
                'Delivery Time': natural 'date and time'
                'Lead Time':= integer 'seconds' = diff ( #'Delivery Time', ^ # 'Creation Time' )
            }
        )
    }
    'Gross Income':= integer 'eurocent' = sum .'Orders'#'Gross Price'
}
numerical-types
    'percent'
    'euro'
        = 'eurocent' * 1 * 10 ^ -2
    'eurocent'
        = 'eurocent' * 'items'
    'items per unit'
    'units'
        = 'items' / 'items per unit'
    'items'
        = 'items' / 'items per unit' // required by 'remainder'; to be fixed
    'date and time' in 'seconds'
    'seconds'
```


```js
'integer expression'
	'type' stategroup (
		'singular'
			'type' stategroup (
				'value' [ 'deprecated' ]
					'value' number
				'expression'
					'expression' component 'calculated signed number selection starting from property'
			)
		'conditional' ['switch']
			'state group selection' ['(',')'] component 'calculated state group selection starting from property'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional number expression'
			)
		'referencer anchor sum' [ 'sum' ]
			'context selection' component 'entity scoped ancestor property path'
			'referencer anchor' [ '<' ] reference
			'filter' component 'derivation node content path'
			'number context selection' component 'entity scoped ancestor node path'
			'number' [ '#' ] reference
			'conversion' component 'numerical type conversion'
		'referencer anchor count' [ 'count' ]
			'context selection' component 'entity scoped ancestor property path'
			'referencer anchor' [ '<' ] reference
			'filter' component 'derivation node content path'
		'sum' [ 'sum' ]
			'collection selection' component 'calculated collection selection starting from property'
			'filter' component 'derivation node content path'
			'property' [ '#' ] reference
			'conversion' component 'numerical type conversion'
		'count' [ 'count' ]
			'collection selection' component 'calculated collection selection starting from property'
			'filter' component 'derivation node content path'
		'remainder' [ 'remainder' ] // NOT SUPPORTED BY TYPE CHECKER
			'numerator' [ '(' ] component 'calculated signed number selection starting from property'
			'conversion rule' ['as'] reference
			'numerator conversion' component 'numerical type conversion'
			'denominator set' [ ',' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'denominator' component 'calculated signed number selection starting from property'
			'denominator conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'division' [ 'division' ]
			'rounding' stategroup (
				'ordinary'
				'ceil' [ 'ceil' ]
				'floor' [ 'floor' ]
			)
			'numerator' [ '(' ] component 'calculated signed number selection starting from property'
			'conversion rule' ['as'] reference
			'numerator conversion' component 'numerical type conversion'
			'denominator set' [ ',' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'denominator' component 'calculated signed number selection starting from property'
			'denominator conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'product' [ 'product' ]
			'left' [ '(' ] component 'calculated signed number selection starting from property'
			'conversion rule' ['as'] reference
			'left conversion' component 'numerical type conversion'
			'right' [ ',' ] component 'calculated signed number selection starting from property'
			'right conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'list operation'
			'operation' stategroup (
				'sum' [ 'sumlist' ]
				'maximum' [ 'max' ]
				'minimum' [ 'min' ]
			)
			'numbers' [ '(' , ')' ] component 'signed number property list'
		'addition' ['add' '(']
			'left' component 'calculated signed number selection starting from property'
			'left conversion' component 'numerical type conversion'
			'right' [ ',' ] component 'calculated signed number selection starting from property'
			'right conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'difference' ['diff']
			'left' [ '(' ] component 'calculated signed number selection starting from property'
			'left constraint' component 'numerical type constraint'
			'right' [ ',' ] component 'calculated signed number selection starting from property'
			'right conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
	)
```

```js
'natural expression'
	'type' stategroup (
		'singular'
			'type' stategroup (
				'value' [ 'deprecated' ]
					'value' number
				'expression'
					'selected number type' stategroup (
						'integer' [ 'unsafe' ]
						'natural'
					)
					'expression' component 'calculated signed number selection starting from property'
			)
		'conditional' ['switch']
			'state group selection' ['(' , ')'] component 'calculated state group selection starting from property'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional natural number expression'
			)
		'referencer anchor sum' [ 'sum' 'unsafe' ]
			'context selection' component 'entity scoped ancestor property path'
			'referencer anchor' [ '<' ] reference
			'filter' component 'derivation node content path'
			'number context selection' component 'entity scoped ancestor node path'
			'number' [ '#' ] reference
			'conversion' component 'numerical type conversion'
		'referencer anchor count' [ 'count' 'unsafe' ]
			'context selection' component 'entity scoped ancestor property path'
			'referencer anchor' [ '<' ] reference
			'filter' component 'derivation node content path'
		'sum' [ 'sum' 'unsafe' ]
			'collection selection' component 'calculated collection selection starting from property'
			'filter' component 'derivation node content path'
			'property' [ '#' ] reference
			'conversion' component 'numerical type conversion'
		'count' [ 'count' 'unsafe' ]
			'collection selection' component 'calculated collection selection starting from property'
			'filter' component 'derivation node content path'
		'remainder' [ 'remainder' 'unsafe' ] // NOT SUPPORTED BY TYPE CHECKER
			'numerator' [ '(' ] component 'calculated signed number selection starting from property'
			'conversion rule' ['as'] reference
			'numerator conversion' component 'numerical type conversion'
			'denominator set' [ ',' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'denominator' component 'calculated signed number selection starting from property'
			'denominator conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'division' [ 'division' ]
			'rounding' stategroup (
				'ordinary' [ 'unsafe' ]
				'ceil' [ 'ceil' ]
				'floor' [ 'floor' 'unsafe' ]
			)
			'numerator type' [ '(' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'numerator' component 'calculated signed number selection starting from property'
			'conversion rule' ['as'] reference
			'numerator conversion' component 'numerical type conversion'
			'denominator type' [ ',' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'denominator' component 'calculated signed number selection starting from property'
			'denominator conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'product' [ 'product' ]
			'left number type' [ '(' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'left' component 'calculated signed number selection starting from property'
			'conversion rule' ['as'] reference
			'left conversion' component 'numerical type conversion'
			'right number type' [ ',' ] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'right' component 'calculated signed number selection starting from property'
			'right conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'list operation'
			'operation' stategroup (
				'sum' [ 'sumlist' ]
				'maximum' [ 'max' ]
				'minimum' [ 'min' ]
			)
			'numbers' [ '(' , ')' ] component 'natural number property list'
		'addition' ['add']
			'left number type' ['('] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'left' component 'calculated signed number selection starting from property'
			'left conversion' component 'numerical type conversion'
			'right number type' [','] stategroup (
				'integer' [ 'unsafe' ]
				'natural'
			)
			'right' component 'calculated signed number selection starting from property'
			'right conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
		'difference' [ 'diff' 'unsafe' ]
			'left' ['('] component 'calculated signed number selection starting from property'
			'left constraint' component 'numerical type constraint'
			'right' [','] component 'calculated signed number selection starting from property'
			'right conversion' component 'numerical type conversion'
			'KEYWORD' [')'] component 'KEYWORD'
	)
```

```js
'numerical type constraint'
```

```js
'numerical type conversion'
	'conversion' stategroup (
		'none'
			'constraint' component 'numerical type constraint'
		'factor'
			'conversion' ['from'] reference
		'base'
			'conversion' ['from' 'base'] reference
	)
```

```js
'calculated signed number selection starting from property'
	'sign' stategroup (
		'negative' [ '-' ]
		'positive'
	)
	'type' stategroup (
		'input parameter'
			'context selection' component 'ancestor node path'
			'state' stategroup ( 'state' )
			'input parameter' [ '&#' ] reference
		'number from property'
			'context selection' component 'ancestor property path'
			'number' [ '#' ] reference
		'number from node'
			'selection' component 'calculated node selection starting from property'
			'number' [ '#' ] reference
	)
```

```js
'signed number property list'
	'selection' component 'calculated signed number selection starting from property'
	'conversion' component 'numerical type conversion'
	'has element' stategroup (
		'no'
		'yes' [',']
			'tail' component 'signed number property list'
	)
```

```js
'natural number property list'
	'selected number type' stategroup (
		'natural'
		'integer' [ 'unsafe' ]
	)
	'selection' component 'calculated signed number selection starting from property'
	'conversion' component 'numerical type conversion'
	'has element' stategroup (
		'no'
		'yes' [',']
			'tail' component 'natural number property list'
	)
```

```js
'conditional number expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional number expression context path'
	)
```

```js
'conditional number expression'
	'has steps' stategroup (
		'no'
			'type' stategroup (
				'value' [ 'zero' ]
				'number'
					'expression context' component 'conditional number expression context path'
					'context' stategroup (
						'target context' [ '$^' ]
							'selection' component 'calculated signed number selection starting from property'
							'conversion' component 'numerical type conversion'
						'expression result'
							'sign' stategroup (
								'negative' [ '-' ]
								'positive'
							)
							'type' [ '$' ] stategroup (
								'numerical input parameter'
									'input parameter' [ '&#' ] reference
									'conversion' component 'numerical type conversion'
								'number from node'
									'context type' stategroup (
										'input parameter'
											'input parameter' [ '&' ] reference
										'this state'
									)
									'selection' component 'calculated descendant node selection starting from node'
									'number' [ '#' ] reference
									'conversion' component 'numerical type conversion'
							)
					)
			)
		'yes' ['switch' '(']
			'expression context' component 'conditional number expression context path'
			'type' stategroup (
				'merge' [ '$^' ]
					'state group selection' component 'calculated state group selection starting from property'
				'flatten' ['$']
					'context type' stategroup (
						'input parameter'
							'input parameter' [ '&' ] reference
						'this state'
					)
					'selection' component 'calculated descendant node selection starting from node'
					'state group' [ '?' ] reference
			)
			'KEYWORD' [')'] component 'KEYWORD'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional number expression'
			)
	)
```

```js
'conditional natural number expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional natural number expression context path'
	)
```

```js
'conditional natural number expression'
	'has steps' stategroup (
		'no'
			'type' stategroup (
				'value' [ 'one' ]
				'number'
					'selected number type' stategroup (
						'natural'
						'integer' [ 'unsafe' ]
					)
					'expression context' component 'conditional natural number expression context path'
					'context' stategroup (
						'target context' [ '$^' ]
							'selection' component 'calculated signed number selection starting from property'
							'conversion' component 'numerical type conversion'
						'expression result'
							'type' [ '$' ] stategroup (
								'numerical input parameter'
									'input parameter' [ '&#' ] reference
									'conversion' component 'numerical type conversion'
								'number from node'
									'context type' stategroup (
										'input parameter'
											'input parameter' [ '&' ] reference
										'this state'
									)
									'selection' component 'calculated descendant node selection starting from node'
									'number' [ '#' ] reference
									'conversion' component 'numerical type conversion'
							)
					)
			)
		'yes' ['switch' '(']
			'expression context' component 'conditional natural number expression context path'
			'type' stategroup (
				'merge' [ '$^' ]
					'state group selection' component 'calculated state group selection starting from property'
				'flatten' ['$']
					'context type' stategroup (
						'input parameter'
							'input parameter' [ '&' ] reference
						'this state'
					)
					'selection' component 'calculated descendant node selection starting from node'
					'state group' [ '?' ] reference
			)
			'KEYWORD' [')'] component 'KEYWORD'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional natural number expression'
			)
	)
```
### Derived states
The code sample exemplifies a derived state group property `Product found`.
The expression for deriving the state checks if the `Product` link produces a `Products` item from a `Products` `Catalog`.
This `Catalog` is provided by an external system, via an Alan `interface`: the `Catalog Provider`.
> ```js
'Catalog': group { can-update: interface 'Catalog Provider'
    'Products': collection ['Name'] {
        'Name': text
        'Price': integer 'eurocent'
    }
}
'Orders': collection ['ID'] {
    'ID': text
    // a link to a 'Products' item from the catalog provider:
    'Product': text ~> ^ .'Products'
    'Product found':= stategroup = any ( >'Product' ) (
        | true  = 'Yes' ( 'Product' => $ )
        | false = 'No'
    ) (
        'Yes' ( 'Product': +'Catalog'.'Products' ) -> {
            'Price': integer 'eurocent' = &'Product'#'Price'
        }
        'No' -> { }
    )
}
```

```js
'state expression'
	'expression type' stategroup (
		'resolvable link' [ 'any' ]
			'link context selection' ['('] component 'ancestor property path'
			'text' [ '>' ] reference
			'KEYWORD' [')'] component 'KEYWORD'
			'yes state instantiation' [ '(' '|' 'true' '=' ] group (
				'state' reference
				'input arguments' collection ( [ '(' , ')' ]
					'type' [ '=>' ] stategroup (
						'target context'
							'selection' component 'calculated node selection starting from property'
						'expression result'
							'expression context path' component 'link text expression context path'
							'state input parameter' stategroup (
								'yes' [ '&' ]
									'input parameter' reference
								'no'
							)
							'entity node selection' component 'entity scoped ancestor node path'
							'selection' component 'calculated descendant node selection starting from node'
					)
				)
			)
			'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
			'KEYWORD2' [')'] component 'KEYWORD'
		'branch match' [ 'match-branch' ]
			'branches' ['(', ')'] collection ( ['|']
				'state instantiation' [ '=' ] group (
					'state' reference
					'input arguments' collection ( [ '(' , ')' ]
						'type' [ '=>' ] stategroup (
							'target context'
								'selection' component 'calculated node selection starting from property'
							'expression result' [ '$' ]
								'expression context path' component 'traversed flatten expression'
								'state input parameter' stategroup (
									'yes' [ '&' ]
										'input parameter' reference
									'no'
								)
								'selection' component 'calculated descendant node selection starting from node'
						)
					)
				)
			)
		'containment' ['any' '(']
			'collection selection' component 'calculated collection selection starting from property'
			'dereference key' component 'dereference'
			'key path' [ '[' ,']' ] component 'calculated node selection starting from property'
			'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation 2'
			'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
			'KEYWORD' [')'] component 'KEYWORD'
		'node equality' ['match' '(']
			'left node type' stategroup (
				'ancestor'
					'selection' component 'ancestor node path'
				'sibling'
					'selection' component 'calculated node selection starting from property'
			)
			'right node' [ '==' ] component 'calculated node selection starting from property'
			'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation 2'
			'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation 2'
			'KEYWORD' [')'] component 'KEYWORD'
		'numerical' ['match']
			'left expression' ['('] component 'calculated signed number selection starting from property'
			'operator' stategroup (
				'equal to' [ '==' ]
				'greater than' [ '>' ]
				'greater than or equal to' [ '>=' ]
				'smaller than' [ '<' ]
				'smaller than or equal to' [ '<=' ]
			)
			'right type' stategroup (
				'value'
					'value' stategroup (
						'zero' [ 'zero' ]
						'one' [ 'one' ]
					)
				'expression'
					'right expression' component 'calculated signed number selection starting from property'
					'right conversion' component 'numerical type conversion'
			)
			'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation'
			'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
			'KEYWORD' [')'] component 'KEYWORD'
		'state merge' ['switch']
			'state group selection' [ '(' , ')' ] component 'calculated state group selection starting from property'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional state group expression'
			)
		'aggregation emptiness' [ 'any' ]
			'aggregate' [ '(' , ')' ] group (
				'collection selection' component 'calculated collection selection starting from property'
				'filter' component 'derivation node content path'
			)
			'no state instantiation' [ '(' '|' 'true' '=' ] group (
				'state' reference
				'input arguments' collection ( [ '(' , ')' ]
					'type' stategroup (
						'node' [ '=>' ]
							'selection' component 'calculated node selection starting from property'
						'number'
							'operation' [ '=' ] stategroup (
								'minimum' [ 'min' ]
								'maximum' [ 'max' ]
								'standard deviation' [ 'std' ]
							)
							'expression' group (
								'descendant selection' [ '$' ] component 'calculated descendant node selection starting from node'
								'number' [ '#' ] reference
							)
					)
				)
			)
			'yes state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
			'KEYWORD' [')'] component 'KEYWORD'
	)
```

```js
'conditional state group expression'
	'has steps' stategroup (
		'no'
			'state' reference
			'input arguments' collection ( [ '(' , ')' ]
				'expression context' [ '=>' ] component 'conditional state group expression context path'
				'context selection' stategroup (
					'target context' [ '$^' ]
						'selection' component 'calculated node selection starting from property'
					'expression result' [ '$' ]
						'context type' stategroup (
							'input parameter'
								'input parameter' [ '&' ] reference
							'this state'
						)
						'selection' component 'calculated descendant node selection starting from node'
				)
			)
		'yes' ['switch' '(']
			'expression context' component 'conditional state group expression context path'
			'type' stategroup (
				'merge' [ '$^' ]
					'state group selection' component 'calculated state group selection starting from property'
				'flatten' ['$']
					'context type' stategroup (
						'input parameter'
							'input parameter' [ '&' ] reference
						'this state'
					)
					'selection' component 'calculated descendant node selection starting from node'
					'state group' [ '?' ] reference
			)
			'KEYWORD' [')'] component 'KEYWORD'
			'states' [ '(' , ')' ] collection ( ['|']
				'expression' [ '=' ] component 'conditional state group expression'
			)
	)
```

```js
'conditional state group expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional state group expression context path'
	)
```

```js
'state instantiation'
	'state' reference
	'input arguments' collection ( [ '(' , ')' ]
		'constraint' stategroup ( 'node type' )
		'selection' [ '=>' ] component 'calculated node selection starting from property'
	)
```

```js
'state instantiation 2'
	'state' reference
	'input arguments' collection ( [ '(' , ')' ]
		'context' [ '=>' ] stategroup (
			'state group property'
				'selection' component 'calculated node selection starting from property'
			'expression result node' [ '$' ]
				'selection' component 'calculated descendant node selection starting from node'
		)
	)
```
### Derived collections

```js
'flatten expression'
	'head' component 'group context property selection'
	'type' stategroup (
		'prefiltered'
			'type' stategroup (
				'group' [ '+' ]
					'group' reference
				'state' [ '?' ]
					'state group' reference
					'state' [ '|' ] reference
			)
			'tail' component 'flatten expression tail'
		'plural'
			'collection' ['.'] reference
			'key value source' stategroup ( 'elementary' )
			'tail' component 'flatten expression tail'
	)
```

```js
'flatten expression tail'
	'head' component 'derivation node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'collection' ['.'] reference
			'key value source' stategroup ( 'elementary' )
			'tail' component 'flatten expression tail'
	)
```

```js
'traversed flatten expression'
	'has steps' stategroup (
		'no'
		'yes' ['^']
			'is not expression input node type' component 'EQ node type'
			'tail' component 'traversed flatten expression'
	)
```

```js
'plural reference expression'
	'type' stategroup (
		'augment' ['map']
			'selection' component 'calculated collection selection starting from property'
			'tail' component 'derivation node content path'
		'merge' [ 'union' ]
			'aggregates' [ '(' , ')' ] collection (
				'aggregate' [ '=>' ] component 'referencer aggregate'
			)
	)
```

```js
'referencer aggregate'
	'head' component 'group context property selection'
	'type' stategroup (
		'prefiltered'
			'type' stategroup (
				'group' [ '+' ]
					'group' reference
				'state' [ '?' ]
					'state group' reference
					'state' [ '|' ] reference
			)
			'tail' component 'referencer aggregate step'
		'plural'
			'collection' ['.'] reference
			'tail' component 'referencer aggregate step'
		'singular'
			'text'[ '>' ] reference
			'dereference' component 'dereference'
			'is backward' component 'EQ direction'
	)
```

```js
'referencer aggregate step'
	'head' component 'derivation node content path'
	'has steps' stategroup (
		'no'
			'text' [ '>' ] reference
			'dereference' component 'dereference'
			'is backward' component 'EQ direction'
		'yes'
			'collection' ['.'] reference
			'tail' component 'referencer aggregate step'
	)
```
## Permissions and Todos
---

Examples for permissions and todos:

> ```js
'Users': collection ['ID']
    can-create: user ?'Type'|'Admin'
    can-delete: user ?'Type'|'Admin'
{ can-update: user ?'Type'|'Admin'
    'ID': text
    'Address': group { can-update: equal ( /*this*/ , user )
        'Street': text
        'City': text
    }
    'Type': stategroup (
        'Admin' -> { }
        'Employee' -> { }
        'Unknown' -> { has-todo: user ?'Type'|'Admin' }
    )
}
// only team members can read team information:
'Teams': collection ['Name'] { can-read: any .'Members' [ user ]
    'Name': text
    'Members': collection ['Member'] {
        'Member': text ~> ^ ^ .'Users'
    }
    'Description': text
}
```


```js
'node permissions definition'
	'read permission' stategroup (
		'inherited'
		'explicit' ['can-read:']
			'permission' component 'permission'
	)
	'update permission' stategroup (
		'inherited'
		'explicit' ['can-update:']
			'permission' component 'permission'
	)
```

```js
'item permissions definition'
	'create permission' stategroup (
		'inherited'
		'explicit' ['can-create:']
			'permission' component 'permission'
	)
	'delete permission' stategroup (
		'inherited'
		'explicit' ['can-delete:']
			'permission' component 'permission'
			'EQ modifier' component 'EQ modifier'
	)
```

```js
'permission'
	'modifier' stategroup (
		'user'
			'requirement' component 'user requirement'
		'imported interface'
			'interface' ['interface'] reference
	)
```

```js
'todo definition'
	'todo' stategroup (
		'no'
		'yes' ['has-todo:']
			'requirement' component 'user requirement'
			'ui' component 'ui todo'
	)
```

```js
'user requirement'
	'type' stategroup (
		'containment' ['any']
			'path' component 'requirement conditional node path'
			'collection' ['.', '['] reference
			'delink key' component 'delink'
			'key path' component 'requirement conditional node path'
			'has filter' [']'] stategroup (
				'no'
				'yes'
					'assignment' component 'optional variable assignment'
					'where' ['where'] component 'KEYWORD'
					'path' ['(', ')'] component 'user requirement'
			)
		'existence'
			'path' component 'requirement conditional node path'
		'equality' ['equal']
			'left path' ['('] component 'requirement conditional node path'
			'right path' [',',')'] component 'requirement conditional node path'
	)
	'has alternative' stategroup (
		'no'
		'yes' ['||']
			'alternative' component 'user requirement'
	)
```

```js
'requirement context node path'
	'context' stategroup (
		'dynamic user' ['user']
		'requirement'
			'head' component 'ancestor node path'
		'variable'
			'head' component 'ancestor variable path'
			'type' stategroup ( 'variable' )
	)
```

```js
'requirement conditional node path'
	'head' component 'requirement context node path'
	'tail' component 'conditional descendant node path'
```
## Commands and Timers
---

Commands enable external systems to perform operations via an Alan `interface` on `application` data.
Furthermore, commands can perform operations on other systems that other systems provide via an Alan `interface`.
For this to work, interfaces have to be listed in the `interfaces` section of an `application` model.
Also, the `external` command needs to be consumed by the application model, like the `Place Order` command in the example:

> ```js
'Products': collection ['Name'] {
    'Name': text
}
'Place Order': command { 'Product': text -> .'Products' }
    external from 'Manufacturer'
'Orders': collection ['ID'] {
    'ID': text
    'Product': text -> ^ .'Products'
    'Creation Time': integer 'date and time' = creation-time
    'Status': stategroup (
        'New' -> {
            'Order from Manufacturer': command { }
                do on ^ ^ (
                    'Place Order' with ( 'Product': text = ^ .'Product' )
                ) and do on ^ (
                    'Status': stategroup = 'Waiting for Manufacturer' ( )
                )
        }
        'Delivered' -> { }
        'Delayed' -> { }
        'Waiting for Manufacturer' -> {
            'Agreed Upon Delivery Time': integer 'date and time'
                timer ontimeout do on ^ (
                    'Status': stategroup = 'Delayed' ( )
                )
        }
    )
}
// for external system 'Delivery Service':
'Register Delivery': command { 'Order': text -> .'Orders' }
    do on @ >'Order' (
        'Status': stategroup = 'Delivered' ( )
    )
```

```js
'command implementation' ['do']
	'type' stategroup (
		'conditional'
			'type' stategroup (
				'state switch' [ 'switch' ]
					'type' stategroup (
						'parameter'
							'path' ['(',')'] group (
								'path' component 'ancestor parameters path'
								'state group' ['?'] reference
							)
							'states' [ '(' , ')' ] collection ( ['|']
								'implementation' component 'command implementation'
							)
						'property'
							'path' ['(',')'] group (
								'path' component 'parametrized singular node path'
								'state group' ['?'] reference
							)
							'states' ['(', ')'] collection ( ['|']
								'variable assignment' component 'optional variable assignment'
								'implementation' component 'command implementation'
							)
					)
				'contains switch' ['any']
					'contains path' ['(', ')'] group (
						'path' component 'parametrized singular node path'
						'collection' ['.'] reference
						'key' ['[',']'] component 'parametrized text expression'
					)
					'cases' ['(',')'] group (
						'true case' ['|' 'true'] group (
							'variable assignment' component 'optional variable assignment'
							'implementation' component 'command implementation'
						)
						'false case' ['|' 'false'] group (
							'implementation' component 'command implementation'
						)
					)
			)
		'map' ['map']
			'type' stategroup (
				'parameter'
					'path' component 'ancestor parameters path'
					'collection' ['.'] reference
				'property'
					'path' component 'parametrized singular node path'
					'collection' ['.'] reference
					'variable assignment' component 'optional variable assignment'
			)
			'implementation' ['(',')'] component 'command implementation'
		'update'
			'update node' component 'parametrized update node'
		'ignore' ['ignore']
	)
	'has more statements' stategroup (
		'no'
		'yes' ['and']
			'statement' component 'command implementation'
	)
```

```js
'parameter definition' [ '{' , '}' ]
	'parameter' component 'parameter'
	'properties' collection indent (
		'preceding siblings' collection predecessors
		'member' component 'member'
		'type' [ ':' ] stategroup (
			'collection' ['collection']
				'key property' ['[',']'] reference
				'key constraint' stategroup (
					// 'no' ( )
					'yes'
				)
				'ui' component 'ui collection parameter'
				'entity' component 'entity'
				'parameters' component 'parameter definition'
			'text' [ 'text' ]
				'has constraint' stategroup (
					'no'
					'yes'
						'referencer' [ '->' ] component 'parameter referencer'
				)
				'ui' component 'ui text parameter'
			'number'
				'set' stategroup (
					'integer' [ 'integer' ]
					'natural' [ 'natural' ]
				)
				'numerical type' reference
				'ui' component 'ui number parameter'
			'file' ['file']
				'ui' component 'ui file parameter'
			'state group' [ 'stategroup' ]
				'ui' component 'ui state group parameter'
				'has states' stategroup has 'states' first 'first' 'yes' 'no'
				'states' [ '(' , ')' ] collection order 'view order' (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'constraints' collection ( ['(',')']
						'expression' component 'parameter state constraint expression'
					)
					'parameters' component 'parameter definition'
				)
		)
	)
```

```js
'delete node'
```

```js
'parametrized update node'
	'context node path' ['on'] component 'parametrized singular node path'
	'variable assignment' component 'optional variable assignment'
	'attributes' [ '(' , ')' ] collection indent (
		'type' stategroup (
			'command'
				'arguments' [ 'with' ] component 'argument definition'
			'property' [ ':' ]
				'type' stategroup (
					'collection' ['collection']
						'operation' stategroup (
							'create' [ 'create' ]
								'initialize node' component 'parametrized initialize node'
							'delete' ['delete']
								'path' component 'parametrized singular node path'
								'delete node' component 'delete node'
						)
					'number'
						'set' stategroup (
							'integer' [ 'integer' ]
							'natural' [ 'natural' ]
						)
						'operator' stategroup (
							'increment' [ 'increment' ]
							'assignment'
								'expression' ['='] component 'parametrized number expression'
						)
					'text' [ 'text' ]
						'expression' ['='] component 'parametrized text expression'
					'file' ['file']
						'expression' ['='] component 'parametrized file expression'
					'state group' [ 'stategroup' ]
						'expression' ['='] component 'parametrized state expression'
				)
		)
	)
```

```js
'parametrized initialize node' [ '(' , ')' ]
	'groups' collection indent (
		'initialize node' [ ':' 'group' ] component 'parametrized initialize node'
	)
	'texts' collection indent (
		'expression' [':' 'text' '='] component 'parametrized text expression'
	)
	'files' collection indent (
		'expression' [':' 'file' '='] component 'parametrized file expression'
	)
	'collections' collection (
		'expression' [':' 'collection' '='] component 'parametrized collection expression'
	)
	'numbers' collection indent (
		'set' stategroup (
			'integer' [ ':' 'integer' ]
			'natural' [ ':' 'natural' ]
		)
		'expression' [ '=' ] component 'parametrized number expression'
	)
	'state groups' collection indent (
		'expression' [ ':' 'stategroup' '=' ] component 'parametrized state expression'
	)
```

```js
'parameter referencer' // 'parameter reference constrain expression'
	'head' component 'parametrized singular node path'
	'collection' ['.'] reference
	'tail' component 'derivation node content path'
```

```js
'argument definition' [ '(' , ')' ]
	'properties' collection (
		'type' [ ':' ] stategroup (
			'collection' [ 'collection' ]
				'key constraint' stategroup (
					// 'no'
					'yes' ['=>']
						'expression' component 'parametrized collection argument expression'
				)
			'number'
				'type' stategroup (
					'integer' [ 'integer' ]
					'natural' [ 'natural' ]
				)
				'expression' ['='] component 'parametrized number expression'
			'text' [ 'text' ]
				// 'has constraint' stategroup (
				// 	'no' ['=']
				// 	'yes' ['=>']
				// )
				'expression' ['='] component 'parametrized text expression'
			'file' ['file']
				'expression' ['='] component 'parametrized file expression'
			'state group' [ 'stategroup' ]
				'expression' ['='] component 'parametrized state argument expression'
		)
	)
```

```js
'ancestor parameters path'
	'has steps' stategroup (
		'no' ['@']
		'yes' ['@^']
			'tail' component 'ancestor parameters path'
	)
```

```js
'parameter state constraint expression'
	'path' ['->'] component 'parametrized conditional node path'
```

```js
'parameter entity scoped context node selection'
	'head' component 'entity scoped ancestor node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'key reference' ['>']
					'text' reference
					'dereference' component 'dereference'
			)
			'tail' component 'parameter entity scoped context node selection'
	)
```

```js
'parametrized context node path'
	'context' stategroup (
		'command'
			'head' component 'ancestor node path'
		'variable'
			'head' component 'ancestor variable path'
			'type' stategroup (
				'variable'
			)
		'parameter'
			'head' component 'ancestor parameters path'
			'reference type' stategroup (
				'text'
					'text' [ '>' ] reference
					'tail' component 'entity scoped ancestor node path'
				'state' ['&']
					'constraint' reference
			)
	)
```

```js
'parametrized singular node path'
	'head' component 'parametrized context node path'
	'tail' component 'singular node path tail'
```

```js
'parametrized conditional node path'
	'head' component 'parametrized context node path'
	'tail' component 'conditional descendant node path'
```

```js
'parametrized text expression'
	'type' stategroup (
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized text expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized text expression'
					)
			)
		'parameter'
			'path' component 'ancestor parameters path'
			'text' [ '.' ] reference
		'property'
			'path' component 'parametrized singular node path'
			'text' [ '.' ] reference
	)
```

```js
'parametrized file expression'
	'type' stategroup (
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized file expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized file expression'
					)
			)
		'parameter'
			'path' component 'ancestor parameters path'
			'file' [ '/' ] reference
		'property'
			'path' component 'parametrized singular node path'
			'file' [ '/' ] reference
	)
```

```js
'parametrized number expression'
	'type' stategroup (
		'binary expression'
			'operation' stategroup (
				'sum' [ 'sum' ]
					'type eq' component 'type eq'
				'difference' [ 'diff' ]
				'division' [ 'division' ]
					'rounding' stategroup (
						'ordinary'
						'ceil' [ 'ceil' ]
						'floor' [ 'floor' ]
					)
					'type eq' component 'type eq'
				'product' ['product']
					'type eq' component 'type eq'
				'min' ['min']
					'type eq' component 'type eq'
				'max' ['max']
					'type eq' component 'type eq'
			)
			'expressions' [ '(' , ')' ] group (
				'left' component 'parametrized number expression'
				'right' [','] component 'parametrized number expression'
			)
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized number expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized number expression'
					)
			)
		'unary expression'
			'type' stategroup (
				'natural to integer cast' ['(' 'integer' ')']
					'expression' component 'parametrized number expression'
			)
		'property'
			'path' component 'parametrized singular node path'
			'number' [ '#' ] reference
		'parameter'
			'path' component 'ancestor parameters path'
			'number' [ '#' ] reference
		'current timestamp' [ 'now' ]
		'static'
			'value' stategroup (
				'zero' [ 'zero' ]
				'one' [ 'one' ]
			)
	)
```

```js
'parametrized state argument expression'
	'type' stategroup (
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized state argument expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized state argument expression'
					)
			)
		'static'
			'state' reference
			'arguments' component 'argument definition'
	)
```

```js
'parametrized state expression'
	'type' stategroup (
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized state expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized state expression'
					)
			)
		'static'
			'state' reference
			'initialize node' component 'parametrized initialize node'
	)
```

```js
'parametrized collection argument expression'
	'type' stategroup (
		'empty'
		'parameter' ['map']
			'selection' component 'ancestor parameters path'
			'collection' ['.'] reference
			'key property' ['[',']'] reference
			'context selection' ['(',')'] component 'parameter entity scoped context node selection'
			'arguments' component 'argument definition'
		'property' ['map']
			'path' component 'parametrized singular node path'
			'collection' ['.'] reference
			'key property' ['[',']'] reference
			'dereference key' component 'dereference'
			'context selection' ['(',')'] component 'parameter entity scoped context node selection'
			'variable assignment' component 'optional variable assignment'
			'arguments' component 'argument definition'
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized collection argument expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized collection argument expression'
					)
			)
	)
```

```js
'parametrized collection expression'
	'type' stategroup (
		'empty'
		'entry' ['create']
			'initialize node' component 'parametrized initialize node'
		'parameter' ['map']
			'selection' component 'ancestor parameters path'
			'collection' [ '.' ] reference
			'key property' ['[',']'] reference
			'initialize node' component 'parametrized initialize node'
		'property' ['map']
			'path' component 'parametrized singular node path'
			'collection' ['.'] reference
			'key property' ['[',']'] reference
			'variable assignment' component 'optional variable assignment'
			'initialize node' component 'parametrized initialize node'
		'state switch' ['switch']
			'type' stategroup (
				'parameter'
					'path' ['(',')'] group (
						'path' component 'ancestor parameters path'
						'state group' ['?'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'expression' ['='] component 'parametrized collection expression'
					)
				'property'
					'path' ['(',')'] group (
						'path' component 'parametrized singular node path'
						'state group' ['?'] reference
					)
					'states' ['(', ')'] collection ( ['|']
						'variable assignment' component 'optional variable assignment'
						'expression' ['='] component 'parametrized collection expression'
					)
			)
	)
```
## Node type identification
---

```js
'node path'
	'steps' component 'node path step'
```

```js
'node path step'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
				'group'
					'group' [ '+' ] reference
				'collection'
					'collection' [ '.' ] reference
			)
			'tail' component 'node path step'
	)
```
## Output parameters (legacy)
---
Output parameter definitions are helpers/sub-expressions for navigation expressions.

```js
'output parameters'
```

```js
'output parameters definition'
	'parameters' component 'output parameters'
	'output parameters' collection ( [ '(' , ')' ]
		'dependable' component 'dependency'
		'type' stategroup (
			'elementary' [ '->' ]
				'head' component 'entity scoped ancestor node path'
				'selection' component 'resolved node descendant selection starting from node'
			'derived' [ '=>' ]
				'head' component 'entity scoped ancestor node path'
				'context type' stategroup (
					'input parameter' [ '&' ]
						'input parameter' reference
					'result node'
				)
				'selection' component 'calculated descendant node selection starting from node'
		)
	)
```
## Navigation
---
Examples of typical navigation steps:
> ```js
.'My Text'       // select text value
/'My File'       // select file value
#'My Number'     // select number value
.'My Collection' // select collection
?'My StateGroup' // select stategroup
|'My State'      // select/require state
+'My Group'      // select group node
--
>>'My Text'               // go to referenced node
>>'My Text'$'Output'      // go to reference output node
&'My State ctx'           // go to state context node
?'My Stategroup'$'Output' // go to stategroup output node
--
^                // go to parent node
$^               // go to parent variable context
$                // select variable
```

### Node navigation

```js
'ancestor node path'
	'has steps' stategroup (
		'no'
		'yes' ['^']
			'tail' component 'ancestor node path'
	)
```

```js
'entity scoped ancestor node path'
	'path' component 'ancestor node path'
```

```js
'singular node path tail'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'reference'
					'text' [ '>' ] reference
					'dereference' component 'dereference'
				'output parameter'
					'text' ['>'] reference
					'dereference' component 'dereference'
					'output parameter' [ '$' ] reference
				'group' ['+']
					'group' reference
				'state group output parameter'
					'state group' ['?'] reference
					'output parameter' ['$'] reference
				'state context parameter'
					'parameter' [ '&' ] reference
			)
			'tail' component 'singular node path tail'
	)
```

```js
'conditional descendant node path'
	'head' component 'singular node path tail'
	'has steps' stategroup (
		'no'
		'yes'
			'state group' ['?'] reference
			'state' ['|'] reference
			'tail' component 'conditional descendant node path'
	)
```
### Variable assignment and navigation

```js
'optional variable assignment'
	'has assignment' stategroup (
		'no'
		'yes'
			'assignment' component 'variable assignment'
	)
```

```js
'variable assignment' ['as' '$']
	'variable' component 'variable'
```

```js
'ancestor variable path'
	'has steps' stategroup (
		'no' ['$']
		'yes' ['$^']
			'tail' component 'ancestor variable path'
	)
```
### Shared node navigation for constraints & derivations (legacy)

```js
'ancestor property path'
	'has steps' stategroup (
		'no'
		'yes' ['^']
			'tail' component 'ancestor property path'
	)
```

```js
'entity scoped ancestor property path'
	'path' component 'ancestor property path'
```

```js
'group node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'group' [ '+' ] reference
			'tail' component 'group node selection'
	)
```

```js
'resolved node selection starting from property'
	'type' stategroup (
		'input parameter'
			'type' stategroup (
				'state'
					'context selection' component 'ancestor property path'
					'state' stategroup (
						'state'
					)
					'input parameter' [ '&' ] reference
			)
			'tail' component 'resolved node descendant selection starting from node'
		'this node'
			'context selection' component 'ancestor property path'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
					'tail' component 'resolved node descendant selection starting from node'
				'state group output parameter'
					'state group' [ '?' ] reference
					'output parameter' [ '$' ] reference
				'referencer output'
					'text' [ '>' ] reference
					'is backward' stategroup ( 'is backward' )
					'output type' stategroup (
						'referenced node'
						'output parameter'
							'output parameter' [ '$' ] reference
					)
			)
	)
```
### Node navigation for constraints (legacy)

```js
'resolved state group selection starting from property'
	'type' stategroup (
		'state group'
			'context selection' component 'ancestor property path'
			'state group' [ '?' ] reference
		'node'
			'selection' component 'resolved node selection starting from property'
			'state group' [ '?' ] reference
	)
```

```js
'resolved collection selection starting from property'
	'type' stategroup (
		'collection'
			'context selection' component 'ancestor property path'
			'collection' [ '.' ] reference
		'node'
			'selection' component 'resolved node selection starting from property'
			'collection' [ '.' ] reference
	)
```

```js
'resolved node descendant selection starting from node'
	'group selection' component 'group node selection'
	'type' stategroup (
		'this node'
			'state group output parameter'
				'state group' [ '?' ] reference
				'output parameter' [ '$' ] reference
			'referencer output'
				'text' [ '>' ] reference
				'is backward' stategroup ( 'is backward' )
				'output type' stategroup (
					'referenced node'
					'output parameter'
						'output parameter' [ '$' ] reference
				)
	)
```

```js
'node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'node content path'
	)
```

```js
'unresolved node selection'
	'type' stategroup (
		'this node'
			'context selection' component 'ancestor property path'
			'type' stategroup (
				'this'
				'referencer output'
					'text' [ '>' ] reference
					'is forward' stategroup ( 'is forward' )
			)
	)
	'tail' component 'group node selection'
```
### Node navigation for derivations (legacy)

```js
'derivation node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'derivation node content path'
	)
```

```js
'group context property selection'
	'has steps' stategroup (
		'no'
		'yes' [ '^' ]
			'tail' component 'group context property selection'
	)
```

```js
'calculated input parameter node selection'
	'type' stategroup (
		'state'
			'context selection' component 'ancestor node path'
			'state' stategroup ( 'state' )
			'input parameter' [ '&' ] reference
	)
```

```js
'calculated descendant node selection starting from node'
	'group selection' component 'group node selection'
	'type' stategroup (
		'this node'
		'state group output parameter'
			'state group' [ '?' ] reference
			'output parameter' [ '$' ] reference
		'referencer output'
			'text' [ '>' ] reference
			'dereference' component 'dereference'
			'output type' stategroup (
				'referenced node'
				'output parameter'
					'output parameter' [ '$' ] reference
			)
	)
```

```js
'calculated descendant node selection starting from property'
	'type' stategroup (
		'group'
			'group' [ '+' ] reference
			'tail' component 'calculated descendant node selection starting from node'
		'state group output parameter'
			'state group' [ '?' ] reference
			'output parameter' [ '$' ] reference
		'referencer output'
			'text' [ '>' ] reference
			'dereference' component 'dereference'
			'output type' stategroup (
				'referenced node'
				'output parameter'
					'output parameter' [ '$' ] reference
			)
	)
```

```js
'calculated node selection starting from property'
	'type' stategroup (
		'input parameter'
			'selection' component 'calculated input parameter node selection'
			'tail' component 'calculated descendant node selection starting from node'
		'this node'
			'context selection' component 'ancestor property path'
			'selection' component 'calculated descendant node selection starting from property'
	)
```
### Property navigation for derivations (legacy)

```js
'calculated collection selection starting from property'
	'type' stategroup (
		'collection'
			'context selection' component 'ancestor property path'
			'collection' ['.'] reference
		'node'
			'selection' component 'calculated node selection starting from property'
			'collection' ['.'] reference
	)
```

```js
'calculated state group selection starting from property'
	'type' stategroup (
		'state group'
			'context selection' component 'ancestor property path'
			'state group' [ '?' ] reference
		'node'
			'selection' component 'calculated node selection starting from property'
			'state group' [ '?' ] reference
	)
```
## User interface annotations
---
User interface annotations, or annotations for short, are recognizable by the
`@` character before the keyword. E.g. `@default:`. Most annotations
affect generated user interfaces (a system of type `auto-webclient`); they typically
do not affect custom user interfaces (system type `webclient`).

It is possible to use multiple annotations on a single property. Be aware that
they should be added in a specific order. Consult this grammar for the order of
annotations.

### Defaults
Most property types support the `@default:` annotation. Defaults apply default values to properties of new
nodes only and fail silently. That is, if the path contains a state navigation step and the
stategroup is not in that state, the default won't be applied. In the following
example the `Score` property will not be set when the state of `Default Score`
is anything other than `Known`.

>```js
'Score': natural 'score' @default: ? 'Default Score' | 'Known' # 'Value'
```

A default value is not necessarily a valid value. If validation
rules or constraints apply, a default value can be invalid.
When a derived value is used, make sure it is not a part of the new
node. Derived values on new nodes are computed after the node is saved,
and will therefore not be included in default values.

The property description would get set to: `Deliver  pieces`.

>```js
'Description': text @default: "Deliver ", to-text . 'To deliver' " pieces."
'To deliver' := integer 'pieces' = sum ^ . 'Order' # 'Amount'
```

### Identifying properties

Properties that are important for the identification of a collection entry can be marked
with the `@identifying` annotation. Identifying properties are shown together with the
unique identifier of a collection entry, whenever the entry is referenced.
For example, when an employee has a uniquely identifying personnel number
in a collection of employees, a reference to employee will show the name of the employee
when the 'name' property is marked as identifying.

### Icons

For better visual identification an icon can be specified using the @icon
attribute. As an argument it takes an icon name. A complete list of the
supported icons can be found at: https://octicons.github.com/.

```js
'context node selection'
	'head' component 'ancestor node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'context node selection'
	)
```

```js
'ui text validation'
	'regular expression' text
```

```js
'ui number limit'
	'type' stategroup (
		'static'
			'limit' number
		'dynamic'
			'base' stategroup (
				'today' [ 'today' ]
				'now' [ 'now' ]
			)
			'with offset' stategroup (
				'no'
				'yes' [ '+' ]
					'offset' number
			)
	)
```

```js
'ui file name expression'
	'has steps' stategroup (
		'no'
		'yes' [ '&' ]
			'type' stategroup (
				'static'
					'text' text
				'property'
					'path' component 'context node selection'
					'type' stategroup (
						'text' [ '.' ]
							'text' reference
						'number' [ '#' ]
							'number' reference
						'state group' [ '?' ]
							'state group' reference
							'states' [ '(' , ')' ] collection (
								'state file name expression' [ '(' , ')' ] component 'ui file name expression'
							)
					)
			)
			'tail' component 'ui file name expression'
	)
```

```js
'ui linked node mapping path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'ui linked node mapping path'
	)
```

```js
'ui linked node mapping' [ '(' , ')' ]
	'properties' collection indent (
		'type' stategroup (
			'number' [ 'number' '<-' ]
				'path' component 'ui linked node mapping path'
				'number' reference
			'text' [ 'text' '<-' ]
				'path' component 'ui linked node mapping path'
				'source text' reference
			'file' [ 'file' '<-' ]
				'path' component 'ui linked node mapping path'
				'file' reference
			'group' [ 'group' ]
				'path' component 'ui linked node mapping path'
				'mapping' component 'ui linked node mapping'
			'state group' [ 'stategroup' '<-' ]
				'path' component 'ui linked node mapping path'
				'linked node state group' [ '?' ] reference
				'linked node states' [ '(' , ')' ] collection indent (
					'state' [ '->' ] reference
					'mapping' component 'ui linked node mapping'
				)
			'collection' [ 'collection' ]
		)
	)
```

```js
'ui singular node path'
	'head' component 'ancestor node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state constraint' [ '&' ]
					'input parameter' reference
				'state group output parameter'
					'state group' [ '?' ] reference
					'output parameter' [ '$' ] reference
				'referencer output'
					'text' [ '>' ] reference
					'dereference' component 'dereference'
					'output parameter' [ '$' ] reference
				'group' [ '+' ]
					'group' reference
				'reference' [ '>' ]
					'text' reference
					'dereference' component 'dereference'
			)
			'tail' component 'ui singular node path'
	)
```

```js
'ui conditional node path'
	'head' component 'ui singular node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
				'link' [ '~>' ]
					'text' reference
					'delink' component 'delink'
			)
			'tail' component 'ui conditional node path'
	)
```

```js
'ui parametrized node path'
	'head' component 'parametrized context node path'
	'tail' component 'ui node path tail'
```

```js
'ui node path'
	'head' component 'ancestor node path'
	'tail' component 'ui node path tail'
```

```js
'ui node path tail'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'reference'
					'text' [ '>' ] reference
					'delink' component 'delink'
				'output parameter'
					'text' ['>'] reference
					'dereference' component 'dereference'
					'output parameter' [ '$' ] reference
				'group' ['+']
					'group' reference
				'state group output parameter'
					'state group' ['?'] reference
					'output parameter' ['$'] reference
				'state context parameter'
					'parameter' [ '&' ] reference
				'state'
					'state group' ['?'] reference
					'state' ['|'] reference
			)
			'tail' component 'ui node path tail'
	)
```

```js
'ui numerical type'
	'represent as' stategroup (
		'model'
		'date' [ '@date' ]
		'date and time' [ '@date-time' ]
		'decimal' [ '@factor:' '10^' ]
			'point translation' number
		'duration' [ '@duration:' ]
			'unit' stategroup (
				'seconds' [ 'seconds' ]
				'minutes' [ 'minutes' ]
				'hours' [ 'hours' ]
			)
	)
	'label' stategroup (
		'model'
		'custom' [ '@label:' ]
			'label' text
	)
```

```js
'ui command attribute'
	'visible' stategroup (
		'true' [ '@visible' ]
		'false' [ '@hidden' ]
	)
```
### Group
The `@breakout` annotation indicates that a group property
should not be displayed together with the other properties. At the time of
this writing, the group is put in a separate tab in the details view of an entry.
Note that the tab is always added to the top level tabs of a details view.
That is, if a group is inside a state or another group, it is not added to the tabs of the state.

```js
'ui group property'
	'visible' stategroup (
		'true'
			'break out' stategroup (
				'no'
				'yes' [ '@breakout' ]
			)
		'false' [ '@hidden' ]
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
```
### Collection
The `@default:` annotation copies entries of a source collection into the annotated collection.
A subset of the entries from the source collection can be copied by specifying a state filter:

>```js
'Labels': collection ['Name'] {
	'Name': text
	'Default': stategroup (
		'Yes' -> { }
		'No' -> { }
	)
}
'Issues': collection ['Name']  {
	'Name': text
	'Labels': collection ['Name'] @default: > 'Name' ? 'Default' | 'Yes' {
		'Name': text -> ^ ^ . 'Labels'
	}
}
```

This only applies to new nodes holding collections. This annotation does nothing for
collections on the root node:

> ```js
root {
	'People': collection ['Name'] {
		'Name': text
	}
	'Employees': collection ['Name'] @default: > 'Name' { // This has no effect.
		'Name': text
	}
}
```

Collections can only be initialized from the collection that it references,
using the key property, or using a derived link that derives from the key. In
the latter case, other collections can be used to initialize an entry as long as
the keys are the same.

> ```js`
'Imported Categories': collection ['Id'] {
	'Id': text
}
'Gegevens': collection ['Id'] @default: >'Category' {
	'Id': text /* -> some constraint or not */
	'Category':= text = .'Id' ~> ^ .'Imported Categories'
}
````

```js
'ui collection property'
	'sort' stategroup (
		'no'
		'yes'
			'direction' stategroup (
				'ascending' ['@ascending:']
				'descending' ['@descending:']
			)
			'property context' component 'ui conditional node path'
			'type' stategroup (
				'text' ['.']
					'property' reference
				'number' ['#']
					'property' reference
			)
	)
	'visible' stategroup (
		'true'
		'false' [ '@hidden' ]
	)
	'size' stategroup (
		'small' [ '@small' ]
		'large'
	)
	'can be dormant' stategroup (
		'no'
		'yes' [ '@dormant' ]
			'context' component 'derivation node content path'
			'state group' [ '?' ] reference
			'dormant state' [ '|' ] reference
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
	'default' stategroup (
		'no'
		'yes' [ '@default:' ]
			'key property' ['>'] reference
			'delink' component 'delink'
			'entry filter' component 'ui node path tail'
	)
	'linked node mapping' stategroup (
		'none'
		'from linked entry' [ '@linked-node-mapping' ]
			'context node selection' component 'entity scoped ancestor node path'
				'mapping' component 'ui linked node mapping'
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
	'has style' stategroup (
		'no'
		'yes' [ '@style:' ]
			'context' component 'ui conditional node path'
			'state group' [ '?' ] reference
			'type' stategroup (
				'select'
					'state' [ '|' ] reference
					'style' component 'ui style'
				'switch'
					'states' [ '(' , ')' ] collection ( ['|']
						'has style' ['='] stategroup (
							'yes'
								'style' component 'ui style'
							'no' ['none']
						)
					)
			)
	)
```

```js
'ui number property'
	'visible' stategroup (
		'true'
		'false' [ '@hidden' ]
	)
	'identifying' stategroup (
		'no'
		'yes' [ '@identifying' ]
	)
	'default' stategroup (
		'no'
		'yes' [ '@default:' ]
			'value' stategroup (
				'today' [ 'today' ]
				'now' [ 'now' ]
				'one' [ 'one' ]
				'zero' [ 'zero' ]
				'property'
					'path' component 'ui node path'
					'number' [ '#' ] reference
			)
	)
	'metadata' stategroup (
		'no'
		'yes' [ '@metadata' ]
	)
	'validation' group (
		'has minimum' stategroup (
			'no'
			'yes' [ '@min:' ]
				'minimum' component 'ui number limit'
		)
		'has maximum' stategroup (
			'no'
			'yes' [ '@max:' ]
				'maximum' component 'ui number limit'
		)
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
```

```js
'ui file property'
	'file name expression' stategroup (
		'no'
		'yes' [ '@name' ]
			'file name expression' [ '(' , ')' ] component 'ui file name expression'
	)
	'visible' stategroup (
		'true'
		'false' [ '@hidden' ]
	)
	'identifying' stategroup (
		'no'
		'yes' [ '@identifying' ]
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
```

```js
'ui default text expression'
	'type' stategroup (
		'static'
			'value' text
		'dynamic'
			'type' stategroup (
				'text'
					'path' component 'ui parametrized node path'
					'text' [ '.' ] reference
				'number' [ 'to-text' ]
					'path' component 'ui parametrized node path'
					'number' [ '.' ] reference
			)
	)
	'has next' stategroup (
		'no'
		'yes'
			'next' [','] component 'ui default text expression'
	)
```

```js
'ui text property'
	'visible' stategroup (
		'true'
		'false' [ '@hidden' ]
	)
	'identifying' stategroup (
		'no'
		'yes' [ '@identifying' ]
	)
	'type' stategroup (
		'default'
		'multi-line' [ '@multi-line' ]
	)
	'default value' stategroup (
		'no'
		'yes' [ '@default:' ]
			'source' stategroup (
				'expression'
					'expression' component 'ui default text expression'
				'current user' ['user']
					'constraint' component 'EQ node type'
				'guid' ['guid']
			)
	)
	'has validation' stategroup (
		'no'
		'yes' [ '@validate:' ]
			'rules' component 'ui text validation'
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
```

```js
'ui state group property'
	'visible' stategroup (
		'true'
		'false' [ '@hidden' ]
	)
	'identifying' stategroup (
		'no'
		'yes' [ '@identifying' ]
	)
	'default state' stategroup (
		'no'
		'yes' [ '@default:' ]
			'source' stategroup (
				'state'
					'state' reference
				'state switch' ['switch' '(']
					'path' group (
						'path' component 'ui node path'
						'state group' ['?',')'] reference
					)
					'states' [ '(' , ')' ] collection ( ['|']
						'action' stategroup (
							'do nothing' ['ignore']
							'set state'
								'state' ['='] reference
						)
					)
			)
	)
	'constraining collection' stategroup (
		'no'
		'yes' [ '@ordered:' ]
			'type' stategroup ( 'linear' )
			'first entry state' reference
			'state' [ 'or' ] reference
			'constraining reference' [ '.' ] reference
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
```

```js
'ui state'
	'desired state' stategroup (
		'no'
		'yes' [ '@desired' ]
	)
	'verified state' stategroup (
		'no'
		'yes' [ '@verified' ]
	)
	'icon' stategroup (
		'no'
		'yes' [ '@icon:' ]
			'name' text
	)
	'has style' stategroup (
		'no'
		'yes' [ '@style:' ]
			'style' component 'ui style'
	)
```

```js
'ui collection parameter'
	'default' stategroup (
		'yes' ['@default:' 'map']
			'entry filter' component 'ui node path tail'
		'no'
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
```

```js
'ui text parameter'
	'has validation' stategroup (
		'no'
		'yes' [ '@validate:' ]
			'rules' component 'ui text validation'
	)
	'default' stategroup (
		'no'
			'sticky' stategroup (
				'yes' [ '@sticky' ]
				'no'
			)
		'yes' ['@default:']
			'source' stategroup (
				'guid' [ 'guid' ]
				'current user' [ 'user' ]
					'constraint' component 'EQ node type'
				'expression'
					'expression' component 'ui default text expression'
			)
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
```

```js
'ui number parameter'
	'default' stategroup (
		'no'
			'sticky' stategroup (
				'yes' [ '@sticky' ]
				'no'
			)
		'yes' ['@default:']
			'value' stategroup (
				'today' ['today' ]
				'now' ['now' ]
				'one' ['one' ]
				'zero' ['zero' ]
				'property'
					'path' component 'ui parametrized node path'
					'number' [ '#' ] reference
			)
	)
	'validation' group (
		'has minimum' stategroup (
			'no'
			'yes' [ '@min:' ]
				'minimum' component 'ui number limit'
		)
		'has maximum' stategroup (
			'no'
			'yes' [ '@max:' ]
				'maximum' component 'ui number limit'
		)
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
```

```js
'ui file parameter'
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
```

```js
'ui state group parameter'
	'default state' stategroup (
		'no'
			'sticky' stategroup (
				'yes' [ '@sticky' ]
				'no'
			)
		'yes' [ '@default:' ]
			'source' stategroup (
				'state'
					'state' reference
				'state switch' ['switch' '(']
					'path' group (
						'path' component 'parametrized conditional node path'
						'state group' ['?',')'] reference
					)
					'states' [ '(' , ')' ] collection  ( ['|']
						'action' stategroup (
							'do nothing' ['ignore']
							'set state'
								'state' ['='] reference
						)
					)
			)
	)
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
```

```js
'ui todo'
	'has description' stategroup (
		'no'
		'yes' [ '@description:' ]
			'description' text
	)
```

```js
'ui style'
	'style' stategroup (
		'foreground' ['foreground']
		'background' ['background']
		'brand' ['brand']
		'link' ['link']
		'accent' ['accent']
		'success' ['success']
		'warning' ['warning']
		'error' ['error']
		'blue' ['blue']
		'orange' ['orange']
		'green' ['green']
		'red' ['red']
		'purple' ['purple']
		'teal' ['teal']
	)
```
## Type checker annotation rules
---
The rules below are for the type checker; they do not require keywords, so you can ignore them when writing a model.

```js
'KEYWORD'
```

```js
'value source base'
```

```js
'value source'
```

```js
'dependency'
```

```js
'direction type'
```

```js
'modifier'
```

```js
'type'
```

```js
'set type'
```

```js
'integer'
	'set type' component 'set type'
```

```js
'natural'
	'set type' component 'set type'
```

```js
'entity'
```

```js
'member'
```

```js
'variable'
```

```js
'parameter'
```

```js
'link'
```

```js
'reference'
```

```js
'delink'
	'delink' stategroup ( 'yes' )
```

```js
'dereference'
	'dereference' stategroup ( 'yes' )
```

```js
'linker'
	'link' component 'link'
```

```js
'referencer'
	'dependable' component 'dependency'
	'reference' component 'reference'
	'linker' component 'linker'
```

```js
'type eq'
```

```js
'EQ modifier'
```

```js
'EQ node type'
```

```js
'EQ member'
```

```js
'EQ direction'
```
## Unsupported legacy rules
---

```js
'log node' [ '(' , ')' ]
	'properties' collection (
		'type' [ ':' ] stategroup (
			'group' [ 'group' ]
				'node' component 'log node'
			'number' [ 'number' ]
			'state group' [ 'stategroup' ]
				'states' [ '(' , ')' ] collection (
					'node' component 'log node'
				)
			'text' [ 'text' ]
			'file' ['file']
		)
	)
```
