---
layout: doc
origin: datastore
language: consumed_interfaces_mapping
version: app-extensions.1
type: grammar
---


```js
'interfaces to imported interfaces' [ 'interfaces' ] collection (
	'imported interface' ['=>'] reference
)
```

```js
'imported interfaces' [ 'imported-interfaces' ] collection (
	'interface' [ '=' ] reference
	'context keys' collection ( [ '(' , ')' ]
		'value' [ ':' 'text' '=' '.' ] reference
	)
	'mapping' component 'node type mapping'
)
```

```js
'EQ member'
```

```js
'argument mapping' [ '(' , ')' ]
	'conditional' stategroup (
		'yes' [ '?' ]
			'state group' [ '@' ] reference
			'states' [ '(' , ')' ] collection ( [ '|' ]
				'arguments' component 'argument mapping'
			)
		'no'
			'properties' collection (
				'type' [ ':' ] stategroup (
					'collection' [ 'collection' '=>' ]
						'collection' [ '@' ] reference
						'arguments' component 'argument mapping'
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
								'arguments' component 'argument mapping'
							'mapped' [ 'switch' '(' ]
								'state group' [ '@' , ')' ] reference
								'mapping' ['(', ')'] collection ( [ '|' ]
									'mapped state' [ '=' ] reference
									'arguments' component 'argument mapping'
								)
						)
				)
			)
	)
```

```js
'command mapping'
	'command' reference
	'argument mapping' ['with'] component 'argument mapping'
```

```js
'node type mapping' [ '(' , ')' ]
	'attributes' collection (
		'type' stategroup (
			'referencer anchor' [ ':' 'reference-set' ]
			'log' [ ':' 'log' ]
			'command' [ ':' 'command' ]
				'implementation' stategroup (
					'internal'
					'external'
						'mapping' [ 'do' ] component 'command mapping'
				)
			'property'
				'type' stategroup (
					'group'
						'type' stategroup (
							'elementary' [ ':' 'group' ]
								'group' [ '=' '+' ] reference
								'mapping' component 'node type mapping'
							'derived' [ ':=' 'group']
						)
					'collection'
						'type' stategroup (
							'elementary' [ ':' 'collection' ]
								'has key constraint' stategroup (
									'yes' ['=>']
									'no' ['=']
								)
								'collection' [ '.' ] reference
								'mapping' component 'node type mapping'
							'derived' [ ':=' 'collection' ]
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
										'number' ['=' '#'] reference
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
										'text' [ '.' ] reference
								)
							'derived' [ ':=' 'text' ]
						)
					'file'
						'type' stategroup (
							'elementary' [ ':' 'file' ]
								'file' ['=' '/'] reference
							'derived' [ ':=' 'file' ]
						)
					'state group'
						'type' stategroup (
							'elementary' [ ':' 'stategroup' '=' 'switch' '(' ]
								'state group' [ '?' , ')' ] reference
								'states' [ '(' , ')' ] collection ( [ '|' ]
									'state' [ '=' ] reference
									'mapping' component 'node type mapping'
								)
							'derived' [ ':=' 'stategroup' ]
						)
				)
		)
	)
```
