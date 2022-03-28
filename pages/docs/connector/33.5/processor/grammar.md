---
layout: doc
origin: connector
language: processor
version: 33.5
type: grammar
---

1. TOC
{:toc}

### The Standard Libraries
The connector provides a set of standard libraries.
These libraries provide functionality outside the language constructs of the connector.

#### Calendar
The calendar library provides conversions between the connectors internal date time representation and broken down time.

```js
define 'type' as @API choice ( 'date' 'date-time' 'time' )

define 'weekday' as @API choice (
	'Monday':    1
	'Tuesday':   2
	'Wednesday': 3
	'Thursday':  4
	'Friday':    5
	'Saturday':  6
	'Sunday':    7
)

define 'calendar' as @API {
	'year': integer
	'day of year': integer
	'month': integer
	'day of month': integer
	'week': integer
	'day of week': 'weekday'
	'hour': integer
	'minute': integer
	'second': integer
}

library
	/* Converts Alan Time to broken down time.
	 * When information is not present in the source, it is set to zero.
	 */
	function 'convert'
		< integer , 'calendar' >
		(
			$'source type': 'type'
			$'timezone': optional text
		)
		binds: "c5e5166832c5eb9eec7481afa9c4a3c9689a1b6a"
```

#### Network
The network library provides functions to perform network request and the data structures to represent related objects.

```js
define 'network method' as @API choice ( 'get' 'head' 'post' 'put' 'delete' )
define 'network security' as @API choice ( 'strict' 'preferred' 'none' )
define 'key value list' as @API collection unicode case folding text

define 'network request' as @API {
	'method': 'network method'
	'parameters': optional 'key value list'
	'headers': optional 'key value list'
	'content': optional text
}
define 'network response' as @API {
	'status': integer
	'headers': 'key value list'
	'content': text
}

define 'network authentication' as @API {
	'username': text
	'password': text
}

define 'network message part' as @API {
	'mime type': text
	'mime sub type': text
	'content': text
}
define 'network message' as @API {
	'from': 'key value list'
	'recipients': 'key value list'
	'recipients extra': optional 'key value list'
	'recipients hidden': optional 'key value list'
	'subject': optional text
	'headers': optional 'key value list'
	'attachments': optional list {
		'name': text
		'part': 'network message part'
	}
	'body': 'network message part'
}

library
	/* Parses and decorates text as 'network message'.
	 * Optionally a 'preferred mime subtype' of MIME type `text` can be provided.
	 * When a MIME part with this type is found, it becomes a candidate for the body.
	 * The MIME type `text/plain` is always considered as a candidate for the body.
	 */
	function 'parse network message'
		< text , unsafe 'network message' >
		(
			$'preferred mime subtype': text
		)
		binds: "a9727dd7a7a001ff7ced169b93e6b209d03ffe96"

	/* Performs an HTTP(S) request.
	 * Methods are mapped directly to their HTTP equivalent.
	 * When provided, 'content' is send with the request.
	 */
	function 'http'
		< boolean , unsafe 'network response' >
		(
			$'server': text
			$'path': text
			$'authentication': optional 'network authentication'
			$'request': 'network request'
		)
		binds: "26b4d11d4f2a785d5c80be5aec16b94ef739cb8f"

	/* Performs an FTP(S) request.
	 * Method mapping:
	 *  > 'get': Retrieves the content of 'path'. For this to work on directories, 'path' must end with a slash (/).
	 *  > 'head': Retrieves the directory entries at 'path' without meta data. 'path' must be a directory, but does not need to end with a slash (/).
	 *  > 'post': Stores 'content' in 'path'.
	 *  > 'put': Identical to 'post'.
	 *  > 'delete': Attempts to remove 'path'. Unlike other methods, this transmits 'path' directly to the server for interpretation.
	 * Only when storing data, should content be set.
	 */
	function 'ftp'
		< boolean , unsafe optional text >
		(
			$'server': text
			$'path': text
			$'method': 'network method'
			$'authentication': optional 'network authentication'
			$'security': 'network security'
			$'content': optional text
		)
		binds: "7752d005d762c5aad87720bffe634d7ca012f833"

	/* Retrieves all messages matching 'criteria' with IMAP(S).
	 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
	 * All messages are parsed as if passed to `function 'parse network message'`.
	 */
	function 'imap'
		< boolean , unsafe plural 'network message' >
		(
			$'server': text
			$'path': text
			$'criteria': text
			$'authentication': optional 'network authentication'
			$'security': 'network security'
			$'preferred mime subtype': text
		)
		binds: "fdf2d49d643d45d11f8312665743db62e4cbc3b0"

	/* Send a message with SMTP(S).
	 * When the transfer fails, this function throws an error.
	 */
	function 'smtp'
		< boolean , unsafe boolean >
		(
			$'server': text
			$'authentication': optional 'network authentication'
			$'security': 'network security'
			$'message': 'network message'
		)
		binds: "eee8e142b5a92d5fd361a3865a0fd1d44250e99f"

	/* Register webserver handlers.
	 * The handler is used as the path to respond to.
	 * Each handler is triggered by external web requests for the path.
	 */
	hook 'webserver'
		on 'network response'
		(
			$'request': 'network request'
		)
		binds: "3646e76f83861027942b241a95a2e91c023873bd"
```

#### Plural
The plural library provides algorithms operating on sets.

```js
library
	/* Sorts a set based on a comparison function.
	 */
	function 'sort'
		< template plural T , plural T , plural T >
		(
			$'compare': lambda on boolean (
				$'A': T
				$'B': T
			)
		)
		binds: "354397a819e32138d5f64e235fa01fcdd218403a"

	/* Selects a single entry in a set based on a comparison function.
	 * This returns the entry for which `compare` results in true when the entry is `A` and false when `B` compared to all other entries in the set.
	 * It fails when no such entry is found.
	 */
	function 'select'
		< template plural T , plural T , unsafe T >
		(
			$'compare': lambda on boolean (
				$'A': T
				$'B': T
			)
		)
		binds: "7bc2180c97c2a18d32e8b9334b7027cf09ca475d"

	/* Filters a set.
	 * This returns a new set containing only the entries for which `filter` results in true.
	 */
	function 'filter'
		< template plural T , plural T , plural T >
		(
			$'filter': lambda on boolean (
				$'entry': T
			)
		)
		binds: "c34096effde804589af15914169b375ff34b2b20"
```

#### Unicode
The unicode library provides functions to manipulate text values.
These functions require UTF-8 encoded data.

```js
define 'trim style' as @API choice ( 'leading' 'trailing' 'both' 'none' )

library
	/* Removes leading and/or trailing whitespace from a text value.
	 */
	function 'trim'
		< text , text >
		(
			$'style': 'trim style'
		)
		binds: "90f6a92fc16f3c79c5095ce69994ed3f31012470"

	/* Split a text into multiple fragments.
	 * Empty fragments are automatically removed.
	 */
	function 'split'
		< text , plural text >
		(
			$'style': 'trim style'
		)
		binds: "f0ac58660348a12cbcbd257438034886f34dfd1a"
```
### Processor
#### The internal library.
Allows defining reusable types.

{: #grammar-rule--library }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library</span>': dictionary { [ <span class="token operator">define</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
		'<span class="token string">schema</span>' {
			/* Define a schema type.
			 * Optionally the `@API` option can be used to suppress usages analysis.
			 */
			'<span class="token string">analysis</span>': stategroup (
				'<span class="token string">API</span>' { [ <span class="token operator">@API</span> ] }
				'<span class="token string">full</span>' { }
			)
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">pattern</span>' { [ <span class="token operator">pattern</span> ]
			/* Define a pattern.
			 */
			'<span class="token string">analysis</span>': stategroup (
				'<span class="token string">API</span>' { [ <span class="token operator">@API</span> ] }
				'<span class="token string">full</span>' { }
			)
			'<span class="token string">rule</span>': component <a href="#grammar-rule--pattern-rule">'pattern rule'</a>
		}
		'<span class="token string">locale</span>' { [ <span class="token operator">locale</span> ]
			/* Define a custom locale.
			 */
			'<span class="token string">positive sign</span>': [ <span class="token operator">positive-sign:</span> ] text
			'<span class="token string">negative sign</span>': [ <span class="token operator">negative-sign:</span> ] text
			'<span class="token string">decimal point</span>': [ <span class="token operator">decimal-point:</span> ] text
		}
	)
}
</pre>
</div>
</div>
#### The default locale.
Allows overwriting the builtin default locale.

