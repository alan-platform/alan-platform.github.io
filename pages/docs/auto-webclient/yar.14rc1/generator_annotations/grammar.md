---
layout: "doc"
origin: "auto-webclient"
language: "generator_annotations"
version: "yar.14rc1"
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

	'dashboard' feature 'dashboard 2'

	'layout' {
		'density': stategroup @default: 'compact' (
			'compact' { }
			'comfortable' { }
		)
	}

node-features
	'permissions' component {
		'source': stategroup (
			'user' {
				'user': user binding {
					'stategroup': stategroup binding {
						'state': state binding { }
					}
				}
			}
			'node' {
				'node': node binding { }
			}
		)
	}

	'dimension' component unbound {
		'dimension': stategroup @default: 'default' (
			'custom' {
				'width': number
				'height': number
			}
			'default' { }
		)
	}

	'margin' component unbound {
		'margin': stategroup @default: 'default' (
			'custom' {
				'top': number
				'right': number
				'bottom': number
				'left': number
			}
			'default' { }
		)
	}

	'color' component unbound {
		'color': stategroup @default: 'auto' (
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
			'hex' {
				'value': text
			}
		)
	}

	'range' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'range start': stategroup (
			'static' {
				'value': number
			}
			'dynamic' {
				'value': number binding { }
			}
		)
		'ranges': list {
			'type': stategroup (
				'green' { }
				'blue' { }
				'orange' { }
				'red' { }
			)
			'range size': stategroup (
				'static' {
					'value': number
				}
				'dynamic' {
					'value': number binding { }
				}
			)
		}
		'value': number binding { }
		'style': stategroup (
			'progress bar' { }
			'gauge' { }
		)
	}

	'pie chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': query binding {
			'label': query text binding { }
			'property': query number binding { }
			'merge small slices': stategroup (
				'yes' {
					'below percentage': number
				}
				'no' { }
			)
			'sorting': stategroup (
				'yes' {
					'direction': stategroup (
						'ascending' { }
						'descending' { }
					)
				}
				'no' { }
			)
		}
	}

	'bar chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': query binding {
			'label': query text binding { }
			'style': stategroup (
				'grouped' {
					'bars': list {
						'property': query number binding { }
						'color': feature 'color'
					}
				}
				'stacked' {
					'bars': list {
						'property': query number binding { }
						'color': feature 'color'
					}
				}
				'bar' {
					'property': query number binding { }
				}
			)
			'sorting': stategroup (
				'yes' {
					'direction': stategroup (
						'ascending' { }
						'descending' { }
					)
					'axis': stategroup (
						'single' {
							'sort': query number binding { }
						}
						'sum' { }
					)
				}
				'no' { }
			)
		}
	}

	'line chart query' component query {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'label': query text binding { }
		'lines': list {
			'property': query number binding { }
			'color': feature 'color'
		}
		'style': stategroup (
			'line' { }
			'area' { }
		)
		'sort': query number binding {
			'direction': stategroup (
				'ascending' { }
				'descending' { }
			)
		}
	}

	'chart value' component query {
		'type': stategroup (
			'text' {
				'property': query text binding { }
			}
			'number' {
				'property': query number binding { }
			}
		// TODO 'state group' {
		// 	'property': query stategroup binding { }
		// }
		)
	}

	'2d chart query' component query {
		'title': text
		'x': feature 'chart value'
		'x label': stategroup @default: 'auto' (
			'auto' { }
			'text' {
				'property': query text binding { }
			}
		)
		'x axis title': stategroup @default: 'none' (
			'none' { }
			'set' {
				'text': text
			}
		)
		'y axis title': stategroup @default: 'none' (
			'none' { }
			'set' {
				'text': text
			}
		)
		'format x': stategroup @default: 'auto' (
			'auto' { }
			'day' { }
			'month' { }
			'month and year' { }
			'week' { }
			'week and year' { }
			'custom' {
				'parts': list non-empty {
					'type': stategroup (
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
						'text' {
							'value': text
						}
					)
				}
			}
		)
		'group x value': stategroup @default: 'no' (
			'no' { }
			'yes' {
				'group by': stategroup @default: 'none' (
					'none' { }
					'week' { }
					'month' { }
					'quarter' { }
					'year' { }
				)
			}
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
			'y': query number binding { }
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
				'custom' {
					'color': text
				}
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
					'value': query text binding { }
					'color': stategroup @default: 'auto' (
						'auto' { }
						'custom' {
							'color': query text binding { }
						}
					)
				}
			)
		}
	}

	'line chart' {
		'query': query binding {
			'chart': feature 'line chart query'
		}
	}

	'scatter chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': query binding {
			'label': query text binding { }
			'x label': text
			'x property': query number binding { }
			'y label': text
			'y property': query number binding { }
			'style': stategroup (
				'dot' { }
				'connected dot' {
					'sort': query number binding {
						'direction': stategroup (
							'ascending' { }
							'descending' { }
						)
					}
				}
				'bubble' {
					'z property': query number binding { }
				}
			)
		}
	}

	'radar chart' {
		'dimension': feature 'dimension'
		'margin': feature 'margin'
		'query': query binding {
			'label': query text binding { }
			'values': list {
				'property': query number binding { }
			}
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
			'yes' {
				'size': number @default: 20
			}
			'no' { }
		)
		'widgets': list {
			'x': number
			'width': number
			'y': number
			'height': number
			'widget': stategroup (
				'number' {
					'value': number binding { }
					'number size': stategroup (
						'large' { }
						'fixed' {
							'value': number
						}
					)
					'unit size': stategroup @default: 'auto' (
						'auto' { }
						'fixed' {
							'value': number
						}
					)
				}
				'range' {
					'range': feature 'range'
				}
				'pie chart' {
					'chart': feature 'pie chart'
				}
				'bar chart' {
					'chart': feature 'bar chart'
				}
				'line chart' {
					'chart': feature 'line chart'
				}
				'scatter chart' {
					'chart': feature 'scatter chart'
				}
				'radar chart' {
					'chart': feature 'radar chart'
				}
				'legend' {
					'binding': stategroup (
						'static' {
							'values': list {
								'label': text
								'color': feature 'color'
							}
						}
						'dynamic' {
							'query': query binding {
								'label': query text binding { }
							}
						}
					)
				}
			)
		}
	}

	'dashboard 2' {
		'has permissions': stategroup @default: 'no' (
			'yes' feature 'permissions'
			'no' { }
		)
		'widgets': list {
			'type': stategroup (
				'grouped charts' {
					'query': query binding {
						'charts': list {
							'widget': stategroup (
								'2d chart' {
									'chart': feature '2d chart query'
								}
								'reference filter' {
									/// In order to use the reference filter, make sure the text property is a
									/// reference. Also configure the filter on the query property correctly by
									/// providing the filter `in selection` as follows:
									/// ```
									/// 'a reference' -> ^ : text 'entry' filter in selection
									/// ```
									'property': query text binding { }
								}
								'table' {
									'title': text
									'size': stategroup @default: 'small' (
										'small' { }
										'medium' { }
										'large' { }
									)
									'properties': list {
										'property': query property binding { }
									}
								}
							)
						}
					}
				}
				'tabs' {
					'widgets': list {
						'name': text
						'widget': feature 'dashboard 2'
					}
				}
			)
		}
	}

	'label' component {
		'parts': list non-empty {
			'type': stategroup (
				'static text' {
					'text': text
				}
				'dynamic text' {
					'text': text binding { }
				}
				'dynamic number' {
					'number': number binding { }
				}
			)
		}
	}

	'planning' component {
		'label': text
		'has permissions': stategroup @default: 'no' (
			'yes' feature 'permissions'
			'no' { }
		)
		'default zoom level': feature 'zoom level'
		'has more zoom levels': stategroup @default: 'no' (
			'yes' {
				'zoom levels': list non-empty feature 'zoom level'
			}
			'no' { }
		)
		'type': stategroup @default: 'default' (
			'default' { }
			'specific start and end' feature 'start and end'
		)
		'windows': list non-empty {
			'label': text
			'rows': feature 'planning rows'
		}
		'global commands': list {
			'command': command binding { }
		}
		'has holidays': stategroup @default: 'no' (
			'yes' {
				'holidays': collection binding {
					'holiday': text binding { }
					'start and end': feature 'start and end'
					'highlight background': stategroup @default: 'yes' (
						'yes' { }
						'state dependent' {
							'stategroup': stategroup binding {
								'state to highlight': state binding { }
							}
						}
						'no' { }
					)
				}
			}
			'no' { }
		)
	}

	'planning rows' component {
		'rows': collection binding {
			'label': feature 'label'
			'options': feature 'row options'
			'items': feature 'planning items'
			'has background items': stategroup @default: 'no' (
				'yes' feature 'planning background items'
				'no' { }
			)
			'has children': stategroup @default: 'no' (
				'yes' feature 'planning rows'
				'no' { }
			)
		}
		'has bottom rows': stategroup @default: 'no' (
			'yes' feature 'planning custom rows'
			'no' { }
		)
	}

	'planning items' component {
		'items': collection binding {
			'has label': stategroup (
				'yes' feature 'label'
				'no' { }
			)
			'start and end': feature 'start and end'
			'options': feature 'item options'
			'foreground options': feature 'foreground item options'
		}
	}

	'planning background items' component {
		'items': collection binding {
			'has label': stategroup @default: 'no' (
				'yes' feature 'label'
				'no' { }
			)
			'start and end': feature 'start and end'
			'options': feature 'item options'
		}
	}

	'planning custom rows' component {
		'rows': list {
			'label': feature 'label'
			'has tooltip': stategroup @default: 'no' (
				'yes' feature 'label'
				'no' { }
			)
			'items': feature 'planning items'
			'has background items': stategroup @default: 'no' (
				'yes' feature 'planning background items'
				'no' { }
			)
		}
	}

	'start and end' component {
		'start': number binding { }
		'end': number binding { }
	}

	'row options' component {
		'is reference set': stategroup @default: 'no' (
			'yes' {
				'reference': text binding { }
			}
			'no' { }
		)
		'has right label': stategroup @default: 'no' (
			'yes' {
				'label': feature 'label'
				'has tooltip': stategroup @default: 'no' (
					'yes' feature 'label'
					'no' { }
				)
			}
			'no' { }
		)
		'has filters': stategroup @default: 'no' (
			'yes' feature 'filters'
			'no' { }
		)
		'has tooltip': stategroup @default: 'no' (
			'yes' feature 'label'
			'no' { }
		)
		'filter start and end': stategroup @default: 'no' (
			'yes' feature 'start and end'
			'no' { }
		)
		'has popup': stategroup @default: 'no' (
			'yes' feature 'popup'
			'no' { }
		)
		'can create entry': stategroup @default: 'no' (
			'yes' {
				'create': command binding {
					'start': number binding { }
					'end': number binding { }
					'snap': feature 'snap'
				}
				'has alternative create command': stategroup @default: 'no' (
					'yes' {
						'create': command binding {
							'start': number binding { }
							'end': number binding { }
							'snap': feature 'snap'
						}
					}
					'no' { }
				)
				'draggable': stategroup (
					'yes' { }
					'no' { }
				)
			}
			'no' { }
		)
		'can be partitioned': stategroup @default: 'no' (
			'yes' feature 'partitions'
			'no' { }
		)
		'hide row when it has no items or child rows': stategroup @default: 'no' (
			'yes' { }
			'no' { }
		)
	}

	'item options' component {
		'is reference set': stategroup @default: 'no' (
			'yes' {
				'reference': text binding { }
			}
			'no' { }
		)
		'has filters': stategroup @default: 'no' (
			'yes' feature 'filters'
			'no' { }
		)
		'has tooltip': stategroup @default: 'no' (
			'yes' feature 'label'
			'no' { }
		)
		'has context menu': stategroup @default: 'no' (
			'yes' feature 'context menu'
			'no' { }
		)
	}

	'foreground item options' component {
		'draggable': stategroup @default: 'no' (
			'yes' feature 'draggable'
			'no' { }
		)
		'has popup': stategroup @default: 'no' (
			'yes' feature 'popup'
			'no' { }
		)
		'has icon bar': stategroup @default: 'no' (
			'yes' feature 'icon bar'
			'no' { }
		)
	}

	'partitions' component {
		'type': stategroup (
			'static' {
				'type': stategroup (
					'text' {
						'text': text binding { }
					}
					'stategroup' {
						'stategroup': stategroup binding { }
					}
				)
			}
			'dynamic' {
				'partitions': list non-empty {
					'label': text
					'type': stategroup (
						'text' {
							'text': text binding { }
						}
						'stategroup' {
							'stategroup': stategroup binding { }
						}
					)
				}
			}
		)
	}

	'filters' component {
		'filters': list non-empty {
			'label': text
			'type': stategroup (
				'number' {
					'number': number binding {
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
										'offset': number
									}
									'static number' {
										'criteria': number
									}
								)
							}
							'no' { }
						)
					}
				}
				'text' {
					'text': text binding {
						'has default filter': stategroup @default: 'no' (
							'yes' {
								'filter type': stategroup (
									'simple' {
										'value': text
									}
									'containment' {
										'relation': stategroup (
											'in' { }
											'not in' { }
										)
										'reference': text binding { }
									}
								)
							}
							'no' { }
						)
					}
				}
				'stategroup' {
					'stategroup': stategroup binding {
						'has default filter': stategroup @default: 'no' (
							'yes' {
								'filter type': stategroup (
									'state' { }
									'not state' { }
								)
								'state': state binding { }
							}
							'no' { }
						)
					}
				}
			)
		}
	}

	'zoom level' component unbound {
		'name': text
		'type': stategroup (
			'week' { }
			'day' {
				'show weekends': stategroup (
					'yes' { }
					'no' { }
				)
			}
			'hour' {
				'show weekends': stategroup (
					'yes' { }
					'no' { }
				)
			}
		)
	}

	'snap' component unbound {
		'snap': stategroup (
			'none' { }
			'minute' {
				'minutes': number
			}
			'day' { }
			'week' { }
			'month' { }
			'year' { }
		)
	}

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

	'context menu' component {
		'commands': list non-empty {
			'has icon': stategroup @default: 'no' (
				'yes' {
					'icon': text
				}
				'no' { }
			)
			'command': command binding { }
		}
	}

	'icon bar' component {
		'stategroups': list non-empty {
			'stategroup': stategroup binding {
				'states': list {
					'state': state binding {
						'has tooltip': stategroup @default: 'no' (
							'yes' feature 'label'
							'no' { }
						)
					}
				}
			}
		}
	}

	'draggable' component {
		'move': command binding {
			'start': number binding { }
			'can switch row': stategroup @default: 'no' (
				'yes' {
					'row': text binding { }
				}
				'no' { }
			)
			'snap': feature 'snap'
		}
		'has alternative move command': stategroup @default: 'no' (
			'yes' {
				'move': command binding {
					'start': number binding { }
					'can switch row': stategroup @default: 'no' (
						'yes' {
							'row': text binding { }
						}
						'no' { }
					)
					'snap': feature 'snap'
				}
			}
			'no' { }
		)
	}

	'node' component {
		'entries': list non-empty {
			'type': stategroup (
				'number' {
					'number': number binding { }
				}
				'text' {
					'text': text binding { }
				}
				'stategroup' {
					'stategroup': stategroup binding {
						'states': list {
							'state': state binding {
								'has node': stategroup @default: 'no' (
									'yes' feature 'node'
									'no' { }
								)
							}
						}
					}
				}
				'file' {
					'file': file binding { }
				}
				'command' {
					'command': command binding { }
				}
				'query' {
					'label': feature 'label'
					'query': query binding { }
				}
				'chart' {
					'label': feature 'label'
					'type': stategroup (
						'range' {
							'range': feature 'range'
						}
						'pie chart' {
							'chart': feature 'pie chart'
						}
						'bar chart' {
							'chart': feature 'bar chart'
						}
						'line chart' {
							'chart': feature 'line chart'
						}
						'scatter chart' {
							'chart': feature 'scatter chart'
						}
						'radar chart' {
							'chart': feature 'radar chart'
						}
					)
				}
			)
		}
	}

