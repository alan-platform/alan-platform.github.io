---
layout: doc
origin: datastore
language: migration
version: 38
type: grammar
---


## root


### no regexp context

```js
'no regexp context' component 'regexp context'
```

### root context

```js
'root context' component 'node context'
```

### root danger

```js
'root danger' component 'unsafe context'
```

### no enriched

```js
'no enriched' component 'enriched'
```

### root

```js
'root' ['root'] component 'node mapping'
```

### numerical types
Converts numerical types from the 'from' model to the target 'to' model.
Conversions can be chained.
Examples:
- no conversion:  `'source' -> 'target'`
- multiplication: `'source' -> 'target'  = 'source' * 10`
- division:       `'hours'  -> 'minutes' = 'hours' / 10` = 'days' / 1440

```js
'numerical types' ['numerical' 'type' 'conversion'] collection indent (
	'underlying type' ['->'] reference
	'conversion rules' collection ( ['=']
		'rule' stategroup (
			'copy'
			'multiply' ['*']
				'factor' number
			'divide' ['/']
				'factor' number
		)
	)
)
```

### numerical type mappings
Maps numerical types, `'source' -> 'target'`

```js
'numerical type mappings' ['numerical' 'type' 'mapping'] collection indent (
	'to type' ['->'] reference
)
```

## component rules


### context

```js
'context'
```

### regexp context

```js
'regexp context'
```

### node context

```js
'node context'
	'context' component 'context'
```

### regexp set context

```js
'regexp set context'
```

### node set context

```js
'node set context'
	'context' component 'context'
```

### dangerous context

```js
'dangerous context'
```

### safe context

```js
'safe context'
	'danger' component 'dangerous context'
```

### unsafe context

```js
'unsafe context'
	'danger' component 'dangerous context'
```

### unguaranteed operation
Mark an operations that might not succeed given certain data.

```js
'unguaranteed operation'
	'context switch' stategroup (
		'safe'
		'unsafe' ['<!', '>']
			'comment' text
	)
```

### enriched

```js
'enriched'
```

### numerical type dereference

```js
'numerical type dereference'
```

### node context creation

```js
'node context creation'
	'regexp' stategroup (
		'inherit'
		'instance' ['instance' 'regexp']
			'expression' reference
			'unguaranteed operation' component 'unguaranteed operation'
			'value' component 'text expression'
			'regexp' component 'regexp context'
	)
	'context node' component 'node context'
```

### node set context creation

```js
'node set context creation'
	'regexp set' stategroup (
		'inherit'
		'instance' ['instance' 'regexp']
			'expression' reference
			'unguaranteed operation' component 'unguaranteed operation'
			'value' component 'text expression'
			'regexp set' component 'regexp set context'
	)
	'context node' component 'node set context'
```

### context selection path

```js
'context selection path'
	'has steps' stategroup (
		'no'
			'context creation' stategroup (
				'none'
				'node context' [':']
					'context creation' component 'node context creation'
				'node set context' [':(', ')']
					'context set creation' component 'node set context creation'
			)
		'yes'
			'type' stategroup (
				'group' ['+']
					'source group' reference
					'context creation' component 'node context creation'
				'group set' ['+(', ')']
					'source group' reference
					'context set creation' component 'node set context creation'
				'collection'
					'source collection' stategroup (
						'dictionary' ['.']
							'source dictionary' reference
						'matrix' ['%']
							'source matrix' reference
					)
					'context regexp set' component 'regexp set context'
					'context set creation' component 'node set context creation'
				'collection set'
					'source collection' stategroup (
						'dictionary' ['.(', ')']
							'source dictionary' reference
						'matrix' ['%(', ')']
							'source matrix' reference
					)
					'context regexp set' component 'regexp set context'
					'context set creation' component 'node set context creation'
				'entry' ['entry']
					'source' stategroup (
						'expression'
							'entry' component 'entry expression'
						'enrichment' ['@']
							'entry' reference
					)
					'context creation' component 'node context creation'
				'reference' ['>']
					'source reference' reference
					'context creation' component 'node context creation'
				'reference set' ['>(', ')']
					'source reference' reference
					'context set creation' component 'node set context creation'
				'matrix key' ['>key']
					'source location' stategroup ( 'constrain' )
					'context creation' component 'node context creation'
				'matrix key set' ['>key(', ')']
					'source location' stategroup ( 'constrain' )
					'context set creation' component 'node set context creation'
				'parent'
					'parent type' stategroup (
						'dictionary' ['.^']
							'context creation' component 'node context creation'
						'matrix' ['%^']
							'context creation' component 'node context creation'
						'group' ['+^']
							'context creation' component 'node context creation'
						'state group' ['?^']
							'context creation' component 'node context creation'
					)
				'parent set'
					'parent type' stategroup (
						'dictionary' ['.^(', ')']
							'context set creation' component 'node set context creation'
						'matrix' ['%^(', ')']
							'context set creation' component 'node set context creation'
						'group' ['+^(', ')']
							'context set creation' component 'node set context creation'
						'state group' ['?^(', ')']
							'context set creation' component 'node set context creation'
					)
			)
			'tail' component 'context selection path'
	)
```

