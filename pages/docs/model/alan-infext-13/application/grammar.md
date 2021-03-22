---
layout: doc
origin: model
language: application
version: alan-infext-13
type: grammar
---

1. TOC
{:toc}

## The *minimal model*
---
Every valid Alan model instantiates the [`root` rule](#the-root-rule).
We can use that rule for extracting a minimal model.
For the `application` language, the minimal model is

> ```js
users
interfaces
root { }
numerical-types
```

Thus, every `application` model defines `users` for access control, `interfaces` specifying operations and data from external systems, a `root` type, and `numerical-types`.
The next section explains the minimal model in more detail.
## Data model structure
---
### The `root` rule
##### Application users
The language supports two classes of users: `anonymous` users and `dynamic` users.
Anonymous users do not require login; dynamic users do.

The keyword `anonymous` enables `anonymous` user access to your application.
If you do not plan to support anonymous users, you just leave it out: the `'no'` state for `'allow anonymous user'` is the default, requiring no code at all.

User authentication can either be application-specific, or it can be done via a separate module for single sign-on.
If you want user authentication to be application-specific, you need to specify which collection and text property holds (hashed) user passwords.
In addition, you have to specify states for the 'active' and 'reset' status of the password.

{: #grammar-rule--allow-anonymous-user }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">allow anonymous user</span>': @section [ <span class="token operator">users</span> ] stategroup (
	'<span class="token string">no</span>' { }
	'<span class="token string">yes</span>' { @block indent [ <span class="token operator">anonymous</span> ] }
)
</pre>
</div>
</div>

{: #grammar-rule--has-dynamic-users }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has dynamic users</span>': stategroup (
	'<span class="token string">no</span>' { }
	'<span class="token string">yes</span>' { @block indent
		'<span class="token string">context node path</span>': [ <span class="token operator">dynamic:</span> ] component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
		'<span class="token string">users collection</span>': [ <span class="token operator">.</span> ] reference
		'<span class="token string">supports user sign-up</span>': stategroup (
			'<span class="token string">yes</span>' { @block indent
				'<span class="token string">user initializer</span>': [ <span class="token operator">user-initializer:</span> ] component <a href="#grammar-rule--user-initializer">'user initializer'</a>
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">has password authentication</span>': stategroup (
			'<span class="token string">yes</span>' { @block indent
				'<span class="token string">password node</span>': [ <span class="token operator">password:</span> ] component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
				'<span class="token string">password collection</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">password property</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">password status</span>': @block [ <span class="token operator">password-status:</span> ] group {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">active state</span>': @block indent [ <span class="token operator">active:</span> ] group {
						'<span class="token string">state</span>': reference
						'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
					}
					'<span class="token string">reset state</span>': @block indent [ <span class="token operator">reset:</span> ] group {
						'<span class="token string">state</span>': reference
						'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
					}
				}
				'<span class="token string">password initializer</span>': @block [ <span class="token operator">password-initializer:</span> ] component <a href="#grammar-rule--password-initializer">'password initializer'</a>
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">has external authentication</span>': stategroup (
			'<span class="token string">yes</span>' { @block indent
				'<span class="token string">authorities node</span>': [ <span class="token operator">external-authentication:</span> ] component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
				'<span class="token string">authorities collection</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">identities node</span>': @block indent [ <span class="token operator">identities:</span> ] component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
				'<span class="token string">identities collection</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">user reference</span>': [ <span class="token operator">></span> ] reference
				'<span class="token string">identity initializer</span>': @block indent [ <span class="token operator">identity-initializer:</span> ] component <a href="#grammar-rule--identity-initializer">'identity initializer'</a>
			}
			'<span class="token string">no</span>' { }
		)
	}
)
</pre>
</div>
</div>
##### Interfaces
If your application consumes data from external sources, you will have defined an Alan `interface`.
In order to consume an `interface`, you mention it in a list of `interfaces`, so that you can reference the `interface` when configuring [permissions](#permissions-and-todos).
The `path` is a navigation path that produces a context node on which interface conformant data will be imported at runtime.
The `node type` specifying the context node, requires a permission definition to satisfy the modifier constraint: `can-update: interface '<imported interfaces id>'`.

{: #grammar-rule--imported-interfaces }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">imported interfaces</span>': @section [ <span class="token operator">interfaces</span> ] dictionary { @block indent
	'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--group-node-path">'group node path'</a> //'<span class="token string">singular node path tail</span>'
}
</pre>
</div>
</div>
##### The `root` node type
Alan models are hierarchical models specifying hierarchical data.
An Alan model is a hierarchy of nested types with a single root type:
> ```js
root { }
```

The `root` type (short for node type) is a complex type that nests other (complex) types. Types are surrounded by
curly braces, and their identification is a path which starts from the root type. We refer to
an instance of a type as a node. The rule for defining a type carries the same name: `node`; it should be read as the `node type` rule,
as we define `node types` in a model (for legacy reasons it is called the `'node'` rule).

{: #grammar-rule--root }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': @section [ <span class="token operator">root</span> ] component <a href="#grammar-rule--node">'node'</a>
</pre>
</div>
</div>
##### Numerical types
Numbers in an application model require a numerical type. Also, computations with numbers of different numerical types require conversion rules.
Divisions require a division conversion rule, products require a product conversion rule, and so on. Some examples of numerical types, with conversion rules are
> ```js
'date' in 'days' @date
'date and time' in 'seconds' @date-time
'days'
'milliseconds'
    = 'seconds' * 1 * 10 ^ 3 // rule for converting 'seconds' to milliseconds
    @factor: 10^ 3
    @label: "sec"
'minutes' @duration: minutes
'seconds'
    = 'seconds' * 'factor' // 'seconds' times a 'factor' produces 'seconds'
    = 'seconds' / 'factor'
    = 'milliseconds' * 1 * 10 ^ -3
    = 'minutes' * 60 * 10 ^ 0
    @duration: seconds
'factor'
    = 'factor' * 'factor'
    = 'seconds' / 'seconds'
```

Annotations like `@date` map numerical types to formats for easy modification in the GUI.
With `@factor` you can present 1000 milliseconds as 1 second to the application user.<br>
If you do so, be sure to set `@label:` to `"sec"` as well!

{: #grammar-rule--numerical-types }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">numerical types</span>': @section [ <span class="token operator">numerical-types</span> ] dictionary { @block indent
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">relative</span>' {
			'<span class="token string">timer resolution</span>': stategroup (
				'<span class="token string">none</span>' { }
				'<span class="token string">seconds</span>' { [ <span class="token operator">:</span> <span class="token operator">time-in-seconds</span> ] }
			)
			'<span class="token string">range type</span>': [ <span class="token operator">in</span> ] reference
		}
		'<span class="token string">absolute</span>' {
			'<span class="token string">product conversions</span>': dictionary { @block indent [ <span class="token operator">=</span> ]
				'<span class="token string">right</span>': [ <span class="token operator">*</span> ] reference
			}
			'<span class="token string">division conversions</span>': dictionary { @block indent [ <span class="token operator">=</span> ]
				'<span class="token string">denominator</span>': [ <span class="token operator">/</span>@trim-none ] reference
			}
		}
	)
	'<span class="token string">singular conversions</span>': dictionary { @block indent [ <span class="token operator">=</span> ]
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">factor</span>' {
				'<span class="token string">invert</span>': stategroup (
					'<span class="token string">no</span>' { [ <span class="token operator">*</span> ] }
					'<span class="token string">yes</span>' { [ <span class="token operator">/</span>@trim-none ] }
				)
				'<span class="token string">factor</span>': integer
				'<span class="token string">base</span>': [ <span class="token operator">*</span> ] integer
				'<span class="token string">exponent</span>': [ <span class="token operator">^</span> ] integer
			}
			'<span class="token string">base</span>' {
				'<span class="token string">offset</span>': [ <span class="token operator">+</span> ] integer
				'<span class="token string">base</span>': [ <span class="token operator">*</span> ] integer
				'<span class="token string">exponent</span>': [ <span class="token operator">^</span> ] integer
				'<span class="token string">unit conversion</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' {
						'<span class="token string">conversion rule</span>': [ <span class="token operator">in</span> ] reference
					}
				)
			}
		)
	}
	'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-numerical-type">'ui numerical type'</a>
}
</pre>
</div>
</div>
### Node types
Node types contain a `permissions definition` for controlling read and update permissions,
 a `todo definition` to mark a node as a `todo`-item,
 and `attributes`.
An attribute is of type `property`, `reference-set`, `command`, or `action`.

##### Property attributes
A `property` specifies a part of the data structure.
Alan supports six different property types:
`text`, `file`, `number` (with subtypes `integer` and `natural`), `collection`, `stategroup`, and `group`.