{: #grammar-rule--custom-locale }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom locale</span>': stategroup (
	'<span class="token string">yes</span>' {
		/* Use a custom locale as the default.
		 * All locale dependent operations without an explicit locale use this locale.
		 */
		'<span class="token string">default</span>': [ <span class="token operator">default-locale:</span> ] component <a href="#grammar-rule--library-selector">'library selector'</a>
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>
#### The type of the connector.
This is chosen externally, the archetype here must follow the external choice.

{: #grammar-rule--archetype }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">archetype</span>': stategroup (
	'<span class="token string">scheduled provider</span>' { [ <span class="token operator">provider</span> ]
		/* The connector is an Alan Interface Provider.
		 * As a provider, the connector runs the main routine based on an external schedule.
		 * Optionally, command handlers can be provided.
		 */
		/* Main routine.
		 * Each run of the main routine must create a snapshot of the current state.
		 * As a result the current state must always be a complete dataset and not an update to a previous dataset.
		 */
		'<span class="token string">main routine</span>': component <a href="#grammar-rule--statement">'statement'</a>
		/* Dataset initialization.
		 * Before a provider can process command and generate events, a dataset is required.
		 * When available, the last result of the main routine is used as dataset.
		 * Otherwise the initialization is used to determine the initial dataset.
		 */
		'<span class="token string">initialization</span>': stategroup (
			'<span class="token string">custom</span>' { [ <span class="token operator">init</span> ]
				/* Use a custom routine to generate the initial dataset.
				 * This can be used to prevent additional runs of the main routine when this would exceed rate limits/query quotas.
				 */
				'<span class="token string">routine</span>': component <a href="#grammar-rule--statement">'statement'</a>
			}
			'<span class="token string">main</span>' { [ <span class="token operator">init</span> <span class="token operator">main</span> ]
				/* Use the main routine to generate the initial dataset.
				 * This run of the main routine is in addition to runs caused by the external schedule.
				 */
			}
			'<span class="token string">none</span>' {
				/* Do not generate an initial dataset.
				 * Received commands are ignored until the main routine is triggered.
				 */
			}
		)
		/* Command routines.
		 * These routines are run when the corresponding command is received.
		 * Commands can have multiple handlers. When the command is received, all handlers are executed in an undefined order.
		 * Received commands for which no handlers exist are ignored.
		 */
		'<span class="token string">routines</span>': dictionary { [ <span class="token operator">routine</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			/* The command the routine binds to.
			 * The command data is available in `$`.
			 */
			'<span class="token string">command</span>': [ <span class="token operator">on</span> <span class="token operator">command</span> ] reference
			/* The path to the node the command is defined at.
			 * The path becomes the initial scope of the routine.
			 */
			'<span class="token string">named type</span>': component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">execute</span>' {
					/* Execute a statement.
					 * From this context Alan Interface events can be executed.
					 */
					'<span class="token string">statement</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">schedule</span>' { [ <span class="token operator">schedule</span> ]
					/* Schedule a run of the main routine immediately after the command.
					 * The main routine is run, and consumers are updated, regardless of the external schedule.
					 * This run of the main routine is in addition to runs caused by the external schedule.
					 * These additional runs are scheduled regardless of the current dataset state.
					 */
				}
			)
		}
		/* The hooks.
		 * See `Library Hooks` for more information.
		 */
		'<span class="token string">hooks</span>': set {
			'<span class="token string">hook</span>': component <a href="#grammar-rule--library-hook">'library hook'</a>
		}
	}
	'<span class="token string">consumer</span>' { [ <span class="token operator">consumer</span> ]
		/* The connector is an Alan Interface Consumer.
		 * As a consumer, the connector runs routines based on the nodes touched by updates or received events.
		 */
		/* The context keys on which to subscribe.
		  * CAVEAT: The context keys are only evaluated once at startup.
		  */
		'<span class="token string">context keys</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		/* The routines.
		 * Each routine is bound to something in the interface.
		 * The routine is triggered based on the interface binding.
		 */
		'<span class="token string">routines</span>': dictionary { [ <span class="token operator">routine</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">binding</span>': [ <span class="token operator">on</span> ] stategroup (
				'<span class="token string">event</span>' {
					/* The routine binds to an event.
					 * When the event is received, the routine is run.
					 * The event data is available in `$`.
					 */
					'<span class="token string">event</span>': [ <span class="token operator">event</span> ] reference
				}
				'<span class="token string">node</span>' {
					/* The routine binds to a node.
					 * When the node is touched by an update, the routine is run.
					 * The routine is only run after the update is fully processed.
					 * As a result, the routine always has a fully initialized dataset available, but is not informed which data was updated.
					 */
				}
			)
			/* The path to the node the routine binds to or the event is defined at.
			 * The path becomes the initial scope of the routine.
			 */
			'<span class="token string">named type</span>': component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
			/* From this context Alan Interface events can be executed.
			 */
			'<span class="token string">statement</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		/* The hooks.
		 * See `Library Hooks` for more information.
		 */
		'<span class="token string">hooks</span>': set {
			'<span class="token string">hook</span>': component <a href="#grammar-rule--library-hook">'library hook'</a>
		}
	}
	'<span class="token string">library</span>' { [ <span class="token operator">library</span> ]
		/* The connector is a library.
		 * Currently only standard libraries are supported.
		 *
		 * A standard library consist of a set of function signatures.
		 * These functions are implemented by the connector runtime.
		 */
		'<span class="token string">functions</span>': dictionary { [ <span class="token operator">function</span> ]
			'<span class="token string">signature</span>': component <a href="#grammar-rule--signature">'signature'</a>
			'<span class="token string">binds</span>': [ <span class="token operator">binds:</span> ] text
		}
		/* A standard library can expose hooks.
		 * Each hook is triggered by external events.
		 */
		'<span class="token string">hooks</span>': dictionary { [ <span class="token operator">hook</span> ]
			'<span class="token string">signature</span>': component <a href="#grammar-rule--signature">'signature'</a>
			'<span class="token string">binds</span>': [ <span class="token operator">binds:</span> ] text
		}
	}
)
</pre>
</div>
</div>

{: #grammar-rule--library-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library selector</span>' {
	/* Select a type from a standard or the internal library.
	 */
	'<span class="token string">library</span>': stategroup (
		'<span class="token string">dependency</span>' {
			'<span class="token string">dependency</span>': [, <span class="token operator">/</span> ] reference
		}
		'<span class="token string">self</span>' { }
	)
	'<span class="token string">type</span>': reference
}
</pre>
</div>
</div>
#### Library Hook
The standard library defines hooks.
When or how these hooks are triggered is defined by the individual hooks.
Providers and consumers can add lambdas to these hooks.
These lambdas are executed when the hook is triggered.
Some hooks only trigger a subset of the added lambdas, based on the handler name.

Lambdas added to hooks can execute side-effects based on there context.
Providers can execute events.
Consumers can execute commands.

{: #grammar-rule--library-hook }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library hook</span>' {
	/* The standard library and hook to add the lambda to.
	 */
	'<span class="token string">library</span>': [ <span class="token operator">add-hook</span> ] reference
	'<span class="token string">hook</span>': [ <span class="token operator">::</span> ] reference
	/* The handler name.
	 * Usages of this value is defined by the individual hooks.
	 */
	'<span class="token string">name</span>': text
	/* The implementation to run when the hook is triggered.
	 * The root node of the interface data is available in `$`.
	 * The arguments for the library hook defined parameters become the initial scope.
	 */
	'<span class="token string">instance</span>': component <a href="#grammar-rule--callable-instance">'callable instance'</a>
	'<span class="token string">implementation</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--lambda-implementation">'lambda implementation'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--locale-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">locale selector</span>' {
	'<span class="token string">locale</span>': stategroup (
		'<span class="token string">custom</span>' {
			'<span class="token string">selector</span>': [ <span class="token operator">locale:</span> ] component <a href="#grammar-rule--library-selector">'library selector'</a>
		}
		'<span class="token string">default</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--interface-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface type path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">[]</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' { }
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--interface-type-path">'interface type path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
#### Interface Named Path
As the connector does not allow stepping from a child node to the parent, the path is segmented.
Each segment has a name and specifies a part of the path. This name is then assigned that node.
This allows a routine to access its parents by explicitly naming them.

{: #grammar-rule--interface-named-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface named path</span>' {
	'<span class="token string">segments</span>': dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has previous</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">previous</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">steps</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--interface-type-path">'interface type path'</a>
	}
	'<span class="token string">has segment</span>': stategroup = node-switch .'<span class="token string">segments</span>' (
		| nodes = '<span class="token string">yes</span>' {
			'<span class="token string">first</span>' = first
			'<span class="token string">last</span>' = last
		}
		| none  = '<span class="token string">no</span>'
	)
}
</pre>
</div>
</div>

{: #grammar-rule--comparator }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">comparator</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">unicode</span>' { [ <span class="token operator">unicode</span> ]
			/* The unicode comparator operates only on texts.
			 * It supports equality and relational comparisons.
			 */
			'<span class="token string">case folding</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">case</span> <span class="token operator">folding</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">simple</span>' {
			/* The simple comparator behaves depending on the it operates on.
			 *  > boolean: supports only equality comparisons
			 *  > integer: supports equality and relational comparisons
			 *  > text   : supports only equality comparisons, 2 texts are considered equal when they are bitwise identical
			 *  > file   : supports only equality comparisons, 2 files are considered equal when both text values are identical
			 */
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schema-scalar-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema scalar type</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">boolean</span>' { [ <span class="token operator">boolean</span> ]
			/* A boolean type can hold the value `true` or `false`.
			 */
		}
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
			/* An integer can hold numbers.
			 * Integers can not have a fraction.
			 */
			'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
			/* A text can hold any type of binary data.
			 * While a text can hold arbitrary binary data, all text operations require the data to be valid utf-8 encoded data.
			 * When data is encoded differently, it must first be converted.
			 * NOTE: The connector does not track the encoding of data.
			 *       Passing data not encoded as utf-8 to a text operation causes the operation to fail, even if the operation is normally guaranteed.
			 *       An encoding failure results in an implicit throw, bypassing any alternative handling present!
			 */
		}
		'<span class="token string">choice</span>' { [ <span class="token operator">choice</span> ]
			/* A choice can hold a single value from a user defined set of values.
			 * A choice has a base type, this type only effects parsing and serialization.
			 * So a choice with an integer base type cannot be compared to an actual integer.
			 */
			'<span class="token string">options</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">has next</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">base type</span>': stategroup (
					'<span class="token string">integer</span>' {
						'<span class="token string">value</span>': [ <span class="token operator">:</span> ] integer
					}
					'<span class="token string">text</span>' { }
				)
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schema-complex-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema complex type</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">any</span>' { [ <span class="token operator">any</span> ]
			/* Differed type.
			 * The type of this data can not yet be determined.
			 * This allows other data in the same schema to define the type of this by decorating this value at a later point.
			 */
		}
		'<span class="token string">library</span>' {
			/* Library type.
			 * This is not an actual type.
			 * The type of this data is the referred type.
			 */
			'<span class="token string">selector</span>': component <a href="#grammar-rule--library-selector">'library selector'</a>
		}
		'<span class="token string">union</span>' { [ <span class="token operator">union</span> ]
			/* Union type.
			 * The type of this data is conditional.
			 * Parsing is not able to determine the type, it must be explicitly give a type through a separate decorate step.
			 * Serialization does not include the type information and omits the value when the type was not yet determined.
			 */
			'<span class="token string">types</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">has next</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
			}
		}
		'<span class="token string">node</span>' {
			/* Node type.
			 * Parsing and serialization expects the type information (property names) to be present in the data.
			 */
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">headless</span>' { [ <span class="token operator">headless</span> ]
			/* Node type.
			 * Unlike the normal node type, this expects the data to be ordered and uses the property order during parsing and serialization.
			 */
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
			/* Set type.
			 * This holds a dynamic amount of data, or no data at all (empty set).
			 * Every entry in the set is an `entity` with an implicit key and a value of `type`.
			 * A comparator is used for matching the implicit keys.
			 */
			'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">list</span>' { [ <span class="token operator">list</span> ]
			/* Set type.
			 * This holds a dynamic amount of data, or no data at all (empty set).
			 * Every entry in the set is of `type`.
			 * Entries in a list have no unique identification.
			 */
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">table</span>' { [ <span class="token operator">table</span> ]
			/* Special set type.
			 * A table behaves as if it was a list of headless nodes, except for a special parsing/serialization specialization.
			 * The table expects the very first row in serialized from to be the header.
			 * This header must match all properties in the node, but can do so in any order.
			 * Unlike the headless node, where the property order is defined by the schema, the parsing/serialization order of all properties is defined by this header row.
			 */
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">scalar</span>' {
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-scalar-type">'schema scalar type'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schema-node-type }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema node type</span>' {
	/* A node is a container containing a static set of named values, the properties.
	 * When the document type supports it, each property itself can have a set of attributes.
	 * These attributes can either be a text (to be retrieved and processed later) or a filter (to reduce the possible matches in serialized form).
	 * A property can be marked as optional, an optional property may be omitted or have a special no value construct in serialized form.
	 *
	 * A property can be marked as protected, an protected property's data is always excluded from data dumps.
	 * This is to prevent the connector leaking sensitive data.
	 * NOTE: Using @protected is no guarantee the relevant data is never included.
	 *       When the sensitive that is also present in unprotected data, it will still be readable in that data.
	 */
	'<span class="token string">properties</span>': [ <span class="token operator">{</span>, <span class="token operator">}</span> ] dictionary {
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has attributes</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator"><</span>, <span class="token operator">></span> ]
				'<span class="token string">attributes</span>': dictionary {
					'<span class="token string">has next</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">type</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--schema-scalar-type">'schema scalar type'</a>
				}
				'<span class="token string">filters</span>': dictionary { [ <span class="token operator">where</span> ]
					'<span class="token string">has next</span>': stategroup = node-switch successor (
						| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
						| none = '<span class="token string">no</span>'
					)
					'<span class="token string">value</span>': [ <span class="token operator">is</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
				}
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">protect</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">@protected</span> ] }
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">is optional</span>': stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">optional</span> ] }
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--stack-block }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stack block</span>' {
	/* A stack block is a group of `let` expressions.
	 * With `let` expressions it is possible to store a value in a name.
	 * This value can be retrieved at a later point.
	 *
	 * A `let` expression is not a variable.
	 * Unlike a variable, a `let` expression is always given a value when it is declared.
	 * It also can never be assigned a different value at a later point.
	 */
	'<span class="token string">values</span>': dictionary { [ <span class="token operator">let</span> <span class="token operator">$</span> ]
		'<span class="token string">has previous</span>': stategroup = node-switch predecessor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">previous</span>' = predecessor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': stategroup (
			'<span class="token string">inferred</span>' {
				/* Source driven `let`.
				 * The result of the promise is assigned to the name.
				 * The type of this `let` is inferred from the promise.
				 */
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
			}
			'<span class="token string">schema</span>' {
				/* Target driven `let`.
				 * The type of this `let` is the type of the schema. It must be a node type.
				 * This executes the statement with the schema as target.
				 */
				'<span class="token string">schema</span>': [ <span class="token operator">as</span> ] component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
				'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			}
			'<span class="token string">lambda</span>' {
				/* Lambda `let`.
				 * The type of this `let` is a callable object.
				 */
				'<span class="token string">lambda</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--lambda-definition">'lambda definition'</a>
			}
		)
	}
}
</pre>
</div>
</div>

{: #grammar-rule--stack-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stack selector</span>' {
	/* Navigate the stack.
	 * Each frame on the stack is created by a scope.
	 */
	'<span class="token string">stack</span>': stategroup (
		'<span class="token string">non-empty</span>' {
			'<span class="token string">select</span>': stategroup (
				'<span class="token string">this frame</span>' {
					/* Select a value in the selected frame.
					 */
					'<span class="token string">value</span>': [ <span class="token operator">$</span> ] reference
				}
				'<span class="token string">parent frame</span>' {
					/* Select a value in the parent frame.
					 */
					'<span class="token string">tail</span>': [ <span class="token operator">^</span> ] component <a href="#grammar-rule--stack-selector">'stack selector'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--target-type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target type path step</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">command</span>' {
					'<span class="token string">command</span>': [ <span class="token operator">command</span> ] reference
				}
				'<span class="token string">event</span>' {
					'<span class="token string">event</span>': [ <span class="token operator">event</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--target-type-path-step">'target type path step'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--target-type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target type path</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
		'<span class="token string">absolute</span>' {
			'<span class="token string">root</span>': stategroup (
				'<span class="token string">interface</span>' { [ <span class="token operator">interface</span> ] }
				'<span class="token string">schema</span>' {
					'<span class="token string">selector</span>': component <a href="#grammar-rule--library-selector">'library selector'</a>
				}
				'<span class="token string">boolean</span>' { [ <span class="token operator">boolean</span> ] }
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
			'<span class="token string">steps</span>': component <a href="#grammar-rule--target-type-path-step">'target type path step'</a>
		}
		'<span class="token string">relative</span>' {
			'<span class="token string">steps</span>': component <a href="#grammar-rule--target-type-path-step">'target type path step'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type path step</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">indexed collection</span>' { [ <span class="token operator">[]</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
				}
				'<span class="token string">command</span>' {
					'<span class="token string">command</span>': [ <span class="token operator">command</span> ] reference
				}
				'<span class="token string">event</span>' {
					'<span class="token string">event</span>': [ <span class="token operator">event</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--type-path-step">'type path step'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--type-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type path</span>' {
	'<span class="token string">root</span>': stategroup (
		'<span class="token string">interface</span>' { [ <span class="token operator">interface</span> ] }
		'<span class="token string">schema</span>' {
			'<span class="token string">schema</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">context</span>' { [ <span class="token operator">context</span> ] }
	)
	'<span class="token string">steps</span>': component <a href="#grammar-rule--type-path-step">'type path step'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--type-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type definition</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">file</span>' { [ <span class="token operator">file</span> ] }
		'<span class="token string">optional</span>' { [ <span class="token operator">optional</span> ]
			'<span class="token string">sub type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">plural</span>' { [ <span class="token operator">plural</span> ]
			'<span class="token string">sub type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">lambda</span>' {
			'<span class="token string">signature</span>': [ <span class="token operator">lambda</span> ] component <a href="#grammar-rule--signature">'signature'</a>
		}
		'<span class="token string">type</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--type-path">'type path'</a>
		}
		'<span class="token string">template</span>' { [ <span class="token operator">T</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--signature-parameters }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signature parameters</span>' {
	/* Parameter definition of a callable object.
	 */
	'<span class="token string">parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has next</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--type-definition">'type definition'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--signature-promise }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signature promise</span>' {
	/* The signature of a callable object.
	 * This represents a callable object that must be called in a promise chain context.
	 */
	'<span class="token string">template</span>': [ <span class="token operator"><</span> ] stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">requirement</span>': [ <span class="token operator">template</span>, <span class="token operator">T</span> <span class="token operator">,</span> ] stategroup (
				'<span class="token string">plural</span>' { [ <span class="token operator">plural</span> ] }
				'<span class="token string">optional</span>' { [ <span class="token operator">optional</span> ] }
				'<span class="token string">none</span>' { }
			)
		}
		'<span class="token string">no</span>' { }
	)
	/* The type of the input.
	 * When written inline, the input type can be inferred (implicit).
	 */
	'<span class="token string">context</span>': stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">context</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">implicit</span>' { }
	)
	/* The promise guarantee of the callable object.
	 */
	'<span class="token string">guarantee</span>': [ <span class="token operator">,</span> ] stategroup (
		'<span class="token string">yes</span>' { }
		'<span class="token string">no</span>' { [ <span class="token operator">unsafe</span> ] }
	)
	/* The type of the output.
	 */
	'<span class="token string">result</span>': [, <span class="token operator">></span> ] component <a href="#grammar-rule--type-definition">'type definition'</a>
	/* The parameter definition.
	 */
	'<span class="token string">parameters</span>': component <a href="#grammar-rule--signature-parameters">'signature parameters'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--signature-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signature statement</span>' {
	/* The signature of a callable object.
	 * This represents a callable object that must be called as a statement.
	 */
	/* The target the callable object must be called on.
	 * When written inline, the target can be inferred.
	 */
	'<span class="token string">target</span>': stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--target-type-path">'target type path'</a>
		}
		'<span class="token string">inferred</span>' { }
	)
	/* The parameter definition.
	 */
	'<span class="token string">parameters</span>': component <a href="#grammar-rule--signature-parameters">'signature parameters'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--signature }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signature</span>' {
	/* The signature of a callable object.
	 */
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">promise</span>' {
			'<span class="token string">signature</span>': component <a href="#grammar-rule--signature-promise">'signature promise'</a>
		}
		'<span class="token string">statement</span>' {
			'<span class="token string">signature</span>': component <a href="#grammar-rule--signature-statement">'signature statement'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--callable-instance }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">callable instance</span>' {
	'<span class="token string">template</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator"><</span>, <span class="token operator">></span> ]
			'<span class="token string">type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-implementation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda implementation</span>' {
	/* The implementation of a lambda.
	 * Currently lambdas can only be statements.
	 */
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">statement</span>' {
			'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-argument }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda argument</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">optional</span>' {
			/* Set an optional parameter.
			 * Lambda arguments must always explicitly set or unset.
			 */
			'<span class="token string">action</span>': stategroup (
				'<span class="token string">set</span>' { [ <span class="token operator">set</span> ]
					'<span class="token string">argument</span>': component <a href="#grammar-rule--lambda-argument">'lambda argument'</a>
				}
				'<span class="token string">unset</span>' { [ <span class="token operator">unset</span> ] }
			)
		}
		'<span class="token string">signature</span>' { [ <span class="token operator">lambda</span> <span class="token operator">=></span> ]
			/* Set the implementation of a lambda.
			 * The signature of the lambda is taken from the parameter.
			 */
			'<span class="token string">lambda</span>': component <a href="#grammar-rule--lambda-implementation">'lambda implementation'</a>
		}
		'<span class="token string">choice</span>' {
			/* Set a choice.
			 * The available values of the choice are taken from the parameter.
			 */
			'<span class="token string">option</span>': [ <span class="token operator">option</span> ] reference
		}
		'<span class="token string">node</span>' {
			/* Set a node.
			 * This allows the creation of new data inline instead of retrieving stored data.
			 */
			'<span class="token string">statement</span>': [ <span class="token operator">new</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">value</span>' {
			/* Set the value.
			 */
			'<span class="token string">value</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-arguments }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda arguments</span>' {
	/* The arguments for a callable object.
	 * This creates a new scoped bound to the signature parameters.
	 * The created scope will be the initial scope of the callable object when called.
	 */
	'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">argument</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--lambda-argument">'lambda argument'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--lambda-definition }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">lambda definition</span>' {
	/* Defines a new lambda.
	 */
	'<span class="token string">signature</span>': [ <span class="token operator">lambda</span> ] component <a href="#grammar-rule--signature">'signature'</a>
	'<span class="token string">instance</span>': component <a href="#grammar-rule--callable-instance">'callable instance'</a>
	'<span class="token string">lambda</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--lambda-implementation">'lambda implementation'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--callable-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">callable selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">function</span>' {
			/* Select a function from the standard library.
			 */
			'<span class="token string">library</span>': reference
			'<span class="token string">function</span>': [ <span class="token operator">::</span> ] reference
			'<span class="token string">instance</span>': component <a href="#grammar-rule--callable-instance">'callable instance'</a>
		}
		'<span class="token string">recurs</span>' { [ <span class="token operator">self</span> ]
			/* Select self.
			 * This represents the currently executing lambda.
			 * Only available in a lambda implementation.
			 */
		}
		'<span class="token string">new</span>' {
			/* Create and select a new lambda.
			 * This lambda is anonymous.
			 */
			'<span class="token string">lambda</span>': component <a href="#grammar-rule--lambda-definition">'lambda definition'</a>
		}
		'<span class="token string">stored</span>' {
			/* Retrieve a stored lambda.
			 */
			'<span class="token string">value</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--decimal-import-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">decimal import rule</span>' {
	/* Enable/Disable decimal point translation.
	 * Decimal point translation is only every applied during parsing and serialization.
	 * The translation is provided from the parsing point of view, during serialization the inverse is applied.
	 */
	'<span class="token string">decimal point translation</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">places</span>': [ <span class="token operator"><<</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--date-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">date expression</span>' {
	'<span class="token string">year</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">calendar</span>' {
			'<span class="token string">month</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
			'<span class="token string">day</span>': [ <span class="token operator">-</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
		}
		'<span class="token string">week</span>' { [ <span class="token operator">W</span> ]
			'<span class="token string">week</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
			'<span class="token string">day of week</span>': stategroup (
				'<span class="token string">monday</span>' { [ <span class="token operator">Monday</span> ] }
				'<span class="token string">tuesday</span>' { [ <span class="token operator">Tuesday</span> ] }
				'<span class="token string">wednesday</span>' { [ <span class="token operator">Wednesday</span> ] }
				'<span class="token string">thursday</span>' { [ <span class="token operator">Thursday</span> ] }
				'<span class="token string">friday</span>' { [ <span class="token operator">Friday</span> ] }
				'<span class="token string">saturday</span>' { [ <span class="token operator">Saturday</span> ] }
				'<span class="token string">sunday</span>' { [ <span class="token operator">Sunday</span> ] }
			)
		}
		'<span class="token string">ordinal</span>' {
			'<span class="token string">day</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--time-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">time expression</span>' {
	'<span class="token string">hour</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">minute</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">second</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--pattern-rule-piece }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">pattern rule piece</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">pattern</span>' {
			'<span class="token string">capture</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">$</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
		}
		'<span class="token string">static</span>' {
			'<span class="token string">text</span>': text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--pattern-rule-piece">'pattern rule piece'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--pattern-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">pattern rule</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	/* Describes a custom pattern.
	 * A pattern is an ordered set of named parts, with each part an ordered set of pieces.
	 * Each part must capture a single piece. Only dynamic patterns can be captured.
	 * A pattern must contains at least a single part.
	 */
	'<span class="token string">parts</span>': dictionary {
		'<span class="token string">has next</span>': [ <span class="token operator">:</span> ] stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
			| none = '<span class="token string">no</span>'
		)
		'<span class="token string">pieces</span>': component <a href="#grammar-rule--pattern-rule-piece">'pattern rule piece'</a>
	}
	'<span class="token string">head</span>': reference = first
}
</pre>
</div>
</div>

{: #grammar-rule--format-rule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">format rule</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">dynamic</span>' {
			'<span class="token string">padding</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Select the justification and padding character.
					 * Zero padding can only be applied to decimals.
					 * NOTE: This selects the justification/alignment of the text value, justify right causes padding to be added to the LEFT!
					 */
					'<span class="token string">justify</span>': stategroup (
						'<span class="token string">right zero</span>' { [ <span class="token operator">@zero</span> ] }
						'<span class="token string">right space</span>' { }
						'<span class="token string">left space</span>' { [ <span class="token operator">@left</span> ] }
					)
					/* Select the minimum amount of characters written.
					 * Longer values are not truncated.
					 */
					'<span class="token string">places</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
		}
		'<span class="token string">static</span>' {
			'<span class="token string">text</span>': text
		}
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">,</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--format-rule">'format rule'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promise-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise path</span>' {
	'<span class="token string">step</span>': stategroup (
		'<span class="token string">optional value</span>' { [ <span class="token operator">get</span> ]
			/* Retrieve the value of an optional value.
			 * This fails when the optional value is not set.
			 */
		}
		'<span class="token string">entity lookup</span>' {
			/* Retrieve the value of an entry in an indexed set.
			 * A set is considered indexed when the entry type is `entity`.
			 * This fails when the provided key does not exist in the set.
			 * On success it results in the entity value, not the entity itself.
			 */
			'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--promise">'promise'</a>
		}
		'<span class="token string">file fetch</span>' {
			/* Retrieve a property from a file.
			 */
			'<span class="token string">field</span>': stategroup (
				'<span class="token string">token</span>' { [ <span class="token operator">.token</span> ] }
				'<span class="token string">extension</span>' { [ <span class="token operator">.extension</span> ] }
			)
		}
		'<span class="token string">entity fetch</span>' {
			/* Retrieve a property from an entity.
			 */
			'<span class="token string">field</span>': stategroup (
				'<span class="token string">key</span>' { [ <span class="token operator">.key</span> ] }
				'<span class="token string">value</span>' { [ <span class="token operator">.value</span> ] }
			)
		}
		'<span class="token string">node fetch</span>' {
			/* Retrieve a property of a node.
			 * Optionally an attribute from the property can be retrieved.
			 */
			'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">sub property</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] reference
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">interface choice</span>' {
			/* Retrieve the value of a specific state.
			 * This fails when the choice is set to another state.
			 */
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
		}
		'<span class="token string">plural size</span>' { [ <span class="token operator">.size</span> ]
			/* Retrieve the size of a set.
			 */
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promise-chain }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise chain</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': stategroup (
				'<span class="token string">path</span>' {
					'<span class="token string">step</span>': component <a href="#grammar-rule--promise-path">'promise path'</a>
				}
				'<span class="token string">complex</span>' { [ <span class="token operator">=></span> ]
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">parse</span>' {
							'<span class="token string">as</span>': [ <span class="token operator">parse</span> <span class="token operator">as</span> ] stategroup (
								'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ]
									/* Parses a JSON object.
									 * On success it results in a document and must first be passed to a decorator before it is usable.
									 */
								}
								'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ]
									/* Parses a XML document.
									 * On success it results in a document and must first be passed to a decorator before it is usable.
									 */
								}
								'<span class="token string">ISO Date Time</span>' { [ <span class="token operator">ISODateTime</span> ]
									/* Parses an ISO-8601 date and time, however it must have at least Seconds accuracy. (source: https://en.wikipedia.org/wiki/ISO_8601)
									 * Combines an ISODate and ISOTime separated with T, but the Date and Time components must both be in the same format.
									 *  Calendar dates + Time: YYYYMMDDThhmmss[.sss] or YYYY-MM-DDThh:mm:ss[.sss]
									 *  Week dates + Time: YYYYWwwDThhmmss[.sss] or YYYY-Www-DThh:mm:ss[.sss]
									 *  Ordinal dates + Time: YYYYDDDThhmmss[.sss] or YYYY-DDDThh:mm:ss[.sss]
									 * In all cases the Time component may contain a Time Zone, when omitted local time is assumed.
									 * On success it results in an Alan DateTime.
									 */
								}
								'<span class="token string">ISO Date</span>' { [ <span class="token operator">ISODate</span> ]
									/* Parses an ISO-8601 date, however it must have Day accuracy. (source: https://en.wikipedia.org/wiki/ISO_8601)
									 *  Calendar dates: YYYYMMDD or YYYY-MM-DD
									 *  Week dates: YYYYWwwD or YYYY-Www-D
									 *  Ordinal dates: YYYYDDD or YYYY-DDD
									 * On success it results in an Alan Date.
									 */
								}
								'<span class="token string">ISO Time</span>' { [ <span class="token operator">ISOTime</span> ]
									/* Parses an ISO-8601 time, however it must have at least Seconds accuracy. (source: https://en.wikipedia.org/wiki/ISO_8601)
									 *  Time: hhmmss[.sss] or hh:mm:ss[.sss]
									 *   The fraction separated by a decimal point is allowed but discarded.
									 *  Time Zone: Z or ±hh or ±hhmm or ±hh:mm
									 *   The timezone is allowed but discarded.
									 * On success it results in the amount of seconds since midnight.
									 */
								}
								'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
									/* Parses a decimal value.
									 *  Decimal: [+-]d[.f]
									 *   Any number of digits can be provided, but the supported range is limited by the implementation.
									 *   An optional minus or plus sign is allowed before the first digit to set the sign.
									 *   Optionally no digits can be provided before the decimal point, which implies the value of 0.
									 *   The fraction separated by a decimal point is allowed and the amount of digits may differ from the `rule`,
									 *   but only the digits specified by `rule` are kept with possibly additional 0 digits introduced when insufficient precision was provided.
									 */
									'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
									'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
								}
								'<span class="token string">lines</span>' { [ <span class="token operator">lines</span> ]
									/* Split all lines of a text value.
									 * Optionally leading and/or trailing spaces can be removed from each line.
									 * Empty lines, after trimming, are removed.
									 * It always results in a list of texts, with each entry a single line.
									 */
									'<span class="token string">trim spaces</span>': stategroup (
										'<span class="token string">yes</span>' { [ <span class="token operator">trim</span>, <span class="token operator">spaces</span> ]
											'<span class="token string">locations</span>': stategroup (
												'<span class="token string">leading</span>' { [ <span class="token operator">leading</span> ] }
												'<span class="token string">trailing</span>' { [ <span class="token operator">trailing</span> ] }
												'<span class="token string">both</span>' { }
											)
										}
										'<span class="token string">no</span>' { }
									)
								}
								'<span class="token string">pattern</span>' { [ <span class="token operator">pattern</span> ]
									/* Parses a custom pattern.
									 * On success it results in a node with all properties set to their respective captured value.
									 */
									'<span class="token string">pattern</span>': stategroup (
										'<span class="token string">library</span>' {
											'<span class="token string">selector</span>': component <a href="#grammar-rule--library-selector">'library selector'</a>
										}
										'<span class="token string">inline</span>' {
											'<span class="token string">rule</span>': component <a href="#grammar-rule--pattern-rule">'pattern rule'</a>
										}
									)
								}
							)
						}
						'<span class="token string">serialize</span>' {
							'<span class="token string">as</span>': [ <span class="token operator">serialize</span> <span class="token operator">as</span> ] stategroup (
								'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ] }
								'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ] }
								'<span class="token string">ISO Date Time</span>' { [ <span class="token operator">ISODateTime</span> ] }
								'<span class="token string">ISO Date</span>' { [ <span class="token operator">ISODate</span> ] }
								'<span class="token string">ISO Time</span>' { [ <span class="token operator">ISOTime</span> ] }
								'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
									'<span class="token string">locale</span>': component <a href="#grammar-rule--locale-selector">'locale selector'</a>
									'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
								}
							)
						}
						'<span class="token string">decorate</span>' {
							'<span class="token string">type</span>': [ <span class="token operator">decorate</span> <span class="token operator">as</span> ] stategroup (
								'<span class="token string">source</span>' {
									/* Decorate parsed data according to a schema.
									 */
									'<span class="token string">schema</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
								}
								'<span class="token string">union</span>' {
									/* Decorate a union type.
									 * When the type is already know, this works as a type cast.
									 */
									'<span class="token string">type</span>': [ <span class="token operator">union</span> ] reference
								}
							)
						}
						'<span class="token string">make</span>' { [ <span class="token operator">make</span> ]
							'<span class="token string">type</span>': stategroup (
								'<span class="token string">date</span>' { [ <span class="token operator">date</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
									/* Creates an Alan Date for individual components. */
									'<span class="token string">date</span>': component <a href="#grammar-rule--date-expression">'date expression'</a>
								}
								'<span class="token string">date time</span>' { [ <span class="token operator">date-time</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
									/* Creates an Alan DateTime for individual components. */
									'<span class="token string">date</span>': component <a href="#grammar-rule--date-expression">'date expression'</a>
									'<span class="token string">time</span>': [ <span class="token operator">T</span> ] component <a href="#grammar-rule--time-expression">'time expression'</a>
								}
								'<span class="token string">time</span>' { [ <span class="token operator">time</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
									/* Creates a time in seconds for individual components. */
									'<span class="token string">time</span>': component <a href="#grammar-rule--time-expression">'time expression'</a>
								}
							)
						}
						'<span class="token string">compare</span>' {
							/* Compares the current value with another value.
							 * Both values must be of the same type and support the comparison.
							 */
							'<span class="token string">type</span>': stategroup (
								'<span class="token string">equality</span>' { [ <span class="token operator">is</span> ] }
								'<span class="token string">relational</span>' {
									'<span class="token string">operator</span>': stategroup (
										'<span class="token string">smaller</span>' { [ <span class="token operator">less-than</span> ] }
										'<span class="token string">smaller equal</span>' { [ <span class="token operator">less-than</span> <span class="token operator">or</span> <span class="token operator">is</span> ] }
										'<span class="token string">greater</span>' { [ <span class="token operator">greater-than</span> ] }
										'<span class="token string">greater equal</span>' { [ <span class="token operator">greater-than</span> <span class="token operator">or</span> <span class="token operator">is</span> ] }
									)
								}
							)
							'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
							'<span class="token string">other</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
						}
						'<span class="token string">reduce</span>' {
							'<span class="token string">merge</span>': stategroup (
								'<span class="token string">value</span>' {
									/* Merge a set of values.
									 * The `for each` sub-chain is run for each value in the input set, the result must match the type required by the operator.
									 */
									'<span class="token string">merge type</span>': stategroup (
										'<span class="token string">shared</span>' { [ <span class="token operator">shared</span> ]
											/* Reduces a set of values to a single shared value.
											 * Shared values are detected with an equality check.
											 * It succeeds only when all values pass an equality check and the set contains at least one value.
											 */
											'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
										}
										'<span class="token string">unique</span>' { [ <span class="token operator">unique</span> ]
											/* Removes all duplicate values from a set of values.
											 * Duplicates are detected with an equality check.
											 * The order of the set is maintained, duplicates are placed at the first occurrence.
											 */
											'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
										}
										'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ]
											/* Calculates the sum of a set of integers.
											 * It results in the sum of all values, or the additive identity when the set is empty.
											 */
										}
										'<span class="token string">product</span>' { [ <span class="token operator">product</span> ]
											/* Calculates the product of a set of integers.
											 * It results in the produce of all values, or the multiplicative identity when the set is empty.
											 */
										}
										'<span class="token string">join</span>' { [ <span class="token operator">join</span> ]
											/* Concatenates a set of texts.
											 * Optionally a separator can be added between each element.
											 * The entries are joined in the order of the set.
											 */
											'<span class="token string">separator</span>': stategroup (
												'<span class="token string">yes</span>' {
													'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
												}
												'<span class="token string">no</span>' { }
											)
										}
										'<span class="token string">logical and</span>' { [ <span class="token operator">and</span> ]
											/* Calculates the logical and of a set of booleans.
											 * It fails when the set is empty.
											 */
										}
										'<span class="token string">logical or</span>' { [ <span class="token operator">or</span> ]
											/* Calculates the logical or of a set of booleans.
											 * It fails when the set is empty.
											 */
										}
									)
									'<span class="token string">for each</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
								}
								'<span class="token string">select</span>' { [ <span class="token operator">select</span> ]
									/* Select a single value in a set.
									 * The selected entry must match `true` when compared with all other entries.
									 * The set must contain at least one entry.
									 */
									'<span class="token string">compare</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
								}
								'<span class="token string">filter</span>' { [ <span class="token operator">filter</span> ]
									/* Filter a set of values.
									 * It results in a set only containing the entries which passed the sub-promise with `true`.
									 * The order of the set is maintained.
									 */
									'<span class="token string">filter</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
								}
							)
						}
						'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
							/* Partition a set.
							 * It groups all entries with the `key` together in a bucket.
							 * The result is a set of key-value pairs, where the key is the shared `key` and the value is a set of the entries with that `key`.
							 * The order of buckets is undefined.
							 * The order of entries within a bucket is maintained.
							 */
							'<span class="token string">comparator</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--comparator">'comparator'</a>
							'<span class="token string">key</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
						}
					)
				}
				'<span class="token string">call</span>' { [ <span class="token operator">=></span> ]
					/* Call a standard library function or lambda. */
					'<span class="token string">selection</span>': [ <span class="token operator">call</span> ] component <a href="#grammar-rule--callable-selector">'callable selector'</a>
					'<span class="token string">arguments</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--lambda-arguments">'lambda arguments'</a>
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
#### Promise
A promise consists of a `head`, an instruction producing a value without any input, and a `chain`.
The chain of a promise is a set of ordered instructions which each take the output of the previous instruction as their input.
Each instruction in the chain, as well as the head, has a `promise guarantee`. When this guarantee is `yes`, the instruction will always succeed regardless of the input.
Likewise, when this guarantee is `no`, the instruction may fail at runtime when the input does not meet the instruction's requirements.
The individual instructions are separated with `=>`. Instructions with sub-promises, wrap the sub-promise in parenthesis `( ... )`.
These sub-promises propagate their guarantee to the parent promise, allow the handling of possible runtime failures at the top-level promise. Although they can handle the failures on their own.
Just like sub-promises, instructions in a chain pass their guarantee to the next instruction.
At the end of a chain, when the guarantee is `no`, an alternative must be provided.
An alternative is indicated with `||`. It provides an alternative promise to obtain a value when the previous promise fails at runtime.
When the end of the alternative promise chain the guarantee is again `no`, an other alternative must be provided.
This pattern repeats itself until a promise is provided with a guarantee of `yes` or the guarantee can be propagated to the parent.
Alternatively, when no such promise can be provided, the promise can be terminated with a `throw`.
Throwing causes execution of the statements to be aborted until a `try` statement is found.
All changes, if any, to the target since this try are undone an execution resumes at the corresponding `catch` statement.

The promise guarantees safe execution. When an instruction fails at runtime, the remainder of the chain is aborted and the alternative is evaluated.
As a result it is always safe the chain multiple instructions with a guarantee of no.

{: #grammar-rule--promise }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise</span>' {
	'<span class="token string">head</span>': stategroup (
		/* fetch from key-value pair system */
		'<span class="token string">variable</span>' {
			/* Retrieves a variable from the instance-data.
			 */
			'<span class="token string">variable</span>': [ <span class="token operator">var</span> ] reference
		}
		/* static/hardcoded values */
		'<span class="token string">static boolean</span>' {
			/* Create a static boolean value.
			 */
			'<span class="token string">value</span>': stategroup (
				'<span class="token string">true</span>' { [ <span class="token operator">true</span> ] }
				'<span class="token string">false</span>' { [ <span class="token operator">false</span> ] }
			)
		}
		'<span class="token string">static integer</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">integer</span>' {
					/* Create a static integer value.
					 */
					'<span class="token string">value</span>': integer
				}
				'<span class="token string">current time</span>' { [ <span class="token operator">now</span> ]
					/* Retrieves the current time.
					 * The time indicates when the current routine was started and does not change during the execution of the routine.
					 * This is the time as known by the hosting server.
					 */
				}
			)
		}
		'<span class="token string">static text</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">text</span>' {
					/* Create a static text value.
					 */
					'<span class="token string">value</span>': text
				}
				'<span class="token string">line break</span>' { [ <span class="token operator">line-break</span> ]
					/* Create a static text value containing the line break value.
					 */
				}
				'<span class="token string">guid</span>' { [ <span class="token operator">guid</span> ]
					/* Generate a new GUID.
					 * This GUID is a Version 4 UUID.
					 * The random data is obtained from a CSPRNG.
					 */
				}
			)
		}
		/* fetch from execution state */
		'<span class="token string">stored</span>' {
			/* Retrieve the value of a `let` expression.
			 */
			'<span class="token string">selection</span>': component <a href="#grammar-rule--stack-selector">'stack selector'</a>
		}
		'<span class="token string">context</span>' { [ <span class="token operator">$</span> ]
			/* Retrieve the current context (`$`).
			 */
		}
		'<span class="token string">captured error</span>' { [ <span class="token operator">error</span> ]
			/* Retrieve the captured error.
			 * This is only valid inside a `catch` statement.
			 */
		}
		/* compute new values */
		'<span class="token string">list constructor</span>' { [ <span class="token operator">list</span> ]
			/* Construct a list object.
			 * This allows for the conversion of a static list to a dynamic list.
			 * The order of entries is identical to the promise order.
			 */
			'<span class="token string">promises</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promises">'promises'</a>
		}
		'<span class="token string">list merge</span>' {
			/* This operations are identical to the equivalently named operations in promise-chains `reduce` instruction.
			 * Unlike the reduce operations, these operate on static set of values instead of a dynamic set.
			 */
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ] }
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ] }
				'<span class="token string">concatenate</span>' { [ <span class="token operator">concatenate</span> ]
					'<span class="token string">separator</span>': stategroup (
						'<span class="token string">yes</span>' {
							'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
						}
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">logical and</span>' { [ <span class="token operator">and</span> ] }
				'<span class="token string">logical or</span>' { [ <span class="token operator">or</span> ] }
			)
			'<span class="token string">promises</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promises">'promises'</a>
		}
		'<span class="token string">arithmetic</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">inversion</span>' { [ <span class="token operator">-</span> ]
					/* Invert the sign of an integer.
					 */
					'<span class="token string">operand</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
				}
				'<span class="token string">division</span>' { [ <span class="token operator">division</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Divide one integer by another integer.
					 * When the resulting fraction, if any, is truncated.
					 * This fails when `denominator` is zero.
					 */
					'<span class="token string">numerator</span>': component <a href="#grammar-rule--promise">'promise'</a>
					'<span class="token string">denominator</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--promise">'promise'</a>
				}
			)
		}
		'<span class="token string">logic</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">negation</span>' { [ <span class="token operator">not</span> ]
					/* Toggle the value of a boolean.
					 */
					'<span class="token string">operand</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
				}
			)
		}
		'<span class="token string">file constructor</span>' { [ <span class="token operator">file</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			/* Construct a file object.
			 */
			'<span class="token string">token</span>': [ <span class="token operator">token</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--promise">'promise'</a>
			'<span class="token string">extension</span>': [ <span class="token operator">extension</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--promise">'promise'</a>
		}
		'<span class="token string">format</span>' { [ <span class="token operator">format</span> ]
			/* Generate a new text value from a format rule.
			 */
			'<span class="token string">format</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--format-rule">'format rule'</a>
		}
	)
	'<span class="token string">chain</span>': component <a href="#grammar-rule--promise-chain">'promise chain'</a>
	'<span class="token string">alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">||</span> ] stategroup (
				'<span class="token string">value</span>' {
					/* Provide an alternative promise. */
					'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
				}
				'<span class="token string">throw</span>' {
					/* Throw a new error. */
					'<span class="token string">message</span>': [ <span class="token operator">throw</span> ] text
				}
			)
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--promises }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promises</span>' {
	'<span class="token string">value</span>': component <a href="#grammar-rule--promise">'promise'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--promises">'promises'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
#### Value Promise
This represents a top-level promise.
A value promise indicates that a promise guarantee of no cannot be propagated from the wrapped promise.
The wrapped promise must always have an alternative with a guarantee of yes, or throw.

{: #grammar-rule--value-promise }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value promise</span>' {
	'<span class="token string">promise</span>': component <a href="#grammar-rule--promise">'promise'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--target-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">target expression</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">unset</span>' { [ <span class="token operator">unset</span> ]
			/* Explicitly set an optional value to unset.
			 * This allows the setting of an optional value to be dependent on some condition.
			 */
		}
		'<span class="token string">set</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">node</span>' {
					/* Target a node.
					 * All mandatory properties must be specified.
					 * Optional properties may be omitted, which is identical to setting them to `unset`.
					 * When a property has attributes, all attributes must also be specified.
					 */
					'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
						'<span class="token string">attributes</span>': stategroup (
							'<span class="token string">yes</span>' {
								'<span class="token string">attributes</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] dictionary {
									'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
								}
							}
							'<span class="token string">no</span>' { }
						)
						'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
				}
				'<span class="token string">entry</span>' { [ <span class="token operator">create</span> ]
					/* Create a new entry in a set.
					 * When the set has implicit keys, a key must be provided.
					 */
					'<span class="token string">implicit key</span>': stategroup (
						'<span class="token string">yes</span>' {
							'<span class="token string">value</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">branch</span>' { [ <span class="token operator">create</span> ]
							/* Set an Alan Interface `stategroup` or `union` to the specified state/type.
							 */
							'<span class="token string">state</span>': reference
							'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
						}
						'<span class="token string">leaf</span>' {
							/* Set a `schema scalar type` choice to the specified value.
							 */
							'<span class="token string">option</span>': [ <span class="token operator">option</span> ] reference
						}
					)
				}
				'<span class="token string">scalar</span>' {
					/* Assign a scalar the produced value.
					 */
					'<span class="token string">value</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">statement</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">block</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
			/* Start a new block.
			 * Optionally a block can introduce a new scope.
			 * A block allows multiple independent statements to be written in the same context.
			 * Multiple statements are only allowed when the current target supports multiple values.
			 */
			'<span class="token string">scope</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">stack block</span>': component <a href="#grammar-rule--stack-block">'stack block'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">statement</span>': component <a href="#grammar-rule--statements">'statements'</a>
		}
		'<span class="token string">guard</span>' {
			/* Guard a statement and provide an alternative path.
			 * This catches all throws found in the guarded statement.
			 * When a throw is caught, the changes to the target are reverted and the fallback statement is executed.
			 * When the guarded statement is successfully executed, the fallback statement is skipped.
			 */
			'<span class="token string">guarded statement</span>': [ <span class="token operator">try</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			'<span class="token string">optional assignment</span>': [ <span class="token operator">catch</span> ] stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">fallback statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">condition</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">boolean</span>' {
					/* Execute a conditional branch.
					 * The condition is evaluated and based on the result, either the `true` or `false` case is executed.
					 */
					'<span class="token string">condition</span>': [ <span class="token operator">match</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">on true</span>': [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
						'<span class="token string">on false</span>': [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
				}
				'<span class="token string">existence</span>' {
					/* Execute a conditional branch.
					 * The promise without a guarantee of yes is evaluated.
					 * Based on whether or not the promise succeeded or failed, the corresponding case is executed.
					 * When the promise succeeds, the result is available in `$`.
					 */
					'<span class="token string">value</span>': [ <span class="token operator">any</span> ] component <a href="#grammar-rule--promise">'promise'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
						'<span class="token string">on value</span>': [ <span class="token operator">|</span> <span class="token operator">value</span> <span class="token operator">as</span> <span class="token operator">$</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
						'<span class="token string">on error</span>': [ <span class="token operator">|</span> <span class="token operator">error</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
				}
				'<span class="token string">switch</span>' {
					/* Execute a conditional branch.
					 * The branch is determined based on a user defined choice.
					 * When the choice is an Alan Interface `stategroup`, the state node is optionally available in `$`.
					 */
					'<span class="token string">value</span>': [ <span class="token operator">switch</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
					'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
						'<span class="token string">has next</span>': stategroup = node-switch successor (
							| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
							| none = '<span class="token string">no</span>'
						)
						'<span class="token string">optional assignment</span>': stategroup (
							'<span class="token string">yes</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ] }
							'<span class="token string">no</span>' { }
						)
						'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
				}
			)
		}
		'<span class="token string">walk</span>' {
			/* Execute a statement once for each entry in a set.
			 * The entry for which the statement is executed, is available in `$`.
			 */
			'<span class="token string">value</span>': [ <span class="token operator">walk</span>, <span class="token operator">as</span> <span class="token operator">$</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
			'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">call</span>' {
			/* Call a standard library function or lambda. */
			'<span class="token string">selection</span>': [ <span class="token operator">call</span> ] component <a href="#grammar-rule--callable-selector">'callable selector'</a>
			'<span class="token string">arguments</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--lambda-arguments">'lambda arguments'</a>
		}
		'<span class="token string">log operation</span>' { [ <span class="token operator">@log:</span> ]
			/* Write a message to the debug channel.
			 */
			'<span class="token string">message</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
		}
		'<span class="token string">no operation</span>' { [ <span class="token operator">no-op</span> ]
			/* No action.
			 * This is to terminate an execution path without doing anything.
			 * It is only allowed when the target allows no value.
			 *
			 * This statement allows for the creation of empty sets.
			 * Unlike all other targets, which define no default/initial value, sets are default empty.
			 */
		}
		'<span class="token string">throw</span>' {
			/* Throw a error.
			 * This can either be a new error, or when inside a `catch` statement it can rethrow the caught error.
			 */
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">captured error</span>' { [ <span class="token operator">rethrow</span> ] }
				'<span class="token string">new error</span>' { [ <span class="token operator">throw</span> ]
					'<span class="token string">message</span>': text
				}
			)
		}
		'<span class="token string">target</span>' {
			'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
		}
		'<span class="token string">execute</span>' {
			/* Execute a Alan Interface command or event.
			 */
			'<span class="token string">context</span>': [ <span class="token operator">execute</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">command</span>' {
					'<span class="token string">command</span>': [ <span class="token operator">command</span> ] reference
				}
				'<span class="token string">event</span>' {
					'<span class="token string">event</span>': [ <span class="token operator">event</span> ] reference
				}
			)
			'<span class="token string">statement</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--statements }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">statements</span>' {
	'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
	'<span class="token string">has more statements</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">statement</span>': component <a href="#grammar-rule--statements">'statements'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
