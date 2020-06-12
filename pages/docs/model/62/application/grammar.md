---
layout: doc
origin: model
language: application
version: 62
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
If you want user authentication to be application-specific, you need to specify which text property holds (hashed) user passwords.
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
		'<span class="token string">context node path</span>': [ <span class="token operator">dynamic</span> <span class="token operator">:</span> ] component <a href="#grammar-rule--node-content-path">'node content path'</a>
		'<span class="token string">users collection</span>': [ <span class="token operator">.</span> ] reference
		'<span class="token string">has user authentication</span>': stategroup (
			'<span class="token string">yes</span>' { @block indent
				'<span class="token string">password node</span>': [ <span class="token operator">password</span> <span class="token operator">:</span> ] component <a href="#grammar-rule--node-content-path">'node content path'</a>
				'<span class="token string">password property</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">password status</span>': @block indent [ <span class="token operator">password-status</span> <span class="token operator">:</span> ] group {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">active state</span>': @block indent [ <span class="token operator">active</span> <span class="token operator">:</span> ] group {
						'<span class="token string">state</span>': reference
						'<span class="token string">initializer</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
					}
					'<span class="token string">reset state</span>': @block indent [ <span class="token operator">reset</span> <span class="token operator">:</span> ] group {
						'<span class="token string">state</span>': reference
						'<span class="token string">initializer</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
					}
				}
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">has external authentication</span>': stategroup (
			'<span class="token string">yes</span>' { @block indent
				'<span class="token string">authorities node</span>': [ <span class="token operator">external</span> <span class="token operator">authentication</span> <span class="token operator">:</span> ] component <a href="#grammar-rule--node-content-path">'node content path'</a>
				'<span class="token string">authorities collection</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">identities node</span>': component <a href="#grammar-rule--node-content-path">'node content path'</a>
				'<span class="token string">identities collection</span>': [ <span class="token operator">.</span> ] reference
				'<span class="token string">user reference</span>': [ <span class="token operator">:</span> ] reference
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
	'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--group-node-selection">'group node selection'</a> //'<span class="token string">singular node path tail</span>'
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
				'<span class="token string">undefined</span>' { }
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
An attribute is of type `property`, `reference-set`, or `command`.

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
'Price'       : integer 'euro'
'Release Date': natural 'date and time'
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
    'Simple' -> { ... /* attributes of this type */ ... }
    'Assembled' -> { ... /* attributes of this type */ ... }
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
'copy of City':= text = .'City' // derived value property with expression
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
	'<span class="token string">has attributes</span>': stategroup = match .'<span class="token string">attributes</span>' (
		| some = '<span class="token string">yes</span>' {
			'<span class="token string">first</span>' = first
			'<span class="token string">last</span>' = last
		}
		| none = '<span class="token string">no</span>'
	)
	'<span class="token string">attributes</span>': @raw dictionary { @block
		'<span class="token string">has predecessor</span>': stategroup = match predecessor (
			| some = '<span class="token string">yes</span>' { '<span class="token string">attribute</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has successor</span>': stategroup = match successor (
			| some = '<span class="token string">yes</span>' { '<span class="token string">attribute</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">referencer anchor</span>' { [ <span class="token operator">:</span> <span class="token operator">reference-set</span> ]
				'<span class="token string">node type path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--node-type-id">'node type id'</a>
				'<span class="token string">reference path</span>': [ <span class="token operator">=</span> <span class="token operator">inverse</span> ] group {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
			}
			'<span class="token string">command</span>' { [ <span class="token operator">:</span> <span class="token operator">command</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">global</span>' {
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-command-attribute">'ui command attribute'</a>
					}
					'<span class="token string">component</span>' { [ <span class="token operator">component</span> ] }
				)
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
				'<span class="token string">implementation</span>': stategroup (
					'<span class="token string">external</span>' { [ <span class="token operator">external</span> ] }
					'<span class="token string">internal</span>' {
						'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
					}
				)
			}
			'<span class="token string">action</span>' { [ <span class="token operator">:</span> <span class="token operator">action</span> ]
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
				'<span class="token string">action</span>': component <a href="#grammar-rule--ui-action">'ui action'</a>
			}
			'<span class="token string">property</span>' {
				'<span class="token string">data type</span>': stategroup (
					'<span class="token string">elementary</span>' { [ <span class="token operator">:</span> ] }
					'<span class="token string">derived</span>' { [ <span class="token operator">:=</span> ] }
				)
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
							'<span class="token string">derived</span>' {
								'<span class="token string">key constraint</span>': stategroup (
									'<span class="token string">no</span>' { [ <span class="token operator">=</span> <span class="token operator">flatten</span> ]
										'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
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
									'<span class="token string">yes</span>' { [ <span class="token operator">=</span> ]
										'<span class="token string">expression</span>': component <a href="#grammar-rule--plural-reference-expression">'plural reference expression'</a>
									}
								)
							}
						)
						'<span class="token string">permissions</span>': component <a href="#grammar-rule--item-permissions-definition">'item permissions definition'</a>
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-collection-property">'ui collection property'</a>
						'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
					}
					'<span class="token string">number</span>' {
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' {
								'<span class="token string">set</span>': stategroup (
									'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
									'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
								)
								'<span class="token string">numerical type</span>': reference
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">causal</span>' {
										'<span class="token string">type</span>': stategroup (
											'<span class="token string">mutation</span>' { [ <span class="token operator">=</span> <span class="token operator">mutation-time</span> ]
												'<span class="token string">watched property</span>': stategroup (
													'<span class="token string">number</span>' { [ <span class="token operator">#</span> ]
														'<span class="token string">number</span>': reference
													}
													'<span class="token string">text</span>' { [ <span class="token operator">.</span> ]
														'<span class="token string">text</span>': reference
													}
												)
											}
											'<span class="token string">creation</span>' { [ <span class="token operator">=</span> <span class="token operator">creation-time</span> ] }
											'<span class="token string">destruction</span>' {
												'<span class="token string">destruction operation</span>': stategroup (
													'<span class="token string">set to lifetime</span>' { [ <span class="token operator">=</span> <span class="token operator">life-time</span> ] }
													'<span class="token string">add lifetime</span>' { [ <span class="token operator">add</span> <span class="token operator">life-time</span> ] }
													'<span class="token string">subtract lifetime</span>' { [ <span class="token operator">subtract</span> <span class="token operator">life-time</span> ] }
												)
												'<span class="token string">watched stategroup</span>': [ <span class="token operator">?</span> ] reference
												'<span class="token string">watched state</span>': [ <span class="token operator">|</span> ] reference
											}
										)
									}
									'<span class="token string">simple</span>' {
										'<span class="token string">record mutation time</span>': stategroup (
											'<span class="token string">yes</span>' { @block [ <span class="token operator">mutation-time</span> ]
												'<span class="token string">meta property</span>': [ <span class="token operator">=</span> <span class="token operator">#</span> ] reference
											}
											'<span class="token string">no</span>' { }
										)
									}
								)
							}
							'<span class="token string">derived</span>' {
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
										'<span class="token string">numerical type</span>': reference
										'<span class="token string">conversion</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--numerical-type-conversion2">'numerical type conversion2'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--integer-expression">'integer expression'</a>
									}
									'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ]
										'<span class="token string">numerical type</span>': reference
										'<span class="token string">conversion</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--numerical-type-conversion2">'numerical type conversion2'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--natural-expression">'natural expression'</a>
									}
								)
							}
						)
						'<span class="token string">behaviour</span>': stategroup (
							'<span class="token string">none</span>' { }
							'<span class="token string">timer</span>' { [ <span class="token operator">timer</span> <span class="token operator">ontimeout</span> ]
								'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-number-property">'ui number property'</a>
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">expression</span>': component <a href="#grammar-rule--file-expression">'file expression'</a>
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-file-property">'ui file property'</a>
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' {
								'<span class="token string">has constraint</span>': stategroup (
									'<span class="token string">no</span>' { }
									'<span class="token string">yes</span>' { [ <span class="token operator">-></span> ]
										'<span class="token string">expression</span>': component <a href="#grammar-rule--reference-constraint-expression">'reference constraint expression'</a>
										'<span class="token string">output parameters</span>': component <a href="#grammar-rule--output-parameters-definition">'output parameters definition'</a>
									}
								)
								'<span class="token string">record mutation time</span>': @block stategroup (
									'<span class="token string">yes</span>' { [ <span class="token operator">mutation-time</span> ]
										'<span class="token string">meta property</span>': [ <span class="token operator">=</span> <span class="token operator">#</span> ] reference
									}
									'<span class="token string">no</span>' { }
								)
							}
							'<span class="token string">derived</span>' {
								'<span class="token string">has constraint</span>': stategroup (
									'<span class="token string">no</span>' { [ <span class="token operator">=</span> ]
										'<span class="token string">value source</span>': stategroup (
											'<span class="token string">key</span>' { [ <span class="token operator">$</span> ] }
											'<span class="token string">expression</span>' {
												'<span class="token string">expression</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
											}
										)
									}
									'<span class="token string">yes</span>' { [ <span class="token operator">=></span> ]
										'<span class="token string">expression</span>': component <a href="#grammar-rule--derived-reference-constraint-expression">'derived reference constraint expression'</a>
										'<span class="token string">output parameters</span>': component <a href="#grammar-rule--output-parameters-definition">'output parameters definition'</a>
										'<span class="token string">value provision</span>': indent [ <span class="token operator">=</span> ] stategroup (
											'<span class="token string">key</span>' { [ <span class="token operator">$</span> ] }
											'<span class="token string">expression</span>' {
												'<span class="token string">expression</span>': component <a href="#grammar-rule--singular-reference-expression">'singular reference expression'</a>
											}
										)
									}
								)
							}
						)
						'<span class="token string">value type</span>': stategroup (
							'<span class="token string">link</span>' { [ <span class="token operator">~></span> ]
								'<span class="token string">selection</span>': component <a href="#grammar-rule--link-text-expression">'link text expression'</a>
							}
							'<span class="token string">simple</span>' { }
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-text-property">'ui text property'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">elementary</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">expression</span>': component <a href="#grammar-rule--state-expression">'state expression'</a>
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-state-group-property">'ui state group property'</a>
						'<span class="token string">output parameters</span>': @list indent dictionary { @block [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
							'<span class="token string">type</span>': stategroup (
								'<span class="token string">elementary</span>' { [ <span class="token operator">-></span> ] }
								'<span class="token string">derived</span>' { [ <span class="token operator">=></span> ] }
							)
							'<span class="token string">node selection</span>': component <a href="#grammar-rule--node-type-id">'node type id'</a>
						}
						'<span class="token string">first state</span>': reference = first
						'<span class="token string">states</span>': @raw [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary @order: .'<span class="token string">view order</span>' { @block
							'<span class="token string">has successor</span>': stategroup = match successor (
								| some = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
								| none = '<span class="token string">no</span>'
							)
							'<span class="token string">record lifetime</span>': stategroup (
								'<span class="token string">yes</span>' { [ <span class="token operator">life-time</span> ]
									'<span class="token string">meta property</span>': [ <span class="token operator">=</span> <span class="token operator">#</span> ] reference
									'<span class="token string">creation timestamp</span>': [ <span class="token operator">from</span> ] reference
								}
								'<span class="token string">no</span>' { }
							)
							'<span class="token string">input parameters</span>': @list indent dictionary { @block [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">node</span>' {
										'<span class="token string">type</span>': stategroup (
											'<span class="token string">elementary</span>' { [ <span class="token operator">-></span> ]
												'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-state-group-selection-starting-from-property">'resolved state group selection starting from property'</a>
												'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
												'<span class="token string">tail</span>': component <a href="#grammar-rule--node-content-path">'node content path'</a>
											}
											'<span class="token string">derived</span>' { [ <span class="token operator">:</span> ]
												'<span class="token string">node selection</span>': component <a href="#grammar-rule--node-type-id">'node type id'</a>
											}
										)
									}
									'<span class="token string">number</span>' {
										'<span class="token string">set</span>': [ <span class="token operator">:</span> ] stategroup (
											'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
											'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
										)
										'<span class="token string">numerical type</span>': reference
									}
								)
							}
							'<span class="token string">output arguments</span>': [ <span class="token operator">-></span> ] dictionary { @block [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
								'<span class="token string">type</span>': stategroup (
									'<span class="token string">elementary</span>' { [ <span class="token operator">-></span> ]
										'<span class="token string">type</span>': stategroup (
											'<span class="token string">descendant</span>' {
												'<span class="token string">type</span>': stategroup (
													'<span class="token string">input parameter</span>' { [ <span class="token operator">&</span> ]
														'<span class="token string">input parameter</span>': reference
													}
													'<span class="token string">this</span>' { }
												)
												'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-node-descendant-selection-starting-from-node">'resolved node descendant selection starting from node'</a>
											}
											'<span class="token string">ancestor</span>' { [ <span class="token operator">^</span> ]
												'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-node-selection-starting-from-property">'resolved node selection starting from property'</a>
											}
										)
									}
									'<span class="token string">derived</span>' { [ <span class="token operator">=></span> ]
										'<span class="token string">type</span>': stategroup (
											'<span class="token string">descendant</span>' {
												'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
											}
											'<span class="token string">ancestor</span>' { [ <span class="token operator">^</span> ]
												'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
											}
										)
									}
								)
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
## Constraints
---
The `application` language supports two types of constraints on data: *reference constraints* and *graph constraints*.

___Reference constraints___ ensure that text properties hold a key value that uniquely identifies an item in a single specific `collection`.
This ensures that derived value computations and command invocations can safely use references.
In the GUI, reference constraints translate to a select list from which the application user has to choose an item.

Reference constraint expressions exist in two different flavours:
(1) `backward` reference expressions that use earlier defined attributes and (2)
`forward` reference expressions that freely use earlier and later defined attributes.
We recommend limiting the use of `forward` references, as their use in computations is restricted for ensuring terminating computations.

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
      // a (bidirectional) backward reference:
    'Product': text -> ^ .'Products' -<'Orders'
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
         // a 'backward' (self) reference that partakes in a graph:
        'Product': text -> ^ graph 'assembly' // reference to a 'Products' item in the assembly graph
        'Part Price': integer 'euro' = >'Product'#'Product Price'
    }
    'Product Price': integer 'euro' = sum .'Parts'#'Part Price' // recursion!
}
```

{: #grammar-rule--reference-inversion }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference inversion</span>' {
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

{: #grammar-rule--reference-constraint-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference constraint expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">backward</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">simple</span>' {
					'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-collection-selection-starting-from-property">'resolved collection selection starting from property'</a>
				}
				'<span class="token string">graph edge</span>' {
					'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
					'<span class="token string">graph</span>': [ <span class="token operator">graph</span> ] reference
				}
			)
		}
		'<span class="token string">forward</span>' { [ <span class="token operator">forward</span> ]
			'<span class="token string">head</span>': component <a href="#grammar-rule--unresolved-node-selection">'unresolved node selection'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--node-content-path">'node content path'</a>
	'<span class="token string">inversion</span>': component <a href="#grammar-rule--reference-inversion">'reference inversion'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--derived-reference-constraint-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">derived reference constraint expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">backward</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-collection-selection-starting-from-property">'calculated collection selection starting from property'</a>
		}
		'<span class="token string">self</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.self</span> ] stategroup (
				'<span class="token string">collection</span>' { }
			)
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
	'<span class="token string">inversion</span>': component <a href="#grammar-rule--reference-inversion">'reference inversion'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--graph-constraints-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">graph constraints definition</span>' {
	'<span class="token string">constraints</span>': dictionary { @block indent
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">acyclic</span>' { [ <span class="token operator">acyclic-graph</span> ] }
			'<span class="token string">linear</span>' { [ <span class="token operator">ordered-graph</span> ] }
		)
	}
}
</pre>
</div>
</div>
## Links
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
    'Product': text ~> ^ +'Catalog' .'Products'
}
```

{: #grammar-rule--link-text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">link text expression</span>' {
	'<span class="token string">dependency</span>': stategroup (
		'<span class="token string">link</span>' {
			'<span class="token string">text path</span>': component <a href="#grammar-rule--calculated-text-selection-starting-from-property">'calculated text selection starting from property'</a>
			'<span class="token string">text value type is link</span>': stategroup (
				'<span class="token string">yes</span>' { }
			)
			'<span class="token string">group selection</span>': component <a href="#grammar-rule--group-node-selection">'group node selection'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">collection selection</span>': component <a href="#grammar-rule--calculated-collection-selection-starting-from-property">'calculated collection selection starting from property'</a>
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
	'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
	'<span class="token string">inversion</span>': component <a href="#grammar-rule--reference-inversion">'reference inversion'</a>
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
'Address label':= text
    = +'Address'.'Street' " " +'Address'.'Street number' // "Huntington Rd 12B"
```

{: #grammar-rule--text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">singular</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--text-expression-tail">'text expression tail'</a>
		}
		'<span class="token string">conditional</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group selection</span>': component <a href="#grammar-rule--calculated-state-group-selection-starting-from-property">'calculated state group selection starting from property'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-text-expression">'conditional text expression'</a>
			}
		}
		'<span class="token string">boolean</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">true</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression-tail">'text expression tail'</a>
				'<span class="token string">false</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--text-expression-tail">'text expression tail'</a>
			}
		}
	)
	'<span class="token string">has successor</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--text-expression">'text expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--text-expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">text expression tail</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">value</span>' {
			'<span class="token string">value</span>': text
		}
		'<span class="token string">text</span>' {
			'<span class="token string">context</span>': stategroup (
				'<span class="token string">this</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--calculated-text-selection-starting-from-property">'calculated text selection starting from property'</a>
				}
				'<span class="token string">variable</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--variable-descendant-node-path">'variable descendant node path'</a>
					'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional text expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--text-expression-tail">'text expression tail'</a>
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-calculated-state-group-path">'variablized calculated state group path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-text-expression">'conditional text expression'</a>
			}
		}
	)
}
</pre>
</div>
</div>
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
    'Manufacturer': text -> ^ .'Manufacturers'
}
'Orders': collection ['ID'] {
    'ID': text
    'Product': text -> ^ .'Products' ( 'Manufacturer' => >'Manufacturer' )
    'Manufacturer':= text => ^ .'Manufacturers' = >'Product'$'Manufacturer'
}
```

{: #grammar-rule--singular-reference-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular reference expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">branch</span>' // branch of derived collection constructed using flatten expressions
		{
			'<span class="token string">branch</span>': [ <span class="token operator">from</span> ] reference
			'<span class="token string">expression</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
		}
		'<span class="token string">singular</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
		}
	)
}
</pre>
</div>
</div>
### Derived files
An example of a derived file property `Contract`.
The property holds the value of a `Default Contract` in case of a `Standard` `Agreement`, and a `Custom` `Contract` in case of a `Custom` `Agreement`:
> ```js
'Default Contract': file
'Agreement': stategroup (
    'Standard' -> { }
    'Custom' -> {
        'Contract': file
    }
)
'Contract':= file = switch ?'Agreement' (
    |'Default' = /'Default Contract'
    |'Custom' = $ /'Contract'
)
```

{: #grammar-rule--file-expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">file expression tail</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">file</span>' {
					'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
					'<span class="token string">file</span>': [ <span class="token operator">/</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
					'<span class="token string">file</span>': [ <span class="token operator">/</span> ] reference
				}
			)
		}
		'<span class="token string">variable</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--variable-descendant-node-path">'variable descendant node path'</a>
			'<span class="token string">file</span>': [ <span class="token operator">/</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-file-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional file expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--file-expression-tail">'file expression tail'</a>
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-calculated-state-group-path">'variablized calculated state group path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-file-expression">'conditional file expression'</a>
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--file-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">file expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">singular</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--file-expression-tail">'file expression tail'</a>
		}
		'<span class="token string">conditional</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group selection</span>': component <a href="#grammar-rule--calculated-state-group-selection-starting-from-property">'calculated state group selection starting from property'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-file-expression">'conditional file expression'</a>
			}
		}
		'<span class="token string">boolean</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">true</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--file-expression-tail">'file expression tail'</a>
				'<span class="token string">false</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--file-expression-tail">'file expression tail'</a>
			}
		}
	)
}
</pre>
</div>
</div>
### Derived numbers
Examples of derived number properties, including required conversion rules:

> ```js
root {
    'Tax Percentage': natural 'percent'
    'Products': collection ['Name'] {
        'Name': text
        'Price': integer 'eurocent'
        'Price (euro)':= integer 'euro' = from 'eurocent' #'Price'
        'Order Unit Quantity': natural 'items per unit'
        'Orders': reference-set -> .'Orders' = inverse >'Product'
        'Sales Value':= integer 'eurocent' = sum <'Orders'#'Price'
        'Items Sold':= integer 'items' = count <'Orders'
    }
    'Total Sales Value':= integer 'eurocent' = sum .'Products'#'Sales Value'
    'Number of Products':= integer 'items' = count .'Products'
    'Orders': collection ['ID'] {
        'ID': text
        'Product': text -> ^ .'Products' -<'Orders'
        'Quantity': natural 'items'
        'Loss':= integer 'items' = remainder ( #'Quantity' as 'items', >'Product' #'Order Unit Quantity' )
        'Price':= integer 'eurocent' = product ( >'Product'#'Price' as 'eurocent' , #'Quantity' )
        'Order Units':= natural 'units' = division ceil ( #'Quantity' as 'items' , >'Product'#'Order Unit Quantity' )
        'Tax': integer 'eurocent'
        'Gross Price':= integer 'eurocent' = sum ( #'Price', #'Tax' )
        'Creation Time': integer 'date and time'
        'Estimated Lead Time': integer 'seconds'
        'Estimated Delivery Time':= integer 'date and time' = add ( #'Creation Time', #'Estimated Lead Time' )
        'Delivered': stategroup (
            'No' -> { }
            'Yes' -> {
                'Delivery Time': natural 'date and time'
                'Lead Time':= integer 'seconds' = diff ( #'Delivery Time', ^ # 'Creation Time' )
            }
        )
    }
    'Gross Income':= integer 'eurocent' = sum .'Orders'#'Gross Price'
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


{: #grammar-rule--integer-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">integer expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">singular</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">value</span>' { [ <span class="token operator">deprecated</span> ]
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">expression</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
				}
			)
		}
		'<span class="token string">conditional</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group selection</span>': component <a href="#grammar-rule--calculated-state-group-selection-starting-from-property">'calculated state group selection starting from property'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-number-expression">'conditional number expression'</a>
			}
		}
		'<span class="token string">boolean</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">true</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
				'<span class="token string">false</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
			}
		}
		'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ]
			'<span class="token string">set path</span>': component <a href="#grammar-rule--calculated-set-selection-starting-from-property">'calculated set selection starting from property'</a>
			'<span class="token string">number path</span>': component <a href="#grammar-rule--entity-scoped-number-path">'entity scoped number path'</a>
		}
		'<span class="token string">count</span>' { [ <span class="token operator">count</span> ]
			'<span class="token string">set path</span>': component <a href="#grammar-rule--calculated-set-selection-starting-from-property">'calculated set selection starting from property'</a>
		}
		'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] // NOT SUPPORTED BY TYPE CHECKER
			'<span class="token string">numerator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
			'<span class="token string">numerator conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">denominator set</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">denominator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">denominator conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
			'<span class="token string">rounding</span>': stategroup (
				'<span class="token string">ordinary</span>' { }
				'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
				'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
			)
			'<span class="token string">numerator</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
			'<span class="token string">numerator conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">denominator set</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">denominator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">denominator conversion</span>': [, <span class="token operator">)</span> ] component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">product</span>' { [ <span class="token operator">product</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
			'<span class="token string">left conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">list operation</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
				'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
			)
			'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] @list indent component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
		'<span class="token string">addition</span>' { [ <span class="token operator">add</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">left conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">difference</span>' { [ <span class="token operator">diff</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--natural-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">natural expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">singular</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">value</span>' { [ <span class="token operator">deprecated</span> ]
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">expression</span>' {
					'<span class="token string">selected number type</span>': stategroup (
						'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
						'<span class="token string">natural</span>' { }
					)
					'<span class="token string">expression</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
				}
			)
		}
		'<span class="token string">conditional</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group selection</span>': component <a href="#grammar-rule--calculated-state-group-selection-starting-from-property">'calculated state group selection starting from property'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-natural-number-expression">'conditional natural number expression'</a>
			}
		}
		'<span class="token string">boolean</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">true</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
				'<span class="token string">false</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
			}
		}
		'<span class="token string">remainder</span>' { [ <span class="token operator">remainder</span> <span class="token operator">unsafe</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] // NOT SUPPORTED BY TYPE CHECKER
			'<span class="token string">numerator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
			'<span class="token string">numerator conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">denominator set</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">denominator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">denominator conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
			'<span class="token string">rounding</span>': stategroup (
				'<span class="token string">ordinary</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
				'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> <span class="token operator">unsafe</span> ] }
			)
			'<span class="token string">numerator type</span>': [ <span class="token operator">(</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">numerator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
			'<span class="token string">numerator conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">denominator type</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">denominator</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">denominator conversion</span>': [, <span class="token operator">)</span> ] component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">product</span>' { [ <span class="token operator">product</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left number type</span>': stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">left</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
			'<span class="token string">left conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">right number type</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">right</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">list operation</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
				'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
			)
			'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] @list indent component <a href="#grammar-rule--natural-number-property-list">'natural number property list'</a>
		}
		'<span class="token string">addition</span>' { [ <span class="token operator">add</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left number type</span>': stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">left</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">left conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
			'<span class="token string">right number type</span>': [ <span class="token operator">,</span> ] stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
				'<span class="token string">natural</span>' { }
			)
			'<span class="token string">right</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
		'<span class="token string">difference</span>' { [ <span class="token operator">diff</span> <span class="token operator">unsafe</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">left</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--numerical-type-conversion }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">numerical type conversion</span>' {
	'<span class="token string">conversion</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">conversion</span>': [ <span class="token operator">from</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--numerical-type-conversion2 }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">numerical type conversion2</span>' {
	'<span class="token string">conversion</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">conversion</span>': [ <span class="token operator">from</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--sign-inversion }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">sign inversion</span>' {
	'<span class="token string">sign inversion</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">-</span> ] }
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-signed-number-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated signed number selection starting from property</span>' {
	'<span class="token string">sign inversion</span>': component <a href="#grammar-rule--sign-inversion">'sign inversion'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">input parameter</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
			'<span class="token string">input parameter</span>': [ <span class="token operator">&#</span> ] reference
		}
		'<span class="token string">number from property</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
		'<span class="token string">number from node</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--signed-number-property-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signed number property list</span>' {
	'<span class="token string">selection</span>': @block component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
	'<span class="token string">conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
	'<span class="token string">has element</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': @block component <a href="#grammar-rule--signed-number-property-list">'signed number property list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--natural-number-property-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">natural number property list</span>' {
	'<span class="token string">selected number type</span>': @block stategroup (
		'<span class="token string">natural</span>' { }
		'<span class="token string">integer</span>' { [ <span class="token operator">unsafe</span> ] }
	)
	'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
	'<span class="token string">conversion</span>': component <a href="#grammar-rule--numerical-type-conversion">'numerical type conversion'</a>
	'<span class="token string">has element</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': @block component <a href="#grammar-rule--natural-number-property-list">'natural number property list'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--number-expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression tail</span>' {
	'<span class="token string">conversion</span>': component <a href="#grammar-rule--numerical-type-conversion2">'numerical type conversion2'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">variable</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">static</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
		}
		'<span class="token string">property</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-calculated-number-path">'variablized calculated number path'</a>
		}
		'<span class="token string">aggregate</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">property</span>' {
					'<span class="token string">operation</span>': stategroup (
						'<span class="token string">minimum</span>' { [ <span class="token operator">min</span> ] }
						'<span class="token string">maximum</span>' { [ <span class="token operator">max</span> ] }
						'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
						'<span class="token string">standard deviation</span>' { [ <span class="token operator">std</span> ] }
					)
					'<span class="token string">path</span>': [ <span class="token operator">$</span> ] component <a href="#grammar-rule--entity-scoped-number-path">'entity scoped number path'</a>
				}
				'<span class="token string">count</span>' { [ <span class="token operator">count</span> <span class="token operator">$</span> ] }
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional number expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-calculated-state-group-path">'variablized calculated state group path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-number-expression">'conditional number expression'</a>
			}
		}
	)
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

{: #grammar-rule--conditional-natural-number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional natural number expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-calculated-state-group-path">'variablized calculated state group path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-natural-number-expression">'conditional natural number expression'</a>
			}
		}
	)
}
</pre>
</div>
</div>
### Derived states
The code sample exemplifies a derived state group property `Product found`.
The expression for deriving the state checks if the `Product` link produces a `Products` item from a `Products` `Catalog`.
This `Catalog` is provided by an external system, via an Alan `interface`: the `Catalog Provider`.
> ```js
'Catalog': group { can-update: interface 'Catalog Provider'
    'Products': collection ['Name'] {
        'Name': text
        'Price': integer 'eurocent'
    }
}
'Orders': collection ['ID'] {
    'ID': text
    // a link to a 'Products' item from the catalog provider:
    'Product': text ~> ^ .'Products'
    'Product found':= stategroup = any >'Product' (
        | true  = 'Yes' ( 'Product' => $ )
        | false = 'No'
    ) (
        'Yes' ( 'Product': +'Catalog'.'Products' ) -> {
            'Price': integer 'eurocent' = &'Product'#'Price'
        }
        'No' -> { }
    )
}
```

{: #grammar-rule--state-instantiation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state instantiation</span>' {
	'<span class="token string">state</span>': reference
	'<span class="token string">input arguments</span>': @list indent dictionary { @block [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">node</span>' { [ <span class="token operator">=></span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">this</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
					}
					'<span class="token string">variable</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--variable-descendant-node-path">'variable descendant node path'</a>
					}
				)
			}
			'<span class="token string">number</span>' {
				'<span class="token string">set</span>': [ <span class="token operator">:</span> ] stategroup (
					'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
					'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
				)
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--number-expression-tail">'number expression tail'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--state-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state expression</span>' {
	'<span class="token string">expression type</span>': stategroup (
		'<span class="token string">branch match</span>' { [ <span class="token operator">match-branch</span> ]
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">state instantiation</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--state-instantiation">'state instantiation'</a>
			}
		}
		'<span class="token string">state merge</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group selection</span>': component <a href="#grammar-rule--calculated-state-group-selection-starting-from-property">'calculated state group selection starting from property'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-state-group-expression">'conditional state group expression'</a>
			}
		}
		'<span class="token string">boolean</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--boolean-expression">'boolean expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">true</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--state-instantiation">'state instantiation'</a>
				'<span class="token string">false</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--state-instantiation">'state instantiation'</a>
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--boolean-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">boolean expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">any</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">any linked node</span>' { [ <span class="token operator">any</span> ]
					'<span class="token string">link context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">any key</span>' { [ <span class="token operator">any</span> ]
					'<span class="token string">collection selection</span>': component <a href="#grammar-rule--calculated-collection-selection-starting-from-property">'calculated collection selection starting from property'</a>
					'<span class="token string">key path</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				}
				'<span class="token string">any in set</span>' { [ <span class="token operator">any</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--calculated-set-selection-starting-from-property">'calculated set selection starting from property'</a>
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				}
			)
		}
		'<span class="token string">node equality</span>' { [ <span class="token operator">match</span> ]
			'<span class="token string">left node type</span>': stategroup (
				'<span class="token string">ancestor</span>' {
					'<span class="token string">selection</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
				}
				'<span class="token string">sibling</span>' {
					'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
				}
			)
			'<span class="token string">right node</span>': [ <span class="token operator">==</span> ] component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
		}
		'<span class="token string">numerical</span>' { [ <span class="token operator">match</span> ]
			'<span class="token string">left expression</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
			'<span class="token string">operator</span>': stategroup (
				'<span class="token string">equal to</span>' { [ <span class="token operator">==</span> ] }
				'<span class="token string">greater than</span>' { [ <span class="token operator">></span>@trim-none ] }
				'<span class="token string">greater than or equal to</span>' { [ <span class="token operator">>=</span> ] }
				'<span class="token string">smaller than</span>' { [ <span class="token operator"><</span>@trim-none ] }
				'<span class="token string">smaller than or equal to</span>' { [ <span class="token operator"><=</span> ] }
			)
			'<span class="token string">right type</span>': stategroup (
				'<span class="token string">value</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
				}
				'<span class="token string">expression</span>' {
					'<span class="token string">right conversion</span>': component <a href="#grammar-rule--numerical-type-conversion2">'numerical type conversion2'</a>
					'<span class="token string">right expression</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
				}
			)
			'<span class="token string">left to variable assignment</span>': component <a href="#grammar-rule--number-variable-assignment">'number variable assignment'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--conditional-state-group-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional state group expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">state instantiation</span>': component <a href="#grammar-rule--state-instantiation">'state instantiation'</a>
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--variablized-calculated-state-group-path">'variablized calculated state group path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--conditional-state-group-expression">'conditional state group expression'</a>
			}
		}
	)
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
	'<span class="token string">head</span>': component <a href="#grammar-rule--group-context-property-selection">'group context property selection'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">prefiltered</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
		}
		'<span class="token string">plural</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
	)
	'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--flatten-expression-tail">'flatten expression tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--flatten-expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">flatten expression tail</span>' {
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
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--flatten-expression-tail">'flatten expression tail'</a>
		}
	)
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
		'<span class="token string">augment</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-collection-selection-starting-from-property">'calculated collection selection starting from property'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
		}
		'<span class="token string">merge</span>' { [ <span class="token operator">union</span> ]
			'<span class="token string">aggregates</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
				'<span class="token string">aggregate</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--referencer-aggregate">'referencer aggregate'</a>
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--referencer-aggregate }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">referencer aggregate</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--group-context-property-selection">'group context property selection'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">prefiltered</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
					'<span class="token string">group</span>': reference
				}
				'<span class="token string">state</span>' { [ <span class="token operator">?</span> ]
					'<span class="token string">state group</span>': reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--referencer-aggregate-step">'referencer aggregate step'</a>
		}
		'<span class="token string">plural</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--referencer-aggregate-step">'referencer aggregate step'</a>
		}
		'<span class="token string">singular</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--referencer-aggregate-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">referencer aggregate step</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
		}
		'<span class="token string">yes</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--referencer-aggregate-step">'referencer aggregate step'</a>
		}
	)
}
</pre>
</div>
</div>
## Permissions and Todos
---

Examples for permissions and todos:

> ```js
'Users': collection ['ID']
    can-create: user ?'Type'|'Admin'
    can-delete: user ?'Type'|'Admin'
{ can-update: user ?'Type'|'Admin'
    'ID': text
    'Address': group { can-update: equal ( /*this*/ , user )
        'Street': text
        'City': text
    }
    'Type': stategroup (
        'Admin' -> { }
        'Employee' -> { }
        'Unknown' -> { has-todo: user ?'Type'|'Admin' }
    )
}
// only team members can read team information:
'Teams': collection ['Name'] { can-read: any .'Members' [ user ]
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
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">existence</span>' { [ <span class="token operator">any</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
			'<span class="token string">has filter</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' {
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
					'<span class="token string">path</span>': [ <span class="token operator">where</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--user-requirement">'user requirement'</a>
				}
			)
		}
		'<span class="token string">equality</span>' {
			'<span class="token string">left path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
			'<span class="token string">right path</span>': [ <span class="token operator">==</span> ] component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
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
'Place Order': command { 'Product': text -> .'Products' }
    external from 'Manufacturer'
'Orders': collection ['ID'] {
    'ID': text
    'Product': text -> ^ .'Products'
    'Creation Time': integer 'date and time' = creation-time
    'Status': stategroup (
        'New' -> {
            'Order from Manufacturer': command { }
                do on ^ ^ (
                    'Place Order' with ( 'Product': text = ^ .'Product' )
                ) and do on ^ (
                    'Status': stategroup = 'Waiting for Manufacturer' ( )
                )
        }
        'Delivered' -> { }
        'Delayed' -> { }
        'Waiting for Manufacturer' -> {
            'Agreed Upon Delivery Time': integer 'date and time'
                timer ontimeout do on ^ (
                    'Status': stategroup = 'Delayed' ( )
                )
        }
    )
}
// for external system 'Delivery Service':
'Register Delivery': command { 'Order': text -> .'Orders' }
    do on @ >'Order' (
        'Status': stategroup = 'Delivered' ( )
    )
```

{: #grammar-rule--command-implementation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command implementation</span>' { [ <span class="token operator">do</span> ]
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">conditional</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">parameter</span>' {
							'<span class="token string">path</span>': group {
								'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
								'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
							}
							'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
								'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
							}
						}
						'<span class="token string">property</span>' {
							'<span class="token string">path</span>': group {
								'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
								'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
							}
							'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
								'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
								'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
							}
						}
					)
				}
				'<span class="token string">existence</span>' { [ <span class="token operator">any</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
						'<span class="token string">true case</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> ] group {
							'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
							'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
						}
						'<span class="token string">false case</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> ] group {
							'<span class="token string">implementation</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
						}
					}
				}
			)
		}
		'<span class="token string">map</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				}
			)
			'<span class="token string">implementation</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] @block indent component <a href="#grammar-rule--command-implementation">'command implementation'</a>
		}
		'<span class="token string">update</span>' {
			'<span class="token string">update node</span>': component <a href="#grammar-rule--parametrized-update-node">'parametrized update node'</a>
		}
		'<span class="token string">ignore</span>' { [ <span class="token operator">ignore</span> ] }
	)
	'<span class="token string">has more statements</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">and</span> ]
			'<span class="token string">statement</span>': component <a href="#grammar-rule--command-implementation">'command implementation'</a>
		}
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
		'<span class="token string">has predecessor</span>': stategroup = match predecessor (
			| some = '<span class="token string">yes</span>' { '<span class="token string">property</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
				'<span class="token string">key constraint</span>': stategroup (
					'<span class="token string">yes</span>' { }
				)
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
			'<span class="token string">number</span>' {
				'<span class="token string">set</span>': stategroup (
					'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
					'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
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
					'<span class="token string">has successor</span>': stategroup = match successor (
						| some = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">constraints</span>': @list indent dictionary { @block [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
						'<span class="token string">expression</span>': component <a href="#grammar-rule--parameter-state-constraint-expression">'parameter state constraint expression'</a>
					}
					'<span class="token string">parameters</span>': @raw component <a href="#grammar-rule--parameter-definition">'parameter definition'</a>
				}
			}
		)
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

{: #grammar-rule--parametrized-update-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized update node</span>' {
	'<span class="token string">context node path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
	'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
	'<span class="token string">attributes</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">command</span>' {
				'<span class="token string">arguments</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--argument-definition">'argument definition'</a>
			}
			'<span class="token string">property</span>' { [ <span class="token operator">:</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">operation</span>': stategroup (
							'<span class="token string">create</span>' { [ <span class="token operator">create</span> ]
								'<span class="token string">initialize node</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
							}
							'<span class="token string">delete</span>' { [ <span class="token operator">delete</span> ]
								'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
								'<span class="token string">delete node</span>': component <a href="#grammar-rule--delete-node">'delete node'</a>
							}
						)
					}
					'<span class="token string">number</span>' {
						'<span class="token string">set</span>': stategroup (
							'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
							'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
						)
						'<span class="token string">operator</span>': stategroup (
							'<span class="token string">increment</span>' { [ <span class="token operator">increment</span> ] }
							'<span class="token string">assignment</span>' {
								'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
							}
						)
					}
					'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-text-expression">'parametrized text expression'</a>
					}
					'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-file-expression">'parametrized file expression'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-expression">'parametrized state expression'</a>
					}
				)
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-initialize-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized initialize node</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent
	'<span class="token string">groups</span>': dictionary { @block
		'<span class="token string">initialize node</span>': [ <span class="token operator">:</span> <span class="token operator">group</span> ] component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
	}
	'<span class="token string">texts</span>': dictionary { @block
		'<span class="token string">expression</span>': [ <span class="token operator">:</span> <span class="token operator">text</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-text-expression">'parametrized text expression'</a>
	}
	'<span class="token string">files</span>': dictionary { @block
		'<span class="token string">expression</span>': [ <span class="token operator">:</span> <span class="token operator">file</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-file-expression">'parametrized file expression'</a>
	}
	'<span class="token string">collections</span>': dictionary { @block
		'<span class="token string">expression</span>': [ <span class="token operator">:</span> <span class="token operator">collection</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-collection-expression">'parametrized collection expression'</a>
	}
	'<span class="token string">numbers</span>': dictionary { @block
		'<span class="token string">set</span>': stategroup (
			'<span class="token string">integer</span>' { [ <span class="token operator">:</span> <span class="token operator">integer</span> ] }
			'<span class="token string">natural</span>' { [ <span class="token operator">:</span> <span class="token operator">natural</span> ] }
		)
		'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
	}
	'<span class="token string">state groups</span>': dictionary { @block
		'<span class="token string">expression</span>': [ <span class="token operator">:</span> <span class="token operator">stategroup</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-expression">'parametrized state expression'</a>
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
	'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
	'<span class="token string">tail</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--argument-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">argument definition</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent
	'<span class="token string">properties</span>': dictionary { @block
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
				'<span class="token string">key constraint</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">=></span> ]
						'<span class="token string">expression</span>': component <a href="#grammar-rule--parametrized-collection-argument-expression">'parametrized collection argument expression'</a>
					}
				)
			}
			'<span class="token string">number</span>' {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
					'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
				)
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
			}
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-text-expression">'parametrized text expression'</a>
			}
			'<span class="token string">file</span>' { [ <span class="token operator">file</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-file-expression">'parametrized file expression'</a>
			}
			'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-argument-expression">'parametrized state argument expression'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-state-constraint-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter state constraint expression</span>' {
	'<span class="token string">path</span>': [ <span class="token operator">-></span> ] component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--parameter-entity-scoped-context-node-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameter entity scoped context node selection</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">key reference</span>' { [ <span class="token operator">></span> ]
					'<span class="token string">text</span>': reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-entity-scoped-context-node-selection">'parameter entity scoped context node selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-text-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized text expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-text-expression">'parametrized text expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-text-expression">'parametrized text expression'</a>
					}
				}
			)
		}
		'<span class="token string">parameter</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">property</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-file-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized file expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-file-expression">'parametrized file expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-file-expression">'parametrized file expression'</a>
					}
				}
			)
		}
		'<span class="token string">parameter</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
			'<span class="token string">file</span>': [ <span class="token operator">/</span> ] reference
		}
		'<span class="token string">property</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">file</span>': [ <span class="token operator">/</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized number expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">binary expression</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">difference</span>' { [ <span class="token operator">diff</span> ] }
				'<span class="token string">division</span>' { [ <span class="token operator">division</span> ]
					'<span class="token string">rounding</span>': stategroup (
						'<span class="token string">ordinary</span>' { }
						'<span class="token string">ceil</span>' { [ <span class="token operator">ceil</span> ] }
						'<span class="token string">floor</span>' { [ <span class="token operator">floor</span> ] }
					)
				}
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
				'<span class="token string">min</span>' { [ <span class="token operator">min</span> ] }
				'<span class="token string">max</span>' { [ <span class="token operator">max</span> ] }
			)
			'<span class="token string">expressions</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
				'<span class="token string">left</span>': component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
				'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
			}
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
					}
				}
			)
		}
		'<span class="token string">unary expression</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">natural to integer cast</span>' { [ <span class="token operator">(</span> <span class="token operator">integer</span> <span class="token operator">)</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--parametrized-number-expression">'parametrized number expression'</a>
				}
			)
		}
		'<span class="token string">property</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
		'<span class="token string">parameter</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
		'<span class="token string">current timestamp</span>' { [ <span class="token operator">now</span> ] }
		'<span class="token string">static</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--static-number-value">'static number value'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-state-argument-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized state argument expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-argument-expression">'parametrized state argument expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-argument-expression">'parametrized state argument expression'</a>
					}
				}
			)
		}
		'<span class="token string">static</span>' {
			'<span class="token string">state</span>': reference
			'<span class="token string">arguments</span>': component <a href="#grammar-rule--argument-definition">'argument definition'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-state-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized state expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-expression">'parametrized state expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-state-expression">'parametrized state expression'</a>
					}
				}
			)
		}
		'<span class="token string">static</span>' {
			'<span class="token string">state</span>': reference
			'<span class="token string">initialize node</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-collection-filter-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized collection filter path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--node-step">'node step'</a>
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--parametrized-collection-filter-path">'parametrized collection filter path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-collection-argument-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized collection argument expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">empty</span>' { }
		'<span class="token string">entry</span>' {
			'<span class="token string">arguments</span>': component <a href="#grammar-rule--argument-definition">'argument definition'</a>
		}
		'<span class="token string">parameter</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">filter</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
			'<span class="token string">context selection</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--parameter-entity-scoped-context-node-selection">'parameter entity scoped context node selection'</a>
			'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
			'<span class="token string">arguments</span>': [ <span class="token operator">)</span> ] component <a href="#grammar-rule--argument-definition">'argument definition'</a>
		}
		'<span class="token string">property</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
			'<span class="token string">filter</span>': component <a href="#grammar-rule--parametrized-collection-filter-path">'parametrized collection filter path'</a>
			'<span class="token string">context selection</span>': [ <span class="token operator">(</span> ] component <a href="#grammar-rule--parameter-entity-scoped-context-node-selection">'parameter entity scoped context node selection'</a>
			'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
			'<span class="token string">arguments</span>': [ <span class="token operator">)</span> ] component <a href="#grammar-rule--argument-definition">'argument definition'</a>
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-collection-argument-expression">'parametrized collection argument expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-collection-argument-expression">'parametrized collection argument expression'</a>
					}
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--parametrized-collection-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parametrized collection expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">empty</span>' { }
		'<span class="token string">entry</span>' { [ <span class="token operator">create</span> ]
			'<span class="token string">initialize node</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
		}
		'<span class="token string">parameter</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">filter</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
			'<span class="token string">key property</span>': [ <span class="token operator">(</span> <span class="token operator">[</span>, <span class="token operator">]</span> <span class="token operator">)</span> ] reference
			'<span class="token string">initialize node</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
		}
		'<span class="token string">property</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
			'<span class="token string">filter</span>': component <a href="#grammar-rule--parametrized-collection-filter-path">'parametrized collection filter path'</a>
			'<span class="token string">key property</span>': [ <span class="token operator">(</span> <span class="token operator">[</span>, <span class="token operator">]</span> <span class="token operator">)</span> ] reference
			'<span class="token string">initialize node</span>': component <a href="#grammar-rule--parametrized-initialize-node">'parametrized initialize node'</a>
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-collection-expression">'parametrized collection expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--parametrized-collection-expression">'parametrized collection expression'</a>
					}
				}
			)
		}
	)
}
</pre>
</div>
</div>
## Node type identification
---

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
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-type-id-path">'node type id path'</a>
		}
	)
}
</pre>
</div>
</div>
## Output parameters (legacy)
---
Output parameter definitions are helpers/sub-expressions for navigation expressions.

{: #grammar-rule--output-parameters }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">output parameters</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--output-parameters-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">output parameters definition</span>' {
	'<span class="token string">parameters</span>': component <a href="#grammar-rule--output-parameters">'output parameters'</a>
	'<span class="token string">output parameters</span>': dictionary { @block indent [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">elementary</span>' { [ <span class="token operator">-></span> ]
				'<span class="token string">head</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
				'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-node-descendant-selection-starting-from-node">'resolved node descendant selection starting from node'</a>
			}
			'<span class="token string">derived</span>' { [ <span class="token operator">=></span> ]
				'<span class="token string">head</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
				'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
			}
		)
	}
}
</pre>
</div>
</div>
## Navigation
---
Examples of typical navigation steps:
> ```js
.'My Text'       // select text value
/'My File'       // select file value
#'My Number'     // select number value
.'My Collection' // select collection
?'My StateGroup' // select stategroup
|'My State'      // select/require state
+'My Group'      // select group node
--
>>'My Text'               // go to referenced node (for text with constraint)
>|>'My Text'              // go to referenced node (for text with link)
>>'My Text'$'Output'      // go to reference output node
&'My State ctx'           // go to state context node
?'My Stategroup'$'Output' // go to stategroup output node
--
^                // go to parent node
$^               // go to parent variable context
$                // select variable
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

{: #grammar-rule--entity-scoped-ancestor-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity scoped ancestor node path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
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
		'<span class="token string">this</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
		}
		'<span class="token string">variable</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">variable</span>' { }
			)
		}
		'<span class="token string">parameter</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
			'<span class="token string">reference type</span>': stategroup (
				'<span class="token string">text</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
					'<span class="token string">tail</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
				}
				'<span class="token string">state</span>' { [ <span class="token operator">&</span> ]
					'<span class="token string">constraint</span>': reference
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
		'<span class="token string">output parameter</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">group</span>' { [ <span class="token operator">+</span> ]
			'<span class="token string">group</span>': reference
		}
		'<span class="token string">state group output parameter</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">state context parameter</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&</span> ] reference
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
		}
		'<span class="token string">entry</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">key path</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">node</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">key type</span>': stategroup (
							'<span class="token string">linked</span>' { }
							'<span class="token string">simple</span>' {
								'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
							}
						)
					}
					'<span class="token string">parameter</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
					}
				)
			}
		}
		'<span class="token string">reference</span>' {
			'<span class="token string">reference base</span>': stategroup (
				'<span class="token string">link reference</span>' { [ <span class="token operator">|></span> ] }
				'<span class="token string">referencer reference</span>' { [ <span class="token operator">></span> ] }
			)
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
### Variable assignment and navigation

{: #grammar-rule--optional-variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">optional variable assignment</span>' {
	'<span class="token string">has assignment</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ]
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
'<span class="token string">variable assignment</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--number-variable-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number variable assignment</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ancestor-variable-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor variable path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">yes</span>' { [ <span class="token operator">$^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
		}
	)
}
</pre>
</div>
</div>
### Parameter navigation

{: #grammar-rule--ancestor-parameters-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor parameters path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">@</span> ] }
		'<span class="token string">yes</span>' { [ <span class="token operator">@^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
		}
	)
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
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
		}
	)
}
</pre>
</div>
</div>
### Shared node navigation for constraints & derivations (legacy)

