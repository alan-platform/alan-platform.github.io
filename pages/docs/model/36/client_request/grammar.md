---
layout: doc
origin: model
language: client_request
version: 36
type: grammar
---


## root


### type

```js
'type' stategroup (
	'collection query'
		'context node path' [ 'collection' ] component 'id path'
		'collection path' [ 'select' ] component 'collection path'
		'filters' group (
			'todo filter' stategroup (
				'yes' ['where' 'has-todo']
					'path' ['(',')'] component 'conditional path'
				'no'
			)
		)
		'properties' collection (
			'path' [ '->' ] component 'conditional path'
			'type' stategroup (
				'number' [ 'number' ]
					'type' stategroup (
						'property' [ ':' ]
							'number' reference
						'expression' [ '(' , ')' ]
							'expression' component 'number expression2'
					)
					'filtering' stategroup (
						'enabled'
							'operator' stategroup (
								'equal to' [ '==' ]
								'greater than' [ '>' ]
								'greater than or equal to' [ '>=' ]
								'smaller than' [ '<' ]
								'smaller than or equal to' [ '<=' ]
							)
							'criteria' number
						'disabled'
					)
				'reference' [ 'reference' ]
					'type' stategroup (
						'functional id' ['id']
						'reference' [':']
							'reference' reference
					)
					'include reference' stategroup (
						'no'
						'yes' ['#include-reference']
					)
					'filtering' stategroup (
						'enabled' ['(', ')']
							'referenced node' component 'id path'
						'disabled'
					)
				'state group' [ 'stategroup' ]
					'state group' [ ':' ] reference
					'filtering' stategroup (
						'enabled' [ 'include' ]
							'states to include' [ '(' , ')' ] collection ( )
						'disabled'
					)
				'text' [ 'text' ]
					'type' stategroup (
						'property'
							'type' stategroup (
								'functional id' [ 'id' ]
								'property' [ ':' ]
									'text' reference
							)
						'expression' [ '(' , ')' ]
							'expression' component 'text expression'
					)
					'filtering' stategroup (
						'enabled' [ '(' , ')' ]
							'expression' component 'filter expression'
						'disabled'
					)
				'file' ['file']
					'file' [':'] reference
			)
		)
		'maximum amount of entries' [ 'limit' ] number
	'acyclic graph tree query'
		'context node' ['graph'] component 'id path'
		'type' ['select'] stategroup (
			'dictionary' ['from' 'dictionary']
				'graph' reference
			'matrix' ['from' 'matrix']
				'graph' reference
		)
	'acyclic graph list query'
		'context node' component 'id path'
		'entry points' ['select'] component 'entry point path'
		'collection' component 'ancestor path'
		'collection type' stategroup (
			'dictionary' ['dictionary']
				'graph' ['flatten'] reference
			'matrix' ['matrix']
				'graph' ['flatten'] reference
		)
		'query' group (
			'collection path' ['collection'] component 'collection path'
			'properties' collection (
				'path' ['->'] component 'conditional path'
				'type' stategroup (
					'number' ['number']
						'number' reference
					'text' ['text']
						'type' stategroup (
							'functional id' ['id']
							'property'
								'text' reference
						)
					'state group' ['stategroup']
						'state group' reference
				)
			)
		)
	'denseness query'
		'context node' ['denseness'] component 'id path'
		'dictionary' ['.'] reference
		'maximum amount of entries' [ 'limit' ] number
	'mutation'
		'context node' [ 'update' ] component 'id path'
		'update node' component 'update node'
	'subscription'
		'mutation permissions' stategroup (
			'include'
			'ignore' ['#ignore-mutation-permissions']
		)
		'context node' [ 'subscribe' 'to' ] component 'id path'
		'subscribed properties' component 'subscribed properties'
	'subscription deletion'
	'parameter query'
		'context node path' [ 'parameters' ] component 'id path'
		'type' stategroup (
			'elementary'
				'parameter type' [ 'select' ] stategroup (
					'output parameter'
						'type' stategroup (
							'state group output parameter' [ '?' ]
								'state group' reference
								'output parameter' [ '$' ] reference
							'referencer output'
								'referencer type' stategroup (
									'matrix' [ '%}' ]
									'output type' stategroup (
										'referenced node'
										'output parameter' [ '$' ]
											'output parameter' reference
									)
									'reference' [ '>' ]
										'reference' reference
										'output type' stategroup (
											'referenced node'
											'output parameter' [ '$' ]
												'output parameter' reference
										)
								)
						)
					'input parameter'
						'type' stategroup (
							'state' [ '*&' ]
								'input parameter' reference
						)
				)
			'derived' [ 'derived' ]
				'parameter type' [ 'select' ] stategroup (
					'output parameter'
						'type' stategroup (
							'state group output parameter' [ '?' ]
								'state group' reference
								'output parameter' [ '$' ] reference
							'referencer output'
								'referencer type' stategroup (
									'matrix' [ '%}' ]
									'output type' stategroup (
										'referenced node'
										'output parameter' [ '$' ]
											'output parameter' reference
									)
									'reference' [ '>' ]
										'reference' reference
										'output type' stategroup (
											'referenced node'
											'output parameter' [ '$' ]
												'output parameter' reference
										)
								)
						)
					'input parameter'
						'type' stategroup (
							'state' [ '*&' ]
								'input parameter' reference
						)
				)
		)
	'command execution'
		'context node' [ 'execute' ] component 'id path'
		'command' [ ':' ] reference
		'arguments' [ 'with' ] component 'command arguments'
)
```

