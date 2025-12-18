---
layout: "doc"
origin: "connector"
language: "variables"
version: "38"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variables</span>': dictionary { [ <span class="token operator">var</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
	'<span class="token string">secret</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">secret</span> ] }
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has variables</span>': stategroup = node-switch .'<span class="token string">variables</span>' (
	| nodes = '<span class="token string">yes</span>' { }
	| none  = '<span class="token string">no</span>'
)
</pre>
</div>
</div>
