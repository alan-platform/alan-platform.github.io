---
layout: doc
origin: connector
language: stdlib/calendar
version: 33
type: processor
---

1. TOC
{:toc}

```js
define 'type' as @API choice ( 'date' 'date-time' 'time' )
define 'weekday' as @API choice (
	'Monday':    1
	'Tuesday':   2
	'Wednesday': 3
	'Thursday':  4
	'Friday':    5
	'Saturday':  6
	'Sunday':    7
)
define 'calendar' as @API {
	'year': integer
	'day of year': integer
	'month': integer
	'day of month': integer
	'week': integer
	'day of week': 'weekday'
	'hour': integer
	'minute': integer
	'second': integer
}
library
	/* Converts Alan Time to broken down time.
	 * When information is not present in the source, it is set to zero.
	 */
	function 'convert'
		< integer , 'calendar' >
		(
			$'source type': 'type'
			$'timezone': optional text
		)
		binds: "builtin::calendar::convert"
```
