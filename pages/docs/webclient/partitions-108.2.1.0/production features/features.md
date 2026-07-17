---
layout: "doc"
origin: "webclient"
language: "production features"
version: "partitions-108.2.1.0"
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
	'label' component list non-empty stategroup @strategy (
		'static text' text
		'dynamic text' binding text { }
		'dynamic number' binding number { }
	)
	'optional label' component stategroup @default: 'not set' @strategy (
		'set' feature 'label'
		'not set' none
	)
	'labels' component list non-empty {
		'label': feature 'label'
	}
	'optional labels' component stategroup @default: 'not set' @strategy (
		'set' feature 'labels'
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
	// Planning features
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
	'optional planning holidays' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning holidays'
		'not set' none
	)
	'global property' component stategroup @strategy (
		'number' binding number { }
		'text' binding text { }
		'command' binding command { }
		'label' feature 'label'
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
			'rows': feature 'rows list'
			'bottom rows': feature 'optional custom rows'
		}
		'global properties': list feature 'global property'
		'holidays': feature 'optional planning holidays'
	}
	'planning rows' component binding nodes {
		'is reference set': feature 'is reference set'
		'items': feature 'planning items'
		'background items': feature 'optional background items'
		'children': feature 'optional rows list'
		'filters': feature 'optional filters'
		'custom sorting': feature 'optional sorting'
		'custom query limit': feature 'optional simple query limit' // default: 1000
		'label': feature 'label'
		'right label': feature 'optional label with tooltip'
		'node filters': feature 'optional node filters'
		'color': feature 'planning color'
		'background color': feature 'planning color'
		'tooltip': feature 'optional label'
		'start and end filter': feature 'optional start and end'
		'popup': feature 'optional popup'
		'entry creation command': feature 'optional entry creation'
		'partitioning': feature 'optional partitioning'
		'filters dependent on children or items': feature 'filters dependent on children or items'
		'icon bar': feature 'optional icon bar'
	}
	'optional rows' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning rows'
		'not set' none
	)
	'rows list' component stategroup @strategy (
		'multiple' list non-empty feature 'planning rows'
		'singular' feature 'planning rows'
	)
	'optional rows list' component stategroup @default: 'not set' @strategy (
		'multiple' list non-empty feature 'planning rows'
		'singular' feature 'planning rows'
		'not set' none
	)
	'planning items' component binding nodes {
		'is reference set': feature 'is reference set'
		'start and end': feature 'start and end'
		'label': feature 'optional label'
		'more labels': feature 'optional labels'
		'filters': feature 'optional filters'
		'node filters': feature 'optional node filters'
		'color': feature 'planning color'
		'tooltip': feature 'optional label'
		'context menu': feature 'optional context menu'
		'custom sorting': feature 'optional sorting'
		'custom query limit': feature 'optional simple query limit' // default: 1000
		'draggable': feature 'optional draggable'
		'popup': feature 'optional popup'
		'icon bar': feature 'optional icon bar'
	}
	'planning background items' component binding nodes {
		'is reference set': feature 'is reference set'
		'start and end': feature 'start and end'
		'label': feature 'optional label'
		'filters': feature 'optional filters'
		'node filters': feature 'optional node filters'
		'color': feature 'planning color'
		'tooltip': feature 'optional label'
		'context menu': feature 'optional context menu'
		'custom query limit': feature 'optional simple query limit' // default: 1000
	}
	'optional background items' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning background items'
		'not set' none
	)
	'planning custom rows' component list {
		'label': feature 'label'
		'tooltip': feature 'optional label'
		'items': feature 'planning items'
		'background items': feature 'optional background items'
	}
	'optional custom rows' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning custom rows'
		'not set' none
	)
	'start and end' component {
		'start': binding number { }
		'end': binding number { }
	}
	'optional start and end' component stategroup @default: 'not set' @strategy (
		'set' feature 'start and end'
		'not set' none
	)
	'optional entry creation' component stategroup @default: 'not set' @strategy (
		'set' {
			'create': feature 'create command'
			'alternative create command': feature 'optional create command'
			'draggable': stategroup (
				'yes' { }
				'no' { }
			)
		}
		'not set' none
	)
	'create command' component binding command {
		'start': binding number { }
		'end': binding number { }
		'snap': feature 'snap'
	}
	'optional create command' component stategroup @default: 'not set' @strategy (
		'set' feature 'create command'
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
	'node filters' component list non-empty binding node { }
	'optional node filters' component stategroup @default: 'not set' @strategy (
		'set' feature 'node filters'
		'not set' none
	)
	'planning color' component stategroup @default: 'auto' @strategy (
		'auto' none
		'property' binding text { }
		'custom' text
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
	'optional filters' component stategroup @default: 'not set' @strategy (
		'set' feature 'filters'
		'not set' none
	)
	'filters dependent on children or items' component { // todo: universeel maken met een query die leeg kan zijn
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
		'hide row when it has no background items': stategroup @default: 'no' (
			'yes' { }
			'no' { }
		)
		'show option to filter by background items': stategroup @default: 'no' (
			'yes' {
				'hide row when it has no background items label': text @default: "Hide rows without background items"
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
	'snap' component unbound stategroup (
		'none' { }
		'minute' number
		'day' { }
		'week' { }
		'month' { }
		'year' { }
	)
	'popup' component {
		'label': feature 'label'
		'node': feature 'node'
		'has open view button': stategroup (
			'yes' {
				'label': text
			}
			'no' { }
		)
	}
	'optional popup' component stategroup @default: 'not set' @strategy (
		'set' feature 'popup'
		'not set' none
	)
	'context menu' component list non-empty {
		'icon': stategroup @default: 'not set' @strategy (
			'set' text
			'not set' none
		)
		'command': binding command { }
	}
	'optional context menu' component stategroup @default: 'not set' @strategy (
		'set' feature 'context menu'
		'not set' none
	)
	'is reference set' component stategroup @default: 'no' @strategy (
		'yes' binding text reference { }
		'no' none
	)
	'icon bar' component list non-empty binding states {
		'tooltip': stategroup @default: 'not set' @strategy (
			'set' feature 'label'
			'not set' none
		)
	}
	'optional icon bar' component stategroup @default: 'not set' @strategy (
		'set' feature 'icon bar'
		'not set' none
	)
	'move command' component binding command {
		'start': binding number { }
		'can switch row': stategroup @default: 'no' (
			'yes' binding text reference { }
			'no' { }
		)
		'snap': feature 'snap'
	}
	'optional move command' component stategroup @default: 'not set' @strategy (
		'set' feature 'move command'
		'not set' none
	)
	'draggable' component {
		'move': feature 'move command'
		'alternative move command': feature 'optional move command'
	}
	'optional draggable' component stategroup @default: 'not set' @strategy (
		'set' feature 'draggable'
		'not set' none
	)
	'node' component list non-empty stategroup (
		'number' binding number { }
		'text' binding text { }
		'stategroup' binding states {
			'node': feature 'optional node'
		}
		'file' binding file { }
		'command' binding command { }
		'query' { }
		'chart' { }
	)
	'optional node' component stategroup @default: 'not set' @strategy (
		'set' feature 'node'
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
	'optional sorting' component stategroup @default: 'not set' @strategy (
		'set' feature 'sorting'
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
reference-set-features
command-features
action-features
```
