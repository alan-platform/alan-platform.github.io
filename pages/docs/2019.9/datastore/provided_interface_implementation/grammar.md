---
layout: doc
origin: datastore
language: provided_interface_implementation
version: 48.2
type: grammar
---


```js
'node identification' group (
	'composite key' component 'node identity'
	'key' component 'node identity'
	'none' component 'node identity'
)
```

```js
'no variable' component 'variable'
```

```js
'no filter' [ 'root' '=' ] component 'filter'
```

```js
'variable assignment' ['root'] component 'optional variable assignment'
```

```js
'application root node' component 'interface context id path'
```

```js
'root context' component 'context'
```

```js
'root member' component 'member'
```

```js
'root' component 'node type mapping'
// 'numerical types' ['numerical-types-mapping'] collection (
// 	'source numerical types' collection ( )
// )
```

```js
'EQ entity type'
```

```js
'EQ collection'
```

```js
'EQ interface node type'
```

```js
'node identity'
```

```js
'INEQ identification type'
```

```js
'member'
```

```js
'filter'
```

```js
'variable'
```

```js
'context'
```

```js
'EQ member'
```

```js
'dereference'
	'dereference' stategroup ( 'yes' )
```

```js
'delink'
	'delink' stategroup ( 'yes' )
```

```js
'interface context id path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection entry'
					'collection' [ '.' , '[' ] reference
					'id' [ '@' , ']' ] reference
				'group' [ '+' ]
					'group' reference
				'state' [ '?']
					'state group' reference
					'state' [ '|' ] reference
			)
			'variable assignment' component 'optional variable assignment'
			'tail' component 'interface context id path'
	)
```

```js
'key separator'
	'separator' ['join'] stategroup (
		'dot' ['.']
		'dash' ['-']
		'colon' [':']
		'greater than' ['>']
		'space' ['space']
	)
```

```js
'key constructor'
	'branch concatenation' stategroup (
		'yes'
			'type' stategroup (
				'prepend' ['prepend-branch']
				'append' ['append-branch']
			)
		'no'
			'constraint' stategroup ( 'no' )
	)
	'key separator' stategroup (
		'yes'
			'key separator' component 'key separator'
		'no'
			'constraint: composite key not allowed without key separator' component 'INEQ identification type'
			'no successor' stategroup ( 'no' )
	)
```

```js
'node type mapping' [ '(' , ')' ]
	'attributes' collection (
		'type' [ ':' ] stategroup (
			'command' [ 'command' ]
				'implementation' component 'command mapping'
			'property'
				'type' stategroup (
					'collection' [ 'collection' ]
						'type' stategroup (
							'empty' [ '=' 'empty']
							'dynamic'
								'key type' stategroup (
									'dictionary' [ '=' ]
										'key constructor' component 'key constructor'
									'matrix' [ '->','=' ]
										'referencer' group (
											'head' component 'singular imp node path'
											'collection' [ '.' ] reference
											'branches' ['(',')'] collection ( ['-|']
												'tail' component 'conditional descendant imp node path'
												'constraint: interface node type equality' component 'EQ interface node type'
												'constraint: reference constraint not allowed for composite keys' component 'INEQ identification type'
											)
										)
								)
								'has branch' stategroup has 'branches' first 'first' 'yes' 'no'
								'branches' ['(',')'] collection (
									'has successor' stategroup has successor 'successor' 'yes' 'no'
									'expression' ['='] component 'collection expression'
									'type' stategroup (
										'dictionary'
										'matrix' ['(', ')']
											'branch' ['from'] reference
											'key path' ['>[',']'] component 'collection key node path'
									)
									'context' component 'context'
									'node' component 'node type mapping'
								)
							)
					'group' [ 'group' ]
						'expression' ['='] component 'group expression'
						'node' component 'node type mapping'
					'number'
						'type' stategroup (
							'integer' [ 'integer' ]
							'natural' [ 'natural' ]
						)
						'expression' ['='] component 'number expression'
					'reference' [ 'text' ]
						'referencer' ['->'] group (
							'head' component 'singular imp node path'
							'collection' [ '.' ] reference
							'branch' ['-|'] reference
							'constraint: reference constraint not allowed for composite keys' component 'INEQ identification type'
							'tail' component 'conditional descendant imp node path'
							'constraint: interface node type equality' component 'EQ interface node type'
						)
						'expression' ['='] component 'reference expression'
					'state group' [ 'stategroup' ]
						'expression' ['='] component 'state expression'
					'text' [ 'text' ]
						'expression' ['='] component 'text expression'
					'file' ['file']
						'expression' ['='] component 'file expression'
				)
		)
	'attribute' component 'member'
)
```

