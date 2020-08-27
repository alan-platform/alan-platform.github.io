---
layout: doc
origin: connector-consumer
language: variables
version: 9b
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--variables }
<div class="language-js highlighter-rouge">
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
