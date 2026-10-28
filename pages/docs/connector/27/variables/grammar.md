---
layout: doc
origin: connector
language: variables
version: 27
type: grammar
url: "/pages/docs/connector/27/variables/grammar.html"
toc: true
---



<div id="grammar-rule--variables" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variables</span>': dictionary { [ <span class="token operator">var</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
}
</pre>
</div>
</div>
