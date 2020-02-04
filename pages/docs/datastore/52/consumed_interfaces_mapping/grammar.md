---
layout: doc
origin: datastore
language: consumed_interfaces_mapping
version: 52
type: grammar
---


{: #grammar-rule--interfaces-to-imported-interfaces }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interfaces to imported interfaces</span>' [ <span class="token operator">interfaces</span> ] collection (
	'<span class="token string">imported interface</span>' [ <span class="token operator">=></span> ] reference
)
</pre>
</div>
</div>

{: #grammar-rule--imported-interfaces }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">imported interfaces</span>' [ <span class="token operator">imported-interfaces</span> ] collection (
	'<span class="token string">interface</span>' [ <span class="token operator">=</span> ] reference
	'<span class="token string">context keys</span>' collection ( [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
		'<span class="token string">value</span>' [ <span class="token operator">:</span> <span class="token operator">text</span> <span class="token operator">=</span> <span class="token operator">.</span> ] reference
	)
	'<span class="token string">mapping</span>' component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
)
</pre>
</div>
</div>

{: #grammar-rule--EQ-member }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">EQ member</span>'
</pre>
</div>
</div>

{: #grammar-rule--argument-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">argument mapping</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">conditional</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">?</span> ]
			'<span class="token string">state group</span>' [ <span class="token operator">@</span> ] reference
			'<span class="token string">states</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( [ <span class="token operator">|</span> ]
				'<span class="token string">arguments</span>' component <a href="#grammar-rule--argument-mapping">'argument mapping'</a>
			)
		'<span class="token string">no</span>'
			'<span class="token string">properties</span>' collection (
				'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">collection</span>' [ <span class="token operator">collection</span> <span class="token operator">=></span> ]
						'<span class="token string">collection</span>' [ <span class="token operator">@</span> ] reference
						'<span class="token string">arguments</span>' component <a href="#grammar-rule--argument-mapping">'argument mapping'</a>
					'<span class="token string">number</span>'
						'<span class="token string">numerical type</span>' stategroup (
							'<span class="token string">integer</span>' [ <span class="token operator">integer</span> ]
							'<span class="token string">natural</span>' [ <span class="token operator">natural</span> ]
						)
						'<span class="token string">number</span>' [ <span class="token operator">=</span> <span class="token operator">@</span> ] reference
					'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
						'<span class="token string">has constraint</span>' stategroup (
							'<span class="token string">no</span>' [ <span class="token operator">=</span> ]
								'<span class="token string">text</span>' [ <span class="token operator">@</span> ] reference
							'<span class="token string">yes</span>' [ <span class="token operator">=></span> ]
								'<span class="token string">text</span>' [ <span class="token operator">@</span> ] reference
						)
					'<span class="token string">file</span>' [ <span class="token operator">file</span> ]
						'<span class="token string">file</span>' [ <span class="token operator">=</span> <span class="token operator">@</span> ] reference
					'<span class="token string">state group</span>' [ <span class="token operator">stategroup</span> <span class="token operator">=</span> ]
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">fixed</span>'
								'<span class="token string">state</span>' reference
								'<span class="token string">arguments</span>' component <a href="#grammar-rule--argument-mapping">'argument mapping'</a>
							'<span class="token string">mapped</span>' [ <span class="token operator">switch</span> ]
								'<span class="token string">state group</span>' [ <span class="token operator">@</span> ] reference
								'<span class="token string">mapping</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( [ <span class="token operator">|</span> ]
									'<span class="token string">mapped state</span>' [ <span class="token operator">=</span> ] reference
									'<span class="token string">arguments</span>' component <a href="#grammar-rule--argument-mapping">'argument mapping'</a>
								)
						)
				)
			)
	)
</pre>
</div>
</div>

