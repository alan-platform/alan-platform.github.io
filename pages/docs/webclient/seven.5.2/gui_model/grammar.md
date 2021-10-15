---
layout: doc
origin: webclient
language: gui_model
version: seven.5.2
type: grammar
---

1. TOC
{:toc}


{: #grammar-rule--has-user-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has user node</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">users</span> ]
		'<span class="token string">context</span>': component <a href="#grammar-rule--gui-static-conditional-path">'gui static conditional path'</a>
		'<span class="token string">users</span>': [ <span class="token operator">.</span> ] reference
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

{: #grammar-rule--root }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': [ <span class="token operator">root</span> ] component <a href="#grammar-rule--gui-node">'gui node'</a>
</pre>
</div>
</div>

{: #grammar-rule--numerical-types }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">numerical types</span>': [ <span class="token operator">numerical</span> <span class="token operator">types</span> ] dictionary {
	'<span class="token string">representation type</span>': [ <span class="token operator">{</span>, <span class="token operator">}</span> ] stategroup (
		'<span class="token string">model</span>' { }
		'<span class="token string">date</span>' { [ <span class="token operator">date</span> ] }
		'<span class="token string">date and time</span>' { [ <span class="token operator">date-time</span> ] }
		'<span class="token string">HTML date and time</span>' { [ <span class="token operator">HTML</span> <span class="token operator">html-time</span> ] }
		'<span class="token string">duration</span>' { [ <span class="token operator">duration:</span> ]
			'<span class="token string">unit</span>': stategroup (
				'<span class="token string">seconds</span>' { [ <span class="token operator">seconds</span> ] }
				'<span class="token string">minutes</span>' { [ <span class="token operator">minutes</span> ] }
				'<span class="token string">hours</span>' { [ <span class="token operator">hours</span> ] }
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--duplication-node-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">duplication node mapping</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">-></span> ] stategroup (
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ] }
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">mapping</span>': component <a href="#grammar-rule--duplication-node-mapping">'duplication node mapping'</a>
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">mapping</span>': component <a href="#grammar-rule--duplication-node-mapping">'duplication node mapping'</a>
				}
			}
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ] }
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--gui-static-singular-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui static singular path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--gui-static-singular-path">'gui static singular path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--gui-static-conditional-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui static conditional path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--gui-static-conditional-path">'gui static conditional path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--file-name-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">file name expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">&</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">text</span>': text
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--gui-static-singular-path">'gui static singular path'</a>
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">text</span>' { [ <span class="token operator">:</span> ]
							'<span class="token string">text</span>': reference
						}
						'<span class="token string">number</span>' { [ <span class="token operator">#</span> ]
							'<span class="token string">number</span>': reference
						}
						'<span class="token string">state group</span>' { [ <span class="token operator">?</span> ]
							'<span class="token string">state group</span>': reference
							'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
								'<span class="token string">state file name expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--file-name-expression">'file name expression'</a>
							}
						}
					)
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--file-name-expression">'file name expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-validation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text validation</span>' {
	'<span class="token string">regular expression</span>': text
}
</pre>
</div>
</div>

