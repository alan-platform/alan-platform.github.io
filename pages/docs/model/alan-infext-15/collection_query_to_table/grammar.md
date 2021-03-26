---
layout: doc
origin: model
language: collection_query_to_table
version: alan-infext-15
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type</span>': stategroup (
	'<span class="token string">collection query</span>' { [ <span class="token operator">collection</span> <span class="token operator">query</span> ]
		'<span class="token string">columns</span>': component <a href="#grammar-rule--collection-block">'collection block'</a>
	}
	'<span class="token string">acyclic graph list query</span>' { [ <span class="token operator">graph</span> <span class="token operator">query</span> ]
		'<span class="token string">columns</span>': component <a href="#grammar-rule--list-block">'list block'</a>
	}
)
</pre>
</div>
</div>

{: #grammar-rule--collection-block }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection block</span>' {
	'<span class="token string">has columns</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">header</span>': text
			'<span class="token string">property</span>': [ <span class="token operator">-></span> <span class="token operator">select</span> ] reference
			'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
				'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
				'<span class="token string">state</span>' { [ <span class="token operator">state</span> ] }
				'<span class="token string">date</span>' { [ <span class="token operator">date</span> ] }
				'<span class="token string">time</span>' { [ <span class="token operator">time</span> ] }
				'<span class="token string">datetime</span>' { [ <span class="token operator">datetime</span> ] }
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">shift</span>': integer
				}
			)
			'<span class="token string">next</span>': component <a href="#grammar-rule--collection-block">'collection block'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--list-block }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">list block</span>' {
	'<span class="token string">has columns</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">header</span>': text
			'<span class="token string">property</span>': [ <span class="token operator">-></span> <span class="token operator">select</span> ] reference
			'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
				'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
				'<span class="token string">state</span>' { [ <span class="token operator">state</span> ] }
				'<span class="token string">date</span>' { [ <span class="token operator">date</span> ] }
				'<span class="token string">time</span>' { [ <span class="token operator">time</span> ] }
				'<span class="token string">datetime</span>' { [ <span class="token operator">datetime</span> ] }
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">shift</span>': integer
				}
			)
			'<span class="token string">next</span>': component <a href="#grammar-rule--list-block">'list block'</a>
		}
	)
}
</pre>
</div>
</div>
