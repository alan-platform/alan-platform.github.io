---
layout: "doc"
origin: "model"
language: "application"
version: "union-ext.4"
type: "grammar"
---

1. TOC
{:toc}

## The *minimal model*
---
Every valid Alan model instantiates the [`root` rule](#the-root-rule).
From that rule we can extract a minimal model.
In the `application` language, the minimal model is

```js
users
	anonymous
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

If your application supports a `dynamic` collection of users, you can enable user sign-up and authentication.
Enabling user sign-up means that your application will have a sign-up page for new users.

User authentication can either be application-specific, or it can be done via a single application for single sign-on.
For an application that handles user authentication, you need to specify:
- a collection that holds `Passwords` and some required properties, or
- an `Authorities` collection listing third parties that handle authorization using the OAuth standard (Google, Microsoft, etc.).
For application-specific user authentication, you need to specify which collection and text property holds (hashed) user passwords.
In addition, you have to specify states for the 'active' and 'reset' status of the password.

The following model expresses an application that supports all aforementioned features:
- user sign-up, by providing a `user-initializer`
- password authentication, by specifying a `Passwords` collection and required properties
- third party authentication, by specifying an `Authorities` and `Identities` collection

```js
users
	dynamic: .'Users'
		user-initializer: (
			'Type' = create 'Unknown' ( )
		)

		passwords: .'Passwords'
			password-value: .'Data'.'Password'
			password-status: .'Data'.'Active' (
				| active => 'Yes' ( )
				| reset => 'No' ( )
			)
			password-initializer: (
				'Data' = ( )
			)

		authorities: .'Authorities'
			identities: .'Identities'>'User'
			identity-initializer: ( )

root {
	can-update: user .'Type'?'Admin'

	'Users': collection ['Name'] {
		'Name': text
		'Type': stategroup (
			'Admin' { }
			'Unknown' { }
		)
	}
	'Passwords': collection ['User'] {
		'User': text -> ^ .'Users'[]
		'Data': group {
			can-update: user is ( ^ >'User' )

			'Password': text
			'Active': stategroup (
				'No' { }
				'Yes' { }
			)
		}
	}
	'Authorities': collection ['Authority'] {
		'Authority': text
		'Identities': collection ['Identity'] {
			'Identity': text
			'User': text -> ^ ^ .'Users'[]
		}
	}
}
```

The initializers are for setting initial values for a user, password or identity node.
For example, the `user-initializer` sets the `Type` of users that sign up to `Unknown`.
Thus, users cannot sign up as an `Admin`; `Admin` [permissions](#permissions-and-todos) are required to make a new user `Admin`.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">allow anonymous user</span>': [ <span class="token operator">users</span> ] stategroup (
	'<span class="token string">no</span>' { }
	'<span class="token string">yes</span>' { [ <span class="token operator">anonymous</span> ] }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has dynamic users</span>': stategroup (
	'<span class="token string">no</span>' { }
	'<span class="token string">yes</span>' {
		'<span class="token string">users collection path</span>': [ <span class="token operator">dynamic:</span> ] component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
		'<span class="token string">supports user sign-up</span>': stategroup (
			'<span class="token string">yes</span>' {
				'<span class="token string">user initializer</span>': [ <span class="token operator">user-initializer:</span> ] component <a href="#grammar-rule--user-initializer">'user initializer'</a>
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">has password authentication</span>': stategroup (
			'<span class="token string">yes</span>' {
				'<span class="token string">passwords collection path</span>': [ <span class="token operator">passwords:</span> ] component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
				'<span class="token string">password text path</span>': [ <span class="token operator">password-value:</span> ] component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
				'<span class="token string">password status</span>': [ <span class="token operator">password-status:</span> ] group {
					'<span class="token string">state group path</span>': component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary (
						static '<span class="token string">active</span>' [ <span class="token operator">active</span> ]
						static '<span class="token string">reset</span>' [ <span class="token operator">reset</span> ]
					) { [ <span class="token operator">|</span> ]
						'<span class="token string">state</span>': [ <span class="token operator">=></span> ] reference
						'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
					}
				}
				'<span class="token string">password initializer</span>': [ <span class="token operator">password-initializer:</span> ] component <a href="#grammar-rule--password-initializer">'password initializer'</a>
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">has external authentication</span>': stategroup (
			'<span class="token string">yes</span>' {
				'<span class="token string">authorities path</span>': [ <span class="token operator">authorities:</span> ] component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
				'<span class="token string">identities path</span>': [ <span class="token operator">identities:</span> ] component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
				'<span class="token string">user reference</span>': [ <span class="token operator">></span> ] reference
				'<span class="token string">identity initializer</span>': [ <span class="token operator">identity-initializer:</span> ] component <a href="#grammar-rule--identity-initializer">'identity initializer'</a>
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
For consuming an `interface`, you mention it in the `interfaces` section of your `application` model.
This way, you can reference the `interface` when configuring [permissions](#permissions-and-todos).
The `path` is for specifying on which nodes the `interface` conformant data will be imported at runtime.

The nodes themselves may only be modified via the interface: their value source has to be `interface`.
You express that at the `node type` with `can-update: interface '<imported interfaces id>'`.

```js
interfaces
	'Supplier' ( ) = .'Supplier Data' // one supplier
		connection-status: .'Status' (
			| connected => 'Connected' ( )
			| connecting => 'Connecting' ( )
			| disconnected => 'Disconnected' ( )
		)
	'Catalogue' ( ) = .'Catalogues'[] // multiple catalogues
		initializer: ( /* initial data when item is added */ )
		connection-status: .'Status' (
			| connected => 'Connected' ( )
			| connecting => 'Connecting' ( )
			| disconnected => 'Disconnected' ( )
		)

root {
	'Supplier Data': group {
		can-update: interface 'Supplier'

		'Delivery Time': number 'days'
		'Status': stategroup (
			'Connected' { }
			'Connecting' { }
			'Disconnected' { }
		)
	}
	'Catalogues': collection ['Catalogue'] {
		can-update: interface 'Catalogue'

		'Catalogue': text
		'Status': stategroup (
			'Connected' { }
			'Connecting' { }
			'Disconnected' { }
		)
	}
}
```


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">imported interfaces</span>': [ <span class="token operator">interfaces</span> ] dictionary {
	'<span class="token string">parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">value</span>': [ <span class="token operator">=</span> <span class="token operator">.</span> ] reference
	}
	'<span class="token string">path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
	'<span class="token string">instances</span>': stategroup (
		'<span class="token string">many</span>' { [ <span class="token operator">[]</span> ]
			'<span class="token string">initializer</span>': [ <span class="token operator">initializer:</span> ] component <a href="#grammar-rule--interface-instance-initializer">'interface instance initializer'</a>
		}
		'<span class="token string">one</span>' { }
	)
	'<span class="token string">connection status</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">connection-status:</span> ]
			'<span class="token string">state group path</span>': component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary (
				static '<span class="token string">connected</span>' [ <span class="token operator">connected</span> ]
				static '<span class="token string">connecting</span>' [ <span class="token operator">connecting</span> ]
				static '<span class="token string">disconnected</span>' [ <span class="token operator">disconnected</span> ]
			) { [ <span class="token operator">|</span> ]
				'<span class="token string">state</span>': [ <span class="token operator">=></span> ] reference
				'<span class="token string">dataset status</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">dataset-status:</span> ]
						'<span class="token string">state group path</span>': component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
						'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary (
							static '<span class="token string">available</span>' [ <span class="token operator">available</span> ]
							static '<span class="token string">unavailable</span>' [ <span class="token operator">unavailable</span> ]
						) { [ <span class="token operator">|</span> ]
							'<span class="token string">state</span>': [ <span class="token operator">=></span> ] reference
							'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
						}
					}
				)
				'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
			}
		}
	)
}
</pre>
</div>
</div>
##### The `root` node type
Alan models are hierarchical models specifying hierarchical data.
An Alan model is a hierarchy of nested types with a single root type:
```js
root { }
```

The `root` type (short for node type) is a complex type that nests other (complex) types. Types are surrounded by
curly braces, and their identification is a path which starts from the root type. We refer to
an instance of a type as a node. The rule for defining a type carries the same name: `node`; it should be read as the `node type` rule,
as we define `node types` in a model (for legacy reasons it is called the `'node'` rule).

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root</span>': [ <span class="token operator">root</span> ] component <a href="#grammar-rule--node">'node'</a>
</pre>
</div>
</div>
##### Numerical types
Numbers in an application model require a numerical type. Also, computations with numbers of different numerical types require conversion rules.
Divisions require a division conversion rule, products require a product conversion rule, and so on. Some examples of numerical types, with conversion rules are
```js
'date' in 'days' @date
'date and time' in 'seconds' @date-time
'days'
'milliseconds'
	= 'seconds' * 1 * 10 ^ 3 // rule for converting 'seconds' to milliseconds
	@numerical-type: (
		label: "sec"
		decimals: 3
	)
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

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">numerical types</span>': [ <span class="token operator">numerical-types</span> ] dictionary {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">scale</span>' {
			'<span class="token string">timer resolution</span>': stategroup (
				'<span class="token string">none</span>' { }
				'<span class="token string">seconds</span>' { [ <span class="token operator">:</span> <span class="token operator">time-in-seconds</span> ] }
			)
			'<span class="token string">range type</span>': [ <span class="token operator">in</span> ] reference
		}
		'<span class="token string">quantity</span>' {
			'<span class="token string">product conversions</span>': dictionary { [ <span class="token operator">=</span> ]
				'<span class="token string">right</span>': [ <span class="token operator">*</span> ] reference
			}
			'<span class="token string">division conversions</span>': dictionary { [ <span class="token operator">=</span> ]
				'<span class="token string">denominator</span>': [ <span class="token operator">/</span> ] reference
			}
		}
	)
	'<span class="token string">singular conversions</span>': dictionary { [ <span class="token operator">=</span> ]
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">factor</span>' {
				'<span class="token string">invert</span>': stategroup (
					'<span class="token string">no</span>' { [ <span class="token operator">*</span> ] }
					'<span class="token string">yes</span>' { [ <span class="token operator">/</span> ] }
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
`text`, `file`, `number`, `collection`, `stategroup`, and `group`.

*Text*, *file*, and *number* are primitive property types. Text properties hold an unbounded
string value. File properties hold two unbounded string values: a file token and a file extension.
Number properties hold an integer value, with an optional `positive` annotation to ensure values greater zero.
For ensuring that number values have a predefined accuracy, Alan does not support number values with a fractional component.
For expressing the accuracy of a number, number properties reference a [`numerical type`](#numerical-types).

```js
'Name'        : text
'Price'       : number 'euro'
'Release Date': number positive 'date and time'
```

A *collection* property holds a map of key-value pairs. Keys are text values that have
to be unique such that we can reference them unambiguously.
A key field has to be specified explicitly, after the keyword `collection`; values are nodes of an inline defined type that specifies the key field:

```js
Customers : collection ['Customer ID'] {
	'Customer ID': text
	... /* other attributes of this type */ ...
}
```

A *state group* property holds a value indicating a state. States are the alternatives to an aspect
that a state group property indicates. For example, `red`, `orange`, or `green` for a `color` property of a traffic light. The type of the property value corresponds to one out of multiple
predefined state types, such as `simple` or `assembled`:
```js
'Product Type': stategroup (
	'Simple' { ... /* attributes of this type */ ... }
	'Assembled' { ... /* attributes of this type */ ... }
)
```

A *group* property groups related property values, which is useful for presentational purposes:
```js
'Address': group {
	'City': text
	'State': text
	'Zip Code': text
}
```

___Derived values.___ Properties hold either *base* values or *derived* values (derivations).
*Derived* values are computed from base values and other derived values.
Application users cannot modify derived values.
Properties holding *derived* values require an expression for computing their values at runtime:
```js
'City': text					// property holding a base value
'copy of City': text = .'City'  // property with an expression for deriving its value
```

The [derivations](#derived-values) section provides the grammar for derivation expressions,
detailing the different types of computations that the language supports.

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
A `reference-set` is for creating [bidirectional references](#bidirectional-references).
A *reference set* attribute holds the *inverse* of a [reference](#references) which is by default unidirectional.
References determine the values for reference sets; they create *inverse* references when your model specifies it.
Derivation expressions refer to them for computations (e.g. [derived numbers](#derived-numbers)).

##### Command attributes
A `command` is a complex parametrized atomic operation on the dataset.
The application engine executes a `command` in a single transaction.
A `command` attribute specification consists of a definition of `parameters` for the command and an [implementation](#commands-and-timers).

##### Action attributes
An `action` is a sequence of operations that a webclient (GUI) executes.
That is, unlike a `command`, an action can perform multiple different operations, interactively.
Actions provide users with wizards to guide them through their processes.
For an `action`, you can specify parameters that users have to provide before starting the execution of the action.
After the parameters, you have specify which operations should be performed.


{: #grammar-rule--node }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	'<span class="token string">permissions definition</span>': component <a href="#grammar-rule--node-permissions-definition">'node permissions definition'</a>
	'<span class="token string">todo definition</span>': component <a href="#grammar-rule--todo-definition">'todo definition'</a>
	'<span class="token string">has attributes</span>': stategroup = node-switch .'<span class="token string">attributes</span>' (
		| nodes = '<span class="token string">yes</span>' {
			'<span class="token string">first</span>' = first
			'<span class="token string">last</span>' = last
		}
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">attributes</span>': dictionary {
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
				'<span class="token string">referenced type path</span>': group { [ <span class="token operator">-></span> ]
					'<span class="token string">direction</span>': component <a href="#grammar-rule--direction-annotation">'direction annotation'</a>
					'<span class="token string">head</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
					'<span class="token string">root</span>': stategroup (
						'<span class="token string">context</span>' { }
						'<span class="token string">sibling</span>' {
							'<span class="token string">definition</span>': component <a href="#grammar-rule--sibling-reference-definition">'sibling reference definition'</a>
						}
					)
					'<span class="token string">path</span>': component <a href="#grammar-rule--plural-object-path-tail">'plural object path tail'</a>
				}
				'<span class="token string">value source</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">reference</span>' {
						'<span class="token string">reference</span>': [ <span class="token operator">inverse</span> ] component <a href="#grammar-rule--entry-reference-selector">'entry reference selector'</a>
					}
					'<span class="token string">union branch</span>' {
						'<span class="token string">branch</span>': [ <span class="token operator">branch</span> ] reference
					}
				)
			}
			'<span class="token string">command</span>' { [ <span class="token operator">:</span> <span class="token operator">command</span> ]
				'<span class="token string">permission definition</span>': component <a href="#grammar-rule--command-permission-definition">'command permission definition'</a>
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">global</span>' {
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-command-attribute">'ui command attribute'</a>
					}
					'<span class="token string">component</span>' { [ <span class="token operator">component</span> ] }
				)
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--node">'node'</a>
				'<span class="token string">implementation</span>': stategroup (
					'<span class="token string">external</span>' { [ <span class="token operator">external</span> ] }
					'<span class="token string">internal</span>' {
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
						'<span class="token string">implementation</span>': component <a href="#grammar-rule--command">'command'</a>
					}
				)
			}
			'<span class="token string">action</span>' { [ <span class="token operator">:</span> <span class="token operator">action</span> ]
				'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-action-attribute">'ui action attribute'</a>
				'<span class="token string">parameters</span>': component <a href="#grammar-rule--node">'node'</a>
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				'<span class="token string">action</span>': component <a href="#grammar-rule--ui-action">'ui action'</a>
			}
			'<span class="token string">property</span>' { [ <span class="token operator">:</span> ]
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">group</span>' { [ <span class="token operator">group</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">base</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ] }
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-group-property">'ui group property'</a>
						'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
					}
					'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
						'<span class="token string">key property</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] reference
						'<span class="token string">cardinality constraint</span>': component <a href="#grammar-rule--lower-bound-cardinality-constraint">'lower bound cardinality constraint'</a>
						'<span class="token string">graph constraints</span>': component <a href="#grammar-rule--graph-constraints-definition">'graph constraints definition'</a>
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">base</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
								'<span class="token string">key constraint</span>': stategroup (
									'<span class="token string">no</span>' {
										'<span class="token string">branches</span>': [ <span class="token operator">flatten</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
											'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--flatten-expression">'flatten expression'</a>
											'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
											'<span class="token string">node initializer</span>': component <a href="#grammar-rule--node-initializer">'node initializer'</a>
										}
										'<span class="token string">separator</span>': [ <span class="token operator">join</span> ] stategroup (
											'<span class="token string">dot</span>' { [ <span class="token operator">.</span> ] }
											'<span class="token string">dash</span>' { [ <span class="token operator">-</span> ] }
											'<span class="token string">colon</span>' { [ <span class="token operator">:</span> ] }
											'<span class="token string">greater than</span>' { [ <span class="token operator">></span> ] }
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
							'<span class="token string">positive</span>' { [ <span class="token operator">positive</span> ] }
						)
						'<span class="token string">numerical type</span>': reference
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">base</span>' {
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
									'<span class="token string">simple</span>' { }
								)
							}
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' { [ <span class="token operator">parameter</span> ] }
									'<span class="token string">expression</span>' {
										'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
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
							'<span class="token string">base</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' { [ <span class="token operator">parameter</span> ] }
									'<span class="token string">expression</span>' {
										'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
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
								'<span class="token string">direction</span>': component <a href="#grammar-rule--direction-annotation">'direction annotation'</a>
								'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
								'<span class="token string">expression</span>': component <a href="#grammar-rule--entry-reference-definition">'entry reference definition'</a>
								'<span class="token string">assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
								'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-reference-rule">'ui reference rule'</a>
								'<span class="token string">rules</span>': component <a href="#grammar-rule--where-rules-definition">'where rules definition'</a>
							}
						)
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">base</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' { [ <span class="token operator">parameter</span> ] }
									'<span class="token string">derived key</span>' { [ <span class="token operator">key</span> ] }
									'<span class="token string">expression</span>' {
										'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
									}
								)
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-text-property">'ui text property'</a>
					}
					'<span class="token string">state group</span>' { [ <span class="token operator">stategroup</span> ]
						'<span class="token string">type</span>': stategroup (
							'<span class="token string">base</span>' { }
							'<span class="token string">derived</span>' { [ <span class="token operator">=</span> ]
								'<span class="token string">value source</span>': stategroup (
									'<span class="token string">parameter</span>' { [ <span class="token operator">parameter</span> ] }
									'<span class="token string">expression</span>' {
										'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
										'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
									}
								)
							}
						)
						'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-state-group-property">'ui state group property'</a>
						'<span class="token string">first state</span>': reference = first
						'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
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
							'<span class="token string">rules</span>': component <a href="#grammar-rule--where-rules-definition">'where rules definition'</a>
							'<span class="token string">permissions</span>': component <a href="#grammar-rule--item-permissions-definition">'item permissions definition'</a>
							'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-state">'ui state'</a>
							'<span class="token string">node</span>': component <a href="#grammar-rule--node">'node'</a>
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
## Cardinality constraint
---
Collections support a lower bound cardinality constraint, ensuring that a `collection` is not empty.
This is useful for ensuring that you can always derive a reference to the source/sink of an ordered graph.
It also ensures that `min`, `max`, and similar computations on sets of number values do not require a fallback value.


{: #grammar-rule--lower-bound-cardinality-constraint }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lower bound cardinality constraint</span>' {
	'<span class="token string">constraint</span>': stategroup (
		'<span class="token string">non empty</span>' { [ <span class="token operator">non-empty</span> ] }
		'<span class="token string">none</span>' { }
	)
}
</pre>
</div>
</div>
## References
---
References indicate relations between different parts of your application data.
For example, suppose that you have `Orders` and `Products`, where `Orders` reference a `Product`.
You can express that reference in your model, such that your users can see it, and such that you can use it in computations:
```js
'Products': collection ['Name'] {
	'Name': text
	'In Stock': stategroup (
		'No' { }
		'Yes' { }
	)
}
'Orders': collection ['ID'] {
	'ID': text
	'Product': text -> ^ .'Products'[] as $'p'     // reference rule for text
		where 'In Stock' -> $'p'.'In Stock'?'Yes' // additional reference rule for the text
	'Ready': stategroup (
		'No' { }
		'Yes' { }
	)
	'Sent for Delivery': stategroup (
		'No' { }
		'Yes' where 'Order Ready' -> .'Ready'?'Yes' { } // reference rule for state
	)
}
```
The example indicates that you can specify multiple references at a text property.
You can also specify additional rules for the 'main' reference with keyword `$`, which refers to the referenced node.

In order for the text value to reference an item in a collection, its value has to equal the key value of an item in the specified `collection`.
At runtime, reference expressions always produce a single specific node (or none at all, if the reference is broken).
The language ensures that.
In the GUI, references translate to a select list from which the application user has to choose an item.

Alternatively, sometimes a specific state for a state group is related to another node.
The `where`-rule `Order Ready` expresses that: an order can be `Sent for Delivery` if and only if it is `Ready`.

##### Reference behaviour
The *reference behaviour* that you specify, determines how the runtime treats a reference.
Mandatory references (specified with keyword `->`) are constraints that are enforced by the runtime: they have to resolve to a node.
Optional references (specified with keyword `~>`) do not have to resolve to a node.


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
The language ensures that references either point to a *single specific node, or none at all*.
Thus, mandatory references unambiguously point to a single specific node.
Because of that, derived value computations and command invocations can safely use them.

Optional references are especially useful when you want user data to reference imported data (`can-update: interface '...'`).
Mandatory references are not allowed among data from different sources, such that data import is always successfull.
##### Upstream & downstream
Reference constraint expressions exist in two different flavours:
(1) `upstream` reference expressions that use earlier defined attributes and (2)
`downstream` reference expressions that use later defined attributes.
Downstream references require an explicit annotation: `downstream` after the arrow (`->`/`~>`) specifying the reference behaviour.


{: #grammar-rule--direction-annotation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">direction annotation</span>' {
	'<span class="token string">direction</span>': stategroup (
		'<span class="token string">upstream</span>' { }
		'<span class="token string">downstream</span>' { [ <span class="token operator">downstream</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--graph-traversal-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">graph traversal definition</span>' {
	'<span class="token string">traversal type</span>': stategroup (
		'<span class="token string">base order</span>' { }
		'<span class="token string">inverse order</span>' { [ <span class="token operator">inverse</span> ] }
	)
	'<span class="token string">graph</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--graph-traversal-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">graph traversal selector</span>' {
	'<span class="token string">ancestor path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
	'<span class="token string">graph traversal</span>': component <a href="#grammar-rule--graph-traversal-definition">'graph traversal definition'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--graph-traversal-selector">'graph traversal selector'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--recursion-annotation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">recursion annotation</span>' {
	'<span class="token string">recursive graph traversal</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">(</span> <span class="token operator">recurse</span>, <span class="token operator">)</span> ]
			'<span class="token string">selector</span>': component <a href="#grammar-rule--graph-traversal-selector">'graph traversal selector'</a>
		}
	)
}
</pre>
</div>
</div>
[Below](#sibling-references) we explain the annotation for `sibling navigation`.
##### Bidirectional references
Text references are either unidirectional or bidirectional.
For bidirectional references, you specify a reference-set.
If a reference is `downstream` reference, then the `reference-set` holds upstream references.
Conversely, if a reference is `upstream`, then the `reference-set` holds downstream references:

```js
'Products': collection ['Name'] {
	'Name': text
	// reference-set holding downstream references to Orders added by Product references,
	'Orders': reference-set -> downstream ^ .'Orders'* = inverse >'Product'
}
'Orders': collection ['ID'] {
	'ID': text
	// a (bidirectional) upstream reference:
	'Product': text -> ^ .'Products'[]
}
```

>The expression `^ .'Products'` is a navigation expression that produces exactly one collection at runtime.
The Alan runtime interpretes such [navigation expressions](#navigation) as follows:
starting from the `Orders` node, go to the parent node (as expressed by the navigation step `^`);
then select the `Products` collection found on that node.
Thus, at runtime, navigation expressions are executed relative to the context node for which the expression should be evaluated.

##### Sibling references
If you want references from `Products` to other `Products`, you will find that this line gives an error:
```js
`Other Product`: text -> ^ .'Products'[]
```
The compiler requires that you reference an earlier defined property, and not the `Products` property that defines the expression.
For references from `Products` to other other `Products`, you need special `sibling` references.


{: #grammar-rule--entry-reference-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">entry reference definition</span>' {
	'<span class="token string">collection path</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">simple</span>' { [ <span class="token operator">[]</span> ] }
		'<span class="token string">sibling</span>' {
			'<span class="token string">definition</span>': component <a href="#grammar-rule--sibling-reference-definition">'sibling reference definition'</a>
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--descendant-object-path">'descendant object path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--sibling-reference-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">sibling reference definition</span>' {
	'<span class="token string">graph participation</span>': [ <span class="token operator">sibling</span> ] stategroup (
		'<span class="token string">no</span>' {
			'<span class="token string">support self reference</span>': stategroup (
				'<span class="token string">no</span>' { }
				'<span class="token string">yes</span>' { [ <span class="token operator">||</span> <span class="token operator">self</span> ] }
			)
		}
		'<span class="token string">yes</span>' { [ <span class="token operator">in</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			'<span class="token string">graph traversal</span>': component <a href="#grammar-rule--graph-traversal-definition">'graph traversal definition'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--where-rule-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">where rule object path</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--context-object-step">'context object step'</a>
		}
		'<span class="token string">sibling rule</span>' {
			'<span class="token string">rule</span>': reference
		}
	)
	'<span class="token string">path</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--where-rules-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">where rules definition</span>' {
	'<span class="token string">has rule</span>': stategroup = node-switch .'<span class="token string">rules</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">rules</span>': dictionary { [ <span class="token operator">where</span> ]
		'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">rule</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">behaviour</span>': component <a href="#grammar-rule--reference-behaviour">'reference behaviour'</a>
		'<span class="token string">direction</span>': component <a href="#grammar-rule--direction-annotation">'direction annotation'</a>
		'<span class="token string">recursion</span>': component <a href="#grammar-rule--recursion-annotation">'recursion annotation'</a>
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">entry reference</span>' {
				'<span class="token string">expression</span>': component <a href="#grammar-rule--entry-reference-definition">'entry reference definition'</a>
			}
			'<span class="token string">node reference</span>' {
				'<span class="token string">object path</span>': component <a href="#grammar-rule--where-rule-object-path">'where rule object path'</a>
				'<span class="token string">type</span>': stategroup (
					'<span class="token string">existence</span>' { }
					'<span class="token string">equality</span>' { [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
						'<span class="token string">node path</span>': component <a href="#grammar-rule--where-rule-object-path">'where rule object path'</a>
					}
					'<span class="token string">containment</span>' { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
						'<span class="token string">key node path</span>': component <a href="#grammar-rule--where-rule-object-path">'where rule object path'</a>
					}
				)
			}
		)
		'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-reference-rule">'ui reference rule'</a>
	}
}
</pre>
</div>
</div>
The following model expresses sibling references from `Products` to other `Products` which are corresponding (`Parts`),
and also from `Orders` to a `Previous Order`:
{: #example--sibling-recursion }
```js
'Products': collection ['Name']
	'assembly': acyclic-graph
{
	'Name': text
	'Parts': collection ['Product'] {
		// an 'upstream' sibling Product reference that partakes in the 'assembly' graph:
		'Product': text -> ^ sibling in ('assembly')
		'Part Price': number 'euro'
			= ( recurse ^ 'assembly' ) >'Product' /*[1]*/ .'Product Price' /*[2a]*/
	}
	'Parts Cost': number 'euro' = sum .'Parts'* .'Part Price'
	'Assembly Cost': number 'euro'
	'Product Price': number 'euro'
		= ( recurse 'assembly' ) sum ( .'Parts Cost', .'Assembly Cost' ) /*[2b]*/
}
'Orders': collection ['Year']
	'timeline': ordered-graph .'Is First Order' ( ?'Yes'|| ?'No'>'Previous Order' )
{
	'Year': text
	'Price': number 'euro'
	'Is First Order': stategroup (
		'Yes' { }
		'No' {
			'Previous Order': text -> ^ sibling in ('timeline')
		}
	)
	'Total Sales Value': number 'euro' = ( recurse 'timeline' ) switch .'Is First Order' (
		|'Yes' => .'Price'
		|'No' as $'no' => sum (
			.'Price',
			$'no'>'Previous Order'.'Total Sales Value' // recursion!
		)
	)
}
```

##### Graph constraints
The model above also expresses graph constraints.
Graph constraints ensure termination for recursive computations traversing a graph.
Graph constraints ensure that a set of references (edges) together form a graph satisfying a specific property.
For example, an `acyclic-graph` constraint ensures that references that partake in the graph, form a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph).
For a detailed explanation, see [AlanLight](http://resolver.tudelft.nl/uuid:3eedbb63-29ea-4671-a016-4c037eec94cd).


{: #grammar-rule--graph-constraints-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">graph constraints definition</span>' {
	'<span class="token string">graphs</span>': dictionary {
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">acyclic</span>' { [ <span class="token operator">acyclic-graph</span> ] }
			'<span class="token string">ordered</span>' { [ <span class="token operator">ordered-graph</span> ]
				'<span class="token string">ordering property path</span>': group {
					'<span class="token string">ordering state group path</span>': component <a href="#grammar-rule--descendant-base-property-path">'descendant base property path'</a>
					'<span class="token string">ordering states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">sink state</span>': [ <span class="token operator">?</span> ] reference
						'<span class="token string">edge state</span>': [ <span class="token operator">||</span> <span class="token operator">?</span> ] reference
						'<span class="token string">edge reference</span>': [ <span class="token operator">></span> ] reference
					}
				}
			}
		)
		'<span class="token string">value type</span>': stategroup (
			'<span class="token string">base</span>' { }
			// '<span class="token string">derived</span>' { }
		)
	}
}
</pre>
</div>
</div>

The example model expresses that `Products` form an acyclic `assembly` graph via their `Parts`:
`Product` references of `Parts` partake in the acyclic `assembly` graph on `Products`.
The constraint ensures that recursive `Part Price`, `Parts Cost` and `Product Price` computations terminate.

For `Orders`, the model expresses an ordered `timeline` graph, which means that a strict total ordering exists for all `Orders`.
That is: only one `Orders` item does not have preceding `Order`. All other `Orders` do.
For ordered graphs, the application language supports deriving the `source` and the `sink` of the graph: the first `Order` and the most recent `Order`.

Note that the expression for computing a `Part Price` starts with an [annotation](#grammar-rule--recursion-annotation): `( recurse ^ 'assembly' )`.
That is because the `Part Price` is computed recursively: for all recursive computations, the annotation is required.
The (hierarchy of) graph(s) that you have to name as part of the annotation, imply an order in which recursive computations can be evaluated.
If the annotation is missing, the compiler produces an error message indicating that a 'cyclic dependency' exists.
The existence of an order for evaluating recursion ensures that the recursive computations are finite.

A [recursion annotation](#grammar-rule--recursion-annotation) should be placed at a property or reference definition
1. if the recursive expression for computing the value contains a sibling navigation step, like `>'Product'` [1] in the example.
2. if the property or reference (`'Product Price'` at [2b]) is referenced by another recursive expression after a sibling navigation step (`>'Product'` at [2a]).

Note that when providing a recursion annotation, only sibling references that partake in the indicated graphs may be used.
That is, when a computation depends on multiple sibling references partaking in different graphs, you need to split it up into separate computations (derivations).
For computing the value that you need, you can combine the results from the separate computations.

Sometimes, computations traverse the `inverse` of a graph (by using a `reference-set` attribute).
For such computations, you need to add the annotation `inverse`: `( recurse inverse 'assembly' )`.

## Derived values
---
Derived values (derivations) are computed from base values and other derived values.
The application language supports derived texts, numbers, files, states, references, and collections.
Derived texts, numbers, files, states, and references share common grammar rules:
 the [derivation expression](#grammar-rule--derivation-expression) rule and corresponding parts presented below.
The language has special rules for [deriving collections](#derived-collections).

### Recursion and cyclic dependencies
The `application` language guarantees termination for derived value computations.
The solution for achieving this guarantee, rejects recursive computations by default (you will get a cyclic dependency error).

But, the `application` does support recursion, including mutual recursion.
For recursive computations, you need to specify which (acyclic/ordered) graph the computation traverses,
such that termination is guaranteed, as shown in the [sibling references example](#example--sibling-recursion).
For that purpose, you need an [annotation](#grammar-rule--recursion-annotation) after the `=` sign, and before the derivation expression itself: `= ( recurse /* ^ path to graph ^*/ '<graph>' ) ...expression...`.
If you add the annotation to your expression, the expression can only refer to sibling references that partake in the specified graph `'<graph>'`.

Note that the annotation enables you to specify a graph per level in the data hierarchy.
That is, a single computation can traverse both a child and parent graph (and ancestor graphs higher up in the hierarchy).
To ensure termination, you cannot traverse multiple graphs from the same collection, as multiple acyclic graphs may together form cycles.

### Expressions
A derivation expression starts with optional `switch` statements followed by a subexpression that produces a value.
The following code sample exemplifies the use of the different types of `switch` statements, where each case produces a text value:
```js
'Orders': collection ['Order'] {
	'Order': text
	'Price': number 'euro'
}
'Store Status': stategroup (
	'Open' { }
	'Closed' { }
)

/* state switch */
'Store Status Label': text = switch .'Store Status' (
	|'Open'   => "Open"
	|'Closed' => "Closed"
)

/* node switch */
'Favorite Order': text ~> .'Orders'[]
'Favorite Order Exists?': text = switch >'Favorite Order' (
	| none => "No"
	| node => "Yes"
)

/* node set switch */
'How Many Orders?': text = switch .'Orders'* (
	| none  => "No Orders"
	| node  => "One Order"
	| nodes => "More Than One Order"
)

/* number switch */
'Order Count': number 'count' = count .'Orders'*
'More Than 10 Orders?': text = switch .'Order Count' compare ( 10 ) (
	| >  => "More than 10"
	| <  => "Less than 10"
	| == => "Exactly 10"
)
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
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">state group path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
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
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { dynamic-order
				'<span class="token string">node</span>': group { [ <span class="token operator">|</span> <span class="token operator">node</span> ]
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
				}
				'<span class="token string">none</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
			}
		}
		'<span class="token string">set switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">nodes path</span>': component <a href="#grammar-rule--object-set-path">'object set path'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { dynamic-order
				'<span class="token string">match none</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">|</span> <span class="token operator">none</span> <span class="token operator">=></span> ]
						'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
					}
				)
				'<span class="token string">match node</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">|</span> <span class="token operator">node</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
					}
				)
				'<span class="token string">match nodes</span>': stategroup (
					'<span class="token string">no</span>' { }
					'<span class="token string">yes</span>' { [ <span class="token operator">|</span> <span class="token operator">nodes</span> ]
						'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
						'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
					}
				)
			}
		}
		'<span class="token string">number switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">number path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
			'<span class="token string">compare to</span>': [ <span class="token operator">compare</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] stategroup (
				'<span class="token string">constant</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--constant-number-value">'constant number value'</a>
				}
				'<span class="token string">path</span>' {
					'<span class="token string">right number path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
				}
			)
			'<span class="token string">last case</span>': reference = last
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary (
				static '<span class="token string">equals</span>' [ <span class="token operator">==</span> ]
				static '<span class="token string">less than or greater than</span>' [ <span class="token operator"><></span> ]
				static '<span class="token string">greater than</span>' [ <span class="token operator">></span> ]
				static '<span class="token string">greater than or equals</span>' [ <span class="token operator">>=</span> ]
				static '<span class="token string">less than</span>' [ <span class="token operator"><</span> ]
				static '<span class="token string">less than or equals</span>' [ <span class="token operator"><=</span> ]
			) { [ <span class="token operator">|</span> ]
				'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">case</span>' = predecessor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-named-object-assignment">'optional named object assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
			}
		}
		'<span class="token string">recurse</span>' {
			'<span class="token string">step</span>': stategroup (
				'<span class="token string">start</span>' {
					'<span class="token string">binding node path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
					'<span class="token string">recursion start assignment</span>': component <a href="#grammar-rule--named-object-assignment">'named object assignment'</a>
					'<span class="token string">graph traversal</span>': [ <span class="token operator">in</span> ] component <a href="#grammar-rule--graph-traversal-definition">'graph traversal definition'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
				}
				'<span class="token string">repeat</span>' { [ <span class="token operator">recurse</span> ]
					'<span class="token string">recursion start</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--named-object-step">'named object step'</a>
					'<span class="token string">sibling node path</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
				}
			)
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
'<span class="token string">derivation expression list</span>' {
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
					'<span class="token string">branch</span>': [ <span class="token operator">branch</span> ] reference
					'<span class="token string">expression</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
				}
				'<span class="token string">ordered graph node</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">source</span>' { [ <span class="token operator">source-of</span> ] }
						'<span class="token string">sink</span>' { [ <span class="token operator">sink-of</span> ] }
					)
					'<span class="token string">collection path</span>': [, <span class="token operator">*</span> ] component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
					'<span class="token string">ordered graph</span>': [ <span class="token operator">in</span> ] reference
				}
			)
		}
		'<span class="token string">text</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': text
				}
				'<span class="token string">concatenation</span>' { [ <span class="token operator">concat</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-list">'derivation expression list'</a>
				}
			)
		}
		'<span class="token string">number</span>' {
			'<span class="token string">expression</span>': component <a href="#grammar-rule--number-expression">'number expression'</a>
		}
		'<span class="token string">state</span>' {
			'<span class="token string">initializer</span>': component <a href="#grammar-rule--state-initializer">'state initializer'</a>
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
		}
	)
}
</pre>
</div>
</div>
#### Derived texts
A derived text value can consist of static text values and text values from other properties:
```js
'Address': group {
	'Street'       : text // e.g. "Huntington Rd"
	'Street number': text // e.g. "12B"
}
// label for an external billing system, like "Huntington Rd 12B":
'Address label': text = concat ( .'Address'.'Street', " ", .'Address'.'Street number' )
```

#### Derived numbers
Examples of derived number properties, including required conversion rules:
```js
root {
	'Tax Percentage': number positive 'percent'
	'Products': collection ['Name'] {
		'Name': text
		'Price': number 'eurocent'
		'Price (euro)': number 'euro' = from 'eurocent' .'Price'
		'Order Unit Quantity': number positive 'items'
		'Orders': reference-set -> downstream ^ .'Orders'* = inverse >'Product'
		'Sales Value': number 'eurocent' = sum <'Orders'* .'Price'
		'Items Sold': number 'items' = count <'Orders'*
	}
	'Total Sales Value': number 'eurocent' = sum .'Products'* .'Sales Value'
	'Number of Products': number 'items' = count .'Products'*
	'Orders': collection ['ID'] {
		'ID': text
		'Product': text -> ^ .'Products'[]
		'Quantity': number positive 'items'
		'Loss': number 'items' = remainder (
			.'Quantity',
			>'Product' .'Order Unit Quantity'
		)
		'Price': number 'eurocent' = product (
			>'Product'.'Price' as 'eurocent',
			.'Quantity'
		)
		'Order Units': number positive 'units' = division ceil (
			.'Quantity' as 'items' ,
			>'Product'.'Order Unit Quantity'
		)
		'Tax': number 'eurocent'
		'Gross Price': number 'eurocent' = sum ( .'Price', .'Tax' )
		'Creation Time': number 'date and time'
		'Estimated Lead Time': number 'seconds'
		'Estimated Delivery Time': number 'date and time' = add (
			.'Creation Time',
			.'Estimated Lead Time' )
		'Delivered': stategroup (
			'No' { }
			'Yes' {
				'Delivery Time': number positive 'date and time'
				'Lead Time': number 'seconds' = diff 'date and time' (
					.'Delivery Time',
					^ .'Creation Time'
				)
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
	'units'
		= 'items' / 'items'
	'items'
	'date and time' in 'seconds'
	'seconds'
```


{: #grammar-rule--number-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">constant</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--constant-number-value">'constant number value'</a>
		}
		'<span class="token string">unary</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">absolute value</span>' { [ <span class="token operator">abs</span> ] }
				'<span class="token string">numerical type conversion</span>' {
					'<span class="token string">conversion</span>': [ <span class="token operator">from</span> ] reference
				}
				'<span class="token string">sign inversion</span>' { [ <span class="token operator">-</span> ] }
			)
			'<span class="token string">expression</span>': component <a href="#grammar-rule--derivation-expression-tail">'derivation expression tail'</a>
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
					'<span class="token string">expressions</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">numerator</span>': component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
						'<span class="token string">conversion rule</span>': [ <span class="token operator">as</span> ] reference
						'<span class="token string">denominator</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					}
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
					'<span class="token string">numbers</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--derivation-expression-list">'derivation expression list'</a>
				}
				'<span class="token string">addition</span>' { [ <span class="token operator">add</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					'<span class="token string">left</span>': component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
				}
				'<span class="token string">difference</span>' { [ <span class="token operator">diff</span> ]
					'<span class="token string">scale type</span>': reference
					'<span class="token string">expressions</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">left</span>': component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
						'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--unary-number-expression">'unary number expression'</a>
					}
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

{: #grammar-rule--constant-number-value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">constant number value</span>' {
	'<span class="token string">value</span>': integer
}
</pre>
</div>
</div>
#### Derived files
Derived `file` values take their value (token + extension) from another `file` value.
For example, you can derive a `Contract` which is a `Default Contract` in case of a `Standard` `Agreement`, and a `Custom` `Contract` in case of a `Custom` `Agreement`:
```js
'Standard Contract': file
'Agreement': stategroup (
	'Standard' { }
	'Custom' {
		'Contract': file
	}
)
'Contract': file = switch .'Agreement' (
	|'Standard' => .'Standard Contract'
	|'Custom' as $'con'  => $'con'.'Contract'
)
```

#### Derived states
Derived states are computed using the abovementioned `switch` expressions, where different cases lead to different states.
For example, we can derive if a `Product` exists in a `Catalog` of `Products` from a `Catalog Provider`.
For this purpose, we check if the *optional* `Product` reference on an `Order` produces a node or nothing:
```js
'Catalog': group { can-update: interface 'Catalog Provider'
	'Products': collection ['Name'] {
		'Name': text
		'Price': number 'eurocent'
		'Description': text
	}
}
'Orders': collection ['ID'] {
	'ID': text
	'Product': text ~> ^ .'Catalog'.'Products'[]
	'Product found': stategroup = switch >'Product' (
		| node as $ => 'Yes' where 'Found Product' = $ ( 'Price' = $ .'Price' )
		| none => 'No' ( )
	) (
		'Yes' where 'Found Product' -> >'Product' {
			'Description': text = .&'Found Product'.'Description'
			'Price': number 'eurocent' = parameter
		}
		'No' { }
	)
}
```

The expression for deriving a state, has to satisfy all `where` rules for the state.
In the example, the `where` rule expresses that the optional `Product` reference is no longer optional.
Instead, the reference is mandatory in context of the `Yes` state. The expression 'proves' that.
You can use the `Found Product` for deriving values such as `Description` on the state node.

An expression for deriving a state can express how to initialize property values of the state as well, such as `Price` in the example.
To make this work, you have to specify `= parameter` for properties that you want to set with the [state initializer](#grammar-rule--state-initializer).
This language construct is especially useful when a reference to a node like `'Found Product'` is not available.
Furthermore, it useful for special operations such as `source-of` and `sink-of`, which we discuss below.


{: #grammar-rule--state-initializer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">state initializer</span>' {
	'<span class="token string">state</span>': reference
	'<span class="token string">rule arguments</span>': dictionary { [ <span class="token operator">where</span> ]
		'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
	}
	'<span class="token string">node initializer</span>': component <a href="#grammar-rule--node-initializer">'node initializer'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--node-initializer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node initializer</span>' {
	'<span class="token string">arguments</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">expression</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--derivation-expression">'derivation expression'</a>
	}
}
</pre>
</div>
</div>
#### Derived references
Sometimes it is useful to derive a reference to a collection entry for use by the application user and other computations.
Similar to base references, derived references require you to express a text property follow by a reference definition.
For deriving a reference, you have to provide an expression that produces a node that matches the reference definition.
The definition of `'Product copy'` depicts that:
```js
'Products': collection ['Name'] {
	'Name': text
}
'Orders': collection ['Year']
	'timeline': ordered-graph .'Is First Order' ( ?'Yes'|| ?'No'>'Previous Order' )
{
	'Year': text
	'Product': text -> ^ .'Products'[]
	'Product copy': text -> ^ .'Products'[] = >'Product' /* derived reference */
	'Is First Order': stategroup (
		'Yes' { }
		'No' {
			'Previous Order': text -> ^ sibling in ('timeline')
		}
	)
}

/* source-of/sink-of of graph */
'Has Orders': stategroup = switch .'Orders'* (
	| nodes as $ => 'Yes' (
		'Oldest Order' = sink-of $ * in 'timeline'
		'Most Recent Order' = source-of $ * in 'timeline'
	)
	| none => 'No' ( )
) (
	'Yes' {
		'Oldest Order'     : text -> ^ .'Orders'[] = parameter /* derived reference */
		'Most Recent Order': text -> ^ .'Orders'[] = parameter /* derived reference */
	}
	'No' { }
)
```

With the special `source-of` and `sink-of` operation, you can derive a reference to the respective nodes in an ordered graph.
These operations can only be applied to a collection for which we can guarantee non-emptiness, as otherwise the source/sink do not exist.
Therefore, we first `switch` on the content of the `'Orders'` collection.
If it holds `nodes` (meaning that it is not empty), then we can apply the `source-of` and `sink-of` operations.
#### Derived collections

{: #grammar-rule--flatten-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">flatten expression</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--group-ancestor-node-path">'group ancestor node path'</a>
	'<span class="token string">path</span>': component <a href="#grammar-rule--plural-descendant-node-path">'plural descendant node path'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--reference-set-subset-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference set subset step</span>' {
	'<span class="token string">subset</span>': stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">*</span> ] }
		'<span class="token string">yes</span>' { [ <span class="token operator">[</span>, <span class="token operator">]</span> ]
			'<span class="token string">head</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">simple</span>' { }
				'<span class="token string">sibling</span>' { [ <span class="token operator">sibling</span> ] }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--plural-object-path-tail">'plural object path tail'</a>
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
		'<span class="token string">augment</span>' {
			'<span class="token string">collection path</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
			'<span class="token string">filter path</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--descendant-object-path">'descendant object path'</a>
		}
		'<span class="token string">union</span>' { [ <span class="token operator">union</span> ]
			'<span class="token string">branches</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">has predecessor</span>': stategroup = node-switch predecessor (
					| node = '<span class="token string">yes</span>' { }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">has successor</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">source</span>': [ <span class="token operator">=</span> ] stategroup (
					'<span class="token string">dependency</span>' {
						'<span class="token string">path</span>': component <a href="#grammar-rule--plural-object-path">'plural object path'</a>
						'<span class="token string">dependency</span>': component <a href="#grammar-rule--dependency-step">'dependency step'</a>
					}
					'<span class="token string">dependency inversion</span>' {
						'<span class="token string">reference set path</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
						'<span class="token string">subset path</span>': component <a href="#grammar-rule--reference-set-subset-step">'reference set subset step'</a>
					}
				)
			}
			/* The '<span class="token string">first branch</span>' is computed by the compiler.
			** For recursive union computations, the first branch may not require recursion,
			** and should ensure the required cardinality corresponding to the cardinality constraint (one for non-empty). */
			'<span class="token string">first branch</span>': reference = first
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
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] component <a href="#grammar-rule--property-step">'property step'</a>
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
## Permissions and Todos
---
The application language supports expression permission and todo requirements down to the level of a single specific `user` or `interface`.
At the `node type` level you can specify permissions for nodes: read and update permissions.
In addition, you can express that a node creates a todo-item in a [todo-list](#todo-items) of your application.
At collection properties and states, you can specify item permissions: create and delete permissions for collection entries and states.
At command attributes you can express permission requirements for executing a command.



{: #grammar-rule--node-permissions-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node permissions definition</span>' { dynamic-order
	'<span class="token string">read permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { [ <span class="token operator">can-read:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
	'<span class="token string">update permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { [ <span class="token operator">can-update:</span> ]
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
		'<span class="token string">explicit</span>' { [ <span class="token operator">can-create:</span> ]
			'<span class="token string">permission</span>': component <a href="#grammar-rule--permission">'permission'</a>
		}
	)
	'<span class="token string">delete permission</span>': stategroup (
		'<span class="token string">inherited</span>' { }
		'<span class="token string">explicit</span>' { [ <span class="token operator">can-delete:</span> ]
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
	'<span class="token string">source</span>': stategroup (
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
### Permissions
When *read permissions* and *update permissions* are not specified at the root node type, **all** application users can read and update all application data.
Thus, if your applications supports `anonymous` users, anyone with your application's url can access all application data.

To restrict access to your application data, you can start by specifying some permissions at the root node type.
The line `can-read: user` at the `root` expresses that only users with a user account (in the `Users` collection), have access to application data:
```js
root {
	can-read: user
	can-update: user .'Type'?'Admin'

	'Users': collection ['ID']
		can-create: user .'Type'?'Admin'
		can-delete: user .'Type'?'Admin'
	{
		can-read: user is ( /*this*/ ) || user .'Type'?'Admin'
		can-update: user .'Type'?'Admin' // NOTE: unneeded

		'ID': text
		'Address': group { can-update: ^ is ( user )
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
	'Teams': collection ['Name'] { can-read: .'Members' [ user .'ID' ]
		'Name': text
		'Members': collection ['Member'] {
			'Member': text ~> ^ ^ .'Users'[]
		}
		'Description': text
	}
}
```

Node types **inherit** *read* and *update* permission requirements from their ancestor node types.
That is, if you specify required permissions at the `root` node type, you do not have to repeat it a child node type.
The child node type takes the permission requirements from the `root` node type.
##### Read permissions
Read permission requirements are **cumulative**.
That is, in order to read a node, a user requires read permission for *all ancestors nodes* of that node as well.
For example, in order to read a `Members` node specified above,
 a user needs permissions for the ancestor `Teams`-node, as well as the `root` node.
##### Update permissions
Update permission requirements are **not cumulative**.
Instead, update permissions for child nodes **override** permission requirements for parent nodes.
For example, for updates to the root node, we can require an admin: `user .'Type'?'Admin'`.
If we were to omit other permission requirements, only admins would be able to update application data because of inheritance.
But, because of `can-update: ^ is ( user )` at `Address` in the model, users can (only!) update their *own* `Address` information.
> NOTE: for updating a node, users have to be able to *read* ancestor nodes!

##### Create and delete permissions
Create and delete permission requirements for collection entries and states (items) inherit *update* permission requirements from the parent node type.
The permissions are **one-off overrides** that are not carried down in the node type hierarchy.
That is, they only apply to the state type or collection attribute where they are specified.
##### Command execution permissions
Command execution permissions are independent of aforementioned permissions.
Execution permission requirements only apply to the command for which they are specified.
If a command A calls another command B, then required permissions for B are not checked.
That is, the application only verifies that the user is permitted to execute command A.
> NOTE: for executing a command, the command has to be reachable, meaning that users need read access for the node on which they want to execute the command!


{: #grammar-rule--command-permission-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command permission definition</span>' {
	'<span class="token string">execute permission</span>': stategroup (
		'<span class="token string">reachable</span>' { }
		'<span class="token string">explicit</span>' { [ <span class="token operator">can-execute:</span> ]
			'<span class="token string">requirement</span>': component <a href="#grammar-rule--user-requirement">'user requirement'</a>
		}
	)
}
</pre>
</div>
</div>
### Todo items
Todo items are shown in a special section of your generated application.
The list of todo items is constructed from nodes that are marked as todos.
You express that in your model with `has-todo:` followed by an expression that specifies to which users the todo item applies.


{: #grammar-rule--todo-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">todo definition</span>' {
	'<span class="token string">todo</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">has-todo:</span> ]
			'<span class="token string">requirement</span>': component <a href="#grammar-rule--user-requirement">'user requirement'</a>
			'<span class="token string">ui</span>': component <a href="#grammar-rule--ui-todo">'ui todo'</a>
		}
	)
}
</pre>
</div>
</div>
### User requirements
For user requirements you can depend on your application data via complex expressions that traverse your model.
With the `||` keyword, you specify alternatives.
With a `where` clause, you specify requirements on top of requirements ('and').


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
## Commands and Timers
---

Commands enable external systems to perform operations via an Alan `interface` on `application` data.
Furthermore, commands can perform operations on other systems that other systems provide via an Alan `interface`.
For this to work, interfaces have to be listed in the `interfaces` section of an `application` model.
Also, the `external` command needs to be consumed by the application model, like the `Place Order` command in the example:

```js
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
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
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
			'<span class="token string">path</span>': group {
				'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
				'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
			}
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
			}
		}
		'<span class="token string">node switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">expression</span>': component <a href="#grammar-rule--node-expression">'node expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { dynamic-order
				'<span class="token string">node case</span>': [ <span class="token operator">|</span> <span class="token operator">node</span> ] group {
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
				}
				'<span class="token string">none case</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> ] group {
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--command-expression">'command expression'</a>
				}
			}
		}
		'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' {
					'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">reference set</span>' {
					'<span class="token string">reference set</span>': [ <span class="token operator"><</span> ] reference
				}
			)
			'<span class="token string">tail</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
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

{: #grammar-rule--interface-instance-initializer }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface instance initializer</span>' {
	'<span class="token string">initializer</span>': component <a href="#grammar-rule--command-object-expression">'command object expression'</a>
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
				'<span class="token string">constant</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--constant-number-value">'constant number value'</a>
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
					'<span class="token string">expression</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--scalar-expression-list">'scalar expression list'</a>
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
					'<span class="token string">expressions</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
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
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
		}
	)
}
</pre>
</div>
</div>
## Navigation
---
Navigation steps:
```js
.'My Property'          // get property value
?'My State'             // require state
>'My Text'              // get referenced node (for text properties with a reference)
.'My Text'&'Where'      // get 'where'-rule value from property
.&'My State Where'      // get 'where'-rule result from context state
.'My Collection'*       // iterate collection
--
^              // go to parent node
$^             // go to parent context with $ object
$              // select nearest $ object
@              // select nearest parameter node
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
			'<span class="token string">name</span>': stategroup (
				'<span class="token string">implicit</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">explicit</span>' {
					'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-variable-path">'ancestor variable path'</a>
					'<span class="token string">variable</span>': [ <span class="token operator">$</span> ] reference
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

{: #grammar-rule--descendant-base-property-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">descendant base property path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
	'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
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
		'<span class="token string">existence</span>' { }
		'<span class="token string">equality</span>' {
			'<span class="token string">expected node path</span>': [ <span class="token operator">is</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
		}
		'<span class="token string">containment</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">key path</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] group {
				'<span class="token string">path</span>': component <a href="#grammar-rule--conditional-node-path">'conditional node path'</a>
				'<span class="token string">text</span>': [ <span class="token operator">.</span> ] reference
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
		'<span class="token string">yes</span>' {
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
	'<span class="token string">name</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">implicit</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">explicit</span>' {
			'<span class="token string">name</span>': reference = first
			'<span class="token string">named objects</span>': dictionary { [ <span class="token operator">$</span> ]
				'<span class="token string">has successor</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { }
					| none = '<span class="token string">no</span>'
				)
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--named-object-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">named object assignment</span>' {
	'<span class="token string">name</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">implicit</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">explicit</span>' {
			'<span class="token string">name</span>': reference = first
			'<span class="token string">named objects</span>': dictionary { [ <span class="token operator">$</span> ]
				'<span class="token string">has successor</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { }
					| none = '<span class="token string">no</span>'
				)
			}
		}
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
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
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
### Navigation for references & derivations

{: #grammar-rule--named-object-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">named object step</span>' {
	'<span class="token string">name</span>': stategroup (
		'<span class="token string">implicit</span>' { [ <span class="token operator">$</span> ] }
		'<span class="token string">explicit</span>' {
			'<span class="token string">head</span>': component <a href="#grammar-rule--ancestor-named-object-path">'ancestor named object path'</a>
			'<span class="token string">named object</span>': [ <span class="token operator">$</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--context-object-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context object step</span>' {
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">this</span>' { }
		'<span class="token string">variable</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--named-object-step">'named object step'</a>
		}
		'<span class="token string">dynamic user</span>' { [ <span class="token operator">user</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--group-ancestor-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">group ancestor node path</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--group-ancestor-node-path">'group ancestor node path'</a>
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
	'<span class="token string">property</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--where-rule-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">where rule step</span>' {
	'<span class="token string">rule</span>': reference
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
			'<span class="token string">property</span>': [ <span class="token operator">></span> ] component <a href="#grammar-rule--property-step">'property step'</a>
		}
		'<span class="token string">reference rule</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] component <a href="#grammar-rule--property-step">'property step'</a>
			'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] component <a href="#grammar-rule--where-rule-step">'where rule step'</a>
		}
		'<span class="token string">state context rule</span>' {
			'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] component <a href="#grammar-rule--where-rule-step">'where rule step'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--reference-set-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference set step</span>' {
	'<span class="token string">reference set</span>': [ <span class="token operator"><</span> ] reference
}
</pre>
</div>
</div>

{: #grammar-rule--object-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object path tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">parent</span>' { [ <span class="token operator">^</span> ] }
				'<span class="token string">property value</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] component <a href="#grammar-rule--property-step">'property step'</a>
				}
				'<span class="token string">dependency</span>' {
					'<span class="token string">dependency</span>': component <a href="#grammar-rule--dependency-step">'dependency step'</a>
				}
				'<span class="token string">reference set</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--reference-set-step">'reference set step'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--plural-object-path-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural object path tail</span>' {
	'<span class="token string">has steps</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">*</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--plural-object-path-tail">'plural object path tail'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--plural-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural object path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--variablized-object-path">'variablized object path'</a>
	'<span class="token string">path</span>': component <a href="#grammar-rule--plural-object-path-tail">'plural object path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--descendant-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">descendant object path</span>' {
	'<span class="token string">path</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--variablized-object-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variablized object path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--context-object-step">'context object step'</a>
	'<span class="token string">path</span>': component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
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

{: #grammar-rule--object-set-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">object set path</span>' {
	'<span class="token string">collection path</span>': component <a href="#grammar-rule--singular-variablized-object-path">'singular variablized object path'</a>
	'<span class="token string">value path</span>': [ <span class="token operator">*</span> ] component <a href="#grammar-rule--object-path-tail">'object path tail'</a>
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
## User interface annotations
---
User interface annotations, or annotations for short, are recognizable by the
`@` character before the keyword. E.g. `@default:`. Most annotations
affect generated user interfaces (a system of type `auto-webclient`); they typically
do not affect custom user interfaces (system type `webclient`).

It is possible to use multiple annotations on a single property. Be aware that
they should be added in a specific order. Consult this grammar for the order of
annotations.

### Overview
Different attribute types support the same types of annotations.
This overview presents the commonly used annotations that different attribute types share.
#### Defaults
Most property types support the `@default:` annotation. Defaults apply default values to properties of new
nodes only and fail silently. That is, if the path contains a state navigation step and the
stategroup is not in that state, the default won't be applied. In the following
example the `Score` property will not be set when the state of `Default Score`
is anything other than `Known`.

```js
'Score': number positive 'score' @default: .'Default Score'?'Known'.'Value'
```

A default value is not necessarily a valid value. If validation
rules or constraints apply, a default value can be invalid.
When a derived value is used, make sure it is not a part of the new
node. Derived values on new nodes are computed after the node is saved,
and will therefore not be included in default values.
For example, this initializes the `Description` with `Deliver  pieces`:

```js
'Description': text @default: concat ( "Deliver ", to-text .'To deliver', " pieces." )
'To deliver' : number 'pieces' = ^ >'Order'.'Amount'
```
#### Descriptions
All attribute types support the `@description:` annotation.
This annotation adds additional information about an attribute: what it is meant for.
Alan GUI's typically present it as alt text, or a compact description at an input field.
#### Visibility
Commands and attributes that hold derived values, support the `@hidden` annotation.
The annotation hides an attribute from the UI.
#### Identifying properties
Properties that are important for the identification of a collection entry can be marked
with the `@identifying` annotation. Identifying properties are shown together with the
unique identifier of a collection entry, whenever the entry is referenced.
For example, when an employee has a uniquely identifying personnel number
in a collection of employees, a reference to employee will show the name of the employee
when the 'name' property is marked as identifying.


{: #grammar-rule--ui-identifying-property-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui identifying property selection</span>' {
	'<span class="token string">has properties</span>': stategroup = node-switch .'<span class="token string">properties</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">value type</span>': stategroup (
			'<span class="token string">scalar</span>' { }
			'<span class="token string">node</span>' {
				'<span class="token string">selection</span>': component <a href="#grammar-rule--ui-identifying-property-selection">'ui identifying property selection'</a>
			}
			'<span class="token string">choice</span>' {
				'<span class="token string">state key is identifying</span>': stategroup (
					'<span class="token string">no</span>' { [ <span class="token operator">@hidden</span> ] }
					'<span class="token string">yes</span>' { }
				)
				'<span class="token string">first state</span>': reference = first
				'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
					'<span class="token string">has successor</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">selection</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-identifying-property-selection">'ui identifying property selection'</a>
				}
			}
		)
	}
}
</pre>
</div>
</div>
#### Icons
For better visual identification, attributes support the `@icon:` annotation
attribute. As an argument it takes an icon name. A complete list of the
supported icons can be found at: [fonts.google.com/icons](https://fonts.google.com/icons).

### Actions


{: #grammar-rule--ui-action-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui action attribute</span>' {
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>
An action attribute describes a sequence of actions (operations), as explained in the section on [action attributes](#action-attributes).


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
The keyword `interactive` instructs your application to display a screen to the user for applying/executing an operation.

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
The keyword `show` presents the result of an operation after performing it.

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
	'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
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
			'<span class="token string">path</span>': group {
				'<span class="token string">path</span>': component <a href="#grammar-rule--ui-parametrized-node-path">'ui parametrized node path'</a>
				'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
			}
			'<span class="token string">states</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
				'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
			}
		}
		'<span class="token string">node switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">expression</span>': component <a href="#grammar-rule--node-expression">'node expression'</a>
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { dynamic-order
				'<span class="token string">node case</span>': [ <span class="token operator">|</span> <span class="token operator">node</span> ] group {
					'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
				}
				'<span class="token string">none case</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> ] group {
					'<span class="token string">expression</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ui-expression">'ui expression'</a>
				}
			}
		}
		'<span class="token string">walk</span>' { [ <span class="token operator">walk</span> ]
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">collection</span>': [ <span class="token operator">.</span>, <span class="token operator">*</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
			'<span class="token string">variable assignment</span>': component <a href="#grammar-rule--optional-variable-assignment">'optional variable assignment'</a>
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
			'<span class="token string">interaction</span>': component <a href="#grammar-rule--ui-action-interaction">'ui action interaction'</a>
			'<span class="token string">path</span>': component <a href="#grammar-rule--singular-node-path">'singular node path'</a>
			'<span class="token string">operation</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
		}
		'<span class="token string">produce value</span>' {
			'<span class="token string">value</span>': stategroup (
				'<span class="token string">object</span>' {
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-object-expression">'ui object expression'</a>
				}
				'<span class="token string">state</span>' {
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
				'<span class="token string">auto increment</span>' { [ <span class="token operator">auto-increment</span> ]
					'<span class="token string">scope</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
				}
				'<span class="token string">static</span>' {
					'<span class="token string">value</span>': text
				}
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
				'<span class="token string">constant</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--constant-number-value">'constant number value'</a>
				}
				'<span class="token string">now in seconds</span>' { [ <span class="token operator">now</span> ] }
				'<span class="token string">unary expression</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">absolute value</span>' { [ <span class="token operator">abs</span> ] }
						'<span class="token string">numerical type conversion</span>' { [ <span class="token operator">from</span> ]
							'<span class="token string">representation based</span>': stategroup (
								'<span class="token string">ui date and time</span>' { [ <span class="token operator">@date-time</span> ] }
								'<span class="token string">no</span>' { }
							)
							'<span class="token string">conversion</span>': reference
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
					'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--ui-scalar-value-expression-list">'ui scalar value expression list'</a>
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
					'<span class="token string">expressions</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
						'<span class="token string">left</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
						'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
					}
				}
			)
		}
		'<span class="token string">style</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">property</span>' { [ <span class="token operator">to-color</span> ]
					'<span class="token string">expression</span>': component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
				}
				'<span class="token string">fixed</span>' {
					'<span class="token string">style</span>': component <a href="#grammar-rule--ui-style">'ui style'</a>
				}
			)
		}
		'<span class="token string">state</span>' {
			'<span class="token string">state</span>': reference
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--ui-parametrized-node-path">'ui parametrized node path'</a>
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
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
		'<span class="token string">yes</span>' { [ <span class="token operator">||</span> ]
			'<span class="token string">fallback</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-style }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui style</span>' {
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">foreground</span>' { [ <span class="token operator">foreground</span> ] }
		'<span class="token string">background</span>' { [ <span class="token operator">background</span> ] }
		'<span class="token string">brand</span>' { [ <span class="token operator">brand</span> ] }
		'<span class="token string">link</span>' { [ <span class="token operator">link</span> ] }
		'<span class="token string">accent</span>' { [ <span class="token operator">accent</span> ] }
		'<span class="token string">success</span>' { [ <span class="token operator">success</span> ] }
		'<span class="token string">warning</span>' { [ <span class="token operator">warning</span> ] }
		'<span class="token string">error</span>' { [ <span class="token operator">error</span> ] }
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
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">value type</span>': stategroup (
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' { }
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--node-type-id-path">'node type id path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-property-classification }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui property classification</span>' {
	'<span class="token string">classification</span>': stategroup (
		'<span class="token string">identifying</span>' { [ <span class="token operator">@identifying</span> ] }
		'<span class="token string">outlining</span>' { [ <span class="token operator">@outlining</span> ] }
		'<span class="token string">standard</span>' { }
		'<span class="token string">hidden</span>' { [ <span class="token operator">@hidden</span> ] }
	)
}
</pre>
</div>
</div>
### Commands

{: #grammar-rule--ui-command-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui command attribute</span>' { dynamic-order
	'<span class="token string">visible</span>': stategroup (
		'<span class="token string">true</span>' { }
		'<span class="token string">false</span>' { [ <span class="token operator">@hidden</span> ] }
	)
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>
### Groups
The `@breakout` annotation indicates that a group property
should not be displayed together with the other properties. At the time of
this writing, the group is put in a separate tab in the details view of an entry.
Note that the tab is always added to the top level tabs of a details view.
That is, if a group is inside a state or another group, it is not added to the tabs of the state.

{: #grammar-rule--ui-group-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui group property</span>' { dynamic-order
	'<span class="token string">classification</span>': component <a href="#grammar-rule--ui-property-classification">'ui property classification'</a>
	'<span class="token string">break out</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@breakout</span> ] }
	)
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>
### Collections
The `@default:` annotation copies entries of a source collection into the annotated collection.
A subset of the entries from the source collection can be copied by specifying a state filter:

```js
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

```js
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

```js
'Imported Categories': collection ['Id'] {
	'Id': text
}
'Gegevens': collection ['Id'] @default: >'Category' {
	'Id': text /* -> some constraint or not */
	'Category': text ~> ^ .'Imported Categories'[] = .'Id'
}
```

{: #grammar-rule--ui-collection-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui collection property</span>' { dynamic-order
	'<span class="token string">sort</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' {
			'<span class="token string">direction</span>': stategroup (
				'<span class="token string">ascending</span>' { [ <span class="token operator">@ascending:</span> ] }
				'<span class="token string">descending</span>' { [ <span class="token operator">@descending:</span> ] }
			)
			'<span class="token string">path</span>': component <a href="#grammar-rule--ui-node-path">'ui node path'</a>
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
		}
	)
	'<span class="token string">classification</span>': component <a href="#grammar-rule--ui-property-classification">'ui property classification'</a>
	'<span class="token string">break out</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@breakout</span> ] }
	)
	'<span class="token string">size</span>': stategroup (
		'<span class="token string">small</span>' { [ <span class="token operator">@small</span> ] }
		'<span class="token string">large</span>' { }
	)
	'<span class="token string">can be dormant</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@dormant:</span> ]
			'<span class="token string">expression</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
		}
	)
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">default</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">key reference</span>': component <a href="#grammar-rule--entry-reference-selector">'entry reference selector'</a>
			'<span class="token string">entry filter</span>': component <a href="#grammar-rule--node-path-tail">'node path tail'</a>
		}
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
	'<span class="token string">has style</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@style:</span> ]
			'<span class="token string">style expression</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
		}
	)
}
</pre>
</div>
</div>
### Numbers

{: #grammar-rule--ui-number-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui number property</span>' { dynamic-order
	'<span class="token string">classification</span>': component <a href="#grammar-rule--ui-property-classification">'ui property classification'</a>
	'<span class="token string">emphasis</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@emphasis</span> ] }
	)
	'<span class="token string">default</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">dynamic numerical type</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@numerical-type:</span> ]
			'<span class="token string">binding path</span>': component <a href="#grammar-rule--node-path">'node path'</a>
		}
	)
	'<span class="token string">metadata</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@metadata</span> ] }
	)
	'<span class="token string">validation</span>': group {
		'<span class="token string">has minimum</span>': stategroup (
			'<span class="token string">no</span>' { }
			'<span class="token string">yes</span>' { [ <span class="token operator">@min:</span> ]
				'<span class="token string">minimum</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
			}
		)
		'<span class="token string">has maximum</span>': stategroup (
			'<span class="token string">no</span>' { }
			'<span class="token string">yes</span>' { [ <span class="token operator">@max:</span> ]
				'<span class="token string">maximum</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
			}
		)
	}
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>
### Files

{: #grammar-rule--ui-file-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui file property</span>' { dynamic-order
	'<span class="token string">file name expression</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@name:</span> ]
			'<span class="token string">file name expression</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">classification</span>': component <a href="#grammar-rule--ui-property-classification">'ui property classification'</a>
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>
### Texts

{: #grammar-rule--ui-text-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui text property</span>' { dynamic-order
	'<span class="token string">classification</span>': component <a href="#grammar-rule--ui-property-classification">'ui property classification'</a>
	'<span class="token string">emphasis</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@emphasis</span> ] }
	)
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">default</span>' { }
		'<span class="token string">multi-line</span>' { [ <span class="token operator">@multi-line</span> ] }
		'<span class="token string">color</span>' { [ <span class="token operator">@color</span> ] }
		'<span class="token string">url</span>' { [ <span class="token operator">@url</span> ] }
		'<span class="token string">markdown</span>' { [ <span class="token operator">@markdown</span> ] }
		'<span class="token string">html</span>' { [ <span class="token operator">@html</span> ] }
	)
	'<span class="token string">default value</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">has validation</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@validate:</span> ]
			'<span class="token string">rules</span>': component <a href="#grammar-rule--ui-text-validation">'ui text validation'</a>
		}
	)
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
	'<span class="token string">has custom identifying properties</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@show:</span> ]
			'<span class="token string">selection</span>': component <a href="#grammar-rule--ui-identifying-property-selection">'ui identifying property selection'</a>
		}
	)
	'<span class="token string">is label</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@label</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--ui-reference-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui reference rule</span>' { //dynamic-order
	'<span class="token string">has validation</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@validate:</span> <span class="token operator">resolvable</span> ] }
	)
}
</pre>
</div>
</div>
### State groups

{: #grammar-rule--ui-state-group-property }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui state group property</span>' { dynamic-order
	'<span class="token string">classification</span>': component <a href="#grammar-rule--ui-property-classification">'ui property classification'</a>
	'<span class="token string">emphasis</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@emphasis</span> ] }
	)
	'<span class="token string">default state</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@default:</span> ]
			'<span class="token string">default</span>': component <a href="#grammar-rule--ui-scalar-default">'ui scalar default'</a>
		}
	)
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
}
</pre>
</div>
</div>
### States

{: #grammar-rule--ui-state }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui state</span>' { dynamic-order
	'<span class="token string">desired state</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@desired</span> ] }
	)
	'<span class="token string">verified state</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@verified</span> ] }
	)
	'<span class="token string">icon</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@icon:</span> ]
			'<span class="token string">name</span>': text
		}
	)
	'<span class="token string">has style</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@style:</span> ]
			'<span class="token string">style expression</span>': component <a href="#grammar-rule--ui-expression">'ui expression'</a>
		}
	)
	'<span class="token string">transitions</span>': dictionary { [ <span class="token operator">@transition:</span> ]
		'<span class="token string">action</span>': [ <span class="token operator">=></span> <span class="token operator">execute</span> ] reference
	}
}
</pre>
</div>
</div>
### Todo items

{: #grammar-rule--ui-todo }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui todo</span>' {
	'<span class="token string">has description</span>': stategroup (
		'<span class="token string">no</span>' { }
		'<span class="token string">yes</span>' { [ <span class="token operator">@description:</span> ]
			'<span class="token string">description</span>': text
		}
	)
}
</pre>
</div>
</div>
### Numerical types

{: #grammar-rule--ui-numerical-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ui numerical type</span>' {
	'<span class="token string">represent as</span>': stategroup (
		'<span class="token string">model</span>' { }
		'<span class="token string">date</span>' { [ <span class="token operator">@date</span> ] }
		'<span class="token string">date and time</span>' { [ <span class="token operator">@date-time</span> ] }
		'<span class="token string">duration</span>' { [ <span class="token operator">@duration:</span> ]
			'<span class="token string">unit</span>': stategroup (
				'<span class="token string">seconds</span>' { [ <span class="token operator">seconds</span> ] }
				'<span class="token string">minutes</span>' { [ <span class="token operator">minutes</span> ] }
				'<span class="token string">hours</span>' { [ <span class="token operator">hours</span> ] }
			)
		}
		'<span class="token string">custom type</span>' { [ <span class="token operator">@numerical-type:</span> ]
			'<span class="token string">binding</span>': stategroup (
				'<span class="token string">root</span>' { }
				'<span class="token string">dynamic</span>' { [ <span class="token operator">bind</span> ]
					'<span class="token string">path</span>': component <a href="#grammar-rule--node-type-id">'node type id'</a>
					'<span class="token string">assignment</span>': component <a href="#grammar-rule--variable-assignment">'variable assignment'</a>
				}
			)
			'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
				'<span class="token string">label</span>': [ <span class="token operator">label:</span> ] component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
				'<span class="token string">conversion</span>': stategroup (
					'<span class="token string">none</span>' { }
					'<span class="token string">point translation</span>' {
						'<span class="token string">decimals</span>': [ <span class="token operator">decimals:</span> ] component <a href="#grammar-rule--ui-scalar-value-expression">'ui scalar value expression'</a>
					}
				)
			}
		}
	)
}
</pre>
</div>
</div>
