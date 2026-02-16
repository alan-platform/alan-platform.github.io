---
layout: "doc"
origin: "auto-webclient"
language: "generator_annotations"
version: "zora.rc5"
type: "grammar"
---

1. TOC
{:toc}

# Generator Contracts
## Default
The default generator.

```js
global-features
	'full screen planning' {
		'plannings': list non-empty feature 'planning'
	}

	'dashboard' {
		'dashboard': feature 'dashboard 2'
	}

	'layout' {
		'density': stategroup @default: 'compact' (
			'compact' { }
			'comfortable' { }
		)
		'group table columns': stategroup @default: 'no' (
			'no' { }
			'yes' { }
		)
		'show menu': stategroup @default: 'full' (
			'sparse' { }
			'full' { }
		)
		'custom colors': stategroup @default: 'no' (
			'no' { }
			'yes' {
				'primary color': text
				'secondary color': text
				'tertiary color': text
				'error color': text
				'neutral color': text
				'neutral variant color': text
			}
		)
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

	'dimension' component unbound stategroup @default: 'default' @strategy (
		'custom' {
			'width': number
			'height': number
		}
		'default' none
	)

	'margin' component unbound stategroup @default: 'default' @strategy (
		'custom' {
			'top': number
			'right': number
			'bottom': number
			'left': number
		}
		'default' none
	)

	'color' component unbound stategroup @default: 'auto' (
		'auto' { }
		'blue' { }
		'orange' { }
		'green' { }
		'red' { }
		'black' { }
		'grey' { }
		'grey light' { }
		'grey dark' { }
		'teal' { }
		'purple' { }
		'hex' text
	)

	'range' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'range start': stategroup (
			'static' number
			'dynamic' binding number { }
		)
		'ranges': list {
			'type': stategroup (
				'green' { }
				'blue' { }
				'orange' { }
				'red' { }
			)
			'range size': stategroup (
				'static' number
				'dynamic' binding number { }
			)
		}
		'value': binding number { }
		'style': stategroup (
			'progress bar' { }
			'gauge' { }
		)
	}

	'pie chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': binding nodes {
			'label': binding text { }
			'property': binding number { }
			'merge small slices': stategroup (
				'below percentage' number
				'no' { }
			)
			'sorting': stategroup (
				'yes' stategroup (
					'ascending' { }
					'descending' { }
				)
				'no' { }
			)
		}
	}

	'bar chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': binding nodes {
			'label': binding text { }
			'style': stategroup (
				'grouped' list {
					'property': binding number { }
					'color': feature 'color'
				}
				'stacked' list {
					'property': binding number { }
					'color': feature 'color'
				}
				'bar' binding number { }
			)
			'sorting': stategroup (
				'yes' {
					'direction': stategroup (
						'ascending' { }
						'descending' { }
					)
					'axis': stategroup (
						'single' binding number { }
						'sum' { }
					)
				}
				'no' { }
			)
		}
	}

	'line chart query' component {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'label': binding text { }
		'lines': list {
			'property': binding number { }
			'color': feature 'color'
		}
		'style': stategroup (
			'line' { }
			'area' { }
		)
		'sort': binding number {
			'direction': stategroup (
				'ascending' { }
				'descending' { }
			)
		}
	}

	'chart value' component {
		'type': stategroup (
			'text' binding text { }
			'number' binding number { }
		// TODO 'state group' {
		// 	'property': query stategroup binding { }
		// }
		)
	}

	'custom table properties' component list binding { }

	'2d chart query' component {
		'title': text
		'x': feature 'chart value'
		'x label': stategroup @default: 'auto' (
			'auto' { }
			'text' binding text { }
		)
		'x axis title': stategroup @default: 'none' (
			'none' { }
			'set' text
		)
		'y axis title': stategroup @default: 'none' (
			'none' { }
			'set' text
		)
		'format x': stategroup @default: 'auto' (
			'auto' { }
			'day' { }
			'month' { }
			'month and year' { }
			'week' { }
			'week and year' { }
			'custom' list non-empty stategroup (
				'abbreviated weekday name' { }
				'full weekday name' { }
				'abbreviated month name' { }
				'full month name' { }
				'the locale’s date and time' { }
				'zero-padded day of the month' { }
				'space-padded day of the month' { }
				'microseconds' { }
				'ISO 8601 week-based year without century' { }
				'ISO 8601 week-based year with century' { }
				'hour (24-hour clock)' { }
				'hour (12-hour clock)' { }
				'day of the year' { }
				'month' { }
				'minute' { }
				'milliseconds' { }
				'either AM or PM' { }
				'quarter of the year' { }
				'milliseconds since UNIX epoch' { }
				'seconds since UNIX epoch' { }
				'second' { }
				'Monday-based (ISO 8601) weekday' { }
				'Sunday-based week of the year' { }
				'ISO 8601 week of the year' { }
				'Sunday-based weekday' { }
				'Monday-based week of the year' { }
				'the locale’s date' { }
				'the locale’s time' { }
				'year without century' { }
				'year with century' { }
				'time zone offset' { }
				'percent sign' { }
				'text' text
			)
		)
		'group x value': stategroup @default: 'no' (
			'no' { }
			'yes' stategroup @default: 'none' (
				'none' { }
				'week' { }
				'month' { }
				'quarter' { }
				'year' { }
			)
		)
		'size': stategroup @default: 'small' (
			'small' { }
			'medium' { }
			'large' { }
		)
		'bar mode': stategroup @default: 'grouped' (
			'grouped' { }
			'stacked' { }
		)
		'lines': list {
			'name': text @default: ""
			'y': binding number { }
			/// setting `y aggregate` switches the default `sum` function to handle multiple y
			/// values on the same x value.
			'y aggregate': stategroup @default: 'sum' (
				'sum' { }
				'minimum' { }
				'maximum' { }
				'average' { }
			)
			'color': stategroup @default: 'auto' (
				'auto' { }
				'custom' text
			)
			'style': stategroup @default: 'line' (
				'line' {
					'stack': stategroup @default: 'no' (
						'no' { }
						'yes' { }
					)
					'shape': stategroup @default: 'linear' (
						'linear' { }
						'horizontal vertical' { }
						'vertical horizontal' { }
						'horizontal vertical horizontal' { }
						'vertical horizontal vertical' { }
						'spline' { }
					)
					'dash': stategroup @default: 'solid' (
						'solid' { }
						'dot' { }
						'dash dot' { }
						'long dash dot' { }
					)
				}
				'area' { }
				'bar' { }
			)
			'partition': stategroup @default: 'no' (
				'no' { }
				'yes' {
					'value': binding text { }
					'color': stategroup @default: 'auto' (
						'auto' { }
						'custom' binding text { }
					)
				}
			)
			'show legend': stategroup @default: 'yes' (
				'yes' { }
				'no' { }
			)
		}
		'drill down properties': stategroup @default: 'auto' (
			'auto' { }
			'custom' feature 'custom table properties'
		)
	}

	'line chart' binding nodes {
		'chart': feature 'line chart query'
	}

	'scatter chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': binding nodes {
			'label': binding text { }
			'x label': text
			'x property': binding number { }
			'y label': text
			'y property': binding number { }
			'style': stategroup (
				'dot' { }
				'connected dot' binding number {
					'sort': stategroup (
						'ascending' { }
						'descending' { }
					)
				}
				'bubble' binding number { }
			)
		}
	}

	'radar chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': binding nodes {
			'label': binding text { }
			'values': list binding number { }
			'style': stategroup (
				'spider' { }
				'radar' { }
			)
		}
	}

	'dashboard' {
		'cell width': number
		'cell height': number
		'grid gap': stategroup @default: 'yes' (
			'yes' number @default: 20
			'no' { }
		)
		'widgets': list {
			'x': number
			'width': number
			'y': number
			'height': number
			'widget': stategroup (
				'number' {
					'value': binding number { }
					'number size': stategroup (
						'large' { }
						'fixed' number
					)
					'unit size': stategroup @default: 'auto' (
						'auto' { }
						'fixed' number
					)
				}
				'range' feature 'range'
				'pie chart' feature 'pie chart'
				'bar chart' feature 'bar chart'
				'line chart' feature 'line chart'
				'scatter chart' feature 'scatter chart'
				'radar chart' feature 'radar chart'
				'legend' stategroup (
					'static' list {
						'label': text
						'color': feature 'color'
					}
					'dynamic' binding nodes {
						'label': binding text { }
					}
				)
			)
		}
	}

	'dashboard 2' {
		'permissions': feature 'permissions'
		'widgets': list stategroup (
			'grouped charts' feature 'grouped charts'
			'tabs' list {
				'name': text
				'widget': feature 'dashboard 2'
			}
		)
	}

	'grouped charts' component binding nodes {
		'include filters': stategroup @default: 'yes' (
			'yes' { }
			'no' { }
		)
		'filters': feature 'optional filters'
		'custom limit': feature 'optional query limit'
		'custom sorting': feature 'optional sorting'
		'charts': list stategroup (
			'2d chart' feature '2d chart query'
			'filter' stategroup @strategy (
				'text' binding text { }
				'number' binding number { }
				'stategroup' binding stategroup { }
			)
			'table' {
				'title': text
				'size': stategroup @default: 'small' (
					'small' { }
					'medium' { }
					'large' { }
				)
				'properties': feature 'custom table properties'
			}
		)
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

	'planning items' component binding nodes {
		'is reference set': feature 'is reference set'
		'start and end': feature 'start and end'
		'label': feature 'optional label'
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

	'properties' component list {
		'label': text
		'property': stategroup @strategy (
			'stategroup' binding stategroup {
				'filter': stategroup (
					'yes' {
						'states to include': list binding state { }
					}
					'simple' { }
					'no' { }
				)
			}
			'number' binding number {
				'filter': stategroup (
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
					'no' { }
				)
			}
			'text' binding text {
				'filter': stategroup (
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
					'no' { }
				)
			}
			'file' binding file { }
			'command' binding command { }
			'action' binding action { }
		)
	}

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
		'query' {
			'label': feature 'label'
			'query': feature 'query'
		}
		'chart' {
			'label': feature 'label'
			'type': stategroup (
				'range' feature 'range'
				'pie chart' feature 'pie chart'
				'bar chart' feature 'bar chart'
				'line chart' feature 'line chart'
				'scatter chart' feature 'scatter chart'
				'radar chart' feature 'radar chart'
			)
		}
	)

	'optional node' component stategroup @default: 'not set' @strategy (
		'set' feature 'node'
		'not set' none
	)

	'query' component binding nodes {
		'custom sorting': feature 'optional sorting'
		'custom limit': feature 'optional query limit'
		'filters': feature 'optional filters'
		'properties': feature 'properties'
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

	'query limit' component {
		'sample': stategroup @default: 'no' (
			'yes' {
				'sample size': number
				'sample limit': number
			}
			'no' { }
		)
		'absolute limit': number
	}

	'optional query limit' component stategroup @default: 'not set' @strategy (
		'set' feature 'query limit'
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
	'include in grid' none

action-features
	'include in grid' none
```
## Handheld
The handheld generator.