collection-features

stategroup-features

number-features

text-features

file-features
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
```
## Production
The production generator.

```js
global-features

node-features

collection-features

stategroup-features

number-features

text-features

file-features
```
# Annotations
## Global Features
Configure global features provided by the selected generator.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has global features</span>': stategroup (
	'<span class="token string">yes</span>' {
		'<span class="token string">configured features</span>': dictionary { [ <span class="token operator">feature</span> ]
			'<span class="token string">has more features</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next feature</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">feature</span>': component <a href="#grammar-rule--feature">'feature'</a>
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
## Sparse Annotation Tree
The root node of the annotations.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
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
	'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
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

{: #grammar-rule--query-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">query path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
					'<span class="token string">result</span>': stategroup (
						'<span class="token string">referenced node</span>' { }
						'<span class="token string">rule</span>' {
							'<span class="token string">rule</span>': [ <span class="token operator">$</span> ] reference
						}
					)
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--query-path">'query path'</a>
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
	'<span class="token string">node features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
	'<span class="token string">has handheld frames</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">handheld frames</span>': dictionary { [ <span class="token operator">handheld:</span> ]
				'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-view-frame">'handheld view frame'</a>
			}
			'<span class="token string">main frame</span>': reference = first
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">reference set</span>' { [ <span class="token operator">reference-set</span> ]
				'<span class="token string">has custom queries</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">custom queries</span>': dictionary { [ <span class="token operator">query</span> ]
							'<span class="token string">has more queries</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">next query</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
						}
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
						'<span class="token string">custom queries</span>': dictionary { [ <span class="token operator">query</span> ]
							'<span class="token string">has more queries</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">next query</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
						}
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">collection features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
				'<span class="token string">sub tree</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">stategroup features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
				}
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">number features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">text features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">file features</span>': component <a href="#grammar-rule--features-matrix">'features matrix'</a>
			}
		)
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
		'<span class="token string">feature</span>': component <a href="#grammar-rule--feature">'feature'</a>
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
	'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--feature-properties }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature properties</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
			'<span class="token string">binding</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
					'<span class="token string">node</span>' { [ <span class="token operator">node</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
					}
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">state</span>' { [ <span class="token operator">state</span> ]
						'<span class="token string">state</span>': reference
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">number</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">file</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">command</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">action</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">query</span>' { [ <span class="token operator">query</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
					}
					'<span class="token string">query property</span>' { [ <span class="token operator">query</span> <span class="token operator">property</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query stategroup</span>' { [ <span class="token operator">query</span> <span class="token operator">stategroup</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query number</span>' { [ <span class="token operator">query</span> <span class="token operator">number</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query text</span>' { [ <span class="token operator">query</span> <span class="token operator">text</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query file</span>' { [ <span class="token operator">query</span> <span class="token operator">file</span> ]
						'<span class="token string">property</span>': reference
					}
				)
				'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
			}
			'<span class="token string">configuration</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">list</span>' {
						'<span class="token string">properties</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--feature-properties-list">'feature properties list'</a>
					}
					'<span class="token string">stategroup</span>' {
						'<span class="token string">state</span>': reference
						'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
					}
					'<span class="token string">number</span>' {
						'<span class="token string">value</span>': integer
					}
					'<span class="token string">text</span>' {
						'<span class="token string">value</span>': text
					}
				)
			}
			'<span class="token string">feature</span>' {
				'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--feature-properties-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature properties list</span>' {
	'<span class="token string">has entry</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">entry</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--feature-properties-list">'feature properties list'</a>
		}
		'<span class="token string">no</span>' { }
	)
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
		'<span class="token string">context path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--query-path">'query path'</a>
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
								'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--query-path">'query path'</a>
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
						'<span class="token string">path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--query-path">'query path'</a>
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
					'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
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
