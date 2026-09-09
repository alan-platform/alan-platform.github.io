---
layout: "doc"
origin: "webclient"
language: "handheld features"
version: "zora.2.0"
type: "features"
---

1. TOC
{:toc}

```js
global-features
node-features
	'text label' unbound text
	'string' component list non-empty stategroup @strategy (
		// 'icon' {
		// 	'name': text
		// }
		'static text' text
		'stategroup' binding stategroup { }
		'number' binding number { }
		'text' binding text { }
		'node' {
			'italic': stategroup @default: 'no' (
				'yes' { }
				'no' { }
			)
			'bold': stategroup @default: 'no' (
				'yes' { }
				'no' { }
			)
			'subtle': stategroup @default: 'no' (
				'yes' { }
				'no' { }
			)
			'underline': stategroup @default: 'no' (
				'yes' { }
				'no' { }
			)
			'font size': stategroup @default: 'normal' (
				'normal' { }
				'small' { }
				'large' { }
			)
			'value': feature 'string'
		}
	// 'file' binding file { }
	// 'command' binding command { }
	// 'action' binding action { }
	)
	'item list' {
		'collection': binding nodes {
			'layout': stategroup (
				'item list' {
					'properties': list non-empty feature 'string'
					'properties aside': list feature 'string'
				}
				'cards' {
					'sections': list non-empty feature 'string'
				}
			)
			'filters': feature 'optional filters'
			'sorting': feature 'optional sorting'
			'open view': stategroup @default: 'none' @strategy (
				'view' view
				'none' none
			)
		}
	}
	'optional sorting' component stategroup @default: 'not set' @strategy (
		'set' feature 'sorting'
		'not set' none
	)
	// Common feature
	'sorting' component {
		'direction': stategroup (
			'ascending' { }
			'descending' { }
		)
		'type': stategroup (
			'number' binding number { }
			'text' binding text { }
			'stategroup' binding stategroup { }
		)
	}
	'optional filters' component stategroup @default: 'not set' @strategy (
		'set' feature 'filters'
		'not set' none
	)
	// Common features
	'query property key' component stategroup @default: 'auto' @strategy (
		'auto' { }
		'set' text
	)
```
A number filter is added as a filter on the query column. Use 'simple' to let the
user choose the operator and the value, or 'yes' to set a fixed criteria that the
user cannot change.
```js
	'number filter' component stategroup @default: 'simple' (
```
A fixed criteria: an operator plus the value to compare against. That value is
either a 'static' number, or 'now' (the current time) with an optional
'offset'. The offset is in the unit of the bound number property and can be
negative to select a moment in the past.
```js
		'yes' {
			'operator': stategroup (
				'smaller' { }
				'smaller equal' { }
				'greater' { }
				'greater equal' { }
				'equal' { }
			)
			'criteria': stategroup (
				'now' stategroup @strategy (
					'no offset' { }
					'offset' number
				)
				'static' number
			)
		}
```
The user chooses the operator and the value.
```js
		'simple' { }
	)
```
A text filter is added as a filter on the query column. The default 'auto' lets the
generator pick the most suitable filter for the property.
```js
	'text filter' component stategroup @default: 'auto' (
```
Let the generator pick the filter: a list of the referenced entries to select
from when the text is a reference, a text search otherwise.
```js
		'auto' { }
```
A fixed search pattern that the user cannot change.
```js
		'yes' {
			'criteria': text
		}
```
A text search that the user fills in.
```js
		'simple' { }
```
A list of the referenced entries, to either include ('in') or exclude
('not in'). Only for texts that are references; other texts get no filter.
```js
		'containment' {
			'operator': stategroup (
				'in' { }
				'not in' { }
			)
		}
	)
	'filters' component list non-empty stategroup @strategy (
		'stategroup' binding stategroup {
			'label': stategroup @default: 'auto' @strategy (
				'auto' { }
				'set' text
			)
			'filter': stategroup @default: 'simple' (
				'yes' {
					'states to include': list binding state { }
				}
				'simple' { }
			)
			'show': stategroup @default: 'yes' (
				'yes' { }
				'no' { }
			)
		}
		'number' binding number {
			'label': feature 'query property key'
			'filter': feature 'number filter'
			'show': stategroup @default: 'yes' (
				'yes' { }
				'no' { }
			)
		}
		'text' binding text {
			'label': feature 'query property key'
			'filter': feature 'text filter'
			'show': stategroup @default: 'yes' (
				'yes' { }
				'no' { }
			)
		}
	)
	'open view' {
		'view': view
	}
collection-features
	'table layout' none
stategroup-features
	'switch' {
		'on': binding state { }
		'off': binding state { }
	}
number-features
text-features
```
Indicates that this text can be on a bar or qr code.
```js
	'barcode' none
file-features
reference-set-features
command-features
action-features
```
