---
layout: doc
origin: relational-database-bridge
language: database
version: 77
type: grammar
---


```js
'tables' collection order 'dependency graph' (
	'dependencies' collection predecessors
	'source' stategroup (
		'query' [ ':' 'table' '=' ]
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
							'origin' component 'query origin type'
						)
						'join key' [ 'join' ] collection (
							'contra field' [ '==' ] reference
							'filter' stategroup ( 'constrain' )
						)
					)
			)
		'derived' [ ':=' 'table' '=' ]
			'type' stategroup (
				'aggregate'
					'source' reference
					'field mapping' ['fields'] collection (
						'source field' ['='] reference
						'data type' ['as'] stategroup ( //drop this stategroup
							'text' ['text']
							'integer' ['integer']
							'boolean' ['bool']
							'enum' ['enum']
						)
					)
			)
	)
	'fields' [ 'fields' ] collection (
		'source' [ '=' ] stategroup (
			'reference'
				'field' text
				'definition' component 'field'
				'origin' component 'query origin type'
			'inline reference' [ 'inline' ]
				'inline table' reference
				'inline field' [ '.' ] reference
				'origin' component 'query origin type'
			'derived'
				'type' stategroup (
					'query'
						'derivation' stategroup (
							'text'
								'expression' component 'text expression'
							'integer'
								'expression' component 'integer expression'
						)
					'derived'
						'derivation' stategroup (
							'aggregate'
								'type' stategroup (
									'key' ['key'] //TODO: should we constrain primary key is dense on this for aggregates?
									'join' ['join']
										'separator' text
									'integer sum' ['sum']
								)
						)
				)
				'definition' component 'field'
				'origin' component 'derived origin type'
		)
	)
	'has primary key' stategroup (
		'no'
		'yes' [ 'primary-key' ]
			'source type' stategroup (
				'reference'
				'derived' [ '(derived)' ]
			)
			'primary key' collection (
				'filter' stategroup ( 'constrain' )
				'source' stategroup ( // drop this stategroup
					'reference' [ ]
					'derivation' [ '(derived)' ]
				)
				'data type' stategroup ( // drop this stategroup
					'text' [ '(text)' ]
					'integer' [ '(integer)' ]
					'boolean' [ '(bool)' ]
					'enum' [ '(enum)' ]
				)
			)
	)
	'unique indices' collection ( ['unique-index']
		'fields' ['(',')'] collection (
			'data type' stategroup ( // drop this stategroup
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
				'source' stategroup ( // drop this stategroup; use equality constraint
					'reference'
					'derived' [ '(derived)' ]
				)
				'key fields' [ '(' , ')' ] collection (
					'filter' stategroup ( 'constrain' )
					'contra field' [ '==' ] reference
					'source' stategroup ( // drop this stategroup; use equality constraint
						'reference'
						'derived' [ '(derived)' ]
					)
					'data type' stategroup ( // drop this stategroup; use equality constraint
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
					'data type' stategroup ( // drop this stategroup
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
	'prefilters' [ 'where' ] collection (
		'type' [ '=' ] stategroup (
			'field'
				'field' ['.'] reference
				'operation' stategroup (
					'contains'
						'filter' stategroup ( 'constrain' )
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
'origin type'
```

```js
'query origin type'
	'type' component 'origin type'
```

```js
'derived origin type'
	'type' component 'origin type'
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
'base type'
```

```js
'number base type'
	'type' component 'base type'
```

```js
'field'
	'data type' [ 'as' ] stategroup (
		'text' [ 'text' ]
			'type' component 'base type'
			'has import rules' stategroup (
				'yes' ['(', ')']
					'rule: left trim' stategroup (
						'yes' ['trim-left']
						'no'
					)
					'rule: right trim' stategroup (
						'yes' ['trim-right']
						'no'
					)
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
			'type' component 'base type'
		'enum' [ 'enum' ]
			'type' component 'base type'
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
'null guard'
	'nullable' stategroup (
		'no'
		'yes' ['(nullable)']
	)
```

```js
'string concat'
```

```js
'expression' component 'text expression'
	'has field' stategroup (
		'no'
		'yes'
			'next field' component 'string concat'
	)
```

```js
'text expression'
	'type' stategroup (
		'field'
			'field' [ '.' ] reference
			'source' stategroup ( // drop this stategroup
				'reference'
				'inline reference' ['(inline)']
			)
			'data type' stategroup ( // drop this stategroup
				'text'
				'floating point' [ '(float)' ]
				'integer' [ '(integer)' ]
			)
			'null guard' component 'null guard'
		'concat' [ 'concat' ]
			'separator' text
			'string concat' [ '(' , ')' ] component 'string concat'
		'trim' [ 'trim' ]
			'trim character' text
			'expression' [ '(',')' ] component 'text expression'
		'substring' [ 'substring' ]
			'from position' number
			'to position' ['..'] number
			'expression' ['(',')'] component 'text expression'
		'null switch'
			'expression' ['?'] component 'text expression'
			'on null' [':'] stategroup (
				'panic' ['panic']
				'default' ['static']
					'value' text
				'rescue'
					'expression' component 'text expression'
			)
		'split' ['hack' 'str']
			'expression' component 'text expression'
			//* these are the delimiters (only ASCII support) */
			//* it splits on every character match, not on pattern match! */
			'delimiters' ['/'] text
			'position' ['/'] number
	)
```

```js
'integer expression'
	'type' stategroup (
		'string length' [ 'length' ]
			'string' component 'text expression'
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
