---
layout: doc
origin: auto-webclient
language: generator_settings
version: laforge.1
type: grammar
---

Global settings for the user interface.

```js
'application creator' ['application' 'creator:'] text
```

```js
'application name' ['application' 'name:'] text
```

```js
'allow anonymous user' [ 'anonymous' 'login:' ] stategroup (
	'no' [ 'disabled' ]
	'yes' [ 'enabled' ]
)
```

```js
'enable csv actions' [ 'csv' 'actions:' ] stategroup (
	'no' [ 'disabled' ]
	'yes' [ 'enabled' ]
)
```

```js
'report limit' [ 'report' 'limit:' ] number
```

```js
'announcement title' [ 'announcement:' ] text
```

```js
'announcements' [ '[' , ']' ] collection indent ( )
```

```js
'custom color theme' stategroup (
	'no'
	'yes' [ 'color' 'theme:' ]
		'foreground' [ 'foreground:' ] text
		'background' [ 'background:' ] text
		'brand' [ 'brand:' ] text
		'link' [ 'link:' ] text
		'accent' [ 'accent:' ] text
		'success' [ 'success:' ] text
		'warning' [ 'warning:' ] text
		'error' [ 'error:' ] text
		'blue' [ 'blue:' ] text
		'orange' [ 'orange:' ] text
		'green' [ 'green:' ] text
		'red' [ 'red:' ] text
		'purple' [ 'purple:' ] text
		'teal' [ 'teal:' ] text
)
```

```js
'use translations' stategroup (
	'yes'
		'default language' [ 'default' 'language:' ] reference
	'no'
		'engine language' [ 'engine' 'language:' ] stategroup (
			'english' [ 'english' ]
			'dutch' [ 'dutch' ]
		)
)
```
```