## component rules


### filter expression

```js
'filter expression'
	'type' stategroup (
		'wildcard' [ '*' ]
		'alternatives' [ '[' , ']' ]
		'alternatives' collection ( )
	)
	'has more steps' stategroup (
		'yes'
		'tail' component 'filter expression'
		'no'
	)
```

### id path

```js
'id path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary entry' [ '.' ]
					'dictionary' reference
					'id' [ ':' ] text
				'matrix entry' [ '%' ]
					'matrix' reference
					'id' [ ':' ] text
				'group' [ '+' ]
					'group' reference
				'state' [ '?']
					'state group' reference
					'state' [ '*' ] reference
			)
			'tail' component 'id path'
	)
```

### conditional child path

```js
'conditional child path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group' [ '+' ]
					'group' reference
				'state' [ '?' ]
					'state group' reference
					'state' [ '*' ] reference
			)
			'tail' component 'conditional child path'
	)
```

### collection path

```js
'collection path'
	'has steps' stategroup (
		'no'
		'yes'
			'head' component 'conditional child path'
			'type' stategroup (
				'dictionary' [ '.' ]
					'dictionary' reference
				'matrix' [ '%' ]
					'matrix' reference
			)
			'tail' component 'collection path'
	)
```

### entry point path

```js
'entry point path'
	'has steps' stategroup (
		'no'
			'type' stategroup (
				'reference'
					'reference' ['>'] reference
				'matrix key' ['%}']
			)
		'yes'
			'head' component 'conditional child path'
			'type' stategroup (
				'dictionary'
					'dictionary' ['.'] reference
				'matrix'
					'matrix' ['%'] reference
			)
			'tail' component 'entry point path'
	)
```

### ancestor path

```js
'ancestor path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group parent' ['+^']
				'state parent' ['?^']
			)
			'tail' component 'ancestor path'
	)
```

### plural path

```js
'plural path'
	'has steps' stategroup (
		'no'
			'tail' component 'conditional path'
		'yes'
			'head' component 'conditional path'
			'type' stategroup (
				'merge' [ 'merge' ]
					'expected node path' [ '(' , ')' ] component 'node type path'
					'paths' [ '(' , ')' ] collection (
						'plural path' [ '->' ] component 'plural path'
					)
				'dictionary' [ '.' ]
					'dictionary' reference
				'matrix' [ '%' ]
					'matrix' reference
				'referencers to me' [ '<' ]
					'referencing node path' [ '(' , ')' ] component 'node type path'
					'type' stategroup (
						'reference' [ '>' ]
							'reference' reference
						'matrix' [ '%' ]
							'matrix' reference
					)
			)
			'tail' component 'plural path'
	)
```

