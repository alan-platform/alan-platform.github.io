---
layout: doc
origin: webclient
language: widget
version: odo.2
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--binding-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">binding context</span>' stategroup (
	'<span class="token string">none</span>' [ <span class="token operator">static</span> ]
	'<span class="token string">select</span>'
		'<span class="token string">binding</span>' [ <span class="token operator">binding</span> ] reference
		'<span class="token string">switch client binding context</span>' stategroup (
			'<span class="token string">yes</span>' [ <span class="token operator">on</span> ]
				'<span class="token string">constrained on containing binding</span>' stategroup (
					'<span class="token string">yes</span>'
						'<span class="token string">type path</span>' component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
						'<span class="token string">instance binding</span>' reference
					'<span class="token string">no</span>' [ <span class="token operator">unconstrained</span> ]
						'<span class="token string">instance binding</span>' reference
				)
			'<span class="token string">no</span>'
		)
)
</pre>
</div>
</div>

{: #grammar-rule--widget }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget</span>' component <a href="#grammar-rule--widget-configuration-node">'widget configuration node'</a>
</pre>
</div>
</div>

{: #grammar-rule--invalid-implementation-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">invalid implementation context</span>' component <a href="#grammar-rule--widget-implementation-context">'widget implementation context'</a>
</pre>
</div>
</div>

{: #grammar-rule--root-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
</pre>
</div>
</div>

{: #grammar-rule--root-attribute-location }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root attribute location</span>' component <a href="#grammar-rule--control-attribute-location">'control attribute location'</a>
</pre>
</div>
</div>

{: #grammar-rule--switch-block }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">switch block</span>' component <a href="#grammar-rule--state-switch">'state switch'</a>
</pre>
</div>
</div>

{: #grammar-rule--client-binding-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">client binding type path</span>'
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">state</span>'
					'<span class="token string">state group</span>' [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>' [ <span class="token operator">*</span> ] reference
				'<span class="token string">collection</span>'
					'<span class="token string">collection</span>' [ <span class="token operator">.</span> ] reference
				'<span class="token string">binding</span>'
					'<span class="token string">instance binding</span>' reference
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--configuration-attribute-persistence }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">configuration attribute persistence</span>'
	'<span class="token string">persist</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">@persist</span> ]
			'<span class="token string">per session</span>' stategroup (
				'<span class="token string">yes</span>' [ <span class="token operator">session</span> ]
				'<span class="token string">no</span>'
			)
			'<span class="token string">per entry</span>' stategroup (
				'<span class="token string">yes</span>' [ <span class="token operator">entry</span> ]
				'<span class="token string">no</span>'
			)
		'<span class="token string">no</span>'
	)
</pre>
</div>
</div>

{: #grammar-rule--widget-configuration-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget configuration node</span>' [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	'<span class="token string">attributes</span>' collection (
		'<span class="token string">switch client binding context</span>' stategroup (
			'<span class="token string">yes</span>' [ <span class="token operator">on</span> ]
				'<span class="token string">constrained on containing binding</span>' stategroup (
					'<span class="token string">yes</span>'
						'<span class="token string">type path</span>' component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
					'<span class="token string">no</span>' [ <span class="token operator">unconstrained</span> ]
						'<span class="token string">instance binding</span>' reference
				)
			'<span class="token string">no</span>'
		)
		'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">widget</span>' [ <span class="token operator">widget</span> ]
			'<span class="token string">window</span>' [ <span class="token operator">window</span> ]
				'<span class="token string">node</span>' component <a href="#grammar-rule--widget-configuration-node">'widget configuration node'</a>
			'<span class="token string">view</span>' [ <span class="token operator">view</span> ]
			'<span class="token string">inline view</span>' [ <span class="token operator">inline</span> <span class="token operator">view</span> ]
			'<span class="token string">configuration</span>' [ <span class="token operator">configuration</span> ]
				'<span class="token string">type</span>' stategroup (
					'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
						'<span class="token string">persistence</span>' component <a href="#grammar-rule--configuration-attribute-persistence">'configuration attribute persistence'</a>
					'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
						'<span class="token string">persistence</span>' component <a href="#grammar-rule--configuration-attribute-persistence">'configuration attribute persistence'</a>
					'<span class="token string">list</span>' [ <span class="token operator">list</span> ]
						'<span class="token string">node</span>' component <a href="#grammar-rule--widget-configuration-node">'widget configuration node'</a>
					'<span class="token string">state group</span>' [ <span class="token operator">stategroup</span> ]
						'<span class="token string">persistence</span>' component <a href="#grammar-rule--configuration-attribute-persistence">'configuration attribute persistence'</a>
						'<span class="token string">states</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection (
							'<span class="token string">node</span>' [ <span class="token operator">-></span> ] component <a href="#grammar-rule--widget-configuration-node">'widget configuration node'</a>
						)
				)
			'<span class="token string">binding</span>' [ <span class="token operator">binding</span> ]
				'<span class="token string">constrained on containing binding</span>' stategroup (
					'<span class="token string">yes</span>'
						'<span class="token string">type path</span>' component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
						'<span class="token string">instance binding</span>' reference
					'<span class="token string">no</span>' [ <span class="token operator">unconstrained</span> ]
						'<span class="token string">instance binding</span>' reference
				)
				'<span class="token string">node</span>' component <a href="#grammar-rule--widget-configuration-node">'widget configuration node'</a>
		)
	)
</pre>
</div>
</div>

{: #grammar-rule--widget-implementation-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget implementation context</span>'
</pre>
</div>
</div>

{: #grammar-rule--valid-widget-implementation-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">valid widget implementation context</span>'
	'<span class="token string">context</span>' component <a href="#grammar-rule--widget-implementation-context">'widget implementation context'</a>
</pre>
</div>
</div>

{: #grammar-rule--attribute-location }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">attribute location</span>'
</pre>
</div>
</div>

{: #grammar-rule--control-attribute-location }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">control attribute location</span>'
	'<span class="token string">invalid attribute location</span>' component <a href="#grammar-rule--attribute-location">'attribute location'</a>
</pre>
</div>
</div>

{: #grammar-rule--widget-implementation-context-parent-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget implementation context parent path</span>'
	'<span class="token string">has parent step</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>' [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>' component <a href="#grammar-rule--widget-implementation-context-parent-path">'widget implementation context parent path'</a>
		'<span class="token string">root</span>' [ <span class="token operator">root</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--control-binding }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">control binding</span>'
	'<span class="token string">binding type</span>' stategroup (
		'<span class="token string">let declaration</span>'
			'<span class="token string">path</span>' [ <span class="token operator">@</span> ] component <a href="#grammar-rule--widget-implementation-context-parent-path">'widget implementation context parent path'</a>
			'<span class="token string">on widget implementation node</span>' stategroup (
				'<span class="token string">yes</span>'
					'<span class="token string">declaration</span>' reference
			)
		'<span class="token string">static</span>'
			'<span class="token string">control</span>' [ <span class="token operator">control</span> ] reference
			'<span class="token string">node binding</span>' component <a href="#grammar-rule--widget-implementation-node">'widget implementation node'</a>
		'<span class="token string">window</span>'
			'<span class="token string">window</span>' [ <span class="token operator">window</span> ] reference
			'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
			'<span class="token string">control binding</span>' component <a href="#grammar-rule--control-binding">'control binding'</a>
		'<span class="token string">widget</span>'
			'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">widget</span>' [ <span class="token operator">widget</span> ] reference
		'<span class="token string">inline view</span>' [ <span class="token operator">inline</span> <span class="token operator">view</span> ]
			'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">view</span>' reference
	)
</pre>
</div>
</div>

{: #grammar-rule--entries-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entries list</span>'
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>'
			'<span class="token string">node binding</span>' component <a href="#grammar-rule--widget-implementation-node">'widget implementation node'</a>
			'<span class="token string">tail</span>' component <a href="#grammar-rule--entries-list">'entries list'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--context-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context selection</span>'
	'<span class="token string">change context to</span>' stategroup (
		'<span class="token string">engine state</span>' [ <span class="token operator">engine</span> ]
			'<span class="token string">engine state binding</span>' reference
		'<span class="token string">other context</span>'
			'<span class="token string">parent path</span>' component <a href="#grammar-rule--widget-implementation-context-parent-path">'widget implementation context parent path'</a>
			'<span class="token string">path</span>' component <a href="#grammar-rule--context-selection-path">'context selection path'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--bound-context-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">bound context selection</span>'
	'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
	'<span class="token string">cast</span>' stategroup (
		'<span class="token string">to binding</span>' [ <span class="token operator">$</span> ]
	)
</pre>
</div>
</div>

{: #grammar-rule--context-selection-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context selection path</span>'
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">unconstrained configuration attribute</span>'
					'<span class="token string">configuration attribute</span>' [ <span class="token operator">unconstrained</span> <span class="token operator">::</span> ] reference
				'<span class="token string">constrained configuration attribute</span>'
					'<span class="token string">configuration attribute</span>' [ <span class="token operator">::</span> ] reference
				'<span class="token string">client binding</span>'
					'<span class="token string">binding</span>' [ <span class="token operator">switch</span> <span class="token operator">to</span> ] reference
			)
			'<span class="token string">tail</span>' component <a href="#grammar-rule--context-selection-path">'context selection path'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--instruction-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">instruction selection</span>'
	'<span class="token string">configuration attribute type</span>' stategroup (
		'<span class="token string">binding</span>'
			'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
			'<span class="token string">instruction</span>' [ <span class="token operator">>></span> ] reference
			'<span class="token string">instruction argument</span>' stategroup (
				'<span class="token string">none</span>'
				'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
					'<span class="token string">transform</span>' stategroup (
						'<span class="token string">no</span>'
						'<span class="token string">yes</span>' [ <span class="token operator">transform</span> ]
							'<span class="token string">from</span>' stategroup (
								'<span class="token string">text</span>'
									'<span class="token string">transformer</span>' reference
								'<span class="token string">number</span>' [ <span class="token operator">#</span> ]
									'<span class="token string">transformer</span>' reference
							)
					)
				'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
				'<span class="token string">file</span>' [ <span class="token operator">file</span> ]
				'<span class="token string">view</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">view configuration</span>' reference
			)
		'<span class="token string">collection</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">configuration</span>'
					'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
					'<span class="token string">list</span>' [ <span class="token operator">=</span> ] reference
					'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
					'<span class="token string">instruction selection</span>' component <a href="#grammar-rule--instruction-selection">'instruction selection'</a>
				'<span class="token string">binding</span>'
					'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
					'<span class="token string">collection property</span>' [ <span class="token operator">.</span> ] reference
					'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
					'<span class="token string">instruction selection</span>' component <a href="#grammar-rule--instruction-selection">'instruction selection'</a>
			)
		'<span class="token string">switch</span>'
			'<span class="token string">switch</span>' component <a href="#grammar-rule--state-switch">'state switch'</a>
		'<span class="token string">ignore</span>' [ <span class="token operator">ignore</span> ]
		'<span class="token string">configuration</span>'
			'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">instruction</span>' stategroup (
				'<span class="token string">set state</span>' [ <span class="token operator">set</span> <span class="token operator">state</span> ]
					'<span class="token string">state group</span>' reference
					'<span class="token string">state</span>' [ <span class="token operator">:</span> ] reference
					'<span class="token string">node</span>' component <a href="#grammar-rule--instruction-argument-configuration-node">'instruction argument configuration node'</a>
				'<span class="token string">set number</span>' [ <span class="token operator">set</span> <span class="token operator">number</span> ]
					'<span class="token string">number</span>' reference
				'<span class="token string">set text</span>' [ <span class="token operator">set</span> <span class="token operator">text</span> ]
					'<span class="token string">text</span>' reference
			)
	)
</pre>
</div>
</div>

{: #grammar-rule--instruction-argument-configuration-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">instruction argument configuration node</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>' collection (
		'<span class="token string">type</span>' stategroup (
			'<span class="token string">configuration</span>'
				'<span class="token string">type</span>' [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
						'<span class="token string">value type</span>' stategroup (
							'<span class="token string">static</span>'
								'<span class="token string">value</span>' number
							'<span class="token string">instruction argument</span>' [ <span class="token operator">argument</span> ]
						)
					'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
						'<span class="token string">value type</span>' stategroup (
							'<span class="token string">static</span>'
								'<span class="token string">value</span>' text
							'<span class="token string">instruction argument</span>' [ <span class="token operator">argument</span> ]
						)
					'<span class="token string">state group</span>' [ <span class="token operator">state</span> ]
						'<span class="token string">state</span>' reference
						'<span class="token string">node</span>' component <a href="#grammar-rule--instruction-argument-configuration-node">'instruction argument configuration node'</a>
				)
		)
	)
</pre>
</div>
</div>

{: #grammar-rule--instruction-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">instruction list</span>'
	'<span class="token string">instruction selection</span>' component <a href="#grammar-rule--instruction-selection">'instruction selection'</a>
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>' [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>' component <a href="#grammar-rule--instruction-list">'instruction list'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--widget-implementation-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget implementation node</span>' [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	'<span class="token string">define context</span>' stategroup (
		'<span class="token string">yes</span>' [ <span class="token operator">define</span> <span class="token operator">context</span> ]
			'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
			'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">let declarations</span>' collection ( [ <span class="token operator">let</span> ]
				'<span class="token string">let declaration attribute location</span>' component <a href="#grammar-rule--control-attribute-location">'control attribute location'</a>
				'<span class="token string">switch block</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--state-switch">'state switch'</a>
			)
		'<span class="token string">no</span>'
	)
	'<span class="token string">attributes</span>' collection (
		'<span class="token string">location</span>' component <a href="#grammar-rule--attribute-location">'attribute location'</a>
		'<span class="token string">switch block</span>' [ <span class="token operator">:</span> ] component <a href="#grammar-rule--state-switch">'state switch'</a>
	)
</pre>
</div>
</div>

{: #grammar-rule--state-switch }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state switch</span>'
	'<span class="token string">type</span>' stategroup (
		'<span class="token string">attribute</span>'
			'<span class="token string">control attribute type</span>' stategroup (
				'<span class="token string">instruction</span>' [ <span class="token operator">instruction</span> ]
					'<span class="token string">type</span>' stategroup (
						'<span class="token string">singular</span>'
							'<span class="token string">instruction</span>' component <a href="#grammar-rule--instruction-selection">'instruction selection'</a>
						'<span class="token string">list</span>'
							'<span class="token string">instruction list</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--instruction-list">'instruction list'</a>
					)
				'<span class="token string">markup</span>' [ <span class="token operator">markup</span> ]
					'<span class="token string">control binding</span>' component <a href="#grammar-rule--control-binding">'control binding'</a>
				'<span class="token string">property</span>'
						'<span class="token string">type</span>' stategroup (
							'<span class="token string">dictionary</span>' [ <span class="token operator">collection</span> ]
								'<span class="token string">binding type</span>' stategroup (
									'<span class="token string">empty</span>' [ <span class="token operator">empty</span> ]
									'<span class="token string">widget binding</span>'
										'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
										'<span class="token string">collection property</span>' [ <span class="token operator">.</span> ] reference
										'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
										'<span class="token string">node binding</span>' component <a href="#grammar-rule--widget-implementation-node">'widget implementation node'</a>
								)
							'<span class="token string">list</span>' [ <span class="token operator">list</span> ]
								'<span class="token string">binding type</span>' stategroup (
									'<span class="token string">static</span>'
										'<span class="token string">entries</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--entries-list">'entries list'</a>
									'<span class="token string">configuration</span>'
										'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
										'<span class="token string">list</span>' [ <span class="token operator">=</span> ] reference
										'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
										'<span class="token string">node binding</span>' component <a href="#grammar-rule--widget-implementation-node">'widget implementation node'</a>
									'<span class="token string">widget binding</span>'
										'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
										'<span class="token string">collection property</span>' [ <span class="token operator">.</span> ] reference
										'<span class="token string">widget context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
										'<span class="token string">node binding</span>' component <a href="#grammar-rule--widget-implementation-node">'widget implementation node'</a>
							)
							'<span class="token string">number</span>' [ <span class="token operator">number</span> ]
								'<span class="token string">binding type</span>' stategroup (
									'<span class="token string">static number</span>'
										'<span class="token string">value</span>' number
									'<span class="token string">current time</span>' [ <span class="token operator">current</span> <span class="token operator">time</span> ]
										'<span class="token string">throttle</span>' stategroup (
											'<span class="token string">yes</span>'
												'<span class="token string">interval</span>' [ <span class="token operator">interval:</span> ] number
											'<span class="token string">no</span>'
										)
									'<span class="token string">configuration</span>'
										'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
										'<span class="token string">bound number</span>' [ <span class="token operator">=</span> ] reference
									'<span class="token string">widget binding</span>'
										'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
										'<span class="token string">property</span>' [ <span class="token operator">#</span> ] reference
								)
								'<span class="token string">transform</span>' stategroup (
									'<span class="token string">no</span>'
									'<span class="token string">yes</span>' [ <span class="token operator">transform</span> ]
										'<span class="token string">transformer</span>' reference
								)
							'<span class="token string">text</span>' [ <span class="token operator">text</span> ]
								'<span class="token string">type</span>' stategroup (
									'<span class="token string">binding</span>'
										'<span class="token string">text binding</span>' component <a href="#grammar-rule--text-binding">'text binding'</a>
									'<span class="token string">concatenation</span>'
										'<span class="token string">strings</span>' [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--string-list">'string list'</a>
								)
							'<span class="token string">state group</span>' [ <span class="token operator">state</span> ]
								'<span class="token string">state</span>' reference
								'<span class="token string">binding</span>' component <a href="#grammar-rule--widget-implementation-node">'widget implementation node'</a>
						)
			)
		'<span class="token string">control</span>'
			'<span class="token string">control binding</span>' component <a href="#grammar-rule--control-binding">'control binding'</a>
		'<span class="token string">switch</span>'
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">configuration</span>'
					'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
					'<span class="token string">state group</span>' [ <span class="token operator">?</span> ] reference
					'<span class="token string">states</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( [ <span class="token operator">|</span> ]
						'<span class="token string">state context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
						'<span class="token string">next</span>' [ <span class="token operator">-></span> ] component <a href="#grammar-rule--state-switch">'state switch'</a>
					)
				'<span class="token string">binding</span>'
					'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
					'<span class="token string">property</span>' [ <span class="token operator">?</span> ] reference
					'<span class="token string">states</span>' [ <span class="token operator">(</span>, <span class="token operator">)</span> ] collection ( [ <span class="token operator">|</span> ]
						'<span class="token string">state context</span>' component <a href="#grammar-rule--valid-widget-implementation-context">'valid widget implementation context'</a>
						'<span class="token string">next</span>' [ <span class="token operator">-></span> ] component <a href="#grammar-rule--state-switch">'state switch'</a>
					)
			)
	)
</pre>
</div>
</div>

{: #grammar-rule--text-binding }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text binding</span>'
	'<span class="token string">binding type</span>' stategroup (
		'<span class="token string">static</span>'
			'<span class="token string">text</span>' text
		'<span class="token string">phrase</span>'
			'<span class="token string">phrase</span>' [ <span class="token operator">phrase</span> ] reference
		'<span class="token string">configuration</span>'
			'<span class="token string">context</span>' component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">text</span>'
					'<span class="token string">bound text</span>' [ <span class="token operator">=</span> ] reference
				'<span class="token string">number</span>'
					'<span class="token string">number</span>' [ <span class="token operator">configuration</span> <span class="token operator">#</span> ] reference
					'<span class="token string">format</span>' stategroup (
						'<span class="token string">no</span>'
						'<span class="token string">yes</span>' [ <span class="token operator">format</span> ]
							'<span class="token string">formatter</span>' reference
					)
			)
		'<span class="token string">widget binding</span>'
			'<span class="token string">context</span>' component <a href="#grammar-rule--bound-context-selection">'bound context selection'</a>
			'<span class="token string">type</span>' stategroup (
				'<span class="token string">text</span>'
					'<span class="token string">type</span>' stategroup (
						'<span class="token string">key</span>' [ <span class="token operator">.key</span> ]
						'<span class="token string">reference</span>' [ <span class="token operator">></span> ]
							'<span class="token string">property</span>' reference
						'<span class="token string">text</span>' [ <span class="token operator">:</span> ]
							'<span class="token string">property</span>' reference
					)
					'<span class="token string">format</span>' stategroup (
						'<span class="token string">no</span>'
						'<span class="token string">yes</span>' [ <span class="token operator">format</span> ]
							'<span class="token string">formatter</span>' reference
					)
				'<span class="token string">number</span>' [ <span class="token operator">#</span> ]
					'<span class="token string">property</span>' reference
					'<span class="token string">format</span>' stategroup (
						'<span class="token string">no</span>'
						'<span class="token string">yes</span>' [ <span class="token operator">format</span> ]
							'<span class="token string">formatter</span>' reference
					)
			)
	)
</pre>
</div>
</div>

{: #grammar-rule--string-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">string list</span>'
	'<span class="token string">text binding</span>' component <a href="#grammar-rule--text-binding">'text binding'</a>
	'<span class="token string">has steps</span>' stategroup (
		'<span class="token string">no</span>'
		'<span class="token string">yes</span>' [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>' component <a href="#grammar-rule--string-list">'string list'</a>
	)
</pre>
</div>
</div>
