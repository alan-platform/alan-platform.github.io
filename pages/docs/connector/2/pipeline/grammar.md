---
layout: doc
origin: connector
language: pipeline
version: 2
type: grammar
---


{: #grammar-rule--input-data }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">input data</span>' group (
	'<span class="token string">dataset</span>'      component <a href="#grammar-rule--input-data-tag">'input data tag'</a>
	'<span class="token string">notification</span>' component <a href="#grammar-rule--input-data-tag">'input data tag'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--interface-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface type</span>' [ <span class="token operator">pipeline</span> <span class="token operator">interface:</span> ] stategroup (
	'<span class="token string">provide</span>' [ <span class="token operator">provide</span> ]
		'<span class="token string">pipeline</span>' component <a href="#grammar-rule--pipeline">'pipeline'</a>
		'<span class="token string">push stage</span>' [ <span class="token operator">push:</span> ] reference
		'<span class="token string">requires</span>' stategroup ('<span class="token string">interface notification</span>')
)
</pre>
</div>
</div>

{: #grammar-rule--input-data-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">input data tag</span>'
</pre>
</div>
</div>

{: #grammar-rule--pipeline }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">pipeline</span>'
	'<span class="token string">stages</span>' collection ( [ <span class="token operator">stage</span> ]
		'<span class="token string">processor</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] reference
		'<span class="token string">inputs</span>' collection (
			'<span class="token string">type</span>' [ <span class="token operator"><<</span> ] stategroup (
				'<span class="token string">interface data</span>' [ <span class="token operator">dataset</span> ]
				'<span class="token string">raw stream</span>' [ <span class="token operator">raw</span> ]
			)
			'<span class="token string">source stage</span>' reference
		)
	)
</pre>
</div>
</div>
