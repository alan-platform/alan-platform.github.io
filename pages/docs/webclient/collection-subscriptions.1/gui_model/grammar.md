---
layout: doc
origin: webclient
language: gui_model
version: collection-subscriptions.1
type: grammar
---


```js
'type' [ 'root' ]  component 'gui type'
```

```js
'root member' component 'member'
```

```js
'root' component 'gui node'
```

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

```js
'gui type'
```

```js
'member'
```

```js
'gui context'
```

```js
'duplication node mapping'
	'properties' [ '(' , ')' ] collection indent (
		'type' [ '->' ] stategroup (
			'number' [ 'number' ]
			'text' [ 'text' ]
			'file' [ 'file' ]
			'group' [ 'group' ]
				'mapping' component 'duplication node mapping'
			'state group' [ 'stategroup' ]
				'states' [ '(' , ')' ] collection indent ( ['|']
					'mapping' component 'duplication node mapping'
				)
			'collection' [ 'collection' ]
		)
	)
```

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

```js
'linked node mapping'
	'properties' [ '(' , ')' ] collection indent (
		'type' stategroup (
			'number' [ 'number' '<-' ]
				'path' component 'linked node mapping path'
				'number' reference
			'text' [ 'text' '<-' ]
				'path' component 'linked node mapping path'
				'source text' reference
			'file' [ 'file' '<-' ]
				'path' component 'linked node mapping path'
				'file' reference
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
			'collection' [ 'collection' ]
		)
	)
```

```js
'gui static singular path'
	'head' component 'ancestor node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'gui static singular path'
	)
```

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

```js
'text validation'
	'regular expression' text
```

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

```js
'gui command parameters node' [ '{' , '}' ]
	'context' component 'gui context'
	'properties' collection  indent (
		'type' [ ':' ] stategroup (
			'number' [ 'number' ]
				'numerical type' reference
				'default' stategroup (
					'yes' [ 'default:' ]
						'value' stategroup (
							'today' [ 'today' ]
							'now' [ 'now' ]
							'zero' [ 'zero' ]
							'one' [ 'one' ]
							'property' [ 'model' 'property' ]
						)
					'no'
						'sticky' stategroup (
							'yes' [ 'sticky' ]
							'no'
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
				'has constraint' stategroup (
					'no'
					'has validation' stategroup (
						'no'
						'yes' ['validate:']
							'rules' component 'text validation'
					)
					'yes'
						'context' component 'gui context'
						'referenced node' [ '->' ] component 'gui entity type path'
				)
				'default' stategroup (
					'no'
						'sticky' stategroup (
							'no'
							'yes' [ 'sticky' ]
						)
					'yes' [ 'default:' ]
						'source' stategroup (
							'guid' [ 'guid' ]
							'current user' [ 'user' ]
								'constraint' component 'EQ node type'
							'expression' [ 'model' 'expression' ]
						)
				)
			'file' [ 'file' ]
			'collection' [ 'collection' ]
				'navigable' stategroup (
					'yes'
						'referenced node' [ '->' ] component 'gui entity type path'
					'no'
				)
				'parameters' component 'gui command parameters node'
			'state group' [ 'stategroup' ]
				'has states' stategroup has 'states' first 'first' 'yes' 'no'
				'default state' stategroup (
					'no'
						'sticky' stategroup (
							'yes' [ 'sticky' ]
							'no'
						)
					'yes' [ 'default:' ]
						'source' stategroup (
							'state'
								'state' reference
							'state switch' [ 'model' 'switch' ]
						)
				)
				'states' [ '(' , ')' ] collection order 'view order' indent (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'parameters' [ '->' ] component 'gui command parameters node'
				)
		)
	)
```

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
					'collection' [ 'collection' ]
						'key property' ['[',']'] reference
						'node' component 'gui node'
						'duplication mapping' stategroup (
							'none'
							'from current context' [ 'duplicate' 'with' ]
								'mapping' component 'duplication node mapping'
						)
						'linked node mapping' stategroup (
							'none'
							'from linked entry' [ 'copy' 'from' ]
								'context node selection' component 'entity scoped ancestor node path'
								'mapping' [ 'with' ] component 'linked node mapping'
						)
						'default' stategroup (
							'no'
							'yes' ['default:' 'model' 'expression']
						)
					'group' [ 'group' ]
						'gui node' component 'gui node'
					'number' [ 'number' ]
						'numerical type' reference
						'default' stategroup (
							'no'
							'yes'
								'value' stategroup (
									'today' [ 'today' ]
									'now' [ 'now' ]
									'zero' [ 'zero' ]
									'one' [ 'one' ]
									'property' [ 'model' 'property' ]
								)
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
						'navigable' stategroup (
							'yes' [ '->' ]
								'context' component 'gui context'
								'referenced node' component 'gui entity type path'
								'output parameters' collection ( ['(',')']
									'referenced node' ['->'] component 'gui node type path'
								)
							'no'
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
						)
						'value type' stategroup (
							'simple'
							'link' [ 'link' ]
								'navigable' stategroup (
									'yes' ['~>']
										'context' component 'gui context'
										'gui type' component 'gui entity type path'
									'no'
								)
						)
						'default' stategroup (
							'no'
							'yes' [ 'default:' ]
								'source' stategroup (
									'guid' [ 'guid' ]
									'current user' [ 'user' ]
									'expression' [ 'model' 'expression' ]
								)
						)
					'file' [ 'file' ]
						'file name expression' ['name:'] component 'file name expression'
					'state group' [ 'stategroup' ]
						'default' stategroup (
							'no'
							'yes' [ 'default:' ]
								'source' stategroup (
									'state'
										'state' reference
									'state switch' [ 'model' 'switch' ]
								)
						)
						'output parameters' collection ( [ '(' , ')' ]
							'referenced node' [ '->' ] component 'gui node type path'
						)
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' [ '(' , ')' ] collection order 'view order' indent (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'input parameters' collection ( [ '(' , ')' ]
								'referenced node' [ '->' ] component 'gui node type path'
							)
							'gui node' [ '->' ] component 'gui node'
						)
				)
		)
		'attribute' component 'member'
	)
```

```js
'text property constraint'
```

```js
'ancestor node path'
	'has steps' stategroup (
		'no'
		'yes' [ '^' ]
			'tail' component 'ancestor node path'
	)
```

```js
'entity scoped ancestor node path'
	'path' component 'ancestor node path'
```

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

```js
'gui entity type path step'
	'has steps' stategroup (
		'no'
			'tail' component 'gui entity node type path step'
		'yes'
			'head' component 'gui entity node type path step'
			'collection' [ '.' ] reference
			'tail' component 'gui entity type path step'
	)
```

```js
'gui entity type path'
	'head' component 'gui entity node type path step'
	'collection' [ '.' ] reference
	'tail' component 'gui entity type path step'
```

```js
'gui node type path step'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
				'collection'
					'collection' [ '.' ] reference
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'gui node type path step'
	)
```

```js
'gui node type path'
	'steps' component 'gui node type path step'
```

```js
'EQ node type'
```
