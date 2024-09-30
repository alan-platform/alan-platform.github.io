---
layout: "doc"
origin: "auto-webclient"
language: "generator_annotations"
version: "yar.10"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has global features</span>': stategroup (
	'<span class="token string">yes</span>' {
		'<span class="token string">configured features</span>': dictionary { [ <span class="token operator">feature</span> ]
			'<span class="token string">has more features</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next feature</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">feature</span>': component <a href="#grammar-rule--feature">'feature'</a>
		}
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld menu</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">handheld-menu</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
		'<span class="token string">items</span>': dictionary {
			'<span class="token string">icon</span>': [ <span class="token operator">icon:</span> ] text
			'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
			'<span class="token string">has more items</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next item</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
		}
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
</pre>
</div>
</div>
### Navigation expressions

{: #grammar-rule--singular-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
		}
		'<span class="token string">no</span>' { }
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
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
		}
		'<span class="token string">no</span>' { }
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
	'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
	'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
	'<span class="token string">has more steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--query-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">query path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
					'<span class="token string">result</span>': stategroup (
						'<span class="token string">referenced node</span>' { }
						'<span class="token string">rule</span>' {
							'<span class="token string">rule</span>': [ <span class="token operator">$</span> ] reference
						}
					)
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--query-path">'query path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--extended-annotations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">extended annotations</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">has features</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">configured features</span>': dictionary { [ <span class="token operator">feature</span> ]
				'<span class="token string">has more features</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next feature</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">feature</span>': component <a href="#grammar-rule--feature">'feature'</a>
			}
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">has handheld frames</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">handheld frames</span>': dictionary { [ <span class="token operator">handheld:</span> ]
				'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-view-frame">'handheld view frame'</a>
			}
			'<span class="token string">main frame</span>': reference = first
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
			}
			'<span class="token string">reference set</span>' { [ <span class="token operator">reference-set</span> ]
				'<span class="token string">has custom queries</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">custom queries</span>': dictionary { [ <span class="token operator">query</span> ]
							'<span class="token string">has more queries</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">next query</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
						}
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">entries are custom properties</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@properties</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">value</span>' {
								'<span class="token string">value attribute</span>': [ <span class="token operator">value:</span> ] reference
							}
							'<span class="token string">node</span>' { [ <span class="token operator">node</span> ] }
						)
					}
					'<span class="token string">list</span>' { [ <span class="token operator">@list</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">has custom queries</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">custom queries</span>': dictionary { [ <span class="token operator">query</span> ]
							'<span class="token string">has more queries</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">next query</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
						}
					}
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">sub tree</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">annotations</span>': component <a href="#grammar-rule--extended-annotations">'extended annotations'</a>
				}
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--feature }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature</span>' {
	'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--feature-properties }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature properties</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
			'<span class="token string">binding</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">state</span>' { [ <span class="token operator">state</span> ]
						'<span class="token string">state</span>': reference
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">number</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">file</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">command</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">action</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">query</span>' { [ <span class="token operator">query</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--collection-path">'collection path'</a>
						'<span class="token string">query</span>': component <a href="#grammar-rule--custom-query">'custom query'</a>
					}
					'<span class="token string">query property</span>' { [ <span class="token operator">query</span> <span class="token operator">property</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query stategroup</span>' { [ <span class="token operator">query</span> <span class="token operator">stategroup</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query number</span>' { [ <span class="token operator">query</span> <span class="token operator">number</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query text</span>' { [ <span class="token operator">query</span> <span class="token operator">text</span> ]
						'<span class="token string">property</span>': reference
					}
					'<span class="token string">query file</span>' { [ <span class="token operator">query</span> <span class="token operator">file</span> ]
						'<span class="token string">property</span>': reference
					}
				)
				'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
			}
			'<span class="token string">configuration</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">list</span>' {
						'<span class="token string">properties</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--feature-properties-list">'feature properties list'</a>
					}
					'<span class="token string">stategroup</span>' {
						'<span class="token string">state</span>': reference
						'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
					}
					'<span class="token string">number</span>' {
						'<span class="token string">value</span>': integer
					}
					'<span class="token string">text</span>' {
						'<span class="token string">value</span>': text
					}
				)
			}
			'<span class="token string">feature</span>' {
				'<span class="token string">properties</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--feature-properties-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">feature properties list</span>' {
	'<span class="token string">has entry</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">entry</span>': component <a href="#grammar-rule--feature-properties">'feature properties'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--feature-properties-list">'feature properties list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--custom-query }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom query</span>' {
	'<span class="token string">custom limit</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">limit:</span> ]
			'<span class="token string">sample</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">sample size</span>': integer
					'<span class="token string">sample limit</span>': [ <span class="token operator">/</span>, <span class="token operator">/</span> ] integer
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">absolute limit</span>': integer
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">properties</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] dictionary {
		'<span class="token string">has more properties</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next property</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">context path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--query-path">'query path'</a>
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">property</span>': reference
				'<span class="token string">filter</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
						'<span class="token string">states</span>': [ <span class="token operator">?</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">is selected</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">selected</span> ] }
								'<span class="token string">no</span>' { }
							)
						}
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> <span class="token operator">simple</span> ] }
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">property</span>': reference
				'<span class="token string">filter</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
						'<span class="token string">operator</span>': stategroup (
							'<span class="token string">smaller</span>' { [ <span class="token operator"><</span> ] }
							'<span class="token string">smaller equal</span>' { [ <span class="token operator"><=</span> ] }
							'<span class="token string">greater</span>' { [ <span class="token operator">></span> ] }
							'<span class="token string">greater equal</span>' { [ <span class="token operator">>=</span> ] }
							'<span class="token string">equal</span>' { [ <span class="token operator">==</span> ] }
						)
						'<span class="token string">criteria</span>': stategroup (
							'<span class="token string">now</span>' { [ <span class="token operator">now</span> ]
								'<span class="token string">offset</span>': [ <span class="token operator">+</span> ] integer
							}
							'<span class="token string">static</span>' {
								'<span class="token string">value</span>': integer
							}
						)
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> <span class="token operator">simple</span> ] }
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">property</span>': reference
				'<span class="token string">filter</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
						'<span class="token string">criteria</span>': text
					}
					'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> <span class="token operator">simple</span> ] }
					'<span class="token string">containment</span>' { [ <span class="token operator">filter</span>, <span class="token operator">selection</span> ]
						'<span class="token string">operator</span>': stategroup (
							'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
							'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
						)
					}
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">property</span>': reference
			}
			'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
				'<span class="token string">attribute</span>': reference
			}
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">attribute</span>': reference
			}
		)
	}
	'<span class="token string">custom sorting</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">direction</span>': stategroup (
				'<span class="token string">ascending</span>' { [ <span class="token operator">@ascending:</span> ] }
				'<span class="token string">descending</span>' { [ <span class="token operator">@descending:</span> ] }
			)
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">number</span>' {
					'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
				}
				'<span class="token string">text</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
				}
			)
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--annotated-collection-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">annotated collection selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' { }
				'<span class="token string">collection</span>' { [ <span class="token operator">[]</span> ] }
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--annotated-collection-selector">'annotated collection selector'</a>
		}
		'<span class="token string">no</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-frame-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld frame selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">inline</span>' {
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-view-frame">'handheld view frame'</a>
		}
		'<span class="token string">annotated</span>' {
			'<span class="token string">frame</span>': reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-details }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view details</span>' {
	'<span class="token string">title</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">title:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">fields</span>': dictionary {
		'<span class="token string">has more fields</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next field</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">emphasis</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">@emphasis</span> ] }
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-elements }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view elements</span>' {
	'<span class="token string">has element</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">-></span> ] stategroup (
				'<span class="token string">label</span>' { [ <span class="token operator">label:</span> ]
					'<span class="token string">text</span>': reference
				}
				'<span class="token string">inline view</span>' { [ <span class="token operator">inline</span> <span class="token operator">view:</span> ]
					'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
				}
				'<span class="token string">view</span>' {
					'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-elements">'handheld view elements'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-frame }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view frame</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">decision</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">options</span>': dictionary {
				'<span class="token string">has more options</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next option</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">emphasis</span>': [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">low</span>' { }
					'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
					'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
				)
				'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
			}
		}
		'<span class="token string">collection navigation</span>' { [ <span class="token operator">collection</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">collection context</span>': [ <span class="token operator">path:</span> ] stategroup (
				'<span class="token string">this</span>' { }
				'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
			)
			'<span class="token string">path</span>': component <a href="#grammar-rule--annotated-collection-selector">'annotated collection selector'</a>
			'<span class="token string">annotations</span>': group {
				'<span class="token string">header</span>': stategroup (
					'<span class="token string">yes</span>' { }
					'<span class="token string">no</span>' { [ <span class="token operator">@no-header</span> ] }
				)
				'<span class="token string">layout</span>': stategroup (
					'<span class="token string">set</span>' { [ <span class="token operator">@layout:</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">tabular</span>' { [ <span class="token operator">tabular</span> ] }
							'<span class="token string">cards</span>' { [ <span class="token operator">cards</span> ] }
							'<span class="token string">buttons</span>' { [ <span class="token operator">buttons</span> ] }
							'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
								'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--query-path">'query path'</a>
								'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">simple</span>' { }
									'<span class="token string">year</span>' { [ <span class="token operator">by</span>, <span class="token operator">year</span> ] }
									'<span class="token string">month</span>' { [ <span class="token operator">by</span>, <span class="token operator">month</span> ] }
									'<span class="token string">week</span>' { [ <span class="token operator">by</span>, <span class="token operator">week</span> ] }
									'<span class="token string">day</span>' { [ <span class="token operator">by</span>, <span class="token operator">day</span> ] }
									'<span class="token string">hour</span>' { [ <span class="token operator">by</span>, <span class="token operator">hour</span> ] }
								)
							}
						)
					}
					'<span class="token string">default</span>' { }
				)
			}
			'<span class="token string">details</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
				}
				'<span class="token string">no</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
				}
			)
			'<span class="token string">filters</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">filters:</span> ]
					'<span class="token string">fields</span>': dictionary {
						'<span class="token string">has more fields</span>': stategroup = node-switch successor (
							| node = '<span class="token string">yes</span>' { '<span class="token string">next field</span>' = successor }
							| none = '<span class="token string">no</span>'
						)
						'<span class="token string">path</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--query-path">'query path'</a>
						'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">stategroup</span>' {
								'<span class="token string">filter</span>': stategroup (
									'<span class="token string">state</span>' {
										'<span class="token string">state</span>': [ <span class="token operator">is</span> ] reference
									}
									'<span class="token string">not state</span>' {
										'<span class="token string">state</span>': [ <span class="token operator">is</span> <span class="token operator">not</span> ] reference
									}
									'<span class="token string">states</span>' {
										'<span class="token string">states</span>': [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
									}
									'<span class="token string">simple</span>' { [ <span class="token operator">stategroup</span> ] }
								)
							}
							'<span class="token string">number</span>' {
								'<span class="token string">filter</span>': stategroup (
									'<span class="token string">match</span>' {
										'<span class="token string">operator</span>': stategroup (
											'<span class="token string">smaller</span>' { [ <span class="token operator">smaller</span> ] }
											'<span class="token string">smaller equal</span>' { [ <span class="token operator">smaller</span> <span class="token operator">or</span> <span class="token operator">equal</span> ] }
											'<span class="token string">greater</span>' { [ <span class="token operator">greater</span> ] }
											'<span class="token string">greater equal</span>' { [ <span class="token operator">greater</span> <span class="token operator">or</span> <span class="token operator">equal</span> ] }
											'<span class="token string">equal</span>' { [ <span class="token operator">equal</span> ] }
										)
										'<span class="token string">type</span>': [ <span class="token operator">than</span> ] stategroup (
											'<span class="token string">now</span>' { [ <span class="token operator">now</span> <span class="token operator">+</span> ] }
											'<span class="token string">static</span>' { }
										)
										'<span class="token string">offset</span>': integer
									}
									'<span class="token string">simple</span>' { [ <span class="token operator">number</span> ] }
								)
							}
							'<span class="token string">text</span>' {
								'<span class="token string">filter</span>': stategroup (
									'<span class="token string">pattern</span>' {
										'<span class="token string">criteria</span>': [ <span class="token operator">match</span> ] text
									}
									'<span class="token string">simple</span>' { [ <span class="token operator">text</span> ] }
									'<span class="token string">current node</span>' { [ <span class="token operator">this</span> ] }
									'<span class="token string">containment</span>' { [ <span class="token operator">filter</span>, <span class="token operator">selection</span> ]
										'<span class="token string">operator</span>': stategroup (
											'<span class="token string">in</span>' { [ <span class="token operator">in</span> ] }
											'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ] }
										)
									}
								)
							}
						)
					}
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">sort</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">sort:</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--query-path">'query path'</a>
					'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-property">'handheld view property'</a>
					'<span class="token string">direction</span>': stategroup (
						'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
						'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
					)
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">action</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">view:</span> ]
					'<span class="token string">emphasis</span>': stategroup (
						'<span class="token string">low</span>' { }
						'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
						'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
					)
					'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">group navigation</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
		}
		'<span class="token string">state navigation</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
		}
		'<span class="token string">reference navigation</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
		}
		'<span class="token string">pivot view</span>' { [ <span class="token operator">pivot</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">options</span>': group { dynamic-order
				'<span class="token string">show crosshair</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@crosshair</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">show grid</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@grid</span> ] }
					'<span class="token string">no</span>' { }
				)
			}
			'<span class="token string">columns</span>': [ <span class="token operator">columns:</span> <span class="token operator">.</span> ] reference
			'<span class="token string">column grouping</span>': [ <span class="token operator">:</span> ] reference
			'<span class="token string">column label</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
			'<span class="token string">cells</span>': [ <span class="token operator">cells:</span> <span class="token operator">.</span> ] reference
			'<span class="token string">row grouping</span>': [ <span class="token operator">:</span> ] reference
			'<span class="token string">row label</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
			'<span class="token string">content</span>': stategroup (
				'<span class="token string">inline view</span>' { [ <span class="token operator">inline</span> <span class="token operator">view:</span> ]
					'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
				}
				'<span class="token string">label</span>' { [ <span class="token operator">label:</span> ]
					'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
				}
			)
		}
		'<span class="token string">detail view</span>' { [ <span class="token operator">details</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
			'<span class="token string">elements</span>': component <a href="#grammar-rule--handheld-view-elements">'handheld view elements'</a>
		}
		'<span class="token string">command view</span>' { [ <span class="token operator">command</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
			'<span class="token string">selection</span>': [ <span class="token operator">view:</span> ] stategroup (
				'<span class="token string">button</span>' {
					'<span class="token string">emphasis</span>': stategroup (
						'<span class="token string">low</span>' { }
						'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
						'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
					)
				}
				'<span class="token string">scan</span>' { [ <span class="token operator">@scan</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">referencer</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">[]</span> ] reference
					}
					'<span class="token string">path</span>': [ <span class="token operator">using:</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
					'<span class="token string">search property</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">view</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-descriptor }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view descriptor</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic</span>' {
			'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-property-selector">'handheld view property selector'</a>
		}
		'<span class="token string">static text</span>' {
			'<span class="token string">text</span>': reference
		}
		'<span class="token string">icon</span>' {
			'<span class="token string">icon name</span>': [ <span class="token operator">icon:</span> ] text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view property</span>' {
	'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">default</span>' { }
		'<span class="token string">barcode</span>' { [ <span class="token operator">@barcode:</span> ]
			'<span class="token string">barcode type</span>': stategroup (
				'<span class="token string">CODE128</span>' { [ <span class="token operator">CODE128</span> ] }
				'<span class="token string">CODE128A</span>' { [ <span class="token operator">CODE128A</span> ] }
				'<span class="token string">CODE128B</span>' { [ <span class="token operator">CODE128B</span> ] }
				'<span class="token string">CODE128C</span>' { [ <span class="token operator">CODE128C</span> ] }
				'<span class="token string">EAN13</span>' { [ <span class="token operator">EAN13</span> ] }
				'<span class="token string">EAN8</span>' { [ <span class="token operator">EAN8</span> ] }
				'<span class="token string">EAN5</span>' { [ <span class="token operator">EAN5</span> ] }
				'<span class="token string">EAN2</span>' { [ <span class="token operator">EAN2</span> ] }
				'<span class="token string">UPCA</span>' { [ <span class="token operator">UPCA</span> ] }
				'<span class="token string">UPCE</span>' { [ <span class="token operator">UPCE</span> ] }
				'<span class="token string">CODE39</span>' { [ <span class="token operator">CODE39</span> ] }
				'<span class="token string">ITF</span>' { [ <span class="token operator">ITF</span> ] }
				'<span class="token string">ITF14</span>' { [ <span class="token operator">ITF14</span> ] }
				'<span class="token string">MSI10</span>' { [ <span class="token operator">MSI10</span> ] }
				'<span class="token string">MSI11</span>' { [ <span class="token operator">MSI11</span> ] }
				'<span class="token string">MSI1010</span>' { [ <span class="token operator">MSI1010</span> ] }
				'<span class="token string">MSI1110</span>' { [ <span class="token operator">MSI1110</span> ] }
				'<span class="token string">Pharmacode</span>' { [ <span class="token operator">Pharmacode</span> ] }
				'<span class="token string">Codabar</span>' { [ <span class="token operator">Codabar</span> ] }
			)
		}
		'<span class="token string">qrcode</span>' { [ <span class="token operator">@qrcode</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-property-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view property selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">switch</span>' {
			'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-property-selector">'handheld view property selector'</a>
			}
		}
		'<span class="token string">step</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-property-selector">'handheld view property selector'</a>
		}
		'<span class="token string">property</span>' {
			'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-property">'handheld view property'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-command-annotations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld command annotations</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
			}
			'<span class="token string">stategroup</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
				'<span class="token string">states</span>': dictionary {
					'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
				}
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">style</span>': stategroup (
					'<span class="token string">buttons</span>' { [ <span class="token operator">@button</span> ] }
					'<span class="token string">keyboard</span>' { [ <span class="token operator">@keyboard</span> ] }
					'<span class="token string">default</span>' { }
					'<span class="token string">scan</span>' { [ <span class="token operator">@scan</span> <span class="token operator">using:</span> ]
						'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
						'<span class="token string">search property</span>': [ <span class="token operator">.</span> ] reference
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view context</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-context">'handheld view context'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--handheld-view-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">handheld view selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">switch</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
			}
		}
		'<span class="token string">step</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--handheld-view-selector">'handheld view selector'</a>
		}
		'<span class="token string">command</span>' {
			'<span class="token string">command</span>': [ <span class="token operator">command:</span> ] reference
			'<span class="token string">annotations</span>': group { dynamic-order
				'<span class="token string">auto execute</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@auto-execute</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">close after execute</span>': stategroup (
					'<span class="token string">yes</span>' { }
					'<span class="token string">no</span>' { [ <span class="token operator">@keep-open</span> ] }
				)
				'<span class="token string">emphasis</span>': stategroup (
					'<span class="token string">low</span>' { }
					'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
					'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
				)
			}
			'<span class="token string">parameter annotations</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">parameters</span>': component <a href="#grammar-rule--handheld-command-annotations">'handheld command annotations'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">open view</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">and</span> ]
					'<span class="token string">context</span>': component <a href="#grammar-rule--handheld-view-context">'handheld view context'</a>
					'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">has details</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">details</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">details</span>': component <a href="#grammar-rule--handheld-view-details">'handheld view details'</a>
					'<span class="token string">elements</span>': component <a href="#grammar-rule--handheld-view-elements">'handheld view elements'</a>
				}
			)
		}
		'<span class="token string">view</span>' {
			'<span class="token string">emphasis</span>': [ <span class="token operator">:</span> ] stategroup (
				'<span class="token string">low</span>' { }
				'<span class="token string">medium</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">medium</span> ] }
				'<span class="token string">high</span>' { [ <span class="token operator">@emphasis:</span> <span class="token operator">high</span> ] }
			)
			'<span class="token string">context</span>': component <a href="#grammar-rule--handheld-view-context">'handheld view context'</a>
			'<span class="token string">frame</span>': component <a href="#grammar-rule--handheld-frame-selector">'handheld frame selector'</a>
			'<span class="token string">title</span>': stategroup (
				'<span class="token string">custom</span>' { [ <span class="token operator">title:</span> ]
					'<span class="token string">property</span>': component <a href="#grammar-rule--handheld-view-descriptor">'handheld view descriptor'</a>
				}
				'<span class="token string">default</span>' { }
			)
		}
	)
}
</pre>
</div>
</div>
