---
layout: "doc"
origin: "connector"
language: "processor"
version: "38-dev"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">none</span>': component <a href="#grammar-rule--hook">'hook'</a>
</pre>
</div>
</div>
# Release Notes

## 38
#### Syntax Update
The syntax has been changed to better align with other alan languages.
Use the upgrade script to automatically convert a processor from version 36.6.

#### Configuration and variables merged
The functionality of configuration and variables have been merged.
The strict type checking and data guarantees are used, but the data is obtained from the runtime configuration using a new platform feature.

#### Application Support
The connector now understand Application models and can be configured to migrate Application data from one model to another.

#### Data limits in schema
In addition to number range and text length limits, boolean can be constraint to a specific value and binary length can be limited.

#### Auto union decoration
When parsing, unions are automatically resolved to the first type that matches.
This uses the syntactic order of the union's types.

#### Attribute filters removed
Attribute filters on properties of schema nodes are removed.
These can be set through data limits on the actual attributes.

#### Error logging
Logging to the functional error channel with `@error:` is now supported.

#### Template engine improvements
The template engine can infer the amount of decimal places from the input type and reports this information in it's schema output.
This is used to set the default style properties when the number is formatted.
Templates now support escaping for text properties, either with a template wide dictionary or with an instruction specific dictionary.
Escaping can also be disable per instruction.

#### Type system improved
The connector now uses a single type system internally, fixing many type related quirks.
This also merges the different calling conventions used between statement and expressions.
Type checking for XML and CSV has been improved to give proper design time feedback about supported layouts.
Arbitrary types can now be instantiated out of their tree.
Removed cardinality context, results are now either automatically merged (for plural values) or need to be resolved manually (with `discard`).

#### Automatic version migrations
The runtime automatically resolves differences between minor versions, allowing the runtime to execute packages for older versions within the same major version.

#### Debugger improvements
The debugger's ability to step through a program is improved.
It can now step into, over and out of statements.
# The Standard Libraries
The connector provides a set of standard libraries.
These libraries provide functionality outside the language constructs of the connector.
## Calendar
The calendar library provides conversions between the connectors internal date time representation and broken down time.

```js
define 'type': choice ( 'date' 'date-time' 'time' )

define 'calendar': {
	'year': integer
	'month': integer where range ( 1 , 12 )
	'day': integer where range ( 1 , 31 )
}

define 'weekday': choice ( 'Monday': 1 'Tuesday': 2 'Wednesday': 3 'Thursday': 4 'Friday': 5 'Saturday': 6 'Sunday': 7 )

define 'week': {
	'year': integer
	'week': integer where range ( 1 , 53 )
	'day': 'weekday'
}

define 'ordinal': {
	'year': integer
	'day': integer where range ( 1 , 366 )
}

define 'time': {
	'hour': integer where range ( 0 , 23 )
	'minute': integer where range ( 0 , 59 )
	'second': integer where range ( 0 , 59 )
}

define 'date time': {
	'calendar': 'calendar'
	'week': 'week'
	'ordinal': 'ordinal'
	'time': 'time'
}

define 'constructor': {
	'date': union (
		'calendar' 'calendar'
		'week' 'week'
		'ordinal' 'ordinal'
	)
	'time': optional 'time'
}

/* Converts Alan Time to broken down time.
 * When information is not present in the source, it is set to zero.
 * When timezone is not set, it will be evaluated in Etc/UTC.
 */
define 'convert': function (
	integer
	$'source type': 'type'
	$'timezone': optional text
) : 'date time' = "ca798e96fe9b6bd53c960192c8d0cf8cd4175e7f"

/* Construct Alan Time from broken down time.
 * The result is either a date-time or a date, depending on whether or not 'time' is set.
 * When timezone is not set, it will be evaluated in Etc/UTC.
 */
define 'construct': function (
	'constructor'
	$'timezone': optional text
) : integer = "b8397afa5b82bce0c97ff08e5ef7d120a8c1ee73"

library
```
## Network
The network library provides functions to perform network request and the data structures to represent related objects.

