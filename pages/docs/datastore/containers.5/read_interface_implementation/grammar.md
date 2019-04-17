---
layout: doc
origin: datastore
language: read_interface_implementation
version: containers.5
type: grammar
---


```js
'application root node' [ '(' , ')' ] component 'interface context id path'
```

```js
'root' [ 'root' ] component 'read interface implementation node'
```

```js
'EQ member'
```

```js
'dereference'
	'dereference' stategroup ( 'yes' )
```

```js
'interface context id path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection entry' [ '.' ]
					'collection' reference
					'id' [ ':' '@' ] reference
				'group' [ '+' ]
					'group' reference
				'state' [ '?']
					'state group' reference
					'state' [ '*' ] reference
			)
			'tail' component 'interface context id path'
	)
```

```js
'read interface implementation node' [ '(' , ')' ]
	'attributes' collection (
		'type' [ '->' ] stategroup (
			'command' [ 'command' ]
				'implementation' [ 'implementation' ] component 'read interface command implementation'
			'property'
				'type' stategroup (
					'collection' [ 'collection' ]
						'type' stategroup (
							'empty' ['empty']
							'dynamic'
								'type' stategroup (
									'dictionary'
									'matrix'
										'referencer' [ '(' , ')' ] group (
											'head' component 'singular interface implementation node path'
											'collection' [ '.' ] reference
											'tail' component 'interface implementation node content path'
										)
								)
								'path' component 'singular node content path'
								'collection' ['.'] reference
								'node' component 'read interface implementation node'
						)
					'group' [ 'group' ]
						'node' component 'read interface implementation node'
					'number'
						'type' stategroup (
							'static'
								'type' stategroup (
									'integer' [ 'integer' ]
										'value' number
									'natural' [ 'natural' ]
										'value' number
								)
							'dynamic'
								'type' stategroup (
									'integer' [ 'integer' ]
									'natural' [ 'natural' ]
								)
								'path' component 'singular node content path'
								'number' [ ':' ] reference
						)
					'reference' [ 'reference' ]
						'referencer' [ '(' , ')' ] group (
							'head' component 'singular interface implementation node path'
							'collection' [ '.' ] reference
							'tail' component 'interface implementation node content path'
						)
						'path' component 'singular node content path'
						'text' [ ':' ] reference
						'dereference' component 'dereference'
					'state group' [ 'stategroup' ]
						'type' stategroup (
							'static'
								'state' [ 'set' 'to' ] reference
								'node' component 'read interface implementation node'
							'dynamic'
								'path' component 'singular node content path'
								'state group' [ ':' ] reference
								'states' [ '(' , ')' ] collection (
									'state' [ '->' ] reference
									'node' component 'read interface implementation node'
								)
						)
					'text' [ 'text' ]
						'type' stategroup (
							'static'
								'value' text
							'dynamic'
								'path' component 'singular node content path'
								'text' [ ':' ] reference
						)
					'file' ['file']
						'path' component 'singular node content path'
						'file' [':'] reference
				)
	)
)
```

```js
'singular node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'singular node content path'
	)
```

```js
'interface implementation node content path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state' [ '?' ]
					'state group' reference
					'state' [ '*' ] reference
				'group' [ '+' ]
					'group' reference
			)
			'tail' component 'interface implementation node content path'
	)
```

```js
'read interface command implementation'
	'conditional' stategroup (
		'yes' [ '?' ]
			'state group' [ '@' ] reference
			'states' [ '(' , ')' ] collection (
				'implementation' [ '->' ] component 'read interface command implementation'
			)
		'no' [ 'execute' ]
			'command' [ ':' ] reference
			'command arguments' [ 'with' ] component 'command arguments'
	)
```

```js
'command arguments' [ '(' , ')' ]
	'properties' collection (
		'type' [ '->' ] stategroup (
			'collection' [ 'collection' ]
				'collection' [ '@' ] reference
				'command arguments' component 'command arguments'
			'number'
				'numerical type' stategroup (
					'integer' [ 'integer' ]
					'natural' [ 'natural' ]
				)
				'number' [ '@' ] reference
			'text'
				'value provision' stategroup (
					'key' ['text' '@key']
							'is collection key' component 'EQ member'
					'value'
						'not collection key' component 'EQ member'
						'has constraint' stategroup (
							'no' [ 'text' ]
								'text' [ '@' ] reference
							'yes' [ 'reference' ]
								'text' [ '@' ] reference
						)
				)
			'file' ['file']
				'file' [ '@' ] reference
			'state group' [ 'stategroup' ]
				'type' stategroup (
					'fixed'
						'state' reference
						'command arguments' component 'command arguments'
					'map' ['map']
						'state group' ['@'] reference
						'mapping' ['(', ')'] collection (
							'mapped state' [ '->' ] reference
							'command arguments' component 'command arguments'
						)
				)
		)
	)
```

```js
'singular interface implementation node path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection parent' [ '.^' ]
				'static state parent' [ '??^' ] //Hmm...
				'dynamic state parent' [ '?^' ]
				'group parent' [ '+^' ]
				'group' [ '+' ]
					'group' reference
				'reference' [ '>' ]
					'reference' reference
			)
			'tail' component 'singular interface implementation node path'
	)
```
