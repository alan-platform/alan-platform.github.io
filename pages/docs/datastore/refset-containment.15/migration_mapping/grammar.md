---
layout: "doc"
origin: "datastore"
language: "migration_mapping"
version: "refset-containment.15"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': [ <span class="token operator">root</span> ] group {
	'<span class="token string">create root</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
	'<span class="token string">assignment</span>': [ <span class="token operator">=</span> <span class="token operator">root</span> <span class="token operator">as</span> <span class="token operator">$</span> ] component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
	'<span class="token string">root</span>': component <a href="#grammar-rule--node-mapping">'node mapping'</a>
}
</pre>
</div>
</div>
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
/* data context information */
</pre>
</div>
</div>

{: #grammar-rule--context-creation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context creation</span>' { }
/* execution context information */
</pre>
</div>
</div>

{: #grammar-rule--unguaranteed-operation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">unguaranteed operation</span>' {
	'<span class="token string">annotate</span>': [ <span class="token operator"><!</span>, <span class="token operator">!></span> ] stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">annotation</span>': text
		}
		'<span class="token string">no</span>' { }
	)
}
/* static data descriptors */
</pre>
</div>
</div>

{: #grammar-rule--number-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number list</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">single</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">range</span>' {
			'<span class="token string">begin</span>': integer
			'<span class="token string">end</span>': [ <span class="token operator">-</span> ] integer
		}
	)
	'<span class="token string">has more</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--number-list">'number list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text list</span>' {
	'<span class="token string">value</span>': text
	'<span class="token string">has more</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--text-list">'text list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
/* variable stack */
</pre>
</div>
</div>

{: #grammar-rule--variable-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable selector</span>' {
	'<span class="token string">stack</span>': stategroup (
		'<span class="token string">non-empty</span>' {
			'<span class="token string">select</span>': stategroup (
				'<span class="token string">this</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">parent</span>' { [ <span class="token operator">$^</span> ]
					'<span class="token string">tail</span>': component <a href="#grammar-rule--variable-selector">'variable selector'</a>
				}
				'<span class="token string">partition</span>' {
					'<span class="token string">select</span>': stategroup (
						'<span class="token string">key</span>' { [ <span class="token operator">$key</span> ] }
						'<span class="token string">set</span>' { [ <span class="token operator">$set</span> ] }
					)
				}
				'<span class="token string">branch</span>' { [ <span class="token operator">$</span> ]
					'<span class="token string">branch</span>': reference
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: context</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--number }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: number</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--text }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: text</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--regexp }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: regexp</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--array }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: array</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--partition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: partition</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment--block }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment: block</span>' {
	'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">context</span>' { [ <span class="token operator">=</span> ]
				'<span class="token string">expression</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
				'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
			}
			'<span class="token string">array</span>' { [ <span class="token operator">:</span> <span class="token operator">array</span> <span class="token operator">=</span> ]
				'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
				'<span class="token string">transformation</span>': stategroup (
					'<span class="token string">none</span>' { [ <span class="token operator">on</span> ]
						'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
					}
					'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
						'<span class="token string">create bucket</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
					}
				)
				'<span class="token string">index</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
					'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
				}
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--array">'variable assignment: array'</a>
			}
			'<span class="token string">regexp</span>' { [ <span class="token operator">:</span> <span class="token operator">regexp</span> ]
				'<span class="token string">regexp</span>': [ <span class="token operator">=</span> ] reference
				'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				'<span class="token string">value</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--regexp">'variable assignment: regexp'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">:</span> <span class="token operator">number</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--number">'variable assignment: number'</a>
			}
			'<span class="token string">text</span>' { [ <span class="token operator">:</span> <span class="token operator">text</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--text">'variable assignment: text'</a>
			}
		)
	}
}
/* type specific context selection */
</pre>
</div>
</div>

