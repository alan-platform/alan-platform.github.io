---
layout: doc
origin: datastore
language: migration_mapping
version: app-extensions.1
type: grammar
---


```js
'none' group
(
	'operation' component 'tag: operation type'
	'stack'     component 'tag: variable stack'
)
```

```js
'context' group
(
	'singular' component 'tag: context type'
	'plural'   component 'tag: context type'
)
```

```js
'root' ['root'] group
(
	'context'  component 'context creation'
	'variable' ['=' 'root' 'as' '$'] component 'variable assignment: context'
	'root'     component 'node mapping'
)
```
```
/* data context information */
```

```js
'tag: context type'
```

```js
'tag: context'
```

```js
'context creation'
	'tag' component 'tag: context'
/* execution context information */
```

```js
'tag: operation type'
```

```js
'unguaranteed operation'
	'is' ['<!', '!>'] stategroup
	(
		'unguarded'
			'annotation' text
		'guarded'
	)
/* static data descriptors */
```

```js
'static: number list'
	'type' stategroup
	(
		'single'
			'value' number
		'range'
			'begin' number
			'end' ['-'] number
	)
	'has more' stategroup
	(
		'yes'
			'tail' [','] component 'static: number list'
		'no'
	)
```

```js
'static: text list'
	'value' text
	'has more' stategroup
	(
		'yes'
			'tail' [','] component 'static: text list'
		'no'
	)
/* variable stack */
```

```js
'tag: variable stack'
```

```js
'tag: variable'
	'tag' component 'tag: variable stack'
```

```js
'variable selector'
	'is' stategroup ('stack frame')
	'select' stategroup
	(
		'this' ['$']
		'parent' ['$^']
			'tail' component 'variable selector'
		'partition'
			'select' stategroup
			(
				'key' ['$key']
				'set' ['$set']
			)
		'branch' ['$']
			'branch' reference
	)
```

```js
'variable assignment: context'
	'variable' component 'tag: variable'
```

```js
'variable assignment: number'
	'variable' component 'tag: variable'
```

```js
'variable assignment: text'
	'variable' component 'tag: variable'
```

```js
'variable assignment: regexp'
	'variable' component 'tag: variable'
```

```js
'variable assignment: array'
	'variable' component 'tag: variable'
```

```js
'variable assignment: partition'
	'variable' component 'tag: variable'
```

```js
'variable assignment: block'
	'branches' ['(',')'] collection indent
	( ['$']
		'type' stategroup
		(
			'context' ['=']
				'expression' component 'context selector'
				'context' component 'context creation'
				'assignment' component 'variable assignment: context'
			'array' [':''array''=']
				'selection' component 'context selector'
				'is' stategroup ('plural context')
				'transformation' stategroup
				(
					'none' ['on']
						'unguaranteed operation' component 'unguaranteed operation'
					'partition' ['partition']
						'bucket context' component 'context creation'
				)
				'index' ['[',']'] group
				(
					'context' component 'context creation'
					'variable' component 'variable assignment: context'
					'expression' component 'number expression'
				)
				'assignment' component 'variable assignment: array'
			'regexp' [':''regexp']
				'regexp' ['='] reference
				'unguaranteed operation' component 'unguaranteed operation'
				'value' ['on'] component 'text expression'
				'assignment' component 'variable assignment: regexp'
			'number' [':''number']
				'expression' ['='] component 'number expression'
				'assignment' component 'variable assignment: number'
			'text' [':''text']
				'expression' ['='] component 'text expression'
				'assignment' component 'variable assignment: text'
		)
	)
	'variable' component 'tag: variable'
/* type specific context selection */
```

```js
'context selector recursive'
	'step' stategroup
	(
		'yes'
			'type' stategroup
			(
				'group'
					'is' stategroup
					(
						'singular context'
							'group' ['+'] reference
						'plural context'
							'group' ['+','*'] reference
					)
				'collection'
					'is' stategroup
					(
						'singular context'
							'collection' ['.'] reference
						'plural context'
							'collection' ['.','*'] reference
					)
				'entry'
					'is' stategroup
					(
						'singular context'
							'collection' ['.'] reference
							'key' ['[',']'] group
							(
								'expression' component 'text expression'
							)
							'unguaranteed operation' component 'unguaranteed operation'
						'plural context'
							'collection' ['.','*'] reference
							'key' ['[',']'] group
							(
								'context' component 'context creation'
								'variable' component 'variable assignment: context'
								'expression' component 'text expression'
							)
							'unguaranteed operation' component 'unguaranteed operation'
					)
				'reference'
					'is' stategroup
					(
						'singular context'
							'reference' ['>'] reference
							'has' stategroup ('referencer')
						'plural context'
							'reference' ['>','*'] reference
							'has' stategroup ('referencer')
					)
				'parent'
					'is' stategroup
					(
						'singular context' ['^']
						'plural context' ['^','*']
					)
			)
			'temp' component 'context creation'
			'optional assignment' stategroup
			(
				'assign' ['as' '$']
					'variable' component 'variable assignment: context'
				'skip'
			)
			'tail' component 'context selector recursive'
		'no'
	)
```

