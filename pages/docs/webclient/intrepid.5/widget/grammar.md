---
layout: doc
origin: webclient
language: widget
version: intrepid.5
type: grammar
---


## root


### binding context

```js
	'binding context' stategroup (
		'none' [ 'static' ]
		'select'
			'binding' [ 'binding' ] reference
			'switch client binding context' stategroup (
				'yes' [ 'on' ]
					'constrained on containing binding' stategroup (
						'yes'
							'type path' component 'client binding type path'
							'instance binding' reference
						'no' [ 'unconstrained' ]
							'instance binding' reference
					)
				'no'
			)
	)
```

### widget

```js
	'widget' component 'widget configuration node'
```

### invalid implementation context

```js
	'invalid implementation context' component 'widget implementation context'
```

### control binding

```js
	'control binding' component 'control binding'
```

## component rules


### client binding type path

```js
	'client binding type path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state'
						'state group' [ '?' ] reference
						'state' [ '*' ] reference
					'collection'
						'collection' [ '.' ] reference
				)
				'tail' component 'client binding type path'
		)
```

### widget configuration node

```js
	'widget configuration node' [ '(' , ')' ]
		'attributes' collection (
			'switch client binding context' stategroup (
				'yes' [ 'on' ]
					'constrained on containing binding' stategroup (
						'yes'
							'type path' component 'client binding type path'
							'instance binding' reference
						'no' [ 'unconstrained' ]
							'instance binding' reference
					)
				'no'
			)
			'type' [ '->' ] stategroup (
				'widget' [ 'widget' ]
				'window' [ 'window' ]
					'node' component 'widget configuration node'
				'view' [ 'view' ]
				'inline view' [ 'inline' 'view' ]
				'configuration' [ 'configuration' ]
					'type' stategroup (
						'number' [ 'number' ]
						'text' [ 'text' ]
						'list' [ 'list' ]
							'node' component 'widget configuration node'
						'state group' [ 'stategroup' ]
							'states' [ '(' , ')' ] collection (
								'node' [ '->' ] component 'widget configuration node'
							)
					)
				'binding' [ 'binding' ]
					'constrained on containing binding' stategroup (
						'yes'
							'type path' component 'client binding type path'
							'instance binding' reference
						'no' [ 'unconstrained' ]
							'instance binding' reference
					)
					'node' component 'widget configuration node'
			)
		)
```

### client context constraint

```js
	'client context constraint'
```

### widget implementation context

```js
	'widget implementation context'
```

### widget implementation context parent path

```js
	'widget implementation context parent path'
		'has parent step' stategroup (
			'no'
			'yes' [ '^' ]
				'tail' component 'widget implementation context parent path'
		)
```

### control binding

```js
	'control binding'
		'binding type' stategroup (
			'let declaration'
				'path' component 'widget implementation context parent path'
				'declaration' [ '@' ] reference
			'static'
				'control' [ 'control' ] reference
				'node binding' component 'widget implementation node'
			'window'
				'window' [ 'window' ] reference
				'control binding' component 'control binding'
			'widget'
				'select context' stategroup (
					'no'
					'yes' [ 'on' ]
						'context' component 'context selection'
				)
				'widget' [ 'widget' ] reference
			'configuration'
				'switch context' stategroup (
					'no'
					'yes' [ 'configuration' ]
						'context selection path' [ '(', ')' ] component 'context selection path'
				)
				'state group' [ '?' ] reference
				'states' [ '(' , ')' ] collection (
					'control binding' [ '->' ] component 'control binding'
				)
			'context node binding'
				'context' component 'context selection'
				'type' stategroup (
					'state group' [ '?' ]
						'state group property' reference
						'states' [ '(' , ')' ] collection (
							'switch context' stategroup (
								'no' [ '=>' ]
								'state node' [ '->' ]
							)
							'control binding' component 'control binding'
						)
				)
			'inline view' [ 'inline' 'view' ]
				'context' component 'context selection'
				'view' reference
		)
```

### entries list