{: #grammar-rule--ancestor-property-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor property path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--entity-scoped-ancestor-property-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity scoped ancestor property path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--group-node-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">group node selection</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--group-node-selection">'group node selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--resolved-node-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">resolved node selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">input parameter</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
					'<span class="token string">input parameter</span>': [ <span class="token operator">&</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--resolved-node-descendant-selection-starting-from-node">'resolved node descendant selection starting from node'</a>
		}
		'<span class="token string">this node</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
					'<span class="token string">tail</span>': component <a href="#grammar-rule--resolved-node-descendant-selection-starting-from-node">'resolved node descendant selection starting from node'</a>
				}
				'<span class="token string">state group output parameter</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
				}
				'<span class="token string">referencer output</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
					'<span class="token string">output type</span>': stategroup (
						'<span class="token string">referenced node</span>' { }
						'<span class="token string">output parameter</span>' {
							'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
						}
					)
				}
			)
		}
	)
}
</pre>
</div>
</div>
### Node navigation for constraints (legacy)

{: #grammar-rule--resolved-state-group-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">resolved state group selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state group</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-node-selection-starting-from-property">'resolved node selection starting from property'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--resolved-collection-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">resolved collection selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">collection</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--resolved-node-selection-starting-from-property">'resolved node selection starting from property'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--resolved-node-descendant-selection-starting-from-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">resolved node descendant selection starting from node</span>' {
	'<span class="token string">group selection</span>': component <a href="#grammar-rule--group-node-selection">'group node selection'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">this node</span>' { }
		'<span class="token string">state group output parameter</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">referencer output</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">is backward</span>': stategroup (
				'<span class="token string">is backward</span>' { }
			)
			'<span class="token string">output type</span>': stategroup (
				'<span class="token string">referenced node</span>' { }
				'<span class="token string">output parameter</span>' {
					'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--node-content-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node content path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-content-path">'node content path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--unresolved-node-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">unresolved node selection</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">this node</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">this</span>' { }
				'<span class="token string">referencer output</span>' {
					'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
				}
			)
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--group-node-selection">'group node selection'</a>
}
</pre>
</div>
</div>
### Node navigation for derivations (legacy)

{: #grammar-rule--derivation-node-content-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">derivation node content path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
				}
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--group-context-property-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">group context property selection</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--group-context-property-selection">'group context property selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-descendant-node-selection-starting-from-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated descendant node selection starting from node</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">this node</span>' { }
		'<span class="token string">group</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
		}
		'<span class="token string">state group output parameter</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">referencer output</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">output type</span>': stategroup (
				'<span class="token string">referenced node</span>' { }
				'<span class="token string">output parameter</span>' {
					'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
				}
			)
		}
		'<span class="token string">state context parameter</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&</span> ] reference
			'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-descendant-node-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated descendant node selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">group</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
		}
		'<span class="token string">state group output parameter</span>' {
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
		}
		'<span class="token string">referencer output</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">output type</span>': stategroup (
				'<span class="token string">referenced node</span>' { }
				'<span class="token string">output parameter</span>' {
					'<span class="token string">output parameter</span>': [ <span class="token operator">$</span> ] reference
				}
			)
		}
		'<span class="token string">state context parameter</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&</span> ] reference
			'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-node-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated node selection starting from property</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
	'<span class="token string">tail</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-property">'calculated descendant node selection starting from property'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--variable-descendant-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable descendant node path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">variable</span>' { }
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--calculated-descendant-node-selection-starting-from-node">'calculated descendant node selection starting from node'</a>
}
</pre>
</div>
</div>
### Property navigation for derivations (legacy)

