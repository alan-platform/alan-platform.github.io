---
layout: "doc"
origin: "datastore"
language: "consumed_interfaces_mapping"
version: "103"
type: "grammar"
url: "/pages/docs/datastore/103/consumed_interfaces_mapping/grammar.html"
toc: true
---



<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">imported interfaces</span>': [ <span class="token operator">imported-interfaces</span> ] dictionary {
	'<span class="token string">interface</span>': [ <span class="token operator">=</span> ] reference
	'<span class="token string">context keys</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">value</span>': [ <span class="token operator">=</span> ] reference
	}
	'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
}
</pre>
</div>
</div>

<div id="grammar-rule--node-type-mapping" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">type</span>': [ <span class="token operator">=></span> ] stategroup (
					'<span class="token string">internal</span>' {
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--event-mapping">'event mapping'</a>
					}
					'<span class="token string">external</span>' {
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--command-mapping">'command mapping'</a>
					}
				)
			}
			'<span class="token string">property</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">group</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
					}
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> <span class="token operator">=</span> ]
						'<span class="token string">collection</span>': [ <span class="token operator">map</span> <span class="token operator">.</span> ] reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">number</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">text</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">=</span> <span class="token operator">switch</span> ]
						'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
							'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
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

<div id="grammar-rule--parameter-mapping" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> <span class="token operator">=</span> ]
				'<span class="token string">group</span>': [ <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> <span class="token operator">=</span> ]
				'<span class="token string">collection</span>': [ <span class="token operator">map</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">number</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">text</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">=</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">state</span>' {
						'<span class="token string">state</span>': reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
					}
					'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
						'<span class="token string">state group</span>': [ <span class="token operator">@</span> <span class="token operator">.</span> ] reference
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
							'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
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

<div id="grammar-rule--event-node-type-mapping" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">event node type mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> <span class="token operator">=</span> ]
				'<span class="token string">group</span>': [ <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--event-node-type-mapping">'event node type mapping'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> <span class="token operator">=</span> ]
				'<span class="token string">collection</span>': [ <span class="token operator">map</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--event-node-type-mapping">'event node type mapping'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">number</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">text</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">=</span> ]
				'<span class="token string">state group</span>': [ <span class="token operator">switch</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
					'<span class="token string">mapping</span>': component <a href="#grammar-rule--event-node-type-mapping">'event node type mapping'</a>
				}
			}
		)
	}
}
</pre>
</div>
</div>

<div id="grammar-rule--command-mapping" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command mapping</span>' { [ <span class="token operator">execute</span> ]
	'<span class="token string">command</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
}
</pre>
</div>
</div>

<div id="grammar-rule--event-mapping" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">event mapping</span>' { [ <span class="token operator">handle</span> ]
	'<span class="token string">event</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--event-node-type-mapping">'event node type mapping'</a>
}
</pre>
</div>
</div>
