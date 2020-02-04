---
layout: doc
origin: connector
language: processor
version: 2
type: grammar
---


{: #grammar-rule--operation-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">operation type</span>' group (
	'<span class="token string">safe</span>' component <a href="#grammar-rule--operation-tag">'operation tag'</a>
	'<span class="token string">unsafe</span>' component <a href="#grammar-rule--operation-tag">'operation tag'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--existence-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">existence type</span>' group (
	'<span class="token string">mandatory</span>' component <a href="#grammar-rule--existence-tag">'existence tag'</a>
	'<span class="token string">optional</span>' component <a href="#grammar-rule--existence-tag">'existence tag'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type</span>' group (
	'<span class="token string">undefined</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
	'<span class="token string">JSON object</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
	'<span class="token string">JSON array</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
	'<span class="token string">boolean</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
	'<span class="token string">number</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
	'<span class="token string">text</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--input-data }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">input data</span>' [ <span class="token operator">input:</span> ] collection (
	'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">interface data</span>' [ <span class="token operator">interface-data</span> ]
			'<span class="token string">type</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
		'<span class="token string">raw stream</span>' [ <span class="token operator">raw-stream</span> ]
	)
)
</pre>
</div>
</div>

{: #grammar-rule--output-data }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">output data</span>' group (
	'<span class="token string">interface data</span>' component <a href="#grammar-rule--output-data-tag">'output data tag'</a>
	'<span class="token string">interface notification</span>' component <a href="#grammar-rule--output-data-tag">'output data tag'</a>
	'<span class="token string">raw stream</span>' component <a href="#grammar-rule--output-data-tag">'output data tag'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--schemas }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schemas</span>' collection ( [ <span class="token operator">schema</span> ]
	'<span class="token string">root</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--type">'type'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--processor }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">processor</span>' [ <span class="token operator">type:</span> ] stategroup (
	'<span class="token string">HTTP GET</span>' [ <span class="token operator">HTTP</span> <span class="token operator">GET</span> ]
		'<span class="token string">URI</span>' component <a href="#grammar-rule--base-text-expression">'base text expression'</a>
		'<span class="token string">parameters</span>' collection order '<span class="token string">order</span>' (
			'<span class="token string">has next</span>' stategroup has successor '<span class="token string">next</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
			'<span class="token string">value</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--base-text-expression">'base text expression'</a>
		)
		'<span class="token string">has parameters</span>' stategroup has '<span class="token string">parameters</span>' first '<span class="token string">first</span>' '<span class="token string">yes</span>' '<span class="token string">no</span>'
	'<span class="token string">transform</span>' [ <span class="token operator">transform</span> ]
		'<span class="token string">root</span>' component <a href="#grammar-rule--target-root">'target root'</a>
		'<span class="token string">empty</span>' component <a href="#grammar-rule--let-tag">'let tag'</a>
		'<span class="token string">statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
	'<span class="token string">interface diff</span>' [ <span class="token operator">interface-diff</span> ]
		'<span class="token string">source data</span>' reference
)
</pre>
</div>
</div>

