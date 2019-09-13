---
layout: doc
origin: webclient
language: widget
version: laforge.4
type: grammar
---


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

```js
'widget' component 'widget configuration node'
```

```js
'invalid implementation context' component 'widget implementation context'
```

```js
'root context' component 'valid widget implementation context'
```

```js
'root attribute location' component 'control attribute location'
```

```js
'switch block' component 'state switch'
```

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
				'binding'
					'instance binding' reference
			)
			'tail' component 'client binding type path'
	)
```

```js
'configuration attribute persistence'
	'persist' stategroup (
		'yes' [ '@persist' ]
			'per session' stategroup (
				'yes' ['session']
				'no'
			)
			'per entry' stategroup (
				'yes' ['entry']
				'no'
			)
		'no'
	)
```

```js
'widget configuration node' [ '{' , '}' ]
	'attributes' collection (
		'switch client binding context' stategroup (
			'yes' [ 'on' ]
				'constrained on containing binding' stategroup (
					'yes'
						'type path' component 'client binding type path'
					'no' [ 'unconstrained' ]
						'instance binding' reference
				)
			'no'
		)
		'type' [ ':' ] stategroup (
			'widget' [ 'widget' ]
			'window' [ 'window' ]
				'node' component 'widget configuration node'
			'view' [ 'view' ]
			'inline view' [ 'inline' 'view' ]
			'configuration' [ 'configuration' ]
				'type' stategroup (
					'number' [ 'number' ]
						'persistence' component 'configuration attribute persistence'
					'text' [ 'text' ]
						'persistence' component 'configuration attribute persistence'
					'list' [ 'list' ]
						'node' component 'widget configuration node'
					'state group' [ 'stategroup' ]
						'persistence' component 'configuration attribute persistence'
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

```js
'widget implementation context'
```

```js
'valid widget implementation context'
	'context' component 'widget implementation context'
```

```js
'attribute location'
```

```js
'control attribute location'
	'invalid attribute location' component 'attribute location'
```

```js
'widget implementation context parent path'
	'has parent step' stategroup (
		'no'
		'yes' [ '^' ]
			'tail' component 'widget implementation context parent path'
		'root' [ 'root' ]
	)
```

```js
'control binding'
	'binding type' stategroup (
		'let declaration'
			'path' [ '@' ] component 'widget implementation context parent path'
			'on widget implementation node' stategroup (
				'yes'
					'declaration' reference
			)
		'static'
			'control' [ 'control' ] reference
			'node binding' component 'widget implementation node'
		'window'
			'window' [ 'window' ] reference
			'widget context' component 'valid widget implementation context'
			'control binding' component 'control binding'
		'widget'
			'context' component 'context selection'
			'widget' [ 'widget' ] reference
		'inline view' [ 'inline' 'view' ]
			'context' component 'context selection'
			'view' reference
	)
```

```js
'entries list'
	'has steps' stategroup (
		'no'
		'yes'
			'node binding' component 'widget implementation node'
			'tail' component 'entries list'
	)
```

```js
'context selection'
	'change context to' stategroup (
		'engine state' [ 'engine' ]
			'engine state binding' reference
		'other context'
			'parent path' component 'widget implementation context parent path'
			'path' component 'context selection path'
	)
```

```js
'bound context selection'
	'context' component 'context selection'
	'cast' stategroup (
		'to binding' [ '$' ]
	)
```

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

```js
'instruction selection'
	'configuration attribute type' stategroup (
		'binding'
			'context' component 'bound context selection'
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
		'collection'
			'type' stategroup (
				'configuration'
					'context' component 'context selection'
					'list' ['='] reference
					'widget context' component 'valid widget implementation context'
					'instruction selection' component 'instruction selection'
				'binding'
					'context' component 'bound context selection'
					'collection property' ['.'] reference
					'widget context' component 'valid widget implementation context'
					'instruction selection' component 'instruction selection'
			)
		'switch'
			'switch' component 'state switch'
		'ignore' ['ignore']
		'configuration'
			'context' component 'context selection'
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

```js
'instruction argument configuration node' [ '(' , ')' ]
	'attributes' collection (
		'type' stategroup (
			'configuration'
				'type' [':'] stategroup (
					'number' ['number']
						'value type' stategroup (
							'static'
								'value' number
							'instruction argument' ['argument']
						)
					'text' ['text']
						'value type' stategroup (
							'static'
								'value' text
							'instruction argument' ['argument']
						)
					'state group' ['state']
						'state' reference
						'node' component 'instruction argument configuration node'
				)
		)
	)
```

```js
'instruction list'
	'instruction selection' component 'instruction selection'
	'has steps' stategroup (
		'no'
		'yes' [ ',' ]
			'tail' component 'instruction list'
	)
```

```js
'widget implementation node' [ '{' , '}' ]
	'define context' stategroup (
		'yes' [ 'define' 'context' ]
			'widget context' component 'valid widget implementation context'
			'context' component 'context selection'
			'let declarations' collection ( [ 'let' ]
				'let declaration attribute location' component 'control attribute location'
				'switch block' [ ':' ] component 'state switch'
			)
		'no'
	)
	'attributes' collection (
		'location' component 'attribute location'
		'switch block' [':'] component 'state switch'
	)
```

```js
'state switch'
	'type' stategroup (
		'attribute'
			'control attribute type' stategroup (
				'instruction' [ 'instruction' ]
					'type' stategroup (
						'singular'
							'instruction' component 'instruction selection'
						'list'
							'instruction list' [ '[' , ']' ] component 'instruction list'
					)
				'markup' [ 'markup' ]
					'control binding' component 'control binding'
				'property'
						'type' stategroup (
							'dictionary' [ 'collection' ]
								'binding type' stategroup (
									'empty' [ 'empty' ]
									'widget binding'
										'context' component 'bound context selection'
										'collection property' ['.'] reference
										'widget context' component 'valid widget implementation context'
										'node binding' component 'widget implementation node'
								)
							'list' [ 'list' ]
								'binding type' stategroup (
									'static'
										'entries' [ '[' , ']' ] component 'entries list'
									'configuration'
										'context' component 'context selection'
										'list' [ '=' ] reference
										'widget context' component 'valid widget implementation context'
										'node binding' component 'widget implementation node'
									'widget binding'
										'context' component 'bound context selection'
										'collection property' ['.'] reference
										'widget context' component 'valid widget implementation context'
										'node binding' component 'widget implementation node'
							)
							'number' ['number']
								'binding type' stategroup (
									'static number'
										'value' number
									'current time' [ 'current' 'time' ]
										'throttle' stategroup (
											'yes'
												'interval' [ 'interval:' ] number
											'no'
										)
									'configuration'
										'context' component 'context selection'
										'bound number' [ '=' ] reference
									'widget binding'
										'context' component 'bound context selection'
										'property' [ '#' ] reference
								)
								'transform' stategroup (
									'no'
									'yes' [ 'transform' ]
										'transformer' reference
								)
							'text' [ 'text' ]
								'type' stategroup (
									'binding'
										'text binding' component 'text binding'
									'concatenation'
										'strings' [ '[' , ']' ] component 'string list'
								)
							'state group' [ 'state' ]
								'state' reference
								'binding' component 'widget implementation node'
						)
			)
		'control'
			'control binding' component 'control binding'
		'switch'
			'type' stategroup (
				'configuration'
					'context' component 'context selection'
					'state group' [ '?' ] reference
					'states' [ '(' , ')' ] collection ( [ '|' ]
						'state context' component 'valid widget implementation context'
						'next' [ '->' ] component 'state switch'
					)
				'binding'
					'context' component 'bound context selection'
					'property' [ '?' ] reference
					'states' [ '(' , ')' ] collection ( [ '|' ]
						'state context' component 'valid widget implementation context'
						'next' ['->'] component 'state switch'
					)
			)
	)
```

```js
'text binding'
	'binding type' stategroup (
		'static'
			'text' text
		'phrase'
			'phrase' [ 'phrase' ] reference
		'configuration'
			'context' component 'context selection'
			'type' stategroup (
				'text'
					'bound text' [ '=' ] reference
				'number'
					'number' [ 'configuration' '#' ] reference
					'format' stategroup (
						'no'
						'yes' [ 'format' ]
							'formatter' reference
					)
			)
		'widget binding'
			'context' component 'bound context selection'
			'type' stategroup (
				'text'
					'type' stategroup (
						'key' [ '.key' ]
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
			)
	)
```

```js
'string list'
	'text binding' component 'text binding'
	'has steps' stategroup (
		'no'
		'yes' [ ',' ]
			'tail' component 'string list'
	)
```
