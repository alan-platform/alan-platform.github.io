---
layout: doc
origin: connector
language: processor
version: 31.2
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--library }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library</span>': dictionary { [ <span class="token operator">define</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">schema</span>' {
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">pattern</span>' { [ <span class="token operator">pattern</span> ]
			'<span class="token string">rule</span>': component <a href="#grammar-rule--pattern-rule">'pattern rule'</a>
		}
		'<span class="token string">locale</span>' { [ <span class="token operator">locale</span> ]
			'<span class="token string">positive sign</span>': [ <span class="token operator">positive-sign:</span> ] text
			'<span class="token string">negative sign</span>': [ <span class="token operator">negative-sign:</span> ] text
			'<span class="token string">decimal point</span>': [ <span class="token operator">decimal-point:</span> ] text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--custom-locale }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom locale</span>': stategroup (
	'<span class="token string">yes</span>' {
		'<span class="token string">default</span>': [ <span class="token operator">default-locale:</span> ] reference
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

{: #grammar-rule--archetype }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">archetype</span>': stategroup (
	'<span class="token string">scheduled provider</span>' { [ <span class="token operator">provider</span> ]
		'<span class="token string">main routine</span>': component <a href="#grammar-rule--statement">'statement'</a>
		'<span class="token string">command routines</span>': dictionary { [ <span class="token operator">command</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">execute</span>' {
					'<span class="token string">statement</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">schedule</span>' { [ <span class="token operator">schedule</span> ] }
			)
		}
	}
	'<span class="token string">consumer</span>' { [ <span class="token operator">consumer</span> ]
		'<span class="token string">context keys</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">routines</span>': dictionary { [ <span class="token operator">routine</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">binding</span>': [ <span class="token operator">on</span> ] stategroup (
				'<span class="token string">interface</span>' {
					'<span class="token string">binding</span>': stategroup (
						'<span class="token string">event</span>' {
							'<span class="token string">event</span>': [ <span class="token operator">event</span> ] reference
						}
						'<span class="token string">node</span>' { }
					)
					'<span class="token string">named type</span>': component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
				}
				'<span class="token string">webhook</span>' { [ <span class="token operator">webhook</span> ] }
			)
			'<span class="token string">statement</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
	}
)
</pre>
</div>
</div>
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
/* localization support */
</pre>
</div>
</div>

{: #grammar-rule--locale-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">locale selector</span>' {
	'<span class="token string">locale</span>': stategroup (
		'<span class="token string">custom</span>' {
			'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] reference
		}
		'<span class="token string">default</span>' { }
	)
}
/* interface bindings */
</pre>
</div>
</div>

{: #grammar-rule--interface-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface type path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">[]</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' { }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--interface-type-path">'interface type path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--interface-named-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface named path</span>' {
	'<span class="token string">segments</span>': dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has previous</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">previous</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">steps</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--interface-type-path">'interface type path'</a>
	}
	'<span class="token string">has segment</span>': stategroup = node-switch .'<span class="token string">segments</span>' (
		| nodes = '<span class="token string">yes</span>' {
			'<span class="token string">first</span>' = first
			'<span class="token string">last</span>' = last
		}
		| none  = '<span class="token string">no</span>'
	)
}
/* type system */
</pre>
</div>
</div>

{: #grammar-rule--schema-scalar-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema scalar type</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">boolean</span>' { [ <span class="token operator">boolean</span> ] }
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
			'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
		'<span class="token string">choice</span>' { [ <span class="token operator">choice</span> ]
			'<span class="token string">options</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">base type</span>': stategroup (
					'<span class="token string">integer</span>' {
						'<span class="token string">value</span>': [ <span class="token operator">:</span> ] integer
					}
					'<span class="token string">text</span>' { }
				)
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schema-complex-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema complex type</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">any</span>' { [ <span class="token operator">any</span> ] }
		'<span class="token string">library</span>' {
			'<span class="token string">schema</span>': reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">headless</span>' { [ <span class="token operator">headless</span> ]
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">list</span>' { [ <span class="token operator">list</span> ]
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">scalar</span>' {
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-scalar-type">'schema scalar type'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schema-node-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema node type</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">{</span>, <span class="token operator">}</span> ] dictionary {
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has attributes</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator"><</span>, <span class="token operator">></span> ]
				'<span class="token string">attributes</span>': dictionary {
					'<span class="token string">has next</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">type</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--schema-scalar-type">'schema scalar type'</a>
				}
				'<span class="token string">filters</span>': dictionary { [ <span class="token operator">where</span> ]
					'<span class="token string">has next</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">value</span>': [ <span class="token operator">is</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
				}
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">is optional</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">optional</span> ] }
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
	}
}
/* execution state */
</pre>
</div>
</div>

{: #grammar-rule--stack-block }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stack block</span>' {
	'<span class="token string">values</span>': dictionary { [ <span class="token operator">let</span> <span class="token operator">$</span> ]
		'<span class="token string">has previous</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">previous</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">inferred</span>' {
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
			}
			'<span class="token string">schema</span>' {
				'<span class="token string">schema</span>': [ <span class="token operator">as</span> ] component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
				'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			}
			'<span class="token string">lambda</span>' {
				'<span class="token string">lambda</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--lambda-definition">'lambda definition'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--stack-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stack selector</span>' {
	'<span class="token string">stack</span>': stategroup (
		'<span class="token string">non-empty</span>' {
			'<span class="token string">select</span>': stategroup (
				'<span class="token string">this frame</span>' {
					'<span class="token string">value</span>': [ <span class="token operator">$</span> ] reference
				}
				'<span class="token string">parent frame</span>' {
					'<span class="token string">tail</span>': [ <span class="token operator">^</span> ] component <a href="#grammar-rule--stack-selector">'stack selector'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--target-type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target type path step</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">command</span>' {
					'<span class="token string">command</span>': [ <span class="token operator">:</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--target-type-path-step">'target type path step'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--target-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target type path</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
		'<span class="token string">absolute</span>' {
			'<span class="token string">root</span>': stategroup (
				'<span class="token string">interface</span>' { [ <span class="token operator">interface</span> ] }
				'<span class="token string">schema</span>' {
					'<span class="token string">schema</span>': reference
				}
				'<span class="token string">response</span>' { [ <span class="token operator">network</span> ] }
				'<span class="token string">headers</span>' { [ <span class="token operator">headers</span> ] }
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
			'<span class="token string">steps</span>': component <a href="#grammar-rule--target-type-path-step">'target type path step'</a>
		}
		'<span class="token string">relative</span>' {
			'<span class="token string">steps</span>': component <a href="#grammar-rule--target-type-path-step">'target type path step'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type path step</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--type-path-step">'type path step'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type path</span>' {
	'<span class="token string">root</span>': stategroup (
		'<span class="token string">interface</span>' { [ <span class="token operator">interface</span> ] }
		'<span class="token string">schema</span>' {
			'<span class="token string">schema</span>': reference
		}
	)
	'<span class="token string">steps</span>': component <a href="#grammar-rule--type-path-step">'type path step'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--type-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type definition</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">boolean</span>' { [ <span class="token operator">boolean</span> ] }
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
		'<span class="token string">file</span>' { [ <span class="token operator">file</span> ] }
		'<span class="token string">calendar</span>' {
			'<span class="token string">date</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">date</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">time</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">time</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">optional</span>' { [ <span class="token operator">optional</span> ]
			'<span class="token string">sub type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">plural</span>' { [ <span class="token operator">plural</span> ]
			'<span class="token string">sub type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">network</span>' { [ <span class="token operator">network</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">request</span>' { [ <span class="token operator">request</span> ] }
				'<span class="token string">response</span>' { [ <span class="token operator">response</span> ] }
			)
		}
		'<span class="token string">lambda</span>' {
			'<span class="token string">signature</span>': component <a href="#grammar-rule--lambda-signature">'lambda signature'</a>
		}
		'<span class="token string">type</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--type-path">'type path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-signature }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda signature</span>' { [ <span class="token operator">lambda</span> ]
	'<span class="token string">parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--type-definition">'type definition'</a>
	}
	'<span class="token string">target</span>': stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--target-type-path">'target type path'</a>
		}
		'<span class="token string">inferred</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--lambda }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda</span>' {
	'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-arguments }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda arguments</span>' {
	'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
			'<span class="token string">signature</span>' { [ <span class="token operator">lambda</span> <span class="token operator">=></span> ]
				'<span class="token string">lambda</span>': component <a href="#grammar-rule--lambda">'lambda'</a>
			}
			'<span class="token string">choice</span>' {
				'<span class="token string">option</span>': [ <span class="token operator">option</span> ] reference
			}
			'<span class="token string">value</span>' {
				'<span class="token string">value</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda definition</span>' {
	'<span class="token string">signature</span>': component <a href="#grammar-rule--lambda-signature">'lambda signature'</a>
	'<span class="token string">lambda</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--lambda">'lambda'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-selector-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda selector step</span>' {
	'<span class="token string">step</span>': stategroup (
		'<span class="token string">parent</span>' {
			'<span class="token string">tail</span>': [ <span class="token operator">^</span> ] component <a href="#grammar-rule--lambda-selector-step">'lambda selector step'</a>
		}
		'<span class="token string">this</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">recurs</span>' {
			'<span class="token string">steps</span>': component <a href="#grammar-rule--lambda-selector-step">'lambda selector step'</a>
		}
		'<span class="token string">new</span>' {
			'<span class="token string">lambda</span>': component <a href="#grammar-rule--lambda-definition">'lambda definition'</a>
		}
		'<span class="token string">stored</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
	)
}
/* target mapping */
/* implementation */
</pre>
</div>
</div>

{: #grammar-rule--decimal-import-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">decimal import rule</span>' {
	'<span class="token string">decimal point translation</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">places</span>': [ <span class="token operator"><<</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--authentication }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">authentication</span>' {
	'<span class="token string">has authentication</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">authentication</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">username</span>': [ <span class="token operator">username:</span> ] component <a href="#grammar-rule--promise">'promise'</a>
			'<span class="token string">password</span>': [ <span class="token operator">password:</span> ] component <a href="#grammar-rule--promise">'promise'</a>
		}
		'<span class="token string">no</span>' { }
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
	'<span class="token string">year</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">calendar</span>' {
			'<span class="token string">month</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
			'<span class="token string">day</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
		}
		'<span class="token string">week</span>' { [ <span class="token operator">W</span> ]
			'<span class="token string">week</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
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
			'<span class="token string">day</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
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
	'<span class="token string">hour</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">minute</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">second</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--pattern-rule-piece }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">pattern rule piece</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">pattern</span>' {
			'<span class="token string">capture</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
		}
		'<span class="token string">static</span>' {
			'<span class="token string">text</span>': text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--pattern-rule-piece">'pattern rule piece'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--pattern-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">pattern rule</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">parts</span>': dictionary {
		'<span class="token string">has next</span>': [ <span class="token operator">:</span> ] stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">pieces</span>': component <a href="#grammar-rule--pattern-rule-piece">'pattern rule piece'</a>
	}
	'<span class="token string">head</span>': reference = first
}
</pre>
</div>
</div>

{: #grammar-rule--format-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">format rule</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic</span>' {
			'<span class="token string">padding</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Select the justification and padding character.
					 * Zero padding can only be applied to decimals.
					 */
					'<span class="token string">justify</span>': stategroup (
						'<span class="token string">right zero</span>' { [ <span class="token operator">@zero</span> ] }
						'<span class="token string">right space</span>' { }
						'<span class="token string">left space</span>' { [ <span class="token operator">@left</span> ] }
					)
					/* Select the minimum amount of characters written.
					 * Longer values are not truncated.
					 */
					'<span class="token string">places</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
		}
		'<span class="token string">static</span>' {
			'<span class="token string">text</span>': text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--format-rule">'format rule'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promise-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise path</span>' {
	'<span class="token string">step</span>': stategroup (
		'<span class="token string">optional value</span>' { [ <span class="token operator">get</span> ] }
		'<span class="token string">entity lookup</span>' {
			'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--promise">'promise'</a>
		}
		'<span class="token string">file fetch</span>' {
			'<span class="token string">field</span>': stategroup (
				'<span class="token string">token</span>' { [ <span class="token operator">.token</span> ] }
				'<span class="token string">extension</span>' { [ <span class="token operator">.extension</span> ] }
			)
		}
		'<span class="token string">entity fetch</span>' {
			'<span class="token string">field</span>': stategroup (
				'<span class="token string">key</span>' { [ <span class="token operator">.key</span> ] }
				'<span class="token string">value</span>' { [ <span class="token operator">.value</span> ] }
			)
		}
		'<span class="token string">network fetch</span>' {
			'<span class="token string">field</span>': stategroup (
				/* request only */
				'<span class="token string">method</span>' { [ <span class="token operator">.method</span> ] }
				'<span class="token string">parameters</span>' { [ <span class="token operator">.parameters</span> ] }
				'<span class="token string">headers</span>' { [ <span class="token operator">.headers</span> ] }
				/* response only */
				'<span class="token string">status</span>' { [ <span class="token operator">.status</span> ] }
				/* shared */
				'<span class="token string">content</span>' { [ <span class="token operator">.content</span> ] }
			)
		}
		'<span class="token string">calendar fetch</span>' {
			'<span class="token string">part</span>': stategroup (
				'<span class="token string">date</span>' {
					'<span class="token string">field</span>': stategroup (
						'<span class="token string">year</span>' { [ <span class="token operator">.year</span> ] }
						'<span class="token string">month</span>' { [ <span class="token operator">.month</span> ] }
						'<span class="token string">day of month</span>' { [ <span class="token operator">.day-of-month</span> ] }
						'<span class="token string">day of year</span>' { [ <span class="token operator">.day-of-year</span> ] }
					)
				}
				'<span class="token string">time</span>' {
					'<span class="token string">field</span>': stategroup (
						'<span class="token string">hour</span>' { [ <span class="token operator">.hour</span> ] }
						'<span class="token string">minute</span>' { [ <span class="token operator">.minute</span> ] }
						'<span class="token string">second</span>' { [ <span class="token operator">.second</span> ] }
					)
				}
			)
		}
		'<span class="token string">node fetch</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">sub property</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] reference
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">interface choice</span>' {
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promise-chain }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise chain</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': stategroup (
				'<span class="token string">path</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--promise-path">'promise path'</a>
				}
				'<span class="token string">complex</span>' { [ <span class="token operator">=></span> ]
					'<span class="token string">type</span>': stategroup (
						/* type conversions */
						'<span class="token string">parse</span>' {
							'<span class="token string">as</span>': [ <span class="token operator">parse</span> <span class="token operator">as</span> ] stategroup (
								'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ]
									/* Parses a JSON object.
									 * On success it results in source-data and must first be passed to a decorator before it is usable.
									 */
								}
								'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ]
									/* Parses a XML document.
									 * On success it results in source-data and must first be passed to a decorator before it is usable.
									 */
								}
								'<span class="token string">ISO Date Time</span>' { [ <span class="token operator">ISODateTime</span> ]
									/* Parses an ISO-8601 date and time, however it must have at least Seconds accuracy. (source: https://en.wikipedia.org/wiki/ISO_8601)
									 * Combines an ISODate and ISOTime separated with T, but the Date and Time components must both be in the same format.
									 *  Calendar dates + Time: YYYYMMDDThhmmss[.sss] or YYYY-MM-DDThh:mm:ss[.sss]
									 *  Week dates + Time: YYYYWwwDThhmmss[.sss] or YYYY-Www-DThh:mm:ss[.sss]
									 *  Ordinal dates + Time: YYYYDDDThhmmss[.sss] or YYYY-DDDThh:mm:ss[.sss]
									 * In all cases the Time component may contain a Time Zone, when omitted local time is assumed.
									 * On success it results in a Alan DateTime.
									 */
								}
								'<span class="token string">ISO Date</span>' { [ <span class="token operator">ISODate</span> ]
									/* Parses an ISO-8601 date, however it must have Day accuracy. (source: https://en.wikipedia.org/wiki/ISO_8601)
									 *  Calendar dates: YYYYMMDD or YYYY-MM-DD
									 *  Week dates: YYYYWwwD or YYYY-Www-D
									 *  Ordinal dates: YYYYDDD or YYYY-DDD
									 * On success it results in a Alan Date.
									 */
								}
								'<span class="token string">ISO Time</span>' { [ <span class="token operator">ISOTime</span> ]
									/* Parses an ISO-8601 time, however it must have at least Seconds accuracy. (source: https://en.wikipedia.org/wiki/ISO_8601)
									 *  Time: hhmmss[.sss] or hh:mm:ss[.sss]
									 *   The fraction separated by a decimal point is allowed but discarded.
									 *  Time Zone: Z or ±hh or ±hhmm or ±hh:mm
									 *   The timezone is allowed but discarded.
									 * On success it results in the amount of seconds since midnight.
									 */
								}
								'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
									/* Parses a decimal value.
									 *  Decimal: [+-]d[.f]
									 *   Any number of digits can be provided, but the supported range is limited by the implementation.
									 *   An optional minus or plus sign is allowed before the first digit to set the sign.
									 *   Optionally no digits can be provided before the decimal point, which implies the value of 0.
									 *   The fraction separated by a decimal point is allowed and the amount of digits may differ from the `rule`,
									 *   but only the digits specified by `rule` are kept with possibly additional 0 digits introduced when insufficient precision was provided.
									 */
									'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
									'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
								}
								'<span class="token string">lines</span>' { [ <span class="token operator">lines</span> ]
									'<span class="token string">trim spaces</span>': stategroup (
										'<span class="token string">yes</span>' { [ <span class="token operator">trim</span>, <span class="token operator">spaces</span> ]
											'<span class="token string">locations</span>': stategroup (
												'<span class="token string">leading</span>' { [ <span class="token operator">leading</span> ] }
												'<span class="token string">trailing</span>' { [ <span class="token operator">trailing</span> ] }
												'<span class="token string">both</span>' { }
											)
										}
										'<span class="token string">no</span>' { }
									)
								}
								'<span class="token string">pattern</span>' { [ <span class="token operator">pattern</span> ]
									'<span class="token string">pattern</span>': stategroup (
										'<span class="token string">library</span>' {
											'<span class="token string">pattern</span>': reference
										}
										'<span class="token string">inline</span>' {
											'<span class="token string">rule</span>': component <a href="#grammar-rule--pattern-rule">'pattern rule'</a>
										}
									)
								}
							)
						}
						'<span class="token string">serialize</span>' {
							'<span class="token string">as</span>': [ <span class="token operator">serialize</span> <span class="token operator">as</span> ] stategroup (
								'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ] }
								'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ] }
								'<span class="token string">ISO Date Time</span>' { [ <span class="token operator">ISODateTime</span> ] }
								'<span class="token string">ISO Date</span>' { [ <span class="token operator">ISODate</span> ] }
								'<span class="token string">ISO Time</span>' { [ <span class="token operator">ISOTime</span> ] }
								'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
									'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
									'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
								}
							)
						}
						'<span class="token string">decorate</span>' {
							'<span class="token string">schema</span>': [ <span class="token operator">decorate</span> <span class="token operator">as</span> ] component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
						}
						'<span class="token string">https</span>' { [ <span class="token operator">HTTPS</span> ]
							'<span class="token string">server</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
							'<span class="token string">method</span>': stategroup (
								'<span class="token string">get</span>' { [ <span class="token operator">GET</span> ] }
								'<span class="token string">post</span>' { [ <span class="token operator">POST</span> ]
									'<span class="token string">content</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
								}
								'<span class="token string">put</span>' { [ <span class="token operator">PUT</span> ]
									'<span class="token string">content</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
								}
							)
							'<span class="token string">options</span>': group { dynamic-order
								'<span class="token string">has parameters</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">parameters:</span> ]
										'<span class="token string">parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
											'<span class="token string">has next</span>': stategroup = node-switch successor (
												| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
												| none = '<span class="token string">no</span>'
											)
											'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--promise">'promise'</a>
										}
										'<span class="token string">first</span>': reference = first
									}
									'<span class="token string">no</span>' { }
								)
								'<span class="token string">has custom headers</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">headers:</span> ]
										'<span class="token string">headers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
											'<span class="token string">has next</span>': stategroup = node-switch successor (
												| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
												| none = '<span class="token string">no</span>'
											)
											'<span class="token string">value</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--promise">'promise'</a>
										}
									}
									'<span class="token string">no</span>' { }
								)
								'<span class="token string">authentication</span>': component <a href="#grammar-rule--authentication">'authentication'</a>
							}
						}
						'<span class="token string">ftps</span>' { [ <span class="token operator">FTPS</span> ]
							'<span class="token string">server</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
							'<span class="token string">method</span>': stategroup (
								'<span class="token string">get</span>' { [ <span class="token operator">GET</span> ] }
								'<span class="token string">head</span>' { [ <span class="token operator">HEAD</span> ] }
								'<span class="token string">list</span>' { [ <span class="token operator">LIST</span> ] }
								'<span class="token string">put</span>' { [ <span class="token operator">PUT</span> ]
									'<span class="token string">content</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
								}
								'<span class="token string">delete</span>' { [ <span class="token operator">DELETE</span> ] }
							)
							'<span class="token string">options</span>': group { dynamic-order
								'<span class="token string">authentication</span>': component <a href="#grammar-rule--authentication">'authentication'</a>
								'<span class="token string">allow insecure connections</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">@allow-insecure</span> ] }
									'<span class="token string">no</span>' { }
								)
							}
						}
						'<span class="token string">smtps</span>' { [ <span class="token operator">SMTPS</span> ]
							'<span class="token string">server</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
							'<span class="token string">subject</span>': [ <span class="token operator">subject:</span> ] component <a href="#grammar-rule--promise">'promise'</a>
							'<span class="token string">from</span>': [ <span class="token operator">from:</span> ] component <a href="#grammar-rule--promise">'promise'</a>
							'<span class="token string">recipients</span>': [ <span class="token operator">recipients:</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] set {
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">to</span>' { [ <span class="token operator">TO:</span> ] }
									'<span class="token string">cc</span>' { [ <span class="token operator">CC:</span> ] }
								)
								'<span class="token string">recipient</span>': component <a href="#grammar-rule--promise">'promise'</a>
							}
							'<span class="token string">options</span>': group { dynamic-order
								'<span class="token string">authentication</span>': component <a href="#grammar-rule--authentication">'authentication'</a>
								'<span class="token string">send as mime</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">@mime-type:</span> ]
										'<span class="token string">type</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
									}
									'<span class="token string">no</span>' { }
								)
								'<span class="token string">allow insecure connections</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">@allow-insecure</span> ] }
									'<span class="token string">no</span>' { }
								)
								'<span class="token string">attachments</span>': dictionary { [ <span class="token operator">attachment:</span> ]
									'<span class="token string">data</span>': [ <span class="token operator">=</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
								}
							}
						}
						'<span class="token string">imaps</span>' { [ <span class="token operator">IMAPS</span> ]
							'<span class="token string">server</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
							'<span class="token string">method</span>': stategroup (
								'<span class="token string">get</span>' { [ <span class="token operator">GET</span> ]
									'<span class="token string">uid</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
								}
								'<span class="token string">search</span>' { [ <span class="token operator">SEARCH</span> ]
									/* Specifies the criteria to search for.
									 * See RFC-3501 section 6.4.4 for what is valid here.
									 */
									'<span class="token string">criteria</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
								}
							)
							'<span class="token string">options</span>': group {
								'<span class="token string">authentication</span>': component <a href="#grammar-rule--authentication">'authentication'</a>
								'<span class="token string">allow insecure connections</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">@allow-insecure</span> ] }
									'<span class="token string">no</span>' { }
								)
							}
						}
						'<span class="token string">convert</span>' {
							'<span class="token string">to</span>': [ <span class="token operator">to</span> ] stategroup (
								'<span class="token string">date</span>' { [ <span class="token operator">date</span> ] }
								'<span class="token string">date time</span>' { [ <span class="token operator">date-time</span> ] }
								'<span class="token string">time</span>' { [ <span class="token operator">time</span> ] }
							)
						}
						'<span class="token string">make</span>' { [ <span class="token operator">make</span> ]
							'<span class="token string">type</span>': stategroup (
								'<span class="token string">date</span>' { [ <span class="token operator">date</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
									'<span class="token string">date</span>': component <a href="#grammar-rule--date-expression">'date expression'</a>
								}
								'<span class="token string">date time</span>' { [ <span class="token operator">date-time</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
									'<span class="token string">date</span>': component <a href="#grammar-rule--date-expression">'date expression'</a>
									'<span class="token string">time</span>': [ <span class="token operator">T</span> ] component <a href="#grammar-rule--time-expression">'time expression'</a>
								}
								'<span class="token string">time</span>' { [ <span class="token operator">time</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
									'<span class="token string">time</span>': component <a href="#grammar-rule--time-expression">'time expression'</a>
								}
							)
						}
						/* compute new values */
						'<span class="token string">compare</span>' {
							'<span class="token string">type</span>': stategroup (
								'<span class="token string">equality</span>' { [ <span class="token operator">is</span> ] }
								'<span class="token string">relational</span>' {
									'<span class="token string">operator</span>': stategroup (
										'<span class="token string">smaller</span>' { [ <span class="token operator">less-than</span> ] }
										'<span class="token string">smaller equal</span>' { [ <span class="token operator">less-than</span> <span class="token operator">or</span> <span class="token operator">is</span> ] }
										'<span class="token string">greater</span>' { [ <span class="token operator">greater-than</span> ] }
										'<span class="token string">greater equal</span>' { [ <span class="token operator">greater-than</span> <span class="token operator">or</span> <span class="token operator">is</span> ] }
									)
								}
							)
							'<span class="token string">other</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
						}
						'<span class="token string">reduce</span>' {
							'<span class="token string">merge</span>': stategroup (
								'<span class="token string">value</span>' {
									'<span class="token string">merge type</span>': stategroup (
										'<span class="token string">shared</span>' { [ <span class="token operator">shared</span> ] }
										'<span class="token string">unique</span>' { [ <span class="token operator">unique</span> ] }
										'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
										'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
										'<span class="token string">join</span>' { [ <span class="token operator">join</span> ]
											'<span class="token string">separator</span>': stategroup (
												'<span class="token string">yes</span>' {
													'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
												}
												'<span class="token string">no</span>' { }
											)
										}
										'<span class="token string">logical and</span>' { [ <span class="token operator">and</span> ] }
										'<span class="token string">logical or</span>' { [ <span class="token operator">or</span> ] }
									)
									'<span class="token string">for each</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
								}
								'<span class="token string">meta</span>' {
									'<span class="token string">merge type</span>': stategroup (
										'<span class="token string">count</span>' { [ <span class="token operator">count</span> ] }
									)
								}
								'<span class="token string">filter</span>' { [ <span class="token operator">filter</span> ] }
							)
							'<span class="token string">filter</span>': stategroup (
								'<span class="token string">yes</span>' {
									'<span class="token string">filters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">where</span> ]
										'<span class="token string">has next</span>': stategroup = node-switch successor (
											| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
											| none = '<span class="token string">no</span>'
										)
										'<span class="token string">value</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
									}
								}
								'<span class="token string">no</span>' { }
							)
						}
						'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
							'<span class="token string">key</span>': [ <span class="token operator">on</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
						}
					)
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promise }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise</span>' {
	'<span class="token string">head</span>': stategroup (
		/* fetch from key-value pair system */
		'<span class="token string">variable</span>' {
			'<span class="token string">variable</span>': [ <span class="token operator">var</span> ] reference
		}
		/* static/hardcoded values */
		'<span class="token string">static integer</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">static text</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">text</span>' {
					'<span class="token string">value</span>': text
				}
				'<span class="token string">line break</span>' { [ <span class="token operator">line-break</span> ] }
				'<span class="token string">guid</span>' { [ <span class="token operator">guid</span> ] }
			)
		}
		'<span class="token string">static boolean</span>' {
			'<span class="token string">value</span>': stategroup (
				'<span class="token string">true</span>' { [ <span class="token operator">true</span> ] }
				'<span class="token string">false</span>' { [ <span class="token operator">false</span> ] }
			)
		}
		'<span class="token string">static calendar</span>' { [ <span class="token operator">now</span> ]
			'<span class="token string">timezone</span>': stategroup (
				'<span class="token string">explicit</span>' { [ <span class="token operator">in</span> ]
					'<span class="token string">promise</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
				}
				'<span class="token string">utc</span>' { }
			)
		}
		/* fetch from execution state */
		'<span class="token string">stored</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--stack-selector">'stack selector'</a>
		}
		'<span class="token string">context</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">network request</span>' { [ <span class="token operator">network</span> ] }
		'<span class="token string">captured error</span>' { [ <span class="token operator">error</span> ] }
		/* compute new values */
		'<span class="token string">list merge</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
				'<span class="token string">concatenate</span>' { [ <span class="token operator">concatenate</span> ]
					'<span class="token string">separator</span>': stategroup (
						'<span class="token string">yes</span>' {
							'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
						}
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">logical and</span>' { [ <span class="token operator">and</span> ] }
				'<span class="token string">logical or</span>' { [ <span class="token operator">or</span> ] }
			)
			'<span class="token string">promises</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promises">'promises'</a>
		}
		'<span class="token string">arithmetic</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">inversion</span>' { [ <span class="token operator">-</span> ]
					'<span class="token string">operand</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
				}
				'<span class="token string">division</span>' { [ <span class="token operator">division</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">numerator</span>': component <a href="#grammar-rule--promise">'promise'</a>
					'<span class="token string">denominator</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--promise">'promise'</a>
				}
			)
		}
		'<span class="token string">file constructor</span>' { [ <span class="token operator">file</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">token</span>': [ <span class="token operator">token</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--promise">'promise'</a>
			'<span class="token string">extension</span>': [ <span class="token operator">extension</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--promise">'promise'</a>
		}
		'<span class="token string">format</span>' { [ <span class="token operator">format</span> ]
			'<span class="token string">format</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--format-rule">'format rule'</a>
		}
	)
	'<span class="token string">chain</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">||</span> ] stategroup (
				'<span class="token string">value</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
				}
				'<span class="token string">throw</span>' {
					'<span class="token string">message</span>': [ <span class="token operator">throw</span> ] text
				}
			)
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promises }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promises</span>' {
	'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--promises">'promises'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--value-promise }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value promise</span>' {
	'<span class="token string">promise</span>': component <a href="#grammar-rule--promise">'promise'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--target-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">response</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dynamic-order
			'<span class="token string">status</span>': [ <span class="token operator">status</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			'<span class="token string">headers</span>': [ <span class="token operator">headers</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			'<span class="token string">content</span>': [ <span class="token operator">content</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">node</span>' {
			'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			}
		}
		'<span class="token string">entry</span>' { [ <span class="token operator">create</span> ]
			'<span class="token string">implicit key</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">value</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">interface</span>' { [ <span class="token operator">create</span> ]
					'<span class="token string">state</span>': reference
					'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
				}
				'<span class="token string">schema</span>' {
					'<span class="token string">option</span>': [ <span class="token operator">option</span> ] reference
				}
			)
		}
		'<span class="token string">scalar</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">statement</span>' {
	'<span class="token string">type</span>': stategroup (
		/* general statements */
		'<span class="token string">block</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
			'<span class="token string">scope</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">stack block</span>': component <a href="#grammar-rule--stack-block">'stack block'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">statement</span>': component <a href="#grammar-rule--statements">'statements'</a>
		}
		'<span class="token string">guard</span>' {
			'<span class="token string">guarded statement</span>': [ <span class="token operator">try</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			'<span class="token string">optional assignment</span>': [ <span class="token operator">catch</span> ] stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">fallback statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">condition</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">boolean</span>' {
					'<span class="token string">condition</span>': [ <span class="token operator">match</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">on true</span>': [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
						'<span class="token string">on false</span>': [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
				}
				'<span class="token string">existence</span>' {
					'<span class="token string">value</span>': [ <span class="token operator">any</span> ] component <a href="#grammar-rule--promise">'promise'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">on value</span>': [ <span class="token operator">|</span> <span class="token operator">value</span> <span class="token operator">as</span> <span class="token operator">$</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
						'<span class="token string">on error</span>': [ <span class="token operator">|</span> <span class="token operator">error</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
				}
				'<span class="token string">switch</span>' {
					'<span class="token string">value</span>': [ <span class="token operator">switch</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">dynamic</span>' {
							'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
								'<span class="token string">has next</span>': stategroup = node-switch successor (
									| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
									| none = '<span class="token string">no</span>'
								)
								'<span class="token string">optional assignment</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ] }
									'<span class="token string">no</span>' { }
								)
								'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
							}
						}
						'<span class="token string">network method</span>' {
							'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary (
								static '<span class="token string">get</span>' [ <span class="token operator">GET</span> ]
								static '<span class="token string">head</span>' [ <span class="token operator">HEAD</span> ]
								static '<span class="token string">post</span>' [ <span class="token operator">POST</span> ]
								static '<span class="token string">put</span>' [ <span class="token operator">PUT</span> ]
								static '<span class="token string">delete</span>' [ <span class="token operator">DELETE</span> ]
							) { [ <span class="token operator">|</span> ]
								'<span class="token string">has next</span>': stategroup = node-switch successor (
									| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
									| none = '<span class="token string">no</span>'
								)
								'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
							}
						}
					)
				}
			)
		}
		'<span class="token string">walk</span>' {
			'<span class="token string">value</span>': [ <span class="token operator">walk</span>, <span class="token operator">as</span> <span class="token operator">$</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
			'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">call</span>' {
			'<span class="token string">selection</span>': [ <span class="token operator">call</span> ] component <a href="#grammar-rule--lambda-selector">'lambda selector'</a>
			'<span class="token string">arguments</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--lambda-arguments">'lambda arguments'</a>
		}
		'<span class="token string">log operation</span>' { [ <span class="token operator">@log:</span> ]
			'<span class="token string">message</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
		'<span class="token string">no operation</span>' { [ <span class="token operator">no-op</span> ] }
		'<span class="token string">throw</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">captured error</span>' { [ <span class="token operator">rethrow</span> ] }
				'<span class="token string">new error</span>' { [ <span class="token operator">throw</span> ]
					'<span class="token string">message</span>': text
				}
			)
		}
		/* map to target */
		'<span class="token string">target</span>' {
			'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
		}
		/* change target */
		'<span class="token string">execute command</span>' {
			'<span class="token string">context</span>': [ <span class="token operator">execute</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
			'<span class="token string">command</span>': [ <span class="token operator">:</span> ] reference
			'<span class="token string">statement</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--statements }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">statements</span>' {
	'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
	'<span class="token string">has more statements</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">statement</span>': component <a href="#grammar-rule--statements">'statements'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