{: #grammar-rule--operation-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">operation tag</span>'
</pre>
</div>
</div>

{: #grammar-rule--existence-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">existence tag</span>'
</pre>
</div>
</div>

{: #grammar-rule--type-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type tag</span>'
</pre>
</div>
</div>

{: #grammar-rule--output-data-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">output data tag</span>'
/* Constraint Types, required as equality constraints cannot be set on states */
</pre>
</div>
</div>

{: #grammar-rule--echo-operation-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">echo operation tag</span>'
/* Generic Expressions */
</pre>
</div>
</div>

{: #grammar-rule--base-number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">base number expression</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">variable</span>'
			'<span class="token string">variable</span>' [ <span class="token operator">var</span>, <span class="token operator">number</span> ] reference
		'<span class="token string">static</span>'
			'<span class="token string">integer</span>' number
	)
</pre>
</div>
</div>

{: #grammar-rule--base-text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">base text expression</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">interface context key</span>'
			'<span class="token string">key</span>' [ <span class="token operator">interface-key</span> ] reference
		'<span class="token string">variable</span>'
			'<span class="token string">variable</span>' [ <span class="token operator">var</span>, <span class="token operator">text</span> ] reference
		'<span class="token string">static</span>'
			'<span class="token string">text value</span>' text
		'<span class="token string">line break</span>' [ <span class="token operator">line-break</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--number-import-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number import rule</span>'
	'<span class="token string">decimal translation</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator"><<</span> ]
			'<span class="token string">places</span>' component <a href="#grammar-rule--base-number-expression">'base number expression'</a>
		'<span class="token string">no</span>'
	)
/* Schema */
</pre>
</div>
</div>

{: #grammar-rule--entity }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity</span>'
	'<span class="token string">tag</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
	'<span class="token string">type</span>' component <a href="#grammar-rule--type">'type'</a>
</pre>
</div>
</div>

{: #grammar-rule--type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">node</span>'
			'<span class="token string">node</span>' component <a href="#grammar-rule--node">'node'</a>
		'<span class="token string">collection</span>' [ <span class="token operator">collection</span> ]
			'<span class="token string">tag</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
			'<span class="token string">entity</span>' component <a href="#grammar-rule--entity">'entity'</a>
		'<span class="token string">list</span>' [ <span class="token operator">list</span> ]
			'<span class="token string">tag</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
			'<span class="token string">type</span>' component <a href="#grammar-rule--type">'type'</a>
		'<span class="token string">boolean</span>' [ <span class="token operator">boolean</span> ]
		'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
			'<span class="token string">rule</span>' component <a href="#grammar-rule--number-import-rule">'number import rule'</a>
		'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node</span>' [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	'<span class="token string">properties</span>' collection (
		'<span class="token string">type</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--type">'type'</a>
	)
	'<span class="token string">type</span>' component <a href="#grammar-rule--type-tag">'type tag'</a>
/* Transformer */
</pre>
</div>
</div>

{: #grammar-rule--target-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target tag</span>'
</pre>
</div>
</div>

{: #grammar-rule--target-root }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target root</span>'
	'<span class="token string">tag</span>' component <a href="#grammar-rule--target-tag">'target tag'</a>
</pre>
</div>
</div>

{: #grammar-rule--target-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target node</span>'
	'<span class="token string">tag</span>' component <a href="#grammar-rule--target-tag">'target tag'</a>
</pre>
</div>
</div>

{: #grammar-rule--target-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target property</span>'
	'<span class="token string">tag</span>' component <a href="#grammar-rule--target-tag">'target tag'</a>
</pre>
</div>
</div>

{: #grammar-rule--target-collection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target collection</span>'
	'<span class="token string">tag</span>' component <a href="#grammar-rule--target-tag">'target tag'</a>
</pre>
</div>
</div>

{: #grammar-rule--let-tag }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">let tag</span>'
</pre>
</div>
</div>

{: #grammar-rule--let-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">let context</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">single</span>' [ <span class="token operator">$</span> ]
			'<span class="token string">value</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value-statement">'value statement'</a>
		'<span class="token string">multiple</span>'
			'<span class="token string">values</span>' collection ( [ <span class="token operator">$</span> ]
				'<span class="token string">value</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value-statement">'value statement'</a>
			)
	)
	'<span class="token string">tag</span>' component <a href="#grammar-rule--let-tag">'let tag'</a>
</pre>
</div>
</div>

{: #grammar-rule--let-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">let selector</span>'
	'<span class="token string">let context defined</span>' stategroup (
		'<span class="token string">yes</span>'
			'<span class="token string">step</span>' stategroup (
				'<span class="token string">parent</span>' [ <span class="token operator">^</span> ]
					'<span class="token string">tail</span>' component <a href="#grammar-rule--let-selector">'let selector'</a>
				'<span class="token string">none</span>'
			)
	)
</pre>
</div>
</div>

{: #grammar-rule--value-tail-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value tail statement</span>'
	'<span class="token string">has step</span>' stategroup (
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">object fetch</span>'
					'<span class="token string">object key</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--value-statement">'value statement'</a>
					'<span class="token string">as</span>' [ <span class="token operator">as</span> ] stategroup (
						'<span class="token string">JSON object</span>' [ <span class="token operator">object</span> ]
						'<span class="token string">JSON array</span>' [ <span class="token operator">array</span> ]
						'<span class="token string">boolean</span>' [ <span class="token operator">boolean</span> ]
						'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
							'<span class="token string">rule</span>' component <a href="#grammar-rule--number-import-rule">'number import rule'</a>
						'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
					)
				'<span class="token string">node fetch</span>'
					'<span class="token string">property</span>' [ <span class="token operator">.</span> ] reference
				'<span class="token string">collection lookup</span>' [ <span class="token operator">:</span> ]
					'<span class="token string">entity key</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--value-statement">'value statement'</a>
				'<span class="token string">key fetch</span>' [ <span class="token operator">key</span> ]
				'<span class="token string">value fetch</span>' [ <span class="token operator">value</span> ]
				'<span class="token string">parse</span>' [ <span class="token operator">parse</span> ]
					'<span class="token string">as</span>' [ <span class="token operator">as</span> ] stategroup (
						'<span class="token string">JSON</span>' [ <span class="token operator">JSON</span> ]
					)
				'<span class="token string">decorate</span>' [ <span class="token operator">decorate</span> ]
					'<span class="token string">definition</span>' [ <span class="token operator">as</span> ] stategroup (
						'<span class="token string">global</span>'
							'<span class="token string">schema</span>' reference
						'<span class="token string">inline</span>'
							'<span class="token string">root</span>' component <a href="#grammar-rule--type">'type'</a>
					)
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--value-tail-statement">'value tail statement'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--value-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value statement</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">simple number</span>'
			'<span class="token string">expression</span>' component <a href="#grammar-rule--base-number-expression">'base number expression'</a>
		'<span class="token string">simple text</span>'
			'<span class="token string">expression</span>' component <a href="#grammar-rule--base-text-expression">'base text expression'</a>
		'<span class="token string">let</span>'
			'<span class="token string">selection</span>' component <a href="#grammar-rule--let-selector">'let selector'</a>
			'<span class="token string">value</span>' [ <span class="token operator">$</span> ] stategroup (
				'<span class="token string">single</span>'
				'<span class="token string">select</span>'
					'<span class="token string">value</span>' reference
			)
		'<span class="token string">context</span>' [ <span class="token operator">context</span> ]
		'<span class="token string">input data</span>'
			'<span class="token string">source</span>' [ <span class="token operator">&</span> ] reference
		'<span class="token string">list operation</span>'
			'<span class="token string">operation</span>' stategroup (
				'<span class="token string">sum</span>' [ <span class="token operator">sum</span> ]
				'<span class="token string">product</span>' [ <span class="token operator">product</span> ]
				'<span class="token string">concatenate</span>' [ <span class="token operator">concatenate</span> ]
					'<span class="token string">separator</span>' stategroup (
						'<span class="token string">yes</span>'
							'<span class="token string">value</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--value-statement">'value statement'</a>
						'<span class="token string">no</span>'
					)
				'<span class="token string">logical and</span>' [ <span class="token operator">and</span> ]
				'<span class="token string">logical or</span>' [ <span class="token operator">or</span> ]
			)
			'<span class="token string">values</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--value-list-statement">'value list statement'</a>
	)
	'<span class="token string">tail</span>' component <a href="#grammar-rule--value-tail-statement">'value tail statement'</a>
	'<span class="token string">unsafe handling</span>' stategroup (
		'<span class="token string">alternative</span>' [ <span class="token operator">||</span> ]
			'<span class="token string">requires unsafe context</span>' component <a href="#grammar-rule--echo-operation-tag">'echo operation tag'</a>
			'<span class="token string">alternative</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
		'<span class="token string">raise</span>' [ <span class="token operator">||</span> <span class="token operator">raise</span> ]
			'<span class="token string">requires unsafe context</span>' component <a href="#grammar-rule--echo-operation-tag">'echo operation tag'</a>
			'<span class="token string">message</span>' text
		'<span class="token string">none</span>' [ <span class="token operator">||</span> <span class="token operator">none</span> ]
			'<span class="token string">requires unsafe context</span>' component <a href="#grammar-rule--echo-operation-tag">'echo operation tag'</a>
		'<span class="token string">no</span>'
			'<span class="token string">requires safe context</span>' component <a href="#grammar-rule--echo-operation-tag">'echo operation tag'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--value-list-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value list statement</span>'
	'<span class="token string">value</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
	'<span class="token string">has tail</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">,</span> ]
			'<span class="token string">value</span>' component <a href="#grammar-rule--value-list-statement">'value list statement'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--compound-transform-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">compound transform statement</span>'
	'<span class="token string">has statement</span>' stategroup (
		'<span class="token string">yes</span>'
			'<span class="token string">statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
			'<span class="token string">tail</span>' component <a href="#grammar-rule--compound-transform-statement">'compound transform statement'</a>
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--transform-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">transform statement</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">let</span>' [ <span class="token operator">let</span> ]
			'<span class="token string">context</span>' component <a href="#grammar-rule--let-context">'let context'</a>
			'<span class="token string">statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
		'<span class="token string">guard</span>' [ <span class="token operator">guard</span> ]
			'<span class="token string">guarded statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
			'<span class="token string">fallback statement</span>' [ <span class="token operator">catch</span> ] component <a href="#grammar-rule--transform-statement">'transform statement'</a>
		'<span class="token string">map</span>' [ <span class="token operator">map</span> ]
			'<span class="token string">value</span>' stategroup (
				'<span class="token string">schema</span>'
					'<span class="token string">as</span>' stategroup (
						'<span class="token string">collection</span>' [ <span class="token operator">collection</span> ]
						'<span class="token string">list</span>' [ <span class="token operator">list</span> ]
					)
					'<span class="token string">value</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
				'<span class="token string">array</span>' [ <span class="token operator">array</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
					'<span class="token string">as</span>' [ <span class="token operator">as</span> ] stategroup (
						'<span class="token string">JSON object</span>' [ <span class="token operator">object</span> ]
						'<span class="token string">JSON array</span>' [ <span class="token operator">array</span> ]
						'<span class="token string">boolean</span>' [ <span class="token operator">boolean</span> ]
						'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
							'<span class="token string">rule</span>' component <a href="#grammar-rule--number-import-rule">'number import rule'</a>
						'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
					)
			)
			'<span class="token string">statement</span>' [ <span class="token operator">{</span>, <span class="token operator">}</span> ] component <a href="#grammar-rule--compound-transform-statement">'compound transform statement'</a>
		'<span class="token string">condition</span>' [ <span class="token operator">match</span> ]
			'<span class="token string">conditional</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
			'<span class="token string">then statement</span>' [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">-></span> ] component <a href="#grammar-rule--transform-statement">'transform statement'</a>
			'<span class="token string">else statement</span>' [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">-></span> ] component <a href="#grammar-rule--transform-statement">'transform statement'</a>
		/* map to target */
		'<span class="token string">target root</span>' [ <span class="token operator">root</span> ]
			'<span class="token string">node</span>' component <a href="#grammar-rule--target-node">'target node'</a>
			'<span class="token string">statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
		'<span class="token string">target node</span>'
			'<span class="token string">properties</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection (
				'<span class="token string">property</span>' component <a href="#grammar-rule--target-property">'target property'</a>
				'<span class="token string">statement</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--transform-statement">'transform statement'</a>
			)
		'<span class="token string">target property</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">group</span>' [ <span class="token operator">group</span> ]
					'<span class="token string">node</span>' component <a href="#grammar-rule--target-node">'target node'</a>
					'<span class="token string">statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
				'<span class="token string">collection</span>' [ <span class="token operator">collection</span> ]
					'<span class="token string">collection</span>' component <a href="#grammar-rule--target-collection">'target collection'</a>
					'<span class="token string">statements</span>' [ <span class="token operator">{</span>, <span class="token operator">}</span> ] component <a href="#grammar-rule--compound-transform-statement">'compound transform statement'</a>
				'<span class="token string">stategroup</span>' [ <span class="token operator">state</span> ]
					'<span class="token string">state</span>' reference
					'<span class="token string">node</span>' component <a href="#grammar-rule--target-node">'target node'</a>
					'<span class="token string">statement</span>' component <a href="#grammar-rule--transform-statement">'transform statement'</a>
				'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
				'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
				'<span class="token string">reference</span>' [ <span class="token operator">reference</span> ]
					'<span class="token string">value</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
			)
		'<span class="token string">target collection</span>' [ <span class="token operator">entry</span> ]
			'<span class="token string">key</span>' component <a href="#grammar-rule--value-statement">'value statement'</a>
			'<span class="token string">node</span>' component <a href="#grammar-rule--target-node">'target node'</a>
			'<span class="token string">statement</span>' [ <span class="token operator">=</span> ] component <a href="#grammar-rule--transform-statement">'transform statement'</a>
	)
</pre>
</div>
</div>