```js
define 'method': choice ( 'get' 'head' 'post' 'put' 'delete' )

define 'security': choice ( 'strict' 'preferred' 'none' )

define 'key value list': collection case folding text

define 'request': {
	'method': 'method'
	'parameters': optional 'key value list'
	'headers': optional 'key value list'
	'content': optional binary
}

define 'response': {
	'status': integer
	'headers': 'key value list'
	'content': binary
}

define 'authentication': {
	'type': union (
		'user' {
			'username': text
			'password': @protected text
		}
		'oauth' {
			'username': text
			'token': @protected text
		}
	)
}

define 'address': {
	'name': text
	'address': text
}

define 'message part': {
	'type': text
	'content': text
}

define 'message content': {
	'id': text
	'type': text
	'subtype': text
	'content': binary
}

define 'message attachment': {
	'filename': text
	'type': text
	'subtype': text
	'content': binary
}

define 'message': {
	'from': list 'address'
	'sender': optional 'address'
	'reply to': optional list 'address'
	'to': list 'address'
	'cc': optional list 'address'
	'bcc': optional list 'address'
	'subject': optional text
	'date': optional integer
	'message-id': optional text
	'headers': optional 'key value list'
	'content': {
		'parts': list 'message part'
		'content': optional list 'message content'
		'attachments': optional list 'message attachment'
	}
}

/* Parses and decorates text as 'message'.
 */
define 'parse network message': function ( binary ) : unsafe 'message' = "cb3038cf22544368256da4f4843f7751d930873e"

/* Serializes a 'network message' to text.
 */
define 'serialize network message': function (
	'message'
	$'include bcc': boolean
) : unsafe binary = "8991b5e7ace6a89c6c095509b1c9106f19c0656b"

/* Performs an HTTP(S) request.
 * Methods are mapped directly to their HTTP equivalent.
 * When provided, 'content' is send with the request.
 */
define 'http': function (
	$'server': text
	$'path': text
	$'authentication': optional 'authentication'
	$'request': 'request'
) : unsafe 'response' = "171a2a495168c8db61a75ea879759560a5a38db5"

/* Performs an FTP(S) request.
 * Method mapping:
 *  > 'get': Retrieves the content of 'path'. For this to work on directories, 'path' must end with a slash (/).
 *  > 'head': Retrieves the directory entries at 'path' without meta data. 'path' must be a directory, but does not need to end with a slash (/).
 *  > 'post': Stores 'content' in 'path'.
 *  > 'put': Identical to 'post'.
 *  > 'delete': Attempts to remove 'path'. Unlike other methods, this transmits 'path' directly to the server for interpretation.
 * Only when storing data, should content be set.
 */
define 'ftp': function (
	$'server': text
	$'path': text
	$'method': 'method'
	$'authentication': optional 'authentication'
	$'security': 'security'
	$'content': optional binary
) : unsafe optional binary = "25bd9db5582c68caabef54601bb1cef80fc24fe6"

/* Retrieves all messages matching 'criteria' with IMAP(S).
 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
 * All messages are parsed as if passed to `function 'parse network message'`.
 */
define 'imap': function (
	$'server': text
	$'path': text
	$'criteria': text
	$'authentication': optional 'authentication'
	$'security': 'security'
) : unsafe list 'message' = "f263bada59d75b01ecf6f5d620a9d090f5f12926"

/* Retrieves all messages matching 'criteria' with IMAP(S).
 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
 */
define 'imap list': function (
	$'server': text
	$'path': text
	$'criteria': text
	$'authentication': optional 'authentication'
	$'security': 'security'
	$'callback': function ( $'blob': binary ) : boolean
) : unsafe list boolean = "5833f6978cd3090249f0beac809961d9054d5a90"

/* Retrieves all messages after 'last uid' with IMAP(S).
 * Performs an optional UIDVALIDITY check with 'uid validity' when set.
 */
define 'imap list uid': function (
	$'server': text
	$'path': text
	$'uid validity': optional integer
	$'last uid': integer
	$'authentication': optional 'authentication'
	$'security': 'security'
	$'callback': function (
		$'uid': integer
		$'blob': binary
	) : boolean
) : unsafe optional integer = "c0c069849e5ec03a546b737c782a139678c2b695"

/* Retrieves all mailboxes with IMAP(S).
 */
define 'imap listing': function (
	$'server': text
	$'path': text
	$'authentication': optional 'authentication'
	$'security': 'security'
) : unsafe list text = "94c875f1b608ec08204f53bc677d7662168c71d8"

/* Send a message with SMTP(S).
 * The message is serialized as if passed to `function 'serialize network message'`.
 * When the transfer fails, this function throws an error.
 */
define 'smtp': function (
	$'server': text
	$'authentication': optional 'authentication'
	$'security': 'security'
	$'message': 'message'
) : unsafe boolean = "8d09c84214fc074d7d9cc8123e59da15605c01b2"

library
	/* Register webserver handlers.
	 * The handler is used as the path to respond to.
	 * Each handler is triggered by external web requests for the path.
	 */
	hook 'webserver'
		< T is node > (
			T
			$'request': 'request'
		) : 'response' = "dfc3f634b2167c0d7429a10ff11a00550a142354"
```
## Plural
The plural library provides algorithms operating on sets.

```js
/* Sorts a set based on a comparison function.
 */
define 'sort': function < T is plural E > (
	T
	$'compare': function (
		$'A': E
		$'B': E
	) throws : boolean
) throws : T = "bdf496ca369a4ba51e47122cd1ec8fb8bcf37898"

/* Selects a single entry in a set based on a comparison function.
 * This returns the entry for which `compare` results in true when the entry is `A` and false when `B` compared to all other entries in the set.
 * It fails when no such entry is found.
 */
define 'select': function < T is plural E > (
	T
	$'compare': function (
		$'A': E
		$'B': E
	) throws : boolean
) throws : unsafe E = "6f40c5cf50c67547e023cf4540da3f1b0c5af505"

/* Filters a set.
 * This returns a new set containing only the entries for which `filter` results in true.
 */
define 'filter': function < T is plural E > (
	T
	$'filter': function ( $'entry': E ) throws : boolean
) throws : T = "368b73f2ca1fc93c4d4df568ea0438e4c5a8211a"

/* Divide a set in several smaller sets (buckets).
 * The order of the entries is maintained.
 */
define 'split': function < T is plural E > (
	T
	$'bucket size': integer
) : list T = "a21f3c1edb32d67395b4f9a9c2150d5011d13d0b"

library
```
## Unicode
The unicode library provides functions to manipulate text values.

```js
define 'trim style': choice ( 'leading' 'trailing' 'both' 'none' )

define 'alignment': choice ( 'left' 'right' )

define 'message data': {
	'types': collection union (
		'calendar' integer
		'number' integer
		'text' text
	)
}

/* Imports text from binary data.
 * Text is converted from the specified encoding to the internal encoding.
 * When the specified encoding is not known, or no know conversion to the internal encoding is known, the function fails.
 */
define 'import': function (
	binary
	$'encoding': text
) : unsafe text = "9e980f69ab15906c61ceeb1ac1a2125d6fc03349"

/* Exports text to binary data.
 * Text is converted to the specified encoding from the internal encoding.
 * When the specified encoding is not known, or no know conversion from the internal encoding is known, the function fails.
 */
define 'export': function (
	text
	$'encoding': text
) : unsafe binary = "6493b6da20eb5dde5bfb9581543e09b3f1b0fc44"

/* Returns a text value as binary data.
 * The data is encoded in the internal encoding.
 */
define 'as binary': function ( text ) : binary = "6649c6455c721f73c26ce7916b6b705048b79e1b"

/* Replaces all occurrences of the key of the entries in the dictionary with their value.
 */
define 'escape': function (
	text
	$'dictionary': collection text
) : text = "397e23c87d21e3651a5a0341eb06957d6c11a922"

/* Removes all whitespace from a text value.
 */
define 'strip': function ( text ) : text = "b1ad934aa23db1551ece5ecef7e08d824efa660a"

/* Removes leading and/or trailing whitespace from a text value.
 */
define 'trim': function (
	text
	$'style': 'trim style'
) : text = "5652809fd18b42a7313d5793801f4c79f887c3d4"

/* Split a text into multiple fragments.
 * Empty fragments are automatically removed.
 */
define 'split': function (
	text
	$'style': 'trim style'
) : list text = "25e981050bc615be2930712c7c250365b2570345"

/* Adds whitespace to a text value.
 */
define 'pad': function (
	text
	$'align': 'alignment'
	$'length': integer
) : text = "be6f170dc45c3b8b120c5b5954cbd875ce7a7c48"

/* Match a text with a Regular Expression.
 * The whole input must match the pattern.
 */
define 'regex': function (
	text
	$'pattern': text
) : unsafe boolean = "e24486d2b0065ac06d1497e280838b4b3bb9f039"

/* Result of the template function.
 */
define 'template result': {
	'success': boolean /* Value indicating whether the template was transformed correctly or not. */
	'result': text /* On success contains the transformed template, on failure contains the error message. */
	'schema': text /* The schema inferred from the input data. */
}

/* Format a template with dynamic data.
 */
define 'template': function < T is node > (
	T
	$'template': text
	$'dictionary': collection text
	$'locale': text
) : unsafe 'template result' = "63a8bab4a6e2efa51c4d048fdbcde794df07c62a"

library
```
## Data
The data library provides functions to manipulate binary values.

