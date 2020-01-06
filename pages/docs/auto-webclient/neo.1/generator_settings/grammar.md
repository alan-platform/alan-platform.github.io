---
layout: doc
origin: auto-webclient
language: generator_settings
version: neo.1
type: grammar
---

Global settings for the user interface.

```js
'application creator' ['application' 'creator:'] text
```

```js
'application name' ['application' 'name:'] text
```

```js
'allow anonymous user' [ 'anonymous' 'login:' ] stategroup (
	'no' [ 'disabled' ]
	'yes' [ 'enabled' ]
)
```

```js
'enable csv actions' [ 'csv' 'actions:' ] stategroup (
	'no' [ 'disabled' ]
	'yes' [ 'enabled' ]
)
```

```js
'report limit' [ 'report' 'limit:' ] number
```

```js
'announcement title' [ 'announcement:' ] text
```

```js
'announcements' [ '[' , ']' ] collection indent ( )
```

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

```js
'language' [ 'language:' ] text
```

```js
'engine language' [ 'engine' 'language:' ] stategroup (
	'english' [ 'english' ]
	'dutch' [ 'dutch' ]
)
```

```js
'has dashboard' stategroup (
	'yes'
		'dashboard' ['dashboard:'] component 'dashboard'
	'no'
)
```

```js
'has steps' stategroup (
	'no'
	'yes'
		'type' stategroup (
			'group'
				'group' ['+'] reference
		)
		'tail' component 'singular path'
)
```

```js
'head' component 'singular path'
```

```js
'has steps' stategroup (
	'no'
	'yes'
		'type' stategroup (
			'state'
				'state group' ['?'] reference
				'state' ['|'] reference
		)
	'tail' component 'conditional path'
```

```js
'has steps' stategroup (
	'no'
	'yes'
		'head' component 'conditional path'
		'collection' ['.'] reference
		'tail' component 'collection path'
)
```
### Dashboard
Dashboards use a grid layout. The grid needs to be configured with a cell width and cell height. Optionally a gap between cells can be configured.
Widgets are placed on the grid with a coordinate and a size in cells. The upper left cell of the grid is at coordinate (1, 1).
Optionally the size and margin of a widget can be explicitly set. Widgets with axes should be provided with a margin as the axes and labels are placed in the margin.
Each widget has a context node, all paths are relative to this node.

