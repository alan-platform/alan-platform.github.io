---
layout: doc
origin: webclient
language: views
version: janeway.5
type: grammar
---


## root


### dependencies

```js
'dependencies' collection ( [ 'using' ] )
```

### views

```js
'views' collection indent (
	'widget binding context' stategroup (
		'node context'
		'view context'
			'title' [ 'as' ] reference
	)
	'invalid query context' component 'query context'
	'node type' [ 'on' ] component 'gui node type path'
	'queries' [ ] collection ( [ 'query' ]
		'tag' component 'query context'
		'context' [ 'from' ] stategroup (
			'node'
				'switch' stategroup (
					'current'
						'query context' component 'query property context path'
					'root' [ 'root' ]
				)
				'path' [ 'path' ] component 'query path'
			'candidates' [ 'candidates' 'of' ]
				'of' stategroup (
					'reference'
						'type' stategroup (
							'key' [ 'matrix' 'key' ]
							'reference property'
								'property context' component 'query property context path'
								'property' [ 'reference:' ] reference
							'text link property'
								'property context' component 'query property context path'
								'property' [ 'text' 'link:' ] reference
							'key link' [ 'key' 'link' ]
						)
					'command' [ 'command' ]
						'property context' component 'query property context path'
						'command property' reference
						'command parameter context' component 'command parameters type path'
						'type' stategroup (
							'reference'
								'reference parameter' [ 'reference:' ] reference
						)
				)
		)
		'todo filter' stategroup (
			'yes' ['where' 'has-todo']
				'path' ['(',')'] component 'gui conditional path'
			'no'
		)
		'maximum amount of entries' [ 'limit:' ] number
		'has columns' stategroup has 'columns' first 'first' 'yes' 'no'
		'columns' [ '[' , ']' ] collection order 'column order' indent (
			'has successor' stategroup has successor 'successor' 'yes' 'no'
			'name' reference
			'column type' stategroup (
				'id' [ 'id' ]
				'content'
			)
			'path' [ '->' ] component 'gui conditional path'
			'type' [ ':' ] stategroup (
				'text'
					'type' stategroup (
						'functional id' [ 'key' ]
						'property'
							'text' [ 'text' ] reference
					)
					'has filter' stategroup (
						'no'
						'yes' [ 'filter' ]
							'criteria' text
					)
				'file' [ 'file' ]
					'file' reference
					'has filter' stategroup (
						'no'
					)
				'number'
					'number' [ 'number' ] reference
					'unit' text
					'has decimal point translation' stategroup (
						'yes'[ '<<' ]
						'translation' number
						'no'
					)
					'has filter' stategroup (
						'no'
						'yes' [ 'filter' ]
							'operator selected' stategroup (
								'no'
								'yes'
									'operator' stategroup (
										'smaller than' [ '<' ]
										'smaller than or equal to' [ '<=' ]
										'equal to' [ '=' ]
										'greater than or equal to' [ '>=' ]
										'greater than' [ '>' ]
									)
							)
							'initial criteria' stategroup (
								'none' [ 'none' ]
								'yes'
									'source' stategroup (
										'now' [ 'now' ]
											'has offset' stategroup (
												'none'
												'yes'
													'offset' [ '+' ] number
											)
										'static'
											'number' number //fixme nest criteria in operator selected
									)
							)
						)
				'reference'
					'navigable' stategroup (
						'yes'
							'type' stategroup (
								'functional id' [ 'matrix' 'key' ]
								'property'
									'reference' [ 'reference' ] reference
							)
						'no'
							'type' stategroup (
								'functional id' [ 'matrix' 'key' 'text' ]
								'property'
									'reference' [ 'reference' 'text' ] reference
							)
					)
					'has filter' stategroup (
						'no'
						'yes' [ 'filter' ]
							'initialize with' stategroup (
								'current id path'
								'constraint' component 'node constraint'
							)
					)
				'state group'
					'state group' [ 'stategroup' ] reference
					'has filter' stategroup (
						'no'
						'yes' [ 'filter' ]
							'filter enabled' stategroup (
								'yes' [ 'enabled' ]
								'no' [ 'disabled' ]
							)
							'states' [ '?' ] collection indent ( ['|']
								'is selected' stategroup (
									'no'
									'yes' [ 'selected' ]
								)
							)
					)
			)
		)
	)
	'widget' reference
	'configuration node' component 'gui widget configuration node'
)
```

