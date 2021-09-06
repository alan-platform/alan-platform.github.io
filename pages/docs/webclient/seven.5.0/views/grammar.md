---
layout: doc
origin: webclient
language: views
version: seven.5.0
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--dependencies }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dependencies</span>': dictionary { [ <span class="token operator">using</span> ] }
</pre>
</div>
</div>

{: #grammar-rule--views }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">views</span>': dictionary {
	'<span class="token string">translate title</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">title</span>': [ <span class="token operator">as</span> ] reference
		}
	)
	'<span class="token string">start context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
	'<span class="token string">node type</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--gui-node-type-path">'gui node type path'</a>
	'<span class="token string">queries</span>': dictionary { [ <span class="token operator">query</span> ]
		'<span class="token string">context</span>': [ <span class="token operator">from</span> ] stategroup (
			'<span class="token string">node</span>' {
				'<span class="token string">switch</span>': stategroup (
					'<span class="token string">current</span>' {
						'<span class="token string">query context</span>': component <a href="#grammar-rule--gui-node-type-path-step">'gui node type path step'</a>
					}
					'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
				)
				'<span class="token string">path</span>': [ <span class="token operator">path</span> ] component <a href="#grammar-rule--query-path">'query path'</a>
			}
			'<span class="token string">candidates</span>' { [ <span class="token operator">candidates</span> <span class="token operator">of</span> ]
				'<span class="token string">property context</span>': component <a href="#grammar-rule--gui-node-type-path-step">'gui node type path step'</a>
				'<span class="token string">property</span>': [ <span class="token operator">reference:</span> ] reference
			}
		)
		'<span class="token string">todo filter</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">where</span> <span class="token operator">has-todo</span> ]
				'<span class="token string">path</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">query limits</span>': [ <span class="token operator">limit:</span> ] group {
			'<span class="token string">sample size</span>': integer
			'<span class="token string">show all limit</span>': [ <span class="token operator">/</span> ] integer
			'<span class="token string">absolute maximum</span>': [ <span class="token operator">/</span> ] integer
		}
		'<span class="token string">has columns</span>': stategroup = node-switch .'<span class="token string">columns</span>' (
			| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
			| none  = '<span class="token string">no</span>'
		)
		'<span class="token string">columns</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] dictionary {
			'<span class="token string">has successor</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">name</span>': reference
			'<span class="token string">column type</span>': stategroup (
				'<span class="token string">id</span>' { [ <span class="token operator">id</span> ] }
				'<span class="token string">content</span>' { }
			)
			'<span class="token string">path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--conditional-path">'conditional path'</a>
			'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
				'<span class="token string">text</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">text</span> ] reference
					'<span class="token string">filter</span>': stategroup (
						'<span class="token string">none</span>' { }
						'<span class="token string">simple</span>' { [ <span class="token operator">filter</span> ]
							'<span class="token string">criteria</span>': text
						}
						'<span class="token string">current id path</span>' { [ <span class="token operator">filter</span> ] }
					)
				}
				'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
					'<span class="token string">file</span>': reference
				}
				'<span class="token string">number</span>' {
					'<span class="token string">number</span>': [ <span class="token operator">number</span> ] reference
					'<span class="token string">has filter</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
							'<span class="token string">operator selected</span>': stategroup (
								'<span class="token string">no</span>' { }
								'<span class="token string">yes</span>' {
									'<span class="token string">operator</span>': stategroup (
										'<span class="token string">smaller than</span>' { [ <span class="token operator"><</span> ] }
										'<span class="token string">smaller than or equal to</span>' { [ <span class="token operator"><=</span> ] }
										'<span class="token string">equal to</span>' { [ <span class="token operator">=</span> ] }
										'<span class="token string">greater than or equal to</span>' { [ <span class="token operator">>=</span> ] }
										'<span class="token string">greater than</span>' { [ <span class="token operator">></span> ] }
									)
								}
							)
							'<span class="token string">initial criteria</span>': stategroup (
								'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
								'<span class="token string">yes</span>' {
									'<span class="token string">source</span>': stategroup (
										'<span class="token string">now</span>' { [ <span class="token operator">now</span> ]
											'<span class="token string">has offset</span>': stategroup (
												'<span class="token string">none</span>' { }
												'<span class="token string">yes</span>' {
													'<span class="token string">offset</span>': [ <span class="token operator">+</span> ] integer
												}
											)
										}
										'<span class="token string">static</span>' {
											'<span class="token string">number</span>': integer //fixme nest criteria in operator selected
										}
									)
								}
							)
						}
					)
				}
				'<span class="token string">state group</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">stategroup</span> ] reference
					'<span class="token string">has filter</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">filter</span> ]
							'<span class="token string">filter enabled</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
								'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
							)
							'<span class="token string">states</span>': [ <span class="token operator">?</span> ] dictionary { [ <span class="token operator">|</span> ]
								'<span class="token string">is selected</span>': stategroup (
									'<span class="token string">no</span>' { }
									'<span class="token string">yes</span>' { [ <span class="token operator">selected</span> ] }
								)
							}
						}
					)
				}
				'<span class="token string">widget</span>' {
					'<span class="token string">widget column context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">instance</span>': component <a href="#grammar-rule--widget-instance">'widget instance'</a>
				}
			)
		}
	}
	'<span class="token string">instance</span>': component <a href="#grammar-rule--widget-expression">'widget expression'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--model-context }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">model context</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--gui-node-type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui node type path step</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' { }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--gui-node-type-path-step">'gui node type path step'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--gui-node-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui node type path</span>' {
	'<span class="token string">steps</span>': component <a href="#grammar-rule--gui-node-type-path-step">'gui node type path step'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--gui-widget-configuration-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui widget configuration list</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">]</span> ] }
		'<span class="token string">yes</span>' {
			'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--gui-widget-configuration-list">'gui widget configuration list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--view-context-parent-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">view context parent path</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state parent</span>' { [ <span class="token operator">?^</span> ] }
		'<span class="token string">collection parent</span>' { [ <span class="token operator">.^</span> ] }
		'<span class="token string">group parent</span>' { [ <span class="token operator">+^</span> ] }
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--view-context-parent-path">'view context parent path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--view-context-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">view context path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">query entry</span>' { [ <span class="token operator">entry</span> ] }
				'<span class="token string">parent</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--view-context-parent-path">'view context parent path'</a>
				}
				'<span class="token string">reference</span>' { [ <span class="token operator">></span> ] }
				'<span class="token string">entity</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">state rule</span>' { [ <span class="token operator">*&</span> ] }
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--widget-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">group</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
			'<span class="token string">group context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
			'<span class="token string">next</span>': component <a href="#grammar-rule--widget-expression">'widget expression'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
			'<span class="token string">state context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
			'<span class="token string">next</span>': component <a href="#grammar-rule--widget-expression">'widget expression'</a>
		}
		'<span class="token string">switch</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">switch</span> ] reference
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">state context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
				'<span class="token string">next</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--widget-expression">'widget expression'</a>
			}
		}
		'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">parent context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
			'<span class="token string">next</span>': component <a href="#grammar-rule--widget-expression">'widget expression'</a>
		}
		'<span class="token string">widget</span>' {
			'<span class="token string">widget</span>': component <a href="#grammar-rule--widget-instance">'widget instance'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--widget-instance }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget instance</span>' {
	'<span class="token string">widget</span>': reference
	'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--gui-widget-configuration-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui widget configuration attribute</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">widget</span>' { [ <span class="token operator">:</span> <span class="token operator">widget</span> ]
			'<span class="token string">instance</span>': component <a href="#grammar-rule--widget-expression">'widget expression'</a>
		}
		'<span class="token string">window</span>' {
			'<span class="token string">window</span>': [ <span class="token operator">window</span> ] reference
			'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
		}
		'<span class="token string">view</span>' {
			'<span class="token string">render</span>': stategroup (
				'<span class="token string">inline</span>' { [ <span class="token operator">:</span> <span class="token operator">inline</span> <span class="token operator">view</span> ] }
				'<span class="token string">in window</span>' { [ <span class="token operator">:</span> <span class="token operator">open</span> <span class="token operator">view</span> ]
					'<span class="token string">window</span>': [ <span class="token operator">@</span> ] reference
				}
			)
			'<span class="token string">using views</span>': stategroup (
				'<span class="token string">internal</span>' { }
				'<span class="token string">external</span>' { [ <span class="token operator">from</span> ]
					'<span class="token string">views</span>': reference
				}
			)
			'<span class="token string">view context</span>': component <a href="#grammar-rule--view-context-path">'view context path'</a>
			'<span class="token string">view</span>': [ <span class="token operator">:</span> ] reference
		}
		'<span class="token string">configuration</span>' { [ <span class="token operator">:</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">number</span>' {
					'<span class="token string">source</span>': stategroup (
						'<span class="token string">now</span>' { [ <span class="token operator">now</span> ]
							'<span class="token string">has offset</span>': stategroup (
								'<span class="token string">none</span>' { }
								'<span class="token string">yes</span>' {
									'<span class="token string">offset</span>': [ <span class="token operator">+</span> ] integer
								}
							)
						}
						'<span class="token string">static</span>' {
							'<span class="token string">number</span>': integer
						}
					)
				}
				'<span class="token string">text</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">static</span>' {
							'<span class="token string">value</span>': text
						}
						'<span class="token string">phrase</span>' {
							'<span class="token string">value</span>': reference
						}
					)
				}
				'<span class="token string">list</span>' {
					'<span class="token string">list</span>': [ <span class="token operator">[</span> ] component <a href="#grammar-rule--gui-widget-configuration-list">'gui widget configuration list'</a>
				}
				'<span class="token string">states list</span>' {
					'<span class="token string">has states</span>': stategroup = node-switch .'<span class="token string">states</span>' (
						| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
						| none  = '<span class="token string">no</span>'
					)
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
						'<span class="token string">has successor</span>': stategroup = node-switch successor (
							| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
							| none = '<span class="token string">no</span>'
						)
						'<span class="token string">configuration</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
					}
				}
				'<span class="token string">state group</span>' {
					'<span class="token string">state</span>': reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
			)
		}
		'<span class="token string">model binding</span>' { [ <span class="token operator">::</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">window</span>' { [ <span class="token operator">window</span> ]
					'<span class="token string">window</span>': reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">entity</span>' { [ <span class="token operator">entity</span> ]
					'<span class="token string">context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">current node</span>' { [ <span class="token operator">node</span> ]
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">collection context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">ordered graph</span>' { [ <span class="token operator">ordered-graph</span> ]
					'<span class="token string">ordered graph</span>': [ <span class="token operator">:</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">sort property</span>' { [ <span class="token operator">sort</span> ]
					'<span class="token string">on</span>': stategroup (
						'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
						'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
						'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ] }
					)
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">property</span>': reference
					'<span class="token string">property context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">query</span>' { [ <span class="token operator">query</span> ]
					'<span class="token string">query context</span>': stategroup (
						'<span class="token string">node</span>' {
							'<span class="token string">switch</span>': stategroup (
								'<span class="token string">root</span>' { [ <span class="token operator">on</span> <span class="token operator">root</span> ]
									'<span class="token string">query</span>': reference
								}
								'<span class="token string">current node</span>' {
									'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
									'<span class="token string">query</span>': reference
								}
							)
						}
						'<span class="token string">candidates</span>' { [ <span class="token operator">candidates</span> ]
							'<span class="token string">query</span>': reference
						}
					)
					'<span class="token string">has refresh interval</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">refresh:</span> ]
							'<span class="token string">interval</span>': integer
						}
					)
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">group</span>': [ <span class="token operator">group</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">state group</span>': reference
					'<span class="token string">configuration</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">state</span>' { [ <span class="token operator">state</span> ]
					'<span class="token string">state group context</span>': stategroup (
						'<span class="token string">states list</span>' { }
						'<span class="token string">state group binding</span>' {
							'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
						}
					)
					'<span class="token string">state context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">state rule</span>' { [ <span class="token operator">*&</span> ]
					'<span class="token string">rule</span>': reference
					'<span class="token string">state rule context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
					'<span class="token string">number context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">property</span>': reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
					'<span class="token string">text context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">property</span>': reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
					'<span class="token string">file context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">property</span>': reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
					'<span class="token string">command context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">command</span>': reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
					'<span class="token string">action context</span>': component <a href="#grammar-rule--model-context">'model context'</a>
					'<span class="token string">property path</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
					'<span class="token string">action</span>': reference
					'<span class="token string">can use containing view</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">use</span> <span class="token operator">containing</span> <span class="token operator">view</span> ] }
					)
					'<span class="token string">view bindings</span>': dictionary {
						'<span class="token string">window</span>': [ <span class="token operator">:</span> <span class="token operator">open</span> <span class="token operator">view</span> <span class="token operator">@</span> ] reference
						'<span class="token string">using views</span>': stategroup (
							'<span class="token string">internal</span>' { }
							'<span class="token string">external</span>' { [ <span class="token operator">from</span> ]
								'<span class="token string">views</span>': reference
							}
						)
						'<span class="token string">view</span>': [ <span class="token operator">:</span> ] reference
						'<span class="token string">can open entry</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' {
								'<span class="token string">window</span>': [ <span class="token operator">and</span> <span class="token operator">open</span> <span class="token operator">view</span> <span class="token operator">@</span> ] reference
								'<span class="token string">using views</span>': stategroup (
									'<span class="token string">internal</span>' { }
									'<span class="token string">external</span>' { [ <span class="token operator">from</span> ]
										'<span class="token string">views</span>': reference
									}
								)
								'<span class="token string">view</span>': [ <span class="token operator">:</span> ] reference
							}
						)
					}
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">query number</span>' {
					'<span class="token string">number</span>': [ <span class="token operator">query</span> <span class="token operator">number</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">query text</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">query</span> <span class="token operator">text</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">query file</span>' {
					'<span class="token string">file</span>': [ <span class="token operator">query</span> <span class="token operator">file</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">query stategroup</span>' {
					'<span class="token string">stategroup</span>': [ <span class="token operator">query</span> <span class="token operator">stategroup</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">report</span>' {
					'<span class="token string">report</span>': [ <span class="token operator">report</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">report text parameter</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">report</span> <span class="token operator">text</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
				'<span class="token string">report number parameter</span>' {
					'<span class="token string">number</span>': [ <span class="token operator">report</span> <span class="token operator">number</span> ] reference
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--gui-widget-configuration-node">'gui widget configuration node'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--gui-widget-configuration-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui widget configuration node</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	'<span class="token string">configuration</span>': dictionary {
		'<span class="token string">attribute</span>': component <a href="#grammar-rule--gui-widget-configuration-attribute">'gui widget configuration attribute'</a>
	}
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
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">reference rule</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
					'<span class="token string">rule</span>': [ <span class="token operator">$</span> ] reference
				}
				'<span class="token string">state rule</span>' {
					'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-path">'singular path'</a>
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
				'<span class="token string">optional reference</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">~></span> ] reference
				}
				'<span class="token string">collection entry</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">entry key</span>': text
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-path">'conditional path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--model-binding-property-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">model binding property path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">state group</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--model-binding-property-path">'model binding property path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--query-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">query path step</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--query-path-step">'query path step'</a>
		}
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
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--query-path-step">'query path step'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--query-path">'query path'</a>
		}
	)
}
</pre>
</div>
</div>
