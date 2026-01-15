---
layout: "doc"
origin: "webclient"
language: "widget"
version: "partitions.1"
type: "grammar"
---

1. TOC
{:toc}

## Widgets
---

Widgets are used to initialize and compose controls and bind data to them using
the [client bindings](../client bindings/client_bindings.html). Widgets in turn
are used by [views](../views/grammar.html) which manage the binding to the
application model.

A widget can be seen as two parts. First its [configuration](#configuration),
and second its implementation. The widget configuration describes an interface
for others that make use of widgets (i.e. views).

The implementation part of a widget determines what gets rendered using one or
more controls. The implementation binds data from the client state or the widget
configuration to the controls. Binding in this case means that the controls are
updated whenever the source data changes. Selecting controls and binding data is
done by using [expressions](#grammar-rule--expression).


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">dependencies</span>': dictionary { [ <span class="token operator">using</span> ] }
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">binding context</span>': [ <span class="token operator">binds:</span> ] stategroup (
	'<span class="token string">none</span>' { [ <span class="token operator">unbound</span> ] }
	'<span class="token string">select</span>' {
		'<span class="token string">binding</span>': reference
		'<span class="token string">switch client binding context</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">on</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
				'<span class="token string">constrained on containing binding</span>': stategroup (
					'<span class="token string">yes</span>' {
						'<span class="token string">type path</span>': component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
						'<span class="token string">instance binding</span>': reference
					}
					'<span class="token string">no</span>' { [ <span class="token operator">unconstrained</span> ]
						'<span class="token string">instance binding</span>': reference
					}
				)
			}
			'<span class="token string">no</span>' { }
		)
	}
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration">'widget configuration'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">define variable</span>': stategroup (
	'<span class="token string">yes</span>' {
		'<span class="token string">variable</span>': component <a href="#grammar-rule--variable">'variable'</a>
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression</span>': [ <span class="token operator">render:</span> ] component <a href="#grammar-rule--expression">'expression'</a>
</pre>
</div>
</div>
### Configuration
---

The configuration part of a widget consist of attributes of the types: `widget`,
`window`, `view`, `binding`, `number`, `text`, `list` and `stategroup`.

Some attributes are optional if a default is set. For example text attributes
can have a default set.

```js
'language': text default: "English"
```

#### Text, number, list and stategroup

Attributes of this type are used to configure the behaviour and state of the
widget. These values can be updated using expressions when invoked from an
event.

#### Binding

A binding attribute references a binding type in the `client bindings`. It can
be used to access data from the client state. When an attribute of this type is
used in a view, it typically needs some additional model information like
property name.

#### Widgets

A widget attribute references another widget definition. They can be used in
expressions to bind to a markup attribute of a control or to invoke in an
expression at the top level of the widget implementation.

#### Views and windows

Views are shown in a `window`. A window is a fixed place in the user interface
where zero or more views can be rendered. A webclient project needs at least one
window and one view to properly function.

For widgets, view attributes are used to open new content. E.g. opening a new
view when the user clicks on a link or a row in a table.

{: #grammar-rule--widget-configuration }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget configuration</span>' {
	'<span class="token string">switch client binding context</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">on</span> ]
			'<span class="token string">constrained on containing binding</span>': stategroup (
				'<span class="token string">yes</span>' { }
				'<span class="token string">no</span>' { [ <span class="token operator">unconstrained</span> ]
					'<span class="token string">instance binding</span>': reference
				}
			)
			'<span class="token string">type path</span>': component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">widget</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">anonymous</span>' { [ <span class="token operator">widget</span> ] }
				'<span class="token string">typed</span>' {
					'<span class="token string">type</span>': [ <span class="token operator">widget:</span> ] stategroup (
						'<span class="token string">self</span>' { [ <span class="token operator">self</span> ] }
						'<span class="token string">external</span>' {
							'<span class="token string">widget</span>': reference
						}
					)
				}
			)
		}
		'<span class="token string">window</span>' { [ <span class="token operator">window</span> ]
			'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration">'widget configuration'</a>
		}
		'<span class="token string">view</span>' { [ <span class="token operator">view</span> ] }
		'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] dynamic-order
			'<span class="token string">persistence</span>': component <a href="#grammar-rule--configuration-attribute-persistence">'configuration attribute persistence'</a>
			'<span class="token string">has default</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">default:</span> ]
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] dynamic-order
			'<span class="token string">has default</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">default:</span> ]
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">static</span>' {
							'<span class="token string">value</span>': text
						}
						'<span class="token string">phrase</span>' {
							'<span class="token string">phrase</span>': reference
						}
						'<span class="token string">unique id</span>' { [ <span class="token operator">unique-id</span> ] }
					)
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">persistence</span>': component <a href="#grammar-rule--configuration-attribute-persistence">'configuration attribute persistence'</a>
		}
		'<span class="token string">list</span>' { [ <span class="token operator">list</span> ]
			'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration">'widget configuration'</a>
		}
		'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ] dynamic-order
			'<span class="token string">has default</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">default:</span> ]
					'<span class="token string">state</span>': reference
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">persistence</span>': component <a href="#grammar-rule--configuration-attribute-persistence">'configuration attribute persistence'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration">'widget configuration'</a>
			}
		}
		'<span class="token string">binding</span>' { [ <span class="token operator">binding</span> ]
			'<span class="token string">constrained on containing binding</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">type path</span>': component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
					'<span class="token string">instance binding</span>': reference
				}
				'<span class="token string">no</span>' { [ <span class="token operator">unconstrained</span> ]
					'<span class="token string">instance binding</span>': reference
				}
			)
			'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration">'widget configuration'</a>
		}
		'<span class="token string">node</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
			'<span class="token string">attributes</span>': dictionary {
				'<span class="token string">mutable</span>': [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">inherit</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">mutable</span> ] }
				)
				'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration">'widget configuration'</a>
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--client-binding-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">client binding type path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">binding</span>' {
					'<span class="token string">instance binding</span>': [ <span class="token operator">/</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--client-binding-type-path">'client binding type path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--configuration-attribute-persistence }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">configuration attribute persistence</span>' {
	'<span class="token string">persist</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">@persist</span> ]
			'<span class="token string">per session</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">session</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">per entry</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">entry</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">no</span>' { }
	)
}
// TODO update documentation
</pre>
</div>
</div>
### Expressions
---