### conditional path

```js
'conditional path'
	'has steps' stategroup (
		'no'
			'tail' component 'singular path'
		'yes'
			'head' component 'singular path'
			'type' stategroup (
				'state' [ '?' ]
					'state group' reference
					'state' [ '*' ] reference
			)
			'tail' component 'conditional path'
	)
```

### singular path

```js
'singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
				//'state group output parameter' [ '?' ]
				//	'state group' reference
				//	'output parameter' [ '$' ] reference
				'reference' [ '>' ]
					'reference' reference
				'matrix key' [ '%}' ]
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'singular path'
	)
```

### node type path

```js
'node type path'
	'steps' component 'node type path step'
```

### node type path step

```js
'node type path step'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state' [ '?' ]
					'state group' reference
					'state' [ '*' ] reference
				'group' [ '+' ]
					'group' reference
				'dictionary' [ '.' ]
					'dictionary' reference
				'matrix' [ '%' ]
					'matrix' reference
			)
			'tail' component 'node type path step'
	)
```

### aggregate2

```js
'aggregate2'
	'head' component 'singular path'
	'type' stategroup (
		'dictionary' [ '.' ]
			'dictionary' reference
		'matrix' [ '%' ]
			'matrix' reference
		'referencers to me' [ '<' ]
			'referencing node path' [ '(' , ')' ] component 'node type path'
			'type' stategroup (
				'reference' [ '>' ]
					'reference' reference
				'matrix' [ '%' ]
					'matrix' reference
			)
	)
	'tail' component 'conditional path'
```

### number aggregate2

```js
'number aggregate2' [ '(' , ')' ]
	'aggregate' [ '#' ] component 'aggregate2'
	'property name' [ ':' ] reference
```

### signed number property2

```js
'signed number property2'
	'path' [ '#' ] component 'singular path'
	'sign' [ ':' ] stategroup (
		'negative' [ '-' ]
		'positive'
	)
	'property name' reference
```

### signed number property list

```js
'signed number property list'
```

### has element

```js
'has element' stategroup (
	'no'
	'yes'
	'signed number property' component 'signed number property2'
	'tail' component 'signed number property list'
)
```

### number expression2

```js
'number expression2'
	'type' stategroup (
		'value'
			'value' number
		'number property'
			'signed number property' component 'signed number property2'
		'sum' [ 'sum' ]
			'number aggregate' component 'number aggregate2'
		'sum list' [ 'sumlist' ]
			'numbers' [ '(' , ')' ] component 'signed number property list'
		'remainder' [ 'remainder' ]
			//keyword '('
			'number' component 'signed number property2'
			'modulus' component 'signed number property2'
			//keyword ')'
		'product' [ 'product' ]
			'numbers' [ '(' , ')' ] component 'signed number property list'
		'division' [ 'division' ]
			'rounding' stategroup (
				'ordinary'
				'ceil' [ 'ceil' ]
				'floor' [ 'floor' ]
			)
			//keyword '('
			'numerator' component 'signed number property2'
			'denominator' component 'signed number property2'
			//keyword ')'
		'count' [ 'count' ]
			'aggregate' [ '(' , ')' ] component 'aggregate2'
		'state based' [ '?' ]
			'path' component 'singular path'
			'state group' [ ':' ] reference
			'states' [ '(' , ')' ] collection (
				'value' [ '->' ] component 'number expression2'
			)
		'maximum' [ 'max' ]
			//keyword '('
			'left expression' component 'number expression2'
			'right expression' component 'number expression2'
			//keyword ')'
		'minimum' [ 'min' ]
			//keyword '('
			'left expression' component 'number expression2'
			'right expression' component 'number expression2'
			//keyword ')'
	)
```

### singular text expression

```js
'singular text expression'
	'type' stategroup (
		'static'
			'string' text
		'dynamic'
			'path' component 'singular path'
			'type' stategroup (
				'text' [ ':' ]
					'text' reference
				'id' [ 'id' ]
			)
	)
```

