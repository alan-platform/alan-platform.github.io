---
layout: "doc"
origin: "webclient"
language: "query"
version: "yar.13rc11.2"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">query type</span>': stategroup (
	'<span class="token string">collection</span>' {
		'<span class="token string">context node path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">collection path</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-selector">'collection selector'</a>
		'<span class="token string">properties</span>': [ <span class="token operator">select</span> ] dictionary {
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
					'<span class="token string">value</span>': component <a href="#grammar-rule--collection-expression">'collection expression'</a>
					'<span class="token string">format</span>': component <a href="#grammar-rule--collection-format">'collection format'</a>
				}
				'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
					'<span class="token string">value</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
					'<span class="token string">format</span>': component <a href="#grammar-rule--number-format">'number format'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
					'<span class="token string">value</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
					'<span class="token string">format</span>': component <a href="#grammar-rule--text-format">'text format'</a>
				}
				'<span class="token string">stategroup</span>' { [ <span class="token operator">state</span> ]
					'<span class="token string">value</span>': component <a href="#grammar-rule--stategroup-expression">'stategroup expression'</a>
					'<span class="token string">format</span>': component <a href="#grammar-rule--state-format">'state format'</a>
				}
			)
		}
		'<span class="token string">has first</span>': stategroup = node-switch .'<span class="token string">properties</span>' (
			| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
			| none  = '<span class="token string">no</span>'
		)
		'<span class="token string">filters</span>': [ <span class="token operator">where</span> ] group {
			'<span class="token string">todo filter</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">has-todo</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">filters</span>': set {
				'<span class="token string">path</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--node-path">'node path'</a>
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">property</span>' {
						'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">number</span>' {
								'<span class="token string">expression</span>': component <a href="#grammar-rule--number-filter-expression">'number filter expression'</a>
							}
							'<span class="token string">state group</span>' { [ <span class="token operator">in</span> ]
								'<span class="token string">states to include</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">?</span> ] }
							}
						)
					}
					'<span class="token string">node</span>' {
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">existence</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">exists</span>' { [ <span class="token operator">exists</span> ] }
									'<span class="token string">not exists</span>' { [ <span class="token operator">not</span> <span class="token operator">exists</span> ] }
								)
							}
							'<span class="token string">containment</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
									'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
								)
								'<span class="token string">references</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--reference-filter-list">'reference filter list'</a>
							}
						)
					}
				)
			}
		}
		'<span class="token string">record limit</span>': [ <span class="token operator">limit</span> ] component <a href="#grammar-rule--number-value">'number value'</a>
	}
	'<span class="token string">graph</span>' {
		'<span class="token string">context selection</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">entry points</span>': group {
			'<span class="token string">collection selection</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-selector">'collection selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">graph</span>': [ <span class="token operator">flatten</span> ] reference
		}
		'<span class="token string">query</span>': group {
			'<span class="token string">collection selection</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-selector">'collection selector'</a>
			'<span class="token string">properties</span>': [ <span class="token operator">select</span> ] dictionary {
				'<span class="token string">has next</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--node-path">'node path'</a>
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">number</span>' { [ <span class="token operator">#</span> ]
						'<span class="token string">number</span>': reference
						'<span class="token string">format</span>': component <a href="#grammar-rule--number-format">'number format'</a>
					}
					'<span class="token string">text</span>' { [ <span class="token operator">.</span> ]
						'<span class="token string">text</span>': reference
						'<span class="token string">format</span>': component <a href="#grammar-rule--text-format">'text format'</a>
					}
					'<span class="token string">stategroup</span>' { [ <span class="token operator">?</span> ]
						'<span class="token string">state group</span>': reference
						'<span class="token string">format</span>': component <a href="#grammar-rule--state-format">'state format'</a>
					}
				)
			}
			'<span class="token string">has first</span>': stategroup = node-switch .'<span class="token string">properties</span>' (
				| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
				| none  = '<span class="token string">no</span>'
			)
		}
	}
)
</pre>
</div>
</div>

{: #grammar-rule--id-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">id path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">collection entry</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">attribute</span>': reference
					'<span class="token string">entry id</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--text-value">'text value'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--id-path">'id path'</a>
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
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">state rule</span>' { [ <span class="token operator">.&</span> ]
					'<span class="token string">rule</span>': reference
				}
				'<span class="token string">reference rule</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">collection entry</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">entry key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] text
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path">'node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--entity-descendant-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity descendant selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--entity-descendant-selector">'entity descendant selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--entity-descendant-selector">'entity descendant selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-selector">'collection selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">property</span>' {
			'<span class="token string">node selection</span>': component <a href="#grammar-rule--node-path">'node path'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">property</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection format</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">join</span>' { [ <span class="token operator">join</span> ]
			'<span class="token string">separator</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--text-value">'text value'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number value</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">static</span>' {
			'<span class="token string">value</span>': integer
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">value</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--number-value">'number value'</a>
		}
		'<span class="token string">property</span>' {
			'<span class="token string">node selection</span>': component <a href="#grammar-rule--node-path">'node path'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">:</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number format</span>' {
	'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
		'<span class="token string">date</span>' { [ <span class="token operator">date</span> ] }
		'<span class="token string">time</span>' { [ <span class="token operator">time</span> ] }
		'<span class="token string">datetime</span>' { [ <span class="token operator">datetime</span> ] }
		'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
			'<span class="token string">shift</span>': integer
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text value</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">static</span>' {
			'<span class="token string">value</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">value</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--text-value">'text value'</a>
		}
		'<span class="token string">property</span>' {
			'<span class="token string">node selection</span>': component <a href="#grammar-rule--node-path">'node path'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">:</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text format</span>' {
	'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--stategroup-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stategroup expression</span>' {
	'<span class="token string">node selection</span>': component <a href="#grammar-rule--node-path">'node path'</a>
	'<span class="token string">attribute</span>': [ <span class="token operator">:</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--state-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state format</span>' {
	'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-filter-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number filter expression</span>' {
	'<span class="token string">operator</span>': stategroup (
		'<span class="token string">range</span>' {
			'<span class="token string">greater than</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">></span> ]
					'<span class="token string">criterium</span>': component <a href="#grammar-rule--number-value">'number value'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">less than</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator"><</span> ]
					'<span class="token string">criterium</span>': component <a href="#grammar-rule--number-value">'number value'</a>
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">equals</span>' { [ <span class="token operator">==</span> ]
			'<span class="token string">criterium</span>': component <a href="#grammar-rule--number-value">'number value'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--reference-filter-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference filter list</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
		'<span class="token string">query context</span>' { }
	)
	'<span class="token string">referenced node</span>': component <a href="#grammar-rule--id-path">'id path'</a>
	'<span class="token string">has alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">alternative</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--reference-filter-list">'reference filter list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
