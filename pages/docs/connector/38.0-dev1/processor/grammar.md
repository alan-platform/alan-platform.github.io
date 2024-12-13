---
layout: "doc"
origin: "connector"
language: "processor"
version: "38.0-dev1"
type: "grammar"
---

1. TOC
{:toc}

# Release Notes

## 37.0
#### Variables form runtime configuration
The values of variables are now obtained form the runtime configuration of the system.
The available variables are now defined by the project wiring.

[example](./tests/variable-integer/processor.alan).

[example](./tests/variable-text/processor.alan).
# The Standard Libraries
The connector provides a set of standard libraries.
These libraries provide functionality outside the language constructs of the connector.
## Calendar
The calendar library provides conversions between the connectors internal date time representation and broken down time.

```js
define 'type': @API choice ( 'date' 'date-time' 'time' )

define 'calendar': @API {
	'year': integer
	'month': integer @limit: { 1 , 12 }
	'day': integer @limit: { 1 , 31 }
}

define 'weekday': @API choice ( 'Monday': 1 'Tuesday': 2 'Wednesday': 3 'Thursday': 4 'Friday': 5 'Saturday': 6 'Sunday': 7 )

define 'week': @API {
	'year': integer
	'week': integer @limit: { 1 , 53 }
	'day': 'weekday'
}

define 'ordinal': @API {
	'year': integer
	'day': integer @limit: { 1 , 366 }
}

define 'time': @API {
	'hour': integer @limit: { 0 , 23 }
	'minute': integer @limit: { 0 , 59 }
	'second': integer @limit: { 0 , 59 }
}

define 'date time': @API {
	'calendar': 'calendar'
	'week': 'week'
	'ordinal': 'ordinal'
	'time': 'time'
}

define 'constructor': @API {
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
) : 'date time' = "51eedd39c3d5f175ac0da05d4cbc4aa78d7ca349"

/* Construct Alan Time from broken down time.
 * The result is either a date-time or a date, depending on whether or not 'time' is set.
 * When timezone is not set, it will be evaluated in Etc/UTC.
 */
define 'construct': function (
	'constructor'
	$'timezone': optional text
) : integer = "deadb7441535bd91e23f564564ef24ea6c76201b"

library
```
### Calendar Examples

```js
consumer ( )

routine 'test' on root
do {
	let $'source': 'calendar'/'constructor' = (
		'date' = create 'calendar' (
			'year' = 2021
			'month' = 2
			'day' = 3
		)
		'time' = (
			'hour' = 10
			'minute' = 20
			'second' = 30
		)
	)
	let $'value' = call 'calendar'::'construct' (
		$'source'
		$'timezone' = set "Europe/Amsterdam"
	)

	switch is ( $'value', 212479060830 ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root
do {
	let $'source': 'calendar'/'constructor' = (
		'date' = create 'calendar' (
			'year' = 2021
			'month' = 8
			'day' = 4
		)
		'time' = (
			'hour' = 10
			'minute' = 20
			'second' = 30
		)
	)
	let $'value' = call 'calendar'::'construct' (
		$'source'
		$'timezone' = set "Europe/Amsterdam"
	)

	switch is ( $'value', 212494782030 ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```
## Network
The network library provides functions to perform network request and the data structures to represent related objects.

```js
define 'network method': @API choice ( 'get' 'head' 'post' 'put' 'delete' )

define 'network security': @API choice ( 'strict' 'preferred' 'none' )

define 'key value list': @API collection case folding text

define 'network request': @API {
	'method': 'network method'
	'parameters': optional 'key value list'
	'headers': optional 'key value list'
	'content': optional binary
}

define 'network response': @API {
	'status': integer
	'headers': 'key value list'
	'content': binary
}

define 'network authentication': @API {
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

define 'network message part': @API {
	'mime type': text
	'mime sub type': text
	'content': binary
}

define 'network message part list': @API list {
	'name': text
	'part': 'network message part'
}

define 'network message': @API {
	'from': 'key value list'
	'recipients': 'key value list'
	'recipients extra': optional 'key value list'
	'recipients hidden': optional 'key value list'
	'subject': optional text
	'headers': optional 'key value list'
	'attachments': optional 'network message part list'
	'body related': optional 'network message part list'
	'body': 'network message part'
}

/* Parses and decorates text as 'network message'.
 * A 'preferred mime subtype' of MIME type `text` must be provided.
 * When a MIME part with this type is found, it becomes a candidate for the body.
 * The MIME type `text/plain` is always considered as a candidate for the body.
 */
define 'parse network message': function (
	binary
	$'preferred mime subtype': text
) : unsafe 'network message' = "b2a2d89de3b939e67e1ee6e2de957c0ffeeca418"

/* Serializes a 'network message' to text.
 */
define 'serialize network message': function (
	'network message'
	$'include hidden recipients': boolean
) : unsafe binary = "536ba1ca4408cb166bff181d546cd0e47a73d943"

/* Performs an HTTP(S) request.
 * Methods are mapped directly to their HTTP equivalent.
 * When provided, 'content' is send with the request.
 */
define 'http': function (
	$'server': text
	$'path': text
	$'authentication': optional 'network authentication'
	$'request': 'network request'
) : unsafe 'network response' = "588ebe5b89772935df17c9415ad893e803ee4389"

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
	$'method': 'network method'
	$'authentication': optional 'network authentication'
	$'security': 'network security'
	$'content': optional binary
) : unsafe optional binary = "c6998cf3b3f5407b3f5e3560664a6f196bc9bc9e"

/* Retrieves all messages matching 'criteria' with IMAP(S).
 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
 * All messages are parsed as if passed to `function 'parse network message'`.
 */
define 'imap': function (
	$'server': text
	$'path': text
	$'criteria': text
	$'authentication': optional 'network authentication'
	$'security': 'network security'
	$'preferred mime subtype': text
) : unsafe list 'network message' = "cfa2e53a9406c4a434da0db4c284bd598fbd2cb6"

/* Retrieves all messages matching 'criteria' with IMAP(S).
 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
 */
define 'imap list': function (
	$'server': text
	$'path': text
	$'criteria': text
	$'authentication': optional 'network authentication'
	$'security': 'network security'
	$'callback': function ( $'blob': binary ) : on boolean
) : unsafe list boolean = "398fc59dc553be91ebc465188c255360548239a9"

/* Send a message with SMTP(S).
 * The message is serialized as if passed to `function 'serialize network message'`.
 * When the transfer fails, this function throws an error.
 */
define 'smtp': function (
	$'server': text
	$'authentication': optional 'network authentication'
	$'security': 'network security'
	$'message': 'network message'
) : unsafe boolean = "63920ddc94b96041d3a9962be42a313b3119c8d0"

library
	/* Register webserver handlers.
	 * The handler is used as the path to respond to.
	 * Each handler is triggered by external web requests for the path.
	 */
	hook 'webserver'
		( $'request': 'network request' ) : on 'network response' = "044bdc2dd86dc731d5f087429ffaddc8ecbb5d63"
```
### Network Examples