Expressions are used to yield a value. At the top level of the widget
implementation it is used to select a control. The most simple variant of an
expression is.

```js
control 'empty' ( )
```

The above snippet initializes a new control called 'empty' and renders nothing.

Expressions are also used to bind data to control properties.

```js
'text' = $ .'text' value
```

#### Context in expressions

Widget expressions use a so called context to get their data from or to execute
instructions.

At the start of the widget, the context is set to the binding context of the
node and the root widget configuration. The binding context refers to a binding
in the [client bindings](../client bindings/client_bindings.html).

This is best explained using the following example.

```js
binds: 'node' {
	'text': binding 'text' {
		'empty label': text
	}
} as $

render: switch $ .'text'[ .'is set'] (
	|'no' as $ => control 'text' (
		'text' = $ .'empty label' value
	)
	|'yes' as $'text value' => control 'text' (
		'text' = $'text value'[ .'text']
	)
)
```

The widget is configured to start at the `node` binding. It has one binding
attribute called `text`. That attribute has one sub attribute `empty label`.

The widget expression starts with a `switch` to check if the text property is
set or not. First the `text` attribute is selected using the double colon
keyword (`::`). This does two things. First it set the widget configuration
context to the node containing the `empty label` attribute. Second it switches
the client binding context from `node` to `text` since it is a binding
attribute.

Then the `is set` property is selected. The `is set` property is a member of the
`text` binding from the client bindings. The two cases of the switch are
handled. In the `no` case the context is assigned to the anonymous variable
`$`. This does not change the configuration context, but does change the client
binding context to `'text'.'is set'?'no'`. The `yes` case defines a names scope
`$'text value'`. It is used to get the `text` value from.

To summarize. There are two scopes:
- **anonymous**: When the scope is defined using a variable `as $`.
- **named**: When the scope variable gets a name `as $'variable name'`.

> **Pro Tip!** Use variable names when widgets get more complex and mix
> different scopes.

