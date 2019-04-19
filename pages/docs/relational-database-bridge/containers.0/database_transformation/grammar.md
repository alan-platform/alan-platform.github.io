---
layout: doc
origin: relational-database-bridge
language: database_transformation
version: containers.0
type: grammar
---


```js
'root context' component 'location context'
```

```js
'root enrichments' component 'enrichments'
```

```js
'root expressions' component 'expression stack'
```

```js
'root' [ 'root' ] component 'database 2 node mapping'
```

```js
'location context'
```

```js
'record context'
	'location context' component 'location context'
```

```js
'record set context'
	'location context' component 'location context'
```

```js
'enrichments'
```

```js
'expression stack'
```

```js
'dangerous context'
```

```js
'unsafe context'
	'danger' component 'dangerous context'
```

```js
'safe context'
	'danger' component 'dangerous context'
```

```js
'unguaranteed operation'
	'context' stategroup (
		'unsafe' [ '<!' , '>' ]
			'comment' text
		'safe'
	)
```

```js
'null guard'
	'has guard' stategroup (
		'no'
		'yes' [ 'nullable' ]
			'unguaranteed operation' component 'unguaranteed operation'
	)
```

```js
'data type'
```

```js
'numerical type'
	'data type' component 'data type'
```

```js
'integer type'
	'numerical type' component 'numerical type'
```

```js
'natural type'
	'numerical type' component 'numerical type'
```

```js
'text type'
	'data type' component 'data type'
```

```js
'integer list'
	'type' stategroup (
		'single value'
			'value' number
		'range'
			'begin value' number
			'end value' [ '...' ] number
	)
	'has more' stategroup (
		'no'
		'yes'
			'tail' component 'integer list'
	)
```

```js
'text list'
	'value' text
	'has more' stategroup (
		'no'
		'yes'
			'tail' component 'text list'
	)
```

```js
'link path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'explicit foreign key'
					'link' ['>>'] reference
					'context type' stategroup (
						'record'
							'context record' component 'record context'
						'record set' ['(set)']
							'context record set' component 'record set context'
					)
				'implicit foreign key' ['implicit-key']
					'target table' [ 'table' ] reference
					'key type' stategroup (
						'primary key'
							'foreign key' ['(', ')'] collection (
								'data type' stategroup (
									'text' ['text']
										'contra value' ['=='] component 'text expression'
									'enum' ['enum']
										'contra value' ['=='] component 'enum expression'
									'integer' ['integer']
										'contra value' ['=='] component 'number expression'
								)
							)
						'unique index'
							'index' ['index'] reference
							'foreign key' ['(', ')'] collection (
								'data type' stategroup (
									'enum' ['enum']
										'contra value' ['=='] component 'enum expression'
									'text' ['text']
										'contra value' ['=='] component 'text expression'
									'integer' ['integer']
										'contra value' ['=='] component 'number expression'
								)
							)
					)
					'context type' stategroup (
						'record'
							'context record key' component 'record context'
							'context record out' component 'record context'
						'record set' ['(set)']
							'context record key' component 'record context'
							'context record set out' component 'record set context'
					)
					'unguaranteed operation' component 'unguaranteed operation'
				'child collection' ['inverse']
					'source' [ 'table' ] reference
					'context type' stategroup (
						'record'
						'record set' ['(set)']
					)
					'links to me' ['>'] reference
					'context record set' component 'record set context'
				'enriched context' ['enriched']
					'enrichment' ['>>'] reference
				'expressed context' ['exp']
					'selection' component 'expression selector'
					'expression' ['>>'] reference
			)
			'tail' component 'link path'
	)
```

```js
'link dereference'
	'context type' stategroup (
		'record'
		'record set' ['*' '(set)']
	)
```

```js
'record dereference'
	'record constraint' stategroup ( 'record' )
```

```js
'record set dereference'
	'record set constraint' stategroup ( 'record set' )
```

```js
'floating point transformation'
	'transformation' stategroup (
		'divide' [ '/' ]
		'multiply' [ '*' ]
	)
	'factor' number
	'rounding' stategroup (
		'ordinary' ['round']
		'ceil'     ['ceil']
		'floor'    ['floor']
	)
```

```js
'expressions'
	'stack frame' component 'expression stack'
	'expressions' collection ( ['exp']
		'data type' stategroup (
			'number'
				'numerical type' stategroup (
					'integer' [ 'integer' ]
						'expression' component 'number expression'
						'integer' component 'integer type'
					'natural' [ 'natural' ]
						'expression' component 'natural expression'
						'natural' component 'natural type'
				)
			'text' [ 'text' ]
				'expression' component 'text expression'
			'context'
				'link' component 'link path'
				'dereference' component 'link dereference'
			'array' ['array']
				'expression' component 'array expression'
		)
	)
```