{: #grammar-rule--command-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command mapping</span>'
	'<span class="token string">command</span>' reference
	'<span class="token string">argument mapping</span>' [ <span class="token operator">with</span> ] component <a href="#grammar-rule--argument-mapping">'argument mapping'</a>
</pre>
</div>
</div>

{: #grammar-rule--node-type-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type mapping</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>' collection (
		'<span class="token string">type</span>' stategroup (
			'<span class="token string">referencer anchor</span>' [ <span class="token operator">:</span> <span class="token operator">reference-set</span> ]
			'<span class="token string">command</span>' [ <span class="token operator">:</span> <span class="token operator">command</span> ]
				'<span class="token string">implementation</span>' stategroup (
					'<span class="token string">internal</span>'
					'<span class="token string">external</span>'
						'<span class="token string">mapping</span>' [ <span class="token operator">do</span> ] component <a href="#grammar-rule--command-mapping">'command mapping'</a>
				)
			'<span class="token string">property</span>'
				'<span class="token string">type</span>' stategroup (
					'<span class="token string">group</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">elementary</span>' [ <span class="token operator">:</span> <span class="token operator">group</span> ]
								'<span class="token string">group</span>' [ <span class="token operator">=</span> <span class="token operator">+</span> ] reference
								'<span class="token string">mapping</span>' component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
							'<span class="token string">derived</span>' [ <span class="token operator">:=</span> <span class="token operator">group</span> ]
						)
					'<span class="token string">collection</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">elementary</span>' [ <span class="token operator">:</span> <span class="token operator">collection</span> ]
								'<span class="token string">has key constraint</span>' stategroup (
									'<span class="token string">yes</span>' [ <span class="token operator">=></span> ]
									'<span class="token string">no</span>' [ <span class="token operator">=</span> ]
								)
								'<span class="token string">collection</span>' [ <span class="token operator">.</span> ] reference
								'<span class="token string">mapping</span>' component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
							'<span class="token string">derived</span>' [ <span class="token operator">:=</span> <span class="token operator">collection</span> ]
						)
					'<span class="token string">number</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">elementary</span>'
								'<span class="token string">type</span>' stategroup (
									'<span class="token string">causal</span>' [ <span class="token operator">:</span> <span class="token operator">number</span> <span class="token operator">causal</span> ]
									'<span class="token string">simple</span>' [ <span class="token operator">:</span> ]
										'<span class="token string">type</span>' stategroup (
											'<span class="token string">integer</span>' [ <span class="token operator">integer</span> ]
											'<span class="token string">natural</span>' [ <span class="token operator">natural</span> ]
										)
										'<span class="token string">number</span>' [ <span class="token operator">=</span> <span class="token operator">#</span> ] reference
								)
							'<span class="token string">derived</span>' [ <span class="token operator">:=</span> <span class="token operator">number</span> ]
						)
					'<span class="token string">text</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">elementary</span>' [ <span class="token operator">:</span> <span class="token operator">text</span> ]
								'<span class="token string">type</span>' stategroup (
									'<span class="token string">key</span>' [ <span class="token operator">(key)</span> ]
										'<span class="token string">is collection key</span>' component <a href="#grammar-rule--EQ-member">'EQ member'</a>
									'<span class="token string">value</span>'
										'<span class="token string">not collection key</span>' component <a href="#grammar-rule--EQ-member">'EQ member'</a>
										'<span class="token string">has constraint</span>' stategroup (
											'<span class="token string">yes</span>' [ <span class="token operator">=></span> ]
											'<span class="token string">no</span>' [ <span class="token operator">=</span> ]
										)
										'<span class="token string">text</span>' [ <span class="token operator">.</span> ] reference
								)
							'<span class="token string">derived</span>' [ <span class="token operator">:=</span> <span class="token operator">text</span> ]
						)
					'<span class="token string">file</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">elementary</span>' [ <span class="token operator">:</span> <span class="token operator">file</span> ]
								'<span class="token string">file</span>' [ <span class="token operator">=</span> <span class="token operator">/</span> ] reference
							'<span class="token string">derived</span>' [ <span class="token operator">:=</span> <span class="token operator">file</span> ]
						)
					'<span class="token string">state group</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">elementary</span>' [ <span class="token operator">:</span> <span class="token operator">stategroup</span> <span class="token operator">=</span> <span class="token operator">switch</span> ]
								'<span class="token string">state group</span>' [ <span class="token operator">?</span> ] reference
								'<span class="token string">states</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( [ <span class="token operator">|</span> ]
									'<span class="token string">state</span>' [ <span class="token operator">=</span> ] reference
									'<span class="token string">mapping</span>' component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
								)
							'<span class="token string">derived</span>' [ <span class="token operator">:=</span> <span class="token operator">stategroup</span> ]
						)
				)
		)
	)
</pre>
</div>
</div>