```js
'command mapping' ['do']
	'path' ['on'] component 'singular node path'
	'command' ['('] reference
	'argument mapping' [ 'with' ,')'] component 'argument mapping'
```

```js
'argument mapping' [ '(' , ')' ]
	'properties' collection (
		'type' [ ':' ] stategroup (
			'collection' [ 'collection' ]
				'collection' [ '=' 'map' '@' '.' ] reference
				'argument mapping' component 'argument mapping'
			'number'
				'numerical type' stategroup (
					'integer' [ 'integer' ]
					'natural' [ 'natural' ]
				)
				'number' [ '=' '@' '#' ] reference
			'text'
				'value provision' stategroup (
					'key' ['text' '=' '@key']
						'constraint: text is collection key' component 'EQ member'
					'value'
						'constraint: text is not collection key' component 'EQ member'
						'has constraint' stategroup (
							'no' [ 'text' ]
								'text' [ '=' '@' '.' ] reference
							'yes' [ 'text' ]
								'type' ['='] stategroup (
									'parameter'
										'reference' ['@' '>'] reference
									'variable'
										'path' component 'context node path'
								)
						)
				)
			'file' ['file']
				'file' [ '=' '@' '/' ] reference
			'state group' [ 'stategroup' ]
				'type' [ '=' ] stategroup (
					'fixed'
						'state' reference
						'argument mapping' component 'argument mapping'
					'map' [ 'switch' '(' '@' ]
						'state group' [ '?' , ')' ] reference
						'mapping' ['(', ')'] collection ( [ '|' ]
							'mapped state' [ '=' ] reference
							'argument mapping' component 'argument mapping'
						)
					'match branch' ['match-branch']
						'path' ['(',')'] group (
							'head' component 'singular imp node path'
							'collection' ['.'] reference
							'item reference' ['[',']'] stategroup (
								'key'['@key']
								'text'
									'reference' ['@' '>'] reference
							)
						)
						'branches' ['(',')'] collection ( ['|']
							// 'tail' component 'conditional descendant imp node path'
							'state mapping context variable' stategroup (
								'current variable'
								'branch context variable' ['bind' '$']
							)
							// 'EQ interface node type' component 'EQ interface node type'
							'state' ['='] reference
							'argument mapping' component 'argument mapping'
						)
				)
		)
	)
```

```js
'filter expression'
	'has filter' stategroup (
		'no'
		'yes'['where']
			'filter' component 'filter'
			'has filters' stategroup has 'filters' first 'first' 'yes' 'no'
			'filters' ['(',')'] collection ( ['$']
				'has successor' stategroup has successor 'successor' 'yes' 'no'
				'type' stategroup (
					'singular result'
						'path' ['='] component 'conditional node path'
					'equality' ['=' 'equal']
						'left path' ['('] component 'singular node path'
						'right path' [',', ')'] component 'singular node path'
				)
			)
	)
```

```js
'group expression'
	'type' stategroup (
		'none'
		'bound'
			'path' component 'singular node path'
			'context' component 'context'
			'variable assignment' component 'variable assignment'
	)
```

```js
'collection expression'
	'head' component 'context node path'
	'tail' component 'collection expression tail'
```

```js
'collection expression tail'
	// pnet := pdnp filter? stva? pnet //ambiguous because filter and stva optional.
	// pnet := ( pdnp | pdnp filter pnet | pdnp filter stva pnet | pdnp stva pnet  )
	'has steps' stategroup (
		'no'
			'filter' component 'filter expression'
		'yes'
			'type' stategroup (
				'singular'
					'step' component 'singular node step'
				'conditional'
					'step' component 'conditional descendant node step'
				'plural'
					'step' component 'plural descendant node step'
			)
			'variable assignment' component 'optional variable assignment'
			'tail' component 'collection expression tail'
	)
```

```js
'number expression'
	'path' component 'singular node path'
	'type' stategroup (
		'property'
			'number' [ '#' ] reference
		'state context parameter'
			'number' [ '&#' ] reference
	)
```

```js
'file expression'
	'path' component 'singular node path'
	'file' [ '/' ] reference
```