{: #grammar-rule--calculated-collection-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated collection selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">collection</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-reference-set-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated reference set selection starting from property</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--entity-scoped-ancestor-property-path">'entity scoped ancestor property path'</a>
	'<span class="token string">reference set</span>': [ <span class="token operator"><</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-set-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated set selection starting from property</span>' {
	'<span class="token string">container</span>': stategroup (
		'<span class="token string">collection</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--calculated-collection-selection-starting-from-property">'calculated collection selection starting from property'</a>
		}
		'<span class="token string">reference set</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--calculated-reference-set-selection-starting-from-property">'calculated reference set selection starting from property'</a>
		}
	)
	'<span class="token string">filter</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-state-group-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated state group selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state group</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--calculated-text-selection-starting-from-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">calculated text selection starting from property</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">text</span>' {
			'<span class="token string">context selection</span>': component <a href="#grammar-rule--ancestor-property-path">'ancestor property path'</a>
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
		}
		'<span class="token string">node</span>' {
			'<span class="token string">selection</span>': component <a href="#grammar-rule--calculated-node-selection-starting-from-property">'calculated node selection starting from property'</a>
			'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--variablized-calculated-state-group-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variablized calculated state group path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this</span>' {
			'<span class="token string">state group selection</span>': component <a href="#grammar-rule--calculated-state-group-selection-starting-from-property">'calculated state group selection starting from property'</a>
		}
		'<span class="token string">variable</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--variable-descendant-node-path">'variable descendant node path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--variable-descendant-number-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variable descendant number path</span>' {
	'<span class="token string">sign inversion</span>': component <a href="#grammar-rule--sign-inversion">'sign inversion'</a>
	'<span class="token string">path</span>': component <a href="#grammar-rule--variable-descendant-node-path">'variable descendant node path'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state context parameter</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&#</span> ] reference
		}
		'<span class="token string">property</span>' {
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--entity-scoped-number-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entity scoped number path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--entity-scoped-ancestor-node-path">'entity scoped ancestor node path'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">state context parameter</span>' {
			'<span class="token string">parameter</span>': [ <span class="token operator">&#</span> ] reference
		}
		'<span class="token string">property</span>' {
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--variablized-calculated-number-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variablized calculated number path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--calculated-signed-number-selection-starting-from-property">'calculated signed number selection starting from property'</a>
		}
		'<span class="token string">variable</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--variable-descendant-number-path">'variable descendant number path'</a>
		}
	)
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
'Score': natural 'score' @default: ? 'Default Score' | 'Known' # 'Value'
```

A default value is not necessarily a valid value. If validation
rules or constraints apply, a default value can be invalid.
When a derived value is used, make sure it is not a part of the new
node. Derived values on new nodes are computed after the node is saved,
and will therefore not be included in default values.

The property description would get set to: `Deliver  pieces`.

>```js
'Description': text @default: "Deliver ", to-text . 'To deliver' " pieces."
'To deliver' := integer 'pieces' = sum ^ . 'Order' # 'Amount'
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