{: #grammar-rule--expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">node switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--conditional-context-selection">'conditional context selection'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { dynamic-order
				'<span class="token string">node</span>': group { [ <span class="token operator">|</span> <span class="token operator">node</span> ]
					'<span class="token string">variable</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
				}
				'<span class="token string">none</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
			}
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">configuration</span>' {
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
						'<span class="token string">next</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
					}
				}
				'<span class="token string">binding</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">[</span> <span class="token operator">.</span>, <span class="token operator">]</span> ] reference
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
						'<span class="token string">next</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
					}
				}
			)
		}
		'<span class="token string">value switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--scalar">'scalar'</a>
			'<span class="token string">compare to</span>': [ <span class="token operator">compare</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--scalar">'scalar'</a>
			'<span class="token string">last case</span>': reference = last
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary (
				static '<span class="token string">equals</span>' [ <span class="token operator">==</span> ]
				static '<span class="token string">not equal</span>' [ <span class="token operator">!=</span> ]
				static '<span class="token string">greater than</span>' [ <span class="token operator">></span> ]
				static '<span class="token string">greater than or equals</span>' [ <span class="token operator">>=</span> ]
				static '<span class="token string">less than</span>' [ <span class="token operator"><</span> ]
				static '<span class="token string">less than or equals</span>' [ <span class="token operator"><=</span> ]
			) { [ <span class="token operator">|</span> ]
				'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">case</span>' = predecessor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
			}
		}
		'<span class="token string">set switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">configuration</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">widget binding</span>' {
					'<span class="token string">collection property</span>': [ <span class="token operator">[</span> <span class="token operator">.</span>, <span class="token operator">]</span> ] reference
				}
			)
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { dynamic-order
				'<span class="token string">none</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
				'<span class="token string">match node</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">|</span> <span class="token operator">node</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
						'<span class="token string">next</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
					}
				)
				'<span class="token string">nodes</span>': group { [ <span class="token operator">|</span> <span class="token operator">nodes</span> ]
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
					'<span class="token string">next</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
				}
			}
		}
		'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">configuration</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">widget binding</span>' {
					'<span class="token string">collection property</span>': [ <span class="token operator">[</span> <span class="token operator">.</span>, <span class="token operator">*</span> <span class="token operator">]</span> ] reference
					'<span class="token string">sort</span>': stategroup (
						'<span class="token string">yes</span>' { [ <span class="token operator">sort</span> <span class="token operator">by</span> ]
							'<span class="token string">by</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
						}
						'<span class="token string">no</span>' { }
					)
				}
			)
			'<span class="token string">variable</span>': component <a href="#grammar-rule--variable">'variable'</a>
			'<span class="token string">entry expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
		}
		'<span class="token string">target</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression-target">'expression target'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--expression-target }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression target</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">control</span>' {
			'<span class="token string">control binding</span>': component <a href="#grammar-rule--control-binding">'control binding'</a>
		}
		'<span class="token string">converter</span>' { [ <span class="token operator">converter</span> ]
			'<span class="token string">control</span>': component <a href="#grammar-rule--static-control">'static control'</a>
		}
		'<span class="token string">create entry</span>' {
			'<span class="token string">for</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': reference
				}
				'<span class="token string">node</span>' { }
			)
			'<span class="token string">target</span>': stategroup (
				'<span class="token string">node</span>' {
					'<span class="token string">node</span>': component <a href="#grammar-rule--node-binding">'node binding'</a>
				}
				'<span class="token string">widget configuration</span>' {
					'<span class="token string">configuration</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--expression-target">'expression target'</a>
				}
			)
		}
		'<span class="token string">widget configuration</span>' {
			'<span class="token string">context</span>': stategroup (
				'<span class="token string">instance</span>' {
					'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
				}
				'<span class="token string">type</span>' { [ <span class="token operator">%</span> ]
					'<span class="token string">select</span>': stategroup (
						'<span class="token string">current</span>' { }
						'<span class="token string">attribute</span>' {
							'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
						}
					)
				}
			)
			'<span class="token string">assign</span>': stategroup (
				'<span class="token string">binding</span>' { [ <span class="token operator">as</span> <span class="token operator">binding</span> ]
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--expression-target">'expression target'</a>
				}
				'<span class="token string">widget</span>' { [ <span class="token operator">as</span> <span class="token operator">widget</span> ] }
				'<span class="token string">plain</span>' { [ <span class="token operator">;</span> ] }
			)
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
		'<span class="token string">instruction</span>' {
			'<span class="token string">instruction</span>': component <a href="#grammar-rule--instruction-selection">'instruction selection'</a>
		}
		'<span class="token string">sort collection</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">direction</span>': stategroup (
				'<span class="token string">ascending</span>' { [ <span class="token operator">ascending</span> ] }
				'<span class="token string">descending</span>' { [ <span class="token operator">descending</span> ] }
			)
		}
		'<span class="token string">scalar</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--scalar">'scalar'</a>
		}
		'<span class="token string">let declaration</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--context-ancestor-path">'context ancestor path'</a>
			'<span class="token string">declaration</span>': [ <span class="token operator">$</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression list</span>' {
	'<span class="token string">optional context definition</span>': component <a href="#grammar-rule--optional-context-definition">'optional context definition'</a>
	'<span class="token string">expression</span>': component <a href="#grammar-rule--expression">'expression'</a>
	'<span class="token string">has next</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">next</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--expression-list">'expression list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--one-or-more-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">one or more expression</span>' {
	'<span class="token string">multiplicity</span>': stategroup (
		'<span class="token string">singular</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">plural</span>' {
			'<span class="token string">expression</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--expression-list">'expression list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-binding }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node binding</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">attributes</span>': dictionary {
		'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--static-control }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">static control</span>' {
	'<span class="token string">library</span>': stategroup (
		'<span class="token string">additional</span>' {
			'<span class="token string">control</span>': reference external
		}
		'<span class="token string">default</span>' {
			'<span class="token string">control</span>': reference
		}
	)
	'<span class="token string">node binding</span>': component <a href="#grammar-rule--node-binding">'node binding'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--control-binding }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">control binding</span>' {
	'<span class="token string">binding type</span>': stategroup (
		'<span class="token string">static</span>' {
			'<span class="token string">control</span>': [ <span class="token operator">control</span> ] component <a href="#grammar-rule--static-control">'static control'</a>
		}
		'<span class="token string">window</span>' { [ <span class="token operator">window</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">variable</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--variable">'variable'</a>
			'<span class="token string">control binding</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--control-binding">'control binding'</a>
		}
		'<span class="token string">widget</span>' {
			'<span class="token string">source</span>': stategroup (
				'<span class="token string">configuration</span>' {
					'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
					'<span class="token string">override</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">override</span> ]
							'<span class="token string">attributes</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
								'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
							}
						}
					)
				}
				'<span class="token string">inline</span>' {
					'<span class="token string">context</span>': component <a href="#grammar-rule--optional-context-selection">'optional context selection'</a>
					'<span class="token string">type</span>': [ <span class="token operator">widget</span> ] stategroup (
						'<span class="token string">self</span>' { [ <span class="token operator">self</span> ] }
						'<span class="token string">external</span>' {
							'<span class="token string">widget</span>': reference
						}
					)
					'<span class="token string">configuration</span>': component <a href="#grammar-rule--widget-configuration-binding">'widget configuration binding'</a>
				}
			)
		}
		'<span class="token string">client binding widget</span>' {
			'<span class="token string">context</span>': [ <span class="token operator">binding</span> <span class="token operator">widget</span> ] component <a href="#grammar-rule--context-selection">'context selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--widget-configuration-binding }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget configuration binding</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--scalar }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">scalar</span>' {
	'<span class="token string">binding type</span>': stategroup (
		'<span class="token string">static text</span>' {
			'<span class="token string">text</span>': text
		}
		'<span class="token string">phrase</span>' {
			'<span class="token string">phrase</span>': reference
		}
		'<span class="token string">configuration</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">text</span>' { [ <span class="token operator">value</span> ] }
				'<span class="token string">number</span>' { [ <span class="token operator">#</span> <span class="token operator">value</span> ] }
			)
		}
		'<span class="token string">event</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">text</span>' { [ <span class="token operator">argument</span> ] }
				'<span class="token string">number</span>' { [ <span class="token operator">#</span> <span class="token operator">argument</span> ] }
			)
		}
		'<span class="token string">binding</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">key</span>' { [ <span class="token operator">.key</span> ] }
				'<span class="token string">property</span>' { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">text</span>' { [ <span class="token operator">.</span> ] }
						'<span class="token string">reference</span>' { [ <span class="token operator">></span> ] }
						'<span class="token string">number</span>' { [ <span class="token operator">#</span> ] }
					)
					'<span class="token string">property</span>': reference
				}
			)
		}
		'<span class="token string">static number</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">unary expression</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">absolute value</span>' { [ <span class="token operator">abs</span> ] }
				'<span class="token string">sign inversion</span>' { [ <span class="token operator">-</span> ] }
			)
			'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--scalar">'scalar'</a>
		}
		'<span class="token string">list expression</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
				'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
			)
			'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
		}
		'<span class="token string">current time</span>' { [ <span class="token operator">current</span> <span class="token operator">time</span> ]
			'<span class="token string">throttle</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">interval</span>': [ <span class="token operator">interval:</span> ] integer
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">list index</span>' {
			'<span class="token string">context</span>': [, <span class="token operator">index</span> ] component <a href="#grammar-rule--context-selection">'context selection'</a>
		}
		'<span class="token string">let declaration</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--context-ancestor-path">'context ancestor path'</a>
			'<span class="token string">declaration</span>': [ <span class="token operator">$</span>, <span class="token operator">;</span> ] reference
		}
	)
	'<span class="token string">transform</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">transform</span> ]
			'<span class="token string">transformer</span>': reference
		}
	)
	'<span class="token string">format</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">format</span> ]
			'<span class="token string">formatter</span>': reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--instruction-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">instruction selection</span>' {
	'<span class="token string">action</span>': stategroup (
		'<span class="token string">execute instruction</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">instruction</span>': [ <span class="token operator">>></span> ] reference
			'<span class="token string">has arguments</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' {
					'<span class="token string">first argument</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--instruction-argument">'instruction argument'</a>
				}
			)
		}
		'<span class="token string">update configuration</span>' { [ <span class="token operator">set</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
			'<span class="token string">instruction</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--widget-configuration-binding">'widget configuration binding'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--instruction-argument }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">instruction argument</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
		}
		'<span class="token string">file</span>' { [ <span class="token operator">file</span> ] }
		'<span class="token string">view</span>' { [ <span class="token operator">view</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
		}
	)
	'<span class="token string">next argument</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">exists</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">argument</span>': component <a href="#grammar-rule--instruction-argument">'instruction argument'</a>
		}
	)
}
</pre>
</div>
</div>
### Let declarations