*Text*, *file*, and *number* are primitive property types. Text properties hold an unbounded
string value. File properties hold two unbounded string values: a file token and a file extension.
Integer number properties hold an integer value, and natural number properties hold an integer
value greater than zero.
For ensuring that number values have a predefined accuracy, Alan does not support number values with a fractional component.
For expressing the accuracy of a number, number properties reference a [`numerical type`](#numerical-types).

> ```js
'Name'        : text
'Price'       : number 'euro'
'Release Date': number positive 'date and time'
```

A *collection* property holds a map of key-value pairs. Keys are text values that have
to be unique such that we can reference them unambiguously.
A key field has to be specified explicitly, after the keyword `collection`; values are nodes of an inline defined type that specifies the key field:

> ```js
Customers : collection ['Customer ID'] {
    'Customer ID': text
    ... /* other attributes of this type */ ...
}
```

A *state group* property holds a value indicating a state. States are the alternatives to an aspect
that a state group property indicates. For example, `red`, `orange`, or `green` for a `color` property of a traffic light. The type of the property value corresponds to one out of multiple
predefined state types, such as `simple` or `assembled`:
> ```js
'Product Type': stategroup (
    'Simple' { ... /* attributes of this type */ ... }
    'Assembled' { ... /* attributes of this type */ ... }
)
```

A *group* property groups related property values, which is useful for presentational purposes:
> ```js
'Address': group {
    'City': text
    'State': text
    'Zip Code': text
}
```

___Derived values.___ Properties of the different types hold either *elementary* values or *derived* values (derivations).
*Derived* values are computed from elementary values and other derived values.
Application users cannot modify derived values.
Properties holding *derived* values require an expression for computing their values at runtime:
> ```js
'City': text                    // elementary value property
'copy of City': text = .'City' // derived value property with expression
```

The [derivations](#derivations) section provides the grammar for derivation expressions,
detailing the different computations that the language supports.

___Presentation options.___ The `ui` component properties reference [GUI annotation rules](#gui-annotations) for tweaking and tuning the behaviour and presentation of properties in the generated GUI.
Some examples of GUI annotations are
- `@hidden`: hides a derived property from the UI.
- `@description: "a description"`: describes the property in more detail to the user.
  Useful in combination with validation rules!
- `@validate: "[a-b]+"`: sets a regex for text properties that defines what values are acceptable.
- `@min:` and `@max:`: limits number values.
- `@identifying`: marks a property to always be displayed in addition to an collection entry's key.
- `@default: 'Assembled'`: specifies a default state for a state group property.
- `@default: today|now`: sets date or date-time number value to the current time.
- `@default: guid`: initializes a text property with a generated unique id string.
- `@small`: displays (small) collections inline, and includes them when pressing 'Duplicate'.
- `@multi-line`: presents a multi-line text area for a text property.

##### Reference set attributes
A `reference-set` is a special property that holds a set of inverse references created by reference [constraints](#constraints).
Derivation expressions use them for computations (e.g. [derived numbers](#derived-numbers)).

##### Command attributes
A `command` is a complex parametrized atomic operation on the dataset; a `command` is executed in a single transaction.
A `command` attribute on a `node type` consists of a `parameter definition` and an [implementation](#commands-and-timers).

{: #grammar-rule--node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ] indent
	'<span class="token string">permissions definition</span>': @list component <a href="#grammar-rule--node-permissions-definition">'node permissions definition'</a>
	'<span class="token string">todo definition</span>': component <a href="#grammar-rule--todo-definition">'todo definition'</a>
	'<span class="token string">has attributes</span>': stategroup = node-switch .'<span class="token string">attributes</span>' (
		| nodes = '<span class="token string">yes</span>' {
			'<span class="token string">first</span>' = first
			'<span class="token string">last</span>' = last
		}
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">attributes</span>': @raw dictionary { @block
		'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">attribute</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">attribute</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">reference set</span>' { [ <span class="token operator">:</span> <span class="token operator">reference-set</span> ]
				'<span class="token string">node type path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--node-type-id">'node type id'</a>
				'<span class="token string">value source</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">reference</span>' {
						'<span class="token string">reference</span>': [ <span class="token operator">inverse</span> ] component <a href="#grammar-rule--entry-reference-selector">'entry reference selector'</a>
					}
					'<span class="token string">union branch</span>' {
						'<span class="token string">branch</span>': [ <span class="token operator">from</span> ] reference
					}
				)
			}
			'<span class="token string">command</span>' { [ <span class="token operator">:</span> <span class="token operator">command</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">global</span>' {
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-command-attribute">'ui command attribute'</a>
					}
					'<span class="token string">component</span>' { [ <span class="token operator">component</span> ] }
				)
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
				'<span class="token string">permission definition</span>': component <a href="#grammar-rule--command-permission-definition">'command permission definition'</a>
				'<span class="token string">implementation</span>': stategroup (
					'<span class="token string">external</span>' { [ <span class="token operator">external</span> ] }
					'<span class="token string">internal</span>' {
						'<span class="token string">implementation</span>': component <a href="#grammar-rule--command">'command'</a>
					}
				)
			}
			'<span class="token string">action</span>' { [ <span class="token operator">:</span> <span class="token operator">action</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
				'<span class="token string">action</span>': component <a href="#grammar-rule--ui-action">'ui action'</a>
			}
			'<span class="token string">property</span>' { [ <span class="token operator">:</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ] }
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-group-property">'ui group property'</a>
						'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
					}
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' {
								'<span class="token string">graph constraints</span>': component <a href="#grammar-rule--graph-constraints-definition">'graph constraints definition'</a>
							}
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
								'<span class="token string">key constraint</span>': stategroup (
									'<span class="token string">no</span>' {
										'<span class="token string">branches</span>': [ <span class="token operator">flatten</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
											'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--flatten-expression">'flatten expression'</a>
										}
										'<span class="token string">separator</span>': [ <span class="token operator">join</span> ] stategroup (
											'<span class="token string">dot</span>' { [ <span class="token operator">.</span> ] }
											'<span class="token string">dash</span>' { [ <span class="token operator">-</span> ] }
											'<span class="token string">colon</span>' { [ <span class="token operator">:</span> ] }
											'<span class="token string">greater than</span>' { [ <span class="token operator">></span>@trim-none ] }
											'<span class="token string">space</span>' { [ <span class="token operator">space</span> ] }
										)
									}
									'<span class="token string">yes</span>' {
										'<span class="token string">expression</span>': component <a href="#grammar-rule--plural-reference-expression">'plural reference expression'</a>
									}
								)
							}
						)
						'<span class="token string">permissions</span>': component <a href="#grammar-rule--item-permissions-definition">'item permissions definition'</a>
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-collection-property">'ui collection property'</a>
						'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
					}
					'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
						'<span class="token string">set type</span>': stategroup (
							'<span class="token string">integer</span>' { }
							'<span class="token string">natural</span>' { [ <span class="token operator">positive</span> ] }
						)
						'<span class="token string">numerical type</span>': reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' {
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">causal</span>' {
										'<span class="token string">type</span>': stategroup (
											'<span class="token string">mutation</span>' { [ <span class="token operator">=</span> <span class="token operator">mutation-time</span> ]
												'<span class="token string">watched property</span>': [ <span class="token operator">.</span> ] reference
											}
											'<span class="token string">creation</span>' { [ <span class="token operator">=</span> <span class="token operator">creation-time</span> ] }
											'<span class="token string">destruction</span>' {
												'<span class="token string">destruction operation</span>': stategroup (
													'<span class="token string">set to lifetime</span>' { [ <span class="token operator">=</span> <span class="token operator">life-time</span> ] }
													'<span class="token string">add lifetime</span>' { [ <span class="token operator">add</span> <span class="token operator">life-time</span> ] }
													'<span class="token string">subtract lifetime</span>' { [ <span class="token operator">subtract</span> <span class="token operator">life-time</span> ] }
												)
												'<span class="token string">watched stategroup</span>': [ <span class="token operator">.</span> ] reference
												'<span class="token string">watched state</span>': [ <span class="token operator">?</span> ] reference
											}
										)
									}
									'<span class="token string">simple</span>' {
										'<span class="token string">metadata recording</span>': component <a href="#grammar-rule--metadata-recording">'metadata recording'</a>
									}
								)
							}
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' { [ <span class="token operator">parameter</span> ] }
									'<span class="token string">expression</span>' {
										'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
									}
								)
							}
						)
						'<span class="token string">behaviour</span>': stategroup (
							'<span class="token string">none</span>' { }
							'<span class="token string">timer</span>' { [ <span class="token operator">timer</span> <span class="token operator">ontimeout</span> ]
								'<span class="token string">implementation</span>': component <a href="#grammar-rule--command">'command'</a>
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-number-property">'ui number property'</a>
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' {
								'<span class="token string">metadata recording</span>': component <a href="#grammar-rule--metadata-recording">'metadata recording'</a>
							}
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' { [ <span class="token operator">parameter</span> ] }
									'<span class="token string">expression</span>' {
										'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
									}
								)
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-file-property">'ui file property'</a>
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">has reference</span>': stategroup (
							'<span class="token string">no</span>' { }
							'<span class="token string">yes</span>' {
								'<span class="token string">behaviour</span>': component <a href="#grammar-rule--reference-behaviour">'reference behaviour'</a>
								'<span class="token string">expression</span>': component <a href="#grammar-rule--entry-reference-definition">'entry reference definition'</a>
								'<span class="token string">rules</span>': indent dictionary { @block [ <span class="token operator">where</span> ]
									'<span class="token string">has successor</span>': stategroup = node-switch successor (
										| node = '<span class="token string">yes</span>' { '<span class="token string">rule</span>' = successor }
										| none = '<span class="token string">no</span>'
									)
									'<span class="token string">type</span>': stategroup (
										'<span class="token string">optional entry reference</span>' { [ <span class="token operator">~></span> ]
											'<span class="token string">expression</span>': component <a href="#grammar-rule--entry-reference-definition">'entry reference definition'</a>
										}
										'<span class="token string">node reference</span>' {
											'<span class="token string">behaviour</span>': component <a href="#grammar-rule--reference-behaviour">'reference behaviour'</a>
											'<span class="token string">path</span>': group {
												'<span class="token string">context</span>': stategroup (
													'<span class="token string">referenced node</span>' { [ <span class="token operator">$</span> ] }
													'<span class="token string">sibling rule</span>' {
														'<span class="token string">rule</span>': reference
													}
												)
												'<span class="token string">node path</span>': component <a href="#grammar-rule--object-path">'object path'</a>
											}
										}
									)
								}
							}
						)
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' {
								'<span class="token string">metadata recording</span>': component <a href="#grammar-rule--metadata-recording">'metadata recording'</a>
							}
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' {
										'<span class="token string">type</span>': stategroup (
											'<span class="token string">collection</span>' { [ <span class="token operator">key</span> ] }
											'<span class="token string">state group</span>' { [ <span class="token operator">parameter</span> ] }
										)
									}
									'<span class="token string">expression</span>' {
										'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
									}
								)
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-text-property">'ui text property'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
								'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-state-group-property">'ui state group property'</a>
						'<span class="token string">first state</span>': reference = first
						'<span class="token string">states</span>': @raw [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary @order: .'<span class="token string">view order</span>' { @block
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">record lifetime</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">life-time</span> ]
									'<span class="token string">meta property</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
									'<span class="token string">creation timestamp</span>': [ <span class="token operator">from</span> ] reference
								}
								'<span class="token string">no</span>' { }
							)
							'<span class="token string">rules</span>': @list indent dictionary { @block [ <span class="token operator">where</span> ]
								'<span class="token string">has successor</span>': stategroup = node-switch successor (
									| node = '<span class="token string">yes</span>' { '<span class="token string">rule</span>' = successor }
									| none = '<span class="token string">no</span>'
								)
								'<span class="token string">behaviour</span>': component <a href="#grammar-rule--reference-behaviour">'reference behaviour'</a>
								'<span class="token string">path</span>': group {
									'<span class="token string">context</span>': stategroup (
										'<span class="token string">this node</span>' {
											'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
										}
										'<span class="token string">sibling rule</span>' {
											'<span class="token string">rule</span>': reference
										}
									)
									'<span class="token string">node path</span>': component <a href="#grammar-rule--object-path">'object path'</a>
								}
							}
							'<span class="token string">permissions</span>': component <a href="#grammar-rule--item-permissions-definition">'item permissions definition'</a>
							'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-state">'ui state'</a>
							'<span class="token string">node</span>': @raw component <a href="#grammar-rule--node">'node'</a>
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
## Constraints & links
---
The `application` language supports two types of constraints on data: *reference constraints* and *graph constraints*.