### entry expression

```js
'entry expression'
	'key' ['find'] group (
		'context selection' component 'context selection path'
		'value' [':'] component 'text expression'
	)
	'target' ['in'] group (
		'context selection' component 'context selection path'
		'source collection' [':'] stategroup (
			'dictionary' ['.']
				'source dictionary' reference
			'matrix' ['%']
				'source matrix' reference
		)
	)
	'unguaranteed operation' component 'unguaranteed operation'
```

### collection expression
Set a collection:
- Select source collection: `'target': dictionary = .'source' { }`
- Static: `'target': dictionary = { }`

```js
'collection expression'
	'target' stategroup (
		'static entries'
			'entries' ['(', ')'] collection indent (
				'mapping' component 'node mapping'
			)
		'migrate entries'
			'source collection' stategroup (
				'dictionary' ['.']
					'source dictionary' reference
				'matrix' ['%']
					'source matrix' reference
			)
			'transformation' stategroup (
				'map node'
					'context node' component 'node context'
					'mapping' component 'node mapping'
				'aggregate'
					'regular expression' ['regexp'] reference
					'key expression' ['/'] reference
					'unguaranteed operation' component 'unguaranteed operation'
					'context regexp set' component 'regexp set context'
					'context node set' component 'node set context'
					'mapping' ['(', ')'] component 'node mapping'
			)
		'migrate set'
			'key' ['(', ')'] group (
				'context regexp' component 'regexp context'
				'context node' component 'node context'
				'expression' component 'text expression'
			)
			'transformation' stategroup (
				'map node'
					'unguaranteed operation' component 'unguaranteed operation'
					'context regexp' component 'regexp context'
					'context node' component 'node context'
					'mapping' component 'node mapping'
				'aggregate'
					'context regexp set' component 'regexp set context'
					'context node set' component 'node set context'
					'mapping' ['(', ')'] component 'node mapping'
			)
	)
```

### number expression
Set a number:
- Select source number:             `'target': number = #'source' as 'unit`.
- Set a static value:               `'target': number = 10 as 'unit'`.
- Set a static natural value:       `'target': number = natural 10 as 'unit'`.
- Calculate:                        `'target': number = ( #'a' as 'unit' +  #'b' as 'unit' )`.
- Convert text to number:           `'target': number = to-number .'text property' as 'unit' <!"usually a number">`.
- Convert from another number type: `'target': number = cast 'source' as 'unit' ('conversion')`.
- Enriched?
- Merge?

```js
'number expression'
	'type' stategroup (
		'number'
			'source number' ['#'] reference
			'numerical type mapping' ['as'] reference
		'static'
			'value' stategroup (
				'integer'
					'integer value' number
				'natural' ['natural']
					'natural value' number
			)
			'numerical type' ['as'] reference
		'arithmetic operator' ['(', ')']
			'left context' component 'context selection path'
			'left number' component 'number expression'
			'type' stategroup (
				'add' ['+']
				'subtract' ['-']
				'multiply' ['*']
				'divide' ['/']
			)
			'right context' component 'context selection path'
			'right number' component 'number expression'
		'convert text' ['to-number']
			'value' component 'text expression'
			'conversion block' group (
				'numerical type' ['as'] reference
				'unguaranteed operation' component 'unguaranteed operation'
			)
		'numerical type conversion' ['convert']
			'value to cast' component 'number expression'
			'conversion block' group (
				'numerical type' ['to'] reference
				'conversion rule' ['(',')'] reference
			)
		'enriched' ['@']
			'value' reference
		'merge'
			'type' stategroup (
				'shared value' ['shared']
				'sum' ['sum']
			)
			'unguaranteed operation' component 'unguaranteed operation'
			'context regexp' component 'regexp context'
			'context node' component 'node context'
			'values to merge' ['(', ')'] component 'number expression'
	)
```

### text expression
Set a text:
- Select a source text:      `'target': text = .'source'`
- Select a source reference: `'target': text = >'source'`
- Set a static value:        `'target': text = "some text"`
- Convert a number:          `'target': text = to-text #'number' as 'unit'`
- Select a key:              `'target': text = .key`
- Concatenate:               `'target': text = ( .key , "-" , to-text #'number' as 'unit' )`
- Regexp?
- Enriched?
- Merge?