```js
'dashboard'
	'cell width' ['('] group (
		'size' number
		'unit' stategroup (
			'pixels' ['px']
			'font size' ['fs']
		)
	)
	'cell height' [','] group (
		'size' number
		'unit' stategroup (
			'pixels' ['px']
			'font size' ['fs']
		)
	)
	'grid gap' stategroup (
		'yes' [',',')']
			'size' number
			'unit' stategroup (
				'pixels' ['px']
				'font size' ['fs']
			)
		'no' [')']
	)
	'widgets' collection order 'order' (
		'has successor' stategroup has successor 'successor' 'yes' 'no'
		'x' ['('] number
		'width' ['/'] number
		'y' [','] number
		'height' ['/',')'] number
		'dimension' component 'dashboard ui dimension'
		'margin' component 'dashboard ui margin'
		'context path' component 'conditional path'
		'graph type' [':'] stategroup (
			'number' ['number']
				'value' ['#'] reference
				'size' stategroup (
					'large'
					'fixed' ['size:']
						'number size' stategroup (
							'large'
							'fixed'
								'value' number
						)
						'unit size' stategroup (
							'auto'
							'fixed' [',']
								'value' number
						)
				)
			'range'
				'chart type' stategroup (
					'progress bar' ['progress']
					'gauge' ['gauge']
				)
				'range start' ['ranges:'] stategroup (
					'static'
						'value' number
					'dynamic'
						'value' ['#'] reference
				)
				'ranges' component 'dashboard ranges'
				'value' ['value:''#'] reference
			'pie chart' ['pie-chart']
				'collection' component 'collection path'
				'label path' ['label:'] component 'conditional path'
				'label property' [':'] reference
				'value path' ['value:'] component 'conditional path'
				'value property' ['#'] reference
				'merge small slices' stategroup (
					'yes' ['merge']
						'below percentage' ['below','%'] number
					'no'
				)
				'sorting' stategroup (
					'yes' ['sort:']
						'direction' stategroup (
							'ascending' ['ascending']
							'descending' ['descending']
						)
					'no'
				)
			'bar chart' ['bar-chart']
				'collection' component 'collection path'
				'label path' ['label:'] component 'conditional path'
				'label property' [':'] reference
				'value path' ['value:'] component 'conditional path'
				'value property' ['#'] reference
				'sorting' stategroup (
					'yes' ['sort:']
						'direction' stategroup (
							'ascending' ['ascending']
							'descending' ['descending']
						)
					'no'
				)
			'grouped bar chart' ['grouped-bar-chart']
				'collection' component 'collection path'
				'label path' ['label:'] component 'conditional path'
				'label property' [':'] reference
				'values' ['(',')'] collection order 'order' (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'value path' [':'] component 'conditional path'
					'value property' ['#'] reference
					'color' [','] component 'dashboard color'
				)
				'has value' stategroup has 'values' first 'first' 'yes' 'no'
				'sorting' stategroup (
					'yes' ['sort:']
						'direction' stategroup (
							'ascending' ['ascending']
							'descending' ['descending']
						)
						'axis' stategroup (
							'single'
								'axis' reference
							'sum' ['sum']
						)
					'no'
				)
			'stacked bar chart' ['stacked-bar-chart']
				'collection' component 'collection path'
				'label path' ['label:'] component 'conditional path'
				'label property' [':'] reference
				'values' ['(',')'] collection order 'order' (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'value path' [':'] component 'conditional path'
					'value property' ['#'] reference
					'color' [','] component 'dashboard color'
				)
				'has value' stategroup has 'values' first 'first' 'yes' 'no'
				'sorting' stategroup (
					'yes' ['sort:']
						'direction' stategroup (
							'ascending' ['ascending']
							'descending' ['descending']
						)
						'axis' stategroup (
							'single'
								'axis' reference
							'sum' ['sum']
						)
					'no'
				)
			'line chart' ['line-chart']
				'collection' component 'collection path'
				'label path' ['label:'] component 'conditional path'
				'label property' [':'] reference
				'sort path' ['sort:'] component 'conditional path'
				'sort property' ['#'] reference
				'sort direction' [','] stategroup (
					'ascending' ['ascending']
					'descending' ['descending']
				)
				'values' ['(',')'] collection order 'order' (
					'has successor' stategroup has successor 'successor' 'yes' 'no'
					'value path' [':'] component 'conditional path'
					'value property' ['#'] reference
					'color' [','] component 'dashboard color'
				)
				'has value' stategroup has 'values' first 'first' 'yes' 'no'
			'scatter chart' ['scatter-chart']
				'collection' component 'collection path'
				'label x' ['axis-x:'] text
				'value x path' [','] component 'conditional path'
				'value x property' ['#'] reference
				'label y' ['axis-y:'] text
				'value y path' [','] component 'conditional path'
				'value y property' ['#'] reference
			'bubble chart' ['bubble-chart']
				'collection' component 'collection path'
				'label x' ['axis-x:'] text
				'value x path' [','] component 'conditional path'
				'value x property' ['#'] reference
				'label y' ['axis-y:'] text
				'value y path' [','] component 'conditional path'
				'value y property' ['#'] reference
				'value z path' ['size:'] component 'conditional path'
				'value z property' ['#'] reference
			'connected scatter chart' ['connected-scatter-chart']
				'collection' component 'collection path'
				'sort path' ['sort:'] component 'conditional path'
				'sort property' ['#'] reference
				'sort direction' [','] stategroup (
					'ascending' ['ascending']
					'descending' ['descending']
				)
				'label x' ['axis-x:'] text
				'value x path' [','] component 'conditional path'
				'value x property'['#'] reference
				'label y' ['axis-y:'] text
				'value y path' [','] component 'conditional path'
				'value y property' ['#'] reference
			'spider chart' ['spider-chart']
				'binding' stategroup (
					'static'
						'values' ['(',')'] collection order 'order' (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'value' [':''#'] reference
						)
						'has value' stategroup has 'values' first 'first' 'yes' 'no'
						'color' [','] component 'dashboard color'
					'dynamic'
						'collection' component 'collection path'
						'label path' ['label:'] component 'conditional path'
						'label property' [':'] reference
						'values' ['(',')'] collection order 'order' (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'value path' [':'] component 'conditional path'
							'value property' ['#'] reference
						)
						'has value' stategroup has 'values' first 'first' 'yes' 'no'
				)
			'radar chart' ['radar-chart']
				'binding' stategroup (
					'static'
						'values' ['(',')'] collection order 'order' (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'value' [':''#'] reference
						)
						'has value' stategroup has 'values' first 'first' 'yes' 'no'
						'color' [','] component 'dashboard color'
					'dynamic'
						'collection' component 'collection path'
						'label path' ['label:'] component 'conditional path'
						'label property' [':'] reference
						'values' ['(',')'] collection order 'order' (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'value path' [':'] component 'conditional path'
							'value property' ['#'] reference
						)
						'has value' stategroup has 'values' first 'first' 'yes' 'no'
				)
			'legend' ['legend']
				'binding' stategroup (
					'static'
						'values' ['(',')'] collection order 'order' (
							'has successor' stategroup has successor 'successor' 'yes' 'no'
							'color' [':'] component 'dashboard color'
						)
					'dynamic'
						'collection' component 'collection path'
						'label path' ['label:'] component 'conditional path'
						'label property' [':'] reference
				)
		)
	)
```
#### Widget: Number
Displays a single number found directly under the context node in a (by default) large font.
The label of the numerical type is also shown, by default in the normal font size.
#### Widget: Progress bar
Displays a bar which fills the closer the current value is to the end of the range.
The range of the bar can be split into several segments, each defining a different color.
The bar is given the color of the range the current value is in.
#### Widget: Gauge
Displays a gauge with an indicator where the current value is in the range.
The range can be split into several segments, each defining a different color.
The label of the numerical type is also shown on the gauge.
#### Widget: Pie Chart
Displays a pie chart. It creates a slice for each entry in the query result.
A label and value for each entry must be provided.
Optionally a threshold can be set, slice which occupy less percentage then the threshold are merged in a single 'other' slice.
The entries can optionally be sorted.
As pie charts can not show non-existing (value = 0) or negative values, it can only plot naturals.
#### Widget: Bar Chart
Displays a simple bar chart. It creates a single bar for each entry in the query result.
A label and value for each entry must be provided.
The entries can optionally be sorted.
Bar charts always show an y-axis starting at 0, negative values are not shown.
#### Widget: Grouped Bar Chart
Displays a bar chart like the normal bar chart widget, expect it creates multiple bars for each entry in the query result.
A label and one or more values for each entry must be provided. A color must be provided for each value.
As all values share the same y-axis, the numerical types of all values must be equal.
The entries can optionally be sorted, either on a specific value or the sum of all their values.
Bar charts always show an y-axis starting at 0, negative values are not shown.
#### Widget: Stacked Bar Chart
Displays a bar chart like the normal bar chart widget, expect it separates the bar into multiple segments for each entry in the query result.
A label and one or more values for each entry must be provided. A color must be provided for each value.
As all values share the same y-axis, the numerical types of all values must be equal.
The entries can optionally be sorted, either on a specific value or the sum of all their values.
Bar charts always show an y-axis starting at 0. Negative values cases bars to be placed on top of each other instead of stack on each other and are filter from the set.
#### Widget: Line Chart
Displays a line chart. It creates a single line for each value. Every entry in the query result adds a point to the line.
A sort criteria must be provided as the data has no inherit order. This sets to order of the entries in the query result and is not displayed as line.
As all values share the same y-axis, the numerical types of all values must be equal.
#### Widget: Scatter Chart
Displays a large amount of dots. It creates a single dot for each entry in the query result.
Two values for each entry must be provided, one for the x-axis and the other for the y-axis.
The dots are rendered partially transparent in the accent color.
#### Widget: Bubble Chart
Displays a number of dots like the scatter chart widget, but it takes an additional value for each entry in the query result for the size of the dot.
#### Widget: Connected Scatter Chart
Displays a number of dots like the scatter chart widget, but it also renders a line connecting the varies dots.
A sort criteria must be provided as the data has no inherit order.
The dots are rendered partially transparent in the accent color. The line is rendered solid in the accent color.
#### Widget: Spider Chart
Displays a spider chart. It either creates one area for the context node or creates an area for each entry in the query result.
Three or more values for each entry must be provided, one axis is generated for each value.
As all values share the same axis scale, the numerical types of all values must be equal.
The axes always start a 0, negative values are not shown.
#### Widget: Radar Chart
Displays a radar chart. This is mostly identical to the spider chart.
Unlike the spider chart, the grid is rendered with circles and the areas use rounded corners.
#### Widget: Legend
Displays a legend either for a set of value color pairs or for all entries in a query result.
The query variant automatically assigns colors to the labels use the same algorithm as most of the charts.
### Widget Annotation: Dimension
Allows the default size of a widget to be changed.
All values are in pixels.