```js
'text expression'
	'path' component 'singular node path'
	'text' [ '.' ] reference
```

```js
'state expression'
	'type' stategroup (
		'static'
			'state' reference
			'node' component 'node type mapping'
		'dynamic' [ 'switch' '(' ]
			'path' component 'singular node path'
			'state group' [ '?' , ')' ] reference
			'states' [ '(' , ')' ] collection ( [ '|' ]
				'variable assignment' component 'optional variable assignment'
				'context' component 'context'
				'state' [ '=' ] reference
				'node' component 'node type mapping'
			)
	)
```

```js
'reference expression'
	'path' component 'singular node path'
	'text' [ '>' ] reference
	'dereference' component 'dereference'
	'key path' ['(', ')'] component 'collection key node path'
	//how do we guarantee that the node is an actual member of the collection?
	// the problems is that we have path-dependent references,
	// and that we select a subset of nodes of a specific type,
	// where that subset depends on a complex path: the collection expression.
	//suppose, we only support reference navigation for the head of the collection expression
	//then, we have to prove for the first collection step that the context dependency equals that of the reference (or a path dependent ancestor reference)
	//so, starting at the target reference, we have to prove correctness for all preceding steps.
	//for example, a hierarchy .orders.work orders.tasks requires three references; e.g.:
	// >'order' >'work order' >'task'
	// where we constrain that subsequent references depend on preceding references.
	// state group output parameters may be a problem, but we ignore them for now.
```

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
// 'ancestor node path'
// 	'has steps' stategroup (
// 		'no'
// 		'yes' ['^']
// 			'tail' component 'ancestor node path'
// 	)
```

```js
'context node path'
	'type' stategroup (
		'root' ['root']
		'variable'
			'head' component 'ancestor variable path'
			'type' stategroup (
				'variable'
				'filter'
					'filter' reference
			)
			// 'tail' component 'ancestor node path' // use variables instead
	)
```

```js
'singular node path'
	'head' component 'context node path'
	'tail' component 'singular node path tail'
```

```js
'singular node path tail'
	'has steps' stategroup (
		'no'
		'yes'
			'step' component 'singular node step'
			'tail' component 'singular node path tail'
	)
```

```js
'singular node step'
	'type' stategroup (
		'group' ['+']
			'group' reference
		'reference'
			'text' ['>'] reference
			'dereference' component 'dereference'
		'state context parameter'
			'parameter' ['&'] reference
	)
```

```js
'conditional node path'
	'head' component 'context node path'
	'tail' component 'conditional node path tail'
```

```js
'conditional node path tail'
	'head' component 'singular node path tail'
	'has steps' stategroup (
		'no'
		'yes'
			'step' component 'conditional descendant node step'
			'tail' component 'conditional node path tail'
	)
```

```js
'conditional descendant node step'
	'type' stategroup (
		'state'
			'state group' ['?'] reference
			'state' ['|'] reference
		'collection entry'
			'collection' ['.'] reference
			'delink collection key' component 'delink'
			'key' ['[',']'] group (
				'path' component 'singular node path' //OPT: conditional node path
				'text' ['>'] reference
				'delink text' component 'delink'
				'constraint: linked collection equals collection key link' component 'EQ collection'
			)
	)
```

```js
'plural descendant node step'
	'collection' ['.'] reference
	'type' ['*'] stategroup (
		'elementary'
		'derived' ['(derived)']
	)
```

```js
'collection key node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'reference' ['>']
					'text' reference
					'dereference' component 'dereference'
					'constraint: text is collection key' component 'EQ member'
				'parent' ['^']
					'constraint: no parent step to outside collection' component 'EQ entity type'
				'filter' ['$']
					'filter' reference
			)
			'tail' component 'collection key node path'
	)
```

```js
'conditional descendant branch imp node path'
	'type' stategroup (
		'static'
		'dynamic'
			'state' ['|'] reference //should be '|' but that requires a schema change (always require a state; also for the static case)
	)
```

```js
'conditional descendant imp node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state' [ '?' ]
					'state group' reference
					'path' component 'conditional descendant branch imp node path'
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'conditional descendant imp node path'
	)
```

```js
'singular imp node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'parent' [ '^' ]
				'group' [ '+' ]
					'group' reference
				'reference' [ '>' ]
					'reference' reference
			)
			'tail' component 'singular imp node path'
	)
```
