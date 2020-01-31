---
layout: doc
origin: connector
language: processor
version: 2
type: grammar
---


```js
'operation type' group (
	'safe' component 'operation tag'
	'unsafe' component 'operation tag'
)
```

```js
'existence type' group (
	'mandatory' component 'existence tag'
	'optional' component 'existence tag'
)
```

```js
'type' group (
	'undefined' component 'type tag'
	'JSON object' component 'type tag'
	'JSON array' component 'type tag'
	'boolean' component 'type tag'
	'number' component 'type tag'
	'text' component 'type tag'
)
```

```js
'input data' ['input:'] collection (
	'type' [':'] stategroup (
		'interface data' ['interface-data']
			'type' component 'type tag'
		'raw stream' ['raw-stream']
	)
)
```

```js
'output data' group (
	'interface data' component 'output data tag'
	'interface notification' component 'output data tag'
	'raw stream' component 'output data tag'
)
```

```js
'schemas' collection ( ['schema']
	'root' [':'] component 'type'
)
```

```js
'processor' ['type:'] stategroup (
	'HTTP GET' ['HTTP''GET']
		'URI' component 'base text expression'
		'parameters' collection order 'order' (
			'has next' stategroup has successor 'next' 'yes' 'no'
			'value' ['='] component 'base text expression'
		)
		'has parameters' stategroup has 'parameters' first 'first' 'yes' 'no'
	'transform' ['transform']
		'root' component 'target root'
		'empty' component 'let tag'
		'statement' component 'transform statement'
	'interface diff' ['interface-diff']
		'source data' reference
)
```

```js
'operation tag'
```

```js
'existence tag'
```

```js
'type tag'
```

```js
'output data tag'
/* Constraint Types, required as equality constraints cannot be set on states */
```

```js
'echo operation tag'
/* Generic Expressions */
```

```js
'base number expression'
	'type' stategroup (
		'variable'
			'variable' ['var','number'] reference
		'static'
			'integer' number
	)
```

```js
'base text expression'
	'type' stategroup (
		'interface context key'
			'key' ['interface-key'] reference
		'variable'
			'variable' ['var','text'] reference
		'static'
			'text value' text
		'line break' ['line-break']
	)
```

```js
'number import rule'
	'decimal translation' stategroup (
		'yes' ['<<']
			'places' component 'base number expression'
		'no'
	)
/* Schema */
```

```js
'entity'
	'tag' component 'type tag'
	'type' component 'type'
```

```js
'type'
	'type' stategroup (
		'node'
			'node' component 'node'
		'collection' ['collection']
			'tag' component 'type tag'
			'entity' component 'entity'
		'list' ['list']
			'tag' component 'type tag'
			'type' component 'type'
		'boolean' ['boolean']
		'number' ['number']
			'rule' component 'number import rule'
		'text' ['text']
	)
```

```js
'node' ['{','}']
	'properties' collection (
		'type' [':'] component 'type'
	)
	'type' component 'type tag'
/* Transformer */
```

```js
'target tag'
```

```js
'target root'
	'tag' component 'target tag'
```

```js
'target node'
	'tag' component 'target tag'
```

```js
'target property'
	'tag' component 'target tag'
```

```js
'target collection'
	'tag' component 'target tag'
```

```js
'let tag'
```

```js
'let context'
	'type' stategroup (
		'single' ['$']
			'value' ['='] component 'value statement'
		'multiple'
			'values' collection ( ['$']
				'value' ['='] component 'value statement'
			)
	)
	'tag' component 'let tag'
```

```js
'let selector'
	'let context defined' stategroup (
		'yes'
			'step' stategroup (
				'parent' ['^']
					'tail' component 'let selector'
				'none'
			)
	)
```

