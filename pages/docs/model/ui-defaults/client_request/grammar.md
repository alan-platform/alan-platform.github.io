---
layout: doc
origin: model
language: client_request
version: ui-defaults
type: grammar
---


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
							'text' [':'] reference
							'include reference' stategroup (
								'no'
								'yes' ['#include-reference']
							)
						'expression' [ '(' , ')' ]
							'expression' component 'text expression'
					)
					'filtering' stategroup (
						'simple' [ '(' , ')' ]
							'expression' component 'filter expression'
						'reference' [ '(' , ')' ]
							'dereference' component 'dereference'
							'referenced node' component 'id path'
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
			'collection' ['from' ]
				'graph' reference
		)
	'acyclic graph list query'
		'context node' component 'id path'
		'entry points' ['select'] component 'entry point path'
		'collection' component 'ancestor path'
		'collection type' stategroup (
			'collection' ['collection']
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
						'text' reference
					'state group' ['stategroup']
						'state group' reference
				)
			)
		)
	'denseness query'
		'context node' ['denseness'] component 'id path'
		'constraint' stategroup ('constraint')
		'collection' ['.'] reference
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
								'text' [ '>' ] reference
								'output type' stategroup (
									'referenced node'
									'output parameter' [ '$' ]
										'output parameter' reference
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
								'text' [ '>' ] reference
								'output type' stategroup (
									'referenced node'
									'output parameter' [ '$' ]
										'output parameter' reference
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

```js
'dereference'
	'is dereferenceable' stategroup ( 'dereference' )
```

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

```js
'id path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection entry' [ '.' ]
					'collection' reference
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

```js
'collection path'
	'has steps' stategroup (
		'no'
		'yes'
			'head' component 'conditional child path'
			'collection' [ '.' ] reference
			'tail' component 'collection path'
	)
```

```js
'entry point path'
	'has steps' stategroup (
		'no'
			'text' ['>'] reference
			'dereference' component 'dereference'
		'yes'
			'head' component 'conditional child path'
			'collection' ['.'] reference
			'tail' component 'entry point path'
	)
```

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
				'collection' [ '.' ]
					'collection' reference
			)
			'tail' component 'plural path'
	)
```

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

```js
'singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection parent' [ '.^' ]
				'state parent' [ '?^' ]
				'group parent' [ '+^' ]
				//'state group output parameter' [ '?' ]
				//	'state group' reference
				//	'output parameter' [ '$' ] reference
				'reference' [ '>' ]
					'text' reference
					'dereference' component 'dereference'
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'singular path'
	)
```

```js
'node type path'
	'steps' component 'node type path step'
```

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
				'collection' [ '.' ]
					'collection' reference
			)
			'tail' component 'node type path step'
	)
```

```js
'aggregate2'
	'head' component 'singular path'
	'collection' ['.'] reference
	'tail' component 'conditional path'
```

```js
'number aggregate2' [ '(' , ')' ]
	'aggregate' [ '#' ] component 'aggregate2'
	'property name' [ ':' ] reference
```

```js
'signed number property2'
	'path' [ '#' ] component 'singular path'
	'sign' [ ':' ] stategroup (
		'negative' [ '-' ]
		'positive'
	)
	'property name' reference
```

```js
'signed number property list'
```

```js
'has element' stategroup (
	'no'
	'yes'
	'signed number property' component 'signed number property2'
	'tail' component 'signed number property list'
)
```

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

```js
'singular text expression'
	'type' stategroup (
		'static'
			'string' text
		'dynamic'
			'path' component 'singular path'
			'text' [ ':' ] reference
	)
```

```js
'singular text expression list'
```

```js
'has element' stategroup (
	'no'
	'yes'
	'singular text expression' component 'singular text expression'
	'tail' component 'singular text expression list'
)
```

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

```js
'subscribed properties' [ '(' , ')' ]
	'properties' collection (
		'type' [ '->' ] stategroup (
			'collection' [ 'collection' ]
			'group' [ 'group' ]
				'subscribed properties' component 'subscribed properties'
			'number' [ 'number' ]
			'state group' [ 'stategroup' ]
				'states' [ '(' , ')' ] collection (
					'subscribed properties' [ '->' ] component 'subscribed properties'
				)
			'text' [ 'text' ]
				'include reference' stategroup (
					'no'
					'yes' ['#include-reference']
				)
			'file' ['file']
		)
	)
```

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
			'collection' [ 'collection' ]
				'entries' collection (
					'type' stategroup (
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

```js
'initialize node' [ '(' , ')' ]
	'groups' collection (
		'node' [ '->' 'group' ] component 'initialize node'
	)
	'texts' collection (
		'value' ['->' 'text'] text
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
	'state groups' collection (
		'state' [ '->' 'stategroup' ] reference
		'node' component 'initialize node'
	)
	'collections' collection (
		'entries' [ '->' 'collection' ] collection (
			'node' component 'initialize node'
		)
	)
```

```js
'delete node'
```

```js
'command arguments' [ '(' , ')' ]
	'properties' collection (
		'type' [ '->' ] stategroup (
			'collection' [ 'collection' ]
				'entries' collection (
					'arguments' component 'command arguments'
				)
			'number'
				'type' stategroup (
					'integer' [ 'integer' ]
						'value' number
					'natural' [ 'natural' ]
						'value' number
				)
			'text' [ 'text' ]
				'text' text
			'file' ['file']
				'token' text
				'extension' [':'] text
			'state group' [ 'stategroup' ]
				'state' [ '*' ] reference
				'arguments' component 'command arguments'
		)
	)
```
