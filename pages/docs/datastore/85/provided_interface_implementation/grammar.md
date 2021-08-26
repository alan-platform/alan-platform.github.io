---
layout: doc
origin: datastore
language: provided_interface_implementation
version: 85
type: grammar
---

1. TOC
{:toc}

## The *minimal implementation*
---
Every provided interface implementation contains at least
> ```js
root = root /* context path goes here */ ( /* node type mapping */ )
```

{: #grammar-rule--variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment</span>': [ <span class="token operator">root</span> <span class="token operator">=</span> <span class="token operator">root</span> ] component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
</pre>
</div>
</div>

{: #grammar-rule--application-root-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application root node</span>': component <a href="#grammar-rule--interface-context-id-path">'interface context id path'</a>
</pre>
</div>
</div>

{: #grammar-rule--root }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
</pre>
</div>
</div>
## Context identification path
---
This path can be used for expressing the context node for an interface (the interface `root`).

{: #grammar-rule--interface-context-id-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface context id path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection entry</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">[</span> ] reference
					'<span class="token string">id</span>': [ <span class="token operator">@</span>, <span class="token operator">]</span> ] reference
				}
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--interface-context-id-path">'interface context id path'</a>
		}
	)
}
</pre>
</div>
</div>
## Node type mapping
---

{: #grammar-rule--node-type-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-mapping">'command mapping'</a>
			}
			'<span class="token string">property</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">empty</span>' { [ <span class="token operator">=</span> <span class="token operator">empty</span> ] }
							'<span class="token string">dynamic</span>' {
								'<span class="token string">key constraint</span>': stategroup (
									'<span class="token string">no</span>' { [ <span class="token operator">=</span> ]
										'<span class="token string">key constructor</span>': component <a href="#grammar-rule--key-constructor">'key constructor'</a>
									}
									'<span class="token string">yes</span>' { [ <span class="token operator">-></span>, <span class="token operator">=</span> ]
										'<span class="token string">referencer</span>': group {
											'<span class="token string">head</span>': component <a href="#grammar-rule--singular-imp-node-path">'singular imp node path'</a>
											'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
											'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">-|</span> ]
												'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-descendant-imp-node-path">'conditional descendant imp node path'</a>
											}
										}
									}
								)
								'<span class="token string">has branch</span>': stategroup = node-switch .'<span class="token string">branches</span>' (
									| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
									| none  = '<span class="token string">no</span>'
								)
								'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
									'<span class="token string">has successor</span>': stategroup = node-switch successor (
										| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
										| none = '<span class="token string">no</span>'
									)
									'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-expression">'collection expression'</a>
									'<span class="token string">key constraint</span>': stategroup (
										'<span class="token string">no</span>' { }
										'<span class="token string">yes</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
											'<span class="token string">branch</span>': [ <span class="token operator">from</span> ] reference
											'<span class="token string">key path</span>': [ <span class="token operator">>[</span>,'<span class="token string"> ]</span>'] component <a href="#grammar-rule--collection-key-node-path">'collection key node path'</a>
										}
									)
									'<span class="token string">node</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
								}
							}
						)
					}
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--group-expression">'group expression'</a>
						'<span class="token string">node</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--state-expression">'state expression'</a>
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">has constraint</span>': stategroup (
							'<span class="token string">no</span>' {
								'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
							}
							'<span class="token string">yes</span>' {
								'<span class="token string">referencer</span>': [ <span class="token operator">-></span> ] group {
									'<span class="token string">head</span>': component <a href="#grammar-rule--singular-imp-node-path">'singular imp node path'</a>
									'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
									'<span class="token string">branch</span>': [ <span class="token operator">-|</span> ] reference
									'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-descendant-imp-node-path">'conditional descendant imp node path'</a>
								}
								'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--reference-expression">'reference expression'</a>
							}
						)
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--file-expression">'file expression'</a>
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>
## Command mapping expressions
---