{: #grammar-rule--number-limit }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number limit</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">static</span>' {
			'<span class="token string">limit</span>': integer
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">base</span>': stategroup (
				'<span class="token string">today</span>' { [ <span class="token operator">today</span> ] }
				'<span class="token string">now</span>' { [ <span class="token operator">now</span> ] }
			)
			'<span class="token string">with offset</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">offset</span>': integer
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--gui-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui node</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	'<span class="token string">attributes</span>': dictionary {
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">reference set</span>' { [ <span class="token operator">:</span> <span class="token operator">reference-set</span> ] }
			'<span class="token string">command</span>' { [ <span class="token operator">:</span> <span class="token operator">command</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">global</span>' {
						'<span class="token string">parameters</span>': component <a href="#grammar-rule--gui-node">'gui node'</a>
					}
					'<span class="token string">component</span>' { }
				)
			}
			'<span class="token string">action</span>' { [ <span class="token operator">:</span> <span class="token operator">action</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--gui-node">'gui node'</a>
				'<span class="token string">views</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
					'<span class="token string">view context</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--gui-node-type-path">'gui node type path'</a>
				}
				'<span class="token string">action</span>': component <a href="#grammar-rule--gui-action">'gui action'</a>
			}
			'<span class="token string">property</span>' { [ <span class="token operator">:</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">has ordered graphs</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">ordered-graphs:</span> ]
								'<span class="token string">ordered graphs</span>': dictionary { }
							}
						)
						'<span class="token string">node</span>': component <a href="#grammar-rule--gui-node">'gui node'</a>
						'<span class="token string">duplication mapping</span>': stategroup (
							'<span class="token string">none</span>' { }
							'<span class="token string">from current context</span>' { [ <span class="token operator">duplicate</span> <span class="token operator">with</span> ]
								'<span class="token string">mapping</span>': component <a href="#grammar-rule--duplication-node-mapping">'duplication node mapping'</a>
							}
						)
						'<span class="token string">default</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">default:</span> <span class="token operator">model</span> <span class="token operator">expression</span> ] }
						)
					}
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">gui node</span>': component <a href="#grammar-rule--gui-node">'gui node'</a>
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">numerical type</span>': reference
						'<span class="token string">default</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' {
								'<span class="token string">value</span>': stategroup (
									'<span class="token string">today</span>' { [ <span class="token operator">today</span> ] }
									'<span class="token string">now</span>' { [ <span class="token operator">now</span> ] }
									'<span class="token string">zero</span>' { [ <span class="token operator">zero</span> ] }
									'<span class="token string">one</span>' { [ <span class="token operator">one</span> ] }
									'<span class="token string">expression</span>' { [ <span class="token operator">model</span> <span class="token operator">expression</span> ] }
								)
							}
						)
						'<span class="token string">validation</span>': group {
							'<span class="token string">has minimum</span>': stategroup (
								'<span class="token string">no</span>' { }
								'<span class="token string">yes</span>' { [ <span class="token operator">min:</span> ]
									'<span class="token string">minimum</span>': component <a href="#grammar-rule--number-limit">'number limit'</a>
								}
								'<span class="token string">expression</span>' { [ <span class="token operator">min:</span> <span class="token operator">model</span> <span class="token operator">expression</span> ] }
							)
							'<span class="token string">has maximum</span>': stategroup (
								'<span class="token string">no</span>' { }
								'<span class="token string">yes</span>' { [ <span class="token operator">max:</span> ]
									'<span class="token string">maximum</span>': component <a href="#grammar-rule--number-limit">'number limit'</a>
								}
								'<span class="token string">expression</span>' { [ <span class="token operator">max:</span> <span class="token operator">model</span> <span class="token operator">expression</span> ] }
							)
						}
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">navigable</span>': stategroup (
							'<span class="token string">yes</span>' {
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">optional</span>' { [ <span class="token operator">~></span> ] }
									'<span class="token string">mandatory</span>' { [ <span class="token operator">-></span> ] }
								)
								'<span class="token string">referenced node</span>': component <a href="#grammar-rule--gui-node-type-path">'gui node type path'</a>
								'<span class="token string">rules</span>': dictionary { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
									'<span class="token string">referenced node</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--gui-node-type-path">'gui node type path'</a>
								}
							}
							'<span class="token string">no</span>' {
								'<span class="token string">password property</span>': stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">password</span> ] }
									'<span class="token string">no</span>' { }
								)
							}
						)
						'<span class="token string">has validation</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">validate:</span> ]
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">regular expression</span>' {
										'<span class="token string">rules</span>': component <a href="#grammar-rule--text-validation">'text validation'</a>
									}
									'<span class="token string">optional reference must resolve</span>' { [ <span class="token operator">resolvable</span> ] }
								)
							}
						)
						'<span class="token string">default</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">default:</span> ]
								'<span class="token string">source</span>': stategroup (
									'<span class="token string">guid</span>' { [ <span class="token operator">guid</span> ] }
									'<span class="token string">current user</span>' { [ <span class="token operator">user</span> ] }
									'<span class="token string">expression</span>' { [ <span class="token operator">model</span> <span class="token operator">expression</span> ] }
									'<span class="token string">auto select only candidate</span>' { [ <span class="token operator">only</span> <span class="token operator">candidate</span> ] }
								)
							}
						)
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">file name source</span>': stategroup (
							'<span class="token string">expression</span>' { }
							'<span class="token string">generated</span>' {
								'<span class="token string">file name expression</span>': [ <span class="token operator">name:</span> ] component <a href="#grammar-rule--file-name-expression">'file name expression'</a>
							}
						)
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">default</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' { [ <span class="token operator">default:</span> ]
								'<span class="token string">source</span>': stategroup (
									'<span class="token string">state</span>' {
										'<span class="token string">state</span>': reference
									}
									'<span class="token string">state switch</span>' { [ <span class="token operator">model</span> <span class="token operator">state-switch</span> ] }
								)
							}
						)
						'<span class="token string">has states</span>': stategroup = node-switch .'<span class="token string">states</span>' (
							| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
							| none  = '<span class="token string">no</span>'
						)
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">rules</span>': dictionary { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
								'<span class="token string">referenced node</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--gui-node-type-path">'gui node type path'</a>
							}
							'<span class="token string">gui node</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--gui-node">'gui node'</a>
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

