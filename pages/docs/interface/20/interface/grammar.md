---
layout: doc
origin: interface
language: interface
version: 20
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--context-keys }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context keys</span>': @section [ <span class="token operator">root</span> ] indent dictionary { @block }
</pre>
</div>
</div>

{: #grammar-rule--root }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': component <a href="#grammar-rule--node">'node'</a>
</pre>
</div>
</div>

{: #grammar-rule--numerical-types }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">numerical types</span>': @section [ <span class="token operator">numerical-types</span> ] indent dictionary { @block }
</pre>
</div>
</div>

{: #grammar-rule--node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ] indent
	'<span class="token string">attributes</span>': dictionary { @block
		'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">attribute</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--node">'node'</a>
			}
			'<span class="token string">event</span>' { [ <span class="token operator">event</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--node">'node'</a>
			}
			'<span class="token string">property</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">has constraint</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' {
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">existing</span>' { }
									'<span class="token string">nonexisting</span>' { [ <span class="token operator">new</span> ] }
								)
								'<span class="token string">referencer</span>': component <a href="#grammar-rule--referencer">'referencer'</a>
							}
						)
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">type</span>': component <a href="#grammar-rule--number-type">'number type'</a>
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ] }
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">dense map</span>' { [ <span class="token operator">dense-map</span> ] }
							'<span class="token string">simple</span>' { }
						)
						'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
						'<span class="token string">graphs</span>': component <a href="#grammar-rule--graphs-definition">'graphs definition'</a>
						'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
					}
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
							'<span class="token string">context rules</span>': @list indent component <a href="#grammar-rule--where-clause">'where clause'</a>
							'<span class="token string">node</span>': @raw component <a href="#grammar-rule--node">'node'</a>
						}
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--number-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number type</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">unbounded</span>' { }
		'<span class="token string">bounded</span>' {
			'<span class="token string">invert sign</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">non</span> ] }
			)
			'<span class="token string">sign</span>': stategroup (
				'<span class="token string">positive</span>' { [ <span class="token operator">positive</span> ] }
				'<span class="token string">negative</span>' { [ <span class="token operator">negative</span> ] }
				'<span class="token string">zero</span>' { [ <span class="token operator">zero</span> ] }
			)
		}
	)
	'<span class="token string">numerical type</span>': reference
	'<span class="token string">decimal places</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">decimals:</span> ]
			'<span class="token string">places</span>': integer
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--optional-evaluation-annotation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional evaluation annotation</span>' {
	'<span class="token string">phase</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">downstream</span>' { [ <span class="token operator">downstream</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--explicit-evaluation-annotation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">explicit evaluation annotation</span>' {
	'<span class="token string">phase</span>': stategroup (
		'<span class="token string">upstream</span>' { }
		'<span class="token string">downstream</span>' { [ <span class="token operator">downstream</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--referencer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">referencer</span>' { [ <span class="token operator">-></span> ]
	'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
	'<span class="token string">path</span>': group {
		'<span class="token string">head</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
		'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
	}
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">unrestricted</span>' {
			'<span class="token string">collection step</span>': [ <span class="token operator">.</span>,'<span class="token string">[ ]</span>'] component <a href="#grammar-rule--property-step">'property step'</a>
		}
		'<span class="token string">sibling</span>' { [ <span class="token operator">sibling</span> ]
			'<span class="token string">graph participation</span>': stategroup (
				'<span class="token string">no</span>' {
					'<span class="token string">support self reference</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">||</span> <span class="token operator">self</span> ] }
					)
				}
				'<span class="token string">yes</span>' { [ <span class="token operator">in</span> ]
					'<span class="token string">graphs</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
				}
			)
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
	'<span class="token string">rules</span>': @block indent component <a href="#grammar-rule--where-clause">'where clause'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--where-clause }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">where clause</span>' {
	'<span class="token string">has rule</span>': stategroup = node-switch .'<span class="token string">rules</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">rules</span>': dictionary @tabular { @block [ <span class="token operator">where</span> ]
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">rule</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">evaluation</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--optional-evaluation-annotation">'optional evaluation annotation'</a>
		'<span class="token string">context</span>': stategroup (
			'<span class="token string">sibling rule</span>' {
				'<span class="token string">rule</span>': reference
			}
			'<span class="token string">context</span>' {
				'<span class="token string">path</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
			}
		)
		'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--graphs-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">graphs definition</span>' { indent
	'<span class="token string">graphs</span>': dictionary { @block
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">acyclic</span>' { [ <span class="token operator">acyclic-graph</span> ] }
			'<span class="token string">ordered</span>' { [ <span class="token operator">ordered-graph</span> ]
				'<span class="token string">path</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
				'<span class="token string">ordering property</span>': [ <span class="token operator">></span> ] reference
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--property-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">property step</span>' {
	'<span class="token string">property</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--reference-property-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference property step</span>' {
	'<span class="token string">property</span>': component <a href="#grammar-rule--property-step">'property step'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--node-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node path tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">group</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">group step</span>': component <a href="#grammar-rule--property-step">'property step'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group step</span>': [ <span class="token operator">.</span> ] component <a href="#grammar-rule--property-step">'property step'</a>
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">reference</span>' { [ <span class="token operator">></span> ]
					'<span class="token string">reference</span>': component <a href="#grammar-rule--reference-property-step">'reference property step'</a>
				}
				'<span class="token string">reference rule</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">.</span> ] component <a href="#grammar-rule--reference-property-step">'reference property step'</a>
					'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
				}
				'<span class="token string">state context rule</span>' { [ <span class="token operator">.&</span> ]
					'<span class="token string">context rule</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--context-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context node path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this dataset node</span>' { }
		'<span class="token string">this parameter node</span>' { [ <span class="token operator">@</span> ] }
		'<span class="token string">dataset root</span>' { [ <span class="token operator">root</span> ] }
		'<span class="token string">expression context</span>' { [ <span class="token operator">$</span> ] }
	)
}
</pre>
</div>
</div>