```js
global-features

node-features

collection-features

stategroup-features

number-features

text-features

file-features

command-features

action-features
```
## Production
The production generator.

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
		)
		'windows': list non-empty {
			'label': text
			'rows': feature 'planning rows'
			'bottom rows': feature 'optional custom rows'
		}
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
# Annotations
## Sparse Annotation Tree
The root node of the annotations.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
</pre>
</div>
</div>
## Global Features
Configure global features provided by the selected generator.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has global features</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">global-features:</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
		'<span class="token string">configured features</span>': dictionary { [ <span class="token operator">feature</span> ]
			'<span class="token string">has more features</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next feature</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">feature</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--feature">'feature'</a>
		}
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>
## Handheld Menu

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld menu</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">handheld-menu</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
		'<span class="token string">items</span>': dictionary {
			'<span class="token string">icon</span>': [ <span class="token operator">icon:</span> ] text
			'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
			'<span class="token string">has more items</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next item</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
		}
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>
### Navigation expressions

{: #grammar-rule--singular-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
	'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">*</span> ] reference
	'<span class="token string">has more steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">property</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">group</span>' { }
						'<span class="token string">state</span>' {
							'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
						}
						'<span class="token string">rule</span>' {
							'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
						}
					)
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path">'node path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
### Annotation Node

