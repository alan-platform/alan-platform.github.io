---
layout: doc
origin: model
language: application
version: 40
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
		'users collection' [ '.' ] reference
		'password node' ['password' ':'] component 'node content path'
		'password property' [ '.' ] reference
)
```

### imported interfaces

```js
'imported interfaces' ['interfaces'] collection indent (
	'modifier' component 'modifier'
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

### direction

```js
'direction' group (
	'backward' component 'direction type'
	'forward' component 'direction type'
)
```

### undefined output parameters

```js
'undefined output parameters' component 'output parameters'
```

### undefined direction

```js
'undefined direction' component 'direction type'
```

### undefined link

```js
'undefined link' component 'link'
```

### undefined reference

```js
'undefined reference' component 'reference'
```

### unassigned variable

```js
'unassigned variable' component 'variable'
```

### undefined parameter

```js
'undefined parameter' component 'parameter'
```

### undefined member

```js
'undefined member' component 'member'
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
'type' component 'type'
```

### dependable

```js
'dependable' component 'dependency'
```

### entity

```js
'entity' component 'entity'
```

### root member

```js
'root member' component 'member'
```

### root

```js
'root' [ 'root' ] component 'node'
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

### dependency

```js
'dependency'
```

### graph constraints definition

```js
'graph constraints definition'
	'constraints' collection (
		'type' [':'] stategroup (
			'acyclic' [ 'acyclic-graph' ]
			'linear' [ 'ordered-graph' ]
		)
	)
```

### direction type

```js
'direction type'
```

### modifier

```js
'modifier'
```

### EQ modifier

```js
'EQ modifier'
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

### member

```js
'member'
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
		'collection'
			'context selection' component 'context property selection'
			'collection' [ '.' ] reference
		'node'
			'selection' component 'resolved node selection starting from property'
			'collection' [ '.' ] reference
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
				'text' [ '>' ] reference
				'is backward' stategroup ( 'is backward' )
				'output type' stategroup (
					'referenced node'
					'output parameter'
						'output parameter' [ '$' ] reference
				)
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
					'text' [ '>' ] reference
					'is forward' stategroup ( 'is forward' )
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
				'collection parent' [ '.^' ]
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
				'collection parent' [ '.^' ]
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
				'collection parent' [ '.^' ]
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
			'text' [ '>' ] reference
			'dereference' component 'dereference'
			'output type' stategroup (
				'referenced node'
				'output parameter'
					'output parameter' [ '$' ] reference
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
			'text' [ '>' ] reference
			'dereference' component 'dereference'
			'output type' stategroup (
				'referenced node'
				'output parameter'
					'output parameter' [ '$' ] reference
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
			'collection' ['.'] reference
		'node'
			'selection' component 'calculated node selection starting from property'
			'collection' ['.'] reference
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
				'collection'
					'collection' [ '.' ] reference
			)
			'tail' component 'node path step'
	)
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

### state expression

```js
'state expression'
	'expression type' stategroup (
		'resolvable link' [ 'any' ]
			'link context selection' ['('] component 'context property selection'
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
							'entity node selection' component 'entity scoped context node selection'
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
```

### flatten expression

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

### flatten expression tail

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

### traversed flatten expression

```js
'traversed flatten expression'
	'traversed head' component 'traversed derivation node content path'
	'step back' stategroup (
		'no'
		'yes' ['.^']
			'constraint' component 'EQ node type'
			'tail' component 'traversed flatten expression'
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
			'collection' ['.'] reference
			'tail' component 'referencer aggregate step'
		'singular'
			'text'[ '>' ] reference
			'dereference' component 'dereference'
			'is backward' component 'EQ direction'
	)
```

### referencer aggregate step

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
// 'key'
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
				'parameters root entity' component 'entity'
				'parameters' component 'parameter definition'
				'implementation' stategroup (
					'external' [ 'external' ]
						'interface' [ 'from' ] reference
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
						'ui' group (
							'use as namespace' stategroup (
								'no'
								'yes' [ '@namespace' ] // use as a level in breadcrumbs
							)
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
						)
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
						'ui' group (
							'sort' stategroup (
								'no'
								'yes'
									'direction' stategroup (
										'ascending' ['@ascending:']
										'descending' ['@descending:']
									)
									'property context' ['(',')'] component 'ui conditional path'
									'type' stategroup (
										'text' [':'] // TODO: fix inconsistent grammar
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
									'context' component 'node content path'
									'state group' [ '?' ] reference
									'dormant state' [ '|' ] reference
							)
							'has description' stategroup (
								'no'
								'yes' [ '@description:' ]
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
										'one' [ '@default:' 'one' ]
										'zero' [ '@default:' 'zero' ]
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
							'derived' [ '=' ]
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
							'default value' stategroup (
								'no'
								'yes' [ '@default:' ]
									'source' stategroup (
										'property'
											'context node' component 'context node selection'
											'property' [ '.' ] reference
										'current user' ['user'] // NOTE: syntax change from @metadata
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
						)
					'state group' [ 'stategroup' ]
						'type' stategroup (
							'elementary'
							'derived' ['=']
								'expression' component 'state expression'
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
							'permissions' component 'item permissions definition'
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
		'attribute' component 'member'
	)
```

### output parameters

```js
'output parameters'
```

### output parameters definition

```js
'output parameters definition'
	'parameters' component 'output parameters'
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
```

### linker

```js
'linker'
	'link' component 'link'
```

### referencer

```js
'referencer'
	'dependable' component 'dependency'
	'reference' component 'reference'
	'linker' component 'linker'
```

### reference constraint expression

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
					'ancestor' component 'ancestor node selection'
					'collection constraint' reference
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

### derived reference constraint expression

```js
'derived reference constraint expression'
	'type' stategroup (
		'backward'
			'selection' component 'calculated collection selection starting from property'
		'self'
			'selection' component 'ancestor node selection'
			'collection' [ '.self' ] stategroup ( 'collection' )
	)
	'tail' component 'derivation node content path'
```

### singular reference expression

```js
'singular reference expression'
	'type' stategroup (
		'branch'
			'branch' [ 'from' ] reference
			'root entity constraint' stategroup ( 'root' )
			'expression' [ '[', ']' ] component 'calculated node selection starting from property'
		'singular'
			'expression' component 'calculated node selection starting from property'
	)
```

### plural reference expression

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

### EQ node type

```js
'EQ node type'
```

### EQ member

```js
'EQ member'
```

### EQ direction

```js
'EQ direction'
```

### link text expression

```js
'link text expression'
	'dependency' stategroup (
		'link'
			'context selection' component 'context property selection'
			'text' [ '.' ] reference //TODO: use > (ambiguous right now)
			'group selection' component 'group node selection'
			'collection' ['.'] reference
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

### command implementation

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

### parameter definition

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
				'ui' group (
					'key mapping' stategroup (
						'dense' ['@dense-map']
						'sparse'
					)
					'has description' stategroup (
						'no'
						'yes' [ '@description:' ]
							'description' text
					)
				)
				'entity' component 'entity'
				'parameters' component 'parameter definition'
			'text' [ 'text' ]
				'has constraint' stategroup (
					'no'
						'ui' group (
							'default' stategroup (
								'none'
									'sticky' stategroup (
										'yes' [ '@sticky' ]
										'no'
									)
								'guid' [ '@default:' 'guid' ]
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
					'yes'
						'referencer' [ '->' ] component 'parameter referencer'
						'ui' group (
							'metadata' stategroup (
								'no'
									'sticky' stategroup (
										'yes' [ '@sticky' ]
										'no'
									)
								'yes' [ '@default:' 'user' ]
									'constraint' component 'EQ node type'
							)
							'has description' stategroup (
								'no'
								'yes' [ '@description:' ]
									'description' text
							)
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
					'constraints' collection ( ['(',')']
						'expression' component 'parameter state constraint expression'
					)
					'parameters' component 'parameter definition'
				)
		)
	)
```

### ancestor parameters path

```js
'ancestor parameters path'
	'has steps' stategroup (
		'no' ['@']
		'yes' ['@^']
			'tail' component 'ancestor parameters path'
	)
```

### parameter state constraint expression

```js
'parameter state constraint expression'
	'path' ['->'] component 'parametrized conditional node path'
```

### parameter referencer

```js
'parameter referencer'
	'head' component 'parametrized singular node path'
	'collection' ['.'] reference
	'tail' component 'derivation node content path'
```

### parameter entity scoped context node selection

```js
'parameter entity scoped context node selection'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'key reference' ['>']
					'text' reference
					'dereference' component 'dereference'
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
			)
			'tail' component 'parameter entity scoped context node selection'
	)
```

### parametrized context node path

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
					'tail' component 'ancestor node path'
				'state' ['&']
					'constraint' reference
			)
	)
