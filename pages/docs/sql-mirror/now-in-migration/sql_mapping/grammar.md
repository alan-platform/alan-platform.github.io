---
layout: "doc"
origin: "sql-mirror"
language: "sql_mapping"
version: "now-in-migration"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">formatting</span>': group {
	'<span class="token string">identifier wrapping</span>': [ <span class="token operator">identifier-delimiter:</span> ] group {
		'<span class="token string">open</span>': text
		'<span class="token string">close</span>': text
	}
	'<span class="token string">data type mapping</span>': [ <span class="token operator">data-types</span> ] group {
		'<span class="token string">key</span>': [ <span class="token operator">key:</span> ] text
		'<span class="token string">text</span>': [ <span class="token operator">text:</span> ] text
		'<span class="token string">number</span>': [ <span class="token operator">number:</span> ] text
		'<span class="token string">date</span>': [ <span class="token operator">date:</span> ] text
		'<span class="token string">date-time</span>': [ <span class="token operator">date-time:</span> ] text
		'<span class="token string">state</span>': [ <span class="token operator">state:</span> ] text
	}
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">tables</span>': [ <span class="token operator">schema</span> ] dictionary {
	'<span class="token string">primary key</span>': [ <span class="token operator"><--</span> ] group {
		'<span class="token string">root key field</span>': stategroup (
			'<span class="token string">no</span>' {
				'<span class="token string">entity type path</span>': component <a href="#grammar-rule--entity-type-path">'entity type path'</a>
			}
			'<span class="token string">yes</span>' {
				'<span class="token string">root key</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] text
			}
		)
		'<span class="token string">key fields</span>': dictionary { [ <span class="token operator">[</span> ]
			'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">predecessor</span>' = predecessor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">has successor</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">has tail</span>': [ <span class="token operator">]</span> ] stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' {
					'<span class="token string">entity type path</span>': component <a href="#grammar-rule--entity-type-path">'entity type path'</a>
				}
			)
		}
		'<span class="token string">has key fields</span>': stategroup = node-switch .'<span class="token string">key fields</span>' (
			| nodes = '<span class="token string">yes</span>' {
				'<span class="token string">first</span>' = first
				'<span class="token string">last</span>' = last
			}
			| none  = '<span class="token string">no</span>'
		)
	}
	'<span class="token string">fields</span>': [ <span class="token operator">{</span>, <span class="token operator">}</span> ] dictionary {
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">text</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">key</span>' {
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">primary key</span>' { [ <span class="token operator">primary-key</span> ] }
							'<span class="token string">foreign key</span>' { [ <span class="token operator">foreign-key</span> ] }
						)
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">text</span> ] }
				)
			}
			'<span class="token string">number</span>' {
				'<span class="token string">representation</span>': stategroup (
					'<span class="token string">decimal</span>' { [ <span class="token operator">number</span> ] }
					'<span class="token string">date</span>' { [ <span class="token operator">date</span> ] }
					'<span class="token string">date and time</span>' { [ <span class="token operator">date-time</span> ] }
				)
			}
			'<span class="token string">state</span>' { [ <span class="token operator">state</span> ]
				'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
			}
		)
	}
	'<span class="token string">has fields</span>': stategroup = node-switch .'<span class="token string">fields</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root table</span>': [ <span class="token operator">mapping</span> <span class="token operator">root</span> ] component <a href="#grammar-rule--optional-table-selection">'optional table selection'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">mapping</span>': component <a href="#grammar-rule--mapping-definition">'mapping definition'</a>
</pre>
</div>
</div>

{: #grammar-rule--entity-scoped-node-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity scoped node type path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' { }
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--entity-scoped-node-type-path">'entity scoped node type path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--entity-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity type path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--entity-scoped-node-type-path">'entity scoped node type path'</a>
	'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--table-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">table selection</span>' {
	'<span class="token string">table</span>': [ <span class="token operator">--></span> <span class="token operator">table</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--optional-table-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional table selection</span>' {
	'<span class="token string">select table</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">table</span>': component <a href="#grammar-rule--table-selection">'table selection'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--mapping-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">mapping definition</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">include</span>': stategroup (
			'<span class="token string">no</span>' { [ <span class="token operator">(ignore)</span> ] }
			'<span class="token string">yes</span>' {
				'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">field</span>': [ <span class="token operator">--></span> ] reference
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">field</span>': [ <span class="token operator">--></span> ] reference
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">token field</span>': [ <span class="token operator">--></span> ] reference
						'<span class="token string">extension field</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						// '<span class="token string">optional table</span>' component <a href="#grammar-rule--optional-table-selection">'optional table selection'</a>
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--mapping-definition">'mapping definition'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">state group to field mapping</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">--></span> ]
								'<span class="token string">field</span>': reference // reference !&'<span class="token string">table</span>'.'<span class="token string">fields</span>'
							}
						)
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">state to state value mapping</span>': stategroup (
								'<span class="token string">no</span>' { }
								'<span class="token string">yes</span>' { [ <span class="token operator">--></span> ]
									'<span class="token string">value</span>': reference
								}
							)
							// '<span class="token string">optional table</span>' component <a href="#grammar-rule--optional-table-selection">'optional table selection'</a>
							'<span class="token string">mapping</span>': component <a href="#grammar-rule--mapping-definition">'mapping definition'</a>
						}
					}
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">table</span>': component <a href="#grammar-rule--table-selection">'table selection'</a>
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--mapping-definition">'mapping definition'</a>
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>
