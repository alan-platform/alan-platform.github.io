---
layout: doc
origin: model
language: application
version: 33
type: grammar
---


## root


### user

```js
'user' ['users'] component 'modifier'
```

### allow anonymous user

```js
'allow anonymous user' stategroup (
	'no'
	'yes' [ 'anonymous' ]
)
```

### has dynamic users

```js
'has dynamic users' stategroup (
	'no'
	'yes'
		'context node path' [ 'dynamic' ':' ] component 'node content path'
		'users dictionary' [ '.' ] reference
		'password node' ['password' ':'] component 'node content path'
		'password property' [ '.' ] reference
)
```

### roles

```js
'roles' [ 'roles' ] collection indent (
	'condition' [ ':' ] stategroup (
		'interface' [ 'interface' ]
			'modifier' component 'modifier'
		'user'
			'dynamic' stategroup (
				'no'
				'yes' [ 'dynamic' ]
					'path' component 'node content path'
			)
			'anonymous' stategroup (
				'no'
				'yes' [ 'anonymous' ]
			)
	)
)
```

### source base

```js
'source base' group (
	'elementary' component 'value source base'
	'derived' component 'value source base'
)
```

### source

```js
'source' group (
	'user'			component 'value source'
	'meta'			component 'value source'
	'inference'		component 'value source'
	'calculation'	component 'value source'
)
```

### integer

```js
'integer' component 'integer'
```

### natural

```js
'natural' component 'natural'
```

### type

```js
'type' [ 'root' ] component 'type'
```

### root mutation permission

```js
'root mutation permission' component 'mutation permission definition'
```

### root read permission

```js
'root read permission' component 'read permission definition'
```

### dependable

```js
'dependable' component 'dependency'
```

### entity

```js
'entity' component 'entity'
```

### root

```js
'root' component 'node'
```

### numerical types
Annotations map numerical types to formats for easy modification in the UI.
Examples:
- @date
- @date-time
- @duration: minutes

With `@factor` you can translate 100 cents to 1 euro.<br>
If you do so, be sure to set `label` to "€" as well!

```js
'numerical types' [ 'numerical-types' ] collection indent (
	'type' stategroup (
		'relative' ['in']
			'range type' reference
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
	'ui' group (
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
	)
)
```

## component rules


### value source base

```js
'value source base'
```

### value source

```js
'value source'
```

### value

```js
'value'
```

### elementary value

```js
'elementary value'
	'value' component 'value'
```

### derived value

```js
'derived value'
	'value' component 'value'
```

### dependency

```js
'dependency'
```

### constraints

```js
'constraints'
	'constraints' collection (
		'type' [':'] stategroup (
			'acyclic' [ 'acyclic-graph' ]
			'linear' [ 'ordered-graph' ]
		)
	)
```

### selection type

```js
'selection type'
```

### backward selection

```js
'backward selection'
	'tag' component 'selection type'
```

### forward selection

```js
'forward selection'
	'tag' component 'selection type'
```

### modifier

```js
'modifier'
```

### type

```js
'type'
```

### set type

```js
'set type'
```

### integer

```js
'integer'
	'set type' component 'set type'
```

### natural

```js
'natural'
	'set type' component 'set type'
```

### entity

```js
'entity'
```

### resolved node selection starting from property

```js
'resolved node selection starting from property'
	'type' stategroup (
		'input parameter'
			'type' stategroup (
				'state'
					'context selection' component 'context property selection'
					'state' stategroup (
						'state'
					)
					'input parameter' [ '&' ] reference
			)
			'tail' component 'resolved node descendant selection starting from node'
		'this node'
			'context selection' component 'context property selection'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
					'tail' component 'resolved node descendant selection starting from node'
				'state group output parameter'
					'state group' [ '?' ] reference
					'output parameter' [ '$' ] reference
				'referencer output'
					'referencer type' stategroup (
						'matrix' [ '>key' ]
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
						'reference'
							'reference' [ '>' ] reference
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
					)
			)
	)
```

### resolved state group selection starting from property

```js
'resolved state group selection starting from property'
	'type' stategroup (
		'state group'
			'context selection' component 'context property selection'
			'state group' [ '?' ] reference
		'node'
			'selection' component 'resolved node selection starting from property'
			'state group' [ '?' ] reference
	)
```

### resolved collection selection starting from property

```js
'resolved collection selection starting from property'
	'type' stategroup (
		'dictionary'
			'context selection' component 'context property selection'
			'dictionary' [ '.' ] reference
		'matrix'
			'context selection' component 'context property selection'
			'matrix' [ '%' ] reference
		'node'
			'selection' component 'resolved node selection starting from property'
			'collection type' stategroup (
				'dictionary'
					'dictionary' [ '.' ] reference
				'matrix'
					'matrix' [ '%' ] reference
			)
	)
```

### resolved node descendant selection starting from node

```js
'resolved node descendant selection starting from node'
	'group selection' component 'group node selection' //NOTE: not supported by parser generator
	'type' stategroup (
		'this node'
			'state group output parameter'
				'state group' [ '?' ] reference
				'output parameter' [ '$' ] reference
			'referencer output'
				'referencer type' stategroup (
					'matrix' [ '>key' ]
					'output type' stategroup (
						'referenced node'
						'output parameter'
							'output parameter' [ '$' ] reference
					)
					'reference'
						'reference' [ '>' ] reference
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
				)
	)
```

### derivation selection path

```js
'derivation selection path'
	'context' stategroup (
		'this node'
			'context selection' component 'derivation node selection'
		'output parameter'
			'context selection' component 'derivation node selection'
			'type' stategroup (
				'state group output parameter'
					'state group' [ '?' ] reference
					'output parameter' [ '$' ] reference
				'referencer output'
					'referencer type' stategroup (
						'matrix' [ '>key' ]
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
						'reference' [ '>' ]
							'reference' reference
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
					)
			)
		'input parameter'
			'context node selection' component 'derivation node selection'
			'type' stategroup (
				'state' [ '&' ]
					'input parameter' reference
			)
			'tail' component 'derivation node selection'
	)
```

### node content path

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

### traversed derivation node content path

```js
'traversed derivation node content path'
	'step back' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state' [ '?^' ]
				'group' [ '+^' ]
			)
			'tail' component 'traversed derivation node content path'
	)
```

### group context property selection

```js
'group context property selection'
	'has steps' stategroup (
		'no'
		'yes' [ '+^' ]
			'tail' component 'group context property selection'
	)
```

### entity scoped context property selection

```js
'entity scoped context property selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
			)
			'tail' component 'entity scoped context property selection'
	)
```

### entity scoped context node selection

```js
'entity scoped context node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
			)
			'tail' component 'entity scoped context node selection'
	)
```

### unresolved node selection

```js
'unresolved node selection'
	'type' stategroup (
		'this node'
			'context selection' component 'context property selection'
			'type' stategroup (
				'this'
				'referencer output'
					'referencer type' stategroup (
						'matrix' [ '>key' ]
						'reference'
							'reference' [ '>' ] reference
					)
			)
	)
	'tail' component 'group node selection'
```