{: #grammar-rule--extended-annotations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">extended annotations</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">command features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">action features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">reference set</span>' { [ <span class="token operator">reference-set</span> ]
				'<span class="token string">has custom queries</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">queries</span>': component <a href="#grammar-rule--custom-queries">'custom queries'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">entries are custom properties</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@properties</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">value</span>' {
								'<span class="token string">value attribute</span>': [ <span class="token operator">value:</span> ] reference
							}
							'<span class="token string">node</span>' { [ <span class="token operator">node</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">show as list</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@list:</span> ]
						'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">has custom queries</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">queries</span>': component <a href="#grammar-rule--custom-queries">'custom queries'</a>
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">collection features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">stategroup features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
				}
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">number features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">text features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">has features</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@features:</span> ]
						'<span class="token string">file features</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--features-matrix">'features matrix'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
		)
	}
	'<span class="token string">has features</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">features:</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">feature library</span>': dictionary { [ <span class="token operator">component</span> ]
				'<span class="token string">contract</span>': [ <span class="token operator">:</span> <span class="token operator">feature</span> ] reference
				'<span class="token string">feature</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--feature">'feature'</a>
			}
			'<span class="token string">node features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">has handheld frames</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">handheld frames</span>': dictionary { [ <span class="token operator">handheld:</span> ]
				'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-view-frame">'handheld view frame'</a>
			}
			'<span class="token string">main frame</span>': reference = first
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--custom-queries }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom queries</span>' {
	'<span class="token string">default custom query</span>': stategroup (
		'<span class="token string">none</span>' { }
		'<span class="token string">select</span>' {
			'<span class="token string">query</span>': [ <span class="token operator">default:</span> ] reference
		}
	)
	'<span class="token string">custom queries</span>': dictionary { [ <span class="token operator">query</span> ]
		'<span class="token string">has more queries</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next query</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--features-matrix }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">features matrix</span>' {
	'<span class="token string">configured features</span>': dictionary { [ <span class="token operator">feature</span> ]
		'<span class="token string">has more features</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next feature</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">feature</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--feature">'feature'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--feature }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">model binding</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
				'<span class="token string">node</span>' { [ <span class="token operator">on</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
				}
				'<span class="token string">nodes</span>' {
					'<span class="token string">context</span>': component <a href="#grammar-rule--node-path">'node path'</a>
					'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--collection-path">'collection path'</a>
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' { [ <span class="token operator">state</span> ]
					'<span class="token string">state</span>': reference
				}
			)
			'<span class="token string">feature</span>': component <a href="#grammar-rule--feature-node">'feature node'</a>
		}
		'<span class="token string">states binding</span>' { [ <span class="token operator">stategroup</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">feature</span>': component <a href="#grammar-rule--feature-node">'feature node'</a>
			}
		}
		'<span class="token string">node</span>' {
			'<span class="token string">feature</span>': component <a href="#grammar-rule--feature-node">'feature node'</a>
		}
		'<span class="token string">list</span>' {
			'<span class="token string">has entries</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">list</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--feature-list">'feature list'</a>
				}
				'<span class="token string">no</span>' { [ <span class="token operator">empty</span> ] }
			)
		}
		'<span class="token string">stategroup</span>' {
			'<span class="token string">state</span>': reference
			'<span class="token string">feature</span>': component <a href="#grammar-rule--feature-reference">'feature reference'</a>
		}
		'<span class="token string">number</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">text</span>' {
			'<span class="token string">value</span>': text
		}
		'<span class="token string">none</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--feature-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature list</span>' {
	'<span class="token string">entry</span>': component <a href="#grammar-rule--feature-reference">'feature reference'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--feature-list">'feature list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--feature-reference }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature reference</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">reference</span>' {
			'<span class="token string">feature</span>': [ <span class="token operator">!</span> ] reference
		}
		'<span class="token string">inline</span>' {
			'<span class="token string">feature</span>': component <a href="#grammar-rule--feature">'feature'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--feature-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature node</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">feature</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--feature-reference">'feature reference'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--custom-query }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom query</span>' {
	'<span class="token string">custom limit</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">limit:</span> ]
			'<span class="token string">sample</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">sample size</span>': integer
					'<span class="token string">sample limit</span>': [ <span class="token operator">/</span>, <span class="token operator">/</span> ] integer
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">absolute limit</span>': integer
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">properties</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] dictionary {
		'<span class="token string">has more properties</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next property</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">context path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--node-path">'node path'</a>
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">property</span>': reference
				'<span class="token string">filter</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
						'<span class="token string">states</span>': [ <span class="token operator">?</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">is selected</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">selected</span> ] }
								'<span class="token string">no</span>' { }
							)
						}
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> <span class="token operator">simple</span> ] }
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">property</span>': reference
				'<span class="token string">filter</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
						'<span class="token string">operator</span>': stategroup (
							'<span class="token string">smaller</span>' { [ <span class="token operator"><</span> ] }
							'<span class="token string">smaller equal</span>' { [ <span class="token operator"><=</span> ] }
							'<span class="token string">greater</span>' { [ <span class="token operator">></span> ] }
							'<span class="token string">greater equal</span>' { [ <span class="token operator">>=</span> ] }
							'<span class="token string">equal</span>' { [ <span class="token operator">==</span> ] }
						)
						'<span class="token string">criteria</span>': stategroup (
							'<span class="token string">now</span>' { [ <span class="token operator">now</span> ]
								'<span class="token string">offset</span>': [ <span class="token operator">+</span> ] integer
							}
							'<span class="token string">static</span>' {
								'<span class="token string">value</span>': integer
							}
						)
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> <span class="token operator">simple</span> ] }
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">property</span>': reference
				'<span class="token string">filter</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
						'<span class="token string">criteria</span>': text
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> <span class="token operator">simple</span> ] }
					'<span class="token string">containment</span>' { [ <span class="token operator">filter</span>, <span class="token operator">selection</span> ]
						'<span class="token string">operator</span>': stategroup (
							'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
							'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">property</span>': reference
			}
			'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
				'<span class="token string">attribute</span>': reference
			}
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">attribute</span>': reference
			}
		)
	}
	'<span class="token string">custom sorting</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">direction</span>': stategroup (
				'<span class="token string">ascending</span>' { [ <span class="token operator">@ascending:</span> ] }
				'<span class="token string">descending</span>' { [ <span class="token operator">@descending:</span> ] }
			)
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">number</span>' {
					'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
				}
				'<span class="token string">text</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
				}
			)
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
### Handheld