```

### parametrized singular node path

```js
'parametrized singular node path'
	'head' component 'parametrized context node path'
	'tail' component 'singular node path tail'
```

### parametrized conditional node path

```js
'parametrized conditional node path'
	'head' component 'parametrized context node path'
	'tail' component 'conditional descendant node path'
```

### parametrized text expression

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

### parametrized file expression

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

### parametrized state argument expression

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

### parametrized state expression

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

### parametrized collection argument expression

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

### parametrized collection expression

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

### argument definition

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

### parametrized update node

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

### parametrized initialize node

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

### variable

```js
'variable'
```

### parameter

```js
'parameter'
```

### link

```js
'link'
```

### reference

```js
'reference'
```

### delink

```js
'delink'
	'delink' stategroup ( 'yes' )
```

### dereference

```js
'dereference'
	'dereference' stategroup ( 'yes' )
```

### optional variable assignment

```js
'optional variable assignment'
	'has assignment' stategroup (
		'no'
		'yes'
			'assignment' component 'variable assignment'
	)
```

### variable assignment

```js
'variable assignment' ['as' '$']
	'variable' component 'variable'
```

### ancestor variable path

```js
'ancestor variable path'
	'has steps' stategroup (
		'no' ['$']
		'yes' ['$^']
			'tail' component 'ancestor variable path'
	)
