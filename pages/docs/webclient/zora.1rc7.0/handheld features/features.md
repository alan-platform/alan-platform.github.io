---
layout: "doc"
origin: "webclient"
language: "handheld features"
version: "zora.1rc7.0"
type: "features"
---

1. TOC
{:toc}

```js
global-features
node-features
	'text label' unbound text
	'string' list non-empty stategroup @strategy (
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
	// Common feature
	'filters' component list non-empty {
		'label': text
		'property': stategroup @strategy (
			'stategroup' binding stategroup {
				'filter': stategroup @default: 'simple' (
					'yes' {
						'states to include': list binding state { }
					}
					'simple' { }
				)
			}
			'number' binding number {
				'filter': stategroup @default: 'simple' (
					'yes' {
						'operator': stategroup (
							'smaller' { }
							'smaller equal' { }
							'greater' { }
							'greater equal' { }
							'equal' { }
						)
						'criteria': stategroup (
							'now' {
								'offset': number
							}
							'static' {
								'value': number
							}
						)
					}
					'simple' { }
				)
			}
			'text' binding text {
				'filter': stategroup @default: 'simple' (
					'yes' {
						'criteria': text
					}
					'simple' { }
					'containment' {
						'operator': stategroup (
							'in' { }
							'not in' { }
						)
					}
				)
			}
		)
		'show': stategroup @default: 'yes' (
			'yes' { }
			'no' { }
		)
	}
	'open view' {
		'view': view
	}
collection-features
stategroup-features
number-features
text-features
```
Indicates that this text can be on a bar or qr code.
```js
	'barcode' none
file-features
command-features
action-features
```
