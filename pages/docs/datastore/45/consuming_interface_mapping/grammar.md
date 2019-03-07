---
layout: doc
origin: datastore
language: consuming_interface_mapping
version: 45
type: grammar
---


## root


### interfaces to imported interfaces mapping

```js
'interfaces to imported interfaces mapping' [ 'interfaces' ] collection (
	'context keys' collection ( [ '(' , ')' ]
		'value' [ ':' 'text' '=' '.' ] reference
	)
	'imported interface' [ '=>' ] reference
)
```

### imported interfaces to interfaces mapping

```js
'imported interfaces to interfaces mapping' [ 'imported' 'interfaces' ] collection (
	'interface' [ '=>' ] reference
)
```

### root

```js
'root' [ 'root' ] component 'sparse node mapping'
```

## component rules


### EQ member

```js
'EQ member'
```

### singular interface node content path

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

### command arguments

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

### command implementation

```js
'command implementation'
	'path' component 'singular interface node content path'
	'command' [ 'do' ] reference
	'command arguments' [ 'with' ] component 'command arguments'
```

### sparse node mapping

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

### dense node mapping

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
