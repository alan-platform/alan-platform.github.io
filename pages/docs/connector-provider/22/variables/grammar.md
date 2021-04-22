---
layout: doc
origin: connector-provider
language: variables
version: 22
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--variables }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variables</span>': dictionary { @block [ <span class="token operator">var</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
}
</pre>
</div>
</div>
