---
layout: "doc"
origin: "webclient"
language: "default features"
version: "yar.16rc2.0"
type: "features"
---

1. TOC
{:toc}

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
```
setting `y aggregate` switches the default `sum` function to handle multiple y
values on the same x value.
```js
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
		'filters': feature 'filters'
		'custom limit': feature 'query limit'
		'custom sorting': feature 'sorting'
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
				'properties': list binding { }
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
	'planning holidays' component binding collection {
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
		'label': feature 'label'
		'options': feature 'row options'
		'items': feature 'planning items'
		'background items': feature 'optional background items'
		'children': feature 'optional rows'
	}
	'optional rows' component stategroup @default: 'not set' @strategy (
		'set' feature 'planning rows'
		'not set' none
	)
	'planning items' component binding nodes {
		'label': feature 'optional label'
		'start and end': feature 'start and end'
		'options': feature 'item options'
		'foreground options': feature 'foreground item options'
	}
	'planning background items' component binding nodes {
		'label': feature 'optional label'
		'start and end': feature 'start and end'
		'options': feature 'item options'
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
	'row options' component {
		'is reference set': feature 'is reference set'
		'right label': feature 'optional label with tooltip'
		'filters': feature 'optional filters'
		'tooltip': feature 'optional label'
		'start and end filter': feature 'optional start and end'
		'popup': feature 'optional popup'
		'entry creation command': feature 'optional entry creation'
		'partitioning': feature 'optional partitioning'
		'has filters dependent on children or items': stategroup @default: 'no' (
			'yes' feature 'filters dependent on children or items'
			'no' { }
		)
		'icon bar': feature 'optional icon bar'
	}
	'item options' component {
		'is reference set': feature 'is reference set'
		'filters': feature 'optional filters'
		'tooltip': feature 'optional label'
		'context menu': feature 'optional context menu'
	}
	'foreground item options' component {
		'draggable': feature 'optional draggable'
		'popup': feature 'optional popup'
		'icon bar': feature 'optional icon bar'
	}
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
	'filters' component list non-empty {
		'label': text
		'type': stategroup (
			'number' binding number {
				'has default filter': stategroup @default: 'no' (
					'yes' {
						'relation': stategroup (
							'smaller than' { }
							'smaller than or equal to' { }
							'equal to' { }
							'greater than or equal to' { }
							'greater than' { }
						)
						'comparand': stategroup (
							'now' {
								'offset': stategroup (
									'set' number
									'none' { }
								)
							}
							'static number' number
						)
					}
					'no' { }
				)
			}
			'text' binding text {
				'has default filter': stategroup @default: 'no' (
					'yes' stategroup (
						'simple' text
						'containment' {
							'relation': stategroup (
								'in' { }
								'not in' { }
							)
							'reference': binding text { }
						}
					)
					'no' { }
				)
			}
			'stategroup' binding stategroup {
				'has default filter': stategroup @default: 'no' (
					'yes' {
						'filter type': stategroup (
							'state' { }
							'not state' { }
						)
						'state': binding state { }
					}
					'no' { }
				)
			}
		// 'file' binding file { } TODO
		)
	}
	'optional filters' component stategroup @default: 'not set' @strategy (
		'set' feature 'filters'
		'not set' none
	)
	'filters dependent on children or items' component {
		'hide row when it has no items label': text @default: "Hide rows without items"
		'hide row when it has no items': stategroup @default: 'no' (
			'yes' { }
			'no' { }
		)
		'hide row when it has no child rows label': text @default: "Hide rows without child rows"
		'hide row when it has no child rows': stategroup @default: 'no' (
			'yes' { }
			'no' { }
		)
	}
	'optional filters dependent on children or items' component stategroup @default: 'not set' @strategy (
		'set' feature 'filters dependent on children or items'
		'not set' none
	)
	'zoom level' component unbound {
		'name': text
		'type': stategroup (
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
		'custom sorting': feature 'sorting'
		'custom limit': feature 'query limit'
		'properties': feature 'filters'
	}
	'sorting' component stategroup @default: 'no' (
		'yes' {
			'direction': stategroup (
				'ascending' { }
				'descending' { }
			)
			'type': stategroup (
				'number' binding number { }
				'text' binding text { }
			)
		}
		'no' { }
	)
	'query limit' component stategroup @default: 'no' (
		'yes' {
			'sample': stategroup (
				'yes' {
					'sample size': number
					'sample limit': number
				}
				'no' { }
			)
			'absolute limit': number
		}
		'no' { }
	)
collection-features
stategroup-features
number-features
text-features
file-features
```
