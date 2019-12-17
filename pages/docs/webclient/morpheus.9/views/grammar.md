---
layout: doc
origin: webclient
language: views
version: morpheus.9
type: grammar
---


```js
'dependencies' collection ( [ 'using' ] )
```

```js
'views' collection indent (
	'translate title' stategroup (
		'no'
		'yes'
			'title' [ 'as' ] reference
	)
	'start context' component 'model context'
	'node type' ['(', ')'] component 'gui node type path'
	'queries' collection ( [ 'query' ]
		'tag' component 'context'
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
							'text property'
								'property context' component 'query property context path'
								'property' [ 'reference:' ] reference
							'text link property'
								'property context' component 'query property context path'
								'property' [ 'text' 'link:' ] reference
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
				'path' ['(',')'] component 'conditional path'
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
			'path' [ '->' ] component 'conditional path'
			'type' [ ':' ] stategroup (
				'text'
					'text' [ 'text' ] reference
					'filter' stategroup (
						'none'
						'simple' [ 'filter' ]
							'criteria' text
						'current id path' [ 'filter' ]
							'constraint' component 'node constraint'
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
	'context switch' stategroup (
		'no switch' [ '=' ]
		'switch' [ '==' ]
			'widget context constraint' component 'widget context constraint'
	)
	'widget' reference
	'configuration node' component 'gui widget configuration node'
)
```

```js
'node constraint'
```

```js
'model context'
	'context' component 'context'
```

```js
'context'
```

```js
'command parameters type path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state group'
					'property' [ '?' ] reference
					'state' [ '|' ] reference
				'collection'
					'property' [ '.' ] reference
			)
			'tail' component 'command parameters type path'
	)
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

```js
'gui node type path'
	'steps' component 'gui node type path step'
```

```js
'gui widget configuration list'
	'has steps' stategroup (
		'no' [ ']' ]
		'yes'
			'configuration' component 'gui widget configuration node'
			'tail' component 'gui widget configuration list'
	)
```

```js
'view context parent path'
	'type' stategroup (
		'state parent' [ '?^' ]
		'collection parent' [ '.^' ]
		'group parent' [ '+^' ]
	)
	'has tail' stategroup (
		'no'
		'yes'
			'tail' component 'view context parent path'
	)
```

```js
'view context path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'query entry' [ 'entry' ]
				'parent'
					'path' component 'view context parent path'
				'linked text node' [ ':>' ]
				'reference' [ '>' ]
				'command reference' [ '/>' ]
				'entity' [ '$' ]
			)
	)
	'widget context constraint'
```

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
					'inline' [ ':' 'inline' 'view' ]
					'in window'[ ':' 'open' 'view' ]
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
						'context' component 'model context'
						'configuration' component 'gui widget configuration node'
					'current node' [ 'node' ]
						'configuration' component 'gui widget configuration node'
					'collection' [ 'collection' ]
						'query context constraint' component 'node constraint'
						'property path' component 'model binding property path'
						'collection' [ '.' ] reference
						'request type' stategroup (
							'query' [ 'query' ]
							'subscription' [ 'subscribe' ]
						)
						'query' reference
						'configuration' component 'gui widget configuration node'
					'query' [ 'query' ]
						'query context' stategroup (
							'node'
								'switch' stategroup (
									'root' [ 'on' 'root' ]
										'query' reference
									'current node'
										'property path' component 'model binding property path'
										'query' reference
								)
							'candidates' [ 'candidates' ]
								'query' reference
						)
						'has refresh interval' stategroup (
							'no'
							'yes' [ 'refresh:' ]
								'interval' number
						)
						'configuration' component 'gui widget configuration node'
					'group'
						'group context' component 'model context'
						'group' [ 'group' ] reference
						'configuration' component 'gui widget configuration node'
					'state group' [ 'stategroup' ]
						'property path' component 'model binding property path'
						'state group' reference
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' [ '(' , ')' ] collection order 'view order' indent (
							'state context' component 'model context'
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'configuration' [ '->' ] component 'gui widget configuration node'
						)
					'command' [ 'command' ]
						'command context' component 'model context'
						'property path' component 'model binding property path'
						'command' reference
						'configuration' component 'gui widget configuration node'
					'number' [ 'number' ]
						'number context' component 'model context'
						'property path' component 'model binding property path'
						'property' reference
						'conversion' component 'number conversion'
						'configuration' component 'gui widget configuration node'
					'text' [ 'text' ]
						'text context' component 'model context'
						'navigable' stategroup (
							'reference'[ 'reference' ]
							'link' [ 'link' ]
							'no'
						)
						'property path' component 'model binding property path'
						'property' reference
						'configuration' component 'gui widget configuration node'
					'file' [ 'file' ]
						'file context' component 'model context'
						'property path' component 'model binding property path'
						'property' reference
						'configuration' component 'gui widget configuration node'
					'command parameter text' [ '>>' 'text' ]
						'has constraint' stategroup (
							'yes' [ 'reference' ]
								'reference context' component 'model context'
							'no'
						)
						'property' reference
						'configuration' component 'gui widget configuration node'
					'command parameter file' [ '>>' 'file' ]
						'property' reference
						'configuration' component 'gui widget configuration node'
					'command parameter number' [ '>>' 'number' ]
						'property' reference
						'conversion' component 'number conversion'
						'configuration' component 'gui widget configuration node'
					'command parameter state group' [ '>>' 'stategroup' ]
						'property' reference
						'has states' stategroup has 'states' first 'first' 'yes' 'no'
						'states' collection order 'view order' indent ( [ '|' ]
							'state context' component 'model context'
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'configuration' component 'gui widget configuration node'
						)
					'command parameter collection' [ '>>' 'collection' ]
						'collection context' component 'model context'
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

```js
'number conversion'
	'has decimal point translation' stategroup (
		'yes'[ '<<' ]
			'translation' number
		'no'
	)
```

```js
'singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'collection parent' [ '.^' ]
				'group parent' [ '+^' ]
				'state parent' [ '?^' ]
				'group'
					'group' [ '+' ] reference
				'reference'
					'reference' [ '>' ] reference
				'reference output'
					'reference' ['>'] reference
					'output parameter' ['$'] reference
				'state constraint'
					'input parameter' [ '&' ] reference
				'state group output parameter'
					'state group' ['?'] reference
					'output parameter' ['$'] reference
			)
			'tail' component 'singular path'
	)
```

```js
'conditional path'
	'head' component 'singular path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'state'
					'state group' [ '?' ] reference
					'state' [ '|' ] reference
			)
			'tail' component 'conditional path'
	)
```

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

```js
'query path'
	'has steps' stategroup (
		'no'
		'yes'
			'head' component 'query path step'
			'collection' [ '.' ] reference
			'tail' component 'query path'
	)
```