{: #grammar-rule--context-node-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context node selection</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">group</span>' {
					'<span class="token string">group</span>': [ <span class="token operator">+</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--context-node-selection">'context node selection'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-identifying-property-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui identifying property selection</span>' {
	'<span class="token string">has properties</span>': stategroup = match .'<span class="token string">properties</span>' (
		| some = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none = '<span class="token string">no</span>'
	)
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary @order: .'<span class="token string">view order</span>' { @block indent
		'<span class="token string">has successor</span>': stategroup = match successor (
			| some = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
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
							'<span class="token string">has successor</span>': stategroup = match successor (
								| some = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
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

{: #grammar-rule--ui-target-node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target node</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ui-target-collection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target collection</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ui-target-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target attribute</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ui-target-parameter-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target parameter definition</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ui-target-parameter }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target parameter</span>' { }
</pre>
</div>
</div>

{: #grammar-rule--ui-target-node-collection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target node collection</span>' {
	'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-node">'ui target node'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--ui-target-parameter-collection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui target parameter collection</span>' {
	'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-parameter-definition">'ui target parameter definition'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--ui-action-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui action expression</span>' {
	'<span class="token string">operation</span>': stategroup (
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
					}
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
						'<span class="token string">stategroup</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
					}
				}
			)
		}
		'<span class="token string">existence</span>' { [ <span class="token operator">any</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent group {
				'<span class="token string">true case</span>': @block [ <span class="token operator">|</span> <span class="token operator">true</span> ] group {
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
				}
				'<span class="token string">false case</span>': @block [ <span class="token operator">|</span> <span class="token operator">false</span> ] group {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
				}
			}
		}
		'<span class="token string">map</span>' { [ <span class="token operator">map</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parameter</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				}
			)
			'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] @block indent component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
		}
		'<span class="token string">ignore</span>' { [ <span class="token operator">ignore</span> ]
			/* target */
		}
		'<span class="token string">select target</span>' {
			'<span class="token string">interactive</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">interactive</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">show target</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">and</span> <span class="token operator">show</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">target</span>': stategroup (
				'<span class="token string">node</span>' {
					'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-node">'ui target node'</a>
				}
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">collection type</span>': component <a href="#grammar-rule--ui-target-node-collection">'ui target node collection'</a>
					'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-collection">'ui target collection'</a>
				}
			)
			'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
		}
		'<span class="token string">target node</span>' {
			'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
				'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-attribute">'ui target attribute'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
			}
		}
		'<span class="token string">target attribute</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">action</span>' { [ <span class="token operator">action</span> ]
					'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-parameter-definition">'ui target parameter definition'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
				}
				'<span class="token string">command</span>' { [ <span class="token operator">command</span> ]
					'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-parameter-definition">'ui target parameter definition'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
				}
				'<span class="token string">property</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
							'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-node">'ui target node'</a>
							'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
						}
						'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
							'<span class="token string">collection type</span>': component <a href="#grammar-rule--ui-target-node-collection">'ui target node collection'</a>
							'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-collection">'ui target collection'</a>
							'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
						}
						'<span class="token string">stategroup</span>' { [ <span class="token operator">state</span> ]
							'<span class="token string">state</span>': reference
							'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-node">'ui target node'</a>
							'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
						}
						'<span class="token string">number</span>' {
							'<span class="token string">set type</span>': stategroup (
								'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
								'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
							)
							'<span class="token string">default</span>': component <a href="#grammar-rule--ui-number-default">'ui number default'</a>
						}
						'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
							'<span class="token string">default</span>': component <a href="#grammar-rule--ui-text-default">'ui text default'</a>
						}
					)
				}
			)
		}
		'<span class="token string">target collection</span>' {
			'<span class="token string">collection type</span>': stategroup (
				'<span class="token string">parameter</span>' { [ <span class="token operator">@</span> <span class="token operator">create</span> ] }
				'<span class="token string">node</span>' { [ <span class="token operator">create</span> ] }
			)
			'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
		}
		'<span class="token string">target parameter definition</span>' { [ <span class="token operator">@</span> ]
			'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
				'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-parameter">'ui target parameter'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
			}
		}
		'<span class="token string">target parameter</span>' { [ <span class="token operator">@</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
					'<span class="token string">collection type</span>': component <a href="#grammar-rule--ui-target-parameter-collection">'ui target parameter collection'</a>
					'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-collection">'ui target collection'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
				}
				'<span class="token string">stategroup</span>' { [ <span class="token operator">state</span> ]
					'<span class="token string">state</span>': reference
					'<span class="token string">target</span>': component <a href="#grammar-rule--ui-target-parameter-definition">'ui target parameter definition'</a>
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
				}
				'<span class="token string">number</span>' {
					'<span class="token string">set type</span>': stategroup (
						'<span class="token string">natural</span>' { [ <span class="token operator">natural</span> ] }
						'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
					)
					'<span class="token string">default</span>': component <a href="#grammar-rule--ui-number-default">'ui number default'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
					'<span class="token string">default</span>': component <a href="#grammar-rule--ui-text-default">'ui text default'</a>
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
'<span class="token string">ui action</span>' {
	'<span class="token string">expression</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--ui-action-expression">'ui action expression'</a>
	'<span class="token string">has more actions</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">and</span> ]
			'<span class="token string">action</span>': component <a href="#grammar-rule--ui-action">'ui action'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-number-default-expression-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number default expression list</span>' {
	'<span class="token string">value</span>': component <a href="#grammar-rule--ui-number-default-expression">'ui number default expression'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ui-number-default-expression-list">'ui number default expression list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-number-default-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number default expression</span>' {
	'<span class="token string">value</span>': stategroup (
		'<span class="token string">today</span>' { [ <span class="token operator">today</span> ] }
		'<span class="token string">now</span>' { [ <span class="token operator">now</span> ] }
		'<span class="token string">one</span>' { [ <span class="token operator">one</span> ] }
		'<span class="token string">zero</span>' { [ <span class="token operator">zero</span> ] }
		'<span class="token string">static integer</span>' { [ <span class="token operator">integer</span> ]
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">static natural</span>' { [ <span class="token operator">natural</span> ]
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">expression</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
			)
			'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent component <a href="#grammar-rule--ui-number-default-expression-list">'ui number default expression list'</a>
		}
		'<span class="token string">parameter</span>' {
			'<span class="token string">path</span>': group {
				'<span class="token string">ancestor</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
				'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
			}
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
		'<span class="token string">property</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--ui-parametrized-node-path">'ui parametrized node path'</a>
			'<span class="token string">number</span>': [ <span class="token operator">#</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-number-default }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number default</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-number-default-expression">'ui number default expression'</a>
	'<span class="token string">has fallback</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">||</span> ] @break? indent
			'<span class="token string">fallback</span>': component <a href="#grammar-rule--ui-number-default">'ui number default'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-text-default-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui text default expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">auto increment</span>' { [ <span class="token operator">auto-increment</span> ] }
		'<span class="token string">static</span>' {
			'<span class="token string">value</span>': text
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">property type</span>': stategroup (
				'<span class="token string">number</span>' { [ <span class="token operator">to-text</span> ]
					'<span class="token string">numerical type</span>': reference
					'<span class="token string">pad</span>': stategroup (
						'<span class="token string">yes</span>' { [ <span class="token operator">pad</span> ]
							'<span class="token string">size</span>': integer
							'<span class="token string">character</span>': [ <span class="token operator">with</span> ] text
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-number-default-expression">'ui number default expression'</a>
				}
				'<span class="token string">text</span>' {
					'<span class="token string">property context</span>': stategroup (
						'<span class="token string">node</span>' {
							'<span class="token string">path</span>': component <a href="#grammar-rule--ui-parametrized-node-path">'ui parametrized node path'</a>
							'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
						}
						'<span class="token string">parameter</span>' {
							'<span class="token string">path</span>': group {
								'<span class="token string">ancestor</span>': component <a href="#grammar-rule--ancestor-parameters-path">'ancestor parameters path'</a>
								'<span class="token string">tail</span>': component <a href="#grammar-rule--parameter-path-tail">'parameter path tail'</a>
							}
							'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
						}
					)
				}
			)
		}
	)
	'<span class="token string">concatenate with</span>': stategroup (
		'<span class="token string">nothing</span>' { }
		'<span class="token string">text</span>' {
			'<span class="token string">expression</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--ui-text-default-expression">'ui text default expression'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-text-default }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui text default</span>' {
	'<span class="token string">value</span>': stategroup (
		'<span class="token string">expression</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-text-default-expression">'ui text default expression'</a>
			'<span class="token string">has fallback</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">||</span> ] @break? indent
					'<span class="token string">fallback</span>': component <a href="#grammar-rule--ui-text-default">'ui text default'</a>
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">current user</span>' { [ <span class="token operator">user</span> ] }
		'<span class="token string">guid</span>' { [ <span class="token operator">guid</span> ] }
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

{: #grammar-rule--ui-file-name-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui file name expression</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">&</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">text</span>': text
				}
				'<span class="token string">property</span>' {
					'<span class="token string">path</span>': component <a href="#grammar-rule--context-node-selection">'context node selection'</a>
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">text</span>' { [ <span class="token operator">.</span> ]
							'<span class="token string">text</span>': reference
						}
						'<span class="token string">number</span>' { [ <span class="token operator">#</span> ]
							'<span class="token string">number</span>': reference
						}
						'<span class="token string">state group</span>' { [ <span class="token operator">?</span> ]
							'<span class="token string">state group</span>': reference
							'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block
								'<span class="token string">state file name expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent component <a href="#grammar-rule--ui-file-name-expression">'ui file name expression'</a>
							}
						}
					)
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ui-file-name-expression">'ui file name expression'</a>
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

{: #grammar-rule--ui-command-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui command attribute</span>' { @list indent
	'<span class="token string">visible</span>': @block stategroup (
		'<span class="token string">true</span>' { [ <span class="token operator">@visible</span> ] }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
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
		'Yes' -> { }
		'No' -> { }
	)
}
'Issues': collection ['Name']  {
	'Name': text
	'Labels': collection ['Name'] @default: > 'Name' ? 'Default' | 'Yes' {
		'Name': text -> ^ ^ . 'Labels'
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
	'Employees': collection ['Name'] @default: > 'Name' { // This has no effect.
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
	'Category':= text = .'Id' ~> ^ .'Imported Categories'
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
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">text</span>' { [ <span class="token operator">.</span> ]
					'<span class="token string">property</span>': reference
				}
				'<span class="token string">number</span>' { [ <span class="token operator">#</span> ]
					'<span class="token string">property</span>': reference
				}
			)
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
		'<span class="token string">large</span>' { }
	)
	'<span class="token string">can be dormant</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@dormant</span> ]
			'<span class="token string">context</span>': component <a href="#grammar-rule--derivation-node-content-path">'derivation node content path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">dormant state</span>': [ <span class="token operator">|</span> ] reference
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
			'<span class="token string">key property</span>': [ <span class="token operator">></span> ] reference
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
			'<span class="token string">context</span>': component <a href="#grammar-rule--ui-node-path">'ui node path'</a>
			'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">select</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">|</span> ] reference
					'<span class="token string">style</span>': component <a href="#grammar-rule--ui-style">'ui style'</a>
				}
				'<span class="token string">switch</span>' {
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">has style</span>': [ <span class="token operator">=</span> ] stategroup (
							'<span class="token string">yes</span>' {
								'<span class="token string">style</span>': component <a href="#grammar-rule--ui-style">'ui style'</a>
							}
							'<span class="token string">no</span>' { [ <span class="token operator">none</span> ] }
						)
					}
				}
			)
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
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-number-default">'ui number default'</a>
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
		'<span class="token string">yes</span>' { [ <span class="token operator">@name</span> ]
			'<span class="token string">file name expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent component <a href="#grammar-rule--ui-file-name-expression">'ui file name expression'</a>
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
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-text-default">'ui text default'</a>
		}
	)
	'<span class="token string">has validation</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@validate:</span> ]
			'<span class="token string">rules</span>': component <a href="#grammar-rule--ui-text-validation">'ui text validation'</a>
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
			'<span class="token string">source</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': reference
				}
				'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--ui-node-path">'ui node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">action</span>': stategroup (
							'<span class="token string">do nothing</span>' { [ <span class="token operator">ignore</span> ] }
							'<span class="token string">set state</span>' {
								'<span class="token string">state</span>': [ <span class="token operator">=</span> ] reference
							}
						)
					}
				}
			)
		}
	)
	'<span class="token string">constraining collection</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@ordered:</span> ]
			'<span class="token string">first entry state</span>': reference
			'<span class="token string">state</span>': [ <span class="token operator">or</span> ] reference
			'<span class="token string">constraining reference</span>': [ <span class="token operator">.</span> ] reference
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
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> <span class="token operator">map</span> ]
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
	'<span class="token string">has validation</span>': @block stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@validate:</span> ]
			'<span class="token string">rules</span>': component <a href="#grammar-rule--ui-text-validation">'ui text validation'</a>
		}
	)
	'<span class="token string">default</span>': @block stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">sticky</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">@sticky</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-text-default">'ui text default'</a>
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
		'<span class="token string">no</span>' {
			'<span class="token string">sticky</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">@sticky</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-number-default">'ui number default'</a>
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
		'<span class="token string">no</span>' {
			'<span class="token string">sticky</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">@sticky</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">source</span>': stategroup (
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': reference
				}
				'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
					'<span class="token string">path</span>': group {
						'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
						'<span class="token string">state group</span>': [ <span class="token operator">?</span> ] reference
					}
					'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] indent dictionary { @block [ <span class="token operator">|</span> ]
						'<span class="token string">action</span>': stategroup (
							'<span class="token string">do nothing</span>' { [ <span class="token operator">ignore</span> ] }
							'<span class="token string">set state</span>' {
								'<span class="token string">state</span>': [ <span class="token operator">=</span> ] reference
							}
						)
					}
				}
			)
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
