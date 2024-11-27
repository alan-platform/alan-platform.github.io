---
layout: "doc"
origin: "webclient"
language: "default features"
version: "yar.12rc6.0"
type: "features"
---

1. TOC
{:toc}

```js
global-features
	'full screen planning' {
		'default zoom level': feature 'zoom level'
		'has more zoom levels': stategroup @default: 'no' (
			'yes' {
				'zoom levels': list non-empty {
					'zoom level': feature 'zoom level'
				}
			}
			'no' { }
		)
		'windows': list non-empty {
			'label': text
			'window': feature 'planning'
		}
	}
	'dashboard' {
		'dashboard': feature 'dashboard 2'
	}
node-features
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
		'rows': collection binding {
			'label': feature 'label'
			'options': feature 'row options'
			'items': collection binding {
				'label': feature 'label'
				'start': number binding { }
				'end': number binding { }
				'options': feature 'item options'
			}
		}
	}
	'row options' component {
		'is reference set': stategroup @default: 'no' (
			'yes' {
				'reference': text binding { }
			}
			'no' { }
		)
		'has filters': stategroup @default: 'no' (
			'yes' {
				'filters': feature 'filters'
			}
			'no' { }
		)
		'has tooltip': stategroup @default: 'no' (
			'yes' {
				'label': feature 'label'
			}
			'no' { }
		)
		'has group': stategroup @default: 'no' (
			'yes' {
				'group': text binding { }
			}
			'no' { }
		)
		'has children': stategroup @default: 'no' (
			'yes' {
				'rows': feature 'planning'
			}
			'no' { }
		)
		'filter start and end': stategroup @default: 'no' (
			'yes' {
				'start': number binding { }
				'end': number binding { }
			}
			'no' { }
		)
		'has popup': stategroup @default: 'no' (
			'yes' {
				'popup': feature 'popup'
			}
			'no' { }
		)
		'can create entry': stategroup @default: 'no' (
			'yes' {
				'create': command binding {
					'start': number binding { }
					'end': number binding { }
				}
			}
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
			'yes' {
				'filters': feature 'filters'
			}
			'no' { }
		)
		'has tooltip': stategroup @default: 'no' (
			'yes' {
				'label': feature 'label'
			}
			'no' { }
		)
		'draggable': stategroup @default: 'no' (
			'yes' {
				'move': command binding {
					'start': number binding { }
					'can switch row': stategroup @default: 'no' (
						'yes' {
							'row': text binding { }
						}
						'no' { }
					)
					'can be dropped on item': stategroup @default: 'no' (
						'yes' {
							'item': text binding { }
						}
						'no' { }
					)
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
							'can be dropped on item': stategroup @default: 'no' (
								'yes' {
									'item': text binding { }
								}
								'no' { }
							)
						}
					}
					'no' { }
				)
			}
			'no' { }
		)
		'has popup': stategroup @default: 'no' (
			'yes' {
				'popup': feature 'popup'
			}
			'no' { }
		)
		'has icon bar': stategroup @default: 'no' (
			'yes' {
				'stategroups': list non-empty {
					'stategroup': stategroup binding {
						'states': list {
							'state': state binding {
								'has tooltip': stategroup @default: 'no' (
									'yes' {
										'label': feature 'label'
									}
									'no' { }
								)
							}
						}
					}
				}
			}
			'no' { }
		)
		'has context menu': stategroup @default: 'no' (
			'yes' {
				'context menu': feature 'context menu'
			}
			'no' { }
		)
	}
	'filters' component {
		'filters': list non-empty {
			'label': text
			'type': stategroup (
				'number' {
					'number': number binding { }
				}
				'text' {
					'text': text binding { }
				}
				'stategroup' {
					'stategroup': stategroup binding { }
				}
			)
		}
	}
	'zoom level' component unbound {
		'name': text
		'days before today': number
		'days after today': number
		'tag interval': number
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
		'width': number
		'date tags size': stategroup (
			'm' { }
			's' { }
			'xs' { }
		)
		'round off to day': stategroup (
			'yes' { }
			'no' { }
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
									'yes' {
										'node': feature 'node'
									}
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
				// 'planning' {
				// 	'planning': feature 'planning'
				// }
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