{: #grammar-rule--let-declarations }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">let declarations</span>' {
	'<span class="token string">let declarations</span>': dictionary { [ <span class="token operator">let</span> <span class="token operator">$</span> ]
		'<span class="token string">target</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">control</span>' { }
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> <span class="token operator">=</span> ] }
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> <span class="token operator">=</span> ] }
			'<span class="token string">control property</span>' {
				'<span class="token string">library</span>': stategroup (
					'<span class="token string">additional</span>' {
						'<span class="token string">control</span>': [ <span class="token operator">control</span> ] reference external
					}
					'<span class="token string">default</span>' {
						'<span class="token string">control</span>': [ <span class="token operator">control</span> ] reference
					}
				)
				'<span class="token string">type path</span>': [, <span class="token operator">=</span> ] component <a href="#grammar-rule--control-type-path">'control type path'</a>
			}
			'<span class="token string">widget property</span>' {
				'<span class="token string">type</span>': [ <span class="token operator">widget</span> ] stategroup (
					'<span class="token string">self</span>' { [ <span class="token operator">self</span> ] }
					'<span class="token string">external</span>' {
						'<span class="token string">widget</span>': reference
					}
				)
				'<span class="token string">type path</span>': [, <span class="token operator">=</span> ] component <a href="#grammar-rule--widget-type-path">'widget type path'</a>
			}
			'<span class="token string">instruction</span>' { [ <span class="token operator">instruction</span> <span class="token operator">=</span> ] }
		)
		'<span class="token string">expression</span>': component <a href="#grammar-rule--one-or-more-expression">'one or more expression'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--control-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">control type path</span>' {
	'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' {
					'<span class="token string">path</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--control-type-path">'control type path'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">path</span>': component <a href="#grammar-rule--control-type-path">'control type path'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--widget-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">widget type path</span>' {
	'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' {
					'<span class="token string">path</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--widget-type-path">'widget type path'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">path</span>': component <a href="#grammar-rule--widget-type-path">'widget type path'</a>
				}
				'<span class="token string">binding</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--widget-type-path">'widget type path'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>
### Variables

{: #grammar-rule--variable }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">current</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--context-selection-path">'context selection path'</a>
		}
		'<span class="token string">other context</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
		}
	)
	'<span class="token string">identifier</span>': [ <span class="token operator">as</span> <span class="token operator">$</span> ] stategroup (
		'<span class="token string">anonymous</span>' { }
		'<span class="token string">named</span>' {
			'<span class="token string">named values</span>': dictionary {
				'<span class="token string">has successor</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { }
					| none = '<span class="token string">no</span>'
				)
			}
			'<span class="token string">name</span>': reference = first
		}
	)
	'<span class="token string">let declarations</span>': component <a href="#grammar-rule--let-declarations">'let declarations'</a>
	'<span class="token string">more variables</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">variable</span>': component <a href="#grammar-rule--variable">'variable'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--optional-context-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional context definition</span>' {
	'<span class="token string">define context</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">variable</span>': [ <span class="token operator">define</span> <span class="token operator">context</span>, <span class="token operator">=></span> ] component <a href="#grammar-rule--variable">'variable'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable assignment</span>' {
	'<span class="token string">assign</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">variable</span>': component <a href="#grammar-rule--variable">'variable'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