```js
'expression selector'
	'type' stategroup (
		'this'
		'parent' ['^']
			'tail' component 'expression selector'
	)
```

```js
'database 2 node mapping' [ '(' , ')' ]
	'unsafe context'  component 'unsafe context'
	'expressions' component 'expressions'
	'properties' collection (
		'type' [ ':' ] stategroup (
			'collection' [ 'collection' ]
				'key type' stategroup (
					'dictionary' [ '=' ]
					'matrix' [ '=>' ]
				)
				'type' stategroup (
					'root collection' [ 'table' ]
						'source' reference
					'child collection' ['inverse']
						'link' component 'link path'
						'source' [ 'table' ] reference
						'dereference' component 'link dereference'
						'links to me' [ '>' ] reference
					'record set' [ '(set)' ]
						'link' component 'link path'
						'dereference' component 'record set dereference'
					'expression' [ '(' , ')' ]
						'definition' [ '{{' , '}}' ] reference
						'tree' component 'collection expression tree'
				)
				'transformation' stategroup (
					'none'
						'context record' component 'record context'
						'key expression' [ '[' , ']' ] component 'text expression'
						'unguaranteed operation' component 'unguaranteed operation'
					'aggregate' [ 'aggregate' ]
						'context record' component 'record context'
						'key expression' [ '[' , ']' ] component 'text expression'
						'context record set' component 'record set context'
				)
				'mapping' component 'database 2 node mapping'
			'group' [ 'group' ]
				'mapping' component 'database 2 node mapping'
			'number'
				'type' stategroup (
					'expression'
						'numerical type' stategroup (
							'integer' [ 'integer' '=' ]
								'expression' component 'number expression'
							'natural' [ 'natural' '=' ]
								'expression' component 'natural expression'
						)
					'current time'
						'numerical type' stategroup (
							'integer' ['integer' '=' 'now']
							'natural' ['natural' '=' 'now']
								'unguaranteed operation' component 'unguaranteed operation'
						)
				)
			'reference' [ 'text' '=>' ]
				'expression' component 'text expression'
			'state group' [ 'stategroup' '=' ]
				'expression' component 'state group expression'
			'text' [ 'text' '=' ]
				'expression' component 'text expression'
		)
	)
```

```js
'regular expression part'
	'has part' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'static'
					'text' text
				'pattern' [ '[' , ']' ]
					'type' stategroup (
						'decimal' [ '%d' ]
					)
			)
			'repeat' stategroup (
				'none'
				'exact' [ '{' , '}' ]
					'occurrences' number
			)
	)
```

```js
'regular expression'
	'first class' stategroup has 'classes' first 'first' 'set' 'empty'
	'classes' collection ( [ '$' ]
		'next class' stategroup has successor 'next' 'set' 'last'
		'capture' [ '(' , ')' ] component 'regular expression part'
		'tail' component 'regular expression part'
	)
```

```js
'string concat'
	'expression' component 'text expression'
	'has field' stategroup (
		'no'
		'yes' [ ',' ]
			'next field' component 'string concat'
	)
```

```js
'text expression'
	'type' stategroup (
		'concat' [ 'concat' ]
			'separator' text
			'string concat' [ '(' , ')' ] component 'string concat'
		'join' [ 'join' ]
			'separator' text
			'context record' component 'record context'
			'values' [ '(' , ')' ] component 'text expression'
		'field'
			'link' component 'link path'
			'context type' stategroup (
				'record'
					'field' [ '.' ] reference
					'null guard' component 'null guard'
					'data type constraint' stategroup ( 'text' )
				'record set'
					'field' [ '.' ] reference
					'null guard' component 'null guard'
					'data type constraint' stategroup ( 'text' )
					'merge' stategroup (
						'shared value' [ 'shared' ]
							'unguaranteed operation' component 'unguaranteed operation'
					)
			)
		'enrichment' [ 'enriched' ]
			'enrichment' reference
		'expression' ['exp']
			'selection' component 'expression selector'
			'expression' reference
		'trim' [ 'trim' ]
			'trim character' text
			'expression' [ '(' , ')' ] component 'text expression'
		'static'
			'value' text
		'stringify number' [ 'to-text' ]
			'expression' component 'number expression'
	)
```