___Reference constraints___ ensure that text properties hold a key value that uniquely identifies an item in a single specific `collection`.
This ensures that derived value computations and command invocations can safely use references.
In the GUI, reference constraints translate to a select list from which the application user has to choose an item.

Reference constraint expressions exist in two different flavours:
(1) `upstream` reference expressions that use earlier defined attributes and (2)
`downstream` reference expressions that freely use earlier and later defined attributes.

References can be unidirectional or bidirectional. For bidirectional references, you specify a reference-set:
> ```js
'Products': collection ['Name']
    'assembly': acyclic-graph
{
    'Name': text
      // reference-set holding Orders added by Product references:
    'Orders': reference-set -> .'Orders' = inverse >'Product'
}
'Orders': collection ['ID'] {
    'ID': text
      // a (bidirectional) upstream reference:
    'Product': text -> ^ .'Products'[] -<'Orders'
}
```

The expression `^ .'Products'` is a navigation expression that produces exactly one collection at runtime.
The Alan runtime interpretes such [navigation expressions](#navigation) as follows:
starting from the `Orders` node, go to the parent node (as expressed by the navigation step `^`);
then select the `Products` collection found on that node.
Thus, at runtime, navigation expressions are executed relative to the context node for which the expression should be evaluated.

___Graph constraints___ ensure termination for recursive computations traversing a graph.
Graph constraints constrain that a set of references (edges) together form a graph satisfying a specific property.
For example, an `acyclic-graph` constraint ensures that references that partake in the graph, form a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph).
For a detailed explanation, see [AlanLight](http://resolver.tudelft.nl/uuid:3eedbb63-29ea-4671-a016-4c037eec94cd).

The code sample below presents a graph constraint `assembly`.
`Product` references of `Parts` partake in the acyclic `assembly` graph on `Products`.
The constraint ensures that `Product Price` computations terminate:
> ```js
'Products': collection ['Name']
    'assembly': acyclic-graph
{
    'Name': text
    'Parts': collection ['Product'] {
         // an 'upstream' sibling reference that partakes in a graph:
        'Product': text -> ^ sibling in ('assembly') // reference to a 'Products' item in the assembly graph
        'Part Price': number 'euro' = >'Product'.'Product Price'
    }
    'Product Price': number 'euro' = sum .'Parts'* .'Part Price' // recursion!
}
```
---
Links mark relations between nodes that are not, or cannot be enforced by the runtime.
Similar to constraints, they also feature select lists in the generated GUI.

Links are especially useful when importing data from external systems via an Alan `interface`.
An Alan `application` requires that imports via an Alan `interface` always succeed.
Therefore, `application` data cannot put constraints on imported data; that is, unless the `interface` specifies them.
To exemplify this, suppose that order management application imports `Products` from a `Catalog Provider`.
As `Catalog Provider` can remove `Products` at any given time, we cannot put constraints on them.
`Orders` have to *link* to `Products` instead:
> ```js
'Catalog': group { can-update: interface 'Catalog Provider'
    'Products': collection ['Name'] {
        'Name': text
    }
}
'Orders': collection ['ID'] {
    'ID': text
     // a link to a 'Products' item from the catalog provider:
    'Product': text ~> ^ .'Catalog' .'Products'[]
}
```

{: #grammar-rule--entry-reference-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entry reference definition</span>' {
	'<span class="token string">evaluation</span>': component <a href="#grammar-rule--explicit-evaluation-annotation">'explicit evaluation annotation'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">simple</span>' {
			'<span class="token string">collection path</span>': [,'<span class="token string">[ ]</span>'] component <a href="#grammar-rule--object-path">'object path'</a>
		}
		'<span class="token string">sibling</span>' {
			'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
			'<span class="token string">graph participation</span>': [ <span class="token operator">sibling</span> ] stategroup (
				'<span class="token string">no</span>' {
					'<span class="token string">support self reference</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">||</span> <span class="token operator">self</span> ] }
					)
				}
				'<span class="token string">yes</span>' { [ <span class="token operator">in</span> ]
					'<span class="token string">graph</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] reference
				}
			)
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--descendant-object-path">'descendant object path'</a>
	'<span class="token string">inversion</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">-<</span> ]
			'<span class="token string">reference set</span>': reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--reference-behaviour }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference behaviour</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">mandatory</span>' { [ <span class="token operator">-></span> ] }
		'<span class="token string">optional</span>' { [ <span class="token operator">~></span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--graph-constraints-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">graph constraints definition</span>' {
	'<span class="token string">graphs</span>': dictionary { @block indent
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">acyclic</span>' { [ <span class="token operator">acyclic-graph</span> ] }
			'<span class="token string">ordered</span>' { [ <span class="token operator">ordered-graph</span> ]
				'<span class="token string">ordering property path</span>': group {
					'<span class="token string">path</span>': component <a href="#grammar-rule--group-node-path">'group node path'</a>
					'<span class="token string">ordering state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">ordering states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">sink state</span>': [ <span class="token operator">?</span> ] reference
						'<span class="token string">edge state</span>': [ <span class="token operator">||</span> <span class="token operator">?</span> ] reference
						'<span class="token string">edge reference</span>': [ <span class="token operator">></span> ] reference
					}
				}
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--explicit-evaluation-annotation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">explicit evaluation annotation</span>' {
	'<span class="token string">phase</span>': stategroup (
		'<span class="token string">upstream</span>' { }
		'<span class="token string">downstream</span>' { [ <span class="token operator">downstream</span> ] }
	)
	'<span class="token string">sibling navigation</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">graph traversal</span>': [ <span class="token operator">(</span> <span class="token operator">sibling</span>, <span class="token operator">)</span> ] stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">in</span> ]
					'<span class="token string">traversal type</span>': stategroup (
						'<span class="token string">base order</span>' { }
						'<span class="token string">inverse order</span>' { [ <span class="token operator">inverse</span> ] }
					)
					'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
					'<span class="token string">graph</span>': reference
				}
			)
		}
	)
}
</pre>
</div>
</div>
Node type identification path for reference sets.