## component rules


### node constraint

```js
'node constraint'
```

### query context

```js
'query context'
```

### command parameters type path

```js
'command parameters type path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state group'
					'property' [ '?' ] reference
					'state' [ '|' ] reference
				'matrix'
					'property' [ '%' ] reference
			)
			'tail' component 'command parameters type path'
	)
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

### query property context path

```js
'query property context path'
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
			'tail' component 'query property context path'
	)
```

### gui node type path

```js
'gui node type path'
	'steps' component 'gui node type path step'
```

### gui widget configuration list

```js
'gui widget configuration list'
	'has steps' stategroup (
		'no' [ ']' ]
		'yes'
			'configuration' component 'gui widget configuration node'
			'tail' component 'gui widget configuration list'
	)
```

### view context parent path

```js
'view context parent path'
	'type' stategroup (
		'state parent' [ '?^' ]
		'dictionary parent' [ '.^' ]
		'matrix parent' [ '%^' ]
		'group parent' [ '+^' ]
	)
	'has tail' stategroup (
		'no'
		'yes'
			'tail' component 'view context parent path'
	)
```

### view context path

```js
'view context path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'parent'
					'path' component 'view context parent path'
				'matrix key' [ '>key' ]
				'linked key node' [ '.>' ]
				'linked text node' [ ':>' ]
				'reference' [ '>' ]
				'command reference' [ '/>' ]
				'command matrix' [ '/>key' ]
				'entity' [ '$' ]
			)
	)
	'widget context constraint'