```js
define 'base64 alphabet': choice ( 'base64' 'base64url' )

/* Converts text from one encoding to another.
 * Available encodings depend on the hosting systems.
 */
define 'convert': function (
	binary
	$'from': text
	$'to': text
) : unsafe binary = "e84c70582091283e8ef035eb15edd57b5e1bfa93"

/* Convert binary data to base64 text.
 * Alphabet as defined by RFC-4648.
 */
define 'base64 encode': function (
	binary
	$'alphabet': 'base64 alphabet'
) : text = "a28d688c547335308cefd17e61fd26e0bda09610"

/* Convert base64 text to binary data.
 * Alphabet as defined by RFC-4648.
 */
define 'base64 decode': function (
	text
	$'alphabet': 'base64 alphabet'
) : unsafe binary = "4c9ab1bc2636b3711553500ec4e153e8356e4778"

/* Loads an archive from data.
 * Archive format and any compression/encoding are automatically detected.
 */
define 'load archive': function ( binary ) : unsafe collection binary = "fba823216f0f6dc6bbb644fc0c2c0b21ae69f8c1"

library
```
# Processor
## Obscure data
Obscures all textual data during assignment in a consistent way.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">obscure data</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">obscure</span> <span class="token operator">data</span> ] }
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>
## The internal library.
Allows defining reusable types.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library</span>': dictionary { [ <span class="token operator">define</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">schema</span>' {
			/* Define a schema type.
			 */
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">pattern</span>' { [ <span class="token operator">pattern</span> ]
			/* Define a pattern.
			 */
			'<span class="token string">rule</span>': component <a href="#grammar-rule--pattern-rule">'pattern rule'</a>
		}
		'<span class="token string">function</span>' { [ <span class="token operator">function</span> ]
			/* Define a function.
			 */
			'<span class="token string">signature</span>': component <a href="#grammar-rule--signature">'signature'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">implementation</span>' {
					'<span class="token string">implementation</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--function-implementation">'function implementation'</a>
				}
				'<span class="token string">binding</span>' {
					/* The function is part of a standard library.
					 * These functions are implemented by the connector runtime.
					 */
					'<span class="token string">binds</span>': [ <span class="token operator">=</span> ] text
				}
			)
		}
	)
}
</pre>
</div>
</div>
## The type of the connector.
This is chosen externally, the archetype here must follow the external choice.

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
		'<span class="token string">main routine</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
		/* Dataset initialization.
		 * Before a provider can process commands and generate events, a dataset is required.
		 * When available, the last result of the main routine is used as dataset.
		 * Otherwise the initialization is used to determine the initial dataset.
		 */
		'<span class="token string">initialization</span>': [ <span class="token operator">init</span> ] stategroup (
			'<span class="token string">custom</span>' {
				/* Use a custom routine to generate the initial dataset.
				 * This can be used to prevent additional runs of the main routine when this would exceed rate limits/query quotas.
				 */
				'<span class="token string">routine</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
			}
			'<span class="token string">main</span>' { [ <span class="token operator">main</span> ]
				/* Use the main routine to generate the initial dataset.
				 * This run of the main routine is in addition to runs caused by the external schedule.
				 */
			}
			'<span class="token string">none</span>' { [ <span class="token operator">none</span> ]
				/* Do not generate an initial dataset.
				 * Received commands are ignored until the main routine is triggered.
				 */
			}
		)
		/* Command routines.
		 * These routines are run when the corresponding command is received.
		 * Commands can have multiple handlers. When the command is received, all handlers are executed in an undefined order.
		 * Received commands for which no handlers exist, are ignored.
		 */
		'<span class="token string">routines</span>': dictionary { [ <span class="token operator">routine</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			/* The path to the command the routine is bound to.
			 * The path becomes the initial scope of the routine.
			 */
			'<span class="token string">binding</span>': [ <span class="token operator">on</span> <span class="token operator">root</span> ] component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">execute</span>' {
					/* Execute a statement.
					 * From this context Alan Interface events can be executed.
					 */
					'<span class="token string">statement</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
				}
				'<span class="token string">schedule</span>' { [ <span class="token operator">schedule</span> ]
					/* Schedule a run of the main routine immediately after the command.
					 * The main routine is run, and consumers are updated, regardless of the external schedule.
					 * This run of the main routine is in addition to runs caused by the external schedule.
					 * This fully ignores the binding path of the routine and even triggers properly when there is no dataset yet.
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
		 * The statement is restricted, see '<span class="token string">statement</span>' for details.
		 */
		'<span class="token string">context keys</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
		/* The routines.
		 * Each routine is bound to something in the interface.
		 * The routine is triggered based on the interface binding.
		 */
		'<span class="token string">routines</span>': dictionary { [ <span class="token operator">routine</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			/* The path to the interface data the routine is bound to.
			 * The path becomes the initial scope of the routine.
			 */
			'<span class="token string">binding</span>': [ <span class="token operator">on</span> <span class="token operator">root</span> ] component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
			/* From this context Alan Interface commands can be executed.
			 */
			'<span class="token string">statement</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
		}
		/* The hooks.
		 * See `Library Hooks` for more information.
		 */
		'<span class="token string">hooks</span>': set {
			'<span class="token string">hook</span>': component <a href="#grammar-rule--library-hook">'library hook'</a>
		}
	}
	'<span class="token string">migration</span>' { [ <span class="token operator">root</span> <span class="token operator">=</span> <span class="token operator">root</span> <span class="token operator">as</span> <span class="token operator">$</span> ]
		/* The connector is a migration.
		 * As a migration, the connector runs a single routine once.
		 */
		/* The routine mapping data from '<span class="token string">source</span>' to '<span class="token string">target</span>'
		 */
		'<span class="token string">statement</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
	}
	'<span class="token string">library</span>' { [ <span class="token operator">library</span> ]
		/* The connector is a library.
		 * Currently only standard libraries are supported.
		 */
		/* A library can expose hooks.
		 * Each hook is triggered by external events.
		 */
		'<span class="token string">hooks</span>': dictionary { [ <span class="token operator">hook</span> ]
			'<span class="token string">signature</span>': component <a href="#grammar-rule--signature">'signature'</a>
			'<span class="token string">binds</span>': [ <span class="token operator">=</span> ] text
		}
	}
)
</pre>
</div>
</div>
## Internal error handler.
Allows specifying an error handler routine.
Example:

```js
consumer {
	( )
}
/* error-handler example
 *  this logs the error report
 */
on error {
	@log: $
}
```


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">error handler</span>': stategroup (
	'<span class="token string">yes</span>' {
		/* The routine to execute for uncaught errors.
		 * When a notification/command/event triggers multiple routines, the error reports from these are bundled and the handler is executed only once for the bundle.
		 * The statement is restricted, see '<span class="token string">statement</span>' for details.
		 */
		'<span class="token string">statement</span>': [ <span class="token operator">on</span> <span class="token operator">error</span> ] component <a href="#grammar-rule--block-statement">'block statement'</a>
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

{: #grammar-rule--hook }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">hook</span>' { }
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
## Library Hook
The standard library defines hooks.
When or how these hooks are triggered is defined by the individual hooks.
Providers and consumers can add functions to these hooks.
These functions are executed when the hook is triggered.
Some hooks only trigger a subset of the added functions, based on the handler name.

Functions added to hooks can execute side-effects based on their context.
Providers can execute events.
Consumers can execute commands.

Example:

```js
consumer {
	( )
}

/* Standard Library `network.lib`::`webserver` example
 *  this registers a webserver hook for the `/echo` path
 *  the original request is returned as JSON
 */
add-hook 'network'::'webserver' "/echo" {
	(
		'status' = 200
		'headers' = create [ "content-type" ] "application/json"
		'content' = call 'unicode'::'as binary' ( serialize $'request' as JSON )
	)
}
```


{: #grammar-rule--library-hook }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library hook</span>' {
	/* The standard library and hook to add the function to.
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
	'<span class="token string">implementation</span>': component <a href="#grammar-rule--function-implementation">'function implementation'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--interface-binding-assignment }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface binding assignment</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	'<span class="token string">name</span>': reference = first
	'<span class="token string">named objects</span>': [ <span class="token operator">as</span> ] dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">has successor</span>': stategroup = node-switch successor (
			| node = '<span class="token string">yes</span>' { }
			| none = '<span class="token string">no</span>'
		)
	}
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
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ]
					/* Collection binding.
					 * The set of entries touched by an update (and only the touched entries) are made available.
					 * The value of each entry is an optional node.
					 * When an entry was created or updated, the node is set to the entry node.
					 * When an entry was removed, the node is unset.
					 */
				}
				'<span class="token string">stategroup</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">attribute</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--interface-type-path">'interface type path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--interface-named-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interface named path</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--interface-type-path">'interface type path'</a>
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">assignment</span>': component <a href="#grammar-rule--interface-binding-assignment">'interface binding assignment'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
		}
		'<span class="token string">no</span>' { }
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
		'<span class="token string">case folding</span>' { [ <span class="token operator">case</span> <span class="token operator">folding</span> ]
			/* The case-folding comparator operates only on texts.
			 * It supports equality and relational comparisons.
			 */
		}
		'<span class="token string">simple</span>' {
			/* The simple comparator behaves depending on the it operates on.
			 *  > boolean: supports only equality comparisons
			 *  > integer: supports equality and relational comparisons
			 *  > binary : supports only equality comparisons, 2 binaries are considered equal when they are bitwise identical
			 *  > text   : supports equality and relational comparisons, 2 texts are compared based on their code-points, the values are not normalized
			 *  > file   : supports only equality comparisons, 2 files are considered equal when both token and extension are identical
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
			'<span class="token string">limits</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">where</span> ]
					/* Limit the value.
					 */
					'<span class="token string">must be</span>': stategroup (
						'<span class="token string">true</span>' { [ <span class="token operator">true</span> ] }
						'<span class="token string">false</span>' { [ <span class="token operator">false</span> ] }
					)
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">number</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
					/* An integer can hold numbers.
					 * Integers can not have a fraction.
					 * Parsing and serializing always uses base 10.
					 */
				}
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
				}
			)
			'<span class="token string">limits</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">where</span> <span class="token operator">range</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Limit the value range.
					 * All limits are inclusive.
					 */
					'<span class="token string">lower</span>': stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the minimum value.
							 * The value is evaluated after the decimal import rule.
							 */
							'<span class="token string">value</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">upper</span>': [ <span class="token operator">,</span> ] stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the maximum value.
							 * The value is evaluated after the decimal import rule.
							 */
							'<span class="token string">value</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">binary</span>' { [ <span class="token operator">binary</span> ]
			/* A data can hold any type of binary data.
			 */
			'<span class="token string">limits</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">where</span> <span class="token operator">length</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Limit the binary length in bytes.
					 * All limits are inclusive.
					 */
					'<span class="token string">lower</span>': stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the minimum length of the value.
							 * The length is measured in code-points.
							 */
							'<span class="token string">length</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">upper</span>': [ <span class="token operator">,</span> ] stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the maximum length of the value.
							 * The length is measured in code-points.
							 */
							'<span class="token string">length</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
			/* A text can hold Unicode data.
			 */
			'<span class="token string">limits</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">where</span> <span class="token operator">length</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Limit the text length in code-points.
					 * All limits are inclusive.
					 */
					'<span class="token string">lower</span>': stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the minimum length of the value.
							 * The length is measured in code-points.
							 */
							'<span class="token string">length</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">upper</span>': [ <span class="token operator">,</span> ] stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the maximum length of the value.
							 * The length is measured in code-points.
							 */
							'<span class="token string">length</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">no</span>' { }
			)
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
			 * Parsing tries each sub-type in order, the first sub-type that successfully parses becomes the selected sub-type.
			 */
			'<span class="token string">types</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">has next</span>': stategroup = node-switch successor (
					| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
					| none = '<span class="token string">no</span>'
				)
				'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
			}
			'<span class="token string">first</span>': reference = first
		}
		'<span class="token string">optional</span>' { [ <span class="token operator">optional</span> ]
			/* Optional type.
			 * Wraps another type and allows it to have an explicit unset state.
			 * Parsing and serialization either expects the data to be completely omitted or have a special none value construct.
			 */
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">node</span>' {
			/* Node type.
			 */
			'<span class="token string">form</span>': stategroup (
				'<span class="token string">ordinary</span>' {
					/* Parsing and serialization expects the type information (property names) to be present in the data.
					 */
				}
				'<span class="token string">headless</span>' { [ <span class="token operator">headless</span> ]
					/* Parsing and serialization expects the data to be ordered by the property order.
					 */
				}
			)
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">collection</span>' { [ <span class="token operator">collection</span> ]
			/* Set type.
			 * This holds a dynamic amount of data, or no data at all (empty set).
			 * Every entry has an implicit key that must be unique within the set.
			 * A comparator is used for matching the implicit keys.
			 */
			'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">list</span>' { [ <span class="token operator">list</span> ]
			/* Set type.
			 * This holds a dynamic amount of data, or no data at all (empty set).
			 * Every entry automatically get a numeric key assigned that is unique within the set, the key holds no semantic meaning.
			 */
			'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
		}
		'<span class="token string">table</span>' { [ <span class="token operator">table</span> ]
			/* Special set type.
			 * A table behaves as if it was a list of headless nodes, except for a special parsing/serialization specialization.
			 * The table expects the very first row in serialized from to be the header.
			 * This header must match all properties in the node, but can do so in any order.
			 * Unlike the headless node, where the property order is defined by the schema, the parsing/serialization order of all properties is defined by this header row.
			 * Every entry automatically get a numeric key assigned that is unique within the set, the key holds no semantic meaning.
			 */
			'<span class="token string">node</span>': component <a href="#grammar-rule--schema-node-type">'schema node type'</a>
		}
		'<span class="token string">template</span>' {
			'<span class="token string">argument</span>': stategroup (
				'<span class="token string">T</span>' { [ <span class="token operator">T</span> ] }
				'<span class="token string">E</span>' { [ <span class="token operator">E</span> ] }
			)
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
	 * Each property itself can have a set of attributes, which must be text types, choices with text base types are also allowed.
	 * A property can be marked as optional, an optional property may be omitted or have a special none value construct in serialized form.
	 *
	 * A property can be marked as protected, protected property data is always excluded from data dumps.
	 * This is to prevent the connector leaking sensitive data.
	 * NOTE: Using @protected is no guarantee the relevant data is never included.
	 *       When the sensitive data is also present in unprotected data, it will still be readable in that data.
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
				'<span class="token string">first</span>': reference = first
			}
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">protect</span>': [ <span class="token operator">:</span> ] stategroup (
			'<span class="token string">yes</span>' { [ <span class="token operator">@protected</span> ] }
			'<span class="token string">no</span>' { }
		)
		'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
	}
	'<span class="token string">has properties</span>': stategroup = node-switch .'<span class="token string">properties</span>' (
		| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
		| none  = '<span class="token string">no</span>'
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schema-instance }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schema instance</span>' {
	'<span class="token string">type</span>': component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
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
			'<span class="token string">explicit</span>' {
				/* Target driven `let`.
				 * The type of this `let` is the type of the schema.
				 */
				'<span class="token string">schema</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--schema-instance">'schema instance'</a>
			}
			'<span class="token string">inferred</span>' {
				/* Source driven `let`.
				 * The type of this `let` is inferred from the statement.
				 */
			}
		)
		'<span class="token string">report unused</span>': stategroup (
			'<span class="token string">yes</span>' { }
			'<span class="token string">no</span>' { [ <span class="token operator">@unused</span> ] }
		)
		'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
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

