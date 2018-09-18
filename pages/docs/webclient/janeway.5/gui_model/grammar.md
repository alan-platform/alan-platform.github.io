---
layout: doc
origin: webclient
language: gui_model
version: janeway.5
type: grammar
---


## root


### type

```js
'type' [ 'root' ]  component 'gui type'
```

### root

```js
'root' component 'gui entity'
```

### numerical types

```js
'numerical types' [ 'numerical' 'types' ] collection indent (
	'representation type' [ '{' , '}' ] stategroup (
		'decimal' [ 'factor:' '10^' ]
			'point translation' number
		'date' [ 'date' ]
		'date and time' [ 'date-time' ]
		'HTML date and time' [ 'HTML' 'html-time' ]
		'duration' [ 'duration:' ]
			'unit' stategroup (
				'seconds' [ 'seconds' ]
				'minutes' [ 'minutes' ]
				'hours' [ 'hours' ]
			)
	)
)
```

## component rules


### gui type

```js
'gui type'
```

### gui context

```js
'gui context'
```

### gui entity

```js
'gui entity'
	'default' stategroup (
		'guid' [ 'guid' ]
		'none'
	)
	'duplication mapping' stategroup (
		'none'
		'from current context' [ 'duplicate' 'with' ]
			'mapping' component 'duplication node mapping'
	)
	'linked node mapping' stategroup (
		'none'
		'from linked entry' [ 'copy' 'from' ]
			'context node selection' component 'entity scoped context node selection'
			'mapping' [ 'with' ] component 'linked node mapping'
	)
	'node' component 'gui node'
```

### duplication node mapping

```js
'duplication node mapping'
	'properties' [ '(' , ')' ] collection indent (
		'type' [ '->' ] stategroup (
			'number' [ 'number' ]
			'text' [ 'text' ]
			'file' [ 'file' ]
			'reference' [ 'reference' ]
			'group' [ 'group' ]
				'mapping' component 'duplication node mapping'
			'state group' [ 'stategroup' ]
				'states' [ '(' , ')' ] collection indent ( ['|']
					'mapping' component 'duplication node mapping'
				)
			'dictionary' [ 'dictionary' ]
			'matrix' [ 'matrix' ]
		)
	)
```

### linked node mapping path

```js
'linked node mapping path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'linked node mapping path'
	)
```

### linked node mapping

```js
'linked node mapping'
	'properties' [ '(' , ')' ] collection indent (
		'type' stategroup (
			'number' [ 'number' '<-' ]
				'path' component 'linked node mapping path'
				'number' reference
			'text' [ 'text' '<-' ]
				'path' component 'linked node mapping path'
				'copy from' stategroup (
					'text'
						'source text' reference
					'reference' [ '>' ]
						'source reference' reference
				)
			'file' [ 'file' '<-' ]
				'path' component 'linked node mapping path'
				'file' reference
			'reference' [ 'reference' '<-' ]
				'path' component 'linked node mapping path'
				'copy from' stategroup (
					'text'
						'source text' reference
					'reference' [ '>' ]
						'source reference' reference
				)
			'group' [ 'group' '<-' ]
				'path' component 'linked node mapping path'
				'mapping' component 'linked node mapping'
			'state group' [ 'stategroup' '<-' ]
				'path' component 'linked node mapping path'
				'linked node state group' [ '?' ] reference
				'linked node states' [ '(' , ')' ] collection indent (
					'state' [ '->' ] reference
					'mapping' component 'linked node mapping'
				)
			'dictionary' [ 'dictionary' ]
		)
	)
```

### gui static singular path

```js
'gui static singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'group parent' [ '+^' ]
				'state parent' [ '?^' ]
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'gui static singular path'
	)
```

### file name expression

```js
'file name expression'
	'has steps' stategroup (
		'no'
		'yes' [ '&' ]
			'type' stategroup (
				'static'
					'text' text
				'property'
					'path' component 'gui static singular path'
					'type' stategroup (
						'text' [ ':' ]
							'text' reference
						'number' [ '#' ]
							'number' reference
						'dictionary key' [ '.key' ]
						'matrix key' [ '>key' ]
						'state group' [ '?' ]
							'state group' reference
							'states' [ '(' , ')' ] collection (
								'state file name expression' [ '(' , ')' ]  component 'file name expression'
							)
					)
			)
			'tail' component 'file name expression'
	)
```

### number expression path

```js
'number expression path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group parent' [ '+^' ]
				'state parent' [ '?^' ]
				'group'
					'group' [ '+' ] reference
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
			)
			'tail' component 'number expression path'
	)
```

### text validation

```js
'text validation'
	'regular expression' text
```

### number limit

