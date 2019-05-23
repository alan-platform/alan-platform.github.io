---
layout: doc
origin: datastore
language: consuming_interface_mapping
version: readimp.9
type: grammar
---


```js
'interfaces to imported interfaces mapping' [ 'interfaces' ] collection (
	'context keys' collection ( [ '(' , ')' ]
		'value' [ ':' 'text' '=' '.' ] reference
	)
	'imported interface' [ '=>' ] reference
)
```

```js
'imported interfaces to interfaces mapping' [ 'imported' 'interfaces' ] collection (
	'interface' [ '=>' ] reference
)
```

```js
'root' [ 'root' ] component 'sparse node mapping'
```

```js
'EQ member'
```

```js
'singular interface node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'singular interface node content path'
	)
```

```js
'command arguments' [ '(' , ')' ]
	'conditional' stategroup (
		'yes' [ '?' ]
			'state group' [ '@' ] reference
			'states' [ '(' , ')' ] collection ( [ '|' ]
				'arguments' component 'command arguments'
			)
		'no'
			'properties' collection (
				'type' [ ':' ] stategroup (
					'collection' [ 'collection' '=>' ]
						'collection' [ '@' ] reference
						'arguments' component 'command arguments'
					'number'
						'numerical type' stategroup (
							'integer' [ 'integer' ]
							'natural' [ 'natural' ]
						)
						'number' [ '=' '@' ] reference
					'text' [ 'text' ]
						'has constraint' stategroup (
							'no' ['=']
								'text' ['@'] reference
							'yes' ['=>']
								'text' ['@'] reference
						)
					'file' ['file']
						'file' [ '=' '@' ] reference
					'state group' [ 'stategroup' '=' ]
						'type' stategroup (
							'fixed'
								'state' reference
								'arguments' component 'command arguments'
							'mapped' [ 'switch' '(' ]
								'state group' [ '@' , ')' ] reference
								'mapping' ['(', ')'] collection ( [ '|' ]
									'mapped state' [ '=' ] reference
									'arguments' component 'command arguments'
								)
						)
				)
			)
	)
```

```js
'command implementation'
	'path' component 'singular interface node content path'
	'command' [ 'do' ] reference
	'command arguments' [ 'with' ] component 'command arguments'
```

```js
'sparse node mapping' [ '(' , ')' ]
	'attributes' collection (
		'type' [ ':' ] stategroup (
			'command' [ 'command' ]
				'interface' ['on'] reference //?
				'implementation' component 'command implementation'
			'property'
				'type' stategroup (
					'group' [ 'group' ]
						'mapping' component 'sparse node mapping'
					'collection' [ 'collection' ]
						'has key constraint' stategroup (
							'yes' ['=>']
							'no' ['=']
						)
						'interface' reference
						'path' component 'singular interface node content path'
						'collection' [ '.' ] reference
						'mapping' component 'dense node mapping'
					'number'
						'type' stategroup (
							'integer' [ 'integer' ]
							'natural' [ 'natural' ]
						)
						'interface' ['='] reference
						'path' component 'singular interface node content path'
						'number' [ '#' ] reference
					'text' [ 'text' ]
						'not collection key' component 'EQ member'
						'has constraint' stategroup (
							'yes' ['=>']
							'no' ['=']
						)
						'interface' reference
						'path' component 'singular interface node content path'
						'text' [ '.' ] reference
					'file' ['file' ]
						'interface' ['='] reference
						'path' component 'singular interface node content path'
						'file' ['/'] reference
					'state group' [ 'stategroup' ]
						'interface' ['=' 'switch' '('] reference
						'path' component 'singular interface node content path'
						'state group' [ '?',')' ] reference
						'states' [ '(' , ')' ] collection ( ['|']
							'state' [ '=' ] reference
							'mapping' component 'dense node mapping'
						)
				)
		)
	)
```

```js
'dense node mapping' [ '(' , ')' ]
	'attributes' collection (
		'type' stategroup (
			'referencer anchor' [ ':' 'reference-set' ]
			'log' [ ':' 'log' ]
			'command' [ ':' 'command' ]
				'implementation' stategroup (
					'internal'
					'external'
						'implementation' ['on'] component 'command implementation'
				)
			'property'
				'type' stategroup (
					'group' [ ':' 'group' ]
						'mapping' component 'dense node mapping'
					'collection'
						'type' stategroup (
							'elementary' [ ':' 'collection' ]
								'has key constraint' stategroup (
									'yes' ['=>']
									'no' ['=']
								)
								'path' component 'singular interface node content path'
								'collection' [ '.' ] reference
								'mapping' component 'dense node mapping'
							'derived' [ ':=' 'collection' '=' ]
						)
					'number'
						'type' stategroup (
							'elementary'
								'type' stategroup (
									'causal' [ ':' 'number' 'causal' ]
									'simple' [ ':' ]
										'type' stategroup (
											'integer' [ 'integer' ]
											'natural' [ 'natural' ]
										)
										'path' [ '=' ] component 'singular interface node content path'
										'number' [ '#' ] reference
								)
							'derived' [ ':=' 'number' ]
						)
					'text'
						'type' stategroup (
							'elementary' [ ':' 'text' ]
								'type' stategroup (
									'key' ['(key)']
										'is collection key' component 'EQ member'
									'value'
										'not collection key' component 'EQ member'
										'has constraint' stategroup (
											'yes' ['=>']
											'no' [ '=' ]
										)
										'path' component 'singular interface node content path'
										'text' [ '.' ] reference
								)
							'derived' [ ':=' 'text' ]
						)
					'file'
						'type' stategroup (
							'elementary' [ ':' 'file' ]
								'path' ['='] component 'singular interface node content path'
								'file' ['/'] reference
							'derived' [ ':=' 'file' ]
						)
					'state group'
						'type' stategroup (
							'elementary' [ ':' 'stategroup' ]
								'path' [ '=' 'switch' '(' ] component 'singular interface node content path'
								'state group' [ '?' , ')' ] reference
								'states' [ '(' , ')' ] collection ( [ '|' ]
									'state' [ '=' ] reference
									'mapping' component 'dense node mapping'
								)
							'derived' [ ':=' 'stategroup' ]
						)
				)
		)
	)
```
