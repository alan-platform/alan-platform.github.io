---
layout: doc
origin: webclient
language: translations
version: morpheus.rc6.0
type: grammar
---


```js
'language' ['language:'] text
```

```js
'engine language' ['engine' 'language:'] stategroup (
	'english' ['english']
	'dutch'['dutch']
)
```

```js
'translations' collection indent (
	'translation' [ ':' ] text
)
```
```
