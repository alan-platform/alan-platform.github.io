---
layout: doc
origin: auto-webclient
language: settings
type: grammar
version: intrepid.5
---

Global settings for the user interface.

## root


### application creator

```js
	'application creator' ['application' 'creator:'] text
```

### application name

```js
	'application name' ['application' 'name:'] text
```

### application wallpaper url

```js
	'application wallpaper url' ['application' 'wallpaper' 'url:'] text
```

### allow anonymous user

```js
	'allow anonymous user' [ 'anonymous' 'login:' ] stategroup (
		'no' [ 'disabled' ]
		'yes' [ 'enabled' ]
	)
```

### enable csv actions

```js
	'enable csv actions' [ 'csv' 'actions:' ] stategroup (
		'no' [ 'disabled' ]
		'yes' [ 'enabled' ]
	)
```

### report limit

```js
	'report limit' [ 'report' 'limit:' ] number
```

### system administrator role

```js
	'system administrator role' [ 'system' 'administrator' 'role:' ] reference
```

### power user role

```js
	'power user role' [ 'power' 'user' 'role:' ] reference
```

### announcement title

```js
	'announcement title' [ 'announcement:' ] text
```

### announcements

```js
	'announcements' [ '[' , ']' ] collection indent ( )
```

### custom color theme

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

## component rules