{: #grammar-rule--context-selector-recursive }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context selector recursive</span>' {
	'<span class="token string">step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span>, <span class="token operator">*</span> ] reference
				}
				'<span class="token string">entry</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
						'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
						'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
						'<span class="token string">expression</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
					}
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
			)
			'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
			'<span class="token string">optional assignment</span>': stategroup (
				'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
				}
				'<span class="token string">skip</span>' { }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--context-selector-recursive">'context selector recursive'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--context-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context selector</span>' {
	'<span class="token string">source</span>': stategroup (
		'<span class="token string">stack</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--variable-selector">'variable selector'</a>
		}
		'<span class="token string">array</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">predecessor</span>' { [ <span class="token operator">predecessor</span> ] }
				'<span class="token string">successor</span>' { [ <span class="token operator">successor</span> ] }
			)
			'<span class="token string">key expression</span>': [ <span class="token operator">of</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">selection</span>': [ <span class="token operator">in</span> ] component <a href="#grammar-rule--variable-selector">'variable selector'</a>
			'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
		}
	)
	'<span class="token string">steps</span>': component <a href="#grammar-rule--context-selector-recursive">'context selector recursive'</a>
}
/* generic sub expressions */
</pre>
</div>
</div>

{: #grammar-rule--regexp-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">regexp selector</span>' {
	'<span class="token string">source</span>': stategroup (
		'<span class="token string">stack</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--variable-selector">'variable selector'</a>
		}
		'<span class="token string">inline</span>' { [ <span class="token operator">inline</span> ]
			'<span class="token string">regexp</span>': reference
			'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
			'<span class="token string">value</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--date-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">date expression</span>' {
	'<span class="token string">year</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">calendar</span>' {
			'<span class="token string">month</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">day</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">week</span>' { [ <span class="token operator">W</span> ]
			'<span class="token string">week</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">day of week</span>': stategroup (
				'<span class="token string">monday</span>' { [ <span class="token operator">Monday</span> ] }
				'<span class="token string">tuesday</span>' { [ <span class="token operator">Tuesday</span> ] }
				'<span class="token string">wednesday</span>' { [ <span class="token operator">Wednesday</span> ] }
				'<span class="token string">thursday</span>' { [ <span class="token operator">Thursday</span> ] }
				'<span class="token string">friday</span>' { [ <span class="token operator">Friday</span> ] }
				'<span class="token string">saturday</span>' { [ <span class="token operator">Saturday</span> ] }
				'<span class="token string">sunday</span>' { [ <span class="token operator">Sunday</span> ] }
			)
		}
		'<span class="token string">ordinal</span>' {
			'<span class="token string">day</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--time-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">time expression</span>' {
	'<span class="token string">hour</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
	'<span class="token string">minute</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
	'<span class="token string">second</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--number-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression list</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
	'<span class="token string">has more</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--number-expression-list">'number expression list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">convert text</span>' { [ <span class="token operator">to-number</span> ]
			'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
			'<span class="token string">value</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
		}
		'<span class="token string">cast to positive number</span>' { [ <span class="token operator">to-positive</span> ]
			'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
			'<span class="token string">value</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">convert date</span>' { [ <span class="token operator">to-date</span> ]
			'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
			'<span class="token string">selection</span>': component <a href="#grammar-rule--regexp-selector">'regexp selector'</a>
			'<span class="token string">components</span>': [ <span class="token operator">where</span> ] group {
				'<span class="token string">year</span>': [ <span class="token operator">year</span> <span class="token operator">=</span> ] reference
				'<span class="token string">offset</span>': stategroup (
					'<span class="token string">month based</span>' {
						'<span class="token string">month</span>': [ <span class="token operator">month</span> <span class="token operator">=</span> ] reference
						'<span class="token string">day of month</span>': [ <span class="token operator">day</span> <span class="token operator">=</span> ] reference
					}
					'<span class="token string">week based</span>' {
						'<span class="token string">week</span>': [ <span class="token operator">week</span> <span class="token operator">=</span> ] reference
						'<span class="token string">day of week</span>': [ <span class="token operator">day</span> <span class="token operator">=</span> ] stategroup (
							'<span class="token string">monday</span>' { [ <span class="token operator">Monday</span> ] }
							'<span class="token string">tuesday</span>' { [ <span class="token operator">Tuesday</span> ] }
							'<span class="token string">wednesday</span>' { [ <span class="token operator">Wednesday</span> ] }
							'<span class="token string">thursday</span>' { [ <span class="token operator">Thursday</span> ] }
							'<span class="token string">friday</span>' { [ <span class="token operator">Friday</span> ] }
							'<span class="token string">saturday</span>' { [ <span class="token operator">Saturday</span> ] }
							'<span class="token string">sunday</span>' { [ <span class="token operator">Sunday</span> ] }
						)
					}
				)
			}
		}
		'<span class="token string">convert date and time</span>' { [ <span class="token operator">to-datetime</span> ]
			'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
			'<span class="token string">selection</span>': component <a href="#grammar-rule--regexp-selector">'regexp selector'</a>
			'<span class="token string">components</span>': [ <span class="token operator">where</span> ] group {
				'<span class="token string">year</span>': [ <span class="token operator">year</span> <span class="token operator">=</span> ] reference
				'<span class="token string">month</span>': [ <span class="token operator">month</span> <span class="token operator">=</span> ] reference
				'<span class="token string">day of month</span>': [ <span class="token operator">day</span> <span class="token operator">=</span> ] reference
				'<span class="token string">hour</span>': [ <span class="token operator">hour</span> <span class="token operator">=</span> ] reference
				'<span class="token string">minute</span>': [ <span class="token operator">minute</span> <span class="token operator">=</span> ] reference
				'<span class="token string">second</span>': [ <span class="token operator">second</span> <span class="token operator">=</span> ] reference
			}
		}
		'<span class="token string">make date</span>' { [ <span class="token operator">make-date</span> ]
			'<span class="token string">date</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--date-expression">'date expression'</a>
		}
		'<span class="token string">make date time</span>' { [ <span class="token operator">make-date-time</span> ]
			'<span class="token string">date</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--date-expression">'date expression'</a>
			'<span class="token string">time</span>': [ <span class="token operator">T</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--time-expression">'time expression'</a>
		}
		'<span class="token string">make time</span>' { [ <span class="token operator">make-time</span> ]
			'<span class="token string">time</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--time-expression">'time expression'</a>
		}
		'<span class="token string">from context</span>' {
			'<span class="token string">merge operation</span>': stategroup (
				'<span class="token string">none</span>' { }
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">shared value</span>' { [ <span class="token operator">shared</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
				'<span class="token string">max value</span>' { [ <span class="token operator">max</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
				'<span class="token string">min value</span>' { [ <span class="token operator">min</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
			)
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">from variable</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--variable-selector">'variable selector'</a>
		}
		'<span class="token string">conditional</span>' {
			'<span class="token string">merge operation</span>': stategroup (
				'<span class="token string">none</span>' { [ <span class="token operator">switch</span> ] }
				'<span class="token string">shared value</span>' { [ <span class="token operator">switch-shared</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
			)
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">predecessor</span>' = predecessor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">optional variable assignment</span>': stategroup (
					'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
						'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
						'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					}
					'<span class="token string">skip</span>' { }
				)
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
			}
			'<span class="token string">has branch</span>': stategroup = node-switch .'<span class="token string">branches</span>' (
				| nodes = '<span class="token string">yes</span>' { '<span class="token string">last</span>' = last }
				| none  = '<span class="token string">no</span>'
			)
		}
		'<span class="token string">unary operation</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">additive inverse</span>' { [ <span class="token operator">-</span> ] }
			)
			'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">list operation</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
			)
			'<span class="token string">list</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--number-expression-list">'number expression list'</a>
		}
		'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
			'<span class="token string">left</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">right</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">static value</span>' {
			'<span class="token string">value</span>': integer
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--date-pattern }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">date pattern</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">text</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
		}
		'<span class="token string">year</span>' { [ <span class="token operator">YYYY</span> ] }
		'<span class="token string">month</span>' { [ <span class="token operator">MM</span> ] }
		'<span class="token string">day of month</span>' { [ <span class="token operator">DD</span> ] }
		'<span class="token string">week</span>' { [ <span class="token operator">WW</span> ] }
		'<span class="token string">day of week</span>' { [ <span class="token operator">D</span> ] }
		'<span class="token string">day of year</span>' { [ <span class="token operator">DDD</span> ] }
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--date-pattern">'date pattern'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--time-pattern }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">time pattern</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">text</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
		}
		'<span class="token string">hour</span>' { [ <span class="token operator">hh</span> ] }
		'<span class="token string">minute</span>' { [ <span class="token operator">mm</span> ] }
		'<span class="token string">second</span>' { [ <span class="token operator">ss</span> ] }
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--time-pattern">'time pattern'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-expression--concatenate }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression: concatenate</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
	'<span class="token string">has more</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--text-expression--concatenate">'text expression: concatenate'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">convert number</span>' { [ <span class="token operator">to-text</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">format date</span>' { [ <span class="token operator">format-date</span> ]
			'<span class="token string">date</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--date-pattern">'date pattern'</a>
			'<span class="token string">value</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">format date and time</span>' { [ <span class="token operator">format-date-time</span> ]
			'<span class="token string">date</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--date-pattern">'date pattern'</a>
			'<span class="token string">time</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--time-pattern">'time pattern'</a>
			'<span class="token string">value</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">format time</span>' { [ <span class="token operator">format-time</span> ]
			'<span class="token string">time</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--time-pattern">'time pattern'</a>
			'<span class="token string">value</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">from context</span>' {
			'<span class="token string">merge operation</span>': stategroup (
				'<span class="token string">none</span>' { }
				'<span class="token string">join</span>' { [ <span class="token operator">join</span> ]
					'<span class="token string">separator</span>': text
				}
				'<span class="token string">shared value</span>' { [ <span class="token operator">shared</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
			)
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">from regexp</span>' { [ <span class="token operator">regexp</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--regexp-selector">'regexp selector'</a>
			'<span class="token string">capture</span>': [ <span class="token operator">@</span> ] reference
		}
		'<span class="token string">from variable</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--variable-selector">'variable selector'</a>
		}
		'<span class="token string">conditional</span>' {
			'<span class="token string">merge operation</span>': stategroup (
				'<span class="token string">none</span>' { [ <span class="token operator">switch</span> ] }
				'<span class="token string">shared value</span>' { [ <span class="token operator">switch-shared</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
			)
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">optional variable assignment</span>': stategroup (
					'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
						'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
						'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					}
					'<span class="token string">skip</span>' { }
				)
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
			}
		}
		'<span class="token string">concatenation</span>' { [ <span class="token operator">concat</span> ]
			'<span class="token string">expressions</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--text-expression--concatenate">'text expression: concatenate'</a>
		}
		'<span class="token string">static value</span>' {
			'<span class="token string">value</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--boolean-expression--candidates }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">boolean expression: candidates</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
	'<span class="token string">has more</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--boolean-expression--candidates">'boolean expression: candidates'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--boolean-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">boolean expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">logic operation</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">and</span>' { [ <span class="token operator">and</span> ] }
				'<span class="token string">or</span>' { [ <span class="token operator">or</span> ] }
			)
			'<span class="token string">expressions</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--boolean-expression--candidates">'boolean expression: candidates'</a>
		}
		'<span class="token string">compare number</span>' {
			'<span class="token string">sub type</span>': stategroup (
				'<span class="token string">binary operation</span>' {
					'<span class="token string">left</span>': [ <span class="token operator">#</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">equal</span>' { [ <span class="token operator">==</span> ] }
						'<span class="token string">greater</span>' { [ <span class="token operator">></span> ] }
						'<span class="token string">greater equal</span>' { [ <span class="token operator">>=</span> ] }
						'<span class="token string">smaller</span>' { [ <span class="token operator"><</span> ] }
						'<span class="token string">smaller equal</span>' { [ <span class="token operator"><=</span> ] }
					)
					'<span class="token string">right</span>': [ <span class="token operator">#</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
				}
				'<span class="token string">set operation</span>' { [ <span class="token operator">is</span> ]
					'<span class="token string">find</span>': [ <span class="token operator">#</span>, <span class="token operator">in</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
					'<span class="token string">in</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--number-list">'number list'</a>
				}
			)
		}
		'<span class="token string">compare text</span>' {
			'<span class="token string">sub type</span>': stategroup (
				'<span class="token string">binary operation</span>' {
					'<span class="token string">left</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">equals</span>' { [ <span class="token operator">equals</span> ] }
						'<span class="token string">starts with</span>' { [ <span class="token operator">starts-with</span> ] }
						'<span class="token string">ends with</span>' { [ <span class="token operator">ends-with</span> ] }
					)
					'<span class="token string">right</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
				}
				'<span class="token string">set operation</span>' {
					'<span class="token string">find</span>': [ <span class="token operator">is</span>, <span class="token operator">in</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
					'<span class="token string">in</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--text-list">'text list'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection selector</span>' {
	'<span class="token string">variable type</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] stategroup (
		'<span class="token string">context</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">create row</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
		}
		'<span class="token string">array</span>' { [ <span class="token operator">array</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--variable-selector">'variable selector'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">map</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--collection-selector">'collection selector'</a>
			'<span class="token string">optional assignment</span>': stategroup (
				'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
				}
				'<span class="token string">skip</span>' { }
			)
			'<span class="token string">mapping</span>': component <a href="#grammar-rule--collection-expression">'collection expression'</a>
		}
		'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--collection-selector">'collection selector'</a>
			'<span class="token string">index</span>': group { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
				'<span class="token string">expression</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
			}
			'<span class="token string">create set</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
			'<span class="token string">optional assignment</span>': stategroup (
				'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">(</span> <span class="token operator">$key</span> <span class="token operator">,</span> <span class="token operator">$set</span> <span class="token operator">)</span> ]
					'<span class="token string">key assignment</span>': component <a href="#grammar-rule--variable-assignment--text">'variable assignment: text'</a>
					'<span class="token string">set assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--partition">'variable assignment: partition'</a>
				}
				'<span class="token string">skip</span>' { }
			)
			'<span class="token string">mapping</span>': component <a href="#grammar-rule--collection-expression">'collection expression'</a>
		}
		'<span class="token string">conditional</span>' {
			'<span class="token string">merge operation</span>': stategroup (
				'<span class="token string">none</span>' { [ <span class="token operator">switch</span> ] }
				'<span class="token string">shared value</span>' { [ <span class="token operator">switch-shared</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
			)
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">optional variable assignment</span>': stategroup (
					'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
						'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
						'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					}
					'<span class="token string">skip</span>' { }
				)
				'<span class="token string">expression</span>': component <a href="#grammar-rule--collection-expression">'collection expression'</a>
			}
		}
		'<span class="token string">new entry</span>' { [ <span class="token operator">=</span> ]
			'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-mapping">'node mapping'</a>
		}
		'<span class="token string">sub expression</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">list</span>': component <a href="#grammar-rule--collection-expression-list">'collection expression list'</a>
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection expression list</span>' {
	'<span class="token string">has expressions</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--collection-expression">'collection expression'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-expression-list">'collection expression list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection mapping</span>' { [ <span class="token operator">=</span> ]
	'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
	'<span class="token string">expression</span>': component <a href="#grammar-rule--collection-expression">'collection expression'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--state-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state mapping</span>' { [ <span class="token operator">=</span> ]
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">panic</span>' { [ <span class="token operator">panic</span> ]
			'<span class="token string">comment</span>': text
		}
		'<span class="token string">conditional</span>' { [ <span class="token operator">match</span> ]
			'<span class="token string">condition</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
			'<span class="token string">on true</span>': [ <span class="token operator">|</span> <span class="token operator">true</span> ] component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			'<span class="token string">on false</span>': [ <span class="token operator">|</span> <span class="token operator">false</span> ] component <a href="#grammar-rule--state-mapping">'state mapping'</a>
		}
		'<span class="token string">enrich</span>' { [ <span class="token operator">try</span> ]
			'<span class="token string">try assign</span>': component <a href="#grammar-rule--variable-assignment--block">'variable assignment: block'</a>
			'<span class="token string">on success</span>': [ <span class="token operator">|</span> <span class="token operator">success</span> ] component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			'<span class="token string">on failure</span>': [ <span class="token operator">|</span> <span class="token operator">failure</span> ] component <a href="#grammar-rule--state-mapping">'state mapping'</a>
		}
		'<span class="token string">context switch</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">on singular</span>': [ <span class="token operator">|</span> <span class="token operator">singular</span> ] group {
				'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			}
			'<span class="token string">on plural</span>': [ <span class="token operator">|</span> <span class="token operator">plural</span> ] group {
				'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
				'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			}
		}
		'<span class="token string">from context</span>' {
			'<span class="token string">merge operation</span>': stategroup (
				'<span class="token string">none</span>' { [ <span class="token operator">switch</span> ] }
				'<span class="token string">shared value</span>' { [ <span class="token operator">switch-shared</span> ]
					'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
				}
			)
			'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">mappings</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">optional variable assignment</span>': stategroup (
					'<span class="token string">assign</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
						'<span class="token string">create context</span>': component <a href="#grammar-rule--context-creation">'context creation'</a>
						'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					}
					'<span class="token string">skip</span>' { }
				)
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			}
		}
		'<span class="token string">from array</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">first</span>' { [ <span class="token operator">first</span> ] }
				'<span class="token string">last</span>' { [ <span class="token operator">last</span> ] }
			)
			'<span class="token string">selection</span>': [ <span class="token operator">in</span> ] component <a href="#grammar-rule--variable-selector">'variable selector'</a>
			'<span class="token string">optional variable assignment</span>': stategroup (
				'<span class="token string">assign</span>' {
					'<span class="token string">assignment</span>': [ <span class="token operator">as</span> <span class="token operator">$</span> ] component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
				}
				'<span class="token string">skip</span>' { }
			)
			'<span class="token string">on success</span>': [ <span class="token operator">|</span> <span class="token operator">success</span> ] component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			'<span class="token string">on failure</span>': [ <span class="token operator">|</span> <span class="token operator">failure</span> ] component <a href="#grammar-rule--state-mapping">'state mapping'</a>
		}
		'<span class="token string">set state</span>' {
			'<span class="token string">state</span>': reference
			'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-mapping">'node mapping'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">define block</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">block</span>': component <a href="#grammar-rule--variable-assignment--block">'variable assignment: block'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">optional binding</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">bind</span>' {
						'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
						'<span class="token string">create context</span>': [ <span class="token operator">as</span> ] component <a href="#grammar-rule--context-creation">'context creation'</a>
						'<span class="token string">assignment</span>': [ <span class="token operator">$</span> ] component <a href="#grammar-rule--variable-assignment--context">'variable assignment: context'</a>
					}
					'<span class="token string">skip</span>' { }
				)
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-mapping">'node mapping'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--collection-mapping">'collection mapping'</a>
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--state-mapping">'state mapping'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">value source</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">clock</span>' { [ <span class="token operator">now</span> ] }
					'<span class="token string">source</span>' {
						'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
					}
				)
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">value source</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">static</span>' { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
						'<span class="token string">token</span>': text
						'<span class="token string">extension</span>': [ <span class="token operator">,</span> ] text
					}
					'<span class="token string">context</span>' {
						'<span class="token string">merge operation</span>': [ <span class="token operator">/</span> ] stategroup (
							'<span class="token string">none</span>' { }
							'<span class="token string">shared value</span>' { [ <span class="token operator">shared</span> ]
								'<span class="token string">unguaranteed operation</span>': component <a href="#grammar-rule--unguaranteed-operation">'unguaranteed operation'</a>
							}
						)
						'<span class="token string">selection</span>': component <a href="#grammar-rule--context-selector">'context selector'</a>
						'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>