```js
'array expression'
	'set type' stategroup (
		'root collection' ['table']
			'source' reference
		'record set' ['(set)']
			'link' component 'link path'
			'dereference' component 'record set dereference'
	)
	'transformation' stategroup (
		'none'
			'context record' ['on'] component 'record context'
			'key expression' ['[', ']'] component 'number expression'
			'unguaranteed operation' component 'unguaranteed operation'
		'aggregate'
			'context record' ['aggregate'] component 'record context'
			'key expression' ['[', ']'] component 'number expression'
			'context record set' component 'record set context'
	)
```

```js
'enum expression'
	'type' stategroup (
		'field'
			'link' component 'link path'
			'context type' stategroup (
				'record'
					'field' [ '.' ] reference
					'null guard' component 'null guard'
					'data type constraint' stategroup ( 'enum' )
				'record set'
					'field' [ '.' ] reference
					'null guard' component 'null guard'
					'data type constraint' stategroup ( 'enum' )
					'merge' stategroup (
						'shared value' [ 'shared' ]
							'unguaranteed operation' component 'unguaranteed operation'
					)
			)
	)
```

```js
'number expression'
	'type' stategroup (
		'convert text' [ 'to-number' ]
			'expression' component 'text expression'
			'to' [ 'as' ] stategroup (
				'number'
					'numerical type' stategroup (
						'integer' [ 'integer' ]
							'integer' component 'integer type'
						'natural' [ 'natural' ]
							'natural' component 'natural type'
					)
				'date and time' [ 'datetime'  ]
					'integer' [ 'regexp' ] component 'integer type'
					'regexp' [ '(' , ')' ] component 'regular expression'
					'year' [ 'where' 'year' '=' ] reference
					'month' [ 'month' '=' ] reference
					'day of month' [ 'day' '=' ] reference
					'hour' [ 'hour' '=' ] reference
					'minute' [ 'minute' '=' ] reference
					'second' [ 'second' '=' ] reference
				'date' [ 'date' ]
					'integer' [ 'regexp' ] component 'integer type'
					'regexp' [ '(' , ')' ] component 'regular expression'
					'year' [ 'where' 'year' '=' ] reference
					'offset' stategroup (
						'month'
							'month' [ 'month' '=' ] reference
							'day of month' [ 'day' '=' ] reference
						'week'
							'week' [ 'week' '=' ] reference
							'day of week' [ 'day' '=' ] stategroup (
								'monday' ['Monday']
								'tuesday' ['Tuesday']
								'wednesday' ['Wednesday']
								'thursday' ['Thursday']
								'friday' ['Friday']
								'saturday' ['Saturday']
								'sunday' ['Sunday']
							)
					)
			)
			'unguaranteed operation' component 'unguaranteed operation'
		'field'
			'link' component 'link path'
			'context type' stategroup (
				'record'
					'field' ['.'] reference
					'data type' stategroup (
						'floating point'
							'transformer' component 'floating point transformation'
						'decimal' ['(decimal)']
						'integer'
					)
					'null guard' component 'null guard'
				'record set'
					'merge' stategroup (
						'shared value' ['shared']
							'unguaranteed operation' component 'unguaranteed operation'
						'sum' [ 'sum' ]
						'select'
							'selector' stategroup (
								'min' [ 'min' ]
								'max' [ 'max' ]
							)
							'unguaranteed operation' component 'unguaranteed operation'
					)
					'field' [ '.' ] reference
					'data type' stategroup (
						'floating point'
							'transformer' component 'floating point transformation'
						'decimal' ['(decimal)']
						'integer'
					)
					'null guard' component 'null guard'
			)
			'integer' component 'integer type'
		'enrichment' [ 'enriched' ]
			'enrichment' reference
		'expression' ['exp']
			'selection' component 'expression selector'
			'expression' reference
		'operator'
			'type' stategroup (
				'add' [ 'sum' ]
				'subtract' [ 'subtract' ]
				'multiply' [ 'product' ]
				'divide' [ 'division' ]
			)
			'left' [ '(' , ',' ] component 'number expression'
			'right' component 'number expression'
			'integer' [ ')' ] component 'integer type'
		'static integer'
			'type' stategroup (
				'integer'
					'value' number
					'integer' component 'integer type'
				'natural'
					'value' number
					'natural' [ '(natural)' ] component 'natural type'
			)
		)
```

```js
'natural expression'
	'expression' component 'number expression'
	'natural' component 'natural type'
	'constrain' stategroup (
		'no'
		'yes' [ 'constrain' ]
			'unguaranteed operation' component 'unguaranteed operation'
	)
```