### singular text expression list

```js
'singular text expression list'
```

### has element

```js
'has element' stategroup (
	'no'
	'yes'
	'singular text expression' component 'singular text expression'
	'tail' component 'singular text expression list'
)
```

### text expression

```js
'text expression'
	//NOTE: result node is an ugly way to enforce a location on type==id
	'type' stategroup (
		'singular'
			'expression' component 'singular text expression'
		'concatenation' [ 'concat' ]
			'parts' [ '(' , ')' ] component 'singular text expression list'
		'join' [ 'join' ]
			'node collection' [ '(' , ')' ] component 'plural path'
			'expression' component 'text expression'
			'separator' [ 'with' ] text
	)
```

### subscribed properties

```js
'subscribed properties' [ '(' , ')' ]
	'properties' collection (
		'type' [ '->' ] stategroup (
			'dictionary' [ 'dictionary' ]
			'group' [ 'group' ]
				'subscribed properties' component 'subscribed properties'
			'matrix' [ 'matrix' ]
			'number' [ 'number' ]
			'reference' [ 'reference' ]
				'include reference' stategroup (
					'no'
					'yes' ['#include-reference']
				)
			'state group' [ 'stategroup' ]
				'states' [ '(' , ')' ] collection (
					'subscribed properties' [ '->' ] component 'subscribed properties'
				)
			'text' [ 'text' ]
			'file' ['file']
		)
	)
```

### update node

```js
'update node' [ '(' , ')' ]
	'properties' collection (
		'type' [ '->' ] stategroup (
			'group' [ 'group' ]
				'update node' component 'update node'
			'number'
				'type' stategroup (
					'integer' [ 'integer' ]
						'new value' number
					'natural' [ 'natural' ]
						'new value' number
				)
			'reference' [ 'reference' ]
				'new referenced node' text
			'state group' [ 'stategroup' ]
				'state' reference
				'type' stategroup (
					'set' [ 'set' ]
						'node' [ 'to' ] component 'initialize node'
						'delete node' component 'delete node'
					'update' [ 'update' ]
						'update node' component 'update node'
				)
			'text' [ 'text' ]
				'new value' text
			'file' ['file']
				'new token' text
				'new extension' [':'] text
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
							'update node' component 'update node'
						'remove' [ 'remove' ]
							'delete node' component 'delete node'
					)
				)
		)
	)
```

### initialize node

```js
'initialize node' [ '(' , ')' ]
	'groups' collection (
		'node' [ '->' 'group' ] component 'initialize node'
	)
	'texts' collection (
		'value' [ '->' 'text' ] text
	)
	'files' collection (
		'token' ['->' 'file'] text
		'extension' [':'] text
	)
	'numbers' collection (
		'type' [ '->' ] stategroup (
			'integer' [ 'integer' ]
				'value' number
			'natural' [ 'natural' ]
				'value' number
		)
	)
	'references' collection (
		'referenced node' [ '->' 'reference' ] text
	)
	'state groups' collection (
		'state' [ '->' 'stategroup' ] reference
		'node' component 'initialize node'
	)
	'dictionaries' collection (
		'entries' [ '->' 'dictionary' ] component 'new collection entries'
	)
	'matrices' collection (
		'entries' [ '->' 'matrix' ] component 'new collection entries'
	)
```

### new collection entries

```js
'new collection entries'
	'entries' collection (
		'node' component 'initialize node'
	)
```

### delete node

```js
'delete node'
```

### command arguments

```js
'command arguments' [ '(' , ')' ]
	'properties' collection (
		'type' [ '->' ] stategroup (
			'matrix' [ 'matrix' ]
				'entries' collection (
					'arguments' component 'command arguments'
				)
			'reference' [ 'reference' ]
				'entry' text
			'number' [ 'number' ]
				'number' number
			'text' [ 'text' ]
				'text' text
			'file' ['file']
				'token' text
				'extension' [':'] text
			'state group' [ 'stategroup' ]
				'state' [ '*' ] reference
				'arguments' component 'command arguments'
		)
	)```