```js
'value tail statement'
	'has step' stategroup (
		'yes'
			'type' stategroup (
				'object fetch'
					'object key' ['[',']'] component 'value statement'
					'as' ['as'] stategroup (
						'JSON object' ['object']
						'JSON array' ['array']
						'boolean' ['boolean']
						'number' ['number']
							'rule' component 'number import rule'
						'text' ['text']
					)
				'node fetch'
					'property' ['.'] reference
				'collection lookup' [':']
					'entity key' ['[',']'] component 'value statement'
				'key fetch' ['key']
				'value fetch' ['value']
				'parse' ['parse']
					'as' ['as'] stategroup (
						'JSON' ['JSON']
					)
				'decorate' ['decorate']
					'definition' ['as'] stategroup (
						'global'
							'schema' reference
						'inline'
							'root' component 'type'
					)
			)
			'tail' component 'value tail statement'
		'no'
	)
```

```js
'value statement'
	'type' stategroup (
		'simple number'
			'expression' component 'base number expression'
		'simple text'
			'expression' component 'base text expression'
		'let'
			'selection' component 'let selector'
			'value' ['$'] stategroup (
				'single'
				'select'
					'value' reference
			)
		'context' ['context']
		'input data'
			'source' ['&'] reference
		'list operation'
			'operation' stategroup (
				'sum' ['sum']
				'product' ['product']
				'concatenate' ['concatenate']
					'separator' stategroup (
						'yes'
							'value' ['[',']'] component 'value statement'
						'no'
					)
				'logical and' ['and']
				'logical or' ['or']
			)
			'values' ['(',')'] component 'value list statement'
	)
	'tail' component 'value tail statement'
	'unsafe handling' stategroup (
		'alternative' ['||']
			'requires unsafe context' component 'echo operation tag'
			'alternative' component 'value statement'
		'raise' ['||''raise']
			'requires unsafe context' component 'echo operation tag'
			'message' text
		'none' ['||''none']
			'requires unsafe context' component 'echo operation tag'
		'no'
			'requires safe context' component 'echo operation tag'
	)
```

```js
'value list statement'
	'value' component 'value statement'
	'has tail' stategroup (
		'yes' [',']
			'value' component 'value list statement'
		'no'
	)
```

```js
'compound transform statement'
	'has statement' stategroup (
		'yes'
			'statement' component 'transform statement'
			'tail' component 'compound transform statement'
		'no'
	)
```

```js
'transform statement'
	'type' stategroup (
		'let' ['let']
			'context' component 'let context'
			'statement' component 'transform statement'
		'guard' ['guard']
			'guarded statement' component 'transform statement'
			'fallback statement' ['catch'] component 'transform statement'
		'map' ['map']
			'value' stategroup (
				'schema'
					'as' stategroup (
						'collection' ['collection']
						'list' ['list']
					)
					'value' component 'value statement'
				'array' ['array']
					'value' component 'value statement'
					'as' ['as'] stategroup (
						'JSON object' ['object']
						'JSON array' ['array']
						'boolean' ['boolean']
						'number' ['number']
							'rule' component 'number import rule'
						'text' ['text']
					)
			)
			'statement' ['{','}'] component 'compound transform statement'
		'condition' ['match']
			'conditional' component 'value statement'
			'then statement' ['|''true''->'] component 'transform statement'
			'else statement' ['|''false''->'] component 'transform statement'
		/* map to target */
		'target root' ['root']
			'node' component 'target node'
			'statement' component 'transform statement'
		'target node'
			'properties' ['(',')'] collection (
				'property' component 'target property'
				'statement' ['='] component 'transform statement'
			)
		'target property'
			'type' stategroup (
				'group' ['group']
					'node' component 'target node'
					'statement' component 'transform statement'
				'collection' ['collection']
					'collection' component 'target collection'
					'statements' ['{','}'] component 'compound transform statement'
				'stategroup' ['state']
					'state' reference
					'node' component 'target node'
					'statement' component 'transform statement'
				'number' ['number']
					'value' component 'value statement'
				'text' ['text']
					'value' component 'value statement'
				'reference' ['reference']
					'value' component 'value statement'
			)
		'target collection' ['entry']
			'key' component 'value statement'
			'node' component 'target node'
			'statement' ['='] component 'transform statement'
	)
```
