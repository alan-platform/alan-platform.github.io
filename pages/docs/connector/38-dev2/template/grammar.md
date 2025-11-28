---
layout: "doc"
origin: "connector"
language: "template"
version: "38-dev2"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">prefix</span>': text
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': component <a href="#grammar-rule--statement">'statement'</a>
</pre>
</div>
</div>

{: #grammar-rule--named-object-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">named object assignment</span>' {
	'<span class="token string">name</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">name</span>': reference = first
			'<span class="token string">named objects</span>': dictionary { [ <span class="token operator">$</span> ]
				'<span class="token string">has successor</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { }
					| none = '<span class="token string">no</span>'
				)
			}
		}
		'<span class="token string">implicit</span>' { [ <span class="token operator">$</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--optional-named-object-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional named object assignment</span>' {
	'<span class="token string">has assignment</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">assignment</span>': component <a href="#grammar-rule--named-object-assignment">'named object assignment'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ancestor-named-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor named object path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">$^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-named-object-path">'ancestor named object path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--named-object-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">named object step</span>' {
	'<span class="token string">name</span>': stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-named-object-path">'ancestor named object path'</a>
			'<span class="token string">named object</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">implicit</span>' { [ <span class="token operator">$</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--object-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object path step</span>' {
	'<span class="token string">property</span>': reference
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
		'<span class="token string">state</span>' {
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">scalar</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--object-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object path tail</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': [ <span class="token operator">.</span> ] component <a href="#grammar-rule--object-path-step">'object path step'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">context</span>': stategroup (
				'<span class="token string">variable</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--named-object-step">'named object step'</a>
				}
				'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
				'<span class="token string">number</span>' {
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">text</span>' {
					'<span class="token string">value</span>': text
				}
			)
		}
		'<span class="token string">implicit</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--object-path-step">'object path step'</a>
		}
	)
	'<span class="token string">steps</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--number-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number path</span>' {
	'<span class="token string">object</span>': component <a href="#grammar-rule--object-path">'object path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--text-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text path</span>' {
	'<span class="token string">object</span>': component <a href="#grammar-rule--object-path">'object path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">statement</span>' {
	'<span class="token string">has statement</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
					'<span class="token string">objects</span>': component <a href="#grammar-rule--object-path">'object path'</a>
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
					'<span class="token string">prefix</span>': text
					'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
					'<span class="token string">suffix</span>': [ <span class="token operator">/walk</span> ] text
				}
				'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
					'<span class="token string">stategroup</span>': component <a href="#grammar-rule--object-path">'object path'</a>
					'<span class="token string">empty</span>': text
					'<span class="token string">states</span>': dictionary { [ <span class="token operator">case</span> ]
						'<span class="token string">variable</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
						'<span class="token string">prefix</span>': text
						'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
						'<span class="token string">empty</span>': [ <span class="token operator">/case</span> ] text
					}
					'<span class="token string">suffix</span>': [ <span class="token operator">/switch</span> ] text
				}
				'<span class="token string">object switch</span>' { [ <span class="token operator">switch</span> ]
					'<span class="token string">object</span>': component <a href="#grammar-rule--object-path">'object path'</a>
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">lookup</span>' {
							'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--text-path">'text path'</a>
							'<span class="token string">tail</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
						}
						'<span class="token string">equality</span>' { [ <span class="token operator">is</span> ]
							'<span class="token string">other</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] stategroup (
								'<span class="token string">object</span>' {
									'<span class="token string">other object</span>': component <a href="#grammar-rule--object-path">'object path'</a>
								}
								'<span class="token string">first</span>' { [ <span class="token operator">first</span> ] }
								'<span class="token string">last</span>' { [ <span class="token operator">last</span> ] }
							)
						}
						'<span class="token string">existence</span>' { }
					)
					'<span class="token string">empty</span>': text
					'<span class="token string">node</span>': [ <span class="token operator">case</span> <span class="token operator">node</span> ] group {
						'<span class="token string">variable</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
						'<span class="token string">prefix</span>': text
						'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
						'<span class="token string">empty</span>': [ <span class="token operator">/case</span> ] text
					}
					'<span class="token string">none</span>': stategroup (
						'<span class="token string">yes</span>' { [ <span class="token operator">case</span> <span class="token operator">none</span> ]
							'<span class="token string">prefix</span>': text
							'<span class="token string">none</span>': component <a href="#grammar-rule--statement">'statement'</a>
							'<span class="token string">empty</span>': [ <span class="token operator">/case</span> ] text
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">suffix</span>': [ <span class="token operator">/switch</span> ] text
				}
				'<span class="token string">format</span>' { [ <span class="token operator">format</span> ]
					'<span class="token string">object</span>': component <a href="#grammar-rule--object-path">'object path'</a>
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">number</span>' {
							'<span class="token string">with base</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">/</span> ]
									'<span class="token string">base</span>': component <a href="#grammar-rule--number-path">'number path'</a>
								}
								'<span class="token string">no</span>' { }
							)
							'<span class="token string">style</span>': stategroup (
								'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ] }
								'<span class="token string">currency</span>' { [ <span class="token operator">currency=</span> ]
									'<span class="token string">currency</span>': component <a href="#grammar-rule--text-path">'text path'</a>
								}
								'<span class="token string">spellout</span>' { [ <span class="token operator">spellout</span> ] }
							)
							'<span class="token string">styling</span>': dictionary {
								'<span class="token string">value</span>': [ <span class="token operator">=</span> ] stategroup (
									'<span class="token string">off</span>' { [ <span class="token operator">off</span> ] }
									'<span class="token string">object</span>' {
										'<span class="token string">object</span>': component <a href="#grammar-rule--object-path">'object path'</a>
									}
								)
							}
						}
						'<span class="token string">date time</span>' {
							'<span class="token string">with time</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">date-time</span> ] }
								'<span class="token string">no</span>' { [ <span class="token operator">date</span> ] }
							)
							'<span class="token string">style</span>': stategroup (
								'<span class="token string">pattern</span>' { [ <span class="token operator">style=</span> ]
									/* https://unicode-org.github.io/icu/userguide/format_parse/datetime/#date-field-symbol-table */
									'<span class="token string">value</span>': component <a href="#grammar-rule--text-path">'text path'</a>
								}
								'<span class="token string">full</span>' { [ <span class="token operator">style=full</span> ] }
								'<span class="token string">long</span>' { [ <span class="token operator">style=long</span> ] }
								'<span class="token string">medium</span>' { [ <span class="token operator">style=medium</span> ] }
								'<span class="token string">short</span>' { [ <span class="token operator">style=short</span> ] }
							)
							'<span class="token string">styling</span>': dictionary {
								'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--text-path">'text path'</a>
							}
						}
					)
					'<span class="token string">suffix</span>': text
				}
				'<span class="token string">text</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--text-path">'text path'</a>
					'<span class="token string">escaping</span>': stategroup (
						'<span class="token string">default</span>' { }
						'<span class="token string">overwrite</span>' {
							'<span class="token string">dictionary</span>': [ <span class="token operator">escape=(</span>, <span class="token operator">)</span> ] dictionary {
								'<span class="token string">text</span>': [ <span class="token operator">=</span> ] text
							}
						}
						'<span class="token string">none</span>' { [ <span class="token operator">escape=none</span> ] }
					)
					'<span class="token string">suffix</span>': text
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
