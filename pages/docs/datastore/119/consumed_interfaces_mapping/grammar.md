---
layout: "doc"
origin: "datastore"
language: "consumed_interfaces_mapping"
version: "119"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">imported interfaces</span>': [ <span class="token operator">imported-interfaces</span> ] dictionary {
	'<span class="token string">interface</span>': [ <span class="token operator">=</span> ] reference
	'<span class="token string">parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">source parameter</span>': [ <span class="token operator">=</span> ] reference
	}
	'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--application-rules-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application rules mapping</span>' {
	'<span class="token string">rules</span>': dictionary { [ <span class="token operator">where</span> ]
		'<span class="token string">source rule</span>': [ <span class="token operator">=</span> ] reference
	}
}
</pre>
</div>
</div>

{: #grammar-rule--interface-rules-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface rules mapping</span>' {
	'<span class="token string">rules</span>': dictionary { [ <span class="token operator">where</span> ]
		'<span class="token string">source rule</span>': [ <span class="token operator">=</span> ] reference
	}
}
</pre>
</div>
</div>

{: #grammar-rule--node-type-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
				'<span class="token string">type</span>': [ <span class="token operator">=></span> ] stategroup (
					'<span class="token string">internal</span>' {
						'<span class="token string">source event</span>': [ <span class="token operator">handle</span> ] reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
					}
					'<span class="token string">external</span>' {
						'<span class="token string">target command</span>': [ <span class="token operator">execute</span> ] reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
					}
				)
			}
			'<span class="token string">property</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">text</span>': [ <span class="token operator">=</span> ] reference
						'<span class="token string">has rules</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' {
								'<span class="token string">rules mapping</span>': component <a href="#grammar-rule--application-rules-mapping">'application rules mapping'</a>
							}
						)
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">number</span>': [ <span class="token operator">=</span> ] reference
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">file</span>': [ <span class="token operator">=</span> ] reference
					}
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">group</span>': [ <span class="token operator">=</span> ] reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
					}
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> <span class="token operator">=</span> ]
						'<span class="token string">collection</span>': reference
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">=</span> ]
						'<span class="token string">state group</span>': reference
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
							'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
							'<span class="token string">has rules</span>': stategroup (
								'<span class="token string">no</span>' { }
								'<span class="token string">yes</span>' {
									'<span class="token string">rules mapping</span>': component <a href="#grammar-rule--application-rules-mapping">'application rules mapping'</a>
								}
							)
							'<span class="token string">mapping</span>': component <a href="#grammar-rule--node-type-mapping">'node type mapping'</a>
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

{: #grammar-rule--parameter-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter mapping</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">properties</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">text</span>': [ <span class="token operator">=</span> ] reference
				'<span class="token string">has rules</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' {
						'<span class="token string">rules mapping</span>': component <a href="#grammar-rule--interface-rules-mapping">'interface rules mapping'</a>
					}
				)
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">number</span>': [ <span class="token operator">=</span> ] reference
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">file</span>': [ <span class="token operator">=</span> ] reference
			}
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> <span class="token operator">=</span> ]
				'<span class="token string">group</span>': reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> <span class="token operator">=</span> ]
				'<span class="token string">collection</span>': reference
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> <span class="token operator">=</span> ]
				'<span class="token string">state group</span>': reference
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">target state</span>': [ <span class="token operator">=></span> ] reference
					'<span class="token string">has rules</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' {
							'<span class="token string">rules mapping</span>': component <a href="#grammar-rule--interface-rules-mapping">'interface rules mapping'</a>
						}
					)
					'<span class="token string">mapping</span>': component <a href="#grammar-rule--parameter-mapping">'parameter mapping'</a>
				}
			}
		)
	}
}
</pre>
</div>
</div>
