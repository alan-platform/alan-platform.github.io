---
layout: doc
origin: connector
language: pipeline
version: 2
type: grammar
---


```js
'input data' group (
	'dataset'      component 'input data tag'
	'notification' component 'input data tag'
)
```

```js
'interface type' ['pipeline''interface:'] stategroup (
	'provide' ['provide']
		'pipeline' component 'pipeline'
		'push stage' ['push:'] reference
		'requires' stategroup ('interface notification')
)
```

```js
'input data tag'
```

```js
'pipeline'
	'stages' collection ( ['stage']
		'processor' ['(',')'] reference
		'inputs' collection (
			'type' ['<<'] stategroup (
				'interface data' ['dataset']
				'raw stream' ['raw']
			)
			'source stage' reference
		)
	)
```