```

### gui widget configuration node

```js
'gui widget configuration node' [ '{' , '}' ]
	'configuration' collection indent (
		'context switch' stategroup (
			'no switch'
			'switch' [ '$' ]
		)
		'type' stategroup (
			'widget'
				'context switch' stategroup (
					'no switch' [ '=' ]
					'switch' [ '==' ]
						'widget context constraint' component 'widget context constraint'
				)
				'widget' reference
				'configuration' component 'gui widget configuration node'
			'window'
				'window' [ 'window' ] reference
				'configuration' component 'gui widget configuration node'
			'view'
				'render' stategroup (
					'inline' [ 'inline' 'view' ]
					'in window'[ 'open' 'view' ]
						'window' [ '@' ] reference
				)
				'using views'  stategroup (
					'internal'
					'external' [ 'from' ]
						'views' reference
				)
				'view context' component 'view context path'
				'view' [ ':' ] reference
			'configuration' [ ':' ]
				'type' stategroup (
					'number'
						'source' stategroup (
							'now' [ 'now' ]
								'has offset' stategroup (
									'none'
									'yes'
										'offset' [ '+' ] number
								)
							'static'
								'number' number
						)
					'text'
						'type' stategroup (
							'static'
								'value' text
							'phrase'
								'value' reference
						)
					'list'
						'list' [ '[' ] component 'gui widget configuration list'
					'state group'
						'state' reference
						'configuration' component 'gui widget configuration node'
				)
			'model binding' [ '::' ]
				'type' stategroup (
					'window' [ 'window' ]
						'window' reference
						'configuration' component 'gui widget configuration node'
					'entity' [ 'entity' ]
						'configuration' component 'gui widget configuration node'
					'current node' [ 'node' ]
						'configuration' component 'gui widget configuration node'
					'collection' [ 'collection' ]
						'query context constraint' component 'node constraint'
						'property path' component 'model binding property path'
						'collection type' stategroup (
							'matrix'
								'matrix' [ '%' ] reference
							'dictionary'
								'dictionary' [ '.' ] reference
						)
						'request type' stategroup (
							'query' [ 'query' ]
							'subscription' [ 'subscribe' ]
						)
						'query' reference
						'configuration' component 'gui widget configuration node'
					'query' [ 'query' ]
						'query context' stategroup (
							'root' [ 'on' 'root' ]
								'query' reference
							'current node'
								'property path' component 'model binding property path'
								'query' reference
						)
						'has refresh interval' stategroup (
							'no'
							'yes' [ 'refresh:' ]
								'interval' number
						)
						'configuration' component 'gui widget configuration node'
					'group'
						'group' [ 'group' ] reference
						'configuration' component 'gui widget configuration node'
					'state group' [ 'stategroup' ]
						'property path' component 'model binding property path'
						'state group' reference
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' [ '(' , ')' ] collection order 'view order' indent (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'configuration' [ '->' ] component 'gui widget configuration node'
						)
					'command' [ 'command' ]
						'property path' component 'model binding property path'
						'command' reference
						'configuration' component 'gui widget configuration node'
					'number' [ 'number' ]
						'property path' component 'model binding property path'
						'property' reference
						'conversion' component 'number conversion'
						'configuration' component 'gui widget configuration node'
					'text'
						'type' stategroup (
							'key' [ 'key' ]
								'type' stategroup (
									'simple'
									'link' [ 'link' ]
										'has candidates query' stategroup (
											'yes' [ 'candidates:' ]
												'query' reference
											'no'
										)
								)
							'text property' [ 'text' ]
								'type' stategroup (
									'simple'
									'link' [ 'link' ]
										'has candidates query' stategroup (
											'yes' [ 'candidates:' ]
												'query' reference
											'no'
										)
								)
								'property path' component 'model binding property path'
								'property' reference
						)
						'configuration' component 'gui widget configuration node'
					'file' [ 'file' ]
						'property path' component 'model binding property path'
						'property' reference
						'configuration' component 'gui widget configuration node'
					'reference'
						'type' stategroup (
							'key' [ 'matrix' 'key' ]
								'navigable' stategroup (
									'yes'
									'no' [ 'text' ]
								)
							'reference property'
								'property path' component 'model binding property path'
								'navigable' stategroup (
									'yes'
										'property' [ 'reference' ] reference
									'no'
										'property' [ 'reference' 'text' ] reference
								)
						)
						'has candidates query' stategroup (
							'yes' [ 'candidates:' ]
								'query' reference
							'no'
						)
						'configuration' component 'gui widget configuration node'
					'command parameter text' [ '>>' 'text' ]
						'property' reference
						'configuration' component 'gui widget configuration node'
					'command parameter file' [ '>>' 'file' ]
						'property' reference
						'configuration' component 'gui widget configuration node'
					'command parameter reference' [ '>>' ]
						'property' [ 'reference' ] reference
						'has candidates query' stategroup (
							'yes' [ 'candidates:' ]
								'query' reference
							'no'
						)
						'configuration' component 'gui widget configuration node'
					'command parameter number' [ '>>' 'number' ]
						'property' reference
						'conversion' component 'number conversion'
						'configuration' component 'gui widget configuration node'
					'command parameter state group' [ '>>' 'stategroup' ]
						'property' reference
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' collection order 'view order' indent ( [ '|' ]
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'configuration' component 'gui widget configuration node'
						)
					'command parameter matrix' [ '>>' 'matrix' ]
						'property' reference
						'configuration' component 'gui widget configuration node'
					'query number'
						'number' [ 'query' 'number' ] reference
						'conversion' component 'number conversion'
						'configuration' component 'gui widget configuration node'
					'query text'
						'text' [ 'query' 'text' ] reference
						'configuration' component 'gui widget configuration node'
					'query file'
						'file' [ 'query' 'file' ] reference
						'configuration' component 'gui widget configuration node'
				)
		)
	)
```

### number conversion

```js
'number conversion'
	'has decimal point translation' stategroup (
		'yes'[ '<<' ]
			'translation' number
		'no'
	)
	'gui singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'dictionary parent' [ '.^' ]
				'matrix parent' [ '%^' ]
				'group parent' [ '+^' ]
				'state parent' [ '?^' ]
				'matrix key' [ '>key' ]
				'group'
					'group' [ '+' ] reference
				'reference'
					'reference' [ '>' ] reference
			)
			'tail' component 'gui singular path'
	)
```

### gui conditional path

```js
'gui conditional path'
	'has steps' stategroup (
		'no'
			'tail' component 'gui singular path'
		'yes'
			'head' component 'gui singular path'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
			)
			'tail' component 'gui conditional path'
	)
```

### model binding property path

```js
'model binding property path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
			)
			'tail' component 'model binding property path'
	)
```

### query path step

```js
'query path step'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group'
					'group' [ '+' ] reference
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
			)
			'tail' component 'query path step'
	)
```

### query path

```js
'query path'
	'has steps' stategroup (
		'no'
		'yes'
			'head' component 'query path step'
			'collection type' stategroup (
				'matrix'
					'matrix' [ '%' ] reference
				'dictionary'
					'dictionary' [ '.' ] reference
			)
			'tail' component 'query path'
	)
```
