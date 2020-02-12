---
layout: doc
origin: reporter
language: query
version: simple.1
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--query-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">query type</span>' stategroup
(
	'<span class="token string">collection</span>' [ <span class="token operator">collection:</span> ]
		'<span class="token string">context selection</span>' component <a href="#grammar-rule--node-selector">'node selector'</a>
		'<span class="token string">collection selection</span>' [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-selector">'collection selector'</a>
		'<span class="token string">properties</span>' [ <span class="token operator">select</span> ] collection order '<span class="token string">order</span>'
		(
			'<span class="token string">has next</span>' stategroup has successor '<span class="token string">next</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
			'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup
			(
				'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--number-expression">'number expression'</a>
					'<span class="token string">format</span>' component <a href="#grammar-rule--number-format">'number format'</a>
				'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--text-expression">'text expression'</a>
					'<span class="token string">format</span>' component <a href="#grammar-rule--text-format">'text format'</a>
				'<span class="token string">stategroup</span>' [ <span class="token operator">state</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--stategroup-expression">'stategroup expression'</a>
					'<span class="token string">format</span>' component <a href="#grammar-rule--state-format">'state format'</a>
			)
		)
		'<span class="token string">has first</span>' stategroup has '<span class="token string">properties</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
		'<span class="token string">filters</span>' [ <span class="token operator">where</span> ] component <a href="#grammar-rule--filter-expression">'filter expression'</a>
		'<span class="token string">record limit</span>' [ <span class="token operator">limit</span> ] component <a href="#grammar-rule--number-value">'number value'</a>
	'<span class="token string">graph</span>' [ <span class="token operator">graph:</span> ]
		'<span class="token string">context selection</span>' component <a href="#grammar-rule--node-selector">'node selector'</a>
		'<span class="token string">entry points</span>' group
		(
			'<span class="token string">collection selection</span>' [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-selector">'collection selector'</a>
			'<span class="token string">reference</span>' [ <span class="token operator">></span> ] reference
			'<span class="token string">dereference</span>' component <a href="#grammar-rule--dereference">'dereference'</a>
			'<span class="token string">collection</span>' component <a href="#grammar-rule--entity-ancestor-selector">'entity ancestor selector'</a>
			'<span class="token string">collection type</span>' stategroup
			(
				'<span class="token string">collection</span>'
					'<span class="token string">graph</span>' [ <span class="token operator">flatten</span> ] reference
			)
		)
		'<span class="token string">query</span>' group
		(
			'<span class="token string">collection selection</span>' [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-selector">'collection selector'</a>
			'<span class="token string">properties</span>' [ <span class="token operator">select</span> ] collection order '<span class="token string">order</span>'
			(
				'<span class="token string">has next</span>' stategroup has successor '<span class="token string">next</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
				'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup
				(
					'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
						'<span class="token string">node selection</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
						'<span class="token string">property</span>' [ <span class="token operator">:</span> ] reference
						'<span class="token string">format</span>' component <a href="#grammar-rule--number-format">'number format'</a>
					'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
						'<span class="token string">node selection</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
						'<span class="token string">property</span>' [ <span class="token operator">:</span> ] reference
						'<span class="token string">format</span>' component <a href="#grammar-rule--text-format">'text format'</a>
					'<span class="token string">stategroup</span>' [ <span class="token operator">state</span> ]
						'<span class="token string">node selection</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
						'<span class="token string">property</span>' [ <span class="token operator">:</span> ] reference
						'<span class="token string">format</span>' component <a href="#grammar-rule--state-format">'state format'</a>
				)
			)
			'<span class="token string">has first</span>' stategroup has '<span class="token string">properties</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
		)
)
</pre>
</div>
</div>

{: #grammar-rule--dereference }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dereference</span>'
	'<span class="token string">dereference</span>' stategroup
	(
		'<span class="token string">yes</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--entity-equality }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity equality</span>'
</pre>
</div>
</div>

{: #grammar-rule--node-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node selector</span>'
	'<span class="token string">has step</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup
			(
				'<span class="token string">group</span>'
					'<span class="token string">group</span>' [ <span class="token operator">+</span> ] reference
				'<span class="token string">collection entry</span>'
					'<span class="token string">collection</span>' [ <span class="token operator">.</span> ] reference
					'<span class="token string">entry id</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--text-value">'text value'</a>
				'<span class="token string">state</span>'
					'<span class="token string">stategroup</span>' [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>'      [ <span class="token operator">|</span> ] reference
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--node-selector">'node selector'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--singular-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular selector</span>'
	'<span class="token string">has step</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup
			(
				'<span class="token string">group</span>'
					'<span class="token string">group</span>' [ <span class="token operator">+</span> ] reference
				'<span class="token string">parent</span>' [ <span class="token operator">^</span> ]
				'<span class="token string">reference</span>'
					'<span class="token string">reference</span>' [ <span class="token operator">></span> ] reference
					'<span class="token string">dereference</span>' component <a href="#grammar-rule--dereference">'dereference'</a>
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--singular-selector">'singular selector'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--conditional-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional selector</span>'
	'<span class="token string">head</span>' component <a href="#grammar-rule--singular-selector">'singular selector'</a>
	'<span class="token string">has step</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">stategroup</span>' [ <span class="token operator">?</span> ] reference
			'<span class="token string">state</span>'      [ <span class="token operator">|</span> ] reference
			'<span class="token string">tail</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--entity-ancestor-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity ancestor selector</span>'
	'<span class="token string">has step</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup
			(
				'<span class="token string">parent</span>'
					'<span class="token string">entity scope</span>' [ <span class="token operator">^</span> ] component <a href="#grammar-rule--entity-equality">'entity equality'</a>
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--entity-ancestor-selector">'entity ancestor selector'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--entity-descendant-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity descendant selector</span>'
	'<span class="token string">has step</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup
			(
				'<span class="token string">group</span>'
					'<span class="token string">group</span>' [ <span class="token operator">+</span> ] reference
				'<span class="token string">state</span>'
					'<span class="token string">stategroup</span>' [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>'      [ <span class="token operator">|</span> ] reference
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--entity-descendant-selector">'entity descendant selector'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--collection-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection selector</span>'
	'<span class="token string">has step</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">head</span>' component <a href="#grammar-rule--entity-descendant-selector">'entity descendant selector'</a>
			'<span class="token string">collection</span>' [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>' component <a href="#grammar-rule--collection-selector">'collection selector'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--number-value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number value</span>'
	'<span class="token string">type</span>' stategroup
	(
		'<span class="token string">dynamic</span>'
			'<span class="token string">parameter</span>' [ <span class="token operator">&</span> ] reference
		'<span class="token string">static</span>'
			'<span class="token string">value</span>' number
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
		'<span class="token string">value</span>'
			'<span class="token string">value</span>' component <a href="#grammar-rule--number-value">'number value'</a>
		'<span class="token string">property</span>'
			'<span class="token string">node selection</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
			'<span class="token string">property</span>' [ <span class="token operator">:</span> ] reference
	)
</pre>
</div>
</div>

{: #grammar-rule--number-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number format</span>'
	'<span class="token string">type</span>' [ <span class="token operator">as</span> ] stategroup
	(
		'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
		'<span class="token string">date</span>'     [ <span class="token operator">date</span> ]
		'<span class="token string">time</span>'     [ <span class="token operator">time</span> ]
		'<span class="token string">datetime</span>' [ <span class="token operator">datetime</span> ]
		'<span class="token string">decimal</span>'  [ <span class="token operator">decimal</span> ] '<span class="token string">shift</span>' number
	)
</pre>
</div>
</div>

{: #grammar-rule--text-value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text value</span>'
	'<span class="token string">type</span>' stategroup
	(
		'<span class="token string">dynamic</span>'
			'<span class="token string">parameter</span>' [ <span class="token operator">&</span> ] reference
		'<span class="token string">static</span>'
			'<span class="token string">value</span>' text
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
		'<span class="token string">value</span>'
			'<span class="token string">value</span>' component <a href="#grammar-rule--text-value">'text value'</a>
		'<span class="token string">property</span>'
			'<span class="token string">node selection</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
			'<span class="token string">property</span>' [ <span class="token operator">:</span> ] reference
	)
</pre>
</div>
</div>

{: #grammar-rule--text-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text format</span>'
	'<span class="token string">type</span>' [ <span class="token operator">as</span> ] stategroup
	(
		'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--stategroup-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stategroup expression</span>'
	'<span class="token string">node selection</span>' component <a href="#grammar-rule--conditional-selector">'conditional selector'</a>
	'<span class="token string">stategroup</span>' [ <span class="token operator">:</span> ] reference
</pre>
</div>
</div>

{: #grammar-rule--state-format }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state format</span>'
	'<span class="token string">type</span>' [ <span class="token operator">as</span> ] stategroup
	(
		'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--filter-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">filter expression</span>'
	'<span class="token string">has filter</span>' stategroup
	(
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup
			(
				'<span class="token string">number</span>'
					'<span class="token string">left value</span>' component <a href="#grammar-rule--number-expression">'number expression'</a>
					'<span class="token string">operator</span>' stategroup
					(
						'<span class="token string">equal</span>'         [ <span class="token operator">==</span> ]
						'<span class="token string">greater</span>'       [ <span class="token operator">></span> ]
						'<span class="token string">greater equal</span>' [ <span class="token operator">>=</span> ]
						'<span class="token string">smaller</span>'       [ <span class="token operator"><</span> ]
						'<span class="token string">smaller equal</span>' [ <span class="token operator"><=</span> ]
					)
					'<span class="token string">right value</span>' component <a href="#grammar-rule--number-value">'number value'</a>
				'<span class="token string">stategroup</span>'
					'<span class="token string">value</span>' component <a href="#grammar-rule--stategroup-expression">'stategroup expression'</a>
					'<span class="token string">include states</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( )
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--filter-expression">'filter expression'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>