```js
'context selector'
	'source' stategroup
	(
		'stack'
			'selection' component 'variable selector'
			'is' stategroup ('context variable')
		'array'
			'operation' stategroup
			(
				'predecessor' ['predecessor']
				'successor' ['successor']
			)
			'key expression' ['of'] component 'number expression'
			'selection' ['in'] component 'variable selector'
			'unguaranteed operation' component 'unguaranteed operation'
			'is' stategroup ('array variable')
	)
	'steps' component 'context selector recursive'
	'guaranteed' stategroup ('by implementation')
/* generic sub expressions */
```

```js
'regexp selector'
	'source' stategroup
	(
		'stack'
			'selection' component 'variable selector'
			'is' stategroup ('regexp')
		'inline' ['inline']
			'regexp' reference
			'unguaranteed operation' component 'unguaranteed operation'
			'value' ['on'] component 'text expression'
	)
```

```js
'number expression list'
	'expression' component 'number expression'
	'has more' stategroup (
		'no'
		'yes' [',']
			'tail' component 'number expression list'
	)
```

```js
'number expression'
	'type' stategroup
	(
		'convert text'
			'value constraint' stategroup
			(
				'integer' ['to-integer']
				'natural' ['to-natural']
			)
			'unguaranteed operation' component 'unguaranteed operation'
			'value' component 'text expression'
		'cast to natural' ['(natural)']
			'unguaranteed operation' component 'unguaranteed operation'
			'value' component 'number expression'
		'convert date' ['to-date']
			'unguaranteed operation' component 'unguaranteed operation'
			'selection' component 'regexp selector'
			'year' ['where' 'year' '='] reference
			'offset' stategroup
			(
				'month based'
					'month'        ['month' '='] reference
					'day of month' ['day' '='] reference
				'week based'
					'week' ['week' '='] reference
					'day of week' ['day' '='] stategroup
					(
						'monday'    ['Monday']
						'tuesday'	['Tuesday']
						'wednesday'	['Wednesday']
						'thursday'	['Thursday']
						'friday'	['Friday']
						'saturday'	['Saturday']
						'sunday'    ['Sunday']
					)
			)
		'convert date and time' ['to-datetime']
			'unguaranteed operation' component 'unguaranteed operation'
			'selection' component 'regexp selector'
			'year'         ['where' 'year' '='] reference
			'month'        ['month' '='] reference
			'day of month' ['day' '='] reference
			'hour'         ['hour' '='] reference
			'minute'       ['minute' '='] reference
			'second'       ['second' '='] reference
		'from context'
			'is' stategroup
			(
				'singular context'
				'plural context'
					'operation' stategroup
					(
						'shared value' ['shared']
							'unguaranteed operation' component 'unguaranteed operation'
						'sum' ['sum']
						'max' ['max']
							'unguaranteed operation' component 'unguaranteed operation'
						'min' ['min']
							'unguaranteed operation' component 'unguaranteed operation'
					)
			)
			'selection' component 'context selector'
			'number' ['.'] reference
		'from variable'
			'selection' component 'variable selector'
			'is' stategroup ('number variable')
		'conditional'
			'is' stategroup (
				'singular context' ['switch']
				'plural context' ['switch-shared']
					'unguaranteed operation' component 'unguaranteed operation'
			)
			'selection' ['('] component 'context selector'
			'state group' ['?',')'] reference
			'branches' ['(',')'] collection ( ['|']
				'optional variable assignment' stategroup (
					'assign' ['as''$']
						'context' component 'context creation'
						'variable' component 'variable assignment: context'
					'skip'
				)
				'expression' ['='] component 'number expression'
			)
		'unary operation'
			'operation' stategroup (
				'additive inverse' ['-']
			)
			'expression' component 'number expression'
		'list operation'
			'operation' stategroup (
				'sum' ['sum']
				'product' ['product']
			)
			'list' ['(',')'] component 'number expression list'
		'division' ['division']
			'left' ['('] component 'number expression'
			'right' [',',')'] component 'number expression'
		'static value'
			'value constraint' stategroup
			(
				'integer' ['integer']
					'value' number
				'natural' ['natural']
					'value' number
			)
	)
```