```

## /****************** Node navigation ******************/


### ancestor node path

```js
'ancestor node path'
	'has steps' stategroup (
		'no'
		'yes' ['^']
			'tail' component 'ancestor node path'
	)
```

### conditional node path

```js
'conditional node path'
	'head' component 'ancestor node path'
	'tail' component 'conditional descendant node path'
// 'singular node path'
// 	'head' component 'ancestor node path'
// 	'tail' component 'singular node path tail'
```

### singular node path tail

```js
'singular node path tail'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'reference'
					'text' [ '>' ] reference
					'dereference' component 'dereference'
				'output parameter' //deprecated
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

### conditional descendant node path

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
// 'Plural Descendant Node Path'
// 	'head' component 'Conditional Descendant Node Path'
// 	'has steps' stategroup (
// 		'no'
// 		'yes'
// 			'type' stategroup (
// 				'collection' [ '.', '*' ]
// 					'collection' reference
// 				'reference set' [ '>' , '*' ]
// 					'reference set' reference
// 			)
// 			'tail' component 'Plural Descendant Node Path'
// 	)
```

## /****************** Permissions & Todo's ******************/


### user requirement

```js
'user requirement'
	'type' stategroup (
		'containment' ['any']
			'context' stategroup (
				'user' ['user']
					'path' component 'conditional descendant node path'
					'collection' ['.', '['] reference
					'delink key' component 'delink'
					'key path' ['$', ']'] component 'conditional node path'
					'has filter' stategroup (
						'no'
						'yes' ['as' 'user' 'where']
							'path' ['(', ')'] component 'user requirement'
					)
				'definition' ['$']
					'path' component 'conditional node path'
					'collection' ['.', '['] reference
					'delink key' component 'delink'
					'key path' ['user', ']'] component 'conditional descendant node path'
					'has filter' stategroup (
						'no'
						'yes' ['as' '$' 'where']
							'path' ['(', ')'] component 'user requirement'
					)
			)
		'existence'
			'context' stategroup (
				'user' ['user']
				'definition' ['$']
					'head' component 'ancestor node path'
			)
			'tail' component 'conditional descendant node path'
		'equality' ['equal',')']
			'left path' ['(' 'user'] component 'conditional descendant node path'
			'right path' [ ',' '$'] component 'conditional node path'
	)
	'has alternative' stategroup (
		'no'
		'yes' ['||']
			'alternative' component 'user requirement'
	)
```

### permission

```js
'permission'
	'modifier' stategroup (
		'user'
			'type' stategroup (
				'unrestricted' ['unrestricted']
				'restricted'
					'requirement' component 'user requirement'
			)
		'imported interface'
			'interface' ['interface'] reference
	)
```

### item permissions definition

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

### node permissions definition

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

### todo definition

```js
'todo definition'
	'todo' stategroup (
		'no'
		'yes' ['has-todo:']
			'requirement' component 'user requirement'
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

### ui singular path

```js
'ui singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection parent' [ '.^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
				'group' [ '+' ]
					'group' reference
				'reference' [ '>' ]
					'text' reference
					'dereference' component 'dereference'
			)
			'tail' component 'ui singular path'
	)
```

### ui conditional path

```js
'ui conditional path'
	'has steps' stategroup (
		'no'
			'tail' component 'ui singular path'
		'yes'
			'head' component 'ui singular path'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
			)
			'tail' component 'ui conditional path'
	)
```
