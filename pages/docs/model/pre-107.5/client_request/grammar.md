---
layout: "doc"
origin: "model"
language: "client_request"
version: "pre-107.5"
type: "grammar"
---

1. TOC
{:toc}

## Request types

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
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
					'<span class="token string">users filter</span>': stategroup (
						'<span class="token string">requesting user</span>' { [ <span class="token operator">for</span> <span class="token operator">user</span> ] }
						/* In case of no users filter, the expression and filter of a user requirement corresponding to
						** a has-todo expression is only evaluated up to the first dependency on a user.
						** Alternatives that are part of a user requirement are still evaluated. */
						'<span class="token string">none</span>' { }
					)
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">value filters</span>': dictionary {
				'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">property</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
						'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">number</span>' {
								'<span class="token string">expression</span>': component <a href="#grammar-rule--number-filter-expression">'number filter expression'</a>
							}
							'<span class="token string">state group</span>' { [ <span class="token operator">in</span> ]
								'<span class="token string">states to include</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">?</span> ] }
							}
							'<span class="token string">text</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
									'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
								)
								'<span class="token string">expression</span>': component <a href="#grammar-rule--filter-expression">'filter expression'</a>
							}
							'<span class="token string">collection</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
									'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
								)
								'<span class="token string">keys</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">[</span>, <span class="token operator">]</span> ] }
							}
						)
					}
					'<span class="token string">node</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">existence</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">exists</span>' { [ <span class="token operator">exists</span> ] }
									'<span class="token string">not exists</span>' { [ <span class="token operator">not</span> <span class="token operator">exists</span> ] }
								)
							}
							'<span class="token string">containment</span>' {
								'<span class="token string">operator</span>': stategroup (
									'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
									'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
								)
								'<span class="token string">references</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--reference-filter-list">'reference filter list'</a>
							}
						)
					}
					'<span class="token string">texts</span>' {
						'<span class="token string">expression</span>': component <a href="#grammar-rule--filter-expression">'filter expression'</a>
						'<span class="token string">operator</span>': stategroup (
							'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
							'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
						)
						'<span class="token string">text paths</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] set {
							'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
							'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
						}
					}
				)
			}
		}
		'<span class="token string">select entries</span>': stategroup (
			'<span class="token string">yes</span>' {
				'<span class="token string">properties</span>': [ <span class="token operator">select</span> ] component <a href="#grammar-rule--node-query">'node query'</a>
				'<span class="token string">limit number of entries</span>': [ <span class="token operator">limit</span> ] integer
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">aggregates</span>': [ <span class="token operator">aggregate</span> ] dictionary {
			'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
				'<span class="token string">state distribution</span>' { [ <span class="token operator">distribution</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
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
		'<span class="token string">context node</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">entry points</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--entry-point-path">'entry point path'</a>
		'<span class="token string">graph</span>': [ <span class="token operator">flatten</span> ] reference
		'<span class="token string">query</span>': [ <span class="token operator">select</span> ] group {
			'<span class="token string">collection path</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
			'<span class="token string">properties</span>': dictionary {
				'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--node-path">'node path'</a>
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
		'<span class="token string">node update</span>': component <a href="#grammar-rule--node-update">'node update'</a>
	}
	'<span class="token string">subscription</span>' {
		'<span class="token string">mutation permissions</span>': stategroup (
			'<span class="token string">include</span>' { }
			'<span class="token string">ignore</span>' { [ <span class="token operator">#ignore-mutation-permissions</span> ] }
		)
		'<span class="token string">context node</span>': [ <span class="token operator">subscribe</span> <span class="token operator">to</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">node subscription</span>': component <a href="#grammar-rule--node-subscription">'node subscription'</a>
	}
	'<span class="token string">subscription deletion</span>' { }
	'<span class="token string">command execution</span>' {
		'<span class="token string">context node</span>': [ <span class="token operator">execute</span> ] component <a href="#grammar-rule--id-path">'id path'</a>
		'<span class="token string">command</span>': [ <span class="token operator">:</span> ] reference
		'<span class="token string">arguments</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--node-initialization">'node initialization'</a>
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
### Collection query
Queries an hierarchy of collections and produces a `select` and/or `aggregate` result the entries that match the filters.

If a filter cannot be evaluated because the user lacks required permissions, it evaluates to false.
This means that the node will be excluded from the result.
### Acyclic graph tree query
Produces a dependency tree showing the dependencies of a node in a predefined 'graph'.
The 'context node' is the root of the tree.
### Acyclic graph list query
Queries a collection of references and create a flat subgraph of the provided 'graph' for each of them.
The 'query' group defines what data will be queried for each of the entries.

For example, suppose we have this model, specifying `Products` and `Orders`:
```js
'Products': collection ['Name']
	'assembly': acyclic-graph
{
	'Name': text
	'Parts': collection ['Product'] {
		'Product': text -> ^ sibling in ('assembly')
		'Price': number positive 'euro'
	}
}
'Orders': collection ['ID'] {
	'ID': text
	'Products': collection ['Product'] {
		'Product': text -> ^ ^ .'Products'
	}
}
```

And the following query:
```js
on /* root */
from .'Orders'.'Products'>'Product'
flatten 'assembly'
select .'Parts'
	'PP': = #'Price'
```

Then we get a result of the form:
```js
'Orders': (
	['A'] (
		'Products': (
			subgraph ['1'] = ( // flat subgraph:
				['1'] (
					count = 0
					'Parts' = (
						['1.1'] ( 'PP' = 10 )
						['1.2'] ( 'PP' = 20 )
					)
				) // root of the graph
				['1.1'] ( count = 2 'Parts' = ( ) )
				['1.2'] ( count = 1 'Parts' = ( ) )
			)
		)
	)
	['B'] (
		'Products': (
			['2'] ( ['2'] ( count = 0 'Parts' = ( ) ) )
		)
	)
)
```

### Mutation
Updates specified parts of your data.
### Subscription
Subscribes to specific pieces of data.
The subscriber will get notifications in case subscribed data are modified.
### Subscription deletion
Request unsubscribe, and thus halt notifications for a subscription.
### Command execution
Request to execute a command as defined in an application model.
### Password mutation
Updates a user's password.
### Password reset
Resets a user's password.
## Rules

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
	'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">node</span>' { }
		'<span class="token string">collection</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
	)
	'<span class="token string">has alternative</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">alternative</span>': component <a href="#grammar-rule--reference-filter-list">'reference filter list'</a>
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
					'<span class="token string">id</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] text
				}
				'<span class="token string">group</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
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
NOTE: the datastore produces an entry key for a collection entry, iff the user has read permissions for the entry node.

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
				'<span class="token string">candidates</span>' {
					'<span class="token string">source</span>': [ <span class="token operator">candidates</span> ] stategroup (
						'<span class="token string">key reference</span>' { }
						'<span class="token string">where rule</span>' {
							'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
						}
					)
					'<span class="token string">rules</span>': dictionary { [ <span class="token operator">where</span> ] }
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

{: #grammar-rule--node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">state rule</span>' { [ <span class="token operator">.&</span> ]
					'<span class="token string">rule</span>': reference
				}
				'<span class="token string">reference rule</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">collection entry</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">entry key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] text
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path">'node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--aggregate }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">aggregate</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--node-path">'node path'</a>
	'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path">'node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--number-aggregate }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number aggregate</span>' {
	'<span class="token string">aggregate</span>': component <a href="#grammar-rule--aggregate">'aggregate'</a>
	'<span class="token string">property name</span>': [ <span class="token operator">.</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--signed-number-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signed number property</span>' {
	'<span class="token string">sign</span>': stategroup (
		'<span class="token string">negative</span>' { [ <span class="token operator">-</span> ] }
		'<span class="token string">positive</span>' { }
	)
	'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
	'<span class="token string">property name</span>': [ <span class="token operator">.</span> ] reference
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
			'<span class="token string">signed number property</span>': component <a href="#grammar-rule--signed-number-property">'signed number property'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
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
		'<span class="token string">value</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">number property</span>' {
			'<span class="token string">signed number property</span>': component <a href="#grammar-rule--signed-number-property">'signed number property'</a>
		}
		'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ]
			'<span class="token string">number aggregate</span>': component <a href="#grammar-rule--number-aggregate">'number aggregate'</a>
		}
		'<span class="token string">sum list</span>' { [ <span class="token operator">sum</span> ]
			'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
		'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> ]
			'<span class="token string">number</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--signed-number-property">'signed number property'</a>
			'<span class="token string">modulus</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property">'signed number property'</a>
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
			'<span class="token string">numerator</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--signed-number-property">'signed number property'</a>
			'<span class="token string">denominator</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--signed-number-property">'signed number property'</a>
		}
		'<span class="token string">count</span>' { [ <span class="token operator">count</span> ]
			'<span class="token string">aggregate</span>': component <a href="#grammar-rule--aggregate">'aggregate'</a>
		}
		'<span class="token string">state based</span>' { [ <span class="token operator">switch</span> <span class="token operator">(</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span>, <span class="token operator">)</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
			}
		}
		'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">right expression</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
			'<span class="token string">right expression</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
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
			'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
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
	)
}
</pre>
</div>
</div>
NOTE: the datastore produces an entry key for a collection entry, iff the user has read permissions for the entry node.

{: #grammar-rule--node-subscription }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node subscription</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">property</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">include graph endpoints</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">#include-graph-endpoints</span> ] }
						)
						'<span class="token string">include size</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">#include-size</span> ] }
						)
						'<span class="token string">include entries</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">#include-entries</span> ] }
						)
						'<span class="token string">subscribe to</span>': stategroup (
							'<span class="token string">subset</span>' {
								'<span class="token string">keys</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">[</span> ]
									'<span class="token string">subscription</span>': [ <span class="token operator">]</span> ] component <a href="#grammar-rule--node-subscription">'node subscription'</a>
								}
							}
							'<span class="token string">all</span>' {
								'<span class="token string">subscription</span>': component <a href="#grammar-rule--node-subscription">'node subscription'</a>
							}
						)
					}
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">subscription</span>': component <a href="#grammar-rule--node-subscription">'node subscription'</a>
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">subscription</span>': component <a href="#grammar-rule--node-subscription">'node subscription'</a>
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
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ] }
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--node-update }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node update</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">update</span>': component <a href="#grammar-rule--node-update">'node update'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">new value</span>': [ <span class="token operator">=</span> ] integer
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">state</span>': reference
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">set</span>' { [ <span class="token operator">=</span> ]
						'<span class="token string">initialization</span>': component <a href="#grammar-rule--node-initialization">'node initialization'</a>
					}
					'<span class="token string">update</span>' {
						'<span class="token string">update</span>': component <a href="#grammar-rule--node-update">'node update'</a>
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
							'<span class="token string">initialization</span>': component <a href="#grammar-rule--node-initialization">'node initialization'</a>
						}
						'<span class="token string">update</span>' {
							'<span class="token string">update</span>': component <a href="#grammar-rule--node-update">'node update'</a>
						}
						'<span class="token string">remove</span>' { [ <span class="token operator">remove</span> ] }
					)
				}
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--node-initialization }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node initialization</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">initialization</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--node-initialization">'node initialization'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] integer
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">state</span>': [ <span class="token operator">=</span> ] reference
				'<span class="token string">initialization</span>': component <a href="#grammar-rule--node-initialization">'node initialization'</a>
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> <span class="token operator">=</span> ]
				'<span class="token string">value</span>': text
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> <span class="token operator">=</span> ]
				'<span class="token string">token</span>': text
				'<span class="token string">extension</span>': [ <span class="token operator">.</span> ] text
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">entries</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">initialization</span>': component <a href="#grammar-rule--node-initialization">'node initialization'</a>
				}
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--node-query }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node query</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--node-path">'node path'</a>
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">id path</span>' { [ <span class="token operator">id-path</span> ] }
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression">'number expression'</a>
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression">'text expression'</a>
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">file</span>': [ <span class="token operator">=</span> <span class="token operator">/</span> ] reference
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">state group</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">collection</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
				'<span class="token string">include graph endpoints</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">#include-graph-endpoints</span> ] }
				)
				'<span class="token string">properties</span>': component <a href="#grammar-rule--node-query">'node query'</a>
			}
		)
	}
}
</pre>
</div>
</div>