{: #grammar-rule--annotated-collection-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">annotated collection selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' { }
				'<span class="token string">collection</span>' { [ <span class="token operator">[]</span> ] }
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--annotated-collection-selector">'annotated collection selector'</a>
		}
		'<span class="token string">no</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-frame-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld frame selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">inline</span>' {
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-view-frame">'handheld view frame'</a>
		}
		'<span class="token string">annotated</span>' {
			'<span class="token string">frame</span>': reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-details }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view details</span>' {
	'<span class="token string">title</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">title:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">fields</span>': dictionary {
		'<span class="token string">has more fields</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next field</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">emphasis</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">@emphasis</span> ] }
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-elements }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view elements</span>' {
	'<span class="token string">has element</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">-></span> ] stategroup (
				'<span class="token string">label</span>' { [ <span class="token operator">label:</span> ]
					'<span class="token string">text</span>': reference
				}
				'<span class="token string">inline view</span>' { [ <span class="token operator">inline</span> <span class="token operator">view:</span> ]
					'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
				}
				'<span class="token string">view</span>' {
					'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-elements">'handheld view elements'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-frame }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view frame</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">decision</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">options</span>': dictionary {
				'<span class="token string">has more options</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next option</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">emphasis</span>': [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">low</span>' { }
					'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
					'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
				)
				'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
			}
		}
		'<span class="token string">collection navigation</span>' { [ <span class="token operator">collection</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">collection context</span>': [ <span class="token operator">path:</span> ] stategroup (
				'<span class="token string">this</span>' { }
				'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
			)
			'<span class="token string">path</span>': component <a href="#grammar-rule--annotated-collection-selector">'annotated collection selector'</a>
			'<span class="token string">annotations</span>': group {
				'<span class="token string">header</span>': stategroup (
					'<span class="token string">yes</span>' { }
					'<span class="token string">no</span>' { [ <span class="token operator">@no-header</span> ] }
				)
				'<span class="token string">layout</span>': stategroup (
					'<span class="token string">set</span>' { [ <span class="token operator">@layout:</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">tabular</span>' { [ <span class="token operator">tabular</span> ] }
							'<span class="token string">cards</span>' { [ <span class="token operator">cards</span> ] }
							'<span class="token string">buttons</span>' { [ <span class="token operator">buttons</span> ] }
							'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
								'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--node-path">'node path'</a>
								'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">simple</span>' { }
									'<span class="token string">year</span>' { [ <span class="token operator">by</span>, <span class="token operator">year</span> ] }
									'<span class="token string">month</span>' { [ <span class="token operator">by</span>, <span class="token operator">month</span> ] }
									'<span class="token string">week</span>' { [ <span class="token operator">by</span>, <span class="token operator">week</span> ] }
									'<span class="token string">day</span>' { [ <span class="token operator">by</span>, <span class="token operator">day</span> ] }
									'<span class="token string">hour</span>' { [ <span class="token operator">by</span>, <span class="token operator">hour</span> ] }
								)
							}
						)
					}
					'<span class="token string">default</span>' { }
				)
			}
			'<span class="token string">details</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
				}
				'<span class="token string">no</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
				}
			)
			'<span class="token string">filters</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">filters:</span> ]
					'<span class="token string">fields</span>': dictionary {
						'<span class="token string">has more fields</span>': stategroup = node-switch successor (
							| node = '<span class="token string">yes</span>' { '<span class="token string">next field</span>' = successor }
							| none = '<span class="token string">no</span>'
						)
						'<span class="token string">path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--node-path">'node path'</a>
						'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">stategroup</span>' {
								'<span class="token string">filter</span>': stategroup (
									'<span class="token string">state</span>' {
										'<span class="token string">state</span>': [ <span class="token operator">is</span> ] reference
									}
									'<span class="token string">not state</span>' {
										'<span class="token string">state</span>': [ <span class="token operator">is</span> <span class="token operator">not</span> ] reference
									}
									'<span class="token string">states</span>' {
										'<span class="token string">states</span>': [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
									}
									'<span class="token string">simple</span>' { [ <span class="token operator">stategroup</span> ] }
								)
							}
							'<span class="token string">number</span>' {
								'<span class="token string">filter</span>': stategroup (
									'<span class="token string">match</span>' {
										'<span class="token string">operator</span>': stategroup (
											'<span class="token string">smaller</span>' { [ <span class="token operator">smaller</span> ] }
											'<span class="token string">smaller equal</span>' { [ <span class="token operator">smaller</span> <span class="token operator">or</span> <span class="token operator">equal</span> ] }
											'<span class="token string">greater</span>' { [ <span class="token operator">greater</span> ] }
											'<span class="token string">greater equal</span>' { [ <span class="token operator">greater</span> <span class="token operator">or</span> <span class="token operator">equal</span> ] }
											'<span class="token string">equal</span>' { [ <span class="token operator">equal</span> ] }
										)
										'<span class="token string">type</span>': [ <span class="token operator">than</span> ] stategroup (
											'<span class="token string">now</span>' { [ <span class="token operator">now</span> <span class="token operator">+</span> ] }
											'<span class="token string">static</span>' { }
										)
										'<span class="token string">offset</span>': integer
									}
									'<span class="token string">simple</span>' { [ <span class="token operator">number</span> ] }
								)
							}
							'<span class="token string">text</span>' {
								'<span class="token string">filter</span>': stategroup (
									'<span class="token string">pattern</span>' {
										'<span class="token string">criteria</span>': [ <span class="token operator">match</span> ] text
									}
									'<span class="token string">simple</span>' { [ <span class="token operator">text</span> ] }
									'<span class="token string">current node</span>' { [ <span class="token operator">this</span> ] }
									'<span class="token string">containment</span>' { [ <span class="token operator">filter</span>, <span class="token operator">selection</span> ]
										'<span class="token string">operator</span>': stategroup (
											'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
											'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
										)
									}
								)
							}
						)
					}
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">sort</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">sort:</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
					'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-property">'handheld view property'</a>
					'<span class="token string">direction</span>': stategroup (
						'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
						'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
					)
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">action</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">view:</span> ]
					'<span class="token string">emphasis</span>': stategroup (
						'<span class="token string">low</span>' { }
						'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
						'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
					)
					'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">group navigation</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
		}
		'<span class="token string">state navigation</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
		}
		'<span class="token string">reference navigation</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
		}
		'<span class="token string">pivot view</span>' { [ <span class="token operator">pivot</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">options</span>': group { dynamic-order
				'<span class="token string">show crosshair</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@crosshair</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">show grid</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@grid</span> ] }
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">columns</span>': [ <span class="token operator">columns:</span> <span class="token operator">.</span> ] reference
			'<span class="token string">column grouping</span>': [ <span class="token operator">:</span> ] reference
			'<span class="token string">column label</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
			'<span class="token string">cells</span>': [ <span class="token operator">cells:</span> <span class="token operator">.</span> ] reference
			'<span class="token string">row grouping</span>': [ <span class="token operator">:</span> ] reference
			'<span class="token string">row label</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
			'<span class="token string">content</span>': stategroup (
				'<span class="token string">inline view</span>' { [ <span class="token operator">inline</span> <span class="token operator">view:</span> ]
					'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
				}
				'<span class="token string">label</span>' { [ <span class="token operator">label:</span> ]
					'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
				}
			)
		}
		'<span class="token string">detail view</span>' { [ <span class="token operator">details</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
			'<span class="token string">elements</span>': component <a href="#grammar-rule--handheld-view-elements">'handheld view elements'</a>
		}
		'<span class="token string">command view</span>' { [ <span class="token operator">command</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
			'<span class="token string">selection</span>': [ <span class="token operator">view:</span> ] stategroup (
				'<span class="token string">button</span>' {
					'<span class="token string">emphasis</span>': stategroup (
						'<span class="token string">low</span>' { }
						'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
						'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
					)
				}
				'<span class="token string">scan</span>' { [ <span class="token operator">@scan</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">referencer</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
					}
					'<span class="token string">path</span>': [ <span class="token operator">using:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">search property</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-descriptor }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view descriptor</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic</span>' {
			'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-property-selector">'handheld view property selector'</a>
		}
		'<span class="token string">static text</span>' {
			'<span class="token string">text</span>': reference
		}
		'<span class="token string">icon</span>' {
			'<span class="token string">icon name</span>': [ <span class="token operator">icon:</span> ] text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view property</span>' {
	'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">default</span>' { }
		'<span class="token string">barcode</span>' { [ <span class="token operator">@barcode:</span> ]
			'<span class="token string">barcode type</span>': stategroup (
				'<span class="token string">CODE128</span>' { [ <span class="token operator">CODE128</span> ] }
				'<span class="token string">CODE128A</span>' { [ <span class="token operator">CODE128A</span> ] }
				'<span class="token string">CODE128B</span>' { [ <span class="token operator">CODE128B</span> ] }
				'<span class="token string">CODE128C</span>' { [ <span class="token operator">CODE128C</span> ] }
				'<span class="token string">EAN13</span>' { [ <span class="token operator">EAN13</span> ] }
				'<span class="token string">EAN8</span>' { [ <span class="token operator">EAN8</span> ] }
				'<span class="token string">EAN5</span>' { [ <span class="token operator">EAN5</span> ] }
				'<span class="token string">EAN2</span>' { [ <span class="token operator">EAN2</span> ] }
				'<span class="token string">UPCA</span>' { [ <span class="token operator">UPCA</span> ] }
				'<span class="token string">UPCE</span>' { [ <span class="token operator">UPCE</span> ] }
				'<span class="token string">CODE39</span>' { [ <span class="token operator">CODE39</span> ] }
				'<span class="token string">ITF</span>' { [ <span class="token operator">ITF</span> ] }
				'<span class="token string">ITF14</span>' { [ <span class="token operator">ITF14</span> ] }
				'<span class="token string">MSI10</span>' { [ <span class="token operator">MSI10</span> ] }
				'<span class="token string">MSI11</span>' { [ <span class="token operator">MSI11</span> ] }
				'<span class="token string">MSI1010</span>' { [ <span class="token operator">MSI1010</span> ] }
				'<span class="token string">MSI1110</span>' { [ <span class="token operator">MSI1110</span> ] }
				'<span class="token string">Pharmacode</span>' { [ <span class="token operator">Pharmacode</span> ] }
				'<span class="token string">Codabar</span>' { [ <span class="token operator">Codabar</span> ] }
			)
		}
		'<span class="token string">qrcode</span>' { [ <span class="token operator">@qrcode</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-property-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view property selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">switch</span>' {
			'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-property-selector">'handheld view property selector'</a>
			}
		}
		'<span class="token string">step</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-property-selector">'handheld view property selector'</a>
		}
		'<span class="token string">property</span>' {
			'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-property">'handheld view property'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-command-annotations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld command annotations</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
				'<span class="token string">states</span>': dictionary {
					'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
				}
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">style</span>': stategroup (
					'<span class="token string">buttons</span>' { [ <span class="token operator">@button</span> ] }
					'<span class="token string">keyboard</span>' { [ <span class="token operator">@keyboard</span> ] }
					'<span class="token string">default</span>' { }
					'<span class="token string">scan</span>' { [ <span class="token operator">@scan</span> <span class="token operator">using:</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">search property</span>': [ <span class="token operator">.</span> ] reference
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view context</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-context">'handheld view context'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">switch</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
			}
		}
		'<span class="token string">step</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
		}
		'<span class="token string">command</span>' {
			'<span class="token string">command</span>': [ <span class="token operator">command:</span> ] reference
			'<span class="token string">annotations</span>': group { dynamic-order
				'<span class="token string">auto execute</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@auto-execute</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">close after execute</span>': stategroup (
					'<span class="token string">yes</span>' { }
					'<span class="token string">no</span>' { [ <span class="token operator">@keep-open</span> ] }
				)
				'<span class="token string">emphasis</span>': stategroup (
					'<span class="token string">low</span>' { }
					'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
					'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
				)
			}
			'<span class="token string">parameter annotations</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">open view</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">and</span> ]
					'<span class="token string">context</span>': component <a href="#grammar-rule--handheld-view-context">'handheld view context'</a>
					'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">has details</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">details</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
					'<span class="token string">elements</span>': component <a href="#grammar-rule--handheld-view-elements">'handheld view elements'</a>
				}
			)
		}
		'<span class="token string">view</span>' {
			'<span class="token string">emphasis</span>': [ <span class="token operator">:</span> ] stategroup (
				'<span class="token string">low</span>' { }
				'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
				'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
			)
			'<span class="token string">context</span>': component <a href="#grammar-rule--handheld-view-context">'handheld view context'</a>
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
			'<span class="token string">title</span>': stategroup (
				'<span class="token string">custom</span>' { [ <span class="token operator">title:</span> ]
					'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
				}
				'<span class="token string">default</span>' { }
			)
		}
	)
}
</pre>
</div>
</div>