```js
'number limit'
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

### gui command parameters node

```js
'gui command parameters node' [ '{' , '}' ]
	'context' component 'gui context'
	'properties' collection  indent (
		'type' [ ':' ] stategroup (
			'number' [ 'number' ]
				'numerical type' reference
				'initialize' stategroup (
					'empty'
					'with' [ 'default:' ]
						'type' stategroup (
							'sticky' [ 'sticky' ]
							'number' [ '#' ]
								'path' component 'number expression path'
								'property' reference
						)
				)
				'validation' group (
					'has minimum' stategroup (
						'no'
						'yes' ['min:']
							'minimum' component 'number limit'
					)
					'has maximum' stategroup (
						'no'
						'yes' ['max']
							'maximum' component 'number limit'
					)
				)
			'text' [ 'text' ]
				'initialize' stategroup (
					'empty'
					'with' [ 'default:' ]
						'type' stategroup (
							'sticky' [ 'sticky' ]
							'guid' [ 'guid' ]
						)
				)
				'has validation' stategroup (
					'no'
					'yes' ['validate:']
						'rules' component 'text validation'
				)
			'file' [ 'file' ]
			'matrix' [ 'matrix' ]
				'navigable' stategroup (
					'yes'
						'referenced node' [ '->' ] component 'gui entity type path'
					'no'
				)
				'parameters' component 'gui command parameters node'
			'reference' [ 'reference' ]
				'context' component 'gui context'
				'default' stategroup (
					'none'
						'sticky' stategroup (
							'yes' [ 'sticky' ]
							'no'
						)
					'current user' [ 'default:' 'current' 'user' ]
				)
				'referenced node' [ '->' ] component 'gui entity type path'
			'state group' [ 'stategroup' ]
				'has states' stategroup has 'states' first 'first' 'yes' 'no'
				'default state' stategroup (
					'no'
						'sticky' stategroup (
							'yes' [ 'sticky' ]
							'no'
						)
					'yes'
						'state' [ 'default:' ] reference
				)
				'states' [ '(' , ')' ] collection order 'view order' indent (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'parameters' [ '->' ] component 'gui command parameters node'
				)
		)
	)
```

### gui node

```js
'gui node' [ '{' , '}' ]
	'context' component 'gui context'
	'attributes' collection indent (
		'type' stategroup (
			'log' [ ':' 'log' ]
			'referencer anchor' [ ':' 'reference-set' ]
			'command' [ ':' 'command' ]
				'type' stategroup (
					'global'
						'parameters' component 'gui command parameters node'
					'component'
				)
			'property' [':']
				'type' stategroup (
					'dictionary' [ 'dictionary' ]
						'key type' stategroup (
							'simple'
							'link' [ 'link' ]
								'navigable' stategroup (
									'yes' ['->']
										'gui type' component 'gui entity type path'
									'no'
								)
						)
						'has validation' stategroup (
							'no'
							'yes' [ 'validate:' ]
								'rules' component 'text validation'
						)
						'gui entity' component 'gui entity'
					'group' [ 'group' ]
						'gui node' component 'gui node'
					'number' [ 'number' ]
						'numerical type' reference
						'default' stategroup (
							'none'
							'current date and time' [ 'default:' 'today' ]
							'current date' [ 'default:' 'now' ]
						)
						'validation' group (
							'has minimum' stategroup (
								'no'
								'yes' [ 'min:' ]
									'minimum' component 'number limit'
							)
							'has maximum' stategroup (
								'no'
								'yes' [ 'max:' ]
									'maximum' component 'number limit'
							)
						)
					'text' [ 'text' ]
						'value type' stategroup (
							'simple'
							'link' [ 'link' ]
								'navigable' stategroup (
									'yes' ['->']
										'context' component 'gui context'
										'gui type' component 'gui entity type path'
									'no'
								)
						)
						'password property' stategroup (
							'yes' [ 'password' ]
								'constraint' component 'text property constraint'
							'no'
						)
						'has validation' stategroup (
							'no'
							'yes' [ 'validate:' ]
								'rules' component 'text validation'
						)
					'file' [ 'file' ]
						'file name expression' ['name:'] component 'file name expression'
					'reference' [ 'reference' ]
						'default' stategroup (
							'none'
							'current user' [ 'default:' 'current' 'user' ]
						)
						'navigable' stategroup (
							'yes' [ '->' ]
								'context' component 'gui context'
								'referenced node' component 'gui entity type path'
							'no'
						)
					'state group' [ 'stategroup' ]
						'default' stategroup (
							'none'
							'set'
								'state' [ 'default:' ] reference
						)
						'output parameters' collection ( [ '(' , ')' ]
							'referenced node' [ '->' ] component 'gui node type path'
						)
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' [ '(' , ')' ] collection order 'view order' indent (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'gui node' [ '->' ] component 'gui node'
						)
					'matrix' [ 'matrix' ]
						'context' component 'gui context'
						'navigable' stategroup (
							'yes' ['->']
								'referenced node' component 'gui entity type path'
								'context' component 'gui context'
							'no'
						)
						'gui entity' component 'gui entity'
				)
		)
	)
```

### text property constraint

```js
'text property constraint'
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

### gui entity node type path step

```js
'gui entity node type path step'
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
			'tail' component 'gui entity node type path step'
	)
```

### gui entity type path step

```js
'gui entity type path step'
	'has steps' stategroup (
		'no'
			'tail' component 'gui entity node type path step'
		'yes'
			'head' component 'gui entity node type path step'
			'collection type' stategroup (
				'matrix'
					'matrix' [ '%' ] reference
				'dictionary'
					'dictionary' [ '.' ] reference
			)
			'tail' component 'gui entity type path step'
	)
```

### gui entity type path

```js
'gui entity type path'
	'head' component 'gui entity node type path step'
	'collection type' stategroup (
		'matrix'
			'matrix' [ '%' ] reference
		'dictionary'
			'dictionary' [ '.' ] reference
	)
	'tail' component 'gui entity type path step'
```

### gui node type path step

```js
'gui node type path step'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
				'dictionary'
					'dictionary' [ '.' ] reference
				'matrix'
					'matrix' [ '%' ] reference
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'gui node type path step'
	)
```

### gui node type path

```js
'gui node type path'
	'steps' component 'gui node type path step'
```
