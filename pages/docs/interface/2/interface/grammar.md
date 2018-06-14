---
layout: doc
origin: interface
language: interface
type: grammar
version: 2
---


## root [ 'interface' ]


### context keys

```js
	'context keys' [ '(' , ')' ] collection ( )
```

### root

```js
	'root' [ 'root' ] component 'node'
```

### component types

```js
	'component types' [ 'component' 'types' ] collection (
		'node' [ '->' ] component 'node'
	)
```

### numerical types

```js
	'numerical types' [ 'numerical' 'types' ] collection (
		'has factor' stategroup (
			'no'
			'yes'
				'base' number
				'exponent' [ '^' ] number
		)
	)
```

## component rules


### node

```js
	'node' [ '(' , ')' ]
		'attributes' collection (
			'type' [ '->' ] stategroup (
				'command' [ 'command' ]
					'parameters' component 'command parameters'
				'property'
					'type' stategroup (
						'component' [ 'component' ]
							'type' reference
						'collection'
							'type' stategroup (
								'dictionary' [ 'dictionary' ]
								'matrix' [ 'matrix' ]
									'referencer' component 'referencer'
							)
							'node' component 'node'
						'group' [ 'group' ]
							'node' component 'node'
						'number'
							'set' stategroup (
								'integer' ['integer']
								'natural' ['natural']
							)
							'type' reference
						'reference' [ 'reference' ]
							'referencer' component 'referencer'
						'state group' [ 'stategroup' ]
							'output parameters' collection ( [ '(' , ')' ]
								'node selection' [ '->' ] component 'node type path'
							)
							'states' [ '(' , ')' ] collection (
								'output arguments' [ '->' ] collection ( [ '(' , ')' ]
									'path' [ '->' ] component 'node selection path'
								)
								'node' component 'node'
							)
						'text' [ 'text' ]
						'file' ['file']
					)
			)
		)
```

### node type path

```js
	'node type path'
		'root type' stategroup (
			'root'
			'component type' [ '!' ]
				'component type' reference
		)
		'steps' component 'node type path step'
```

### node type path step

```js
	'node type path step'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state' [ '?' ]
						'state group' reference
						'state' [ '*' ] reference
					'collection' [ '.' ]
						'collection' reference
					'group' [ '+' ]
						'group' reference
				)
				'tail' component 'node type path step'
		)
```

### node selection path

```js
	'node selection path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state parent' [ '?^' ]
					'collection parent' [ '.^' ]
					'group parent' [ '+^' ]
					'state group output parameter' [ '?' ]
						'state group' reference
						'output parameter' [ '$' ] reference
					'group' [ '+' ]
						'group' reference
					'reference' [ '>' ]
						'reference' reference
					'matrix key' [ '%}' ]
				)
				'tail' component 'node selection path'
		)
```

### node content path

```js
	'node content path'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'state' [ '?' ]
						'state group' reference
						'state' [ '*' ] reference
					'group' [ '+' ]
						'group' reference
				)
				'tail' component 'node content path'
		)
```

### referencer

```js
	'referencer' [ '(' , ')' ]
		'head' component 'node selection path'
		'collection' [ '.' ] reference
		'tail' component 'node content path'
```

### command parameters

```js
	'command parameters'
		[ '(' , ')' ]
		'properties' collection (
			'type' [ '->' ] stategroup (
				'matrix'
					'type' stategroup (
						'dense' [ 'densematrix' ]
						'sparse' [ 'sparsematrix' ]
					)
					'referencer' component 'command parameter referencer'
					'parameters' [ '->' ] component 'command parameters'
				'reference' [ 'reference' ]
					'referencer' component 'command parameter referencer'
				'number'
					'set' stategroup (
						'integer' [ 'integer' ]
						'natural' [ 'natural' ]
					)
					'numerical type' reference
				'text' [ 'text' ]
				'file' ['file']
				'state group' [ 'stategroup' ]
					'states' [ '(' , ')' ] collection (
						'parameters' [ '->' ] component 'command parameters'
					)
			)
		)
```

### ancestor parameters selection

```js
	'ancestor parameters selection'
		'has steps' stategroup (
			'no'
			'yes'
				'type' stategroup (
					'matrix parent' [ '.^' ]
					'state parent' [ '?^' ]
				)
				'tail' component 'ancestor parameters selection'
		)
```

### command parameter referencer

```js
	'command parameter referencer' [ '(' , ')' ]
		'context type' stategroup (
			'command parameter' [ '$' ]
				'ancestor selection' component 'ancestor parameters selection'
				'type' stategroup (
					'key' [ '%}' ]
					'reference'
						'reference' [ '>' ] reference
				)
			'context node'
		)
		'head' component 'node selection path'
		'collection' [ '.' ] reference
		'tail' component 'node content path'
```