```js
consumer ( )

/* Standard Library `network.lib`::`http` example
 *  this performs a simple HTTPS GET request and validates the response status
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'response' = call 'network'::'http' (
		$'server'         = "https://example.com"
		$'path'           = "/path/to/resource"
		$'authentication' = unset
		$'request'        = new (
			'method' = option 'get'
			'parameters' = create [ "parameter" ] "value"
		)
	) || throw "http request failed"

	switch less-than ( $'response'.'status', 400 ) (
		| true => no-op /* from here `$'response'.'content'` contains the resource data as `binary` */
		| false => no-op /* from here `$'response'.'content'` contains the error response as `binary` */
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`http` example
 *  this performs a simple HTTPS PUT request and validates the response status
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'response' = call 'network'::'http' (
		$'server'         = "https://example.com"
		$'path'           = "/path/to/resource"
		$'authentication' = unset
		$'request'        = new (
			'method' = option 'put'
			'headers' = create [ "content-type" ] "text/plain"
			'content' = call 'unicode'::'as binary' ( "hello world" )
		)
	) || throw "http request failed"

	switch less-than ( $'response'.'status', 400 ) (
		| true => no-op /* from here `$'response'.'content'` contains the resource data as `binary` */
		| false => no-op /* from here `$'response'.'content'` contains the error response as `binary` */
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`http` example
 *  this performs a simple HTTPS GET request with authentication and validates the response status
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'response' = call 'network'::'http' (
		$'server'         = "https://example.com"
		$'path'           = "/path/to/resource"
		$'authentication' = set new (
			'type' = create 'user' (
				'username' = "username"
				'password' = "password"
			)
		)
		$'request'        = new (
			'method' = option 'get'
		)
	) || throw "http request failed"

	switch less-than ( $'response'.'status', 400 ) (
		| true => no-op /* from here `$'response'.'content'` contains the resource data as `binary` */
		| false => no-op /* from here `$'response'.'content'` contains the error response as `binary` */
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`ftp` example
 *  this performs a simple FTPS GET request
 *  note that different versions of security exists for ftp
 *   > implicit security uses the `ftps://` protocol
 *   > explicit security uses the `ftp://` protocol and `STARTTLS` command
 *  by default we fail when the connection cannot be secured, see the example `stdlib.network.ftp.insecure` for an alternative
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'resource' = call 'network'::'ftp' (
		$'server'         = "ftps://example.com"
		$'path'           = "/path/to/resource"
		$'method'         = option 'get'
		$'authentication' = unset
		$'security'       = option 'strict'
		$'content'        = unset
	) || throw "ftp request failed"

	switch $'resource' get (
		| value as $ => no-op /* from here `$` contains the resource data as `binary` */
		| error => no-op
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`ftp` example
 *  this performs a simple FTPS GET request on a directory and parses the result
 *  note that different versions of security exists for ftp
 *   > implicit security uses the `ftps://` protocol
 *   > explicit security uses the `ftp://` protocol and `STARTTLS` command
 *  by default we fail when the connection cannot be secured, see the example `stdlib.network.ftp.insecure` for an alternative
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'resource' = call 'network'::'ftp' (
		$'server'         = "ftps://example.com"
		$'path'           = "/path/to/resource"
		$'method'         = option 'head'
		$'authentication' = unset
		$'security'       = option 'strict'
		$'content'        = unset
	) || throw "ftp request failed"
	let $'file list' = call 'unicode'::'split' (
		call 'unicode'::'import' (
			$'resource' get
			$'encoding' = "ASCII"
		)
		$'style' = option 'none'
	) || throw "ftp response parse error"

	walk $'file list' as $ => no-op /* from here `$` contains the file name relative to `$'path'` */
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`ftp` example
 *  this performs a simple FTPS PUT request
 *  note that different versions of security exists for ftp
 *   > implicit security uses the `ftps://` protocol
 *   > explicit security uses the `ftp://` protocol and `STARTTLS` command
 *  by default we fail when the connection cannot be secured, see the example `stdlib.network.ftp.insecure` for an alternative
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'resource' = call 'network'::'ftp' (
		$'server'         = "ftps://example.com"
		$'path'           = "/path/to/resource"
		$'method'         = option 'put'
		$'authentication' = unset
		$'security'       = option 'strict'
		$'content'        = set call 'unicode'::'as binary' ( "hello world" )
	) || throw "ftp request failed"

	switch $'resource' get (
		| value as $ => no-op /* from here `$` contains the resource data as `binary` */
		| error => no-op
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`ftp` example
 *  this performs a simple FTPS DELETE request
 *  caveat:
 *    unlike other FTPS request, this sends the path to the server as-is
 *    as a result the behavior of this instruction can vary between servers
 *  note that different versions of security exists for ftp
 *   > implicit security uses the `ftps://` protocol
 *   > explicit security uses the `ftp://` protocol and `STARTTLS` command
 *  by default we fail when the connection cannot be secured, see the example `stdlib.network.ftp.insecure` for an alternative
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'resource' = call 'network'::'ftp' (
		$'server'         = "ftps://example.com"
		$'path'           = "/path/to/resource"
		$'method'         = option 'delete'
		$'authentication' = unset
		$'security'       = option 'strict'
		$'content'        = unset
	) || throw "ftp request failed"

	switch $'resource' get (
		| value as $ => no-op /* from here `$` contains the resource data as `binary` */
		| error => no-op
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`ftp` example
 *  this performs a simple FTPS GET request
 *  note that different versions of security exists for ftp
 *   > implicit security uses the `ftps://` protocol
 *   > explicit security uses the `ftp://` protocol and `STARTTLS` command
 *  by default we fail when the connection cannot be secured, this example changes this behavior
 *   > for implicit security this option has no effect
 *   > for explicit security this option will suppress failures when we cannot secure the connection, it will NOT disable security when it is available
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'resource' = call 'network'::'ftp' (
		$'server'         = "ftps://example.com"
		$'path'           = "/path/to/resource"
		$'method'         = option 'get'
		$'authentication' = unset
		$'security'       = option 'preferred' /* or 'none' to completely disable security */
		$'content'        = unset
	) || throw "ftp request failed"

	switch $'resource' get (
		| value as $ => no-op /* from here `$` contains the resource data as `binary` */
		| error => no-op
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`imap` example
 *  this performs a simple IMAPS request to load all new messages
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'messages' = call 'network'::'imap' (
		$'server'                 = "imaps://example.com"
		$'path'                   = "/INBOX/"
		$'criteria'               = "NEW"
		$'authentication'         = unset
		$'security'               = option 'strict'
		$'preferred mime subtype' = "html"
	) || throw "imap request failed"

	walk $'messages' as $ => no-op /* from here $ contains the message as `'network.lib'::'network message'` */
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`imap list` example
 *  this performs a simple IMAPS request to download all new messages
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	let $'results' = call 'network'::'imap list' (
		$'server'         = "imaps://example.com"
		$'path'           = "/INBOX/"
		$'criteria'       = "NEW"
		$'authentication' = unset
		$'security'       = option 'strict'
		$'callback'       = function => {
			/* here the parameter $'blob' contains the unparsed message as `binary` */
			false
		}
	) || throw "imap request failed"

	walk $'results' as $ => no-op /* from here $ contains the result of the user callback */
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`smtp` example
 *  this performs a simple SMTPS request to send an email
 *  note that different versions of security exists for smtp
 *   > implicit security uses the `smtps://` protocol
 *   > explicit security uses the `smtp://` protocol and `STARTTLS` command
 *  by default we fail when the connection cannot be secured, see the example `stdlib.network.ftp.insecure` for an alternative
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on root
do {
	switch call 'network'::'smtp' (
		$'server'         = "smtps://example.com"
		$'authentication' = unset
		$'security'       = option 'strict'
		$'message'        = new (
			'from' = create [ "Me" ] "me@example.com"
			'recipients' = create [ "You" ] "you@example.com"
			'subject' = "example message"
			'attachments' = create (
				'name' = "hello.txt"
				'part' = (
					'mime type' = "text"
					'mime sub type' = "plain"
					'content' = call 'unicode'::'as binary' ( "hello world" )
				)
			)
			'body' = (
				'mime type' = "text"
				'mime sub type' = "plain"
				'content' = call 'unicode'::'as binary' ( "hello world" )
			)
		)
	) (
		| value as $ => /* from here `$` always contains true as `boolean` */ no-op
		| error => throw "smtp request failed"
	)
}
```

```js
consumer ( )

/* Standard Library `network.lib`::`webserver` example
 *  this registers a webserver hook for the `/echo` path
 *  the original request is returned as JSON
 */
add-hook 'network'::'webserver' "/echo"
do (
	'status' = 200
	'headers' = create [ "content-type" ] "application/json"
	'content' = call 'unicode'::'as binary' ( serialize $'request' as JSON )
)
```
## Plural
The plural library provides algorithms operating on sets.

```js
/* Sorts a set based on a comparison function.
 */
define 'sort': function < plural T > (
	plural T
	$'compare': function (
		$'A': T
		$'B': T
	) : on boolean
) : plural T = "1e12c9b9dca734acece28242dbb5bde017f5f48e"

/* Selects a single entry in a set based on a comparison function.
 * This returns the entry for which `compare` results in true when the entry is `A` and false when `B` compared to all other entries in the set.
 * It fails when no such entry is found.
 */
define 'select': function < plural T > (
	plural T
	$'compare': function (
		$'A': T
		$'B': T
	) : on boolean
) : unsafe T = "9a9c7f481fa42b568780431b70468377eff7b4d6"

/* Filters a set.
 * This returns a new set containing only the entries for which `filter` results in true.
 */
define 'filter': function < plural T > (
	plural T
	$'filter': function ( $'entry': T ) : on boolean
) : plural T = "3febf93164d1e9fdf7fb631964ee8dbfa34364e6"

/* Divide a set in several smaller sets (buckets).
 * The order of the entries is maintained.
 */
define 'split': function < plural T > (
	plural T
	$'bucket size': integer
) : plural [integer] plural T = "ef5d5b16ed8acc5e95968e8792460ea7e5027baf"

library
```
### Plural Examples

```js
consumer ( )

routine 'test' on root
do {
	let $'data': list boolean = {
		create true
		create false
		create true
	}
	let $'value' = call 'plural'::'filter' (
		$'data'
		$'filter' = function => {
			$'entry'
		}
	)

	switch is ( $'value' .size , 2 ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root
do {
	let $'data': list integer = {
		create 5
		create 2
		create 5
	}
	let $'magic' = 5
	let $'value' = call 'plural'::'filter' (
		$'data'
		$'filter' = function => {
			is ( $'entry', ^ $'magic' )
		}
	)

	switch is ( $'value' .size , 2 ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root ( as $'Context' )
do {
	let $'object' = call 'plural'::'select' (
		^ $'Context'.'objects'
		$'compare' = function => {
			greater-than ( $'A'.'value', $'B'.'value' )
		}
	) || throw "no unique object to select"

	switch is ( $'object'.'key', "two" ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root ( as $'Context' )
do {
	let $'object' = call 'plural'::'select' (
		^ $'Context'.'objects'
		$'compare' = function => {
			greater-than ( $'A'.'value', $'B'.'value' )
		}
	) || throw "no unique object to select"

	switch is ( $'object'.'key', "two" ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root ( as $'Context' )
do try {
	let $'object' = call 'plural'::'select' (
		^ $'Context'.'objects'
		$'compare' = function => {
			greater-than ( $'A'.'has value'?'yes'.'value', $'B'.'has value'?'yes'.'value' ) || throw "comparison data missing"
		}
	) || throw "no selection"

	throw "object selected"
}
catch as $ => switch is ( $ , "comparison data missing" ) (
	| true => no-op
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on root
do {
	let $'data': list integer = {
		create 16
		create 42
		create 39
	}
	let $'value' = call 'plural'::'sort' (
		$'data'
		$'compare' = function => {
			less-than ( $'A', $'B' )
		}
	)
	let $'result': list text = walk $'value' as $ => create serialize $ as integer

	switch is ( concat ( $'result'* ) separator: ( "," ) , "16,39,42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root
do {
	let $'data': list integer = {
		create 16
		create 42
		create 39
		create 17
		create 43
		create 38
		create 18
		create 44
		create 37
	}
	let $'result': list {
		'bucket': list integer
	} = walk call 'plural'::'split' (
		$'data'
		$'bucket size' = 2
	) as $ => create (
		'bucket' = walk $ as $ => create $
	)

	switch is ( serialize $'result' as JSON , "[{\"bucket\":[16,42]},{\"bucket\":[39,17]},{\"bucket\":[43,38]},{\"bucket\":[18,44]},{\"bucket\":[37]}]" ) (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```
## Unicode
The unicode library provides functions to manipulate text values.

```js
define 'trim style': @API choice ( 'leading' 'trailing' 'both' 'none' )

define 'alignment': @API choice ( 'left' 'right' )

define 'message data': @API {
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
) : unsafe text = "2a30a9e7d2998ed8e90e8a52faf49524428869e2"

/* Exports text to binary data.
 * Text is converted to the specified encoding from the internal encoding.
 * When the specified encoding is not known, or no know conversion from the internal encoding is known, the function fails.
 */
define 'export': function (
	text
	$'encoding': text
) : unsafe binary = "eef64c686f47558009eed2c75d6ebebae60218f4"

/* Returns a text value as binary data.
 * The data is encoded in the internal encoding.
 */
define 'as binary': function ( text ) : binary = "6ca6f8af19bedc6c3331e46bc50a46419f650b27"

/* Replaces all occurrences of the key of the entries in the dictionary with their value.
 */
define 'escape': function (
	text
	$'dictionary': collection text
) : text = "9b8118302c78a0a0ac8e573fa24c146a99595f50"

/* Removes all whitespace from a text value.
 */
define 'strip': function ( text ) : text = "5f803c7c0221d927f7af26b514aea3c7b2b42a0a"

/* Removes leading and/or trailing whitespace from a text value.
 */
define 'trim': function (
	text
	$'style': 'trim style'
) : text = "21e65a1d7106bddaf944bb7d606ed55d0125c324"

/* Split a text into multiple fragments.
 * Empty fragments are automatically removed.
 */
define 'split': function (
	text
	$'style': 'trim style'
) : list text = "aad8e969821db39075163a87a5574563c96e8b1e"

/* Adds whitespace to a text value.
 */
define 'pad': function (
	text
	$'align': 'alignment'
	$'length': integer
) : text = "68cc5618910aaf039f8dcfb531622c4b4217035f"

/* Match a text with a Regular Expression.
 * The whole input must match the pattern.
 */
define 'regex': function (
	text
	$'pattern': text
) : unsafe boolean = "6b34fc680c1447dfe88011fe3582bce02458aae6"

/* Format a message with dynamic data.
 * Pattern syntax:
 *  message = messageText (argument messageText)*
 *  argument = noneArg | simpleArg | complexArg
 *  complexArg = choiceArg | pluralArg | selectArg | selectordinalArg
 *
 *  noneArg = '{' argNameOrNumber '}'
 *  simpleArg = '{' argNameOrNumber ',' argType [',' argStyle] '}'
 *  choiceArg = '{' argNameOrNumber ',' "choice" ',' choiceStyle '}'
 *  pluralArg = '{' argNameOrNumber ',' "plural" ',' pluralStyle '}'
 *  selectArg = '{' argNameOrNumber ',' "select" ',' selectStyle '}'
 *  selectordinalArg = '{' argNameOrNumber ',' "selectordinal" ',' pluralStyle '}'
 *
 *  choiceStyle: see ChoiceFormat
 *  pluralStyle: see PluralFormat
 *  selectStyle: see SelectFormat
 *
 *  argNameOrNumber = argName | argNumber
 *  argName = [^[[:Pattern_Syntax:][:Pattern_White_Space:]]]+
 *  argNumber = '0' | ('1'..'9' ('0'..'9')*)
 *
 *  argType = "number" | "date" | "time" | "spellout" | "ordinal" | "duration"
 *  argStyle = "short" | "medium" | "long" | "full" | "integer" | "currency" | "percent" | argStyleText | "::" argSkeletonText
 *
 * For more information see: https://unicode-org.github.io/icu/userguide/format_parse/
 */
define 'format': function (
	text
	$'data': 'message data'
	$'locale': text
) : unsafe text = "4017ef8bdd42eef994def6b0eb189346351e42a3"

/* Result of the template function.
 */
define 'template result': @API {
	'success': boolean /* Value indicating whether the template was transformed correctly or not. */
	'result': text /* On success contains the transformed template, on failure contains the error message. */
	'schema': text /* The schema inferred from the input data. */
}

/* Format a template with dynamic data.
 */
define 'template': function < node T > (
	T
	$'template': text
	$'locale': text
) : unsafe 'template result' = "d0e58dbcfa96708039017255c3b859a9ddd83bd7"

library
```
### Unicode Examples

```js
consumer ( )

routine 'test' on root
do switch is ( "ç", "ç" ) (
	| true => no-op
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on root
do switch is case folding ( "Ç", "ç" ) (
	| true => no-op
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on root
do {
	/* test vectors for format function */
	let $'vectors': list {
		'format': text
		'result': text
	} = {
		create (
			'format' = "{nr,spellout}"
			'result' = "vier­duizend­twee­honderd"
		)
		create (
			'format' = "{nr,number,currency}"
			'result' = "€ 4.200,00"
		)
		create (
			'format' = "{nr,number}"
			'result' = "4.200"
		)
		create (
			'format' = "{nr}"
			'result' = "4.200"
		)
		create (
			'format' = "{tx}"
			'result' = "hello"
		)
		create (
			'format' = "{dt,date}"
			'result' = "3 feb. 2021"
		)
	}
	let $'data': 'unicode'/'message data' = (
		'types' = {
			create [ "dt" ] create 'calendar' 212479064430
			create [ "nr" ] create 'number' 4200
			create [ "tx" ] create 'text' "hello"
		}
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'pattern' = $
		let $'message' = call 'unicode'::'format' (
			$'pattern'.'format'
			$'data'   = ^ $'data'
			$'locale' = "nl_NL"
		) || throw "error"

		switch is ( $'message', $'pattern'.'result' ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on root
do {
	/* test vectors for trim function */
	let $'vectors': list {
		'input': text
		'result': text
		'align': 'unicode'/'alignment'
		'length': integer
	} = {
		create (
			'input' = "hello"
			'result' = "hello     "
			'align' = option 'left'
			'length' = 10
		)
		create (
			'input' = "hello"
			'result' = "     hello"
			'align' = option 'right'
			'length' = 10
		)
		create (
			'input' = "hello"
			'result' = "hello"
			'align' = option 'left'
			'length' = 2
		)
		create (
			'input' = "à"
			'result' = "à "
			'align' = option 'left'
			'length' = 2
		)
	}

	/* test each vector */
	walk $'vectors' as $ => {
		let $'test' = call 'unicode'::'pad' (
			$ .'input'
			$'align'  = $ .'align'
			$'length' = $ .'length'
		)

		switch is ( $'test', $ .'result' ) (
			| true => no-op
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on root
do {
	let $'match' = call 'unicode'::'regex' (
		"abcde"
		$'pattern' = "[a-z]+"
	) || throw "invalid pattern"

	switch $'match' (
		| true => no-op
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on root
do {
	let $'match' = call 'unicode'::'regex' (
		"abCde"
		$'pattern' = "[a-z]+"
	) || throw "invalid pattern"

	switch $'match' (
		| true => throw "produced wrong value"
		| false => no-op
	)
}
```

```js
consumer ( )

routine 'test' on root
do try {
	let $'match' = call 'unicode'::'regex' (
		"abcde"
		$'pattern' = "[a-z+"
	) || throw "invalid pattern"

	throw "valid pattern"
	/* suppress unused warnings */
	switch $'match' (
		| true => no-op
		| false => no-op
	)
}
catch as $ => switch is ( $ , "invalid pattern" ) (
	| true => no-op
	| false => throw "produced wrong value"
)
```

```js
provider (
	'lines' = {
		let $'lines' = call 'unicode'::'split' (
			"line-0
line-1

line-2"
			$'style' = option 'both'
		)

		walk $'lines' as $ => create (
			'line' = $
		)
	}
)
```

```js
consumer ( )

routine 'test' on root
do {
	/* test vectors for trim function */
	let $'vectors': list text = {
		create "line" // nothing to trim
		create "   line" // leading spaces
		create "line   " // trailing spaces
		create " l i n e " // internal spaces
		create "　l　i　n　e　" // no-ASCII space
	}

	/* test each vector */
	walk $'vectors' as $ => {
		let $'line' = $
		let $'trim' = call 'unicode'::'strip' ( $'line' )

		switch is ( $'trim', "line" ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on root
do {
	/* test vectors for trim function */
	let $'vectors': list text = {
		create "line" // nothing to trim
		create "   line" // leading spaces
		create "line   " // trailing spaces
		create "	line" // tabs
		create "　line" // no-ASCII space
	}

	/* test each vector */
	walk $'vectors' as $ => {
		let $'line' = $
		let $'trim' = call 'unicode'::'trim' (
			$'line'
			$'style' = option 'both'
		)

		switch is ( $'trim', "line" ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```
## Data
The data library provides functions to manipulate binary values.

```js
define 'base64 alphabet': @API choice ( 'base64' 'base64url' )

/* Converts text from one encoding to another.
 * Available encodings depend on the hosting systems.
 */
define 'convert': function (
	binary
	$'from': text
	$'to': text
) : unsafe binary = "e4d0f6bf9b7b7cabe8e8c2cc4b53d115c550440b"

/* Convert binary data to base64 text.
 * Alphabet as defined by RFC-4648.
 */
define 'base64 encode': function (
	binary
	$'alphabet': 'base64 alphabet'
) : text = "c5d27c860215386717377807e82176b389f45750"

/* Convert base64 text to binary data.
 * Alphabet as defined by RFC-4648.
 */
define 'base64 decode': function (
	text
	$'alphabet': 'base64 alphabet'
) : unsafe binary = "29b622344bcdebb3830f4fca17cbaac8d9c4db86"

/* Loads an archive from data.
 * Archive format and any compression/encoding are automatically detected.
 */
define 'load archive': function ( binary ) : unsafe collection binary = "ba36303d2703a9e1d737118905544d36c7755e5a"

library
```
# Examples

```js
consumer ( )

/* now example
 *  this example demonstrates the usages of the now instruction
 */
routine 'test' on root
do {
	let $'date-time' = now

	no-op
	/* suppress unused warnings */
	@log: serialize $'date-time' as ISODateTime
}
```

```js
provider ( )

/* Provide on Command example
 *  this simply forces an immediate execution of the `provider` when command `'force run'` is received
 */
routine 'force run' on root .'force run' schedule
```

```js
/* Provider Initialization
 *  this ensures that the connector always runs with a dataset
 *  it uses a custom routine to generate the initial dataset
 */
provider ( )
init ( )
```

```js
/* Provider Initialization
 *  this ensures that the connector always runs with a dataset
 *  the dataset is provided by the main routine
 */
provider ( )
init main
```
# Processor
## The internal library.
Allows defining reusable types.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library</span>': dictionary { [ <span class="token operator">define</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
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
			 * Optionally the `@API` option can be used to suppress usages analysis.
			 */
			'<span class="token string">analysis</span>': stategroup (
				'<span class="token string">API</span>' { [ <span class="token operator">@API</span> ] }
				'<span class="token string">full</span>' { }
			)
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
			/* The path to the command the routine is bound to.
			 * The path becomes the initial scope of the routine.
			 */
			'<span class="token string">binding</span>': [ <span class="token operator">on</span> <span class="token operator">root</span> ] component <a href="#grammar-rule--interface-named-path">'interface named path'</a>
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
		 * The statement is restricted, see '<span class="token string">statement</span>' for details.
		 */
		'<span class="token string">context keys</span>': component <a href="#grammar-rule--statement">'statement'</a>
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
		 */
		/* A standard library can expose hooks.
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
consumer ( )

/* error-handler example
 *  this logs the error report
 */
on error do @log: $
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
		'<span class="token string">statement</span>': [ <span class="token operator">on</span> <span class="token operator">error</span> <span class="token operator">do</span> ] component <a href="#grammar-rule--statement">'statement'</a>
	}
	'<span class="token string">no</span>' { }
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
consumer ( )

/* Standard Library `network.lib`::`webserver` example
 *  this registers a webserver hook for the `/echo` path
 *  the original request is returned as JSON
 */
add-hook 'network'::'webserver' "/echo"
do (
	'status' = 200
	'headers' = create [ "content-type" ] "application/json"
	'content' = call 'unicode'::'as binary' ( serialize $'request' as JSON )
)
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
	'<span class="token string">implementation</span>': [ <span class="token operator">do</span> ] component <a href="#grammar-rule--statement">'statement'</a>
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
		'<span class="token string">number</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
					/* An integer can hold numbers.
					 * Integers can not have a fraction.
					 */
				}
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
				}
			)
			'<span class="token string">limits</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">@limit:</span> <span class="token operator">{</span>, <span class="token operator">}</span> ]
					/* Limit the value range.
					 * All limits are inclusive.
					 */
					'<span class="token string">lower</span>': stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the minimum value.
							 * The value is evaluated before the decimal import rule.
							 */
							'<span class="token string">value</span>': integer
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">upper</span>': [ <span class="token operator">,</span> ] stategroup (
						'<span class="token string">yes</span>' {
							/* Limit the maximum value.
							 * The value is evaluated before the decimal import rule.
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
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ]
			/* A text can hold Unicode data.
			 */
			'<span class="token string">limits</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">@limit:</span> <span class="token operator">{</span>, <span class="token operator">}</span> ]
					/* Limit the text length.
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
					'<span class="token string">value</span>': [ <span class="token operator">is</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
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
				 * The result of the expression is assigned to the name.
				 * The type of this `let` is inferred from the expression.
				 */
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
			}
			'<span class="token string">schema</span>' {
				/* Target driven `let`.
				 * The type of this `let` is the type of the schema.
				 * This executes the statement with the schema as target.
				 */
				'<span class="token string">schema</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--schema-complex-type">'schema complex type'</a>
				'<span class="token string">statement</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--statement">'statement'</a>
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
			'<span class="token string">index</span>': stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">[integer]</span> ] }
				'<span class="token string">text</span>' { [ <span class="token operator">[text]</span> ] }
				'<span class="token string">inferred</span>' { }
			)
			'<span class="token string">sub type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
		'<span class="token string">function</span>' {
			'<span class="token string">signature</span>': [ <span class="token operator">function</span> ] component <a href="#grammar-rule--signature">'signature'</a>
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

{: #grammar-rule--signature }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">signature</span>' {
	/* The signature of a callable object.
	 */
	'<span class="token string">template</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator"><</span>, <span class="token operator">T</span> <span class="token operator">></span> ]
			/* Add a template type to the signature.
			 * An optional constraint can be added to the type.
			 */
			'<span class="token string">requirement</span>': stategroup (
				'<span class="token string">plural</span>' { [ <span class="token operator">plural</span> ] }
				'<span class="token string">optional</span>' { [ <span class="token operator">optional</span> ] }
				'<span class="token string">node</span>' { [ <span class="token operator">node</span> ] }
				'<span class="token string">none</span>' { }
			)
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">input</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
		/* The type of the input.
		 * When written inline, the input type can be inferred (implicit).
		 */
		'<span class="token string">context</span>': stategroup (
			'<span class="token string">explicit</span>' {
				'<span class="token string">type</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
			}
			'<span class="token string">implicit</span>' { }
			'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
		)
		/* Parameter definition of a callable object.
		 */
		'<span class="token string">parameters</span>': dictionary { [ <span class="token operator">$</span> ]
			'<span class="token string">has next</span>': stategroup = node-switch successor (
				| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
				| none = '<span class="token string">no</span>'
			)
			'<span class="token string">type</span>': [ <span class="token operator">:</span> ] component <a href="#grammar-rule--type-definition">'type definition'</a>
		}
	}
	/* The expression guarantee of the callable object.
	 */
	'<span class="token string">guarantee</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">yes</span>' { }
		'<span class="token string">no</span>' { [ <span class="token operator">unsafe</span> ] }
	)
	/* The type of the output.
	 */
	'<span class="token string">style</span>': stategroup (
		'<span class="token string">target</span>' {
			/* The target the callable object must be called on.
			 * When written inline, the target can be inferred.
			 */
			'<span class="token string">target</span>': stategroup (
				'<span class="token string">explicit</span>' {
					'<span class="token string">path</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--target-type-path">'target type path'</a>
				}
				'<span class="token string">inferred</span>' { }
			)
		}
		'<span class="token string">value</span>' {
			'<span class="token string">result</span>': component <a href="#grammar-rule--type-definition">'type definition'</a>
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

{: #grammar-rule--function-argument }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">function argument</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">optional</span>' {
			/* Set an optional parameter.
			 * Function arguments must always explicitly set or unset.
			 */
			'<span class="token string">action</span>': stategroup (
				'<span class="token string">set</span>' { [ <span class="token operator">set</span> ]
					'<span class="token string">argument</span>': component <a href="#grammar-rule--function-argument">'function argument'</a>
				}
				'<span class="token string">unset</span>' { [ <span class="token operator">unset</span> ] }
			)
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
			'<span class="token string">value</span>': component <a href="#grammar-rule--safe-expression">'safe expression'</a>
		}
	)
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
	 * This creates a new scoped bound to the signature parameters.
	 * The created scope will be the initial scope of the callable object when called.
	 */
	'<span class="token string">with context</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">values</span>': dictionary { [ <span class="token operator">$</span> ]
		'<span class="token string">argument</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--function-argument">'function argument'</a>
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
			'<span class="token string">value</span>': component <a href="#grammar-rule--safe-expression">'safe expression'</a>
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
				'<span class="token string">lazy</span>' { }
				'<span class="token string">greedy</span>' { [ <span class="token operator">*</span> ] }
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
## Promise
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

{: #grammar-rule--expression }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">expression</span>' {
	'<span class="token string">operation</span>': stategroup (
		/* fetch from key-value pair systems */
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
		'<span class="token string">entry key</span>' { [ <span class="token operator">key</span> ]
			/* Retrieve the key of the current entry.
			 * This is only valid inside a `walk` statement.
			 */
		}
		/* type conversions */
		'<span class="token string">parse</span>' { [ <span class="token operator">parse</span> ]
			'<span class="token string">value</span>': component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">as</span>': [ <span class="token operator">as</span> ] stategroup (
				'<span class="token string">JSON</span>' { [ <span class="token operator">JSON</span> ]
					/* Parses JSON.
					 * On success it results in a document and must first be passed to a decorator before it is usable.
					 */
				}
				'<span class="token string">XML</span>' { [ <span class="token operator">XML</span> ]
					/* Parses a XML document.
					 * On success it results in a document and must first be passed to a decorator before it is usable.
					 */
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
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
					'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
				}
			)
		}
		'<span class="token string">decorate</span>' { [ <span class="token operator">decorate</span> ]
			'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">type</span>': [ <span class="token operator">as</span> ] stategroup (
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
		/* compute new values */
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
					 * When the resulting fraction, if any, is truncated.
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
			'<span class="token string">on</span>': stategroup (
				'<span class="token string">value</span>' {
					'<span class="token string">key</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--expression-tail">'expression tail'</a>
				}
				'<span class="token string">key</span>' { [ <span class="token operator">key</span> ] }
			)
		}
		'<span class="token string">file constructor</span>' { [ <span class="token operator">file</span> <span class="token operator">(</span>, <span class="token operator">)</span> ]
			/* Construct a file object.
			 */
			'<span class="token string">token</span>': [ <span class="token operator">token</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--expression">'expression'</a>
			'<span class="token string">extension</span>': [ <span class="token operator">extension</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--expression">'expression'</a>
		}
		'<span class="token string">call</span>' {
			/* Call a standard library function or function. */
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
									'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
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
							'<span class="token string">value</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] component <a href="#grammar-rule--safe-expression">'safe expression'</a>
						}
						'<span class="token string">no</span>' { }
					)
					'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">state</span>' { [ <span class="token operator">create</span> ]
					/* Set an Alan Interface `stategroup` or `union` to the specified state/type.
					 */
					'<span class="token string">state</span>': reference
					'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">scalar</span>' {
					/* Assign a scalar the produced value.
					 */
					'<span class="token string">value</span>': component <a href="#grammar-rule--safe-expression">'safe expression'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>
## Statement
A statement is responsible for the control flow of the processor.
Statements operate on a target, the target specifies the cardinality of the statement.
A cardinality of singular means that the target can only hold a single value, as a result statements which can produce zero or multiple values are not allowed.
A cardinality of plural means that the target can hold any number of values.

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
					'<span class="token string">on error</span>': [ <span class="token operator">|</span> <span class="token operator">error</span> <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">choice</span>' {
					/* Execute a conditional branch.
					 * The branch is determined based on a user defined choice.
					 * When the choice is an Alan Interface `stategroup`, the state node is optionally available in `$`.
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
		}
		'<span class="token string">call</span>' {
			/* Call a standard library function or function. */
			'<span class="token string">selection</span>': [ <span class="token operator">call</span> <span class="token operator">on</span> <span class="token operator">target</span> ] component <a href="#grammar-rule--callable-selector">'callable selector'</a>
			'<span class="token string">arguments</span>': component <a href="#grammar-rule--function-call">'function call'</a>
		}
		'<span class="token string">log operation</span>' { [ <span class="token operator">@log:</span> ]
			/* Write a message to the debug channel.
			 */
			'<span class="token string">message</span>': component <a href="#grammar-rule--safe-expression">'safe expression'</a>
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
</pre>
</div>
</div>
