---
layout: doc
origin: model
language: client_request
version: rev-actions-commands.1
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type</span>': stategroup (
	'<span class="token string">collection query</span>' {
		'<span class="token string">context node path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">collection path</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--collection-query-path">'collection query path'</a>
		'<span class="token string">filters</span>': [ <span class="token operator">where</span> ] group {
			'<span class="token string">todo filter</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">has-todo</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">property filters</span>': dictionary {
				'<span class="token string">path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">number</span>' {
						'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
						'<span class="token string">expression</span>': component <a href="#grammar-rule--number-filter-expression">'number filter expression'</a>
					}
					'<span class="token string">state group</span>' {
						'<span class="token string">state group</span>': [ <span class="token operator">?</span>, <span class="token operator">in</span> ] reference
						'<span class="token string">states to include</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
					}
					'<span class="token string">text</span>' {
						'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">simple</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
								'<span class="token string">expression</span>': component <a href="#grammar-rule--filter-expression">'filter expression'</a>
							}
							'<span class="token string">reference</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
									'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
								)
								'<span class="token string">references</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--reference-filter-list">'reference filter list'</a>
							}
						)
					}
				)
			}
		}
		'<span class="token string">select entries</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">select</span> ]
				'<span class="token string">properties</span>': dictionary {
					'<span class="token string">path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">id path</span>' { [ <span class="token operator">id-path</span> ] }
						'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
							'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression2">'number expression2'</a>
						}
						'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
							'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
						}
						'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
							'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">/</span> ] reference
						}
						'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
							'<span class="token string">state group</span>': [ <span class="token operator">=</span> <span class="token operator">?</span> ] reference
						}
					)
				}
				'<span class="token string">limit number of entries</span>': [ <span class="token operator">limit</span> ] integer
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">aggregates</span>': [ <span class="token operator">aggregate</span> ] dictionary {
			'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
				'<span class="token string">state distribution</span>' { [ <span class="token operator">distribution</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
				}
			)
		}
	}
	'<span class="token string">acyclic graph tree query</span>' {
		'<span class="token string">context node</span>': [ <span class="token operator">graph</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">type</span>': [ <span class="token operator">select</span> ] stategroup (
			'<span class="token string">collection</span>' { [ <span class="token operator">from</span> ]
				'<span class="token string">graph</span>': reference
			}
		)
	}
	'<span class="token string">acyclic graph list query</span>' {
		'<span class="token string">context node</span>': component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">entry points</span>': [ <span class="token operator">select</span> ] component <a href="#grammar-rule--entry-point-path">'entry point path'</a>
		'<span class="token string">graph</span>': [ <span class="token operator">collection</span> <span class="token operator">flatten</span> ] reference
		'<span class="token string">query</span>': group {
			'<span class="token string">collection path</span>': [ <span class="token operator">collection</span> ] component <a href="#grammar-rule--collection-path">'collection path'</a>
			'<span class="token string">properties</span>': dictionary {
				'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">number</span>' { [ <span class="token operator">#</span> ]
						'<span class="token string">number</span>': reference
					}
					'<span class="token string">text</span>' { [ <span class="token operator">.</span> ]
						'<span class="token string">text</span>': reference
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">?</span> ]
						'<span class="token string">state group</span>': reference
					}
				)
			}
		}
	}
	'<span class="token string">mutation</span>' {
		'<span class="token string">context node</span>': [ <span class="token operator">update</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">update node</span>': component <a href="#grammar-rule--update-node">'update node'</a>
	}
	'<span class="token string">subscription</span>' {
		'<span class="token string">mutation permissions</span>': stategroup (
			'<span class="token string">include</span>' { }
			'<span class="token string">ignore</span>' { [ <span class="token operator">#ignore-mutation-permissions</span> ] }
		)
		'<span class="token string">context node</span>': [ <span class="token operator">subscribe</span> <span class="token operator">to</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">subscribed properties</span>': component <a href="#grammar-rule--subscribed-properties">'subscribed properties'</a>
	}
	'<span class="token string">subscription deletion</span>' { }
	'<span class="token string">command execution</span>' {
		'<span class="token string">context node</span>': [ <span class="token operator">execute</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">command</span>': [ <span class="token operator">:</span> ] reference
		'<span class="token string">arguments</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--command-arguments">'command arguments'</a>
	}
	'<span class="token string">password mutation</span>' { [ <span class="token operator">change</span> <span class="token operator">password</span> ]
		'<span class="token string">old password</span>': [ <span class="token operator">from</span> ] text
		'<span class="token string">new password</span>': [ <span class="token operator">to</span> ] text
	}
	'<span class="token string">password reset</span>' { [ <span class="token operator">reset</span> <span class="token operator">password</span> ]
		'<span class="token string">username</span>': [ <span class="token operator">of</span> ] text
	}
)
</pre>
</div>
</div>

{: #grammar-rule--filter-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">filter expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">wildcard</span>' { [ <span class="token operator">*</span> ] }
		'<span class="token string">alternatives</span>' { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
			'<span class="token string">alternatives</span>': dictionary { }
		}
	)
	'<span class="token string">has more steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--filter-expression">'filter expression'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-filter-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number filter expression</span>' {
	'<span class="token string">operator</span>': stategroup (
		'<span class="token string">range</span>' {
			'<span class="token string">greater than</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">></span> ]
					'<span class="token string">criterium</span>': integer
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">less than</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator"><</span> ]
					'<span class="token string">criterium</span>': integer
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">equals</span>' { [ <span class="token operator">==</span> ]
			'<span class="token string">criterium</span>': integer
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--reference-filter-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference filter list</span>' {
	'<span class="token string">referenced node</span>': component <a href="#grammar-rule--id-path">'id path'</a>
	'<span class="token string">has alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">alternative</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--reference-filter-list">'reference filter list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--id-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">id path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection entry</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">collection</span>': reference
					'<span class="token string">id</span>': [ <span class="token operator">:</span> ] text
				}
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--id-path">'id path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-child-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional child path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-child-path">'conditional child path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-child-path">'conditional child path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--collection-query-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection query path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-child-path">'conditional child path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">candidates</span>' { [ <span class="token operator">candidates</span> ]
					'<span class="token string">include reference</span>': stategroup (
						'<span class="token string">yes</span>' { [ <span class="token operator">#include-reference</span> ] }
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">existing entries</span>' { }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-query-path">'collection query path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--entry-point-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entry point path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
		}
		'<span class="token string">yes</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-child-path">'conditional child path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--entry-point-path">'entry point path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--plural-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">merge</span>' { [ <span class="token operator">merge</span> ]
					'<span class="token string">expected node path</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--node-type-path">'node type path'</a>
					'<span class="token string">paths</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
						'<span class="token string">plural path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--plural-path">'plural path'</a>
					}
				}
				'<span class="token string">collection</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">collection</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--plural-path">'plural path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
				'<span class="token string">collection entry</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">entry key</span>': text
				}
				'<span class="token string">link</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">~></span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">state constraint</span>' { [ <span class="token operator">&</span> ]
					'<span class="token string">input parameter</span>': reference
				}
				'<span class="token string">state group output parameter</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
				}
				'<span class="token string">referencer output</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
					'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type path</span>' {
	'<span class="token string">steps</span>': component <a href="#grammar-rule--node-type-path-step">'node type path step'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--node-type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type path step</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">collection</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">collection</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-type-path-step">'node type path step'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--aggregate2 }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">aggregate2</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
	'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--number-aggregate2 }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number aggregate2</span>' {
	'<span class="token string">aggregate</span>': component <a href="#grammar-rule--aggregate2">'aggregate2'</a>
	'<span class="token string">property name</span>': [ <span class="token operator">#</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--signed-number-property2 }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signed number property2</span>' {
	'<span class="token string">sign</span>': stategroup (
		'<span class="token string">negative</span>' { [ <span class="token operator">-</span> ] }
		'<span class="token string">positive</span>' { }
	)
	'<span class="token string">path</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
	'<span class="token string">property name</span>': [ <span class="token operator">#</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--signed-number-property-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signed number property list</span>' {
	'<span class="token string">has element</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">signed number property</span>': component <a href="#grammar-rule--signed-number-property2">'signed number property2'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-expression2 }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression2</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">value</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">number property</span>' {
			'<span class="token string">signed number property</span>': component <a href="#grammar-rule--signed-number-property2">'signed number property2'</a>
		}
		'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ]
			'<span class="token string">number aggregate</span>': component <a href="#grammar-rule--number-aggregate2">'number aggregate2'</a>
		}
		'<span class="token string">sum list</span>' { [ <span class="token operator">sumlist</span> ]
			'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
		'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> ]
			'<span class="token string">number</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--signed-number-property2">'signed number property2'</a>
			'<span class="token string">modulus</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property2">'signed number property2'</a>
		}
		'<span class="token string">product</span>' { [ <span class="token operator">product</span> ]
			'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
		'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
			'<span class="token string">rounding</span>': stategroup (
				'<span class="token string">ordinary</span>' { }
				'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
				'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
			)
			'<span class="token string">numerator</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--signed-number-property2">'signed number property2'</a>
			'<span class="token string">denominator</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property2">'signed number property2'</a>
		}
		'<span class="token string">count</span>' { [ <span class="token operator">count</span> ]
			'<span class="token string">aggregate</span>': component <a href="#grammar-rule--aggregate2">'aggregate2'</a>
		}
		'<span class="token string">state based</span>' { [ <span class="token operator">switch</span> <span class="token operator">(</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span>, <span class="token operator">)</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression2">'number expression2'</a>
			}
		}
		'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ]
			'<span class="token string">left expression</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--number-expression2">'number expression2'</a>
			'<span class="token string">right expression</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--number-expression2">'number expression2'</a>
		}
		'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ]
			'<span class="token string">left expression</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--number-expression2">'number expression2'</a>
			'<span class="token string">right expression</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--number-expression2">'number expression2'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular text expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">static</span>' {
			'<span class="token string">string</span>': text
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-text-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular text expression list</span>' {
	'<span class="token string">has element</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">singular text expression</span>': component <a href="#grammar-rule--singular-text-expression">'singular text expression'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-text-expression-list">'singular text expression list'</a>
		}
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
		'<span class="token string">singular</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--singular-text-expression">'singular text expression'</a>
		}
		'<span class="token string">concatenation</span>' { [ <span class="token operator">concat</span> ]
			'<span class="token string">parts</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--singular-text-expression-list">'singular text expression list'</a>
		}
		'<span class="token string">join</span>' { [ <span class="token operator">join</span> ]
			'<span class="token string">node collection</span>': component <a href="#grammar-rule--plural-path">'plural path'</a>
			'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
			'<span class="token string">separator</span>': [ <span class="token operator">with</span> ] text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--subscribed-properties }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">subscribed properties</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">subscribe on</span>': stategroup (
					'<span class="token string">entries</span>' {
						'<span class="token string">subscribed properties</span>': component <a href="#grammar-rule--subscribed-properties">'subscribed properties'</a>
					}
					'<span class="token string">updates</span>' { }
				)
			}
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">subscribed properties</span>': component <a href="#grammar-rule--subscribed-properties">'subscribed properties'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">subscribed properties</span>': component <a href="#grammar-rule--subscribed-properties">'subscribed properties'</a>
				}
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">include reference</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">#include-reference</span> ] }
				)
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ] }
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--update-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">update node</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">update node</span>': component <a href="#grammar-rule--update-node">'update node'</a>
			}
			'<span class="token string">number</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> <span class="token operator">=</span> ]
						'<span class="token string">new value</span>': integer
					}
					'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> <span class="token operator">=</span> ]
						'<span class="token string">new value</span>': integer
					}
				)
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">state</span>': reference
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">set</span>' { [ <span class="token operator">=</span> ]
						'<span class="token string">node</span>': component <a href="#grammar-rule--initialize-node">'initialize node'</a>
						'<span class="token string">delete node</span>': component <a href="#grammar-rule--delete-node">'delete node'</a>
					}
					'<span class="token string">update</span>' {
						'<span class="token string">update node</span>': component <a href="#grammar-rule--update-node">'update node'</a>
					}
				)
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> <span class="token operator">=</span> ]
				'<span class="token string">new value</span>': text
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> <span class="token operator">=</span> ]
				'<span class="token string">new token</span>': text
				'<span class="token string">new extension</span>': [ <span class="token operator">.</span> ] text
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">entries</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">create</span>' { [ <span class="token operator">create</span> ]
							'<span class="token string">node</span>': component <a href="#grammar-rule--initialize-node">'initialize node'</a>
						}
						'<span class="token string">update</span>' {
							'<span class="token string">update node</span>': component <a href="#grammar-rule--update-node">'update node'</a>
						}
						'<span class="token string">remove</span>' { [ <span class="token operator">remove</span> ]
							'<span class="token string">delete node</span>': component <a href="#grammar-rule--delete-node">'delete node'</a>
						}
					)
				}
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--initialize-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">initialize node</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">groups</span>': dictionary {
		'<span class="token string">node</span>': [ <span class="token operator">:</span> <span class="token operator">group</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--initialize-node">'initialize node'</a>
	}
	'<span class="token string">texts</span>': dictionary {
		'<span class="token string">value</span>': [ <span class="token operator">:</span> <span class="token operator">text</span> <span class="token operator">=</span> ] text
	}
	'<span class="token string">files</span>': dictionary {
		'<span class="token string">token</span>': [ <span class="token operator">:</span> <span class="token operator">file</span> <span class="token operator">=</span> ] text
		'<span class="token string">extension</span>': [ <span class="token operator">.</span> ] text
	}
	'<span class="token string">numbers</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> <span class="token operator">=</span> ]
				'<span class="token string">value</span>': integer
			}
			'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> <span class="token operator">=</span> ]
				'<span class="token string">value</span>': integer
			}
		)
	}
	'<span class="token string">state groups</span>': dictionary {
		'<span class="token string">state</span>': [ <span class="token operator">:</span> <span class="token operator">stategroup</span> <span class="token operator">=</span> ] reference
		'<span class="token string">node</span>': component <a href="#grammar-rule--initialize-node">'initialize node'</a>
	}
	'<span class="token string">collections</span>': dictionary {
		'<span class="token string">entries</span>': [ <span class="token operator">:</span> <span class="token operator">collection</span> ] dictionary {
			'<span class="token string">node</span>': component <a href="#grammar-rule--initialize-node">'initialize node'</a>
		}
	}
}
</pre>
</div>
</div>

{: #grammar-rule--delete-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">delete node</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--command-arguments }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command arguments</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> <span class="token operator">=</span> ]
				'<span class="token string">entries</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">arguments</span>': component <a href="#grammar-rule--command-arguments">'command arguments'</a>
				}
			}
			'<span class="token string">number</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> <span class="token operator">=</span> ]
						'<span class="token string">value</span>': integer
					}
					'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> <span class="token operator">=</span> ]
						'<span class="token string">value</span>': integer
					}
				)
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> <span class="token operator">=</span> ]
				'<span class="token string">text</span>': text
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> <span class="token operator">=</span> ]
				'<span class="token string">token</span>': text
				'<span class="token string">extension</span>': [ <span class="token operator">.</span> ] text
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">state</span>': reference
				'<span class="token string">arguments</span>': component <a href="#grammar-rule--command-arguments">'command arguments'</a>
			}
		)
	}
}
</pre>
</div>
</div>