```js
'numerical set constraint'
```

```js
'text expression: concatenate'
	'expression' component 'text expression'
	'has more' stategroup
	(
		'yes' [',']
			'tail' component 'text expression: concatenate'
		'no'
	)
```

```js
'text expression'
	'type' stategroup
	(
		'convert number' ['to-text']
			'value' component 'number expression'
		'from context'
			'is' stategroup
			(
				'singular context'
				'plural context'
					'operation' stategroup
					(
						'shared value' ['shared']
							'unguaranteed operation' component 'unguaranteed operation'
						'join' ['join']
							'separator' text
					)
			)
			'selection' component 'context selector'
			'text' ['.'] reference
		'from regexp' ['regexp']
			'selection' component 'regexp selector'
			'capture' ['@'] reference
		'from variable'
			'selection' component 'variable selector'
			'is' stategroup ('text')
		'conditional'
			'is' stategroup (
				'singular context' ['switch']
				'plural context' ['switch-shared']
					'unguaranteed operation' component 'unguaranteed operation'
			)
			'selection' ['('] component 'context selector'
			'state group' ['?',')'] reference
			'branches' ['(',')'] collection ( ['|']
				'optional variable assignment' stategroup (
					'assign' ['as''$']
						'context' component 'context creation'
						'variable' component 'variable assignment: context'
					'skip'
				)
				'expression' ['='] component 'text expression'
			)
		'concatenation' ['concat']
			'expressions' ['(', ')'] component 'text expression: concatenate'
		'static value'
			'value' text
	)
```

```js
'boolean expression: candidates'
	'expression' component 'boolean expression'
	'has more' stategroup
	(
		'yes' [',']
			'tail' component 'boolean expression: candidates'
		'no'
	)
```

```js
'boolean expression'
	'type' stategroup
	(
		'logic operation'
			'operation' stategroup
			(
				'and' ['and']
				'or'  ['or']
			)
			'expressions' ['(', ')'] component 'boolean expression: candidates'
		'compare number'
			'sub type' stategroup
			(
				'binary operation'
					'left' ['#'] component 'number expression'
					'operation' stategroup
					(
						'equal' ['==']
						'greater' ['>']
						'greater equal' ['>=']
						'smaller' ['<']
						'smaller equal' ['<=']
					)
					'right' ['#'] component 'number expression'
				'set operation' ['is']
					'find' ['#','in'] component 'number expression'
					'in' ['(', ')'] component 'static: number list'
			)
		'compare text'
			'sub type' stategroup
			(
				'binary operation'
					'left' component 'text expression'
					'operation' stategroup
					(
						'equals' ['equals']
						'starts with' ['starts-with']
						'ends with' ['ends-with']
					)
					'right' component 'text expression'
				'set operation'
					'find' ['is','in'] component 'text expression'
					'in' ['(', ')'] component 'static: text list'
			)
	)
```

```js
'collection selector'
	'variable type' ['(', ')'] stategroup
	(
		'context'
			'selection' component 'context selector'
			'context'  component 'context creation'
		'array' ['array']
			'selection' component 'variable selector'
			'is' stategroup ('array context')
			'guaranteed' stategroup ('by implementation')
	)
```

```js
'collection expression'
	'type' stategroup (
		'map' ['map']
			'selection' component 'collection selector'
			'optional assignment' stategroup (
				'assign' ['as''$']
					'variable' component 'variable assignment: context'
				'skip'
			)
			'mapping' component 'collection expression'
		'partition' ['partition']
			'set is' stategroup ('plural context')
			'row is' stategroup ('singular context')
			'selection' component 'collection selector'
			'index' group
			( ['[', ']']
				'variable' component 'variable assignment: context'
				'expression' component 'text expression'
			)
			'set context' component 'context creation'
			'optional assignment' stategroup
			(
				'assign' ['as' '(' '$key' ',' '$set' ')']
					'key variable' component 'variable assignment: text'
					'set variable' component 'variable assignment: context'
					'variable' component 'variable assignment: partition'
				'skip'
			)
			'mapping' component 'collection expression'
		'conditional'
			'is' stategroup (
				'singular context' ['switch']
				'plural context' ['switch-shared']
					'unguaranteed operation' component 'unguaranteed operation'
			)
			'selection' ['('] component 'context selector'
			'state group' ['?',')'] reference
			'branches' ['(',')'] collection ( ['|']
				'optional variable assignment' stategroup (
					'assign' ['as''$']
						'context' component 'context creation'
						'variable' component 'variable assignment: context'
					'skip'
				)
				'expression' component 'collection expression'
			)
		'new entry' ['=']
			'mapping' component 'node mapping'
		'sub expression' ['(',')']
			'list' component 'collection expression list'
		'none' ['none']
	)
```

