---
layout: doc
origin: auto-webclient
language: generator_settings
version: neo.4
type: grammar
---

1. TOC
{:toc}

### Settings
Global settings for the user interface:

{: #grammar-rule--application-creator }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application creator</span>' [ <span class="token operator">application</span> <span class="token operator">creator:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--application-name }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application name</span>' [ <span class="token operator">application</span> <span class="token operator">name:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--allow-anonymous-user }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">allow anonymous user</span>' [ <span class="token operator">anonymous</span> <span class="token operator">login:</span> ] stategroup (
	'<span class="token string">no</span>' [ <span class="token operator">disabled</span> ]
	'<span class="token string">yes</span>' [ <span class="token operator">enabled</span> ]
)
</pre>
</div>
</div>

{: #grammar-rule--enable-csv-actions }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">enable csv actions</span>' [ <span class="token operator">csv</span> <span class="token operator">actions:</span> ] stategroup (
	'<span class="token string">no</span>' [ <span class="token operator">disabled</span> ]
	'<span class="token string">yes</span>' [ <span class="token operator">enabled</span> ]
)
</pre>
</div>
</div>

{: #grammar-rule--report-limit }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">report limit</span>' [ <span class="token operator">report</span> <span class="token operator">limit:</span> ] number
</pre>
</div>
</div>

{: #grammar-rule--announcement-title }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">announcement title</span>' [ <span class="token operator">announcement:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--announcements }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">announcements</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] collection indent ( )
</pre>
</div>
</div>

{: #grammar-rule--custom-color-theme }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom color theme</span>' stategroup (
	'<span class="token string">no</span>'
	'<span class="token string">yes</span>' [ <span class="token operator">color</span> <span class="token operator">theme:</span> ]
		'<span class="token string">foreground</span>' [ <span class="token operator">foreground:</span> ] text
		'<span class="token string">background</span>' [ <span class="token operator">background:</span> ] text
		'<span class="token string">brand</span>' [ <span class="token operator">brand:</span> ] text
		'<span class="token string">link</span>' [ <span class="token operator">link:</span> ] text
		'<span class="token string">accent</span>' [ <span class="token operator">accent:</span> ] text
		'<span class="token string">success</span>' [ <span class="token operator">success:</span> ] text
		'<span class="token string">warning</span>' [ <span class="token operator">warning:</span> ] text
		'<span class="token string">error</span>' [ <span class="token operator">error:</span> ] text
		'<span class="token string">blue</span>' [ <span class="token operator">blue:</span> ] text
		'<span class="token string">orange</span>' [ <span class="token operator">orange:</span> ] text
		'<span class="token string">green</span>' [ <span class="token operator">green:</span> ] text
		'<span class="token string">red</span>' [ <span class="token operator">red:</span> ] text
		'<span class="token string">purple</span>' [ <span class="token operator">purple:</span> ] text
		'<span class="token string">teal</span>' [ <span class="token operator">teal:</span> ] text
)
</pre>
</div>
</div>

{: #grammar-rule--language }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">language</span>' [ <span class="token operator">language:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--engine-language }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">engine language</span>' [ <span class="token operator">engine</span> <span class="token operator">language:</span> ] stategroup (
	'<span class="token string">english</span>' [ <span class="token operator">english</span> ]
	'<span class="token string">dutch</span>' [ <span class="token operator">dutch</span> ]
)
</pre>
</div>
</div>

{: #grammar-rule--has-dashboard }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has dashboard</span>' stategroup (
	'<span class="token string">yes</span>'
		'<span class="token string">dashboard</span>' [ <span class="token operator">dashboard:</span> ] component <a href="#grammar-rule--dashboard">'dashboard'</a>
	'<span class="token string">no</span>'
)
</pre>
</div>
</div>

{: #grammar-rule--has-landing-page }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has landing page</span>' stategroup (
	'<span class="token string">yes</span>' [ <span class="token operator">landing-page:</span> ]
		'<span class="token string">from</span>' stategroup (
			'<span class="token string">user</span>' [ <span class="token operator">user</span> ]
			'<span class="token string">root</span>' [ <span class="token operator">root</span> ]
		)
		'<span class="token string">expression</span>' component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
	'<span class="token string">no</span>'
)
</pre>
</div>
</div>
### Dashboard
Dashboards use a grid layout. The grid needs to be configured with a cell width and cell height. Optionally a gap between cells can be configured.
Widgets are placed on the grid with a coordinate and a size in cells. The upper left cell of the grid is at coordinate (1, 1).
Optionally the size and margin of a widget can be explicitly set. Widgets with axes should be provided with a margin as the axes and labels are placed in the margin.
Each widget has a context node, all paths are relative to this node.

{: #grammar-rule--dashboard }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard</span>'
	'<span class="token string">cell width</span>' [ <span class="token operator">(</span> ] group (
		'<span class="token string">size</span>' number
		'<span class="token string">unit</span>' stategroup (
			'<span class="token string">pixels</span>' [ <span class="token operator">px</span> ]
			'<span class="token string">font size</span>' [ <span class="token operator">fs</span> ]
		)
	)
	'<span class="token string">cell height</span>' [ <span class="token operator">,</span> ] group (
		'<span class="token string">size</span>' number
		'<span class="token string">unit</span>' stategroup (
			'<span class="token string">pixels</span>' [ <span class="token operator">px</span> ]
			'<span class="token string">font size</span>' [ <span class="token operator">fs</span> ]
		)
	)
	'<span class="token string">grid gap</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">,</span>, <span class="token operator">)</span> ]
			'<span class="token string">size</span>' number
			'<span class="token string">unit</span>' stategroup (
				'<span class="token string">pixels</span>' [ <span class="token operator">px</span> ]
				'<span class="token string">font size</span>' [ <span class="token operator">fs</span> ]
			)
		'<span class="token string">no</span>' [ <span class="token operator">)</span> ]
	)
	'<span class="token string">widgets</span>' collection order '<span class="token string">order</span>' (
		'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
		'<span class="token string">x</span>' [ <span class="token operator">(</span> ] number
		'<span class="token string">width</span>' [ <span class="token operator">/</span> ] number
		'<span class="token string">y</span>' [ <span class="token operator">,</span> ] number
		'<span class="token string">height</span>' [ <span class="token operator">/</span>, <span class="token operator">)</span> ] number
		'<span class="token string">dimension</span>' component <a href="#grammar-rule--dashboard-ui-dimension">'dashboard ui dimension'</a>
		'<span class="token string">margin</span>' component <a href="#grammar-rule--dashboard-ui-margin">'dashboard ui margin'</a>
		'<span class="token string">context path</span>' component <a href="#grammar-rule--conditional-path">'conditional path'</a>
		'<span class="token string">graph type</span>' [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
				'<span class="token string">value</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">size</span>' stategroup (
					'<span class="token string">large</span>'
					'<span class="token string">fixed</span>' [ <span class="token operator">size:</span> ]
						'<span class="token string">number size</span>' stategroup (
							'<span class="token string">large</span>'
							'<span class="token string">fixed</span>'
								'<span class="token string">value</span>' number
						)
						'<span class="token string">unit size</span>' stategroup (
							'<span class="token string">auto</span>'
							'<span class="token string">fixed</span>' [ <span class="token operator">,</span> ]
								'<span class="token string">value</span>' number
						)
				)
			'<span class="token string">range</span>'
				'<span class="token string">chart type</span>' stategroup (
					'<span class="token string">progress bar</span>' [ <span class="token operator">progress</span> ]
					'<span class="token string">gauge</span>' [ <span class="token operator">gauge</span> ]
				)
				'<span class="token string">range start</span>' [ <span class="token operator">ranges:</span> ] stategroup (
					'<span class="token string">static</span>'
						'<span class="token string">value</span>' number
					'<span class="token string">dynamic</span>'
						'<span class="token string">value</span>' [ <span class="token operator">#</span> ] reference
				)
				'<span class="token string">ranges</span>' component <a href="#grammar-rule--dashboard-ranges">'dashboard ranges'</a>
				'<span class="token string">value</span>' [ <span class="token operator">value:</span> <span class="token operator">#</span> ] reference
			'<span class="token string">pie chart</span>' [ <span class="token operator">pie-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
				'<span class="token string">value path</span>' [ <span class="token operator">value:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">merge small slices</span>' stategroup (
					'<span class="token string">yes</span>' [ <span class="token operator">merge</span> ]
						'<span class="token string">below percentage</span>' [ <span class="token operator">below</span>, <span class="token operator">%</span> ] number
					'<span class="token string">no</span>'
				)
				'<span class="token string">sorting</span>' stategroup (
					'<span class="token string">yes</span>' [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>' stategroup (
							'<span class="token string">ascending</span>' [ <span class="token operator">ascending</span> ]
							'<span class="token string">descending</span>' [ <span class="token operator">descending</span> ]
						)
					'<span class="token string">no</span>'
				)
			'<span class="token string">bar chart</span>' [ <span class="token operator">bar-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
				'<span class="token string">value path</span>' [ <span class="token operator">value:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">sorting</span>' stategroup (
					'<span class="token string">yes</span>' [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>' stategroup (
							'<span class="token string">ascending</span>' [ <span class="token operator">ascending</span> ]
							'<span class="token string">descending</span>' [ <span class="token operator">descending</span> ]
						)
					'<span class="token string">no</span>'
				)
			'<span class="token string">grouped bar chart</span>' [ <span class="token operator">grouped-bar-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
				'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
					'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
					'<span class="token string">value path</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
					'<span class="token string">color</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
				)
				'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
				'<span class="token string">sorting</span>' stategroup (
					'<span class="token string">yes</span>' [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>' stategroup (
							'<span class="token string">ascending</span>' [ <span class="token operator">ascending</span> ]
							'<span class="token string">descending</span>' [ <span class="token operator">descending</span> ]
						)
						'<span class="token string">axis</span>' stategroup (
							'<span class="token string">single</span>'
								'<span class="token string">axis</span>' reference
							'<span class="token string">sum</span>' [ <span class="token operator">sum</span> ]
						)
					'<span class="token string">no</span>'
				)
			'<span class="token string">stacked bar chart</span>' [ <span class="token operator">stacked-bar-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
				'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
					'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
					'<span class="token string">value path</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
					'<span class="token string">color</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
				)
				'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
				'<span class="token string">sorting</span>' stategroup (
					'<span class="token string">yes</span>' [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>' stategroup (
							'<span class="token string">ascending</span>' [ <span class="token operator">ascending</span> ]
							'<span class="token string">descending</span>' [ <span class="token operator">descending</span> ]
						)
						'<span class="token string">axis</span>' stategroup (
							'<span class="token string">single</span>'
								'<span class="token string">axis</span>' reference
							'<span class="token string">sum</span>' [ <span class="token operator">sum</span> ]
						)
					'<span class="token string">no</span>'
				)
			'<span class="token string">line chart</span>' [ <span class="token operator">line-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
				'<span class="token string">sort path</span>' [ <span class="token operator">sort:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">sort property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">sort direction</span>' [ <span class="token operator">,</span> ] stategroup (
					'<span class="token string">ascending</span>' [ <span class="token operator">ascending</span> ]
					'<span class="token string">descending</span>' [ <span class="token operator">descending</span> ]
				)
				'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
					'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
					'<span class="token string">value path</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
					'<span class="token string">color</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
				)
				'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
			'<span class="token string">scatter chart</span>' [ <span class="token operator">scatter-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label x</span>' [ <span class="token operator">axis-x:</span> ] text
				'<span class="token string">value x path</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value x property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">label y</span>' [ <span class="token operator">axis-y:</span> ] text
				'<span class="token string">value y path</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value y property</span>' [ <span class="token operator">#</span> ] reference
			'<span class="token string">bubble chart</span>' [ <span class="token operator">bubble-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">label x</span>' [ <span class="token operator">axis-x:</span> ] text
				'<span class="token string">value x path</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value x property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">label y</span>' [ <span class="token operator">axis-y:</span> ] text
				'<span class="token string">value y path</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value y property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">value z path</span>' [ <span class="token operator">size:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value z property</span>' [ <span class="token operator">#</span> ] reference
			'<span class="token string">connected scatter chart</span>' [ <span class="token operator">connected-scatter-chart</span> ]
				'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">sort path</span>' [ <span class="token operator">sort:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">sort property</span>' [ <span class="token operator">#</span> ] reference
				'<span class="token string">sort direction</span>' [ <span class="token operator">,</span> ] stategroup (
					'<span class="token string">ascending</span>' [ <span class="token operator">ascending</span> ]
					'<span class="token string">descending</span>' [ <span class="token operator">descending</span> ]
				)
				'<span class="token string">label x</span>' [ <span class="token operator">axis-x:</span> ] text
				'<span class="token string">value x path</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value x property</span>'[ <span class="token operator">#</span> ] reference
				'<span class="token string">label y</span>' [ <span class="token operator">axis-y:</span> ] text
				'<span class="token string">value y path</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value y property</span>' [ <span class="token operator">#</span> ] reference
			'<span class="token string">spider chart</span>' [ <span class="token operator">spider-chart</span> ]
				'<span class="token string">binding</span>' stategroup (
					'<span class="token string">static</span>'
						'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
							'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
							'<span class="token string">value</span>' [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
						)
						'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
						'<span class="token string">color</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
					'<span class="token string">dynamic</span>'
						'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
						'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
							'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
							'<span class="token string">value path</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
							'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
						)
						'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
				)
			'<span class="token string">radar chart</span>' [ <span class="token operator">radar-chart</span> ]
				'<span class="token string">binding</span>' stategroup (
					'<span class="token string">static</span>'
						'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
							'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
							'<span class="token string">value</span>' [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
						)
						'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
						'<span class="token string">color</span>' [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
					'<span class="token string">dynamic</span>'
						'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
						'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
							'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
							'<span class="token string">value path</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
							'<span class="token string">value property</span>' [ <span class="token operator">#</span> ] reference
						)
						'<span class="token string">has value</span>' stategroup has '<span class="token string">values</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
				)
			'<span class="token string">legend</span>' [ <span class="token operator">legend</span> ]
				'<span class="token string">binding</span>' stategroup (
					'<span class="token string">static</span>'
						'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection order '<span class="token string">order</span>' (
							'<span class="token string">has successor</span>' stategroup has successor '<span class="token string">successor</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
							'<span class="token string">color</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
						)
					'<span class="token string">dynamic</span>'
						'<span class="token string">collection</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">label path</span>' [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>' [ <span class="token operator">:</span> ] reference
				)
		)
	)
</pre>
</div>
</div>
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

{: #grammar-rule--dashboard-ui-dimension }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard ui dimension</span>'
	'<span class="token string">dimension</span>' stategroup (
		'<span class="token string">custom</span>' [ <span class="token operator">@size(</span>, <span class="token operator">)</span> ]
			'<span class="token string">x</span>' number
			'<span class="token string">y</span>' [ <span class="token operator">,</span> ] number
		'<span class="token string">default</span>'
	)
</pre>
</div>
</div>
### Widget Annotation: Margin
Allows the default margin of a widget to be changed.
All values are in pixels.

{: #grammar-rule--dashboard-ui-margin }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard ui margin</span>'
	'<span class="token string">margin</span>' stategroup (
		'<span class="token string">custom</span>' [ <span class="token operator">@margin(</span>, <span class="token operator">)</span> ]
			'<span class="token string">x1</span>' number
			'<span class="token string">x2</span>' [ <span class="token operator">,</span> ] number
			'<span class="token string">y1</span>' [ <span class="token operator">,</span> ] number
			'<span class="token string">y2</span>' [ <span class="token operator">,</span> ] number
		'<span class="token string">default</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--dashboard-ranges }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard ranges</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">green</span>' [ <span class="token operator">green</span> ]
		'<span class="token string">blue</span>' [ <span class="token operator">blue</span> ]
		'<span class="token string">orange</span>' [ <span class="token operator">orange</span> ]
		'<span class="token string">red</span>' [ <span class="token operator">red</span> ]
	)
	'<span class="token string">range size</span>' stategroup (
		'<span class="token string">static</span>'
			'<span class="token string">value</span>' number
		'<span class="token string">dynamic</span>'
			'<span class="token string">value</span>' [ <span class="token operator">#</span> ] reference
	)
	'<span class="token string">has more</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>' component <a href="#grammar-rule--dashboard-ranges">'dashboard ranges'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>
### Widget Color
Allows the selection of a color. This can either be a predefined color or a custom color.
Predefined colors are provided by the color theme.
Custom colors are not bound to the theme and can be any CSS color, for example: `#FF8000`, `rgb(100%, 50%, 0%)` and `hsl(30deg, 100%, 50%)` all specify the same shade of orange.

{: #grammar-rule--dashboard-color }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard color</span>'
	'<span class="token string">color</span>' stategroup (
		'<span class="token string">blue</span>' [ <span class="token operator">blue</span> ]
		'<span class="token string">orange</span>' [ <span class="token operator">orange</span> ]
		'<span class="token string">green</span>' [ <span class="token operator">green</span> ]
		'<span class="token string">red</span>' [ <span class="token operator">red</span> ]
		'<span class="token string">black</span>' [ <span class="token operator">black</span> ]
		'<span class="token string">grey</span>' [ <span class="token operator">grey</span> ]
		'<span class="token string">grey light</span>' [ <span class="token operator">grey</span> <span class="token operator">light</span> ]
		'<span class="token string">grey dark</span>' [ <span class="token operator">grey</span> <span class="token operator">dark</span> ]
		'<span class="token string">teal</span>' [ <span class="token operator">teal</span> ]
		'<span class="token string">purple</span>' [ <span class="token operator">purple</span> ]
		'<span class="token string">hex</span>'
			'<span class="token string">value</span>' text
	)
</pre>
</div>
</div>
### Navigation expressions

{: #grammar-rule--singular-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular path</span>'
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">group</span>'
					'<span class="token string">group</span>' [ <span class="token operator">+</span> ] reference
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--singular-path">'singular path'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--conditional-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional path</span>'
	'<span class="token string">head</span>' component <a href="#grammar-rule--singular-path">'singular path'</a>
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">state</span>'
					'<span class="token string">state group</span>' [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>' [ <span class="token operator">|</span> ] reference
			)
		'<span class="token string">tail</span>' component <a href="#grammar-rule--conditional-path">'conditional path'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--collection-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection path</span>'
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>'
			'<span class="token string">head</span>' component <a href="#grammar-rule--conditional-path">'conditional path'</a>
			'<span class="token string">collection</span>' [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>' component <a href="#grammar-rule--collection-path">'collection path'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--ancestor-entity-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor entity path</span>'
	'<span class="token string">has step</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>' component <a href="#grammar-rule--ancestor-entity-path">'ancestor entity path'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--landing-page-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">landing page path</span>'
	'<span class="token string">from</span>' stategroup (
		'<span class="token string">current</span>'
			'<span class="token string">path</span>' component <a href="#grammar-rule--ancestor-entity-path">'ancestor entity path'</a>
		'<span class="token string">user</span>' [ <span class="token operator">user</span> ]
		'<span class="token string">root</span>' [ <span class="token operator">root</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--landing-page-branches }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">landing page branches</span>'
	'<span class="token string">branch</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
	'<span class="token string">has alternative</span>' stategroup (
		'<span class="token string">yes</span>'
			'<span class="token string">alternative</span>' component <a href="#grammar-rule--landing-page-branches">'landing page branches'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--landing-page-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">landing page selector</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">group step</span>'
			'<span class="token string">group</span>' [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>' component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		'<span class="token string">state switch</span>' [ <span class="token operator">switch</span> ]
			'<span class="token string">stategroup</span>' [ <span class="token operator">.</span> ] reference
			'<span class="token string">cases</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( [ <span class="token operator">|</span> ]
				'<span class="token string">tail</span>' component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
			)
		'<span class="token string">reference step</span>'
			'<span class="token string">text</span>' [ <span class="token operator">></span> ] reference
			'<span class="token string">require</span>' stategroup (
				'<span class="token string">referencer</span>'
			)
			'<span class="token string">output</span>' stategroup (
				'<span class="token string">node</span>'
				'<span class="token string">parameter</span>'
					'<span class="token string">parameter</span>' [ <span class="token operator">$</span> ] reference
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		'<span class="token string">collection lookup</span>'
			'<span class="token string">collection</span>' [ <span class="token operator">.</span> ] reference
			'<span class="token string">require</span>' [ <span class="token operator">[</span> <span class="token operator">user</span> ] stategroup (
				'<span class="token string">key constraint</span>' [ <span class="token operator">></span> ]
					'<span class="token string">references users</span>' component <a href="#grammar-rule--collection-equality">'collection equality'</a>
				'<span class="token string">key hint</span>' [ <span class="token operator">:></span> ]
					'<span class="token string">links users</span>' component <a href="#grammar-rule--collection-equality">'collection equality'</a>
			)
			'<span class="token string">tail</span>' [ <span class="token operator">]</span> ] component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		'<span class="token string">branches</span>'
			'<span class="token string">list</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--landing-page-branches">'landing page branches'</a>
		'<span class="token string">page select</span>' [ <span class="token operator">open</span> ]
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">reports</span>' [ <span class="token operator">reports</span> ]
				'<span class="token string">todos</span>' [ <span class="token operator">todos</span> ]
				'<span class="token string">dashboard</span>' [ <span class="token operator">dashboard</span> ]
				'<span class="token string">entity view</span>' [ <span class="token operator">entity</span> ]
					'<span class="token string">entity</span>' component <a href="#grammar-rule--landing-page-path">'landing page path'</a>
				'<span class="token string">collection view</span>' [ <span class="token operator">collection</span> ]
					'<span class="token string">entity</span>' component <a href="#grammar-rule--landing-page-path">'landing page path'</a>
					'<span class="token string">requires</span>' stategroup (
						'<span class="token string">collection</span>'
					)
			)
		'<span class="token string">none</span>' [ <span class="token operator">none</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--collection-equality }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection equality</span>'
</pre>
</div>
</div>