```js
'collection expression tree'
	'type' stategroup (
		'empty' [ 'empty' ]
		'link'
			'link' component 'link path'
			'dereference' component 'link dereference'
		'branch'
			'type' stategroup (
				'condition list' [ 'match' ]
					'conditions'  [ '(' , ')' ] component 'condition list'
					'on success' [ '|' 'true' ] component 'collection expression tree'
					'on failure' [ '|' 'false' ] component 'collection expression tree'
				'panic' [ 'panic' ]
					'comment' ['<!', '>'] text
			)
	)
```

```js
'condition list'
	'source type' stategroup (
		'field'
			'link' component 'link path'
			'dereference' component 'record dereference'
			'null guard' component 'null guard'
			'data type' stategroup (
				'integer' ['integer']
					'numerical type' component 'numerical type'
				'text' ['text']
					'text type' component 'text type'
			)
			'field' [ '.' ] reference
		'enrichment' [ 'enriched' ]
			'data type' stategroup (
				'integer' ['integer']
					'numerical type' component 'numerical type'
				'text' ['text']
					'text type' component 'text type'
			)
			'enriched field' reference
		'expression' ['exp']
			'selection' component 'expression selector'
			'data type' stategroup (
				'integer' ['integer']
					'numerical type' component 'numerical type'
				'text' ['text']
					'text type' component 'text type'
			)
			'expression' reference
	)
	'condition type' stategroup (
		'equals' ['==']
			'data type' stategroup (
				'integer'
					'value' number
				'text'
					'value' text
			)
		'in' ['in']
			'data type' stategroup (
				'integer'
					'values' ['(', ')'] component 'integer list'
				'text'
					'values' ['(', ')'] component 'text list'
			)
	)
	'has more conditions' stategroup (
		'no'
		'yes' [ '&&' ]
			'tail' component 'condition list'
	)
```

```js
'state group expression'
	'type' stategroup (
		'panic' ['panic']
			'comment' ['<!', '>'] text
		'switch' ['switch' '(']
			'link' component 'link path'
			'dereference' component 'record dereference'
			'field' ['.'] reference
			'null guard' [')'] component 'null guard'
			'data type' [ '(' , ')' ] stategroup (
				'boolean'
					'on true' [ '|' 'true' '=' ] component 'state group expression'
					'on false' [ '|' 'false' '=' ] component 'state group expression'
				'enum'
					'mapping' collection ( [ 'on' ]
						'expression' [ '=' ] component 'state group expression'
					)
			)
		'enrich' [ 'enrich' ]
			'safe context' component 'safe context'
			'enrichments context' component 'enrichments'
			'enrichments' [ '(' , ')' ] collection (
				'data type' stategroup (
					'number' [ ':' ]
						'numerical type' stategroup (
							'integer' [ 'integer' '=' ]
								'expression' component 'number expression'
								'integer' component 'integer type'
							'natural' [ 'natural' '=' ]
								'expression' component 'natural expression'
								'natural' component 'natural type'
						)
					'text' [ ':' 'text' '=' ]
						'expression' component 'text expression'
					'context' [ '=' ]
						'link' component 'link path'
						'dereference' component 'link dereference'
					'array' [ ':' 'array' '=' ]
						'expression' component 'array expression'
				)
			)
			'unsafe context' component 'unsafe context'
			'on success' [ '|' 'success' '=' ] component 'state group expression'
			'on failure' [ '|' 'failure' '=' ] component 'state group expression'
		'if' [ 'match' ]
			'condition list' [ '(' , ')' ] component 'condition list'
			'on success' [ '|' 'true' '=' ] component 'state group expression'
			'on failure' [ '|' 'false' '=' ] component 'state group expression'
		'context cast' [ 'single-record' ]
			'context record' component 'record context'
			'on record' [ '|' 'true' '=' ] component 'state group expression'
			'on record set' [ '|' 'false' '=' ] component 'state group expression'
		'array selector' ['select' '(']
			'selection' stategroup (
				'predecessor' ['predecessor']
					'key expression' ['with'] component 'number expression'
				'successor'   ['successor']
					'key expression' ['with'] component 'number expression'
				'first'       ['first']
				'last'        ['last']
			)
			'array source' ['in' , ')'] stategroup (
				'enrichment'
					'enrichment' ['enriched'] reference
				'expression'
					'selection' ['exp'] component 'expression selector'
					'expression' reference
			)
			'on success' [ '|' 'success' '=' ] component 'state group expression'
			'on failure' [ '|' 'failure' '=' ] component 'state group expression'
		'set state'
			'state' reference
			'mapping' component 'database 2 node mapping'
	)
```