```js
'text expression'
	'type' stategroup (
		'property'
			'data type' stategroup (
				'text'
					'source text' ['.'] reference
				'reference'
					'source reference' ['>'] reference
			)
		'static'
			'value' text
		'stringify' ['to-text']
			'value' component 'number expression'
		'key'
			'collection type' stategroup (
				'dictionary' ['.key']
				'matrix' ['>key']
			)
		'concatenation operator' ['(', ')']
			'left context'  component 'context selection path'
			'left text' component 'text expression'
			'separator' [',', ','] text
			'right context' component 'context selection path'
			'right text' component 'text expression'
		'regexp' ['regexp']
			'type' stategroup (
				'context'
					'context type' stategroup (
						'node'
						'node set'
							'merge' stategroup (
								'shared value' ['shared']
							)
							'unguaranteed operation' component 'unguaranteed operation'
					)
				'inline'
					'expression' reference
					'unguaranteed operation' component 'unguaranteed operation'
					'value' component 'text expression'
			)
			'capture' ['/'] reference
		'enriched' ['@']
			'value' reference
		'merge'
			'type' stategroup (
				'shared value' ['shared']
			)
			'unguaranteed operation' component 'unguaranteed operation'
			'context regexp' component 'regexp context'
			'context node' component 'node context'
			'values to merge' ['(', ')'] component 'text expression'
	)
```

### boolean expression
Compare numbers or texts to decide how to map stategroups.
Examples:
- `number 'unit'#'number' > 'unit' 10`
- `text 'property' == "some text"`

```js
'boolean expression'
	'type' stategroup (
		'compare number' ['number']
			'left context' component 'context selection path'
			'left operand' component 'number expression'
			'operator' stategroup (
				'equal' ['==']
				'smaller' ['<']
				'greater' ['>']
			)
			'right context' component 'context selection path'
			'right operand' component 'number expression'
		'compare text' ['text']
			'left context' component 'context selection path'
			'left operand' component 'text expression'
			'operator' stategroup (
				'equal' ['==']
			)
			'right context' component 'context selection path'
			'right operand' component 'text expression'
	)
	'has tail' stategroup (
		'no'
		'yes' ['&&']
			'tail' component 'boolean expression'
	)
```

### state group expression
Set stategroup value or map states:
- Map to *stategroup*:  `'target': stategroup = switch ( ?'source' ) ( |'a' -> 'a' { } |'b' -> 'b' { } )`
- Set a static value:   `'target': stategroup = 'a' { }`
- Conditional:          `'target': stategroup = match ( <boolean expression> ) | true = 'yes' { } | false = 'no' { }`
- Shared state?
- Enrich?
- Panic: use this to abort a migration data doesn't match your expectations,
  e.g. in an `else` statement, for numbers that are out of range.

```js
'state group expression'
	'type' stategroup (
		'switch state' ['switch' '(']
			'source state group' ['?', ')'] reference
			'mapping' ['(', ')'] collection indent ( ['|']
				'context node' component 'node context'
				'expression' ['='] component 'state group expression'
			)
		'set state'
			'to state' reference
			'mapping' component 'node mapping'
		'conditional' ['match']
			'condition' ['(', ')'] component 'boolean expression'
			'on true' ['|' 'true' '='] component 'state group expression'
			'on false' ['|' 'false' '='] component 'state group expression'
		'switch shared state' ['switch' '(']
			'unguaranteed operation' ['shared'] component 'unguaranteed operation'
			'source state group' ['?', ')'] reference
			'mapping' ['(', ')'] collection indent ( ['|']
				'context node set' component 'node set context'
				'expression' ['='] component 'state group expression'
			)
		'enrich' ['enrich']
			'safe' component 'safe context'
			'enriched' component 'enriched'
			'enrichments' collection indent ( ['@']
				'data type' ['='] stategroup (
					'number'
						'numerical type' ['(', ')'] reference
						'expression' component 'number expression'
					'text'
						'expression' component 'text expression'
					'entry'
						'expression' component 'entry expression'
				)
			)
			'unsafe' component 'unsafe context'
			'on success' ['|' 'success'] component 'state group expression'
			'on failure' ['|' 'failure'] component 'state group expression'
		'panic' ['panic'] // this cause a panic, which aborts the migration without ANY output!
	)
```

### node mapping
Basic target : source mapping.
Use `( + 'some group' )` to walk into a context (e.g. a group) before mapping the node.

```js
'node mapping' ['(', ')']
	'properties' collection indent (
		'source context' stategroup (
			'input context'
			'local context' ['(', ')']
				'source context' component 'context selection path'
		)
		'type' [':'] stategroup (
			'group' ['group' '=']
				'mapping' component 'node mapping'
			'reference' ['text' '=>']
				'expression' component 'text expression'
			'dictionary' ['collection' '=']
				'expression' component 'collection expression'
			'matrix' ['collection' '=>']
				'expression' component 'collection expression'
			'number' ['number' '=']
				'expression' component 'number expression'
				'numerical type' component 'numerical type dereference'
			'text' ['text' '=']
				'expression' component 'text expression'
			'file' ['file']
				'type' stategroup (
					'property'['=']
						'source file' ['/'] reference
					'expression' ['(',')']
						'token' ['token' '='] component 'text expression'
						'extension' ['extension' '='] component 'text expression'
				)
			'state group' ['stategroup' '=']
				'expression' component 'state group expression'
		)
	)
```
