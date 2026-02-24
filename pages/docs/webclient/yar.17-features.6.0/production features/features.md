---
layout: "doc"
origin: "webclient"
language: "production features"
version: "yar.17-features.6.0"
type: "features"
---

1. TOC
{:toc}

```js
global-features
	'full screen planning' {
		'plannings': list non-empty feature 'planning'
	}
node-features
	'permissions' component stategroup @default: 'not set' @strategy (
		'user' binding user {
			'stategroup': binding stategroup {
				'state': binding state { }
			}
		}
		'node' binding node { }
		'not set' none
	)
	'planning' component {
		'label': text
		'permissions': feature 'permissions'
		'default zoom level': feature 'zoom level'
		'has more zoom levels': stategroup @default: 'no' (
			'yes' list non-empty feature 'zoom level'
			'no' { }
		)
		'type': stategroup @default: 'default' (
			'default' { }
			'specific start and end' feature 'start and end'
			'user start and end' binding user {
				'start': binding number { }
				'end': binding number { }
			}
		)
		'windows': list non-empty {
			'label': text
			'rows': feature 'planning rows'
			'bottom rows': feature 'optional custom rows'
		}
		'global commands': list binding command { }
		'holidays': feature 'optional planning holidays'
	}
	'planning rows' component binding nodes {
		'is reference set': feature 'is reference set'
		'items': feature 'planning items'
		'background items': feature 'optional background items'
		'children': feature 'optional rows'
		'filters': feature 'optional filters'
		'custom sorting': feature 'optional sorting'
		'custom query limit': feature 'optional simple query limit' // default: 1000
		'label': feature 'label'
		'right label': feature 'optional label with tooltip'
		'node filters': feature 'optional node filters'
		'tooltip': feature 'optional label'
		'start and end filter': feature 'optional start and end'
		'partitioning': feature 'optional partitioning'
		'filters dependent on children or items': feature 'filters dependent on children or items'
	}
	'sorting' component {
		'direction': stategroup (
			'ascending' { }
			'descending' { }
		)
		'type': stategroup (
			'number' binding number { }
			'text' binding text { }
		)
	}
	'optional sorting' component stategroup @default: 'not set' @strategy (
		'set' feature 'sorting'
		'not set' none
	)
	'partitioning' component stategroup (
		'static' stategroup (
			'text' binding text { }
			'stategroup' binding stategroup { }
		)
		'dynamic' list non-empty {
			'label': text
			'type': stategroup (
				'text' binding text { }
				'stategroup' binding stategroup { }
			)
		}
	)
	'optional partitioning' component stategroup @default: 'not set' @strategy (
		'set' feature 'partitioning'
		'not set' none
	)
	'optional rows' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning rows'
		'not set' none
	)
	'optional custom rows' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning custom rows'
		'not set' none
	)
	'planning custom rows' component list {
		'label': feature 'label'
		'tooltip': feature 'optional label'
		'items': feature 'planning items'
		'background items': feature 'optional background items'
	}
	'label' component list non-empty stategroup @strategy (
		'static text' text
		'dynamic text' binding text { }
		'dynamic number' binding number { }
	)
	'optional label' component stategroup @default: 'not set' @strategy (
		'set' feature 'label'
		'not set' none
	)
	'label with tooltip' component {
		'label': feature 'label'
		'tooltip': feature 'optional label'
	}
	'optional label with tooltip' component stategroup @default: 'not set' @strategy (
		'set' feature 'label with tooltip'
		'not set' none
	)
	'planning items' component binding nodes {
		'is reference set': feature 'is reference set'
		'start and end': feature 'start and end'
		'label': feature 'optional label'
		'filters': feature 'optional filters'
		'node filters': feature 'optional node filters'
		'tooltip': feature 'optional label'
		'custom sorting': feature 'optional sorting'
		'custom query limit': feature 'optional simple query limit' // default: 1000
	}
	'optional filters' component stategroup @default: 'not set' @strategy (
		'set' feature 'filters'
		'not set' none
	)
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
	'is reference set' component stategroup @default: 'no' @strategy (
		'yes' binding text reference { }
		'no' none
	)
	'start and end' component {
		'start': binding number { }
		'end': binding number { }
	}
	'optional start and end' component stategroup @default: 'not set' @strategy (
		'set' feature 'start and end'
		'not set' none
	)
	'zoom level' component unbound {
		'name': text
		'type': stategroup (
			'month' {
				'months before current month': number @default: 1
				'months after current month': number @default: 36
				'default width': number @default: 2500
				'go left button months': number @default: 4
				'go right button months': number @default: 4
			}
			'week' {
				'weeks before current week': number @default: 1
				'weeks after current week': number @default: 52
				'default width': number @default: 2500
				'go left button weeks': number @default: 4
				'go right button weeks': number @default: 4
			}
			'day' {
				'days before today': number @default: 7
				'days after today': number @default: 31
				'default width': number @default: 2000
				'go left button days': number @default: 30
				'go right button days': number @default: 30
				'show weekends': stategroup @default: 'yes' (
					'yes' { }
					'no' { }
				)
			}
			'hour' {
				'days before today': number @default: 7
				'days after today': number @default: 31
				'default width': number @default: 15000
				'go left button days': number @default: 7
				'go right button days': number @default: 7
				'show weekends': stategroup @default: 'yes' (
					'yes' { }
					'no' { }
				)
				'show nights': stategroup @default: 'yes' (
					'yes' { }
					'no' {
						'start of day': number @default: 6
						'end of day': number @default: 18
					}
				)
			}
		)
	}
	'optional planning holidays' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning holidays'
		'not set' none
	)
	'planning holidays' component binding nodes {
		'holiday': binding text { }
		'start and end': feature 'start and end'
		'highlight background': stategroup @default: 'yes' (
			'yes' { }
			'state dependent' binding stategroup {
				'state to highlight': binding state { }
			}
			'no' { }
		)
	}
	'planning background items' component binding nodes {
		'is reference set': feature 'is reference set'
		'start and end': feature 'start and end'
		'label': feature 'optional label'
		'filters': feature 'optional filters'
		'node filters': feature 'optional node filters'
		'tooltip': feature 'optional label'
		'custom query limit': feature 'optional simple query limit' // default: 1000
	}
	'filters dependent on children or items' component {
		'hide row when it has no items': stategroup @default: 'no' (
			'yes' { }
			'no' { }
		)
		'show option to filter by items': stategroup @default: 'no' (
			'yes' {
				'hide row when it has no items label': text @default: "Hide rows without items"
			}
			'no' { }
		)
		'hide row when it has no child rows': stategroup @default: 'no' (
			'yes' { }
			'no' { }
		)
		'show option to filter by children': stategroup @default: 'no' (
			'yes' {
				'hide row when it has no child rows label': text @default: "Hide rows without child rows"
			}
			'no' { }
		)
	}
	'optional background items' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning background items'
		'not set' none
	)
	'node filters' component list non-empty binding node { }
	'optional node filters' component stategroup @default: 'not set' @strategy (
		'set' feature 'node filters'
		'not set' none
	)
	'simple query limit' component number
	'optional simple query limit' component stategroup @default: 'not set' @strategy (
		'set' feature 'simple query limit'
		'not set' none
	)
collection-features
stategroup-features
number-features
text-features
file-features
command-features
action-features
```