{: #grammar-rule--ancestor-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
		}
	)
}
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
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">action</span>' {
					'<span class="token string">action</span>': [ <span class="token operator">action</span> ] reference
				}
				'<span class="token string">command</span>' {
					'<span class="token string">command</span>': [ <span class="token operator">command</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
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

{: #grammar-rule--gui-action-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui action expression</span>' {
	'<span class="token string">operation</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">state-switch</span> ]
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
			}
		}
		'<span class="token string">node switch</span>' { [ <span class="token operator">node-switch</span> ]
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
				'<span class="token string">true case</span>': [ <span class="token operator">|</span> <span class="token operator">nodes</span> ] group {
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
				}
				'<span class="token string">false case</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> ] group {
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
				}
			}
		}
		'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
			'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
		}
		'<span class="token string">ignore</span>' { [ <span class="token operator">ignore</span> ]
			/* target */
		}
		'<span class="token string">update properties</span>' { [ <span class="token operator">update</span> ]
			'<span class="token string">target</span>': stategroup (
				'<span class="token string">node</span>' {
					'<span class="token string">bind view</span>': reference
					'<span class="token string">expression</span>': component <a href="#grammar-rule--object-expression">'object expression'</a>
				}
				'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
				}
			)
		}
		'<span class="token string">execute operation</span>' { [ <span class="token operator">execute</span> ]
			'<span class="token string">bind view</span>': [ <span class="token operator">view</span> ] reference
			'<span class="token string">expression</span>': component <a href="#grammar-rule--object-expression">'object expression'</a>
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">command</span>' { [ <span class="token operator">command</span> ] }
				'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
					'<span class="token string">sub action</span>': [ <span class="token operator">{</span>, <span class="token operator">}</span> ] component <a href="#grammar-rule--gui-action">'gui action'</a>
				}
			)
		}
		'<span class="token string">produce value</span>' {
			'<span class="token string">value</span>': stategroup (
				'<span class="token string">object</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--object-expression">'object expression'</a>
				}
				'<span class="token string">state group</span>' { [ <span class="token operator">state</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--object-expression">'object expression'</a>
				}
				'<span class="token string">scalar</span>' { }
			)
		}
		'<span class="token string">entry list</span>' { [ <span class="token operator">list</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">entries</span>': component <a href="#grammar-rule--entry-expression-list">'entry expression list'</a>
		}
		'<span class="token string">entry</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">create</span>' { [ <span class="token operator">create</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--object-expression">'object expression'</a>
					'<span class="token string">collection type</span>': stategroup (
						'<span class="token string">parameter</span>' { }
						'<span class="token string">node</span>' {
							'<span class="token string">bind view</span>': reference
						}
					)
				}
				'<span class="token string">delete</span>' { [ <span class="token operator">delete</span> ]
					'<span class="token string">bind view</span>': reference
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--object-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object expression</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">default</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--entry-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entry expression list</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
	'<span class="token string">more entries</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--entry-expression-list">'entry expression list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--gui-action }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">gui action</span>' {
	'<span class="token string">expression</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--gui-action-expression">'gui action expression'</a>
	'<span class="token string">has next action</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">and</span> ]
			'<span class="token string">action</span>': component <a href="#grammar-rule--gui-action">'gui action'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
