---
layout: "doc"
origin: "webclient"
language: "main"
version: "yar.17rc1.0"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">initial content</span>': dictionary { [ <span class="token operator">window</span> ]
	'<span class="token string">from</span>': stategroup (
		'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
		'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
	)
	'<span class="token string">expression</span>': component <a href="#grammar-rule--view-expression">'view expression'</a>
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root window</span>': [ <span class="token operator">@</span> ] reference
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">views</span>': [ <span class="token operator">from</span> ] reference
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root view</span>': [ <span class="token operator">:</span> ] reference
</pre>
</div>
</div>

{: #grammar-rule--node-equality }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node equality</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ancestor-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor node path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--view-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">view expression list</span>' {
	'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--view-expression">'view expression'</a>
	'<span class="token string">has alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--view-expression-list">'view expression list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--view-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">view expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">group step</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">expression</span>': component <a href="#grammar-rule--view-expression">'view expression'</a>
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
				'<span class="token string">expression</span>': component <a href="#grammar-rule--view-expression">'view expression'</a>
			}
		}
		'<span class="token string">reference step</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">property rule</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
				}
				'<span class="token string">context rule</span>' {
					'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] reference
				}
			)
			'<span class="token string">expression</span>': component <a href="#grammar-rule--view-expression">'view expression'</a>
		}
		'<span class="token string">collection lookup</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">references users</span>': [ <span class="token operator">[</span> <span class="token operator">user</span> <span class="token operator">></span> ] component <a href="#grammar-rule--node-equality">'node equality'</a>
			'<span class="token string">expression</span>': [ <span class="token operator">]</span> ] component <a href="#grammar-rule--view-expression">'view expression'</a>
		}
		'<span class="token string">branches</span>' {
			'<span class="token string">list</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--view-expression-list">'view expression list'</a>
		}
		'<span class="token string">view open</span>' { [ <span class="token operator">open</span> <span class="token operator">view</span> ]
			'<span class="token string">from</span>': reference
			'<span class="token string">view</span>': [ <span class="token operator">:</span> ] reference
			'<span class="token string">node</span>': [ <span class="token operator">with</span> ] stategroup (
				'<span class="token string">current</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
				}
				'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
				'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
			)
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
	)
}
</pre>
</div>
</div>