### context node selection

```js
'context node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'context node selection'
	)
```

### ancestor node selection

```js
'ancestor node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
			)
			'tail' component 'ancestor node selection'
	)
```

### context property selection

```js
'context property selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
			)
			'tail' component 'context property selection'
	)
```

### group node selection

```js
'group node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'group' [ '+' ] reference
			'tail' component 'group node selection'
	)
```

### derivation node content path

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

### derivation node selection

```js
'derivation node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'derivation node selection'
	)
```

### calculated input parameter node selection

```js
'calculated input parameter node selection'
	'type' stategroup (
		'state'
			'context selection' component 'ancestor node selection'
			'state' stategroup ( 'state' )
			'input parameter' [ '&' ] reference
	)
```

### calculated descendant node selection starting from node

```js
'calculated descendant node selection starting from node'
	'group selection' component 'group node selection' //NOTE: not supported by parser generator
	'type' stategroup (
		'this node'
		'state group output parameter'
			'state group' [ '?' ] reference
			'output parameter' [ '$' ] reference
		'referencer output'
			'referencer type' stategroup (
				'matrix' [ '>key' ]
					'output type' stategroup (
						'referenced node'
						'output parameter'
							'output parameter' [ '$' ] reference
					)
				'reference'
					'reference' [ '>' ] reference
					'output type' stategroup (
						'referenced node'
						'output parameter'
							'output parameter' [ '$' ] reference
					)
				)
	)
```

### calculated descendant node selection starting from property

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
			'referencer type' stategroup (
				'matrix' [ '>key' ]
					'output type' stategroup (
						'referenced node'
						'output parameter'
							'output parameter' [ '$' ] reference
					)
				'reference'
					'reference' [ '>' ] reference
					'output type' stategroup (
						'referenced node'
						'output parameter'
							'output parameter' [ '$' ] reference
					)
			)
	)
```

### calculated node selection starting from property

```js
'calculated node selection starting from property'
	'type' stategroup (
		'input parameter'
			'selection' component 'calculated input parameter node selection'
			'tail' component 'calculated descendant node selection starting from node'
		'this node'
			'context selection' component 'context property selection'
			'selection' component 'calculated descendant node selection starting from property'
	)
```

### calculated collection selection starting from property

```js
'calculated collection selection starting from property'
	'type' stategroup (
		'collection'
			'context selection' component 'context property selection'
			'type' stategroup (
				'dictionary' [ '.' ]
				'matrix' [ '%' ]
			)
			'collection' reference
		'node'
			'selection' component 'calculated node selection starting from property'
			'type' stategroup (
				'dictionary' [ '.' ]
				'matrix' [ '%' ]
			)
			'collection' reference
	)
```

### calculated state group selection starting from property

```js
'calculated state group selection starting from property'
	'type' stategroup (
		'state group'
			'context selection' component 'context property selection'
			'state group' [ '?' ] reference
		'node'
			'selection' component 'calculated node selection starting from property'
			'state group' [ '?' ] reference
	)
```

### node path

```js
'node path'
	'steps' component 'node path step'
```

### node path step

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
				'dictionary'
					'dictionary' [ '.' ] reference
				'matrix'
					'matrix' [ '%' ] reference
			)
			'tail' component 'node path step'
	)
```

### referencer

```js
'referencer'
	'dependable' component 'dependency'
```

### mutation permission definition

```js
'mutation permission definition'
	'role' [ '#writer' ] reference
```

### read permission definition

```js
'read permission definition'
	'role' [ '#reader' ] reference
```

### state instantiation

```js
'state instantiation'
	'state' reference
	'input arguments' collection ( [ '(' , ')' ]
		'constraint' stategroup ( 'node type' )
		'selection' [ '=>' ] component 'calculated node selection starting from property'
	)
```

### state instantiation 2

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

### conditional state group expression

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
					'expression result' [ '$' ] //NOTE: keyword '$' is temporary
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

### conditional state group expression context path

```js
'conditional state group expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional state group expression context path'
	)
```

### dictionary expression

```js
'dictionary expression'
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
			'tail' component 'dictionary expression tail'
		'plural'
			'type' stategroup ( //NOTE: for dev compatible syntax
				'dictionary' [ '.' ]
				'matrix' [ '%' ]
			)
			'collection' reference
			'elementary key' stategroup ( 'elementary key' )
			'tail' component 'dictionary expression tail'
	)
```

### dictionary expression tail

```js
'dictionary expression tail'
	'head' component 'derivation node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup ( //NOTE: for dev compatible syntax
				'dictionary' [ '.' ]
				'matrix' [ '%' ]
			)
			'collection' reference
			'elementary key' stategroup ( 'elementary key' )
			'tail' component 'dictionary expression tail'
	)
```

### node constraint

```js
'node constraint'
```

### traversed dictionary expression

```js
'traversed dictionary expression'
	'traversed head' component 'traversed derivation node content path'
	'step back' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary' [ '.^' ]
				'matrix' [ '%^' ]
			)
			'constraint' component 'node constraint'
			'tail' component 'traversed dictionary expression'
	)
```

### referencer aggregate

```js
'referencer aggregate'
	'head' component 'group context property selection'
	'type' stategroup ( //NOTE: pipe for dev compatible syntax
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
			'type' stategroup ( //NOTE: for dev compatible syntax
				'dictionary' [ '.' ]
				'matrix' [ '%' ]
			)
			'collection' reference
			'tail' component 'referencer aggregate step'
		'singular'
			'referencer type' stategroup (
				'matrix' [ '>key' ]
					'backward' stategroup ( 'backward' )
				'reference' [ '>' ]
					'reference' reference
					'backward' stategroup ( 'backward' )
			)
	)
```

### referencer aggregate step

```js
'referencer aggregate step'
	'head' component 'derivation node content path'
	'has steps' stategroup (
		'no'
			'referencer type' stategroup (
				'matrix' [ '>key' ]
					'backward' stategroup ( 'backward' )
				'reference' [ '>' ]
					'reference' reference
					'backward' stategroup ( 'backward' )
			)
		'yes'
			'type' stategroup ( //NOTE: for dev compatible syntax
				'dictionary' [ '.' ]
				'matrix' [ '%' ]
			)
			'collection' reference
			'tail' component 'referencer aggregate step'
	)
```

### numerical type constraint

```js
'numerical type constraint'
```

### numerical type conversion

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

### calculated signed number selection starting from property

```js
'calculated signed number selection starting from property'
	'sign' stategroup (
		'negative' [ '-' ]
		'positive'
	)
	'type' stategroup (
		'input parameter'
			'context selection' component 'ancestor node selection'
			'state' stategroup ( 'state' )
			'input parameter' [ '&#' ] reference
		'number from property'
			'context selection' component 'context property selection'
			'number' [ '#' ] reference
		'number from node'
			'selection' component 'calculated node selection starting from property'
			'number' [ '#' ] reference
	)
```

### signed number property list

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

### natural number property list

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

### conditional number expression context path

```js
'conditional number expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional number expression context path'
	)
```

