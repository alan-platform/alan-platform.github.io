---
layout: "doc"
origin: "datastore"
language: "provided_interface_implementation"
version: "106"
type: "grammar"
---

1. TOC
{:toc}

## The *minimal implementation*
---
Every provided interface implementation contains at least
> ```js
root = root /* context path goes here */ ( /* node type mapping */ )
```

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment</span>': [ <span class="token operator">root</span> <span class="token operator">=</span> <span class="token operator">root</span> ] component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application root node</span>': component <a href="#grammar-rule--interface-context-id-path">'interface context id path'</a>
</pre>
</div>
</div>

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
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">id</span>': [ <span class="token operator">[</span> <span class="token operator">@</span>, <span class="token operator">]</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
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
										'<span class="token string">branch definer</span>': stategroup (
											'<span class="token string">state group</span>' {
												'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
												'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
											}
											'<span class="token string">implementation</span>' { }
										)
									}
									'<span class="token string">yes</span>' { [ <span class="token operator">-></span>, <span class="token operator">=</span> ]
										'<span class="token string">referencer</span>': group {
											'<span class="token string">head</span>': component <a href="#grammar-rule--singular-imp-node-path">'singular imp node path'</a>
											'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
										}
									}
								)
								'<span class="token string">first branch</span>': reference = first
								'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
									'<span class="token string">has successor</span>': stategroup = node-switch successor (
										| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
										| none = '<span class="token string">no</span>'
									)
									/* '<span class="token string">tail</span>' is a referencer extension for collections with key constraint */
									'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-descendant-imp-node-path">'conditional descendant imp node path'</a>
									'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-expression">'collection expression'</a>
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
								'<span class="token string">head</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--singular-imp-node-path">'singular imp node path'</a>
								'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
								'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-descendant-imp-node-path">'conditional descendant imp node path'</a>
								'<span class="token string">branch</span>': [ <span class="token operator">=</span> <span class="token operator">from</span> ] reference
								'<span class="token string">expression</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
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
'<span class="token string">command mapping</span>' { [ <span class="token operator">=></span> ]
	'<span class="token string">path</span>': [ <span class="token operator">execute</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">command</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">parameter mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
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
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">collection</span>': [ <span class="token operator">=</span> <span class="token operator">map</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">number</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
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
				'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">@</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">state</span>' {
						'<span class="token string">state</span>': reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
					}
					'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> <span class="token operator">@</span> ]
						'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
							'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
						}
					}
					'<span class="token string">branch switch</span>' { [ <span class="token operator">switch</span> ]
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
							'<span class="token string">state</span>': [ <span class="token operator">=></span> ] reference
							'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
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
### Texts, numbers and files

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
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">unary</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">absolute value</span>' { [ <span class="token operator">abs</span> ] }
				'<span class="token string">sign inversion</span>' { [ <span class="token operator">-</span> ] }
			)
			'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">dynamic</span>' { // use value exp instead
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">number</span>': [ <span class="token operator">.</span> ] reference
		}
	)
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
	'<span class="token string">file</span>': [ <span class="token operator">.</span> ] reference
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
					'<span class="token string">step</span>': component <a href="#grammar-rule--node-step">'node step'</a>
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
	'<span class="token string">has rules</span>': stategroup = node-switch .'<span class="token string">rules</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">rules</span>': dictionary { [ <span class="token operator">where</span> ]
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">node path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">existence</span>' { }
			'<span class="token string">equality</span>' {
				'<span class="token string">expected node path</span>': [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
			}
		)
	}
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
		'<span class="token string">state</span>' {
			'<span class="token string">state</span>': reference
			'<span class="token string">node</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
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
		'<span class="token string">no</span>' { }
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
				'<span class="token string">variable</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">rule</span>' {
					'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] reference
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node path tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--node-step">'node step'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--dependency-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dependency step</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">reference</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
		}
		'<span class="token string">reference rule</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">state rule</span>' {
			'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node step</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">group</span>' { [ <span class="token operator">.</span> ]
			'<span class="token string">group</span>': reference
		}
		'<span class="token string">dependency</span>' {
			'<span class="token string">dependency</span>': component <a href="#grammar-rule--dependency-step">'dependency step'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">collection entry</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
				'<span class="token string">key source</span>': stategroup (
					'<span class="token string">key reference</span>' {
						/* The node that the entry key value should point to. */
						/* NOTE: currently, only the key value (text) is matched. */
						'<span class="token string">node path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
					}
					// '<span class="token string">context key</span>' {
					// 	'<span class="token string">context key</span>': [ <span class="token operator">@</span> ] reference
					// }
				)
			}
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
	'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
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
	'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
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
}
</pre>
</div>
</div>
## Expressions for mapping safety
---

{: #grammar-rule--conditional-descendant-branch-imp-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional descendant branch imp node path</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">static</span>' { [ <span class="token operator">?</span> ] }
		'<span class="token string">dynamic</span>' {
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
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
				'<span class="token string">state</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-descendant-branch-imp-node-path">'conditional descendant branch imp node path'</a>
				}
				'<span class="token string">group</span>' { [ <span class="token operator">.</span> ]
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
				'<span class="token string">group</span>' { [ <span class="token operator">.</span> ]
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
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
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
					'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
						'<span class="token string">path</span>': [ <span class="token operator">@</span> ] component <a href="#grammar-rule--ancestor-parameter-path">'ancestor parameter path'</a>
						'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
					}
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--parametrized-singular-imp-node-path">'parametrized singular imp node path'</a>
		}
	)
}
</pre>
</div>
</div>