```js
'collection expression list'
	'has expressions' stategroup (
		'yes'
			'expression' component 'collection expression'
			'tail' component 'collection expression list'
		'no'
	)
```

```js
'collection mapping' ['=']
	'unguaranteed operation' component 'unguaranteed operation'
	'expression' component 'collection expression'
```

```js
'state mapping' ['=']
	'type' stategroup
	(
		'panic' ['panic']
			'comment' text
		'conditional' ['match']
			'condition' ['(', ')'] component 'boolean expression'
			'on true'  ['|' 'true'] component 'state mapping'
			'on false' ['|' 'false'] component 'state mapping'
		'enrich' ['try']
			'try assign' component 'variable assignment: block'
			'guarded operation' component 'tag: operation type'
			'on success' ['|' 'success'] component 'state mapping'
			'on failure' ['|' 'failure'] component 'state mapping'
		'context switch'
			'selection' component 'context selector'
			'is' stategroup ('plural context')
			'on singular' ['|''singular'] group
			(
				'context' component 'context creation'
				'variable' component 'variable assignment: context'
				'mapping' component 'state mapping'
			)
			'on plural' ['|''plural'] group
			(
				'context' component 'context creation'
				'variable' component 'variable assignment: context'
				'mapping' component 'state mapping'
			)
		'from context'
			'is' stategroup
			(
				'singular context' ['switch']
				'plural context' ['switch-shared']
					'unguaranteed operation' component 'unguaranteed operation'
			)
			'selection' ['('] component 'context selector'
			'state group' ['?',')'] reference
			'mappings' ['(',')'] collection indent
			( ['|']
				'optional variable assignment' stategroup
				(
					'assign' ['as' '$']
						'context'  component 'context creation'
						'variable' component 'variable assignment: context'
					'skip'
				)
				'mapping' component 'state mapping'
			)
		'from array'
			'operation' stategroup
			(
				'first' ['first']
				'last' ['last']
			)
			'selection' ['in'] component 'variable selector'
			'is' stategroup ('array variable')
			'optional variable assignment' stategroup
			(
				'assign'
					'variable' ['as' '$'] component 'variable assignment: context'
				'skip'
			)
			'on success' ['|' 'success' ] component 'state mapping'
			'on failure' ['|' 'failure' ] component 'state mapping'
		'set state'
			'state' reference
			'mapping' component 'node mapping'
	)
```

```js
'node mapping' ['(',')']
	'define block' stategroup
	(
		'yes'
			'block' component 'variable assignment: block'
		'no'
	)
	'properties' collection indent
	(
		'type' [':'] stategroup
		(
			'group' ['group']
				'optional binding' ['='] stategroup
				(
					'bind'
						'selection' component 'context selector'
						'context' ['as'] component 'context creation'
						'variable' ['$'] component 'variable assignment: context'
					'skip'
				)
				'mapping' component 'node mapping'
			'collection' ['collection']
				'mapping' component 'collection mapping'
			'stategroup' ['stategroup']
				'mapping' component 'state mapping'
			'number'
				'set type' stategroup
				(
					'integer' ['integer']
					'natural' ['natural']
						'equivalent set type' component 'numerical set constraint'
				)
				'value source' ['='] stategroup
				(
					'clock' ['now']
					'source'
						'expression' component 'number expression'
				)
			'text' ['text']
				'expression' ['='] component 'text expression'
			'file' ['file']
				'value source' ['='] stategroup
				(
					'static' ['[', ']']
						'token' text
						'extension' [','] text
					'context'
						'is' ['/'] stategroup
						(
							'singular context'
							'plural context' ['shared']
								'unguaranteed operation' component 'unguaranteed operation'
						)
						'selection' component 'context selector'
						'file' ['.'] reference
				)
		)
	)
```