### Navigation

{: #grammar-rule--context-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context selection</span>' {
	'<span class="token string">change context to</span>': stategroup (
		'<span class="token string">engine state</span>' { [ <span class="token operator">engine</span> ]
			'<span class="token string">engine state binding</span>': reference
		}
		'<span class="token string">other context</span>' {
			'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--context-ancestor-path">'context ancestor path'</a>
		}
	)
	'<span class="token string">path</span>': component <a href="#grammar-rule--context-selection-path">'context selection path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--context-ancestor-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context ancestor path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">context</span>': stategroup (
				'<span class="token string">anonymous</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">named</span>' {
					'<span class="token string">variable name</span>': [ <span class="token operator">$</span> ] reference
				}
			)
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--context-ancestor-path">'context ancestor path'</a>
		}
		'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--context-selection-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context selection path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': stategroup (
				'<span class="token string">attribute</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">client binding</span>' {
					'<span class="token string">binding</span>': [ <span class="token operator">/</span> ] reference
				}
				'<span class="token string">client binding reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--context-selection-path">'context selection path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--optional-context-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional context selection</span>' {
	'<span class="token string">change context</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--context-selection">'context selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-context-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional context selection</span>' {
	'<span class="token string">change context to</span>': stategroup (
		'<span class="token string">engine state</span>' { [ <span class="token operator">engine</span> ]
			'<span class="token string">engine state binding</span>': reference
		}
		'<span class="token string">other context</span>' {
			'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--context-ancestor-path">'context ancestor path'</a>
		}
	)
	'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-context-selection-path">'conditional context selection path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-context-selection-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional context selection path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">attribute</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">list entry</span>' {
					'<span class="token string">index</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--scalar">'scalar'</a>
				}
				'<span class="token string">widget configuration state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">client binding</span>' {
					'<span class="token string">binding</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--client-binding-context-selection">'client binding context selection'</a>
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-context-selection-path">'conditional context selection path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--client-binding-context-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">client binding context selection</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">binding</span>' {
			'<span class="token string">binding</span>': [ <span class="token operator">/</span> ] reference
		}
		'<span class="token string">collection entry</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--scalar">'scalar'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">reference</span>' {
			'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
		}
	)
	'<span class="token string">has next</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">next</span>': component <a href="#grammar-rule--client-binding-context-selection">'client binding context selection'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