{: #grammar-rule--node-type-id }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type id</span>' {
	'<span class="token string">steps</span>': component <a href="#grammar-rule--node-type-id-path">'node type id path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--node-type-id-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node type id path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">*</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-type-id-path">'node type id path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--entry-reference-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entry reference selector</span>' {
	'<span class="token string">definer</span>': stategroup (
		'<span class="token string">property</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">></span> ] reference
		}
		'<span class="token string">rule</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
		}
	)
}
</pre>
</div>
</div>
## Derivations
---
Derivation expressions use earlier defined properties for deriving values for ensuring terminating computations of derived values (derivations).
After a navigation step for following a reference, derivation expressions can use later defined properties as well.
Please note that some work remains to be done on the `application` language to fully ensure safe computations.
For more details on this, see [AlanLight](http://resolver.tudelft.nl/uuid:3eedbb63-29ea-4671-a016-4c037eec94cd).

### Derived texts without constraint
A derived text property holds a (sequence of) static text values and text values from other properties:

> ```js
'Address': group {
    'Street'       : text // e.g. "Huntington Rd"
    'Street number': text // e.g. "12B"
}
 // label for an external billing system:
'Address label': text
    = .'Address'.'Street' " " .'Address'.'Street number' // "Huntington Rd 12B"
```
### Derived texts with constraint (derived references)
The `application` language supports two types of derived references: `singular` and `branch`.
The `singular` type creates a direct relation between nodes using other relations.
The `branch` type is required for creating derived references to items in derived collections merge nodes of different types (see [node type rule](#node-types)).
The example below shows a property ` for deriving a (`singular`) direct reference from an `Orders` item to a `Manufacturers` item.
The expression for the `Manufacturer` reference an `Orders` item requires specifying an [`output parameter`](#output-parameters-legacy)
after the constraint expression for the `Product` property.

> ```js
'Manufacturers': collection ['Name'] { 'Name': text }
'Products': collection ['Name'] {
    'Name': text
    'Manufacturer': text -> ^ .'Manufacturers'[]
}
'Orders': collection ['ID'] {
    'ID': text
    'Product': text -> ^ .'Products'[]
        where 'Manufacturer' -> >'Manufacturer'
    'Manufacturer': text -> ^ .'Manufacturers'[] = .'Product'&'Manufacturer'
}
```
### Derived files
An example of a derived file property `Contract`.
The property holds the value of a `Default Contract` in case of a `Standard` `Agreement`, and a `Custom` `Contract` in case of a `Custom` `Agreement`:
> ```js
'Default Contract': file
'Agreement': stategroup (
    'Standard' { }
    'Custom' {
        'Contract': file
    }
)
'Contract': file = switch .'Agreement' (
    |'Default' = .'Default Contract'
    |'Custom' = $ .'Contract'
)
```
### Derived numbers
Examples of derived number properties, including required conversion rules:

> ```js
root {
    'Tax Percentage': number positive 'percent'
    'Products': collection ['Name'] {
        'Name': text
        'Price': number 'eurocent'
        'Price (euro)': number 'euro' = from 'eurocent' .'Price'
        'Order Unit Quantity': number positive 'items per unit'
        'Orders': reference-set -> .'Orders' = inverse >'Product'
        'Sales Value': number 'eurocent' = sum <'Orders'* .'Price'
        'Items Sold': number 'items' = count <'Orders'*
    }
    'Total Sales Value': number 'eurocent' = sum .'Products'* .'Sales Value'
    'Number of Products': number 'items' = count .'Products'*
    'Orders': collection ['ID'] {
        'ID': text
        'Product': text -> ^ .'Products'[] -<'Orders'
        'Quantity': number positive 'items'
        'Loss': number 'items' = remainder ( .'Quantity' as 'items', >'Product' .'Order Unit Quantity' )
        'Price': number 'eurocent' = product ( >'Product'.'Price' as 'eurocent' , .'Quantity' )
        'Order Units': number positive 'units' = division ceil ( .'Quantity' as 'items' , >'Product'.'Order Unit Quantity' )
        'Tax': number 'eurocent'
        'Gross Price': number 'eurocent' = sum ( .'Price', .'Tax' )
        'Creation Time': number 'date and time'
        'Estimated Lead Time': number 'seconds'
        'Estimated Delivery Time': number 'date and time' = add ( .'Creation Time', .'Estimated Lead Time' )
        'Delivered': stategroup (
            'No' { }
            'Yes' {
                'Delivery Time': number positive 'date and time'
                'Lead Time': number 'seconds' = diff 'date and time' ( .'Delivery Time', ^ .'Creation Time' )
            }
        )
    }
    'Gross Income': number 'eurocent' = sum .'Orders'* .'Gross Price'
}
numerical-types
    'percent'
    'euro'
        = 'eurocent' * 1 * 10 ^ -2
    'eurocent'
        = 'eurocent' * 'items'
    'items per unit'
    'units'
        = 'items' / 'items per unit'
    'items'
        = 'items' / 'items per unit' // required by 'remainder'; to be fixed
    'date and time' in 'seconds'
    'seconds'
```

### Derived states
The code sample exemplifies a derived state group property `Product found`.
The expression for deriving the state checks if the `Product` link produces a `Products` item from a `Products` `Catalog`.
This `Catalog` is provided by an external system, via an Alan `interface`: the `Catalog Provider`.
> ```js
'Catalog': group { can-update: interface 'Catalog Provider'
    'Products': collection ['Name'] {
        'Name': text
        'Price': number 'eurocent'
    }
}
'Orders': collection ['ID'] {
    'ID': text
    // a link to a 'Products' item from the catalog provider:
    'Product': text ~> ^ .'Products'[]
    'Product found': stategroup = switch >'Product' (
        | node as $ = 'Yes' ( 'Product' = $ )
        | none = 'No' ( )
    ) (
        'Yes' {
            'Product': text -> .'Catalog'.'Products'[] = parameter
            'Price': number 'eurocent' = .&'Product'.'Price'
        }
        'No' { }
    )
}
```


{: #grammar-rule--derivation-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">derivation expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">produce value</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
		}
		'<span class="token string">branch switch</span>' { [ <span class="token operator">switch</span> <span class="token operator">branch</span> ]
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary @tabular { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
			}
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary @tabular { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
			}
		}
		'<span class="token string">node switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">node path</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">equality</span>' {
					'<span class="token string">other node path</span>': [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
				}
				'<span class="token string">existence</span>' { }
			)
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group { //dynamic-order
				'<span class="token string">node</span>': @block group { [ <span class="token operator">|</span> <span class="token operator">node</span> ]
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
				}
				'<span class="token string">none</span>': @block [ <span class="token operator">|</span> <span class="token operator">none</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
			}
		}
		'<span class="token string">set switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">nodes path</span>': component <a href="#grammar-rule--object-set-path">'object set path'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group { //dynamic-order
				'<span class="token string">nodes</span>': @block group { [ <span class="token operator">|</span> <span class="token operator">nodes</span> ]
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
				}
				'<span class="token string">none</span>': @block [ <span class="token operator">|</span> <span class="token operator">none</span>@pad1 <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
				// '<span class="token string">node</span>': @block group {
				// 	'<span class="token string">include case</span>': stategroup (
				// 		'<span class="token string">no</span>' { }
				// 		'<span class="token string">yes</span>' { [ <span class="token operator">|</span> <span class="token operator">node</span>@pad1 ]
				// 			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
				// 			'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
				// 		}
				// 	)
				// }
			}
		}
		'<span class="token string">number switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">number path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
			'<span class="token string">compare to</span>': [ <span class="token operator">compare</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] stategroup (
				'<span class="token string">value</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
				}
				'<span class="token string">path</span>' {
					'<span class="token string">right number path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
				}
			)
			'<span class="token string">last case</span>': reference = last
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary (
				static '<span class="token string">equals</span>' [ <span class="token operator">==</span> ]
				static '<span class="token string">less than or greater than</span>' [ <span class="token operator"><></span> ]
				static '<span class="token string">greater than</span>' [ <span class="token operator">></span> ]
				static '<span class="token string">greater than or equals</span>' [ <span class="token operator">>=</span> ]
				static '<span class="token string">less than</span>' [ <span class="token operator"><</span> ]
				static '<span class="token string">less than or equals</span>' [ <span class="token operator"><=</span> ]
			) { @block [ <span class="token operator">|</span> ]
				'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">case</span>' = predecessor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--derivation-expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">derivation expression tail</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">reference</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">branch</span>' // branch of derived collection constructed using flatten expressions
				{
					'<span class="token string">branch</span>': [ <span class="token operator">from</span> ] reference
					'<span class="token string">expression</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
				}
			)
		}
		'<span class="token string">text</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': text
				}
				'<span class="token string">concatenation</span>' { [ <span class="token operator">concat</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] indent
					'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-list">'derivation expression list'</a>
				}
			)
		}
		'<span class="token string">number</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state instantiation</span>': component <a href="#grammar-rule--state-instantiation">'state instantiation'</a>
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--derivation-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">derivation expression list</span>' { @list
	'<span class="token string">head</span>': component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--derivation-expression-list">'derivation expression list'</a>
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
		'<span class="token string">unary</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
				}
				'<span class="token string">value</span>' { [ <span class="token operator">deprecated</span> ]
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">numerical type conversion</span>' {
					'<span class="token string">conversion</span>': [ <span class="token operator">from</span> ] reference
					'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
				}
				'<span class="token string">sign inversion</span>' { [ <span class="token operator">-</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
				}
			)
		}
		'<span class="token string">aggregate</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection operation</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">property</span>' {
							'<span class="token string">operation</span>': stategroup (
								'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
								'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
								'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
								'<span class="token string">standard deviation</span>' { [ <span class="token operator">std</span> ] }
							)
							'<span class="token string">numbers path</span>': component <a href="#grammar-rule--object-set-path">'object set path'</a>
						}
						'<span class="token string">count</span>' { [ <span class="token operator">count</span> ]
							'<span class="token string">nodes path</span>': component <a href="#grammar-rule--object-set-path">'object set path'</a>
						}
					)
				}
				'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">numerator</span>': component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					'<span class="token string">denominator</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
				}
				'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
					'<span class="token string">rounding</span>': stategroup (
						'<span class="token string">ordinary</span>' { }
						'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
						'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
					)
					'<span class="token string">numerator</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
					'<span class="token string">denominator</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
				}
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">left</span>': component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
					'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
				}
				'<span class="token string">list operation</span>' {
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
						'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
						'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
					)
					'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] @list indent component <a href="#grammar-rule--derivation-expression-list">'derivation expression list'</a>
				}
				'<span class="token string">addition</span>' { [ <span class="token operator">add</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">left</span>': component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
				}
				'<span class="token string">difference</span>' { [ <span class="token operator">diff</span> ]
					'<span class="token string">relative numerical type</span>': reference
					'<span class="token string">left</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					'<span class="token string">right</span>': [ <span class="token operator">,</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--unary-number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">unary number expression</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--static-number-value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">static number value</span>' {
	'<span class="token string">value</span>': stategroup (
		'<span class="token string">zero</span>' { [ <span class="token operator">zero</span> ] }
		'<span class="token string">one</span>' { [ <span class="token operator">one</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--state-instantiation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state instantiation</span>' {
	'<span class="token string">state</span>': reference
	'<span class="token string">arguments</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] @list indent dictionary { @block
		'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
	}
}
</pre>
</div>
</div>
### Derived collections

{: #grammar-rule--flatten-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">flatten expression</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--group-ancestor-path">'group ancestor path'</a>
	'<span class="token string">path</span>': component <a href="#grammar-rule--plural-descendant-node-path">'plural descendant node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--plural-reference-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural reference expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">augment</span>' {
			'<span class="token string">collection path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
			'<span class="token string">filter path</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--descendant-object-path">'descendant object path'</a>
		}
		'<span class="token string">union</span>' { [ <span class="token operator">union</span> ]
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--flatten-expression">'flatten expression'</a>
				'<span class="token string">dependency</span>': component <a href="#grammar-rule--dependency-step">'dependency step'</a>
				'<span class="token string">inversion</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' {
						'<span class="token string">reference set</span>': [ <span class="token operator">-<</span> ] reference
					}
				)
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--plural-descendant-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural descendant node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': component <a href="#grammar-rule--property-step">'property step'</a>
			'<span class="token string">value type</span>': stategroup (
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' { }
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--plural-descendant-node-path">'plural descendant node path'</a>
		}
	)
}
</pre>
</div>
</div>
## Users, Identities, Permissions, and Todos
---

Examples for permissions and todos:

> ```js
'Users': collection ['ID']
    can-create: user .'Type'?'Admin'
    can-delete: user .'Type'?'Admin'
{ can-update: user .'Type'?'Admin'
    'ID': text
    'Address': group { can-update: equal ( /*this*/ , user )
        'Street': text
        'City': text
    }
    'Type': stategroup (
        'Admin' { }
        'Employee' { }
        'Unknown' { has-todo: user .'Type'?'Admin' }
    )
}
// only team members can read team information:
'Teams': collection ['Name'] { can-read: node-switch .'Members' [ user ]
    'Name': text
    'Members': collection ['Member'] {
        'Member': text ~> ^ ^ .'Users'
    }
    'Description': text
}
```


{: #grammar-rule--node-permissions-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node permissions definition</span>' { dynamic-order
	'<span class="token string">read permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { @block [ <span class="token operator">can-read:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
	'<span class="token string">update permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { @block [ <span class="token operator">can-update:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--item-permissions-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">item permissions definition</span>' { dynamic-order
	'<span class="token string">create permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { @block [ <span class="token operator">can-create:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
	'<span class="token string">delete permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { @block [ <span class="token operator">can-delete:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
}
</pre>
</div>
</div>
By default, a user can execute a command if it is reachable.
A command is reachable when a user can read a node for which the command can be executed.

Note that if a command A calls another command B, then required permissions for B are not checked.
That is, the application only verifies that the user is permitted to execute command A.


{: #grammar-rule--command-permission-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command permission definition</span>' {
	'<span class="token string">execute permission</span>': stategroup (
		'<span class="token string">reachable</span>' { }
		'<span class="token string">explicit</span>' { @block [ <span class="token operator">can-execute:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--permission }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">permission</span>' {
	'<span class="token string">modifier</span>': stategroup (
		'<span class="token string">user</span>' {
			'<span class="token string">requirement</span>': component <a href="#grammar-rule--user-requirement">'user requirement'</a>
		}
		'<span class="token string">imported interface</span>' {
			'<span class="token string">interface</span>': [ <span class="token operator">interface</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--todo-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">todo definition</span>' {
	'<span class="token string">todo</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { @block [ <span class="token operator">has-todo:</span> ]
			'<span class="token string">requirement</span>': component <a href="#grammar-rule--user-requirement">'user requirement'</a>
			'<span class="token string">ui</span>': @break? indent component <a href="#grammar-rule--ui-todo">'ui todo'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--user-requirement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">user requirement</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--node-expression">'node expression'</a>
	'<span class="token string">has filter</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
			'<span class="token string">path</span>': [ <span class="token operator">where</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--user-requirement">'user requirement'</a>
		}
	)
	'<span class="token string">has alternative</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">||</span> ]
			'<span class="token string">alternative</span>': component <a href="#grammar-rule--user-requirement">'user requirement'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--user-initializer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">user initializer</span>' {
	'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--password-initializer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">password initializer</span>' {
	'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--identity-initializer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">identity initializer</span>' {
	'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
}
</pre>
</div>
</div>
## Commands and Timers
---

Commands enable external systems to perform operations via an Alan `interface` on `application` data.
Furthermore, commands can perform operations on other systems that other systems provide via an Alan `interface`.
For this to work, interfaces have to be listed in the `interfaces` section of an `application` model.
Also, the `external` command needs to be consumed by the application model, like the `Place Order` command in the example:

> ```js
'Products': collection ['Name'] {
    'Name': text
}
'Place Order': command { 'Product': text -> .'Products'[] } external
'Orders': collection ['ID'] {
    'ID': text
    'Product': text -> ^ .'Products'[]
    'Creation Time': number 'date and time' = creation-time
    'Status': stategroup (
        'New' {
            'Order from Manufacturer': command { }
                => execute .'Place Order' ( 'Product' = ^ .'Product' )
                => update ^ (
                    'Status' = create 'Waiting for Manufacturer' ( )
                )
        }
        'Delivered' { }
        'Delayed' { }
        'Waiting for Manufacturer' {
            'Agreed Upon Delivery Time': number 'date and time'
                timer ontimeout => update ^ (
                    'Status' = ensure 'Delayed' ( )
                )
        }
    )
}
// for external system 'Delivery Service':
'Register Delivery': command { 'Order': text -> .'Orders'[] }
    update @ >'Order' (
        'Status' = create 'Delivered' ( )
    )
```

{: #grammar-rule--command-object-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command object expression</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
		'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--command-object-initialization-behaviour }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command object initialization behaviour</span>' {
	'<span class="token string">behaviour</span>': stategroup (
		'<span class="token string">ensure existence</span>' { [ <span class="token operator">ensure</span> ] }
		'<span class="token string">fail when exists</span>' { [ <span class="token operator">create</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--command-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command expression</span>' {
	'<span class="token string">operation</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
					}
				}
			)
		}
		'<span class="token string">node switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">expression</span>': component <a href="#grammar-rule--node-expression">'node expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">node case</span>': @block [ <span class="token operator">|</span> <span class="token operator">node</span> ] group {
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
				}
				'<span class="token string">none case</span>': @block [ <span class="token operator">|</span> <span class="token operator">none</span> ] group {
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
				}
			}
		}
		'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">has tail</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">where</span> ]
							'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
						}
					)
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">collection</span>' {
							'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
						}
						'<span class="token string">reference set</span>' {
							'<span class="token string">reference set</span>': [ <span class="token operator"><</span> ] reference
						}
					)
					'<span class="token string">has tail</span>': stategroup (
						'<span class="token string">no</span>' { }
						'<span class="token string">yes</span>' { [ <span class="token operator">where</span> ]
							'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
						}
					)
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				}
			)
			'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
		}
		'<span class="token string">ignore</span>' { [ <span class="token operator">ignore</span> ] }
		'<span class="token string">update properties</span>' { [ <span class="token operator">update</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">target</span>': stategroup (
				'<span class="token string">node</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
				}
				'<span class="token string">property</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
				}
			)
		}
		'<span class="token string">execute operation</span>' { [ <span class="token operator">execute</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">command</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">expression</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
		}
		'<span class="token string">produce value</span>' {
			'<span class="token string">value</span>': stategroup (
				'<span class="token string">object</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">behaviour</span>': component <a href="#grammar-rule--command-object-initialization-behaviour">'command object initialization behaviour'</a>
					'<span class="token string">state</span>': reference
					'<span class="token string">expression</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
				}
				'<span class="token string">scalar</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--scalar-expression">'scalar expression'</a>
				}
				'<span class="token string">empty collection</span>' { [ <span class="token operator">empty</span> ] }
				'<span class="token string">current value</span>' { [ <span class="token operator">current</span> <span class="token operator">||</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--command-expression">'command expression'</a>
				}
			)
		}
		'<span class="token string">entry</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">create</span>' {
					'<span class="token string">behaviour</span>': component <a href="#grammar-rule--command-object-initialization-behaviour">'command object initialization behaviour'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
				}
				'<span class="token string">delete</span>' { [ <span class="token operator">delete</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--command }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command</span>' { [ <span class="token operator">=></span> ]
	'<span class="token string">expression</span>': component <a href="#grammar-rule--command-expression">'command expression'</a>
	'<span class="token string">has next command</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">command</span>': component <a href="#grammar-rule--command">'command'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter definition</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ] indent
	'<span class="token string">properties</span>': dictionary { @block
		'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">property</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">property</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-collection-parameter">'ui collection parameter'</a>
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">has constraint</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' {
						'<span class="token string">referencer</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--parameter-referencer">'parameter referencer'</a>
					}
				)
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-text-parameter">'ui text parameter'</a>
			}
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">integer</span>' { }
					'<span class="token string">natural</span>' { [ <span class="token operator">positive</span> ] }
				)
				'<span class="token string">numerical type</span>': reference
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-number-parameter">'ui number parameter'</a>
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-file-parameter">'ui file parameter'</a>
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-state-group-parameter">'ui state group parameter'</a>
				'<span class="token string">first state</span>': reference = first
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary @order: .'<span class="token string">view order</span>' { @block
					'<span class="token string">has successor</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">constraints</span>': @list indent dictionary { @block [ <span class="token operator">where</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--parameter-state-constraint-expression">'parameter state constraint expression'</a>
					}
					'<span class="token string">parameters</span>': @raw component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
				}
			}
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-group-parameter">'ui group parameter'</a>
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-referencer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter referencer</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">collection</span>': [ <span class="token operator">.</span>,'<span class="token string">[ ]</span>'] reference
	'<span class="token string">tail</span>': component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-state-constraint-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter state constraint expression</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--scalar-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">scalar expression list</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--scalar-expression">'scalar expression'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--scalar-expression-list">'scalar expression list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--scalar-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">scalar expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">number</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
				}
				'<span class="token string">now in seconds</span>' { [ <span class="token operator">now</span> ] }
				'<span class="token string">unary expression</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">absolute value</span>' { [ <span class="token operator">abs</span> ] }
						'<span class="token string">numerical type conversion</span>' {
							'<span class="token string">conversion</span>': [ <span class="token operator">from</span> ] reference
						}
						'<span class="token string">sign inversion</span>' { [ <span class="token operator">-</span> ] }
					)
					'<span class="token string">expression</span>': component <a href="#grammar-rule--scalar-expression">'scalar expression'</a>
				}
				'<span class="token string">list expression</span>' {
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
						'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
						'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
						'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
					)
					'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent component <a href="#grammar-rule--scalar-expression-list">'scalar expression list'</a>
				}
				'<span class="token string">binary expression</span>' {
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
							'<span class="token string">rounding</span>': stategroup (
								'<span class="token string">ordinary</span>' { }
								'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
								'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
							)
						}
						'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> ] }
					)
					'<span class="token string">expressions</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent
						'<span class="token string">left</span>': component <a href="#grammar-rule--scalar-expression">'scalar expression'</a>
						'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--scalar-expression">'scalar expression'</a>
					}
				}
			)
		}
		'<span class="token string">text</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': text
				}
			)
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">context</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
			)
		}
	)
}
</pre>
</div>
</div>
## Metadata
---

The metadata recording enables you to record the mutation times of scalar values in your application: texts, numbers, and files.

{: #grammar-rule--metadata-recording }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">metadata recording</span>' {
	'<span class="token string">record mutation time</span>': @block stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">mutation-time</span> ]
			'<span class="token string">meta property</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
## Navigation
---
Navigation steps:
> ```js
.'My Property'            // select property value
?'My State'               // require state
>>'My Text'               // get referenced node (for text properties with a reference)
.'My Text'&'Where'        // get 'where'-rule value from property
.&'My State Where'        // get 'where'-rule result from context state
.'My Collection'*         // iterate collection
--
^                // go to parent node
$^               // go to parent assigned $ object
$                // select assigned $ object
@                // select parameter object
@^               // select parent parameter object
```

### Node navigation

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

{: #grammar-rule--context-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context node path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">dynamic user</span>' { [ <span class="token operator">user</span> ] }
		'<span class="token string">this</span>' { }
		'<span class="token string">variable</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
			'<span class="token string">variable</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">parameter</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
			'<span class="token string">reference type</span>': stategroup (
				'<span class="token string">text</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">constraint</span>': [ <span class="token operator">.&</span> ] reference
				}
			)
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
		'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
		'<span class="token string">property rule</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">group</span>' { [ <span class="token operator">.</span> ]
			'<span class="token string">group</span>': reference
		}
		'<span class="token string">state context rule</span>' {
			'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] reference
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">reference</span>' { [ <span class="token operator">></span> ]
			'<span class="token string">text</span>': reference
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

{: #grammar-rule--node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--context-node-path">'context node path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--singular-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular node path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional node path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--descendant-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">descendant node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">value type</span>': stategroup (
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' { }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node expression</span>' {
	'<span class="token string">node path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">equality</span>' {
			'<span class="token string">expected node path</span>': [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
		}
		'<span class="token string">existence</span>' { }
		'<span class="token string">containment</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">key path</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">node</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">parameter</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
						'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
					}
				)
			}
		}
	)
}
</pre>
</div>
</div>
### Variable assignment and navigation

{: #grammar-rule--optional-variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional variable assignment</span>' {
	'<span class="token string">has assignment</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">as</span> ]
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
'<span class="token string">variable assignment</span>' {
	'<span class="token string">name</span>': reference = first
	'<span class="token string">variables</span>': dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { }
			| none = '<span class="token string">no</span>'
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--named-object-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">named object assignment</span>' {
	'<span class="token string">name</span>': reference = first
	'<span class="token string">named objects</span>': dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { }
			| none = '<span class="token string">no</span>'
		)
	}
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
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">as</span> ]
			'<span class="token string">assignment</span>': component <a href="#grammar-rule--named-object-assignment">'named object assignment'</a>
		}
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
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">$^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-named-object-path">'ancestor named object path'</a>
		}
	)
}
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
### Parameter object navigation

{: #grammar-rule--ancestor-parameter-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor parameter path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">@</span> ] }
		'<span class="token string">yes</span>' { [ <span class="token operator">@^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-parameter-path">'ancestor parameter path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-parameter-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular parameter path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-parameter-path">'ancestor parameter path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-parameter-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional parameter path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-parameter-path">'ancestor parameter path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter path tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
		}
	)
}
</pre>
</div>
</div>
### Navigation for constraints & derivations

{: #grammar-rule--group-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">group node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--group-node-path">'group node path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--singular-variablized-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular variablized object path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--variablized-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variablized object path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this</span>' { }
		'<span class="token string">variable</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-named-object-path">'ancestor named object path'</a>
			'<span class="token string">named object</span>': [ <span class="token operator">$</span> ] reference
		}
	)
	'<span class="token string">path</span>': component <a href="#grammar-rule--object-path">'object path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--group-ancestor-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">group ancestor path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--group-ancestor-path">'group ancestor path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--property-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">property step</span>' {
	'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
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
			'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
		}
		'<span class="token string">reference rule</span>' {
			'<span class="token string">property</span>': component <a href="#grammar-rule--property-step">'property step'</a>
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">state context rule</span>' {
			'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] reference
		}
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
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">property value</span>' {
					'<span class="token string">property</span>': component <a href="#grammar-rule--property-step">'property step'</a>
				}
				'<span class="token string">dependency</span>' {
					'<span class="token string">dependency</span>': component <a href="#grammar-rule--dependency-step">'dependency step'</a>
				}
				'<span class="token string">reference set</span>' {
					'<span class="token string">reference set</span>': [ <span class="token operator"><</span> ] reference
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--object-path">'object path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--descendant-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">descendant object path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--object-path">'object path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--object-set-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object set path</span>' {
	'<span class="token string">collection path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
	'<span class="token string">value path</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--object-path">'object path'</a>
}
</pre>
</div>
</div>
## User interface annotations
---
User interface annotations, or annotations for short, are recognizable by the
`@` character before the keyword. E.g. `@default:`. Most annotations
affect generated user interfaces (a system of type `auto-webclient`); they typically
do not affect custom user interfaces (system type `webclient`).

It is possible to use multiple annotations on a single property. Be aware that
they should be added in a specific order. Consult this grammar for the order of
annotations.

### Defaults
Most property types support the `@default:` annotation. Defaults apply default values to properties of new
nodes only and fail silently. That is, if the path contains a state navigation step and the
stategroup is not in that state, the default won't be applied. In the following
example the `Score` property will not be set when the state of `Default Score`
is anything other than `Known`.

>```js
'Score': number positive 'score' @default: .'Default Score'?'Known'.'Value'
```

A default value is not necessarily a valid value. If validation
rules or constraints apply, a default value can be invalid.
When a derived value is used, make sure it is not a part of the new
node. Derived values on new nodes are computed after the node is saved,
and will therefore not be included in default values.

The property description would get set to: `Deliver  pieces`.

>```js
'Description': text @default: "Deliver ", to-text . 'To deliver' " pieces."
'To deliver' : number 'pieces' = ^ >'Order'.'Amount'
```

### Identifying properties

Properties that are important for the identification of a collection entry can be marked
with the `@identifying` annotation. Identifying properties are shown together with the
unique identifier of a collection entry, whenever the entry is referenced.
For example, when an employee has a uniquely identifying personnel number
in a collection of employees, a reference to employee will show the name of the employee
when the 'name' property is marked as identifying.

### Icons

For better visual identification an icon can be specified using the @icon
attribute. As an argument it takes an icon name. A complete list of the
supported icons can be found at: https://octicons.github.com/.

{: #grammar-rule--ui-identifying-property-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui identifying property selection</span>' {
	'<span class="token string">has properties</span>': stategroup = node-switch .'<span class="token string">properties</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary @order: .'<span class="token string">view order</span>' { @block indent
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }
			'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
				'<span class="token string">selection</span>': component <a href="#grammar-rule--ui-identifying-property-selection">'ui identifying property selection'</a>
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">has identifying states</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' {
						'<span class="token string">identifying</span>': stategroup (
							'<span class="token string">no</span>' { [ <span class="token operator">hide</span> ] }
							'<span class="token string">yes</span>' { }
						)
						'<span class="token string">first state</span>': reference = first
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary @order: .'<span class="token string">view order</span>' { @block indent
							'<span class="token string">has successor</span>': stategroup = node-switch successor (
								| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">selection</span>': component <a href="#grammar-rule--ui-identifying-property-selection">'ui identifying property selection'</a>
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

{: #grammar-rule--ui-action-interaction }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui action interaction</span>' {
	'<span class="token string">interactive</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">interactive</span> ] }
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-action-visualization }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui action visualization</span>' {
	'<span class="token string">show target</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">show</span> ] }
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-object-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui object expression</span>' {
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
		'<span class="token string">default</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--ui-entry-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui entry expression list</span>' {
	'<span class="token string">entry expression</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
	'<span class="token string">more entries</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ui-entry-expression-list">'ui entry expression list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui expression</span>' {
	'<span class="token string">operation</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
					}
				}
			)
		}
		'<span class="token string">node switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">expression</span>': component <a href="#grammar-rule--node-expression">'node expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">node case</span>': @block [ <span class="token operator">|</span> <span class="token operator">node</span> ] group {
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
				}
				'<span class="token string">none case</span>': @block [ <span class="token operator">|</span> <span class="token operator">none</span> ] group {
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
				}
			}
		}
		'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-parameter-path">'singular parameter path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				}
			)
			'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
		}
		'<span class="token string">ignore</span>' { [ <span class="token operator">ignore</span> ] }
		'<span class="token string">update properties</span>' { [ <span class="token operator">update</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">target</span>': stategroup (
				'<span class="token string">node</span>' {
					'<span class="token string">interaction</span>': component <a href="#grammar-rule--ui-action-interaction">'ui action interaction'</a>
					'<span class="token string">visualization</span>': component <a href="#grammar-rule--ui-action-visualization">'ui action visualization'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
				}
			)
		}
		'<span class="token string">execute operation</span>' { [ <span class="token operator">execute</span> ]
			/*
			*	execute .'<span class="token string">My Command or Action</span>' (
			*		'<span class="token string">MyInt</span>' = integer 10
			*		'<span class="token string">MyText</span>' = "text"
			*		'<span class="token string">MyCol</span>' = (
			*			create (
			*				'<span class="token string">K</span>' = @ .'<span class="token string">new key</span>'
			*				'<span class="token string">T</span>' = 10
			*			)
			*		)
			*	)
			*/
			'<span class="token string">interaction</span>': component <a href="#grammar-rule--ui-action-interaction">'ui action interaction'</a>
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">operation</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
		}
		'<span class="token string">produce value</span>' {
			'<span class="token string">value</span>': stategroup (
				'<span class="token string">object</span>' {
					/*
					*	update >'<span class="token string">Node</span>' (
					*		'<span class="token string">Text</span>' = "2"
					*		'<span class="token string">Col</span>' = (
					*			create (
					*				'<span class="token string">User</span>' = "E1"
					*			)
					*		)
					*		'<span class="token string">Group</span>' = (
					*			'<span class="token string">Int</span>' = integer 2
					*		)
					*	)
					*/
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
				}
				'<span class="token string">state</span>' {
					/*
					*	update >'<span class="token string">Node</span>' (
					*		'<span class="token string">StateGroup</span>' = create '<span class="token string">Open</span>' (
					*			'<span class="token string">P1</span>' = "1"
					*		)
					*	)
					*/
					'<span class="token string">state</span>': [ <span class="token operator">create</span> ] reference
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
				}
				'<span class="token string">scalar</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
				}
			)
		}
		'<span class="token string">entry list</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">entries</span>': component <a href="#grammar-rule--ui-entry-expression-list">'ui entry expression list'</a>
		}
		'<span class="token string">entry</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">create</span>' { [ <span class="token operator">create</span> ]
					'<span class="token string">interaction</span>': component <a href="#grammar-rule--ui-action-interaction">'ui action interaction'</a>
					'<span class="token string">visualization</span>': component <a href="#grammar-rule--ui-action-visualization">'ui action visualization'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
				}
				'<span class="token string">delete</span>' { [ <span class="token operator">delete</span> ]
					'<span class="token string">interaction</span>': component <a href="#grammar-rule--ui-action-interaction">'ui action interaction'</a>
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-action }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui action</span>' { [ <span class="token operator">=></span> ]
	'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
	'<span class="token string">has next action</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">action</span>': component <a href="#grammar-rule--ui-action">'ui action'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-scalar-value-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui scalar value expression list</span>' {
	'<span class="token string">value</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ui-scalar-value-expression-list">'ui scalar value expression list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-scalar-value-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui scalar value expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">text</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">auto increment</span>' { [ <span class="token operator">auto-increment</span> ] }
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': text
				}
				'<span class="token string">current user</span>' { [ <span class="token operator">user</span> ] }
				'<span class="token string">guid</span>' { [ <span class="token operator">guid</span> ] }
				'<span class="token string">number to text</span>' { [ <span class="token operator">to-text</span> ]
					'<span class="token string">numerical type</span>': reference
					'<span class="token string">pad</span>': stategroup (
						'<span class="token string">yes</span>' { [ <span class="token operator">pad</span> ]
							'<span class="token string">size</span>': integer
							'<span class="token string">character</span>': [ <span class="token operator">with</span> ] text
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
				}
				'<span class="token string">concatenation</span>' { [ <span class="token operator">concat</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">list</span>': component <a href="#grammar-rule--ui-scalar-value-expression-list">'ui scalar value expression list'</a>
				}
			)
		}
		'<span class="token string">number</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">value</span>' {
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
				}
				'<span class="token string">now in seconds</span>' { [ <span class="token operator">now</span> ] }
				'<span class="token string">unary expression</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">absolute value</span>' { [ <span class="token operator">abs</span> ] }
						'<span class="token string">numerical type conversion</span>' {
							'<span class="token string">conversion</span>': [ <span class="token operator">from</span> ] reference
						}
						'<span class="token string">sign inversion</span>' { [ <span class="token operator">-</span> ] }
					)
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
				}
				'<span class="token string">list expression</span>' {
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
						'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
						'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
						'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
					)
					'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent component <a href="#grammar-rule--ui-scalar-value-expression-list">'ui scalar value expression list'</a>
				}
				'<span class="token string">binary expression</span>' {
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
							'<span class="token string">rounding</span>': stategroup (
								'<span class="token string">ordinary</span>' { }
								'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
								'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
							)
						}
						'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> ] }
					)
					'<span class="token string">expressions</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent
						'<span class="token string">left</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
						'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
					}
				}
			)
		}
		'<span class="token string">style</span>' {
			'<span class="token string">style</span>': component <a href="#grammar-rule--ui-style">'ui style'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state</span>': reference
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--ui-parametrized-node-path">'ui parametrized node path'</a>
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-parameter-path">'conditional parameter path'</a>
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
			)
		}
		'<span class="token string">sticky</span>' { [ <span class="token operator">sticky</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-scalar-default }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui scalar default</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
	'<span class="token string">has fallback</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">||</span> ] @break? indent
			'<span class="token string">fallback</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-text-validation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui text validation</span>' {
	'<span class="token string">regular expression</span>': text
}
</pre>
</div>
</div>

{: #grammar-rule--ui-number-limit }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number limit</span>' {
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

{: #grammar-rule--ui-parametrized-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui parametrized node path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--ui-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui node path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--ui-node-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui node path tail</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--ui-numerical-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui numerical type</span>' { @list indent dynamic-order
	'<span class="token string">represent as</span>': @block stategroup (
		'<span class="token string">model</span>' { }
		'<span class="token string">date</span>' { [ <span class="token operator">@date</span> ] }
		'<span class="token string">date and time</span>' { [ <span class="token operator">@date-time</span> ] }
		'<span class="token string">decimal</span>' { [ <span class="token operator">@factor:</span> <span class="token operator">10^</span> ]
			'<span class="token string">point translation</span>': integer
		}
		'<span class="token string">duration</span>' { [ <span class="token operator">@duration:</span> ]
			'<span class="token string">unit</span>': stategroup (
				'<span class="token string">seconds</span>' { [ <span class="token operator">seconds</span> ] }
				'<span class="token string">minutes</span>' { [ <span class="token operator">minutes</span> ] }
				'<span class="token string">hours</span>' { [ <span class="token operator">hours</span> ] }
			)
		}
	)
	'<span class="token string">label</span>': @block stategroup (
		'<span class="token string">model</span>' { }
		'<span class="token string">custom</span>' { [ <span class="token operator">@label:</span> ]
			'<span class="token string">label</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-handheld-descriptor }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui handheld descriptor</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic value</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">static text</span>' {
			'<span class="token string">text</span>': text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ui-handheld-descriptor">'ui handheld descriptor'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-command-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui command attribute</span>' { @list indent
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' { [ <span class="token operator">@visible</span> ] }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">handheld</span>': @block stategroup (
		'<span class="token string">true</span>' { [ <span class="token operator">@handheld:</span> ]
			'<span class="token string">descriptor</span>': component <a href="#grammar-rule--ui-handheld-descriptor">'ui handheld descriptor'</a>
		}
		'<span class="token string">false</span>' { }
	)
}
</pre>
</div>
</div>
### Group
The `@breakout` annotation indicates that a group property
should not be displayed together with the other properties. At the time of
this writing, the group is put in a separate tab in the details view of an entry.
Note that the tab is always added to the top level tabs of a details view.
That is, if a group is inside a state or another group, it is not added to the tabs of the state.

{: #grammar-rule--ui-group-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui group property</span>' { @list indent dynamic-order
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' {
			'<span class="token string">break out</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">@breakout</span> ] }
			)
		}
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>
### Collection
The `@default:` annotation copies entries of a source collection into the annotated collection.
A subset of the entries from the source collection can be copied by specifying a state filter:

>```js
'Labels': collection ['Name'] {
	'Name': text
	'Default': stategroup (
		'Yes' { }
		'No' { }
	)
}
'Issues': collection ['Name']  {
	'Name': text
	'Labels': collection ['Name'] @default: >'Name'.'Default'?'Yes' {
		'Name': text -> ^ ^ .'Labels'[]
	}
}
```

This only applies to new nodes holding collections. This annotation does nothing for
collections on the root node:

> ```js
root {
	'People': collection ['Name'] {
		'Name': text
	}
	'Employees': collection ['Name'] @default: >'Name' { // This has no effect.
		'Name': text
	}
}
```

Collections can only be initialized from the collection that it references,
using the key property, or using a derived link that derives from the key. In
the latter case, other collections can be used to initialize an entry as long as
the keys are the same.

> ```js`
'Imported Categories': collection ['Id'] {
	'Id': text
}
'Gegevens': collection ['Id'] @default: >'Category' {
	'Id': text /* -> some constraint or not */
	'Category': text ~> ^ .'Imported Categories'[] = .'Id'
}
````

{: #grammar-rule--ui-collection-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui collection property</span>' { @list indent dynamic-order
	'<span class="token string">sort</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">direction</span>': stategroup (
				'<span class="token string">ascending</span>' { [ <span class="token operator">@ascending:</span> ] }
				'<span class="token string">descending</span>' { [ <span class="token operator">@descending:</span> ] }
			)
			'<span class="token string">property context</span>': component <a href="#grammar-rule--ui-node-path">'ui node path'</a>
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
		}
	)
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' {
			'<span class="token string">break out</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">@breakout</span> ] }
			)
		}
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">size</span>': @block stategroup (
		'<span class="token string">small</span>' { [ <span class="token operator">@small</span> ] }
		'<span class="token string">large</span>' {
			'<span class="token string">handheld filter</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">@handheld:</span> ]
					'<span class="token string">filter path</span>': component <a href="#grammar-rule--ui-node-path">'ui node path'</a>
					'<span class="token string">filter stategroup</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">filter state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">no</span>' { }
			)
		}
	)
	'<span class="token string">can be dormant</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@dormant</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--descendant-node-path">'descendant node path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">dormant state</span>': [ <span class="token operator">?</span> ] reference
		}
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">default</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">key reference</span>': component <a href="#grammar-rule--entry-reference-selector">'entry reference selector'</a>
			'<span class="token string">entry filter</span>': component <a href="#grammar-rule--ui-node-path-tail">'ui node path tail'</a>
		}
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
	'<span class="token string">has style</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@style:</span> ]
			'<span class="token string">style expression</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-number-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number property</span>' { @list indent dynamic-order
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' { }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">identifying</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@identifying</span> ] }
	)
	'<span class="token string">default</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">metadata</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@metadata</span> ] }
	)
	'<span class="token string">validation</span>': @block group {
		'<span class="token string">has minimum</span>': stategroup (
			'<span class="token string">no</span>' { }
			'<span class="token string">yes</span>' { [ <span class="token operator">@min:</span> ]
				'<span class="token string">minimum</span>': component <a href="#grammar-rule--ui-number-limit">'ui number limit'</a>
			}
		)
		'<span class="token string">has maximum</span>': stategroup (
			'<span class="token string">no</span>' { }
			'<span class="token string">yes</span>' { [ <span class="token operator">@max:</span> ]
				'<span class="token string">maximum</span>': component <a href="#grammar-rule--ui-number-limit">'ui number limit'</a>
			}
		)
	}
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-file-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui file property</span>' { @list indent dynamic-order
	'<span class="token string">file name expression</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@name:</span> ]
			'<span class="token string">file name expression</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' { }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-text-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui text property</span>' { @list indent dynamic-order
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' { }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">identifying</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@identifying</span> ] }
	)
	'<span class="token string">type</span>': @block stategroup (
		'<span class="token string">default</span>' { }
		'<span class="token string">multi-line</span>' { [ <span class="token operator">@multi-line</span> ] }
	)
	'<span class="token string">default value</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">has validation</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@validate:</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">regular expression</span>' {
					'<span class="token string">rules</span>': component <a href="#grammar-rule--ui-text-validation">'ui text validation'</a>
				}
				'<span class="token string">optional reference must resolve</span>' { [ <span class="token operator">resolvable</span> ] }
			)
		}
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
	'<span class="token string">has custom identifying properties</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@show:</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--ui-identifying-property-selection">'ui identifying property selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-state-group-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui state group property</span>' { @list indent dynamic-order
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' { }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">identifying</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@identifying</span> ] }
	)
	'<span class="token string">default state</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-state }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui state</span>' { @list indent dynamic-order
	'<span class="token string">desired state</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@desired</span> ] }
	)
	'<span class="token string">verified state</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@verified</span> ] }
	)
	'<span class="token string">icon</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
	'<span class="token string">has style</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@style:</span> ]
			'<span class="token string">style</span>': component <a href="#grammar-rule--ui-style">'ui style'</a>
		}
	)
	'<span class="token string">transitions</span>': dictionary { @block [ <span class="token operator">@transition:</span> ]
		'<span class="token string">action</span>': [ <span class="token operator">:</span> ] reference
	}
}
</pre>
</div>
</div>

{: #grammar-rule--ui-collection-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui collection parameter</span>' { @list indent dynamic-order
	'<span class="token string">default</span>': @block stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">key property</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">entry filter</span>': component <a href="#grammar-rule--ui-node-path-tail">'ui node path tail'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-text-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui text parameter</span>' { @list indent dynamic-order
	'<span class="token string">type</span>': @block stategroup (
		'<span class="token string">default</span>' { }
		'<span class="token string">multi-line</span>' { [ <span class="token operator">@multi-line</span> ] }
	)
	'<span class="token string">has validation</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@validate:</span> ]
			'<span class="token string">rules</span>': component <a href="#grammar-rule--ui-text-validation">'ui text validation'</a>
		}
	)
	'<span class="token string">default</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-number-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number parameter</span>' { @list indent dynamic-order
	'<span class="token string">default</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">validation</span>': @block group {
		'<span class="token string">has minimum</span>': stategroup (
			'<span class="token string">no</span>' { }
			'<span class="token string">yes</span>' { [ <span class="token operator">@min:</span> ]
				'<span class="token string">minimum</span>': component <a href="#grammar-rule--ui-number-limit">'ui number limit'</a>
			}
		)
		'<span class="token string">has maximum</span>': stategroup (
			'<span class="token string">no</span>' { }
			'<span class="token string">yes</span>' { [ <span class="token operator">@max:</span> ]
				'<span class="token string">maximum</span>': component <a href="#grammar-rule--ui-number-limit">'ui number limit'</a>
			}
		)
	}
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-file-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui file parameter</span>' { @list indent
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-state-group-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui state group parameter</span>' { @list indent dynamic-order
	'<span class="token string">default state</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-group-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui group parameter</span>' { @list indent
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-todo }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui todo</span>' { @list indent
	'<span class="token string">has description</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-style }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui style</span>' { @list indent
	'<span class="token string">style</span>': @block stategroup (
		'<span class="token string">foreground</span>' { [ <span class="token operator">foreground</span> ] }
		'<span class="token string">background</span>' { [ <span class="token operator">background</span> ] }
		'<span class="token string">brand</span>' { [ <span class="token operator">brand</span> ] }
		'<span class="token string">link</span>' { [ <span class="token operator">link</span> ] }
		'<span class="token string">accent</span>' { [ <span class="token operator">accent</span> ] }
		'<span class="token string">success</span>' { [ <span class="token operator">success</span> ] }
		'<span class="token string">warning</span>' { [ <span class="token operator">warning</span> ] }
		'<span class="token string">error</span>' { [ <span class="token operator">error</span> ] }
		'<span class="token string">blue</span>' { [ <span class="token operator">blue</span> ] }
		'<span class="token string">orange</span>' { [ <span class="token operator">orange</span> ] }
		'<span class="token string">green</span>' { [ <span class="token operator">green</span> ] }
		'<span class="token string">red</span>' { [ <span class="token operator">red</span> ] }
		'<span class="token string">purple</span>' { [ <span class="token operator">purple</span> ] }
		'<span class="token string">teal</span>' { [ <span class="token operator">teal</span> ] }
	)
}
</pre>
</div>
</div>
