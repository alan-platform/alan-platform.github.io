---
layout: doc
origin: model
language: collection_query_to_table
version: 34
type: grammar
---


## root


### type

```js
'type' stategroup (
	'collection query' ['collection' 'query']
		'columns' component 'collection block'
	'acyclic graph list query' ['graph' 'query']
		'columns' component 'list block'
)
```

## component rules


### collection block

```js
'collection block'
	'has columns' stategroup (
		'no'
		'yes'
			'header' text
			'property' ['->' 'select'] reference
			'type' ['as'] stategroup (
				'number' ['number']
				'text' ['text']
				'state' ['state']
				'date' ['date']
				'time' ['time']
				'datetime' ['datetime']
				'decimal' ['decimal'] 'shift' number
			)
			'next' component 'collection block'
	)
```

### list block

```js
'list block'
	'has columns' stategroup (
		'no'
		'yes'
			'header' text
			'property' ['->' 'select'] reference
			'type' ['as'] stategroup (
				'number' ['number']
				'text' ['text']
				'state' ['state']
				'date' ['date']
				'time' ['time']
				'datetime' ['datetime']
				'decimal' ['decimal'] 'shift' number
			)
			'next' component 'list block'
	)
```