{: #grammar-rule--type-path-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">type path step</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">collection</span>' { [ <span class="token operator">*</span> ] }
				'<span class="token string">choice</span>' {
					'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
				}
				'<span class="token string">node</span>' {
					'<span class="token string">attribute</span>': [ <span class="token operator">.</span> ] reference
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
		'<span class="token string">target</span>' { [ <span class="token operator">target</span> ] }
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
		'<span class="token string">function</span>' {
			'<span class="token string">signature</span>': [ <span class="token operator">function</span> ] component <a href="#grammar-rule--signature">'signature'</a>
		}
		'<span class="token string">type</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--type-path">'type path'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--signature }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signature</span>' {
	/* The signature of a callable.
	 */
	'<span class="token string">template</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator"><</span> <span class="token operator">T</span>, <span class="token operator">></span> ]
			/* Add a template type to the signature.
			 * An optional constraint can be added to the type.
			 */
			'<span class="token string">requirement</span>': stategroup (
				'<span class="token string">plural</span>' { [ <span class="token operator">is</span> <span class="token operator">plural</span> <span class="token operator">E</span> ] }
				'<span class="token string">optional</span>' { [ <span class="token operator">is</span> <span class="token operator">optional</span> <span class="token operator">E</span> ] }
				'<span class="token string">node</span>' { [ <span class="token operator">is</span> <span class="token operator">node</span> ] }
				'<span class="token string">none</span>' { }
			)
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">input</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
		/* The implicit parameter definition.
		 */
		'<span class="token string">context</span>': stategroup (
			'<span class="token string">yes</span>' {
				'<span class="token string">type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
			}
			'<span class="token string">no</span>' { }
		)
		/* Parameter definition.
		 */
		'<span class="token string">parameters</span>': dictionary { [ <span class="token operator">$</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">type</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">has parameters</span>': stategroup = node-switch .'<span class="token string">parameters</span>' (
			| nodes = '<span class="token string">yes</span>' { '<span class="token string">first</span>' = first }
			| none  = '<span class="token string">no</span>'
		)
	}
	/* The exception generation capability.
	 */
	'<span class="token string">exceptions</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">throws</span> ] }
		'<span class="token string">no</span>' { }
	)
	/* The expression guarantee of the output.
	 */
	'<span class="token string">guarantee</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">yes</span>' { }
		'<span class="token string">no</span>' { [ <span class="token operator">unsafe</span> ] }
	)
	/* The type of the output.
	 */
	'<span class="token string">result</span>': stategroup (
		'<span class="token string">explicit</span>' {
			'<span class="token string">result</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
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
	/* Instantiates a callable.
	 * Optional can set the template explicitly.
	 * Otherwise the template, if any, is inferred from the context.
	 */
	'<span class="token string">template</span>': stategroup (
		'<span class="token string">explicit</span>' { [ <span class="token operator"><</span>, <span class="token operator">></span> ]
			'<span class="token string">type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">implicit</span>' { }
	)
	'<span class="token string">object</span>': component <a href="#grammar-rule--hook">'hook'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--function-implementation }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">function implementation</span>' {
	/* The implementation of a function.
	 */
	'<span class="token string">statement</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--function-call }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">function call</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
	/* The arguments for a callable object.
	 */
	'<span class="token string">with context</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">values</span>': dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
	}
}
</pre>
</div>
</div>

{: #grammar-rule--root-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">root selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">library</span>' {
			'<span class="token string">library</span>': reference
			'<span class="token string">tail</span>': [ <span class="token operator">::</span> ] component <a href="#grammar-rule--root-selector">'root selector'</a>
		}
		'<span class="token string">this</span>' { }
	)
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
			/* Select a function.
			 */
			'<span class="token string">context</span>': component <a href="#grammar-rule--root-selector">'root selector'</a>
			'<span class="token string">function</span>': reference
			'<span class="token string">instance</span>': component <a href="#grammar-rule--callable-instance">'callable instance'</a>
		}
		'<span class="token string">recurs</span>' { [ <span class="token operator">self</span> ]
			/* Select self.
			 * This represents the currently executing function.
			 * Only available in a function implementation.
			 */
		}
		'<span class="token string">stored</span>' {
			/* Retrieve a stored function.
			 */
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
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
	'<span class="token string">decimal places</span>': integer
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
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
					'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
				}
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
			'<span class="token string">match style</span>': stategroup (
				'<span class="token string">lazy</span>' {
					/* Lazy matching seeks the smallest possible match. */
				}
				'<span class="token string">greedy</span>' { [ <span class="token operator">*</span> ]
					/* Greedy matching seeks the largest possible match. */
				}
			)
			'<span class="token string">repeat</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
					'<span class="token string">lower</span>': stategroup (
						'<span class="token string">yes</span>' {
							'<span class="token string">min</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">upper</span>': [ <span class="token operator">,</span> ] stategroup (
						'<span class="token string">yes</span>' {
							'<span class="token string">max</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
				}
				'<span class="token string">no</span>' { }
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
	 * Each part must capture a single piece. Only dynamic pieces can be captured.
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

{: #grammar-rule--expression-tail-step }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression tail step</span>' {
	'<span class="token string">step</span>': stategroup (
		'<span class="token string">optional value</span>' { [ <span class="token operator">get</span> ]
			/* Retrieve the value of an optional value.
			 * This fails when the optional value is not set.
			 */
		}
		'<span class="token string">entry lookup</span>' {
			/* Retrieve the value of an entry in a collection.
			 * This fails when the provided key does not exist in the set.
			 */
			'<span class="token string">key</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">file fetch</span>' {
			/* Retrieve a property from a file.
			 */
			'<span class="token string">field</span>': stategroup (
				'<span class="token string">token</span>' { [ <span class="token operator">.token</span> ] }
				'<span class="token string">extension</span>' { [ <span class="token operator">.extension</span> ] }
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
		'<span class="token string">choice cast</span>' {
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

{: #grammar-rule--expression-tail }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression tail</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': component <a href="#grammar-rule--expression-tail-step">'expression tail step'</a>
			'<span class="token string">tail</span>': component <a href="#grammar-rule--expression-tail">'expression tail'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
## Expression
An expression consists of an operation optionally followed by path steps.
No all operations guarantee their result and can fail, indicated by the expression guarantee.
For operations that can fail, either an alternative can be provided or the failure can be propagated to the parent context.

{: #grammar-rule--expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression</span>' {
	'<span class="token string">operation</span>': stategroup (
		'<span class="token string">variable</span>' {
			/* Retrieves a variable from the instance-data.
			 */
			'<span class="token string">variable</span>': [ <span class="token operator">var</span> ] reference
		}
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
					'<span class="token string">format</span>': stategroup (
						'<span class="token string">canonical</span>' {
							/* The canonical textual representation of 8-4-4-4-12 groups of hexadecimal digits.
							 */
						}
						'<span class="token string">base 16</span>' { [ <span class="token operator">base16</span> ]
							/* Format as a big-endian base 16 encoded text.
							 */
						}
						'<span class="token string">base 64</span>' { [ <span class="token operator">base64</span> ]
							/* Format as a big-endian base 64 encoded text.
							 */
						}
					)
				}
			)
		}
		'<span class="token string">static choice</span>' {
			/* Select an option.
			 */
			'<span class="token string">option</span>': [ <span class="token operator">option</span> ] reference
		}
		'<span class="token string">function</span>' { [ <span class="token operator">function</span> ]
			/* Create a function.
			 */
			'<span class="token string">signature</span>': stategroup (
				'<span class="token string">explicit</span>' {
					'<span class="token string">signature</span>': component <a href="#grammar-rule--signature">'signature'</a>
					'<span class="token string">instance</span>': component <a href="#grammar-rule--callable-instance">'callable instance'</a>
				}
				'<span class="token string">inferred</span>' { }
			)
			'<span class="token string">implementation</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--function-implementation">'function implementation'</a>
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ]
			/* Returns none.
			 * This will convert to an empty set for plural values.
			 * This will convert to unset for optional values.
			 */
		}
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
		'<span class="token string">entry key</span>' { [ <span class="token operator">key</span> ]
			/* Retrieve the key of the current entry.
			 * This is only valid inside a `walk` statement.
			 */
		}
		'<span class="token string">parse</span>' { [ <span class="token operator">parse</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">as</span>': [ <span class="token operator">as</span> ] stategroup (
				'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ]
					/* Parses JSON.
					 * On success it results in a document and must first be passed to a decorator before it is usable.
					 */
					'<span class="token string">schema</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] component <a href="#grammar-rule--schema-instance">'schema instance'</a>
				}
				'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ]
					/* Parses a XML document.
					 * On success it results in a document and must first be passed to a decorator before it is usable.
					 */
					'<span class="token string">schema</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] component <a href="#grammar-rule--schema-instance">'schema instance'</a>
				}
				'<span class="token string">CSV</span>' { [ <span class="token operator">CSV</span> ]
					/* Parses a CSV document.
					 * The CSV parser conforms to RFC 4180.
					 * Optionally the cell separator can be changed.
					 * On success it results in a document and must first be passed to a decorator before it is usable.
					 */
					'<span class="token string">separator</span>': stategroup (
						'<span class="token string">custom</span>' { [ <span class="token operator">separator:</span> ]
							'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
						}
						'<span class="token string">default</span>' { }
					)
					'<span class="token string">schema</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] component <a href="#grammar-rule--schema-instance">'schema instance'</a>
				}
				'<span class="token string">choice</span>' { [ <span class="token operator">choice</span> ]
					/* Parses text to a choice.
					*/
					'<span class="token string">schema</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] component <a href="#grammar-rule--schema-instance">'schema instance'</a>
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
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
					/* Parses an integer value in base-10.
					 *  Integer: [-]d
					 *   Any number of digits can be provided, but the supported range is limited by the implementation.
					 *   An optional minus sign is allowed before the first digit to set the sign.
					 */
				}
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					/* Parses a decimal value according to a specific locale.
					 *  The format is locale dependent.
					 */
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
					'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
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
		'<span class="token string">serialize</span>' { [ <span class="token operator">serialize</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">as</span>': [ <span class="token operator">as</span> ] stategroup (
				'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ] }
				'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ] }
				'<span class="token string">ISO Date Time</span>' { [ <span class="token operator">ISODateTime</span> ] }
				'<span class="token string">ISO Date</span>' { [ <span class="token operator">ISODate</span> ] }
				'<span class="token string">ISO Time</span>' { [ <span class="token operator">ISOTime</span> ] }
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">integer digits</span>': stategroup (
						'<span class="token string">custom</span>' {
							'<span class="token string">digits</span>': [, <span class="token operator">.</span> ] integer
						}
						'<span class="token string">default</span>' { }
					)
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
					'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
				}
			)
		}
		'<span class="token string">compare</span>' {
			/* Compares two values.
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
			'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
				'<span class="token string">left</span>': component <a href="#grammar-rule--expression">'expression'</a>
				'<span class="token string">right</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--expression">'expression'</a>
			}
		}
		'<span class="token string">arithmetic</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">inversion</span>' { [ <span class="token operator">-</span> ]
					/* Invert the sign of an integer.
					 */
					'<span class="token string">operand</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
				}
				'<span class="token string">sum</span>' { [ <span class="token operator">sum</span> ]
					/* Calculates the sum of a set of integers.
					 * It results in the sum of all values, or the additive identity when the set is empty.
					 */
					'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--plural-expression">'plural expression'</a>
				}
				'<span class="token string">product</span>' { [ <span class="token operator">product</span> ]
					/* Calculates the product of a set of integers.
					 * It results in the produce of all values, or the multiplicative identity when the set is empty.
					 */
					'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--plural-expression">'plural expression'</a>
				}
				'<span class="token string">division</span>' { [ <span class="token operator">division</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Divide one integer by another integer.
					 * The resulting fraction, if any, is truncated.
					 * This fails when `denominator` is zero.
					 */
					'<span class="token string">numerator</span>': component <a href="#grammar-rule--expression">'expression'</a>
					'<span class="token string">denominator</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--expression">'expression'</a>
				}
			)
		}
		'<span class="token string">concatenation</span>' { [ <span class="token operator">concat</span> ]
			/* Concatenates a set of texts.
			 * Optionally a separator can be added between each element.
			 * The entries are joined in the order of the set.
			 */
			'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--plural-expression">'plural expression'</a>
			'<span class="token string">separator</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">separator:</span> ]
					'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">logic</span>' {
			'<span class="token string">operation</span>': stategroup (
				'<span class="token string">negation</span>' { [ <span class="token operator">not</span> ]
					/* Toggle the value of a boolean.
					 */
					'<span class="token string">operand</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
				}
				'<span class="token string">and</span>' { [ <span class="token operator">and</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Calculates the logical and of a set of booleans.
					 * It fails when the set is empty.
					 */
					'<span class="token string">values</span>': component <a href="#grammar-rule--plural-expression">'plural expression'</a>
				}
				'<span class="token string">or</span>' { [ <span class="token operator">or</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Calculates the logical or of a set of booleans.
					 * It fails when the set is empty.
					 */
					'<span class="token string">values</span>': component <a href="#grammar-rule--plural-expression">'plural expression'</a>
				}
			)
		}
		'<span class="token string">reduce</span>' { [ <span class="token operator">reduce</span> ]
			/* Merge a set of values.
			 */
			'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--plural-expression">'plural expression'</a>
			'<span class="token string">to</span>': [ <span class="token operator">to</span> ] stategroup (
				'<span class="token string">shared</span>' { [ <span class="token operator">shared</span> <span class="token operator">value</span> ]
					/* Reduces a set of values to a single shared value.
					 * Shared values are detected with an equality check.
					 * It succeeds only when all values pass an equality check and the set contains at least one value.
					 */
					'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
				}
				'<span class="token string">unique</span>' { [ <span class="token operator">unique</span> <span class="token operator">values</span> ]
					/* Removes all duplicate values from a set of values.
					 * Duplicates are detected with an equality check.
					 * The order of the set is maintained, duplicates are placed at the first occurrence.
					 */
					'<span class="token string">comparator</span>': component <a href="#grammar-rule--comparator">'comparator'</a>
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
			'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">comparator</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--comparator">'comparator'</a>
			'<span class="token string">key</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression-tail">'expression tail'</a>
		}
		'<span class="token string">file constructor</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
			/* Construct a file object.
			 */
			'<span class="token string">token</span>': [ <span class="token operator">token</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">extension</span>': [ <span class="token operator">extension</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">call</span>' {
			/* Call a function.
			 */
			'<span class="token string">selection</span>': [ <span class="token operator">call</span> ] component <a href="#grammar-rule--callable-selector">'callable selector'</a>
			'<span class="token string">arguments</span>': component <a href="#grammar-rule--function-call">'function call'</a>
		}
	)
	'<span class="token string">tail</span>': component <a href="#grammar-rule--expression-tail">'expression tail'</a>
	'<span class="token string">alternative</span>': component <a href="#grammar-rule--expression-alternative">'expression alternative'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--expression-alternative }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression alternative</span>' {
	'<span class="token string">alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">||</span> ] stategroup (
				'<span class="token string">value</span>' {
					/* Provide an alternative expression. */
					'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
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

{: #grammar-rule--plural-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural expression</span>' {
	'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
	'<span class="token string">is plural</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">*</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--expression-tail">'expression tail'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': [ <span class="token operator">,</span> ] component <a href="#grammar-rule--plural-expression">'plural expression'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
## Safe Expression
This represents a top-level expression.
A safe expression indicates that an expression guarantee of no cannot be propagated from the wrapped expression.
The wrapped expression must always have an alternative with a guarantee of yes, or throw.

{: #grammar-rule--safe-expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">safe expression</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--expression">'expression'</a>
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
		'<span class="token string">set</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">node</span>' {
					/* Target a node.
					 * All mandatory properties must be specified.
					 * Optional properties may be omitted, which is identical to setting them to `unset`.
					 * When a property has attributes, all attributes must also be specified.
					 */
					'<span class="token string">properties</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
						'<span class="token string">has previous</span>': stategroup = node-switch predecessor (
							| node = '<span class="token string">yes</span>' { '<span class="token string">previous</span>' = predecessor }
							| none = '<span class="token string">no</span>'
						)
						'<span class="token string">attributes</span>': stategroup (
							'<span class="token string">yes</span>' {
								'<span class="token string">attributes</span>': [ <span class="token operator"><</span>, <span class="token operator">></span> ] dictionary {
									'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--target-expression">'target expression'</a>
								}
							}
							'<span class="token string">no</span>' { }
						)
						'<span class="token string">obscure data</span>': stategroup (
							'<span class="token string">inherit</span>' { }
							'<span class="token string">exclude</span>' { [ <span class="token operator">@exclude</span> ] }
						)
						'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
					}
					'<span class="token string">has properties</span>': stategroup = node-switch .'<span class="token string">properties</span>' (
						| nodes = '<span class="token string">yes</span>' { '<span class="token string">last</span>' = last }
						| none  = '<span class="token string">no</span>'
					)
				}
				'<span class="token string">entry</span>' { [ <span class="token operator">create</span> ]
					/* Create a new set with a single entry.
					 * When the set has implicit keys, a key must be provided.
					 */
					'<span class="token string">implicit key</span>': stategroup (
						'<span class="token string">yes</span>' {
							'<span class="token string">value</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
				}
				'<span class="token string">state</span>' { [ <span class="token operator">create</span> ]
					/* Set a choice to the specified option.
					 */
					'<span class="token string">state</span>': reference
					'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
				}
			)
		}
		'<span class="token string">inferred</span>' {
			/* Assign any value from an expression.
			*/
			'<span class="token string">value</span>': component <a href="#grammar-rule--safe-expression">'safe expression'</a>
		}
	)
}
</pre>
</div>
</div>
## Statement
A statement is responsible for the control flow of the processor.
All statements produce a value that is return to the parent context.

Each statement is bound to an execution context.
The execution context can be restricted when the statement is not allowed to fail.
When the execution context is restricted, operations that (could) generate errors are disabled.

{: #grammar-rule--statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">statement</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">block</span>' {
			'<span class="token string">block</span>': component <a href="#grammar-rule--block-statement">'block statement'</a>
		}
		'<span class="token string">guard</span>' {
			/* Guard a statement and provide an alternative path.
			 * The execution context of the guarded statement is always free, the fallback statement inherits the current execution context.
			 * This catches all throws found in the guarded statement, including implicit throws generated by the runtime.
			 * When the guarded statement is successfully executed, the fallback statement is skipped.
			 */
			'<span class="token string">guarded statement</span>': [ <span class="token operator">try</span> ] component <a href="#grammar-rule--statement">'statement'</a>
			'<span class="token string">optional assignment</span>': [ <span class="token operator">catch</span> ] stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">as</span> <span class="token operator">$</span> ] }
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">fallback statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
		}
		'<span class="token string">switch</span>' {
			'<span class="token string">value</span>': [ <span class="token operator">switch</span> ] component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">boolean</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Execute a conditional branch.
					 * The condition is evaluated and based on the result, either the `true` or `false` case is executed.
					 */
					'<span class="token string">on true</span>': [ <span class="token operator">|</span> <span class="token operator">true</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					'<span class="token string">on false</span>': [ <span class="token operator">|</span> <span class="token operator">false</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">existence</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
					/* Execute a conditional branch.
					 * The expression without a guarantee of yes is evaluated.
					 * Based on whether or not the expression succeeded or failed, the corresponding case is executed.
					 * When the expression succeeds, the result is available in `$`.
					 */
					'<span class="token string">on value</span>': [ <span class="token operator">|</span> <span class="token operator">value</span> <span class="token operator">as</span> <span class="token operator">$</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
					'<span class="token string">on none</span>': [ <span class="token operator">|</span> <span class="token operator">none</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">choice</span>' {
					/* Execute a conditional branch.
					 * The branch is determined based on a user defined choice.
					 * The value of the option is optionally available in `$`.
					 */
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
			'<span class="token string">type</span>': [ <span class="token operator">walk</span> ] stategroup (
				'<span class="token string">plural</span>' {
					/* Execute a statement once for each entry in a set.
					 * The entry for which the statement is executed, is available in `$`.
					 */
					'<span class="token string">value</span>': [, <span class="token operator">as</span> <span class="token operator">$</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
					'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">range</span>' {
					/* Execute a statement for a range of integers.
					 */
					'<span class="token string">range</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
						'<span class="token string">begin</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
						'<span class="token string">end</span>': [ <span class="token operator">until</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
						'<span class="token string">step</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
					}
					'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
			)
			/* The result is determined by the following:
			 *  - When the sub-statement results in a plural type, the results are merged into a single set.
			 *  - Otherwise a new list of the result type is created.
			 */
			'<span class="token string">merge</span>': component <a href="#grammar-rule--hook">'hook'</a>
		}
		'<span class="token string">log</span>' {
			/* Write a message to the selected channel.
			 */
			'<span class="token string">channel</span>': stategroup (
				'<span class="token string">functional error</span>' { [ <span class="token operator">@error:</span> ] }
				'<span class="token string">information</span>' { [ <span class="token operator">@log:</span> ] }
			)
			'<span class="token string">message</span>': component <a href="#grammar-rule--safe-expression">'safe expression'</a>
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
		'<span class="token string">fail</span>' { [ <span class="token operator">fail</span> ]
			/* Completes a function without yielding a value.
			 */
		}
		'<span class="token string">produce</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">explicit</span>' {
					'<span class="token string">path</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--type-path">'type path'</a>
				}
				'<span class="token string">inferred</span>' { }
			)
			'<span class="token string">target</span>': component <a href="#grammar-rule--target-expression">'target expression'</a>
		}
		'<span class="token string">execute</span>' {
			/* Execute a Alan Interface command or event.
			 */
			'<span class="token string">context</span>': [ <span class="token operator">execute</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
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
	'<span class="token string">result</span>': stategroup (
		'<span class="token string">discard</span>' { [ <span class="token operator">do</span> ]
			/* Discard the result of the statement.
			 * The statement is evaluated pure for side-effects.
			 * The result does not participate in the result of the entire sequence.
			 */
		}
		'<span class="token string">return</span>' { }
	)
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

{: #grammar-rule--block-statement }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">block statement</span>' { [ <span class="token operator">{</span>, <span class="token operator">}</span> ]
	/* Start a new block.
	 * Optionally a block can introduce a new scope.
	 * A block allows multiple independent statements to be written in the same context.
	 * The result of the sequence of statements is determined by the following rules:
	 *  - Statements with a result of none, do not participate in the result of the entire sequence.
	 *  - When no statements participate, the result of the sequence is none.
	 *  - When only single statement participates, the result of the sequence is the result of that statement.
	 *  - When multiple statement participate, all must be of the same plural type and the individual values are merged, the sequence result is the result of the merge.
	 */
	'<span class="token string">scope</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">stack block</span>': component <a href="#grammar-rule--stack-block">'stack block'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">statement</span>': component <a href="#grammar-rule--statements">'statements'</a>
}
</pre>
</div>
</div>
