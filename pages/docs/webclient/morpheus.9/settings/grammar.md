---
layout: doc
origin: webclient
language: settings
version: morpheus.9
type: grammar
---


```js
'settings' [ 'settings' ] group (
	'application creator' [ 'application' 'creator' ':' ] reference
	'application name' [ 'application' 'name' ':' ] reference
	'default language' [ 'default' 'language' ':' ] reference
	'allow anonymous user' [ 'anonymous' 'login' ':' ] stategroup (
		'no' [ 'disabled' ]
		'yes' [ 'enabled' ]
	)
	'reload on unexpected error' [ 'reload' 'on' 'unexpected' 'error' ':' ] stategroup (
		'enabled' [ 'enabled' ]
		'disabled' [ 'disabled' ]
	)
	'content selection' [ 'content' 'selection' ':' ] stategroup (
		'enabled' [ 'enabled' ]
		'disabled' [ 'disabled' ]
	)
	'report limit' [ 'report' 'limit' ':' ] number
	'announcement title' [ 'announcement' ':' ] text
	'announcements' [ '[' , ']' ] collection indent ( )
)
```

```js
'windows' [ 'windows' ] collection indent ( )
```

```js
'allow deeplink' stategroup (
	'yes' [ 'deeplink' 'to' ':' ]
		'target window' reference
	'no'
)
```
```
