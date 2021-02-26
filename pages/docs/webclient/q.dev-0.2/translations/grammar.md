---
layout: doc
origin: webclient
language: translations
version: q.dev-0.2
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--language }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">language</span>': @block [ <span class="token operator">language:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--engine-language }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">engine language</span>': @block [ <span class="token operator">engine</span> <span class="token operator">language:</span> ] stategroup (
	'<span class="token string">english</span>' { [ <span class="token operator">english</span> ] }
	'<span class="token string">dutch</span>' { [ <span class="token operator">dutch</span> ] }
)
</pre>
</div>
</div>

{: #grammar-rule--translations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">translations</span>': dictionary @order: canonical { @block indent
	'<span class="token string">translation</span>': [ <span class="token operator">:</span> ] text
}
</pre>
</div>
</div>