```js
'dashboard ui dimension'
	'dimension' stategroup (
		'custom' ['@size(',')']
			'x' number
			'y' [','] number
		'default'
	)
```
### Widget Annotation: Margin
Allows the default margin of a widget to be changed.
All values are in pixels.

```js
'dashboard ui margin'
	'margin' stategroup (
		'custom' ['@margin(',')']
			'x1' number
			'x2' [','] number
			'y1' [','] number
			'y2' [','] number
		'default'
	)
```

```js
'dashboard ranges'
	'type' stategroup (
		'green' ['green']
		'blue' ['blue']
		'orange' ['orange']
		'red' ['red']
	)
	'range size' stategroup (
		'static'
			'value' number
		'dynamic'
			'value' ['#'] reference
	)
	'has more' stategroup (
		'yes' [',']
			'tail' component 'dashboard ranges'
		'no'
	)
```
### Widget Color
Allows the selection of a color. This can either be a predefined color or a custom color.
Predefined colors are provided by the color theme.
Custom colors are not bound to the theme and can be any CSS color, for example: `#FF8000`, `rgb(100%, 50%, 0%)` and `hsl(30deg, 100%, 50%)` all specify the same shade of orange.

```js
'dashboard color'
	'color' stategroup (
		'blue' ['blue']
		'orange' ['orange']
		'green' ['green']
		'red' ['red']
		'black' ['black']
		'grey' ['grey']
		'grey light' ['grey''light']
		'grey dark' ['grey''dark']
		'teal' ['teal']
		'purple' ['purple']
		'hex'
			'value' text
	)
```