```js
	'entries list'
		'has steps' stategroup (
			'no' [ ']' ]
			'yes'
				'node binding' component 'widget implementation node'
				'tail' component 'entries list'
		)
```

### context selection

```js
	'context selection'
		'change context' stategroup (
			'no' [ '$' ]
			'yes'
				'to' stategroup (
					'engine state' [ 'engine' ]
						'engine state binding' reference
					'configuration'
						'path' [ '(' , ')' ] component 'context selection path'
				)
		)
```

### context selection path

```js
	'context selection path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'unconstrained configuration attribute'
						'configuration attribute' [ 'unconstrained' '::' ] reference
					'constrained configuration attribute'
						'configuration attribute' [ '::' ] reference
					'client binding'
						'binding' [ 'switch' 'to' ] reference
				)
				'tail' component 'context selection path'
		)
```

### instruction selection

```js
	'instruction selection'
		'path' component 'widget implementation context parent path'
		'configuration attribute type' stategroup (
			'binding'
				'context' component 'context selection'
				'instruction' [ '>>' ] reference
				'instruction argument' stategroup (
					'none'
					'number' [ 'number' ]
						'transform' stategroup (
							'no'
							'yes' [ 'transform' ]
								'from' stategroup (
									'text'
										'transformer' reference
									'number' [ '#' ]
										'transformer' reference
								)
						)
					'text' [ 'text' ]
					'file' [ 'file' ]
					'view' [ '(' , ')' ]
						'view configuration' reference
				)
			'configuration'
				'instruction' stategroup (
					'set state' [ 'set' 'state' ]
						'state group' reference
						'state' [ ':' ] reference
						'node' component 'instruction argument configuration node'
					'set number' [ 'set' 'number' ]
						'number' reference
					'set text' [ 'set' 'text' ]
						'text' reference
				)
		)
```

### instruction argument configuration node

```js
	'instruction argument configuration node' [ '(' , ')' ]
		'attributes' collection (
			'type' stategroup (
				'configuration'
					'type' stategroup (
						'number'
							'value' number
						'state group'
							'state' reference
							'node' component 'instruction argument configuration node'
					)
			)
		)
```

### instruction list

```js
	'instruction list'
		'instruction selection' component 'instruction selection'
		'has steps' stategroup (
			'no'
			'yes' [ ',' ]
				'tail' component 'instruction list'
		)
```

### widget implementation node

```js
	'widget implementation node' [ '(' , ')' ]
		'context' component 'widget implementation context'
		'let declarations' collection ( [ 'let' ]
			'control binding' [ '->' 'markup' ] component 'control binding'
		)
		'attributes' collection (
			'type' [ '->' ] stategroup (
				'instruction' [ 'instruction' ]
					'type' stategroup (
						'singular'
							'instruction selection' component 'instruction selection'
						'list'
							'instruction list' [ '[' , ']' ] component 'instruction list'
					)
				'markup' [ 'markup' ]
					'control binding' component 'control binding'
				'property'
					'type' stategroup (
						'dictionary' [ 'dictionary' ]
							'path' component 'widget implementation context parent path'
							'dictionary binding' component 'dictionary binding'
						'list' [ 'list' ]
							'binding type' stategroup (
								'static'
									'entries' [ '[' ] component 'entries list'
								'configuration'
									'type' stategroup (
										'list'
											'bound list' [ '|' ] reference
									)
									'node binding' component 'widget implementation node'
								'widget binding'
									'context' component 'context selection'
									'collection property' ['.'] reference
									'node binding' component 'widget implementation node'
							)
						'number' [ 'number' ]
							'path' component 'widget implementation context parent path'
							'number binding' component 'number binding'
						'text' [ 'text' ]
							'path' component 'widget implementation context parent path'
							'text binding' component 'text binding'
						'state group' [ 'stategroup' ]
							'path' component 'widget implementation context parent path'
							'binding' component 'state group binding'
					)
			)
		)
```

### state group binding

