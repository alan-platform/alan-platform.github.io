---
layout: "doc"
origin: "datastore"
language: "regular_expression_engine"
version: "115"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library</span>': dictionary { [ <span class="token operator">regexp</span> ]
	'<span class="token string">captures</span>': dictionary { [ <span class="token operator">@</span> ]
		'<span class="token string">next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">pieces</span>': component <a href="#grammar-rule--pieces">'pieces'</a>
	}
	'<span class="token string">first</span>': reference = first
}
</pre>
</div>
</div>

{: #grammar-rule--match-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">match list</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">code point</span>' {
			'<span class="token string">value</span>': text
		}
		'<span class="token string">code point range</span>' {
			'<span class="token string">begin value</span>': text
			'<span class="token string">end value</span>': [ <span class="token operator">-</span> ] text
		}
	)
	'<span class="token string">tail</span>': stategroup (
		'<span class="token string">list</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--match-list">'match list'</a>
		}
		'<span class="token string">none</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--bracket-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">bracket expression</span>' { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
	'<span class="token string">match type</span>': stategroup (
		'<span class="token string">match</span>' { }
		'<span class="token string">mismatch</span>' { [ <span class="token operator">^</span> ] }
	)
	'<span class="token string">list</span>': component <a href="#grammar-rule--match-list">'match list'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--atom }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">atom</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">bracket expression</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--bracket-expression">'bracket expression'</a>
		}
		'<span class="token string">any code point</span>' { [ <span class="token operator">.</span> ] }
		'<span class="token string">code point</span>' {
			'<span class="token string">value</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--atom-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">atom list</span>' {
	'<span class="token string">atom</span>': component <a href="#grammar-rule--atom">'atom'</a>
	'<span class="token string">tail</span>': stategroup (
		'<span class="token string">list</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--atom-list">'atom list'</a>
		}
		'<span class="token string">none</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--piece }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">piece</span>' {
	'<span class="token string">capture</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">atoms</span>': component <a href="#grammar-rule--atom-list">'atom list'</a>
		}
		'<span class="token string">no</span>' {
			'<span class="token string">atom</span>': component <a href="#grammar-rule--atom">'atom'</a>
		}
	)
	'<span class="token string">repeat</span>': stategroup (
		'<span class="token string">once</span>' { }
		'<span class="token string">wild card</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">optional</span>' { [ <span class="token operator">?</span> ] }
				'<span class="token string">repeater</span>' {
					'<span class="token string">allow no match</span>': stategroup (
						'<span class="token string">yes</span>' { [ <span class="token operator">*</span> ] }
						'<span class="token string">no</span>' { [ <span class="token operator">+</span> ] }
					)
				}
			)
		}
		'<span class="token string">bound</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
			'<span class="token string">min</span>': integer
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">exact</span>' { }
				'<span class="token string">range</span>' { [ <span class="token operator">,</span> ]
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">unlimited</span>' { }
						'<span class="token string">limited</span>' {
							'<span class="token string">max</span>': integer
						}
					)
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--pieces }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">pieces</span>' {
	'<span class="token string">piece</span>': component <a href="#grammar-rule--piece">'piece'</a>
	'<span class="token string">tail</span>': stategroup (
		'<span class="token string">list</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--pieces">'pieces'</a>
		}
		'<span class="token string">none</span>' { }
	)
}
</pre>
</div>
</div>
