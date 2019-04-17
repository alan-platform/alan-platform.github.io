---
layout: doc
origin: sql-mirror
language: sql_mapping
version: containers.5
type: grammar
---


```js
'formatting' group (
	'identifier wrapping' ['identifier-delimiter:'] group (
		'open' text
		'close' text
	)
	'data type mapping' ['data-types'] group (
		'key' ['key:'] text
		'text' ['text:'] text
		'number' ['number:'] text
		'state' ['state:'] text
	)
)
```

```js
'tables' ['schema'] collection indent (
	'table' component 'table'
	'primary key' ['<--'] group (
		'root key field' stategroup (
			'no'
				'entity type path' component 'entity type path'
			'yes'
				'root key' ['(',')'] text
		)
		'key fields' collection ( ['[']
			'has predecessor' stategroup has predecessor 'predecessor' 'yes' 'no'
			'has successor' stategroup has successor 'successor' 'yes' 'no'
			'has tail' [']'] stategroup (
				'no'
				'yes'
					'entity type path' component 'entity type path'
			)
		)
		'has key fields' stategroup has 'key fields' first 'first' last 'last' 'yes' 'no'
	)
	'fields' ['{','}'] collection indent (
		'has successor' stategroup has successor 'successor' 'yes' 'no'
		'type' [':'] stategroup (
			'key'
				'type' stategroup (
					'primary key' ['primary-key']
					'foreign key' ['foreign-key']
				)
			'text' ['text']
			'number' ['number']
			'state' ['state']
				'values' ['(', ')'] collection ( )
		)
	)
	'has fields' stategroup has 'fields' first 'first' 'yes' 'no'
)
```

```js
'undefined table' component 'table'
```

```js
'root table' ['mapping' 'root'] component 'optional table selection'
```

```js
'mapping' component 'mapping definition'
```

```js
'entity scoped node type path'
	'has steps' stategroup (
		'no'
		'yes'
			'type' stategroup (
				'group'
					'group' ['+'] reference
				'state'
					'state group' ['?'] reference
					'state' ['|'] reference
			)
			'tail' component 'entity scoped node type path'
	)
```

```js
'entity type path'
	'head' component 'entity scoped node type path'
	'collection' ['.'] reference
```

```js
'table'
```

```js
'table selection'
	'table' ['-->' 'table'] reference
```

```js
'optional table selection'
	'select table' stategroup (
		'yes'
			'table' component 'table selection'
		'no'
	)
```

```js
'mapping definition' ['(',')']
	'properties' collection (
		'include' stategroup (
			'no' ['(ignore)']
			'yes'
				'type' [':'] stategroup (
					'text' ['text']
						'has constraint' stategroup (
							'no'
								'field' ['-->'] reference
							'yes' ['(->)']
								'field' ['-->'] reference
						)
					'number' ['number']
						'field' ['-->'] reference
					'file' ['file']
						'token field' ['-->'] reference
						'extension field' ['.'] reference
					'group' ['group']
						// 'optional table' component 'optional table selection'
						'mapping' component 'mapping definition'
					'state group' ['stategroup']
						'state group to field mapping' stategroup (
							'no'
							'yes' ['-->']
								'field' reference // reference !&'table'.'fields'
						)
						'states' ['(',')'] collection ( ['|']
							'state to state value mapping' stategroup (
								'no'
								'yes' ['-->']
									'value' reference
							)
							// 'optional table' component 'optional table selection'
							'mapping' component 'mapping definition'
						)
					'collection' ['collection']
						'table' component 'table selection'
						'mapping' component 'mapping definition'
				)
		)
	)
```