### conditional number expression

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
							'type' [ '$' ] stategroup ( //NOTE: keyword '$' is temporary
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

### conditional natural number expression context path

```js
'conditional natural number expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional natural number expression context path'
	)
```

### conditional natural number expression

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
							'type' [ '$' ] stategroup ( //NOTE: keyword '$' is temporary
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

### integer expression

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
			'context selection' component 'entity scoped context property selection'
			'referencer anchor' [ '<' ] reference
			'filter' component 'derivation node content path'
			'number context selection' component 'entity scoped context node selection'
			'number' [ '#' ] reference
			'conversion' component 'numerical type conversion'
		'referencer anchor count' [ 'count' ]
			'context selection' component 'entity scoped context property selection'
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
		'remainder' [ 'remainder' ]
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

### natural expression

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
			'context selection' component 'entity scoped context property selection'
			'referencer anchor' [ '<' ] reference
			'filter' component 'derivation node content path'
			'number context selection' component 'entity scoped context node selection'
			'number' [ '#' ] reference
			'conversion' component 'numerical type conversion'
		'referencer anchor count' [ 'count' 'unsafe' ]
			'context selection' component 'entity scoped context property selection'
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
		'remainder' [ 'remainder' 'unsafe' ]
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

### text selection starting from property

```js
'text selection starting from property'
	'type' stategroup (
		'value'
			'value' text
		'text'
			'type' stategroup (
				'text'
					'context selection' component 'context property selection'
					'text' [ '.' ] reference
				'node'
					'selection' component 'calculated node selection starting from property'
					'text' [ '.' ] reference
			)
		'id'
			'type' stategroup (
				'ancestor'
					'selection' component 'context property selection'
				'node'
					'selection' component 'calculated node selection starting from property'
			)
			'collection type' stategroup (
				'dictionary' [ '.key' ]
			)
	)
```

### conditional text expression context path

```js
'conditional text expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional text expression context path'
	)
```

### conditional text expression

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
						'expression result' [ '$' ] //NOTE: keyword '$' is temporary
							'context type' stategroup (
								'input parameter'
									'input parameter' [ '&' ] reference
								'this state'
							)
							'selection' component 'calculated descendant node selection starting from node'
							'type' stategroup (
								'text'
									'text' [ '.' ] reference
								'id'
									'collection type' stategroup (
										'dictionary' [ '.key' ]
									)
							)
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

### text expression

```js
'text expression'
	//NOTE: result node is an ugly way to enforce a location on type==id
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

### conditional file expression context path

```js
'conditional file expression context path'
	'has steps' stategroup (
		'no'
		'yes' [ '$^' ]
			'tail' component 'conditional file expression context path'
	)
```

### conditional file expression

```js
'conditional file expression'
	'has steps' stategroup (
		'no'
			'expression context' component 'conditional file expression context path'
			'context' stategroup (
				'target context' [ '$^' ]
					'type' stategroup (
						'property'
							'context selection' component 'context property selection'
							'file' [ '/' ] reference
						'node'
							'selection' component 'calculated node selection starting from property'
							'file' [ '/' ] reference
					)
				'expression result' [ '$' ] //NOTE: keyword '$' is temporary
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

### key

```js
'key'
```

### KEYWORD

```js
'KEYWORD'
```

### node
Some examples of ui annotations:
- `@hidden`: derived properties can be hidden from the UI.
- `@description: "a description"`: describe the property in more detail to the user.
  Useful in combination with validation rules!
- `@validate: "[a-b]+"`: set a regex for text properties that defines what values are acceptable.
- `@min:` and `@max:`: set limits on a number value.
- `@identifying`: marks a property to always be displayed in addition to an entry's key.
- `@default: 'yes'`: set a default state.
- `@default: today|now`: set date or date-time number to the current time.
- `@guid`: the key or text property will be set to a generated unique id string.
- `@small`: if the collection is expected to be small, it can be displayed inline and included when duplicating.
- `@multi-line`: create a multi-line text area for this text property.

```js
'node' [ '{' , '}' ]
	'work' stategroup (
		'no'
		'yes'
			'role' [ 'workfor' ] reference
	)
	'attributes' collection (
		'preceding siblings' collection predecessors
		'type' stategroup (
			'referencer anchor'[':' 'reference-set']
				'node context' ['->'] component 'node path'
				'EQ node type' component 'EQ node type'
				'referencer type' ['=>' 'inverse'] stategroup (
					'key' ['>key' ]
					'reference'
						'reference' [ '>' ] reference
				)
			'log' [ ':' 'log' ]
				'root' component 'log node'
			'command' [ ':' 'command' ]
				'type' stategroup (
					'global'
						'ui' group (
							'visible' stategroup (
								'true' [ '@visible' ] // by default commands aren't available in the ui
								'false'
							)
						)
					'component' [ 'component' ]
				)
				'parameters' component 'command parameters'
				'implementation' stategroup (
					'external' [ 'external' ]
						'interface' [ 'from' ] reference
					'internal'
						'implementation' component 'command implementation'
				)
			'property'
				'mutation permission' stategroup (
					'inherited'
					'defined'
						'definition' component 'mutation permission definition'
				)
				'read permission' stategroup (
					'inherited'
					'defined'
						'definition' component 'read permission definition'
				)
				'data type' stategroup (
					'elementary' [ ':' ]
					'derived' [ ':=' ]
				)
				'type' stategroup (
					'group' [ 'group' ]
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
							'derived' ['=']
								'derived value' component 'derived value'
						)
						'ui' group (
							'use as namespace' stategroup (
								'no'
								'yes' [ '@namespace' ] // use as a level in breadcrumbs
							)
							'visible' stategroup (
								'true'
								'false' [ '@hidden' ]
							)
						)
						'node' component 'node'
					'reference' [ 'text' ]
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
								'referencer' [ '->' ] group (
									'type' stategroup (
										'backward'
											'backward' component 'backward selection'
											'selection' component 'resolved collection selection starting from property'
										'forward' [ 'forward' ]
											'head' component 'unresolved node selection'
											'type' stategroup (
												'dictionary' [ '.' ]
												'matrix' [ '%' ]
											)
											'collection' reference
											'constrain' stategroup (
												'no'
													'forward' component 'forward selection'
												'yes' ['/']
													'backward' component 'backward selection'
													'ancestor' component 'ancestor node selection'
													'collection constraint' reference
											)
									)
									'tail' component 'node content path'
									'bidirectional' stategroup (
										'no'
										'yes' [ '-<' ]
											'anchor' reference
									)
								)
								'record mutation time' stategroup (
									'yes' ['mutation-time']
										'meta property' ['=' '#'] reference
									'no'
								)
							'derived' ['=>']
								'derived value' component 'derived value'
								'referencer' ['(' , ')'] group (
										'type' stategroup (
											'backward'
												'backward' component 'backward selection'
												'selection' component 'calculated collection selection starting from property'
												'tail' component 'derivation node content path'
											'self'
												'forward' component 'forward selection'
												'selection' component 'ancestor node selection'
												'type' stategroup (
													'dictionary' [ '.self' ]
												)
										)
									)
									'type' stategroup (
										'dictionary branch'
											'branch' [ 'from' ] reference
											'root entity constraint' stategroup ( 'root' )
											'expression' [ '[', ']' ] component 'calculated node selection starting from property'
										'singular'
											'expression' component 'calculated node selection starting from property'
									)
						)
						'ui' group (
							'visible' stategroup (
								'true'
								'false' [ '@hidden' ]
							)
							'identifying' stategroup (
								'no'
								'yes' [ '@identifying' ]
							)
							'metadata' stategroup (
								'no'
								'yes' [ '@metadata' ]
									'value' stategroup (
										'current user'
											'constraint' component 'node constraint'
									)
							)
							'has description' stategroup (
								'no'
								'yes' [ '@description:' ]
									'description' text
							)
						)
						'output parameters' collection ( [ '(' , ')' ]
							'dependable' component 'dependency'
							'type' stategroup (
								'elementary' [ '->' ]
									'head' component 'entity scoped context node selection'
									'selection' component 'resolved node descendant selection starting from node'
								'derived' [ '=>' ]
									'head' component 'entity scoped context node selection'
									'context type' stategroup (
										'input parameter' [ '&' ]
											'input parameter' reference
										'result node'
									)
									'selection' component 'calculated descendant node selection starting from node'
							)
						)
						'referencer' component 'referencer'
					'dictionary' [ 'collection' ]
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
								'constraints' component 'constraints'
							'derived' [ '=' 'union' ]
								'derived value' component 'derived value'
								'branches' ['(', ')'] collection (
									'expression' [ '=' ] component 'dictionary expression'
								)
								'separator' ['join'] stategroup (
									'dot' ['.']
									'dash' ['-']
									'colon' [':']
									'greater than' ['>']
									'space' ['space']
								)
						)
						'key' component 'key'
						'key type' stategroup (
							'link' [ '~>' ]
								'selection' component 'link text expression'
							'simple'
						)
						'entity' component 'entity'
						'ui' group (
							'visible' stategroup (
								'true'
								'false' [ '@hidden' ]
							)
							'default' stategroup (
								'guid' [ '@guid' ]
								'none'
							)
							'has validation' stategroup (
								'no'
								'yes' [ '@validate:' ]
									'rules' component 'ui text validation'
							)
							'size' stategroup (
								'small' [ '@small' ]
								'large'
							)
							'can be dormant' stategroup (
								'no'
								'yes' [ '@dormant' ]
									'context' component 'node content path'
									'state group' [ '?' ] reference
									'dormant state' [ '|' ] reference
							)
							'has description' stategroup (
								'no'
								'yes' [ '@description:' ]
									'description' text
							)
							'has key description' stategroup (
								'no'
								'yes' [ '@key-description:' ]
									'description' text
							)
							'linked node mapping' stategroup (
								'none'
								'from linked entry' [ '@linked-node-mapping' ]
									'context node selection' component 'entity scoped context node selection'
									'mapping' component 'ui linked node mapping'
							)
						)
						'node' component 'node'
					'matrix' [ 'collection' ]
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
								'referencer' [ '->' ] group (
									'type' stategroup (
										'backward'
											'backward' component 'backward selection'
											'selection' component 'resolved collection selection starting from property'
										'forward' [ 'forward' ]
											'head' component 'unresolved node selection'
											'type' stategroup (
												'dictionary' [ '.' ]
												'matrix' [ '%' ]
											)
											'collection' reference
											'constrain' stategroup (
												'no'
													'forward' component 'forward selection'
												'yes'['/']
													'backward' component 'backward selection'
													'ancestor selection' component 'ancestor node selection' //TODO: remove
													'collection constraint' reference
											)
									)
									'tail' component 'node content path'
									'elementary' stategroup ( 'elementary' )
									'bidirectional' stategroup (
										'no'
										'yes' [ '-<' ]
											'anchor' reference
									)
								)
								'constraints' component 'constraints'
							'derived'
								'derived value' component 'derived value'
								'referencer' [ '=>' ] group (
									'type' stategroup (
										'backward'
											'backward' component 'backward selection'
											'selection' component 'calculated collection selection starting from property'
									)
									'tail' component 'derivation node content path'
								)
								'type' stategroup (
									'augment'
									'merge' [ 'in' ]
										'aggregates' [ '(' , ')' ] collection (
											'aggregate' [ '=>' ] component 'referencer aggregate'
										)
								)
						)
						'ui' group (
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
									'context' component 'node content path'
									'state group' [ '?' ] reference
									'dormant state' [ '|' ] reference
							)
							'has description' stategroup (
								'no'
								'yes' [ '@description:' ]
									'description' text
							)
						)
						'output parameters' collection ( [ '(' , ')' ]
							'dependable' component 'dependency'
							'type' stategroup (
								'elementary' [ '->' ]
									'head' component 'entity scoped context node selection'
									'selection' component 'resolved node descendant selection starting from node'
								'derived' [ '=>' ]
									'head' component 'entity scoped context node selection'
									'context type' stategroup (
										'input parameter' [ '&' ]
											'input parameter' reference
										'result node'
									)
									'selection' component 'calculated descendant node selection starting from node'
							)
						)
						'referencer' component 'referencer'
						'entity' component 'entity'
						'node' component 'node'
					'number'
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
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
													'reference' [ '>' ]
														'reference' reference
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
													'subtract lifetime' [ 'subtract' 'life-time' ] //TODO: drop? we don't need this.
												)
												'watched stategroup' ['?'] reference
												'watched state' ['|'] reference
										)
									'simple'
										'record mutation time' stategroup ( //TODO: use triggers instead, to set mutation time with 'now'?
											'yes' ['mutation-time']
												'meta property' ['=' '#'] reference
											'no'
										)
								)
							'derived'
								'derived value' component 'derived value'
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
							'timer' [ 'timer']
								'timeout operation node' [ 'ontimeout' ] component 'context node selection'
								'timeout operation' [ 'update' ] component 'update node'
						)
						'ui' group (
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
								'yes'
									'value' stategroup (
										'today' [ '@default:' 'today' ]
										'now' [ '@default:' 'now' ]
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
						)
					'file' ['file']
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
							'derived' [ '=' ]
								'derived value' component 'derived value'
								'type' stategroup (
									'singular'
										'type' stategroup (
											'property'
												'context selection' component 'context property selection'
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
						'ui' group (
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
						)
					'text' ['text']
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
								'record mutation time' stategroup (
									'yes' ['mutation-time']
										'meta property' ['=' '#'] reference
									'no'
								)
							'derived'
								'derived value' component 'derived value'
								'expression' [ '=' ] component 'text expression'
						)
						'value type' stategroup (
							'link' [ '~>' ]
								'selection' component 'link text expression'
							'simple'
						)
						'ui' group (
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
						)
					'state group' [ 'stategroup' ]
						'type' stategroup (
							'elementary'
								'elementary value' component 'elementary value'
							'derived' ['=']
								'derived value' component 'derived value'
								'expression type' stategroup (
									'resolvable link' [ 'any' ]
										'link context selection' ['('] component 'context property selection'
										'link type' stategroup (
											'text'
												'text' [ '>' ] reference
											'key' [ '>key' ]
										)
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
														'entity node selection' component 'entity scoped context node selection'
														'selection' component 'calculated descendant node selection starting from node'
												)
											)
										)
										'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
										'KEYWORD2' [')'] component 'KEYWORD'
									'dictionary branch' [ 'match-branch' ]
										'branches' ['(', ')'] collection ( ['|']
											'state instantiation' [ '=' ] group (
												'state' reference
												'input arguments' collection ( [ '(' , ')' ]
													'type' [ '=>' ] stategroup (
														'target context'
															'selection' component 'calculated node selection starting from property'
														'expression result' [ '$' ]
															'expression context path' component 'traversed dictionary expression'
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
									'matrix contains' ['any' '(']
										'collection selection' component 'calculated collection selection starting from property'
										'matrix' stategroup ( 'matrix' )
										'key' [ '[' ,']' ] component 'calculated node selection starting from property'
										'yes state instantiation' [ ')' '(' '|' 'true' '=' ] component 'state instantiation 2'
										'no state instantiation' [ '|' 'false' '=' ] component 'state instantiation'
										'KEYWORD' [')'] component 'KEYWORD'
									'node equality' ['match' '(']
										'left node type' stategroup (
											'ancestor'
												'selection' component 'ancestor node selection'
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
										'aggregate' [ '(' , ')' ] group ( //TODO: remove this group
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
										'yes state instantiation' [ '|' 'false' '=' ] component 'state instantiation' //NOTE: no = yes, and yes = no for syntax migration.
										'KEYWORD' [')'] component 'KEYWORD'
								)
						)
						'ui' group (
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
									'state' reference
							)
							'has description' stategroup (
								'no'
								'yes' [ '@description:' ]
									'description' text
							)
						)
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
											'ancestor' [ '?^' ]
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
											'ancestor' [ '?^' ]
												'selection' component 'calculated node selection starting from property'
										)
								)
							)
							'ui' group (
								'desired state' stategroup (
									'no'
									'yes' [ '@desired' ]
								)
								'verified state' stategroup (
									'no'
									'yes' [ '@verified' ]
								)
							)
							'node' component 'node'
						)
				)
		)
	)
```

### EQ node type

```js
'EQ node type'
```

### link text expression

```js
'link text expression'
	'dependency' stategroup (
		'link'
			'context selection' component 'context property selection'
			'link type' stategroup (
				'text'
					'text' [ '.' ] reference //TODO: use > (ambiguous right now)
				'key' [ '.key' ] //TODO: use >key (ambiguous right now)
					'dictionary' stategroup ( 'dictionary' )
			)
			'group selection' component 'group node selection'
			'type' stategroup (
				'dictionary' [ '.' ]
					'dictionary' reference
				'matrix' [ '%' ]
					'matrix' reference
			)
		'node'
			'collection selection' component 'calculated collection selection starting from property'
	)
	'tail' component 'derivation node content path'
```

### link text expression context path

```js
'link text expression context path'
	'has steps' stategroup (
		'no' [ '$' ]
		'yes' [ '$^' ]
			'tail' component 'link text expression context path'
	)
```

### log node

```js
'log node' [ '(' , ')' ]
	'properties' collection (
		'type' [ ':' ] stategroup (
			'group' [ 'group' ]
				'node' component 'log node'
			'number' [ 'number' ]
			'reference' [ 'reference' ]
			'state group' [ 'stategroup' ]
				'states' [ '(' , ')' ] collection (
					'node' component 'log node'
				)
			'text' [ 'text' ]
			'file' ['file']
		)
	)
```

### delete node

```js
'delete node'
```

### new collection entries

```js
'new collection entries'
	'entries' collection (
		'node' component 'initialize node'
	)
```

### initialize node

```js
'initialize node' [ '(' , ')' ]
	'groups' collection (
		'node' [ ':' 'group' ] component 'initialize node'
	)
	'files' collection (
		'token' [':' 'file'] text
		'extension' text
	)
	'texts' collection (
		'value' [ ':' 'text' ] text
	)
	'numbers' collection (
		'type' [ ':' ] stategroup (
			'natural' [ 'natural' ]
				'value' number
			'integer' [ 'integer' ]
				'value' number
		)
	)
	'references' collection (
		'referenced node' [ ':' 'reference' ] text
	)
	'state groups' collection (
		'state' [ ':' 'stategroup' ] reference
		'node' component 'initialize node'
	)
	'dictionaries' collection (
		'entries' [ ':' 'dictionary' ] component 'new collection entries'
	)
	'matrices' collection (
		'entries' [ ':' 'matrix' ] component 'new collection entries'
	)
```

### update node

```js
'update node' [ '(' , ')' ]
	'properties' collection (
		'type' [ ':' ] stategroup (
			'collection'
				'type' stategroup (
					'dictionary' [ 'dictionary' ]
					'matrix' [ 'matrix' ]
				)
				'entries' collection (
					'type' stategroup (
						'rename' [ 'rename' ]
							'old id' [ 'from' ] reference
						'create' [ 'create' ]
							'node' component 'initialize node'
						'update' [ 'update' ]
							'invalidate referencer' stategroup (
								'no'
								'yes' [ 'invalidate' 'referencer' ]
							)
							'update node' component 'update node'
						'remove' [ 'remove' ]
							'delete node' component 'delete node'
					)
				)
			'group' [ 'group' ]
				'update node' component 'update node'
			'number'
				'type' stategroup (
					'natural' [ 'natural' ]
						'new value' number
					'integer' [ 'integer' ]
						'new value' number
				)
			'reference' [ 'reference' ]
				'new referenced node' text
			'state group' [ 'stategroup' ]
				'state' ['='] reference
				'type' stategroup (
					'set'
						'node' component 'initialize node'
						'delete node' component 'delete node'
					'update' [ 'update' ] //TODO: move 'state' here.
						'update node' component 'update node'
				)
			'text' [ 'text' ]
				'new value' text
			'file' ['file']
				'new token' text
				'new extension' ['.'] text
		)
	)
```

### creation context

```js
'creation context'
```

### creation

```js
'creation'
	'context' component 'creation context'
```

### command implementation

```js
'command implementation' ['do']
	'conditional' stategroup (
		'yes'
			'type' stategroup (
				'state switch' [ 'switch' '(' ]
					'state group' [ '@' , ')' ] reference
					'states' [ '(' , ')' ] collection ( ['|']
						'implementation' component 'command implementation'
					)
				'contains switch' ['any' '(']
					'context node path' component 'unconstrained node selection path'
					'type' stategroup (
						'dictionary'
							'dictionary' [ '.' ] reference
							'type' [ '[' , ']' ] stategroup (
								'text'
									'text' ['@'] reference
								'reference'
									'reference' ['@'] reference
									'context node' component 'command parameter entity scoped context node selection'
									'dictionary' [ '.key' ] group ( )
							)
					)
					'yes case' [ ')' '(' '|' 'true' ] component 'command implementation'
					'no case' [ '|' 'false' ] component 'command implementation'
					'KEYWORD' [')'] component 'KEYWORD'
			)
		'no'
			'target' [ 'on' ] stategroup (
				'parameter'
					'parameter' [ '@' ] reference
				'context node'
					'context node path' component 'unconstrained node selection path'
			)
			'no creation context' component 'creation context'
			'update node' component 'parametrized update node'
	)
```

### node status

```js
'node status'
```

### command parameters

```js
'command parameters' [ '{' , '}' ]
	'properties' collection indent (
		'preceding siblings' collection predecessors
		'type' [ ':' ] stategroup (
			'matrix'
				'type' stategroup (
					'dense' [ 'collection' 'dense' ]
					'sparse' [ 'collection' 'sparse' ]
				)
				'referencer' [ '->' ] component 'command parameter referencer'
				'ui' group (
					'has description' stategroup (
						'no'
						'yes' [ '@description:' ]
							'description' text
					)
				)
				'parameters' component 'command parameters'
			'reference' [ 'text' ]
				'referencer' [ '->' ] component 'command parameter referencer'
				'ui' group (
					'metadata' stategroup (
						'no'
							'sticky' stategroup (
								'yes' [ '@sticky' ]
								'no'
							)
						'yes' [ '@metadata' ]
							'constraint' component 'node constraint'
					)
					'has description' stategroup (
						'no'
						'yes' [ '@description:' ]
							'description' text
					)
				)
			'number'
				'set' stategroup (
					'integer' [ 'integer' ]
					'natural' [ 'natural' ]
				)
				'numerical type' reference
				'ui' group (
					'sticky' stategroup (
						'yes' [ '@sticky' ]
						'no'
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
				)
			'text' [ 'text' ]
				'ui' group (
					'default' stategroup (
						'none'
						'sticky' stategroup (
							'yes' [ '@sticky' ]
							'no'
						)
						'guid' [ '@guid' ]
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
				)
			'file' ['file']
				'ui' group (
					'has description' stategroup (
						'no'
						'yes' [ '@description:' ]
							'description' text
					)
				)
			'state group' [ 'stategroup' ]
				'ui' group (
					'default state' stategroup (
						'no'
						'sticky' stategroup (
							'yes' [ '@sticky' ]
							'no'
						)
						'yes' [ '@default:' ]
							'state' reference
					)
					'has description' stategroup (
						'no'
						'yes' [ '@description:' ]
							'description' text
					)
				)
				'has states' stategroup has 'states' first 'first' 'yes' 'no'
				'states' [ '(' , ')' ] collection order 'view order' (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'parameters' component 'command parameters'
				)
		)
	)
```

### context command parameters selection

```js
'context command parameters selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state parent' [ '@?^' ]
				'matrix parent' [ '@%^' ]
			)
			'tail' component 'context command parameters selection'
	)
```

### context command parameter selection starting from parameter

```js
'context command parameter selection starting from parameter'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state parent' [ '?^' ]
				'matrix parent' [ '%^' ]
			)
			'tail' component 'context command parameter selection starting from parameter'
	)
```

### command parameter referencer

```js
'command parameter referencer'
	'node status' stategroup (
		'new' [ 'new' ]
			'node status' component 'node status'
		'existing'
	)
	'context type' stategroup (
		'command parameter'
			'selection' component 'context command parameter selection starting from parameter'
			'type' stategroup (
				'sibling' [ '$' ]
					'reference' [ '>' ] reference
				'ancestor' [ '$' '>key' ]
			)
		'context node'
			'node status' component 'node status'
	)
	'head' component 'derivation selection path'
	'type' stategroup (
		'dictionary' [ '.' ]
			'dictionary' reference
		'matrix' [ '%' ]
			'matrix' reference
	)
	'tail' component 'derivation node content path'
```

### command parameter entity scoped context node selection

```js
'command parameter entity scoped context node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
				'matrix key' [ '>key' ]
			)
			'tail' component 'command parameter entity scoped context node selection'
	)
```

### parametrized unconstrained node selection path

```js
'parametrized unconstrained node selection path'
	'context' stategroup (
		'this' [ '$' ]
		'command'
		'parameter'
			'selection' component 'context command parameters selection'
			'parameter' [ '@' ] reference
	)
	'path' component 'unconstrained node selection path'
```

### type eq

```js
'type eq'
```

### parametrized number expression

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
		'unary expression'
			'type' stategroup (
				'natural to integer cast' ['(' 'integer' ')']
					'expression' component 'parametrized number expression'
			)
		'property'
			'path' component 'parametrized unconstrained node selection path'
			'number' [ '#' ] reference
		'argument'
			'path' component 'context command parameters selection'
			'number' [ '@' ] reference
		'current timestamp' [ 'now' ]
		'static'
			'value' stategroup (
				'zero' [ 'zero' ]
				'one' [ 'one' ]
			)
	)
```

### command arguments

```js
'command arguments' [ '(' , ')' ]
	'properties' collection (
		'type' [ ':' ] stategroup (
			'matrix' [ 'collection' ]
				'source' ['=>'] stategroup (
					'argument'
						'selection' component 'context command parameters selection'
						'matrix' [ '@' ] reference
						'context selection' component 'command parameter entity scoped context node selection'
						'arguments' component 'command arguments'
					'property'
						'context' stategroup (
							'this' [ '$' ]
								'path' component 'unconstrained node selection path'
								'matrix' [ '%' ] reference
								'context selection' component 'command parameter entity scoped context node selection'
								'arguments' component 'command arguments'
							'calling command'
								'path' component 'unconstrained node selection path'
								'matrix' [ '%' ] reference
								'context selection' component 'command parameter entity scoped context node selection'
								'arguments' component 'command arguments'
						)
				)
			'reference' [ 'text' ]
				'source' ['=>'] stategroup (
					'created entry' [ 'created' 'entry' ]
						'entry' stategroup (
							'ancestor' [ '.^' ]
								'context selection' component 'ancestor node selection'
							'context'
								'type' stategroup (
									'this'
									'descendant'
										'parent reference' [ '$' '>' ] reference
										'head state constraint' component 'node content constraint'
										'type' stategroup (
											'dictionary'
												'dictionary' [ '.' ] reference
											'matrix'
												'matrix' [ '%' ] reference
										)
								)
								'node constraint' component 'node content constraint'
						)
					'new entry argument'
						'selection' component 'context command parameters selection'
						'reference' [ '@' 'new' ] reference
						'context node' component 'command parameter entity scoped context node selection'
					'node'
						'path' component 'parametrized unconstrained node selection path'
				)
			'number'
				'type' stategroup (
					'integer' [ 'integer' ]
					'natural' [ 'natural' ]
				)
				'expression' ['='] component 'parametrized number expression'
			'text' [ 'text' ]
				'source' ['='] stategroup (
					'argument'
						'selection' component 'context command parameters selection'
						'text' [ '@' ] reference
					'property'
						'path' component 'parametrized unconstrained node selection path'
						'type' stategroup (
							'text'
								'text' [ '.' ] reference
							'id' [ '.key' ]
						)
				)
			'file' ['file']
				'source' ['='] stategroup (
					'argument'
						'selection' component 'context command parameters selection'
						'file' [ '@' ] reference
					'property'
						'path' component 'parametrized unconstrained node selection path'
						'file' [ '/' ] reference
				)
			'state group' [ 'stategroup' ]
				'source' ['='] stategroup (
					'fixed'
						'state' reference
						'arguments' component 'command arguments'
					'property' ['switch']
						'context' stategroup (
							'this' [ '(' ]
								'path' ['$'] component 'unconstrained node selection path'
								'state group' ['?', ')'] reference
								'mapping' ['(', ')'] collection ( ['|']
									'mapped state' ['='] reference
									'arguments' component 'command arguments'
								)
							'calling command' [ '(' ]
								'path' component 'unconstrained node selection path'
								'state group' ['?' , ')'] reference
								'mapping' ['(', ')'] collection ( ['|']
									'mapped state' ['='] reference
									'arguments' component 'command arguments'
								)
						)
					'argument' ['switch']
						'selection' ['('] component 'context command parameters selection'
						'state group' ['@', ')'] reference
						'mapping' ['(', ')'] collection ( ['|']
							'mapped state' ['='] reference
							'arguments' component 'command arguments'
						)
				)
		)
	)
```

### node content constraint

```js
'node content constraint'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'node content constraint'
	)
```

### parametrized update node

```js
'parametrized update node' [ '(' , ')' ]
	'attributes' collection indent (
		'type' stategroup (
			'command'
				'arguments' [ 'with' ] component 'command arguments'
			'property' [ ':' ]
				'type' stategroup (
					'collection'
						'type' stategroup (
							'dictionary' ['dictionary']
								'type' stategroup (
									'create' [ 'create' ]
										'key source' stategroup (
											'argument'
												'selection' component 'context command parameters selection'
												'text' [ '@' ] reference
											'node'
												'path' component 'parametrized unconstrained node selection path'
												'dictionary' [ '.key' ] stategroup ( 'dictionary' )
										)
										'initialize node' component 'parametrized initialize node'
										'has update block' stategroup (
											'no'
											'yes' ['and' 'on']
												'path' component 'parametrized unconstrained node selection path'
												'creation' component 'creation'
												'update node' component 'parametrized update node'
										)
									'delete' ['delete']
										'selection' component 'context command parameters selection'
										'entry' [ '@' ] reference
										'delete node' component 'delete node'
								)
							'matrix' ['matrix']
								'type' stategroup (
									'create' [ 'create' ]
										'selection' component 'context command parameters selection'
										'reference' [ '@' ] reference
										'context node' component 'command parameter entity scoped context node selection'
										'initialize node' component 'parametrized initialize node'
										'has update block' stategroup (
											'no'
											'yes' ['and' 'on']
												'path' component 'parametrized unconstrained node selection path'
												'creation' component 'creation'
												'update node' component 'parametrized update node'
										)
									'delete' ['delete']
										'selection' component 'context command parameters selection'
										'entry' ['@'] reference
										'delete node' component 'delete node'
								)
						)
					'number'
						'set' stategroup (
							'integer' [ 'integer' ]
							'natural' [ 'natural' ]
						)
						'operator' stategroup (
							'increment' [ 'increment' ]
							'add'
								'selection' [ 'add' ] component 'context command parameters selection'
								'number' [ '@' ] reference
							'subtract'
								'selection' [ 'subtract' ] component 'context command parameters selection'
								'number' [ '@' ] reference
							'assignment'
								'expression' ['='] component 'parametrized number expression'
						)
					'text' [ 'text' ]
						'source' ['='] stategroup (
							'argument'
								'selection' component 'context command parameters selection'
								'text' [ '@' ] reference
							'property'
								'path' component 'parametrized unconstrained node selection path'
								'type' stategroup (
									'text'
										'text' [ '.' ] reference
									'id' [ '.key' ]
								)
						)
					'file' ['file']
						'source' ['='] stategroup (
							'argument'
								'selection' component 'context command parameters selection'
								'file' [ '@' ] reference
							'property'
								'path' component 'parametrized unconstrained node selection path'
								'file' [ '/' ] reference
						)
					'group' [ 'group' ]
						'update node' component 'parametrized update node'
					'reference' [ 'text' ]
						'source' ['=>'] stategroup (
							'new entry argument'
								'selection' component 'context command parameters selection'
								'reference' [ '@' 'new' ] reference
								'context node' component 'command parameter entity scoped context node selection'
							'node'
								'path' component 'parametrized unconstrained node selection path'
							'created entry' [ 'created' 'entry' ]
								'entry' stategroup (
									'ancestor' [ '.^' ]
										'context selection' component 'ancestor node selection'
									'context'
										'type' stategroup (
											'this'
											'descendant'
												'parent reference' [ '$' '>' ] reference
												'head state constraint' component 'node content constraint'
												'type' stategroup (
													'dictionary'
														'dictionary' [ '.' ] reference
													'matrix'
														'matrix' [ '%' ] reference
												)
										)
										'node constraint' component 'node content constraint'
								)
						)
					'state group' [ 'stategroup' ]
						'type' stategroup (
							'setto or update' ['=']
								'state' reference
								'node' component 'parametrized initialize node'
								'delete node' component 'delete node'
							'map' ['=' 'switch']
								'source' stategroup (
									'argument'
										'selection' ['('] component 'context command parameters selection'
										'state group parameter' [ '@' , ')' ] reference
										'mapping' [ '(' , ')' ] collection ( ['|']
											'state' [ '=' ] reference
											'node' component 'parametrized initialize node'
										)
									'property'
										'context' stategroup (
											'argument'
												'selection' [ '(' ] component 'context command parameters selection'
												'reference' [ '@' , ')' ] reference
												'path' component 'unconstrained node selection path'
												'state group' ['?'] reference
												'mapping' ['(', ')'] collection ( ['|']
													'state' [ '=' ] reference
													'initialize node' component 'parametrized initialize node'
												)
											'update'
												'path' [ '(' '$' ] component 'unconstrained node selection path'
												'state group' ['?' , ')'] reference
												'mapping' ['(', ')'] collection ( ['|']
													'state' [ '=' ] reference
													'initialize node' component 'parametrized initialize node'
												)
											'command'
												'path' ['('] component 'unconstrained node selection path'
												'state group' ['?', ')'] reference
												'mapping' ['(', ')'] collection ( ['|']
													'state' [ '=' ] reference
													'initialize node' component 'parametrized initialize node'
												)
										)
								)
								'delete node' component 'delete node'
							'update'
								'states' [ '(' , ')' ] collection indent ( ['|']
									'preceding states' collection predecessors
									'succeeding states' collection successors
									'action' stategroup (
										'setto' [ '=' ]
											'type' stategroup (
												'preceding state'
													'state' reference
												'succeeding state' [ 'forward' ]
													'state' reference
											)
											'initialize node' component 'parametrized initialize node'
										'update'
											'update node' component 'parametrized update node'
										'ignore' ['ignore']
									)
								)
						)
				)
		)
	)
```

### parametrized initialize node

```js
'parametrized initialize node' [ '(' , ')' ]
	'groups' collection indent (
		'initialize node' [ ':' 'group' ] component 'parametrized initialize node'
	)
	'texts' collection indent (
		'source' [ ':' 'text' '=' ] stategroup (
			'argument'
				'selection' component 'context command parameters selection'
				'text' [ '@' ] reference
			'property'
				'path' component 'parametrized unconstrained node selection path'
				'type' stategroup (
					'text'
						'text' [ '.' ] reference
					'id' [ '.key' ]
				)
		)
	)
	'files' collection indent (
		'source' [ ':' 'file' '=' ] stategroup (
			'argument'
				'selection' component 'context command parameters selection'
				'file' [ '@' ] reference
			'property'
				'path' component 'parametrized unconstrained node selection path'
				'file' [ '/' ] reference
		)
	)
	'matrices' collection (
		'source' [ ':' 'matrix' '=' ] stategroup (
			'empty'
			'argument'
				'type' stategroup (
					'reference'
						'selection' component 'context command parameters selection'
						'reference' [ '@' ] reference
						'context node' component 'command parameter entity scoped context node selection'
						'initialize node' component 'parametrized initialize node'
					'matrix'
						'selection' component 'context command parameters selection'
						'matrix' [ '@' '.' ] reference
						'context node' component 'command parameter entity scoped context node selection'
						'initialize node' component 'parametrized initialize node'
				)
		)
	)
	'dictionaries' collection (
		'source' [ ':' 'dictionary' '=' ] stategroup (
			'empty'
			'entry'
				'key source' stategroup (
					'argument'
						'selection' component 'context command parameters selection'
						'text' [ '@' ] reference
					'node'
						'path' component 'parametrized unconstrained node selection path'
						'dictionary' [ '.key' ] stategroup ( 'dictionary' )
				)
				'initialize node' component 'parametrized initialize node'
			'collection'
				'selection' component 'context command parameters selection'
				'matrix' [ '@' '.' ] reference
				'context node' component 'command parameter entity scoped context node selection'
				'initialize node' component 'parametrized initialize node'
		)
	)
	'numbers' collection indent (
		'set' stategroup (
			'integer' [ ':' 'integer' ]
			'natural' [ ':' 'natural' ]
		)
		'expression' [ '=' ] component 'parametrized number expression'
	)
	'references' collection indent (
		'source' [ ':' 'text' '=>' ] stategroup (
			'new entry argument'
				'selection' component 'context command parameters selection'
				'reference' [ '@' 'new' ] reference
				'context node' component 'command parameter entity scoped context node selection'
			'new entry' ['new' 'entry']
				'type' stategroup (
					'dictionary' ['.']
						'dictionary' reference
					'matrix' ['%']
						'matrix' reference
				)
				'node constraint' component 'node content constraint'
			'node'
				'path' component 'parametrized unconstrained node selection path'
			'created entry' ['created' 'entry']
				'entry' stategroup (
					'ancestor' [ '.^' ]
						'context selection' component 'ancestor node selection'
					'context'
						'type' stategroup (
							'this'
							'descendant' [ '$' ]
								'parent reference' [ '>' ] reference
								'head state constraint' component 'node content constraint'
								'type' stategroup (
									'dictionary'
										'dictionary' [ '.' ] reference
									'matrix'
										'matrix' [ '%' ] reference
								)
						)
						'node constraint' component 'node content constraint'
				)
		)
	)
	'state groups' collection indent (
		'source' [ ':' 'stategroup' '=' ] stategroup (
			'argument' ['switch']
				'selection' ['('] component 'context command parameters selection'
				'state group' [ '@' ] reference
				'KEYWORD' [')'] component 'KEYWORD'
				'states' [ '(' , ')' ] collection indent ( ['|']
					'state' [ '=' ] reference
					'initialize node' component 'parametrized initialize node'
				)
			'property' ['switch']
				'context' stategroup (
					'argument'
						'selection' ['('] component 'context command parameters selection'
						'reference' [ '@' ] reference
						'path' component 'unconstrained node selection path'
						'state group' [':'] reference
						'KEYWORD' [')'] component 'KEYWORD'
						'mapping' ['(', ')'] collection ( ['|']
							'state' ['='] reference
							'initialize node' component 'parametrized initialize node'
						)
					'update'
						'path' ['(' '$'] component 'unconstrained node selection path'
						'state group' ['?'] reference
						'KEYWORD' [')'] component 'KEYWORD'
						'mapping' ['(', ')'] collection ( ['|']
							'state' ['='] reference
							'initialize node' component 'parametrized initialize node'
						)
					'command'
						'path' ['('] component 'unconstrained node selection path'
						'state group' ['?'] reference
						'KEYWORD' [')'] component 'KEYWORD'
						'mapping' ['(', ')'] collection ( ['|']
							'state' ['='] reference
							'initialize node' component 'parametrized initialize node'
						)
				)
			'fixed'
				'state' reference
				'initialize node' component 'parametrized initialize node'
		)
	)
```

### unconstrained node selection path

```js
'unconstrained node selection path'
	'context' stategroup (
		'this node'
			'context selection' component 'context node selection'
		'output parameter'
			'context selection' component 'context node selection'
			'type' stategroup (
				'state group output parameter'
					'state group' [ '?' ] reference
					'output parameter' [ '$' ] reference
				'referencer output'
					'referencer type' stategroup (
						'matrix' [ '>key' ]
						'output type' stategroup (
							'referenced node'
							'output parameter'
								'output parameter' [ '$' ] reference
						)
						'reference' [ '>' ]
							'reference' reference
							'output type' stategroup (
								'referenced node'
								'output parameter'
									'output parameter' [ '$' ] reference
							)
					)
			)
		'input parameter'
			'context node selection' component 'context node selection'
			'type' stategroup (
				'state' [ '&' ]
					'input parameter' reference
			)
			'tail' component 'context node selection'
	)
```

### ui text validation

```js
'ui text validation'
	'regular expression' text
```

### ui number limit

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

### ui file name expression

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
						'text' [ ':' ]
							'text' reference
						'number' [ '#' ]
							'number' reference
						'dictionary key' [ '.}' ]
						'matrix key' [ '%}' ]
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

### ui linked node mapping path

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

### ui linked node mapping

```js
'ui linked node mapping' [ '(' , ')' ]
	'properties' collection indent (
		'type' stategroup (
			'number' [ 'number' '<-' ]
				'path' component 'ui linked node mapping path'
				'number' reference
			'text' [ 'text' '<-' ]
				'path' component 'ui linked node mapping path'
				'copy from' stategroup (
					'text'
						'source text' reference
					'reference' [ '>' ]
						'source reference' reference
				)
			'file' [ 'file' '<-' ]
				'path' component 'ui linked node mapping path'
				'file' reference
			'reference' [ 'reference' '<-' ]
				'path' component 'ui linked node mapping path'
				'copy from' stategroup (
					'text'
						'source text' reference
					'reference' [ '>' ]
						'source reference' reference
				)
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
			'dictionary' [ 'dictionary' ]
		)
	)
```
