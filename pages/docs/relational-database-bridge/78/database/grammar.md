---
layout: doc
origin: relational-database-bridge
language: database
version: 78
type: grammar
---


```js
'numerical sets' group
(
	'natural' component 'set type'
	'integer' component 'set type'
	'real'    component 'set type'
)
```

```js
'tables' collection order 'dependency graph' (
	'dependencies' collection predecessors
	'source' [ ':' 'table' '=' ] group (
		'scoped' stategroup (
			'no'
			'yes'
				'namespace' text
				'selection' component 'table selector'
		)
		'source' text
		'inline tables' stategroup (
			'no'
			'yes'[ 'inline-tables' '(experimental)']
				'sub tables' collection (
					'fields' [ 'fields' ] collection (
						'definition' component 'field'
					)
					'join key' [ 'join' ] collection (
						'contra field' [ '==' ] reference
						'filter' stategroup ( 'constrain' )
					)
				)
		)
	)
	'fields' [ 'fields' ] collection (
		'source' [ '=' ] stategroup (
			'reference'
				'field' text
				'definition' component 'field'
			'inline reference' [ 'inline' ]
				'inline table' reference
				'inline field' [ '.' ] reference
		)
	)
	'has primary key' stategroup (
		'no'
		'yes' [ 'primary-key' ]
			'primary key' collection (
				'filter' stategroup ( 'constrain' )
				'data type' stategroup (
					'text' [ '(text)' ]
					'integer' [ '(integer)' ]
					'boolean' [ '(bool)' ]
					'enum' [ '(enum)' ]
				)
			)
	)
	'unique indices' collection ( ['unique-index']
		'fields' ['(',')'] collection (
			'data type' stategroup (
				'text' [ '(text)' ]
				'integer' [ '(integer)' ]
				'boolean' [ '(bool)' ]
				'enum' [ '(enum)' ]
			)
			'constrain' stategroup ( 'non null' )
		)
	)
	'foreign keys' [ 'foreign-keys' ] collection (
		'table' [ '=>' 'table' ] reference
		'on' ['where'] stategroup (
			'primary key' [ 'primary-key' ]
				'key fields' [ '(' , ')' ] collection (
					'filter' stategroup ( 'constrain' )
					'contra field' [ '==' ] reference
					'data type' stategroup (
						'text' [ '(text)' ]
						'integer' [ '(integer)' ]
						'boolean' [ '(bool)' ]
						'enum' [ '(enum)' ]
					)
				)
			'unique index' [ 'unique-index' ]
				'index' reference
				'key fields' [ '(' , ')' ] collection (
					'contra field' [ '==' ] reference
					'data type' stategroup (
						'text' [ '(text)' ]
						'integer' [ '(integer)' ]
						'boolean' [ '(bool)' ]
						'enum' [ '(enum)' ]
					)
				)
		)
	)
	'sql strategy' ['filter-strategy' ':'] stategroup (
		'exists' ['EXISTS']
		'join' ['JOIN']
	)
	'text encoding' stategroup (
		'ascii'
		'utf8' ['text-encoding' ':' 'utf8']
	)
	'prefilters' collection ( [ 'where' ]
		'type' [ '=' ] stategroup (
			'field'
				'field' ['.'] reference
				'operation' stategroup (
					'contains'
						'comparison' stategroup (
							'in' ['in']
								'arguments' ['(', ')'] collection ( )
							'not in' ['not' 'in']
								'arguments' ['(', ')'] collection ( )
						)
					'search'
						'filter' stategroup ( 'constrain' )
						'type' stategroup (
							'starts with' [ 'starts-with' ]
							'contains' [ 'contains' ]
							'equals' [ '==' ]
						)
						'substring' text
					'compare'
						'left filter' stategroup ( 'constrain' )
						'operator' stategroup (
							'smaller' ['<']
							'greater' ['>']
							'equal' ['==']
						)
						'right' stategroup (
							'property'
								'right' ['.'] reference
								'right filter' stategroup ( 'constrain' )
							'static'
								'value' number
						)
					'in list' ['in']
						'filter' stategroup ( 'constrain' )
						'number list' [ '(',')' ] component 'number list'
				)
			'foreign key' ['foreign-key']
				'foreign key' reference
			'incoming foreign key' [ 'this' ]
				'source table' [ 'in' 'table' ] reference
				'incoming link' ['>'] reference
		)
	)
)
```

```js
'number list'
	'step type' stategroup (
		'single value'
			'value' number
		'range'
			'begin value' number
			'end value' [ '...' ] number
	)
	'has more steps' stategroup (
		'no'
		'yes'
			'tail' component 'number list'
	)
```

```js
'set type'
```

```js
'base type'
```

```js
'number base type'
	'type' component 'base type'
```

```js
'text base type'
	'type' component 'base type'
```

```js
'boolean base type'
	'type' component 'base type'
```

```js
'enum base type'
	'type' component 'base type'
```

```js
'field'
	'data type' [ 'as' ] stategroup (
		'text' [ 'text' ]
			'type' component 'text base type'
			'import rule' stategroup (
				'fixed length' ['(', ')']
					'rule: trim' stategroup (
						'left'  ['trim-left']
						'right' ['trim-right']
						'none'
					)
					'length' number
				'no'
			)
		'floating point' [ 'float' ]
			'type' component 'number base type'
		'decimal' ['decimal']
			'type' component 'number base type'
			'rounding' stategroup (
				'ordinary' //['half-up']
				'ceil'     ['ceil']
				'floor'    ['floor']
			)
			'scale' ['(', ')'] number
		'integer' [ 'integer' ]
			'type' component 'number base type'
		'boolean' [ 'bool' ]
			'type' component 'boolean base type'
		'enum' [ 'enum' ]
			'type' component 'enum base type'
			'values' [ '(' , ')' ] collection ( )
	)
	'nullable' stategroup (
		'yes' [ '(nullable)' ]
		'no'
	)
	'has description' stategroup (
		'no'
		'yes'
			'description' ['</' , '/>'] text
	)
```

```js
'table selector'
	'has step' stategroup (
		'yes'
			'name' ['.'] text
			'tail' component 'table selector'
		'no'
	)
```
