---
layout: doc
origin: reporter
language: expressions
version: 48
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--parameter-initializers }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter initializers</span>' [ <span class="token operator">arguments:</span> ] collection
(
	'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup
	(
		'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
			'<span class="token string">expression</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
		'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
			'<span class="token string">expression</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
	)
)
</pre>
</div>
</div>

{: #grammar-rule--number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression</span>'
	'<span class="token string">type</span>' stategroup
	(
		'<span class="token string">static value</span>'
			'<span class="token string">value</span>' number
		'<span class="token string">dynamic value</span>'
			'<span class="token string">source</span>' stategroup
			(
				'<span class="token string">clock</span>' [ <span class="token operator">now</span> ]
			)
		'<span class="token string">sub expression</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left</span>' component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">operator</span>' stategroup
			(
				'<span class="token string">addition</span>'       [ <span class="token operator">+</span> ]
				'<span class="token string">subtraction</span>'    [ <span class="token operator">-</span> ]
				'<span class="token string">multiplication</span>' [ <span class="token operator">*</span> ]
				'<span class="token string">division</span>'       [ <span class="token operator">/</span> ]
			)
			'<span class="token string">right</span>' component <a href="#grammar-rule--number-expression">'number expression'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression</span>'
	'<span class="token string">type</span>' stategroup
	(
		'<span class="token string">static value</span>'
			'<span class="token string">value</span>' text
	)
</pre>
</div>
</div>