{: #grammar-rule--command-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command mapping</span>' { [ <span class="token operator">do</span> ]
	'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">command</span>': [ <span class="token operator">(</span> ] reference
	'<span class="token string">parameter mapping</span>': [ <span class="token operator">with</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> <span class="token operator">=</span> ]
				'<span class="token string">group</span>': [ <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">collection</span>': [ <span class="token operator">=</span> <span class="token operator">map</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">number</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">#</span> ] reference
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">parameter</span>' {
						'<span class="token string">text</span>': [ <span class="token operator">@</span> <span class="token operator">.</span> ] reference
					}
					'<span class="token string">variable</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
					}
				)
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">/</span> ] reference
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">fixed</span>' {
						'<span class="token string">state</span>': reference
						'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
					}
					'<span class="token string">map</span>' { [ <span class="token operator">switch</span> <span class="token operator">@</span> ]
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
						'<span class="token string">mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">mapped state</span>': [ <span class="token operator">=</span> ] reference
							'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
						}
					}
					'<span class="token string">match branch</span>' { [ <span class="token operator">match-branch</span> ]
						'<span class="token string">path</span>': group {
							'<span class="token string">head</span>': component <a href="#grammar-rule--parametrized-singular-imp-node-path">'parametrized singular imp node path'</a>
							'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
							'<span class="token string">reference</span>': [ <span class="token operator">[</span> <span class="token operator">@</span> <span class="token operator">></span>, <span class="token operator">]</span> ] reference
						}
						'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">state mapping context variable</span>': stategroup (
								'<span class="token string">current variable</span>' { }
								'<span class="token string">branch context variable</span>' { [ <span class="token operator">bind</span> <span class="token operator">$</span> ] }
							)
							'<span class="token string">state</span>': [ <span class="token operator">=</span> ] reference
							'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
						}
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>
## Property mapping expressions
---
### Texts, numbers, files, and references

{: #grammar-rule--text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--file-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">file expression</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">file</span>': [ <span class="token operator">/</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--reference-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference expression</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
	'<span class="token string">key path</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--collection-key-node-path">'collection key node path'</a>
}
</pre>
</div>
</div>
### Collections

{: #grammar-rule--key-separator }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">key separator</span>' {
	'<span class="token string">separator</span>': [ <span class="token operator">join</span> ] stategroup (
		'<span class="token string">dot</span>' { [ <span class="token operator">.</span> ] }
		'<span class="token string">dash</span>' { [ <span class="token operator">-</span> ] }
		'<span class="token string">colon</span>' { [ <span class="token operator">:</span> ] }
		'<span class="token string">greater than</span>' { [ <span class="token operator">></span> ] }
		'<span class="token string">space</span>' { [ <span class="token operator">space</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--key-constructor }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">key constructor</span>' {
	'<span class="token string">branch concatenation</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">prepend</span>' { [ <span class="token operator">prepend-branch</span> ] }
				'<span class="token string">append</span>' { [ <span class="token operator">append-branch</span> ] }
			)
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">key separator</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">key separator</span>': component <a href="#grammar-rule--key-separator">'key separator'</a>
		}
		'<span class="token string">no</span>' { }
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
	'<span class="token string">head</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-expression-tail">'collection expression tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--collection-expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection expression tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">filter</span>': component <a href="#grammar-rule--filter-expression">'filter expression'</a>
		}
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">singular</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--singular-node-step">'singular node step'</a>
				}
				'<span class="token string">conditional</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--conditional-descendant-node-step">'conditional descendant node step'</a>
				}
				'<span class="token string">plural</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--plural-descendant-node-step">'plural descendant node step'</a>
				}
			)
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-expression-tail">'collection expression tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--filter-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">filter expression</span>' {
	'<span class="token string">has filter</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">where</span> ]
			'<span class="token string">has filters</span>': stategroup = node-switch .'<span class="token string">filters</span>' (
				| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
				| none  = '<span class="token string">no</span>'
			)
			'<span class="token string">filters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">$</span> ]
				'<span class="token string">has successor</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">singular result</span>' {
						'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
					}
					'<span class="token string">equality</span>' { [ <span class="token operator">=</span> <span class="token operator">equal</span> ]
						'<span class="token string">left path</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">right path</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
					}
				)
			}
		}
	)
}
</pre>
</div>
</div>
### Groups and stategroups

