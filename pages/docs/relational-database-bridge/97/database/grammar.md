---
layout: doc
origin: relational-database-bridge
language: database
version: 97
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--tables }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">tables</span>': dictionary @order: .'<span class="token string">dependency graph</span>' { @section
	'<span class="token string">source</span>': [ <span class="token operator">:</span> <span class="token operator">table</span> <span class="token operator">=</span> ] group {
		'<span class="token string">scoped</span>': stategroup (
			'<span class="token string">yes</span>' {
				'<span class="token string">namespace</span>': text
				'<span class="token string">selection</span>': component <a href="#grammar-rule--table-selector">'table selector'</a>
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">source</span>': text
		'<span class="token string">inline tables</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">inline-tables</span> <span class="token operator">(experimental)</span> ]
				'<span class="token string">sub tables</span>': dictionary { @block indent
					'<span class="token string">fields</span>': [ <span class="token operator">fields</span> ] dictionary { @block indent
						'<span class="token string">definition</span>': component <a href="#grammar-rule--field">'field'</a>
					}
					'<span class="token string">join key</span>': [ <span class="token operator">join</span> ] dictionary { @block indent
						'<span class="token string">contra field</span>': [ <span class="token operator">==</span> ] reference
					}
				}
			}
			'<span class="token string">no</span>' { }
		)
	}
	'<span class="token string">fields</span>': @block indent [ <span class="token operator">fields</span> ] dictionary { @block indent
		'<span class="token string">source</span>': [ <span class="token operator">=</span> ] stategroup (
			'<span class="token string">reference</span>' {
				'<span class="token string">field</span>': text
				'<span class="token string">definition</span>': component <a href="#grammar-rule--field">'field'</a>
			}
			'<span class="token string">inline reference</span>' { [ <span class="token operator">inline</span> ]
				'<span class="token string">inline table</span>': reference
				'<span class="token string">inline field</span>': [ <span class="token operator">.</span> ] reference
			}
		)
	}
	'<span class="token string">has primary key</span>': stategroup (
		'<span class="token string">yes</span>' { @block indent [ <span class="token operator">primary-key</span> ]
			'<span class="token string">primary key</span>': dictionary { @block indent }
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">unique indices</span>': dictionary { @block indent [ <span class="token operator">unique-index</span> ]
		'<span class="token string">fields</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { @block indent }
	}
	'<span class="token string">foreign keys</span>': @block indent [ <span class="token operator">foreign-keys</span> ] dictionary { @block indent
		'<span class="token string">table</span>': [ <span class="token operator">=></span> <span class="token operator">table</span> ] reference
		'<span class="token string">on</span>': @block indent [ <span class="token operator">where</span> ] stategroup (
			'<span class="token string">primary key</span>' { [ <span class="token operator">primary-key</span> ]
				'<span class="token string">key fields</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { @block indent
					'<span class="token string">contra field</span>': [ <span class="token operator">==</span> ] reference
				}
			}
			'<span class="token string">unique index</span>' { [ <span class="token operator">unique-index</span> ]
				'<span class="token string">index</span>': reference
				'<span class="token string">key fields</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { @block indent
					'<span class="token string">contra field</span>': [ <span class="token operator">==</span> ] reference
				}
			}
		)
	}
	'<span class="token string">text encoding</span>': stategroup (
		'<span class="token string">ascii</span>' { }
		'<span class="token string">utf8</span>' { @block indent [ <span class="token operator">text-encoding</span> <span class="token operator">:</span> <span class="token operator">utf8</span> ] }
	)
	'<span class="token string">prefilters</span>': group {
		'<span class="token string">join statements</span>': dictionary { @block indent [ <span class="token operator">join</span> ] }
		'<span class="token string">has where clause</span>': stategroup (
			'<span class="token string">yes</span>' { @block indent [ <span class="token operator">where</span> ]
				'<span class="token string">where statement</span>': component <a href="#grammar-rule--filter-statement-list">'filter statement list'</a>
			}
			'<span class="token string">no</span>' { }
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--field }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">field</span>' {
	'<span class="token string">data type</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
			'<span class="token string">import rule</span>': stategroup (
				'<span class="token string">fixed length</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">rule: trim</span>': stategroup (
						'<span class="token string">both</span>' { [ <span class="token operator">trim-both</span> ] }
						'<span class="token string">left</span>' { [ <span class="token operator">trim-left</span> ] }
						'<span class="token string">right</span>' { [ <span class="token operator">trim-right</span> ] }
						'<span class="token string">none</span>' { }
					)
					'<span class="token string">length</span>': integer
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">floating point</span>' { [ <span class="token operator">float</span> ] }
		'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
			'<span class="token string">rounding</span>': stategroup (
				'<span class="token string">ordinary</span>' { }
				'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
				'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
			)
			'<span class="token string">scale</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] integer
		}
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
		'<span class="token string">boolean</span>' { [ <span class="token operator">bool</span> ] }
		'<span class="token string">enum</span>' { [ <span class="token operator">enum</span> ]
			'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
		}
	)
	'<span class="token string">nullable</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">(nullable)</span> ] }
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">description</span>': [ <span class="token operator"></</span>, <span class="token operator">/></span> ] text
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--table-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">table selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">name</span>': [ <span class="token operator">.</span> ] text
			'<span class="token string">tail</span>': component <a href="#grammar-rule--table-selector">'table selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number list</span>' {
	'<span class="token string">step type</span>': stategroup (
		'<span class="token string">single value</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">range</span>' {
			'<span class="token string">begin value</span>': integer
			'<span class="token string">end value</span>': [ <span class="token operator">...</span> ] integer
		}
	)
	'<span class="token string">has more steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--number-list">'number list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--filter-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">filter statement</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">contains</span>' {
			'<span class="token string">field</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">comparison</span>': stategroup (
				'<span class="token string">in</span>' { [ <span class="token operator">in</span> ]
					'<span class="token string">arguments</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
				}
				'<span class="token string">not in</span>' { [ <span class="token operator">not</span> <span class="token operator">in</span> ]
					'<span class="token string">arguments</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { }
				}
			)
		}
		'<span class="token string">search</span>' {
			'<span class="token string">field</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">starts with</span>' { [ <span class="token operator">starts-with</span> ] }
				'<span class="token string">contains</span>' { [ <span class="token operator">contains</span> ] }
				'<span class="token string">equals</span>' { [ <span class="token operator">equals</span> ] }
			)
			'<span class="token string">substring</span>': text
		}
		'<span class="token string">compare</span>' {
			'<span class="token string">field</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">operator</span>': stategroup (
				'<span class="token string">smaller</span>' { [ <span class="token operator"><</span> ] }
				'<span class="token string">greater</span>' { [ <span class="token operator">></span> ] }
				'<span class="token string">equal</span>' { [ <span class="token operator">==</span> ] }
				'<span class="token string">not equal</span>' { [ <span class="token operator">!=</span> ] }
			)
			'<span class="token string">right</span>': stategroup (
				'<span class="token string">property</span>' {
					'<span class="token string">right</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">static number</span>' {
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">static text</span>' {
					'<span class="token string">value</span>': text
				}
				'<span class="token string">time span</span>' {
					'<span class="token string">days</span>': [ <span class="token operator">current-date</span> <span class="token operator">-</span> ] integer
				}
			)
		}
		'<span class="token string">in list</span>' {
			'<span class="token string">field</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">number list</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--number-list">'number list'</a>
		}
		'<span class="token string">foreign key</span>' { [ <span class="token operator">foreign-key</span> ]
			'<span class="token string">foreign key</span>': reference
		}
		'<span class="token string">incoming foreign key</span>' { [ <span class="token operator">this</span> ]
			'<span class="token string">source table</span>': [ <span class="token operator">in</span> <span class="token operator">table</span> ] reference
			'<span class="token string">incoming link</span>': [ <span class="token operator">>></span> ] reference
		}
		'<span class="token string">invert</span>' { [ <span class="token operator">not</span> ]
			'<span class="token string">statement</span>': component <a href="#grammar-rule--filter-statement">'filter statement'</a>
		}
		'<span class="token string">list</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">statements</span>': @block indent component <a href="#grammar-rule--filter-statement-list">'filter statement list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--filter-statement-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">filter statement list</span>' {
	'<span class="token string">statement</span>': component <a href="#grammar-rule--filter-statement">'filter statement'</a>
	'<span class="token string">has more statements</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">operator</span>': stategroup (
				'<span class="token string">and</span>' { [ <span class="token operator">and</span> ] }
				'<span class="token string">or</span>' { [ <span class="token operator">or</span> ] }
			)
			'<span class="token string">tail</span>': @block component <a href="#grammar-rule--filter-statement-list">'filter statement list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
