---
layout: "doc"
origin: "auto-webclient"
language: "generator_annotations"
version: "worf.dev2"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has global dashboard</span>': stategroup (
	'<span class="token string">yes</span>' {
		'<span class="token string">dashboard</span>': [ <span class="token operator">dashboard:</span> <span class="token operator">global</span> ] component <a href="#grammar-rule--dashboard">'dashboard'</a>
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
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
'<span class="token string">dashboard</span>' {
	'<span class="token string">cell width</span>': [ <span class="token operator">(</span> ] group {
		'<span class="token string">size</span>': integer
		'<span class="token string">unit</span>': stategroup (
			'<span class="token string">pixels</span>' { [ <span class="token operator">px</span> ] }
		)
	}
	'<span class="token string">cell height</span>': [ <span class="token operator">,</span> ] group {
		'<span class="token string">size</span>': integer
		'<span class="token string">unit</span>': stategroup (
			'<span class="token string">pixels</span>' { [ <span class="token operator">px</span> ] }
		)
	}
	'<span class="token string">grid gap</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span>, <span class="token operator">)</span> ]
			'<span class="token string">size</span>': integer
			'<span class="token string">unit</span>': stategroup (
				'<span class="token string">pixels</span>' { [ <span class="token operator">px</span> ] }
			)
		}
		'<span class="token string">no</span>' { [ <span class="token operator">)</span> ] }
	)
	'<span class="token string">widgets</span>': dictionary {
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">x</span>': [ <span class="token operator">(</span> ] integer
		'<span class="token string">width</span>': [ <span class="token operator">/</span> ] integer
		'<span class="token string">y</span>': [ <span class="token operator">,</span> ] integer
		'<span class="token string">height</span>': [ <span class="token operator">/</span>, <span class="token operator">)</span> ] integer
		'<span class="token string">dimension</span>': component <a href="#grammar-rule--dashboard-ui-dimension">'dashboard ui dimension'</a>
		'<span class="token string">margin</span>': component <a href="#grammar-rule--dashboard-ui-margin">'dashboard ui margin'</a>
		'<span class="token string">context path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
		'<span class="token string">graph type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">value</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">size</span>': stategroup (
					'<span class="token string">large</span>' { }
					'<span class="token string">fixed</span>' { [ <span class="token operator">size:</span> ]
						'<span class="token string">number size</span>': stategroup (
							'<span class="token string">large</span>' { }
							'<span class="token string">fixed</span>' {
								'<span class="token string">value</span>': integer
							}
						)
						'<span class="token string">unit size</span>': stategroup (
							'<span class="token string">auto</span>' { }
							'<span class="token string">fixed</span>' { [ <span class="token operator">,</span> ]
								'<span class="token string">value</span>': integer
							}
						)
					}
				)
			}
			'<span class="token string">range</span>' {
				'<span class="token string">chart type</span>': stategroup (
					'<span class="token string">progress bar</span>' { [ <span class="token operator">progress</span> ] }
					'<span class="token string">gauge</span>' { [ <span class="token operator">gauge</span> ] }
				)
				'<span class="token string">range start</span>': [ <span class="token operator">ranges:</span> ] stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">value</span>': integer
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">value</span>': [ <span class="token operator">#</span> ] reference
					}
				)
				'<span class="token string">ranges</span>': component <a href="#grammar-rule--dashboard-ranges">'dashboard ranges'</a>
				'<span class="token string">value</span>': [ <span class="token operator">value:</span> <span class="token operator">#</span> ] reference
			}
			'<span class="token string">pie chart</span>' { [ <span class="token operator">pie-chart</span> ]
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
							'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">limit</span>': stategroup (
							'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
								'<span class="token string">max entries</span>': integer
							}
							'<span class="token string">default</span>' { }
						)
						'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
						'<span class="token string">value path</span>': [ <span class="token operator">value:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
						'<span class="token string">merge small slices</span>': stategroup (
							'<span class="token string">yes</span>' { [ <span class="token operator">merge</span> ]
								'<span class="token string">below percentage</span>': [ <span class="token operator">below</span>, <span class="token operator">%</span> ] integer
							}
							'<span class="token string">no</span>' { }
						)
					}
				)
				'<span class="token string">sorting</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>': stategroup (
							'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
							'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">bar chart</span>' { [ <span class="token operator">bar-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
							'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">limit</span>': stategroup (
							'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
								'<span class="token string">max entries</span>': integer
							}
							'<span class="token string">default</span>' { }
						)
						'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
						'<span class="token string">value path</span>': [ <span class="token operator">value:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
					}
				)
				'<span class="token string">sorting</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>': stategroup (
							'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
							'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">grouped bar chart</span>' { [ <span class="token operator">grouped-bar-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">limit</span>': stategroup (
					'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
						'<span class="token string">max entries</span>': integer
					}
					'<span class="token string">default</span>' { }
				)
				'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
				'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">has successor</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">value path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
					'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
				}
				'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
					| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
					| none  = '<span class="token string">no</span>'
				)
				'<span class="token string">sorting</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>': stategroup (
							'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
							'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
						)
						'<span class="token string">axis</span>': stategroup (
							'<span class="token string">single</span>' {
								'<span class="token string">axis</span>': reference
							}
							'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">stacked bar chart</span>' { [ <span class="token operator">stacked-bar-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">limit</span>': stategroup (
					'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
						'<span class="token string">max entries</span>': integer
					}
					'<span class="token string">default</span>' { }
				)
				'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
				'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">has successor</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">value path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
					'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
				}
				'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
					| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
					| none  = '<span class="token string">no</span>'
				)
				'<span class="token string">sorting</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">sort:</span> ]
						'<span class="token string">direction</span>': stategroup (
							'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
							'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
						)
						'<span class="token string">axis</span>': stategroup (
							'<span class="token string">single</span>' {
								'<span class="token string">axis</span>': reference
							}
							'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">line chart</span>' { [ <span class="token operator">line-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
						'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">limit</span>': stategroup (
							'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
								'<span class="token string">max entries</span>': integer
							}
							'<span class="token string">default</span>' { }
						)
						'<span class="token string">sort path</span>': [ <span class="token operator">sort:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">sort property</span>': [ <span class="token operator">#</span> ] reference
						'<span class="token string">sort direction</span>': [ <span class="token operator">,</span> ] stategroup (
							'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
							'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
						)
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
							'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
							'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
					}
				)
			}
			'<span class="token string">area chart</span>' { [ <span class="token operator">area-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
						'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">limit</span>': stategroup (
							'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
								'<span class="token string">max entries</span>': integer
							}
							'<span class="token string">default</span>' { }
						)
						'<span class="token string">sort path</span>': [ <span class="token operator">sort:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">sort property</span>': [ <span class="token operator">#</span> ] reference
						'<span class="token string">sort direction</span>': [ <span class="token operator">,</span> ] stategroup (
							'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
							'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
						)
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
							'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
							'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
					}
				)
			}
			'<span class="token string">scatter chart</span>' { [ <span class="token operator">scatter-chart</span> ]
				'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">limit</span>': stategroup (
					'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
						'<span class="token string">max entries</span>': integer
					}
					'<span class="token string">default</span>' { }
				)
				'<span class="token string">label x</span>': [ <span class="token operator">axis-x:</span> ] text
				'<span class="token string">value x path</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value x property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis x</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">label y</span>': [ <span class="token operator">axis-y:</span> ] text
				'<span class="token string">value y path</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value y property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis y</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
			}
			'<span class="token string">bubble chart</span>' { [ <span class="token operator">bubble-chart</span> ]
				'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">limit</span>': stategroup (
					'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
						'<span class="token string">max entries</span>': integer
					}
					'<span class="token string">default</span>' { }
				)
				'<span class="token string">label x</span>': [ <span class="token operator">axis-x:</span> ] text
				'<span class="token string">value x path</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value x property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis x</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">label y</span>': [ <span class="token operator">axis-y:</span> ] text
				'<span class="token string">value y path</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value y property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis y</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">value z path</span>': [ <span class="token operator">size:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value z property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis z</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
			}
			'<span class="token string">connected scatter chart</span>' { [ <span class="token operator">connected-scatter-chart</span> ]
				'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
				'<span class="token string">limit</span>': stategroup (
					'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
						'<span class="token string">max entries</span>': integer
					}
					'<span class="token string">default</span>' { }
				)
				'<span class="token string">sort path</span>': [ <span class="token operator">sort:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">sort property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">sort direction</span>': [ <span class="token operator">,</span> ] stategroup (
					'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
					'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
				)
				'<span class="token string">label x</span>': [ <span class="token operator">axis-x:</span> ] text
				'<span class="token string">value x path</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value x property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis x</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">label y</span>': [ <span class="token operator">axis-y:</span> ] text
				'<span class="token string">value y path</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">value y property</span>': [ <span class="token operator">#</span> ] reference
				'<span class="token string">axis y</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
			}
			'<span class="token string">spider chart</span>' { [ <span class="token operator">spider-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
						'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">limit</span>': stategroup (
							'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
								'<span class="token string">max entries</span>': integer
							}
							'<span class="token string">default</span>' { }
						)
						'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
							'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
					}
				)
			}
			'<span class="token string">radar chart</span>' { [ <span class="token operator">radar-chart</span> ]
				'<span class="token string">axis</span>': component <a href="#grammar-rule--dashboard-axis-range">'dashboard axis range'</a>
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">#</span> ] reference
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
						'<span class="token string">color</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">limit</span>': stategroup (
							'<span class="token string">custom</span>' { [ <span class="token operator">limit:</span> ]
								'<span class="token string">max entries</span>': integer
							}
							'<span class="token string">default</span>' { }
						)
						'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">value path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
							'<span class="token string">value property</span>': [ <span class="token operator">#</span> ] reference
						}
						'<span class="token string">has value</span>': stategroup = node-switch .'<span class="token string">values</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
					}
				)
			}
			'<span class="token string">legend</span>' { [ <span class="token operator">legend</span> ]
				'<span class="token string">binding</span>': stategroup (
					'<span class="token string">static</span>' {
						'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">color</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--dashboard-color">'dashboard color'</a>
						}
					}
					'<span class="token string">dynamic</span>' {
						'<span class="token string">collection</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">label path</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">label property</span>': [ <span class="token operator">:</span> ] reference
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>
#### Widget: integer
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
As pie charts can not show non-existing (value = 0) or negative values, it can only plot positive numbers.
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
#### Widget: Area Chart
Displays an area chart. It creates a single line for each value and fills the area between the line and 0 on the y-axis. Every entry in the query result adds a point to the line.
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
'<span class="token string">dashboard ui dimension</span>' {
	'<span class="token string">dimension</span>': stategroup (
		'<span class="token string">custom</span>' { [ <span class="token operator">@size(</span>, <span class="token operator">)</span> ]
			'<span class="token string">x</span>': integer
			'<span class="token string">y</span>': [ <span class="token operator">,</span> ] integer
		}
		'<span class="token string">default</span>' { }
	)
}
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
'<span class="token string">dashboard ui margin</span>' {
	'<span class="token string">margin</span>': stategroup (
		'<span class="token string">custom</span>' { [ <span class="token operator">@margin(</span>, <span class="token operator">)</span> ]
			'<span class="token string">x1</span>': integer
			'<span class="token string">x2</span>': [ <span class="token operator">,</span> ] integer
			'<span class="token string">y1</span>': [ <span class="token operator">,</span> ] integer
			'<span class="token string">y2</span>': [ <span class="token operator">,</span> ] integer
		}
		'<span class="token string">default</span>' { }
	)
}
</pre>
</div>
</div>
### Widget Annotations: Axis Range
Allows the range of any axis to be changed.
By default the axis range is dynamically calculated based on the data.
When providing a hint, the provided value is guaranteed to be on axis, but the range might be increased beyond the hint to prevent data from going out of bounds of the axis.
A static axis ignores all data and while always have the exact range as provided.

{: #grammar-rule--dashboard-axis-range }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard axis range</span>' {
	'<span class="token string">custom range</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">@range(</span>, <span class="token operator">)</span> ]
			'<span class="token string">min anchor</span>': stategroup (
				'<span class="token string">static</span>' { [ <span class="token operator">force</span> ]
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">hint</span>' {
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">dynamic</span>' { }
			)
			'<span class="token string">max anchor</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">static</span>' { [ <span class="token operator">force</span> ]
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">hint</span>' {
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">dynamic</span>' { }
			)
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--dashboard-ranges }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dashboard ranges</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">green</span>' { [ <span class="token operator">green</span> ] }
		'<span class="token string">blue</span>' { [ <span class="token operator">blue</span> ] }
		'<span class="token string">orange</span>' { [ <span class="token operator">orange</span> ] }
		'<span class="token string">red</span>' { [ <span class="token operator">red</span> ] }
	)
	'<span class="token string">range size</span>': stategroup (
		'<span class="token string">static</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">value</span>': [ <span class="token operator">#</span> ] reference
		}
	)
	'<span class="token string">has more</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--dashboard-ranges">'dashboard ranges'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
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
'<span class="token string">dashboard color</span>' {
	'<span class="token string">color</span>': stategroup (
		'<span class="token string">blue</span>' { [ <span class="token operator">blue</span> ] }
		'<span class="token string">orange</span>' { [ <span class="token operator">orange</span> ] }
		'<span class="token string">green</span>' { [ <span class="token operator">green</span> ] }
		'<span class="token string">red</span>' { [ <span class="token operator">red</span> ] }
		'<span class="token string">black</span>' { [ <span class="token operator">black</span> ] }
		'<span class="token string">grey</span>' { [ <span class="token operator">grey</span> ] }
		'<span class="token string">grey light</span>' { [ <span class="token operator">grey</span> <span class="token operator">light</span> ] }
		'<span class="token string">grey dark</span>' { [ <span class="token operator">grey</span> <span class="token operator">dark</span> ] }
		'<span class="token string">teal</span>' { [ <span class="token operator">teal</span> ] }
		'<span class="token string">purple</span>' { [ <span class="token operator">purple</span> ] }
		'<span class="token string">hex</span>' {
			'<span class="token string">value</span>': text
		}
	)
}
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

{: #grammar-rule--extended-annotations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">extended annotations</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">has inline dashboards</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">inline dashboards</span>': dictionary { [ <span class="token operator">dashboard:</span> ]
				'<span class="token string">has more inline dashboards</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next inline dashboard</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">dashboard</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--dashboard">'dashboard'</a>
			}
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
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
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
					'<span class="token string">list</span>' { [ <span class="token operator">@list</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">has custom queries</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">custom queries</span>': dictionary { [ <span class="token operator">query</span> ]
							'<span class="token string">has more queries</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">next query</span>' = successor }
								| none = '<span class="token string">no</span>'
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
											'<span class="token string">no</span>' { }
										)
									}
									'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
										'<span class="token string">property</span>': reference
										'<span class="token string">filter</span>': stategroup (
											'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
												'<span class="token string">criteria</span>': text
											}
											'<span class="token string">no</span>' { }
										)
									}
									'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
										'<span class="token string">property</span>': reference
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
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">sub tree</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
				'<span class="token string">states</span>': dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
				}
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
		)
	}
}
</pre>
</div>
</div>

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
			'<span class="token string">header</span>': stategroup (
				'<span class="token string">yes</span>' { }
				'<span class="token string">no</span>' { [ <span class="token operator">@no-header</span> ] }
			)
			'<span class="token string">layout</span>': stategroup (
				'<span class="token string">set</span>' { [ <span class="token operator">@layout:</span> ]
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">tabular</span>' { [ <span class="token operator">tabular</span> ] }
						'<span class="token string">cards</span>' { [ <span class="token operator">cards</span> ] }
					)
				}
				'<span class="token string">default</span>' { }
			)
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
				'<span class="token string">states</span>': dictionary { [ <span class="token operator">|</span> ]
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
				'<span class="token string">binding</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">custom</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">title</span>': reference
				}
				'<span class="token string">default</span>' { }
			)
		}
	)
}
</pre>
</div>
</div>