{: #grammar-rule--group-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">group expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">none</span>' { }
		'<span class="token string">bound</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--state-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">static</span>' {
			'<span class="token string">state</span>': reference
			'<span class="token string">node</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
		}
		'<span class="token string">dynamic</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				'<span class="token string">state</span>': [ <span class="token operator">=</span> ] reference
				'<span class="token string">node</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
			}
		}
	)
}
</pre>
</div>
</div>
## Navigation expressions
---

{: #grammar-rule--optional-variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional variable assignment</span>' {
	'<span class="token string">has assignment</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ] }
</pre>
</div>
</div>

{: #grammar-rule--ancestor-variable-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor variable path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">yes</span>' { [ <span class="token operator">$^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--context-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context node path</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
		'<span class="token string">variable</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">variable</span>' { }
				'<span class="token string">filter</span>' {
					'<span class="token string">filter</span>': reference
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular node path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-node-path-tail">'singular node path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--singular-node-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular node path tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--singular-node-step">'singular node step'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-node-path-tail">'singular node path tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-node-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular node step</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
			'<span class="token string">group</span>': reference
		}
		'<span class="token string">reference</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
		}
		'<span class="token string">reference rule</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">state rule</span>' {
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional node path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-node-path-tail">'conditional node path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-node-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional node path tail</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--singular-node-path-tail">'singular node path tail'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--conditional-descendant-node-step">'conditional descendant node step'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-node-path-tail">'conditional node path tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-descendant-node-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional descendant node step</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
		}
		'<span class="token string">collection entry</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
				'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
				'<span class="token string">key source</span>': stategroup (
					'<span class="token string">link</span>' {
						'<span class="token string">text</span>': [ <span class="token operator">|></span> ] reference
					}
					'<span class="token string">node</span>' { }
				)
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--plural-descendant-node-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural descendant node step</span>' {
	'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">*</span> ] reference
	'<span class="token string">legacy annotation</span>': stategroup (
		'<span class="token string">base</span>' { }
		'<span class="token string">derived</span>' { [ <span class="token operator">(derived)</span> ] }
	)
}
</pre>
</div>
</div>
## Expressions for mapping safety
---

{: #grammar-rule--collection-key-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection key node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">reference</span>' { [ <span class="token operator">></span> ]
					'<span class="token string">text</span>': reference
				}
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">filter</span>' { [ <span class="token operator">$</span> ]
					'<span class="token string">filter</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-key-node-path">'collection key node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-descendant-branch-imp-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional descendant branch imp node path</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">static</span>' { }
		'<span class="token string">dynamic</span>' {
			'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-descendant-imp-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional descendant imp node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-descendant-branch-imp-node-path">'conditional descendant branch imp node path'</a>
				}
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-descendant-imp-node-path">'conditional descendant imp node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-imp-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular imp node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">reference</span>' { [ <span class="token operator">></span> ]
					'<span class="token string">reference</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-imp-node-path">'singular imp node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ancestor-parameter-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor parameter path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">@</span> ] }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state parent</span>' { [ <span class="token operator">@?^</span> ] }
				'<span class="token string">collection parent</span>' { [ <span class="token operator">@.^</span> ] }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-parameter-path">'ancestor parameter path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-singular-imp-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized singular imp node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection entry</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">single branch</span>': stategroup (
						'<span class="token string">yes</span>' { }
					)
					'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameter-path">'ancestor parameter path'</a>
						'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
					}
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--parametrized-singular-imp-node-path">'parametrized singular imp node path'</a>
		}
	)
}
</pre>
</div>
</div>