```js
	'state group binding'
		'binding type' stategroup (
			'static'
				'state' reference
				'binding' component 'widget implementation node'
			'configuration' [ '?' ]
				'bound to' reference
				'states' [ '(' , ')' ] collection (
					'switch context' stategroup (
						'no' [ '=>' ]
						'state node' ['->']
					)
					'state binding' component 'state group binding'
				)
			'widget binding'
				'context' component 'context selection'
				'state group binding' [ '?' ] reference
				'states configuration' [ '(' , ')' ] collection (
					'switch context' stategroup (
						'no' [ '=>' ]
						'state node' ['->']
					)
					'state binding' component 'state group binding'
				)
		)
```

### number binding

```js
	'number binding'
		'binding type' stategroup (
			'static number'
				'value' number
			'current time' [ 'current' 'time' ]
				'throttle' stategroup (
					'yes'
						'interval' [ 'interval' ':' ] number
					'no'
				)
			'configuration'
				'type' stategroup (
					'number'
						'bound number' [ ':' ] reference
					'state group'
						'state group' [ '?' ] reference
						'states' [ '(' , ')' ] collection (
							'switch context' stategroup (
								'no' [ '=>' ]
								'state node' ['->']
							)
							'number binding' component 'number binding'
						)
				)
			'widget binding'
				'context' component 'context selection'
				'type' stategroup (
					'number' [ '#' ]
						'property' reference
					'state group'
						'property' [ '?' ] reference
						'states' [ '(' , ')' ] collection (
							'switch context' stategroup (
								'no' [ '=>' ]
								'state node' ['->']
							)
							'number binding' component 'number binding'
						)
				)
		)
		'transform' stategroup (
			'no'
			'yes' [ 'transform' ]
				'transformer' reference
		)
```

### dictionary binding

```js
	'dictionary binding'
		'binding type' stategroup (
			'empty' [ 'empty' ]
			'widget binding'
				'context' component 'context selection'
				'collection property' ['.'] reference
				'node binding' component 'widget implementation node'
			'configuration state group'
				'state group' [ '?' ] reference
				'states' [ '(' , ')' ] collection (
					'binding' [ '->' ] component 'dictionary binding'
				)
			'state group binding'
				'context' component 'context selection'
				'property' ['?'] reference
				'states' [ '(', ')' ] collection (
					'switch context' stategroup (
						'no' [ '=>' ]
						'state node' ['->']
					)
					'binding' component 'dictionary binding'
				)
		)
```

### text binding

```js
	'text binding'
		'binding type' stategroup (
			'static'
				'text' text
			'configuration'
				'type' stategroup (
					'text'
						'bound text' [ ':' ] reference
					'number'
						'number' [ '#' ] reference
						'format' stategroup (
							'no'
							'yes' [ 'format' ]
								'formatter' reference
						)
					'state group'
						'state group' [ '?' ] reference
						'states' [ '(' , ')' ] collection (
							'switch context' stategroup (
								'no' [ '=>' ]
								'state node' ['->']
							)
							'text binding' component 'text binding'
						)
				)
			'widget binding'
				'context' component 'context selection'
				'type' stategroup (
					'text'
						'type' stategroup (
							'key' [ '.}' ]
							'reference' [ '>' ]
								'property' reference
							'text' [ ':' ]
								'property' reference
						)
						'format' stategroup (
							'no'
							'yes' [ 'format' ]
								'formatter' reference
						)
					'number' [ '#' ]
						'property' reference
						'format' stategroup (
							'no'
							'yes' [ 'format' ]
								'formatter' reference
						)
					'state group'
						'property' [ '?' ] reference
						'states' [ '(' , ')' ] collection (
							'switch context' stategroup (
								'no' [ '=>' ]
								'state node' [ '->' ]
							)
							'text binding text' component 'text binding'
						)
				)
			'concatenation'
				'strings' [ '[' , ']' ] component 'string list'
		)
```

### string list

```js
	'string list'
		'text binding' component 'text binding'
		'has steps' stategroup (
			'no'
			'yes' [ ',' ]
				'tail' component 'string list'
		)
```
