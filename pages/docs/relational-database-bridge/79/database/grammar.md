---
layout: doc
origin: relational-database-bridge
language: database
version: 79
type: grammar
---


```js
'base types' group (
	'bool'   component 'base type'
	'number' component 'base type'
	'text'   component 'base type'
)
```

```js
'numerical sets' group
(
	'invalid' component 'set type'
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
	'text encoding' stategroup (
		'ascii'
		'utf8' ['text-encoding' ':' 'utf8']
	)
	'prefilters' group (
		'join statements' collection ( ['join'] )
		'has where clause' stategroup (
			'yes' ['where']
				'where statement' component 'filter statement list'
			'no'
		)
	)
)
```

```js
'base type'
```

```js
'base type constraint'
```

```js
'set type'
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
'field'
	'data type' [ 'as' ] stategroup (
		'text' [ 'text' ]
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
		'decimal' ['decimal']
			'rounding' stategroup (
				'ordinary' //['half-up']
				'ceil'     ['ceil']
				'floor'    ['floor']
			)
			'scale' ['(', ')'] number
		'integer' [ 'integer' ]
		'boolean' [ 'bool' ]
		'enum' [ 'enum' ]
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

```js
'filter statement'
	'type' stategroup (
		'contains'
			'field' ['.'] reference
			'require text' component 'base type constraint'
			'comparison' stategroup (
				'in' ['in']
					'arguments' ['(',')'] collection ( )
				'not in' ['not' 'in']
					'arguments' ['(',')'] collection ( )
			)
		'search'
			'field' ['.'] reference
			'require text' component 'base type constraint'
			'type' stategroup (
				'starts with' ['starts-with']
				'contains' ['contains']
				'equals' ['equals']
			)
			'substring' text
		'compare'
			'field' ['.'] reference
			'operator' stategroup (
				'smaller' ['<']
				'greater' ['>']
				'equal' ['==']
				'not equal' ['!=']
			)
			'right' stategroup (
				'property'
					'right' ['.'] reference
				'static number'
					'require number' component 'base type constraint'
					'value' number
				'static text'
					'require text' component 'base type constraint'
					'value' text
				'time span'
					'require text' component 'base type constraint'
					'days' ['current-date' '-'] number
			)
		'in list'
			'field' ['.'] reference
			'require number' component 'base type constraint'
			'number list' ['(',')'] component 'number list'
		'foreign key' ['foreign-key']
			'foreign key' reference
		'incoming foreign key' ['this']
			'source table' ['in' 'table'] reference
			'incoming link' ['>'] reference
		'invert' ['not']
			'statement' component 'filter statement'
		'list'
			'statements' ['(',')'] component 'filter statement list'
	)
```

```js
'filter statement list'
	'statement' component 'filter statement'
	'has more statements' stategroup (
		'yes'
			'operator' stategroup (
				'and' ['and']
				'or'  ['or']
			)
			'tail' component 'filter statement list'
		'no'
	)
```
