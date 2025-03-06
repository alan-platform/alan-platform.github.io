---
layout: "doc"
origin: "connector"
language: "processor"
version: "36.7-dev2"
type: "grammar"
---

1. TOC
{:toc}

# Release Notes

## 36.6
#### Template Engine
Added a template engine.

[example](./tests/unicode-template/processor.alan)

[example](./tests/unicode-template2/processor.alan)

[example](./tests/unicode-template3/processor.alan)

[example](./tests/unicode-template4/processor.alan)


## 36.5
#### User functions
Added user functions.

[example](./tests/user-function/processor.alan)

#### Unicode Escape
Added an escape function with a custom dictionary.

[example](./tests/unicode-escape/processor.alan)


## 36.4
#### Added related items to network messages
Added the `body related` property to `network message`.
This is currently only used by the serializer.


## 36.3
#### Added greedy pattern matching
Added greedy pattern matching option to integer and decimal patterns.

#### Base64 encoder
Added a base64 encoder function to the `data` library

[example](./tests/base64-encode/processor.alan).

#### Base64 decode
Added a base64 decode function to the `data` library.

[example](./tests/base64-decode/processor.alan).

#### Network message serializer
Added a function to serialize a `network message` to MIME text.


## 36.1
#### Decimal format and locales
Locales or no longer optional for decimal formats.

#### Integer format
A new integer format is added.
Integers are a sequence of base-10 digits with an optional minus prefix for negative numbers.

#### Network authentication
Authentication format in the standard library `network` is changes to support OAuth2 Bearer tokens.

#### Partition on `key`
Support for `key` in `partition` operation.

[example](./tests/partition-key/processor.alan)

#### Changed calendar data layout
Changed the data types of the calendar library to fix inconsistencies between `convert` and `construct`.

[example](./tests/format-datetime/processor.alan)

#### Added new IMAP function
Added a new IMAP function `imap list` to the standard library `network`.
This function passes the unparsed message as a `binary` to a user callback.

[example](./examples/stdlib.network.imap.list/processor.alan)

#### Added greedy pattern matching
Added the option to switch between lazy and greedy text patterns.
The default remains lazy matching.

[example: lazy](./tests/parse-pattern/processor.alan)

[example: greedy](./tests/parse-pattern2/processor.alan)

#### Strict XML serializer
The XML serializer no longer performs any implicit type conversions.
All conversions must be done explicitly.

[example](./tests/serializer-schema-xml/processor.alan)

#### Hacks
The connector supports a dynamic set of hacks.
These can be set/unset through the runtime configuration.

#### Deprecated make date/time
The `make date`, `make date-time` and `make time` operations are deprecated.
These are replaced with the standard library function `'calendar'::'construct'`.

#### Archive support
Added support for loading archives.
# The Standard Libraries
The connector provides a set of standard libraries.
These libraries provide functionality outside the language constructs of the connector.
## Calendar
The calendar library provides conversions between the connectors internal date time representation and broken down time.

```js
define 'type' as @API choice ( 'date' 'date-time' 'time' )

define 'calendar' as @API {
	'year': integer
	'month': integer @limit: { 1 , 12 }
	'day': integer @limit: { 1 , 31 }
}

define 'weekday' as @API choice (
	'Monday':    1
	'Tuesday':   2
	'Wednesday': 3
	'Thursday':  4
	'Friday':    5
	'Saturday':  6
	'Sunday':    7
)
define 'week' as @API {
	'year': integer
	'week': integer @limit: { 1 , 53 }
	'day': 'weekday'
}

define 'ordinal' as @API {
	'year': integer
	'day': integer @limit: { 1 , 366 }
}

define 'time' as @API {
	'hour': integer @limit: { 0 , 23 }
	'minute': integer @limit: { 0 , 59 }
	'second': integer @limit: { 0 , 59 }
}

define 'date time' as @API {
	'calendar': 'calendar'
	'week': 'week'
	'ordinal': 'ordinal'
	'time': 'time'
}

define 'constructor' as @API {
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
define 'convert' as function
	< integer , 'date time' >
	(
		$'source type': 'type'
		$'timezone': optional text
	)
	binds: "d306bc04dd8d1409c53f6f882799eb3624b09ac0"

/* Construct Alan Time from broken down time.
 * The result is either a date-time or a date, depending on whether or not 'time' is set.
 * When timezone is not set, it will be evaluated in Etc/UTC.
 */
define 'construct' as function
	< 'constructor', integer >
	(
		$'timezone': optional text
	)
	binds: "596421faebb0db07f3b4f56c5af963b79f0c3012"

library
```
### Calendar Examples

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
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
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = set "Europe/Amsterdam" )

	switch $'value' => is ( 212479060830 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
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
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = set "Europe/Amsterdam" )

	switch $'value' => is ( 212494782030 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```
## Network
The network library provides functions to perform network request and the data structures to represent related objects.

```js
define 'network method' as @API choice ( 'get' 'head' 'post' 'put' 'delete' )
define 'network security' as @API choice ( 'strict' 'preferred' 'none' )
define 'key value list' as @API collection case folding text

define 'network request' as @API {
	'method': 'network method'
	'parameters': optional 'key value list'
	'headers': optional 'key value list'
	'content': optional binary
}
define 'network response' as @API {
	'status': integer
	'headers': 'key value list'
	'content': binary
}

define 'network authentication' as @API {
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

define 'network message part' as @API {
	'mime type': text
	'mime sub type': text
	'content': binary
}
define 'network message part list' as @API list {
	'name': text
	'part': 'network message part'
}
define 'network message' as @API {
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
define 'parse network message' as function
	< binary , unsafe 'network message' >
	(
		$'preferred mime subtype': text
	)
	binds: "04367c552ffced06d553544dd5c2f0cf943bcf83"

/* Serializes a 'network message' to text.
 */
define 'serialize network message' as function
	<'network message', unsafe binary >
	(
		$'include hidden recipients': boolean
	)
	binds: "3897fab883e2f266c73367826f4ee37e5e5ab53e"

/* Performs an HTTP(S) request.
 * Methods are mapped directly to their HTTP equivalent.
 * When provided, 'content' is send with the request.
 */
define 'http' as function
	< boolean , unsafe 'network response' >
	(
		$'server': text
		$'path': text
		$'authentication': optional 'network authentication'
		$'request': 'network request'
	)
	binds: "63c1fb9ebbc1814b5412bced4f7dc4cf5b5cdda5"

/* Performs an FTP(S) request.
 * Method mapping:
 *  > 'get': Retrieves the content of 'path'. For this to work on directories, 'path' must end with a slash (/).
 *  > 'head': Retrieves the directory entries at 'path' without meta data. 'path' must be a directory, but does not need to end with a slash (/).
 *  > 'post': Stores 'content' in 'path'.
 *  > 'put': Identical to 'post'.
 *  > 'delete': Attempts to remove 'path'. Unlike other methods, this transmits 'path' directly to the server for interpretation.
 * Only when storing data, should content be set.
 */
define 'ftp' as function
	< boolean , unsafe optional binary >
	(
		$'server': text
		$'path': text
		$'method': 'network method'
		$'authentication': optional 'network authentication'
		$'security': 'network security'
		$'content': optional binary
	)
	binds: "508e0611fb1b359247f185b099fee1bbc085aa07"

/* Retrieves all messages matching 'criteria' with IMAP(S).
 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
 * All messages are parsed as if passed to `function 'parse network message'`.
 */
define 'imap' as function
	< boolean , unsafe list 'network message' >
	(
		$'server': text
		$'path': text
		$'criteria': text
		$'authentication': optional 'network authentication'
		$'security': 'network security'
		$'preferred mime subtype': text
	)
	binds: "c2abe22b1ffd86fb2572e27aeb55f6523cad0d30"

/* Retrieves all messages matching 'criteria' with IMAP(S).
 * See RFC-3501 section 6.4.4 for valid values of 'criteria'.
 */
define 'imap list' as function
	< boolean , unsafe list boolean >
	(
		$'server': text
		$'path': text
		$'criteria': text
		$'authentication': optional 'network authentication'
		$'security': 'network security'
		$'callback': lambda on boolean (
			$'blob': binary
		)
	)
	binds: "d9bbba030f267e927db8832ff3036cb2b7b7965b"

/* Send a message with SMTP(S).
 * The message is serialized as if passed to `function 'serialize network message'`.
 * When the transfer fails, this function throws an error.
 */
define 'smtp' as function
	< boolean , unsafe boolean >
	(
		$'server': text
		$'authentication': optional 'network authentication'
		$'security': 'network security'
		$'message': 'network message'
	)
	binds: "b0a76866da2d55eb03e332988519f788178c8f62"

library
	/* Register webserver handlers.
	 * The handler is used as the path to respond to.
	 * Each handler is triggered by external web requests for the path.
	 */
	hook 'webserver'
		on 'network response'
		(
			$'request': 'network request'
		)
		binds: "28d5a0a8bec41be6e4235c0b32ed0bafa13b7c34"
```
### Network Examples

```js
consumer ( )

/* Standard Library `network.lib`::`http` example
 *  this performs a simple HTTPS GET request and validates the response status
 *  when the request fails, the `throw` contains additional information about the cause
 */
routine 'test' on
do {
	let $'response' = true => call 'network'::'http' with (
		$'server' = "https://example.com"
		$'path' = "/path/to/resource"
		$'authentication' = unset
		$'request' = new (
			'method' = option 'get'
			'parameters' = create ["parameter"] "value"
		)
	) || throw "http request failed"

	switch $'response'.'status' => less-than ( 400 ) (
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
routine 'test' on
do {
	let $'response' = true => call 'network'::'http' with (
		$'server' = "https://example.com"
		$'path' = "/path/to/resource"
		$'authentication' = unset
		$'request' = new (
			'method' = option 'put'
			'headers' = create ["content-type"] "text/plain"
			'content' = "hello world" => call 'unicode'::'as binary' with ( )
		)
	) || throw "http request failed"

	switch $'response'.'status' => less-than ( 400 ) (
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
routine 'test' on
do {
	let $'response' = true => call 'network'::'http' with (
		$'server' = "https://example.com"
		$'path' = "/path/to/resource"
		$'authentication' = set new (
			'type' = create 'user' (
				'username' = "username"
				'password' = "password"
			)
		)
		$'request' = new (
			'method' = option 'get'
		)
	) || throw "http request failed"

	switch $'response'.'status' => less-than ( 400 ) (
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
routine 'test' on
do {
	let $'resource' = true => call 'network'::'ftp' with (
		$'server' = "ftps://example.com"
		$'path' = "/path/to/resource"
		$'method' = option 'get'
		$'authentication' = unset
		$'security' = option 'strict'
		$'content' = unset
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
routine 'test' on
do {
	let $'resource' = true => call 'network'::'ftp' with (
		$'server' = "ftps://example.com"
		$'path' = "/path/to/resource"
		$'method' = option 'head'
		$'authentication' = unset
		$'security' = option 'strict'
		$'content' = unset
	) || throw "ftp request failed"
	let $'file list' = $'resource' get => call 'unicode'::'import' with ( $'encoding' = "ASCII" ) => call 'unicode'::'split' with ( $'style' = option 'none' ) || throw "ftp response parse error"

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
routine 'test' on
do {
	let $'resource' = true => call 'network'::'ftp' with (
		$'server' = "ftps://example.com"
		$'path' = "/path/to/resource"
		$'method' = option 'put'
		$'authentication' = unset
		$'security' = option 'strict'
		$'content' = set "hello world" => call 'unicode'::'as binary' with ( )
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
routine 'test' on
do {
	let $'resource' = true => call 'network'::'ftp' with (
		$'server' = "ftps://example.com"
		$'path' = "/path/to/resource"
		$'method' = option 'delete'
		$'authentication' = unset
		$'security' = option 'strict'
		$'content' = unset
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
routine 'test' on
do {
	let $'resource' = true => call 'network'::'ftp' with (
		$'server' = "ftps://example.com"
		$'path' = "/path/to/resource"
		$'method' = option 'get'
		$'authentication' = unset
		$'security' = option 'preferred' /*or 'none' to completely disable security*/
		$'content' = unset
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
routine 'test' on
do {
	let $'messages' = true => call 'network'::'imap' with (
		$'server' = "imaps://example.com"
		$'path' = "/INBOX/"
		$'criteria' = "NEW"
		$'authentication' = unset
		$'security' = option 'strict'
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
routine 'test' on
do {
	let $'results' = true => call 'network'::'imap list' with (
		$'server' = "imaps://example.com"
		$'path' = "/INBOX/"
		$'criteria' = "NEW"
		$'authentication' = unset
		$'security' = option 'strict'
		$'callback' = lambda => {
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
routine 'test' on
do {
	switch true => call 'network'::'smtp' with (
			$'server' = "smtps://example.com"
			$'authentication' = unset
			$'security' = option 'strict'
			$'message' = new (
				'from' = create ["Me"] "me@example.com"
				'recipients' = create ["You"] "you@example.com"
				'subject' = "example message"
				'attachments' = create (
					'name' = "hello.txt"
					'part' = (
						'mime type' = "text"
						'mime sub type' = "plain"
						'content' = "hello world" => call 'unicode'::'as binary' with ( )
					)
				)
				'body' = (
					'mime type' = "text"
					'mime sub type' = "plain"
					'content' = "hello world" => call 'unicode'::'as binary' with ( )
				)
			)
		)
	(
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
	'headers' = create ["content-type"] "application/json"
	'content' = $'request' => serialize as JSON => call 'unicode'::'as binary' with ( )
)
```
## Plural
The plural library provides algorithms operating on sets.

```js
/* Sorts a set based on a comparison function.
 */
define 'sort' as function
	< template plural T , plural T , plural T >
	(
		$'compare': lambda on boolean (
			$'A': T
			$'B': T
		)
	)
	binds: "4e4bc51b80a665baa10535df3b639195c40110d5"

/* Selects a single entry in a set based on a comparison function.
 * This returns the entry for which `compare` results in true when the entry is `A` and false when `B` compared to all other entries in the set.
 * It fails when no such entry is found.
 */
define 'select' as function
	< template plural T , plural T , unsafe T >
	(
		$'compare': lambda on boolean (
			$'A': T
			$'B': T
		)
	)
	binds: "b3bde4040897909027018b18d5bc4ad920bd7965"

/* Filters a set.
 * This returns a new set containing only the entries for which `filter` results in true.
 */
define 'filter' as function
	< template plural T , plural T , plural T >
	(
		$'filter': lambda on boolean (
			$'entry': T
		)
	)
	binds: "d68776aedb6ca2bf0af5f3cc361a5f6dc88cffee"

/* Divide a set in several smaller sets (buckets).
 * The order of the entries is maintained.
 */
define 'split' as function
	< template plural T , plural T , plural [integer] plural T >
	(
		$'bucket size': integer
	)
	binds: "707ffe346ab9e2237c8975cd4735191cabfd47aa"

library
```
### Plural Examples

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list boolean = {
		create true
		create false
		create true
	}
	let $'value' = $'data' => call 'plural'::'filter' with (
		$'filter' = lambda => $'entry'
	)

	switch $'value'.size => is ( 2 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
		create 5
		create 2
		create 5
	}
	let $'magic' = 5
	let $'value' = $'data' => call 'plural'::'filter' with (
		$'filter' = lambda => $'entry' => is ( ^ $'magic' )
	)

	switch $'value'.size => is ( 2 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'object' = ^ $'Context'.'objects' => call 'plural'::'select' with (
		$'compare' = lambda => $'A'.'value' => greater-than ( $'B'.'value' )
	) || throw "no unique object to select"

	switch $'object'.'key' => is ( "two" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'object' = ^ $'Context'.'objects' => call 'plural'::'select' with (
		$'compare' = lambda => $'A'.'value' => greater-than ( $'B'.'value' )
	) || throw "no unique object to select"

	switch $'object'.'key' => is ( "two" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do try {
	let $'object' = ^ $'Context'.'objects' => call 'plural'::'select' with (
		$'compare' = lambda => $'A'.'has value'?'yes'.'value' => greater-than ( $'B'.'has value'?'yes'.'value' ) || throw "comparison data missing"
	) || throw "no selection"

	throw "object selected"
}
catch as $ => switch $ => is ( "comparison data missing" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
		create 16
		create 42
		create 39
	}
	let $'value' = $'data' => call 'plural'::'sort' with (
		$'compare' = lambda => $'A' => less-than ( $'B' )
	)

	switch $'value' => join separator: ( "," ) ( => serialize as decimal locale: "en_US" ) => is ( "16,39,42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
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
	let $'result' as list {
		'bucket': list integer
	} = walk $'data' => call 'plural'::'split' with ( $'bucket size' = 2 ) as $ => create (
		'bucket' = walk $ as $ => create $
	)

	switch $'result' => serialize as JSON => is ( "[{\"bucket\":[16,42]},{\"bucket\":[39,17]},{\"bucket\":[43,38]},{\"bucket\":[18,44]},{\"bucket\":[37]}]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```
## Unicode
The unicode library provides functions to manipulate text values.

```js
define 'trim style' as @API choice ( 'leading' 'trailing' 'both' 'none' )
define 'alignment' as @API choice ( 'left' 'right' )

define 'message data' as @API {
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
define 'import' as function
	< binary , unsafe text >
	(
		$'encoding': text
	)
	binds: "5eda0a0995ac59d7760ecfa8fc914ff6be5510f0"

/* Exports text to binary data.
 * Text is converted to the specified encoding from the internal encoding.
 * When the specified encoding is not known, or no know conversion from the internal encoding is known, the function fails.
 */
define 'export' as function
	< text , unsafe binary >
	(
		$'encoding': text
	)
	binds: "95c1f25e3ed8a0ef1cc5f3dbf9a63d825c4fca04"

/* Returns a text value as binary data.
 * The data is encoded in the internal encoding.
 */
define 'as binary' as function
	< text , binary >
	( )
	binds: "87c97c8e13179e8011a433263adba108b053ac5e"

/* Replaces all occurrences of the key of the entries in the dictionary with their value.
 */
define 'escape' as function
	< text , text >
	(
		$'dictionary': collection text
	)
	binds: "56446bd60eff700fd39b2e60d6622984d671a73a"

/* Removes all whitespace from a text value.
 */
define 'strip' as function
	< text , text >
	( )
	binds: "a255c15caaf00b4ef5284e5616c0ea5384cae258"

/* Removes leading and/or trailing whitespace from a text value.
 */
define 'trim' as function
	< text , text >
	(
		$'style': 'trim style'
	)
	binds: "210540a08d6c7f2f7dc7b0f11d87ca0fb57f6bb2"

/* Split a text into multiple fragments.
 * Empty fragments are automatically removed.
 */
define 'split' as function
	< text , list text >
	(
		$'style': 'trim style'
	)
	binds: "f516f2ea99343dd9d1035d588484ba06fd57d580"

/* Adds whitespace to a text value.
 */
define 'pad' as function
	< text , text >
	(
		$'align': 'alignment'
		$'length': integer
	)
	binds: "1085bfb07ec00ef9b01984e3605f257d0dadbd1c"

/* Match a text with a Regular Expression.
 * The whole input must match the pattern.
 */
define 'regex' as function
	< text , unsafe boolean >
	(
		$'pattern': text
	)
	binds: "24ea697a55dedbc6a58b8ca00d80d5cd1bde4a2b"

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
define 'format' as function
	< text , unsafe text >
	(
		$'data': 'message data'
		$'locale': text
	)
	binds: "00e5893ff46bce3d3278091734b1ca786f41fe83"

/* Result of the template function.
 */
define 'template result' as @API {
	'success': boolean /* Value indicating whether the template was transformed correctly or not. */
	'result': text     /* On success contains the transformed template, on failure contains the error message. */
	'schema': text     /* The schema inferred from the input data. */
}
/* Format a template with dynamic data.
 */
define 'template' as function
	< template node T , T , unsafe 'template result' >
	(
		$'template': text
		$'locale': text
	)
	binds: "033fe1fa04c997458ec88006acffeb044d339582"

library
```
### Unicode Examples

```js
consumer ( )

routine 'test' on
do switch "ç" => is ( "ç" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do switch "Ç" => is case folding ( "ç" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for format function */
	let $'vectors' = list (
		file ( token = "{nr,spellout}" extension = "vier­duizend­twee­honderd" ) ,
		file ( token = "{nr,number,currency}" extension = "€ 4.200,00" ) ,
		file ( token = "{nr,number}" extension = "4.200" ) ,
		file ( token = "{nr}" extension = "4.200" ) ,
		file ( token = "{tx}" extension = "hello" ) ,
		file ( token = "{dt,date}" extension = "3 feb. 2021" )
	)
	let $'data' as 'unicode'/'message data' = (
		'types' = {
			create ["dt"] create 'calendar' 212479064430
			create ["nr"] create 'number' 4200
			create ["tx"] create 'text' "hello"
		}
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'pattern' = $
		let $'message' = $'pattern'.token => call 'unicode'::'format' with (
			$'data' = ^ $'data'
			$'locale' = "nl_NL"
		) || throw "error"

		switch $'message' => is ( $'pattern'.extension ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for trim function */
	let $'vectors' as list {
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
		let $'test' = $ .'input' => call 'unicode'::'pad' with (
			$'align' = $ .'align'
			$'length' = $ .'length'
		)

		switch $'test' => is ( $ .'result' ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'match' = "abcde" => call 'unicode'::'regex' with ( $'pattern' = "[a-z]+" ) || throw "invalid pattern"

	switch $'match' (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'match' = "abCde" => call 'unicode'::'regex' with ( $'pattern' = "[a-z]+" ) || throw "invalid pattern"

	switch $'match' (
		| true => throw "produced wrong value"
		| false => no-op // Test successful
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'match' = "abcde" => call 'unicode'::'regex' with ( $'pattern' = "[a-z+" ) || throw "invalid pattern"

	throw "valid pattern"
	/* suppress unused warnings */
	switch $'match' (
		| true => no-op
		| false => no-op
	)
}
catch as $ => switch $ => is ( "invalid pattern" ) (
	| true => no-op // Vector tested successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'lines' = {
		let $'lines' = "line-0
line-1

line-2" => call 'unicode'::'split' with ( $'style' = option 'both' )

		walk $'lines' as $ => create (
			'line' = $
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for trim function */
	let $'vectors' = list (
		"line",     // nothing to trim
		"   line",  // leading spaces
		"line   ",  // trailing spaces
		" l i n e ",  // internal spaces
		"　l　i　n　e　"  // no-ASCII space
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'line' = $
		let $'trim' = $'line' => call 'unicode'::'strip' with ( )

		switch $'trim' => is ( "line" ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for trim function */
	let $'vectors' = list (
		"line",     // nothing to trim
		"   line",  // leading spaces
		"line   ",  // trailing spaces
		"	line",  // tabs
		"　line"    // no-ASCII space
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'line' = $
		let $'trim' = $'line' => call 'unicode'::'trim' with ( $'style' = option 'both' )

		switch $'trim' => is ( "line" ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```
## Data
The data library provides functions to manipulate binary values.

```js
define 'base64 alphabet' as @API choice ( 'base64' 'base64url' )

/* Converts text from one encoding to another.
 * Available encodings depend on the hosting systems.
 */
define 'convert' as function
	< binary , unsafe binary >
	(
		$'from': text
		$'to': text
	)
	binds: "10fb20740f273873cd35121d33fd980e9c68f242"

/* Convert binary data to base64 text.
 * Alphabet as defined by RFC-4648.
 */
define 'base64 encode' as function
	< binary , text >
	(
		$'alphabet': 'base64 alphabet'
	)
	binds: "b9bfaa1b0da22d82ef967d8f4cc501d102367703"

/* Convert base64 text to binary data.
 * Alphabet as defined by RFC-4648.
 */
define 'base64 decode' as function
	< text , unsafe binary >
	(
		$'alphabet': 'base64 alphabet'
	)
	binds: "1a2fd70ec93a50c8cdb576ca0d3955e9967e90ae"

/* Loads an archive from data.
 * Archive format and any compression/encoding are automatically detected.
 */
define 'load archive' as function
	< binary , unsafe collection binary >
	( )
	binds: "b0dcc6d89228fd4a40e45d3b05c413eb88a0c56c"

library
```
# Processor
## The internal library.
Allows defining reusable types.

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
				'<span class="token string">statement</span>' {
					'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">binding</span>' {
					/* The function is part of a standard library.
					 * These functions are implemented by the connector runtime.
					 */
					'<span class="token string">binds</span>': [ <span class="token operator">binds:</span> ] text
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
			'<span class="token string">binding</span>': [ <span class="token operator">on</span> ] stategroup (
				'<span class="token string">event</span>' {
					/* The routine binds to an event.
					 * When the event is received, the routine is run.
					 * The event data is available in `$`.
					 */
					'<span class="token string">event</span>': [ <span class="token operator">event</span> ] reference
				}
				'<span class="token string">collection</span>' {
					/* The routine binds to an collection.
					 * When any entries in the collection are touched by an update, the routine is run.
					 * The set of touched entries (and only the touched entries) are available in `$`.
					 * The routine is only run after the update is fully processed.
					 * As a result, the routine always has a fully initialized dataset available, but is not informed which data was updated.
					 */
					'<span class="token string">property</span>': [ <span class="token operator">collection</span> ] reference
				}
				'<span class="token string">entry deletion</span>' {
					/* The routine binds to a collection.
					 * When an entry in the collection is deleted, the routine is run.
					 * The key of the delete entry is available in `$`.
					 * The routine is only run after the update is fully processed.
					 * As a result, the routine always has a fully initialized dataset available, but is not informed which data was updated.
					 */
					'<span class="token string">property</span>': [ <span class="token operator">collection</span>, <span class="token operator">deletion</span> ] reference
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
		 */
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
Providers and consumers can add lambdas to these hooks.
These lambdas are executed when the hook is triggered.
Some hooks only trigger a subset of the added lambdas, based on the handler name.

Lambdas added to hooks can execute side-effects based on there context.
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
	'headers' = create ["content-type"] "application/json"
	'content' = $'request' => serialize as JSON => call 'unicode'::'as binary' with ( )
)
```


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
## Interface Named Path
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
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ]
			/* An integer can hold numbers.
			 * Integers can not have a fraction.
			 */
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
			'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
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
				 * The type of this `let` is the type of the schema.
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
				'<span class="token string">node</span>' { [ <span class="token operator">node</span> ] }
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
	/* The promise guarantee of the callable object.
	 */
	'<span class="token string">guarantee</span>': stategroup (
		'<span class="token string">yes</span>' { }
		'<span class="token string">no</span>' { [ <span class="token operator">unsafe</span> ] }
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
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
				'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
					'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
					'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
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
		'<span class="token string">entry lookup</span>' {
			/* Retrieve the value of an entry in a collection.
			 * This fails when the provided key does not exist in the set.
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
											'<span class="token string">value</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise">'promise'</a>
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
									'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
									'<span class="token string">rule</span>': component <a href="#grammar-rule--decimal-import-rule">'decimal import rule'</a>
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
								'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
								'<span class="token string">decimal</span>' { [ <span class="token operator">decimal</span> ]
									'<span class="token string">locale</span>': [ <span class="token operator">locale:</span> ] text
									'<span class="token string">integer digits</span>': stategroup (
										'<span class="token string">custom</span>' { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
											'<span class="token string">places</span>': component <a href="#grammar-rule--value-promise">'value promise'</a>
										}
										'<span class="token string">default</span>' { }
									)
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
										'<span class="token string">yes</span>' { [ <span class="token operator">separator:</span> ]
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
						'<span class="token string">partition</span>' { [ <span class="token operator">partition</span> ]
							/* Partition a set.
							 * It groups all entries with the `key` together in a bucket.
							 * The result is a set of key-value pairs, where the key is the shared `key` and the value is a set of the entries with that `key`.
							 * The order of buckets is undefined.
							 * The order of entries within a bucket is maintained.
							 */
							'<span class="token string">comparator</span>': [ <span class="token operator">on</span> ] component <a href="#grammar-rule--comparator">'comparator'</a>
							'<span class="token string">on</span>': stategroup (
								'<span class="token string">value</span>' {
									'<span class="token string">key</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--promise-chain">'promise chain'</a>
								}
								'<span class="token string">key</span>' { [ <span class="token operator">key</span> ] }
							)
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

{: #grammar-rule--promise }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">promise</span>' {
	'<span class="token string">head</span>': stategroup (
		/* fetch from key-value pair systems */
		'<span class="token string">variable</span>' {
			/* Retrieves a variable from the instance-data.
			 */
			'<span class="token string">variable</span>': [ <span class="token operator">var</span> ] reference
		}
		'<span class="token string">configuration</span>' {
			/* Retrieves a value from the system configuration.
			 */
			'<span class="token string">key</span>': [ <span class="token operator">conf</span> ] text
			'<span class="token string">data type</span>': stategroup (
				'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
				'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
			)
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
		/* compute new values */
		'<span class="token string">list constructor</span>' { [ <span class="token operator">list</span> ]
			/* Construct a list object.
			 * This allows for the conversion of a static list to a dynamic list.
			 * The order of entries is identical to the promise order.
			 */
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
## Value Promise
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
					'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">state</span>' {
					'<span class="token string">type</span>': stategroup (
						'<span class="token string">branch</span>' { [ <span class="token operator">create</span> ]
							/* Set an Alan Interface `stategroup` or `union` to the specified state/type.
							 */
							'<span class="token string">state</span>': reference
							'<span class="token string">statement</span>': component <a href="#grammar-rule--statement">'statement'</a>
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
			'<span class="token string">value</span>': [ <span class="token operator">switch</span> ] component <a href="#grammar-rule--promise">'promise'</a>
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
					 * The promise without a guarantee of yes is evaluated.
					 * Based on whether or not the promise succeeded or failed, the corresponding case is executed.
					 * When the promise succeeds, the result is available in `$`.
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
					'<span class="token string">value</span>': [, <span class="token operator">as</span> <span class="token operator">$</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
					'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
				'<span class="token string">range</span>' {
					/* Execute a statement for a range of integers.
					 */
					'<span class="token string">range</span>': group { [ <span class="token operator">(</span>, <span class="token operator">)</span> ]
						'<span class="token string">begin</span>': [ <span class="token operator">from</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
						'<span class="token string">end</span>': [ <span class="token operator">until</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
						'<span class="token string">step</span>': [ <span class="token operator">with</span> ] component <a href="#grammar-rule--value-promise">'value promise'</a>
					}
					'<span class="token string">statement</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--statement">'statement'</a>
				}
			)
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
# Examples

```js
consumer ( )

/* now example
 *  this example demonstrates the usages of the now instruction
 */
routine 'test' on
do {
	let $'date-time' = now

	no-op
	/* suppress unused warnings */
	@log: $'date-time' => serialize as ISODateTime
}
```

```js
provider ( )

/* Provide on Command example
 *  this simply forces an immediate execution of the `provider` when command `'force run'` is received
 */
routine 'force run' on command 'force run' schedule
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

```js
consumer ( )

routine 'test' on
do {
	let $'data' as {
		'value': optional text
	} = ( )
	let $'value' = $'data'.'value' get || ""

	switch $'value' => is ( "" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = $ .'choice'?'a'.'value' || "fallback value"

	switch $'value' => is ( "chosen value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = $ .'choice'?'a'.'value' || "fallback value"

	switch $'value' => is ( "fallback value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'message' = list ( "hello", "world" ) => join separator: ( " " ) ( )

	switch $'message' => is ( "hello world" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	switch conf "test" integer => is ( 42 ) || throw "no config value" (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	switch conf "test" text => is ( "hello" ) || throw "no config value" (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	throw "failure"
}
catch => switch $ .'value' => is ( "value 101" ) (
	| true => no-op // Test successful
	| false => throw "wrong context value"
)
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do switch $'Context'.'custom' (
	|'yes' as $ => throw "switch wrong case"
	|'no' => switch $ .'default' => is ( "The default value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
)
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do switch $'Context'.'custom' (
	|'yes' as $ => switch $ .'value' => is ( "A custom value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
	|'no' => throw "switch wrong case"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
		create 42
		create 24
	}

	switch $'data' => sum ( ) => is ( 66 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as integer = 42

	switch $'data' => is ( 42 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as text = "hello world"

	switch $'data' => is ( "hello world" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "hello,world" => parse as CSV || throw "invalid CSV"
	let $'object' = $'document' => decorate as list headless {
		'key': text
	} || throw "partial initialization"

	throw "full initialization"
	/* suppress unused warnings */
	walk $'object' as $ =>
		@log: $ .'key'
}
catch as $ => switch $ => is ( "partial initialization" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "{}" => parse as JSON || throw "invalid JSON"
	let $'object' = $'document' => decorate as {
		'key': text
	} || throw "partial initialization"

	throw "full initialization"
	/* suppress unused warnings */
	@log: $'object'.'key'
}
catch as $ => switch $ => is ( "partial initialization" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "<root></root>" => parse as XML || throw "invalid XML"
	let $'object' = $'document' => decorate as {
		'root': {
			'key': text
		}
	} || throw "partial initialization"

	throw "full initialization"
	/* suppress unused warnings */
	@log: $'object'.'root'.'key'
}
catch as $ => switch $ => is ( "partial initialization" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "<root></root>" => parse as XML || throw "invalid XML"
	let $'object' = $'document' => decorate as {
		'root'<'key': text > : { }
	} || throw "partial initialization"

	throw "full initialization"
	/* suppress unused warnings */
	@log: $'object'.'root'<'key'>
}
catch as $ => switch $ => is ( "partial initialization" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'objects' = try {
		create (
			'key' = "key"
		)
		create (
			'key' = "key"
		)
	}
	catch as $ => switch $ => is ( "collection uniqueness constraint violation" ) (
		| true => no-op // Test successful
		| false => throw "invalid error"
	)
)
```

```js
consumer ( )

routine 'test' on
do execute $ command 'command' with (
	'message' = "Hello world!"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'date-time' = 212479064430 => call 'calendar'::'convert' with (
		$'source type' = option 'date-time'
		$'timezone' = unset
	)
	let $'value' = "{Year,number,::group-off integer-width/0000}-{Month,number,::integer-width/00}-{Day,number,::integer-width/00}T{Hour,number,::integer-width/00}:{Minute,number,::integer-width/00}:{Second,number,::integer-width/00}Z" => call 'unicode'::'format' with (
		$'data' = new (
			'types' = {
				create ["Year"] create 'number' $'date-time'.'calendar'.'year'
				create ["Month"] create 'number' $'date-time'.'calendar'.'month'
				create ["Day"] create 'number' $'date-time'.'calendar'.'day'
				create ["Hour"] create 'number' $'date-time'.'time'.'hour'
				create ["Minute"] create 'number' $'date-time'.'time'.'minute'
				create ["Second"] create 'number' $'date-time'.'time'.'second'
			}
		)
		$'locale' = "C"
	) || throw "format error"

	switch $'value' => is ( "2021-02-03T10:20:30Z" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'object' as integer @limit: { , 4 } = 128

	throw "length valid"
	/* suppress unused warnings */
	@log: $'object' => serialize as integer
}
catch as $ => switch $ => is ( "integer value limit violation" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'object' as integer @limit: { 128 , } = 4

	throw "length valid"
	/* suppress unused warnings */
	@log: $'object' => serialize as integer
}
catch as $ => switch $ => is ( "integer value limit violation" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'document' = "{\"key\":3}" => parse as JSON || throw "invalid JSON"
	let $'object' = $'document' => decorate as {
		'key': integer @limit: { , 40 }
	} || throw "value limit exceeded"

	switch $'object'.'key' => is ( 3 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "{\"key\":40}" => parse as JSON || throw "invalid JSON"
	let $'object' = $'document' => decorate as {
		'key': text @limit: { , 4 }
	} || throw "value limit exceeded"

	throw "value valid"
	/* suppress unused warnings */
	@log: $'object'.'key'
}
catch as $ => switch $ => is ( "value limit exceeded" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on collection 'data'
do switch $ => sum ( .'val' )  => is ( 20 ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on collection 'data' deletion
do switch $ => is ( "delete" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider ( )

routine 'test' on command 'command'
do switch $ .'message' => is ( "Hello world!" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'state' = create 'hello' ( )
)

routine 'test' on command 'command'
	$'Hello' = .'state'?'hello'
do switch $ .'message' => is ( "Hello world!" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider ( )

routine 'test' on command 'command'
	$'Context' =
do execute $'Context' event 'event' with (
	'message' = $ .'message'
)
```

```js
consumer ( )

routine 'test' on event 'event'
do switch $ .'message' => is ( "Hello world!" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'value' = {
		try 0
		catch as $ => switch $ => is ( "interface number bounds violation" ) (
			| true => 1 // Test successful
			| false => throw "produced wrong value"
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do try {
	switch "\"hello world" => parse as CSV (
		| value as $ => throw "parse of garbage resulted in valid CSV"
		| error => throw "invalid CSV"
	)
}
catch as $ => switch $ => is ( "invalid CSV" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	switch "hello,world
tester" => parse as CSV (
		| value as $ => throw "parse of garbage resulted in valid CSV"
		| error => throw "invalid CSV"
	)
}
catch as $ => switch $ => is ( "invalid CSV" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	switch "hello world" => parse as JSON (
		| value as $ => throw "parse of garbage resulted in valid JSON"
		| error => throw "invalid JSON"
	)
}
catch as $ => switch $ => is ( "invalid JSON" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	switch "hello world" => parse as XML (
		| value as $ => throw "parse of garbage resulted in valid XML"
		| error => throw "invalid XML"
	)
}
catch as $ => switch $ => is ( "invalid XML" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'items' = {
		let $'key' = "A"

		call lambda ( ) => create (
			'key' = ^ $'key'
		) with ( )
	}
)
```

```js
provider (
	'branches' = {
		let $'create branch' = lambda ( $'create leafs': lambda on * .'leafs' ( ) ) => {
			let $'key' = "A"

			create (
				'key' = $'key'
				'leafs' = call ^ $'create leafs' with ( )
			)
		}
		let $'key' = ".A"

		call $'create branch' with (
			$'create leafs' = lambda => create (
				'key' = ^ $'key'
			)
		)
	}
)
```

```js
provider (
	'items' = {
		let $'key' = "A"
		let $'create' = lambda ( ) => create (
			'key' = ^ $'key'
		)

		call $'create' with ( )
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'greet' = lambda on interface command 'command' ( ) => (
		'message' = "Hello world!"
	)

	execute $ command 'command' with call $'greet' with ( )
}
```

```js
define 'type' as {
	'items': list {
		'value': text
	}
}

provider (
	'items' = {
		let $'lambda' = lambda (
			$'f': 'type'
		) => walk $'f'.'items' as $ => create (
			'key' = $ .'value'
		)

		call $'lambda' with (
			$'f' = new (
				'items' = {
					create (
						'value' = "a"
					)
					create (
						'value' = "b"
					)
				}
			)
		)
	}
)
```

```js
provider (
	'items' = {
		let $'lambda' = lambda (
			$'f': {
				'items': list {
					'value': text
				}
			}
		) => walk $'f'.'items' as $ => create (
			'key' = $ .'value'
		)

		call $'lambda' with (
			$'f' = new (
				'items' = {
					create (
						'value' = "a"
					)
					create (
						'value' = "b"
					)
				}
			)
		)
	}
)
```

```js
provider (
	'items' = {
		let $'data' as list {
			'value': optional text
		} = {
			create (
				'value' = "a"
			)
			create ( )
		}

		walk $'data' as $ => call lambda ( $'f': optional text ) => switch $'f' get (
			| value as $ => create (
				'key' = $
			)
			| error => no-op
		) with ( $'f' = $ .'value' )
	}
)
```

```js
provider (
	'items' = {
		let $'create' = lambda ( $'f': optional text ) => switch $'f' get (
			| value as $ => create (
				'key' = $
			)
			| error => no-op
		)

		call $'create' with ( $'f' = set "a" )
		call $'create' with ( $'f' = unset )
	}
)
```

```js
provider (
	'items' = {
		let $'create' = lambda ( $'key': lambda on * .'key' ( ) ) => create (
			'key' = call $'key' with ( )
		)

		call $'create' with ( $'key' = lambda => "A" )
	}
)
```

```js
provider (
	'items' = {
		let $'create' = lambda (
			$'key': lambda on * .'key' (
				$'val': text
			)
		) => create (
			'key' = call $'key' with ( $'val' = "A" )
		)

		call $'create' with ( $'key' = lambda => $'val' )
	}
)
```

```js
provider (
	'numbers' = {
		let $'data' as {
			'objects': collection {
				'next': optional text
				'value': integer
			}
			'first': text
		} = (
			'objects' = {
				create ["one"] (
					'next' = "two"
					'value' = 1
				)
				create ["two"] (
					'next' = "three"
					'value' = 2
				)
				create ["three"] (
					'value' = 3
				)
			}
			'first' = "one"
		)

		call lambda ( $'key': text ) => {
			let $'entry' = ^ ^ $'data'.'objects'[ ^ $'key'] || throw "invalid reference"

			create (
				'key' = ^ $'key'
				'value' = $'entry'.'value'
			)
			switch $'entry'.'next' get (
				| value as $ => call self with ( $'key' = $ )
				| error => no-op // Test successful
			)
		} with ( $'key' = $'data'.'first' )
	}
)
```

```js
provider (
	'items' = {
		let $'create' = lambda ( $'key': text ) => create (
			'key' = $'key'
		)

		call $'create' with ( $'key' = "A" )
	}
)
```

```js
define 'dataset' as list {
	'key': text
	'val': text
}

provider {
	let $'data' as 'dataset' = {
		create (
			'key' = "A"
			'val' = "hello"
		)
		create (
			'key' = "B"
			'val' = "bye"
		)
	}
	let $'create' = lambda on .'items' ( $'line': 'dataset'* ) => create (
		'key' = $'line'.'key'
		'val' = $'line'.'val'
	)

	(
		'items' = walk $'data' as $ => call $'create' with ( $'line' = $ )
	)
}
```

```js
define 'option' as choice ( 'hello' 'bye' )

consumer ( )

routine 'test' on
do {
	let $'option' = "bye" => decorate as 'option' || throw "option could not be decorated"

	switch $'option' (
		|'hello' => throw "produced wrong value"
		|'bye' => no-op // Test successful
	)
}
```

```js
define 'option' as choice ( 'hello' 'bye' )

consumer ( )

routine 'test' on
do {
	let $'settings' = "{\"option\": \"bye\"}" => parse as JSON => decorate as {
		'option': 'option'
	} || throw "option could not be decorated"

	switch $'settings'.'option' (
		|'hello' => throw "produced wrong value"
		|'bye' => no-op // Test successful
	)
}
```

```js
define 'option' as choice ( 'hello' 'bye' )

consumer ( )

routine 'test' on
do {
	let $'option' as 'option' = option 'bye'

	switch $'option' (
		|'hello' => throw "produced wrong value"
		|'bye' => no-op // Test successful
	)
}
```

```js
define 'text pattern' as pattern ( 'text': $ text )

consumer ( )

routine 'test' on
do {
	let $'values' = "hello world" => parse as pattern 'text pattern' || throw "invalid format"

	switch $'values'.'text' => is ( "hello world" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	switch not ( 42 => is ( 24 ) ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
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
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = unset )

	switch $'value' => is ( 212479064430 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
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
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = unset )

	switch $'value' => is ( 212494789230 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
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
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = set "Europe/Amsterdam" )

	switch $'value' => is ( 212479060830 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
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
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = set "Europe/Amsterdam" )

	switch $'value' => is ( 212494782030 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
		'date' = create 'week' (
			'year' = 2021
			'week' = 5
			'day' = option 'Wednesday'
		)
		'time' = (
			'hour' = 10
			'minute' = 20
			'second' = 30
		)
	)
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = unset )

	switch $'value' => is ( 212479064430 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as 'calendar'/'constructor' = (
		'date' = create 'week' (
			'year' = 2021
			'week' = 31
			'day' = option 'Wednesday'
		)
		'time' = (
			'hour' = 10
			'minute' = 20
			'second' = 30
		)
	)
	let $'value' = $'source' => call 'calendar'::'construct' with ( $'timezone' = unset )

	switch $'value' => is ( 212494789230 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'object' as { } = throw "expected"

	throw "unexpected"
	/* suppress unused warnings */
	@log: $'object' => serialize as JSON
}
catch as $ => switch $ => is ( "expected" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'objects' = {
		let $'dataset' = "{\"objects\":[{\"name\":\"tester\",\"age\":42},{\"name\":\"jester\"}]}" => parse as JSON => decorate as {
			'objects': list {
				'name': text
				'age': optional integer
			}
		} || throw "dataset could not be decorated"

		walk $'dataset'.'objects' as $ => create (
			'key' = $ .'name'
			'age' = switch $ .'age' get (
				| value as $ => create 'known' (
					'age' = $
				)
				| error => create 'unknown' ( )
			)
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'data' as list {
			'name': text
			'age': optional integer
		} = {
			create (
				'name' = "tester"
				'age' = 42
			)
			create (
				'name' = "jester"
			)
		}

		walk $'data' as $ => create (
			'key' = $ .'name'
			'age' = switch $ .'age' get (
				| value as $ => create 'known' (
					'age' = $
				)
				| error => create 'unknown' ( )
			)
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'data' as list {
			'name': text
			'age': optional integer
		} = {
			create (
				'name' = "tester"
				'age' = 42
			)
			create (
				'name' = "jester"
				'age' = unset
			)
		}

		walk $'data' as $ => create (
			'key' = $ .'name'
			'age' = switch $ .'age' get (
				| value as $ => create 'known' (
					'age' = $
				)
				| error => create 'unknown' ( )
			)
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'JSON' = "42" => parse as JSON => decorate as choice ( 'center': 16 'left': 42 'right': 24 ) || throw "invalid json"

	switch $'JSON' (
		|'center' => throw "invalid state `center` selected"
		|'left' => no-op // Test successful
		|'right' => throw "invalid state `right` selected"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'JSON' = "\"left\"" => parse as JSON => decorate as choice ( 'center' 'left' 'right' ) || throw "invalid json"

	switch $'JSON' (
		|'center' => throw "invalid state `center` selected"
		|'left' => no-op // Test successful
		|'right' => throw "invalid state `right` selected"
	)
}
```

```js
provider (
	'objects' = {
		let $'JSON' = "{\"hello\":24,\"world\":42}" => parse as JSON => decorate as collection integer || throw "invalid json"

		walk $'JSON' as $ => create (
			'key' = key
			'val' = $
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'JSON' = "42" => parse as JSON => decorate as integer || throw "invalid json"

	switch $'JSON' => is ( 42 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider (
	'objects' = {
		let $'JSON' = "[\"hello\",\"world\"]" => parse as JSON => decorate as list text || throw "invalid json"

		walk $'JSON' as $ => create (
			'key' = $
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'JSON' = "[[\"key\",\"value\"],[\"hello\",12],[\"world\",42]]" => parse as JSON => decorate as table {
			'key': text
			'value': integer
		} || throw "invalid json"

		walk $'JSON' as $ => create (
			'key' = $ .'key'
			'value' = $ .'value'
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'JSON' = "[[\"value\",\"key\"],[12,\"hello\"],[42,\"world\"]]" => parse as JSON => decorate as table {
			'key': text
			'value': integer
		} || throw "invalid json"

		walk $'JSON' as $ => create (
			'key' = $ .'key'
			'value' = $ .'value'
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'JSON' = "\"hello world\"" => parse as JSON => decorate as text || throw "invalid json"

	switch $'JSON' => is ( "hello world" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider (
	'objects' = {
		let $'CSV' = "key,val
hello,tester
world,jester" => parse as CSV => decorate as table {
			'key': text
			'val': text
		} || throw "invalid csv"

		walk $'CSV' as $ => create (
			'key' = $ .'key'
			'val' = $ .'val'
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'CSV' = "key,val
hello,tester
world,jester
" => parse as CSV => decorate as table {
			'key': text
			'val': text
		} || throw "invalid csv"

		walk $'CSV' as $ => create (
			'key' = $ .'key'
			'val' = $ .'val'
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'CSV' = "hello,tester
world,jester" => parse as CSV => decorate as list headless {
			'key': text
			'val': text
		} || throw "invalid csv"

		walk $'CSV' as $ => create (
			'key' = $ .'key'
			'val' = $ .'val'
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'CSV' = "key;val
hello;tester,user
world;jester" => parse as CSV separator: (";") => decorate as table {
			'key': text
			'val': text
		} || throw "invalid csv"

		walk $'CSV' as $ => create (
			'key' = $ .'key'
			'val' = $ .'val'
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "2021-02-03T10:20:30Z" => parse as ISODateTime || throw "invalid format"

	switch $'value' => is ( 212479064430 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "2021-08-04T10:20:30Z" => parse as ISODateTime || throw "invalid format"

	switch $'value' => is ( 212494789230 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "2021-02-03T10:20:30+04" => parse as ISODateTime || throw "invalid format"

	switch $'value' => is ( 212479050030 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "2021-08-04T10:20:30+04" => parse as ISODateTime || throw "invalid format"

	switch $'value' => is ( 212494774830 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "2021-02-03T10:20:30-04" => parse as ISODateTime || throw "invalid format"

	switch $'value' => is ( 212479078830 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "2021-08-04T10:20:30-04" => parse as ISODateTime || throw "invalid format"

	switch $'value' => is ( 212494803630 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "42" => parse as decimal locale: "en_US" || throw "invalid format"

	switch $'value' => is ( 42 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "42" => parse as decimal locale: "en_US" << ( 2 ) || throw "invalid format"

	switch $'value' => is ( 4200 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "42.42" => parse as decimal locale: "en_US" << ( 2 ) || throw "invalid format"

	switch $'value' => is ( 4242 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = ".42" => parse as decimal locale: "en_US" << ( 2 ) || throw "invalid format"

	switch $'value' => is ( 42 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "42,42" => parse as decimal locale: "nl_NL" << ( 2 ) || throw "invalid format"

	switch $'value' => is ( 4242 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'JSON' = "[42,true]" => parse as JSON || throw "invalid JSON"
	let $'test' = $'JSON' => decorate as headless {
		'A': integer
		'B': boolean
	} || throw "invalid format"

	switch $'test'.'B' (
		| true => switch $'test'.'A' => is ( 42 ) (
			| true => no-op // Test successful
			| false => throw "incorrect value `A`"
		)
		| false => throw "incorrect value `B`"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'JSON' = "[true,false]" => parse as JSON || throw "invalid JSON"
	let $'test' = $'JSON' => decorate as headless {
		'value': boolean
	} || throw "invalid format"

	switch $'test'.'value' (
		| true => throw "parse of invalid headless node succeeded"
		| false => throw "incorrect value"
	)
}
catch as $ => switch $ => is ( "invalid format" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'XML' = "<root><data>hello</data><data>world</data></root>" => parse as XML || throw "invalid XML"
	let $'test' = $'XML' => decorate as {
		'root': {
			'data': headless {
				'A': text
				'B': text
			}
		}
	} || throw "invalid format"

	switch $'test'.'root'.'data'.'A' => is ( "hello" ) (
		| true => switch $'test'.'root'.'data'.'B' => is ( "world" ) (
			| true => no-op // Test successful
			| false => throw "incorrect value `B`"
		)
		| false => throw "incorrect value `A`"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'vectors' as collection integer = {
		create ["42"] 42
		create ["-42"] -42
		create ["4200"] 4200
		create ["0"] 0
	}

	walk $'vectors' as $ => {
		let $'value' = key => parse as integer || throw "invalid format"

		switch $'value' => is ( $ ) (
			| true => no-op // Test successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'json raw' = "{\"value\":null}"
	let $'result' = $'json raw' => parse as JSON => decorate as {
		'value': optional text
	} || throw "could not parse JSON"

	switch $'result'.'value' get (
		| value as $ => throw "produced wrong value"
		| error => no-op // Test successful
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "a.b.c" => parse as pattern ( 'name': $ text "." text ) || throw "invalid format"

	switch $'value'.'name' => is ( "a" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "a.b.c" => parse as pattern ( 'name': $ text * "." text ) || throw "invalid format"

	switch $'value'.'name' => is ( "a.b" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
define 'test' as pattern ( 'full': $ text { 2 , 4 } )

consumer ( )

routine 'test' on
do {
	let $'vectors' as list {
		'value': text
		'match': boolean
	} = {
		create (
			'value' = ""
			'match' = false
		)
		create (
			'value' = "a"
			'match' = false
		)
		create (
			'value' = "ab"
			'match' = true
		)
		create (
			'value' = "abc"
			'match' = true
		)
		create (
			'value' = "abcd"
			'match' = true
		)
		create (
			'value' = "abcde"
			'match' = false
		)
	}

	walk $'vectors' as $ => {
		let $'vector' = $

		switch $'vector'.'value' => parse as pattern 'test' (
			| value as $ => switch $'vector'.'match' (
				| true => no-op // Test successful
				| false => throw "incorrect parse result"
			)
			| error => switch $'vector'.'match' (
				| true => throw "incorrect parse result"
				| false => no-op // Test successful
			)
		)
	}
}
```

```js
define 'test' as pattern ( 'full': $ text { , 4 } )

consumer ( )

routine 'test' on
do {
	let $'vectors' as list {
		'value': text
		'match': boolean
	} = {
		create (
			'value' = ""
			'match' = true
		)
		create (
			'value' = "a"
			'match' = true
		)
		create (
			'value' = "ab"
			'match' = true
		)
		create (
			'value' = "abc"
			'match' = true
		)
		create (
			'value' = "abcd"
			'match' = true
		)
		create (
			'value' = "abcde"
			'match' = false
		)
	}

	walk $'vectors' as $ => {
		let $'vector' = $

		switch $'vector'.'value' => parse as pattern 'test' (
			| value as $ => switch $'vector'.'match' (
				| true => no-op // Test successful
				| false => throw "incorrect parse result"
			)
			| error => switch $'vector'.'match' (
				| true => throw "incorrect parse result"
				| false => no-op // Test successful
			)
		)
	}
}
```

```js
define 'test' as pattern ( 'full': $ text { 2 , } )

consumer ( )

routine 'test' on
do {
	let $'vectors' as list {
		'value': text
		'match': boolean
	} = {
		create (
			'value' = ""
			'match' = false
		)
		create (
			'value' = "a"
			'match' = false
		)
		create (
			'value' = "ab"
			'match' = true
		)
		create (
			'value' = "abc"
			'match' = true
		)
		create (
			'value' = "abcd"
			'match' = true
		)
		create (
			'value' = "abcde"
			'match' = true
		)
	}

	walk $'vectors' as $ => {
		let $'vector' = $

		switch $'vector'.'value' => parse as pattern 'test' (
			| value as $ => switch $'vector'.'match' (
				| true => no-op // Test successful
				| false => throw "incorrect parse result"
			)
			| error => switch $'vector'.'match' (
				| true => throw "incorrect parse result"
				| false => no-op // Test successful
			)
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'values' = "prefix/-1234567890/suffix" => parse as pattern ( 'id': "prefix/" $ decimal locale: "en_US" "/suffix" ) || throw "invalid format"

	switch $'values'.'id' => is ( -1234567890 ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'values' = "[]" => parse as pattern ( 'text': "[" $ text "]" ) || throw "invalid format"

	switch $'values'.'text' => is ( "" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
provider {
	let $'values' = "42::64" => parse as pattern ( 'a': $ decimal locale: "en_US" "::" 'b': $ decimal locale: "en_US" ) || throw "invalid format"

	(
		'a' = $'values'.'a'
		'b' = $'values'.'b'
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'values' = "prefix/value/suffix" => parse as pattern ( 'value': text "/" $ text "/" text ) || throw "invalid format"

	switch $'values'.'value' => is ( "value" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'values' = "prefix/value" => parse as pattern ( 'value': text "/" $ text ) || throw "invalid format"

	switch $'values'.'value' => is ( "value" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'values' = "value/suffix" => parse as pattern ( 'value': $ text "/" text ) || throw "invalid format"

	switch $'values'.'value' => is ( "value" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'values' = "prefix/part/suffix" => parse as pattern ( 'type': "prefix/" $ text "/suffix" ) || throw "invalid format"

	switch $'values'.'type' => is ( "part" ) (
		| true => no-op // Test successful
		| false => throw "incorrect parse result"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'xml raw' = "
<root>
	<element><![CDATA[correct value]]></element>
</root>
"
	let $'result' = $'xml raw' => parse as XML => decorate as {
		'root': {
			'element': text
		}
	} || throw "could not parse XML"

	switch $'result'.'root'.'element' => is ( "correct value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'xml raw' = "
<root>
	<element><![CDATA[correct]]>_<![CDATA[value]]></element>
</root>
"
	let $'result' = $'xml raw' => parse as XML => decorate as {
		'root': {
			'element': text
		}
	} || throw "could not parse XML"

	switch $'result'.'root'.'element' => is ( "correct_value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider {
	let $'xml raw' = "
<data>
	<one>first entry</one>
	<two>second entry</two>
</data>
"
	let $'result' = $'xml raw' => parse as XML => decorate as {
		'data': collection text
	} || throw "could not parse XML"

	(
		'data' = walk $'result'.'data' as $ => create (
			'key' = key
			'value' = $
		)
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'xml raw' = "
<root>
	<element/>
</root>
"
	let $'result' = $'xml raw' => parse as XML => decorate as {
		'root': {
			'element': optional text
		}
	} || throw "could not parse XML"

	switch $'result'.'root'.'element' get (
		| value as $ => throw "produced wrong value"
		| error => no-op // Test successful
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'xml raw' = "<?xml version=\"1.0\" encoding=\"utf-8\"?>
<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">
	<soap:Body>correct value</soap:Body>
</soap:Envelope>
"
	let $'result' = $'xml raw' => parse as XML => decorate as {
		'Envelope': {
			'Body': text
		}
	} || throw "could not parse XML"

	switch $'result'.'Envelope'.'Body' => is ( "correct value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'xml raw' = "
<root>
	<element>wrong value</element>
	<element id=\"correct\">correct value</element>
</root>
"
	let $'result' = $'xml raw' => parse as XML => decorate as {
		'root': {
			'element'< where 'id' is "correct"> : text
		}
	} || throw "could not parse XML"

	switch $'result'.'root'.'element' => is ( "correct value" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider (
	'keys' = {
		let $'data' as list {
			'key': text
			'name': text
		} = {
			create (
				'key' = "tester"
				'name' = "one"
			)
			create (
				'key' = "tester"
				'name' = "two"
			)
			create (
				'key' = "developer"
				'name' = "three"
			)
		}
		let $'buckets' = $'data' => partition on ( .'key' )

		walk $'buckets' as $ => create (
			'key' = key
			'names' = walk $ as $ => create (
				'name' = $ .'name'
			)
		)
	}
)
```

```js
provider (
	'keys' = {
		let $'data' as list {
			'key': integer
			'name': text
		} = {
			create (
				'key' = 1
				'name' = "one"
			)
			create (
				'key' = 2
				'name' = "two"
			)
			create (
				'key' = 2
				'name' = "three"
			)
		}
		let $'buckets' = $'data' => partition on ( .'key' )

		walk $'buckets' as $ => create (
			'key' = key => serialize as decimal locale: "en_US"
			'value' = key
			'names' = walk $ as $ => create (
				'name' = $ .'name'
			)
		)
	}
)
```

```js
provider (
	'keys' = {
		let $'data' as collection text = {
			create ["tester"] "one"
			create ["tester"] "two"
			create ["developer"] "three"
		}
		let $'buckets' = $'data' => partition on key

		walk $'buckets' as $ => create (
			'key' = key
			'names' = walk $ as $ => create (
				'name' = $
			)
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list boolean = {
		create true
		create false
		create true
	}
	let $'value' = $'data' => call 'plural'::'filter' with (
		$'filter' = lambda => $'entry'
	)

	switch $'value'.size => is ( 2 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
		create 5
		create 2
		create 5
	}
	let $'magic' = 5
	let $'value' = $'data' => call 'plural'::'filter' with (
		$'filter' = lambda => $'entry' => is ( ^ $'magic' )
	)

	switch $'value'.size => is ( 2 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'object' = ^ $'Context'.'objects' => call 'plural'::'select' with (
		$'compare' = lambda => $'A'.'value' => greater-than ( $'B'.'value' )
	) || throw "no unique object to select"

	switch $'object'.'key' => is ( "two" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'object' = ^ $'Context'.'objects' => call 'plural'::'select' with (
		$'compare' = lambda => $'A'.'value' => greater-than ( $'B'.'value' )
	) || throw "no unique object to select"

	switch $'object'.'key' => is ( "two" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do try {
	let $'object' = ^ $'Context'.'objects' => call 'plural'::'select' with (
		$'compare' = lambda => $'A'.'has value'?'yes'.'value' => greater-than ( $'B'.'has value'?'yes'.'value' ) || throw "comparison data missing"
	) || throw "no selection"

	throw "object selected"
}
catch as $ => switch $ => is ( "comparison data missing" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
		create 16
		create 42
		create 39
	}
	let $'value' = $'data' => call 'plural'::'sort' with (
		$'compare' = lambda => $'A' => less-than ( $'B' )
	)

	switch $'value' => join separator: ( "," ) ( => serialize as decimal locale: "en_US" ) => is ( "16,39,42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list integer = {
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
	let $'result' as list {
		'bucket': list integer
	} = walk $'data' => call 'plural'::'split' with ( $'bucket size' = 2 ) as $ => create (
		'bucket' = walk $ as $ => create $
	)

	switch $'result' => serialize as JSON => is ( "[{\"bucket\":[16,42]},{\"bucket\":[39,17]},{\"bucket\":[43,38]},{\"bucket\":[18,44]},{\"bucket\":[37]}]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider (
	'number' = var 'integer'
	'text' = var 'text'
	'file' = file (
		token = var 'file-token'
		extension = var 'file-exten'
	)
)
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'name' = ^ $'Context'.'objects' => join ( .'key' )

	switch $'name' => is ( "onetwo" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'name' = ^ $'Context'.'objects' => join separator: ( ", " ) ( .'key' )

	switch $'name' => is ( "one, two" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'value' = ^ $'Context'.'objects' => product ( .'value' )

	switch $'value' => is ( 12 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'name' = ^ $'Context'.'objects' => shared ( .'name' ) || throw "object name not shared"

	switch $'name' => is ( "tester" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'value' = ^ $'Context'.'objects' => sum ( .'value' )

	switch $'value' => is ( 1999 ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do {
	let $'names' = ^ $'Context'.'objects' => unique ( .'name' )

	switch $'names' => join separator: ( "," ) ( ) => is ( "tester,developer" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider (
	'objects' = {
		create (
			'key' = "static"
		)
		try {
			create (
				'key' = "dynamic"
			)
			/* this should undo all changes made in under the try, but no other changes */
			throw "test collection restore"
		}
		catch => no-op
	}
)
```

```js
provider (
	'objects' = {
		let $'set' as list {
			'key': optional text
		} = {
			create ( )
			create (
				'key' = "one"
			)
			create ( )
			create (
				'key' = "two"
			)
			create ( )
		}

		walk $'set' as $ => try create (
			'key' = $ .'key' get || throw "no key"
		)
		catch => no-op
	}
)
```

```js
provider (
	'objects' = {
		let $'data' as collection { } = {
			create ["static"] ( )
			try {
				create ["dynamic"] ( )
				/* this should undo all changes made in under the try, but no other changes */
				throw "test collection restore"
			}
			catch => no-op
		}

		walk $'data' as $ => create (
			'key' = key
		)
	}
)
```

```js
provider (
	'objects' = {
		let $'data' as list {
			'key': text
		} = {
			create (
				'key' = "static"
			)
			try {
				create (
					'key' = "dynamic"
				)
				/* this should undo all changes made in under the try, but no other changes */
				throw "test list restore"
			}
			catch => no-op
		}

		walk $'data' as $ => create (
			'key' = $ .'key'
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'schema' as {
		'data' <'attribute': text > : text
	} = (
		'data' <
			'attribute' = "hello"
		> = "world"
	)

	switch $'schema'.'data'<'attribute'> => is ( "hello" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = 42 => serialize as decimal locale: "en_US"

	switch $'value' => is ( "42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = 4242 => serialize as decimal locale: "en_US" << ( 2 )

	switch $'value' => is ( "42.42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = 4242 => serialize as decimal locale: "nl_NL" << ( 2 )

	switch $'value' => is ( "42,42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = -4242 => serialize as decimal locale: "nl_NL" << ( 2 )

	switch $'value' => is ( "-42,42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list headless {
		'a': optional text
		'b': optional text
	} = {
		create (
			'a' = "hello"
		)
		create (
			'b' = "bye"
		)
	}

	switch $'data' => serialize as JSON => is ( "[[\"hello\",null],[null,\"bye\"]]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'vectors' as collection integer = {
		create ["42"] 42
		create ["-42"] -42
		create ["4200"] 4200
		create ["0"] 0
	}

	walk $'vectors' as $ => {
		let $'value' = $ => serialize as integer

		switch $'value' => is ( key ) (
			| true => no-op // Test successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
	$'Context' =
do switch $'Context' => serialize as JSON => is ( "{\"data\":[{\"key\":\"one\",\"choice\":[\"yes\",{}],\"group1\":{\"value\":42,\"description\":\"test entry one\"},\"group2\":{\"file\":[\"one\",\".txt\"]}},{\"key\":\"two\",\"choice\":[\"yes\",{}],\"group1\":{\"value\":-42,\"description\":\"test entry two\"},\"group2\":{\"file\":[\"two\",\".txt\"]}}]}" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = true => serialize as JSON

	switch $'value' => is ( "true" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = 42 => serialize as JSON

	switch $'value' => is ( "42" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = "hello world" => serialize as JSON

	switch $'value' => is ( "\"hello world\"" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = file ( token = "hello" extension = ".txt" ) => serialize as JSON

	switch $'value' => is ( "[\"hello\",\".txt\"]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'value' = list ( 42 , 12 , 24 ) => serialize as JSON

	switch $'value' => is ( "[42,12,24]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'source' as collection integer = {
		create ["a"] 42
		create ["b"] 12
		create ["c"] 24
	}
	let $'value' = $'source' => serialize as JSON

	switch $'value' => is ( "{\"a\":42,\"b\":12,\"c\":24}" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list choice ( 'one': 1 'two': 2 ) = {
		create option 'one'
		create option 'two'
	}

	switch $'data' => serialize as JSON => is ( "[1,2]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as list choice ( 'one' 'two' ) = {
		create option 'one'
		create option 'two'
	}

	switch $'data' => serialize as JSON => is ( "[\"one\",\"two\"]" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'data' as collection {
		'description': text
		'value': integer
	} = {
		create ["one"] (
			'description' = "test entry one"
			'value' = 42
		)
		create ["two"] (
			'description' = "test entry two"
			'value' = -42
		)
	}

	switch $'data' => serialize as JSON => is ( "{\"one\":{\"description\":\"test entry one\",\"value\":42},\"two\":{\"description\":\"test entry two\",\"value\":-42}}" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'schema' as {
		'data': collection {
			'description': text
			'value': text
		}
	} = (
		'data' = {
			create ["one"] (
				'description' = "test entry one"
				'value' = 42 => serialize as integer
			)
			create ["two"] (
				'description' = "test entry two"
				'value' = -42 => serialize as integer
			)
		}
	)

	switch $'schema' => serialize as XML => is ( "<?xml version=\"1.0\"?>
<data><one><description>test entry one</description><value>42</value></one><two><description>test entry two</description><value>-42</value></two></data>
" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'schema' as {
		'description': text
		'value': text
	} = (
		'description' = "hello world"
		'value' = 42 => serialize as integer
	)

	switch $'schema' => serialize as XML => is ( "<?xml version=\"1.0\"?>
<description>hello world</description><value>42</value>
" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
provider {
	no-op
	(
		'message' = "hello world"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'object' as text @limit: { , 4 } = "hello world"

	throw "length valid"
	/* suppress unused warnings */
	@log: $'object'
}
catch as $ => switch $ => is ( "text length limit violation" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'object' as text @limit: { 40 , } = "hello world"

	throw "length valid"
	/* suppress unused warnings */
	@log: $'object'
}
catch as $ => switch $ => is ( "text length limit violation" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'document' = "{\"key\":\"hello world\"}" => parse as JSON || throw "invalid JSON"
	let $'object' = $'document' => decorate as {
		'key': text @limit: { , 40 }
	} || throw "length limit exceeded"

	switch $'object'.'key' => is ( "hello world" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "{\"key\":\"hello world\"}" => parse as JSON || throw "invalid JSON"
	let $'object' = $'document' => decorate as {
		'key': text @limit: { , 4 }
	} || throw "length limit exceeded"

	throw "length valid"
	/* suppress unused warnings */
	@log: $'object'.'key'
}
catch as $ => switch $ => is ( "length limit exceeded" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'document' = "<key>hello world</key>" => parse as XML || throw "invalid XML"
	let $'object' = $'document' => decorate as {
		'key': text @limit: { , 4 }
	} || throw "length limit exceeded"

	throw "length valid"
	/* suppress unused warnings */
	@log: $'object'.'key'
}
catch as $ => switch $ => is ( "length limit exceeded" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try throw "produce trace-log"
catch as $ => switch $ => is ( "produce trace-log" ) (
	| true => switch error => is ( "VM-Errors:

VM-Stack:
  > guard::tail                               <source>:3:7
  > root::tail                                <source>:3:3
" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
	| false => throw "caught wrong value"
)
```

```js
consumer ( )

routine 'test' on
do try {
	let $'data' as {
		'key': text
		'value': @protected text
	} = (
		'key' = "one"
		'value' = "super secret value"
	)

	throw "produce trace-log"
	/* suppress unused warnings */
	@log: $'data' => serialize as JSON
}
catch as $ => switch $ => is ( "produce trace-log" ) (
	| true => switch error => is ( "VM-Errors:

VM-Stack:
  > block::+0                                 <source>:12:1
     $data = <schema:node>
          'key': text = \"one\"
          'value': ...

  > guard::tail                               <source>:3:7
  > root::tail                                <source>:3:3
" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
	| false => throw "caught wrong value"
)
```

```js
consumer ( )

routine 'test' on
do switch "ç" => is ( "ç" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do switch "Ç" => is case folding ( "ç" ) (
	| true => no-op // Test successful
	| false => throw "produced wrong value"
)
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for format function */
	let $'vectors' = list (
		file ( token = "{nr,spellout}" extension = "vier­duizend­twee­honderd" ) ,
		file ( token = "{nr,number,currency}" extension = "€ 4.200,00" ) ,
		file ( token = "{nr,number}" extension = "4.200" ) ,
		file ( token = "{nr}" extension = "4.200" ) ,
		file ( token = "{tx}" extension = "hello" ) ,
		file ( token = "{dt,date}" extension = "3 feb. 2021" )
	)
	let $'data' as 'unicode'/'message data' = (
		'types' = {
			create ["dt"] create 'calendar' 212479064430
			create ["nr"] create 'number' 4200
			create ["tx"] create 'text' "hello"
		}
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'pattern' = $
		let $'message' = $'pattern'.token => call 'unicode'::'format' with (
			$'data' = ^ $'data'
			$'locale' = "nl_NL"
		) || throw "error"

		switch $'message' => is ( $'pattern'.extension ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for trim function */
	let $'vectors' as list {
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
		let $'test' = $ .'input' => call 'unicode'::'pad' with (
			$'align' = $ .'align'
			$'length' = $ .'length'
		)

		switch $'test' => is ( $ .'result' ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'match' = "abcde" => call 'unicode'::'regex' with ( $'pattern' = "[a-z]+" ) || throw "invalid pattern"

	switch $'match' (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'match' = "abCde" => call 'unicode'::'regex' with ( $'pattern' = "[a-z]+" ) || throw "invalid pattern"

	switch $'match' (
		| true => throw "produced wrong value"
		| false => no-op // Test successful
	)
}
```

```js
consumer ( )

routine 'test' on
do try {
	let $'match' = "abcde" => call 'unicode'::'regex' with ( $'pattern' = "[a-z+" ) || throw "invalid pattern"

	throw "valid pattern"
	/* suppress unused warnings */
	switch $'match' (
		| true => no-op
		| false => no-op
	)
}
catch as $ => switch $ => is ( "invalid pattern" ) (
	| true => no-op // Vector tested successful
	| false => throw "produced wrong value"
)
```

```js
provider (
	'lines' = {
		let $'lines' = "line-0
line-1

line-2" => call 'unicode'::'split' with ( $'style' = option 'both' )

		walk $'lines' as $ => create (
			'line' = $
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for trim function */
	let $'vectors' = list (
		"line",     // nothing to trim
		"   line",  // leading spaces
		"line   ",  // trailing spaces
		" l i n e ",  // internal spaces
		"　l　i　n　e　"  // no-ASCII space
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'line' = $
		let $'trim' = $'line' => call 'unicode'::'strip' with ( )

		switch $'trim' => is ( "line" ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
consumer ( )

routine 'test' on
do {
	/* test vectors for trim function */
	let $'vectors' = list (
		"line",     // nothing to trim
		"   line",  // leading spaces
		"line   ",  // trailing spaces
		"	line",  // tabs
		"　line"    // no-ASCII space
	)

	/* test each vector */
	walk $'vectors' as $ => {
		let $'line' = $
		let $'trim' = $'line' => call 'unicode'::'trim' with ( $'style' = option 'both' )

		switch $'trim' => is ( "line" ) (
			| true => no-op // Vector tested successful
			| false => throw "produced wrong value"
		)
	}
}
```

```js
provider (
	'objects' = {
		let $'dataset' = "{\"objects\":{\"one\":{\"success\":true,\"data\":{\"name\":\"tester\",\"age\":42}},\"two\":{\"success\":false,\"data\":{\"language\":\"English\",\"message\":\"This object contains an error message.\"}}}}" => parse as JSON => decorate as {
			'objects': collection {
				'success': boolean
				'data': union (
					'object' {
						'name': text
						'age': integer
					}
					'error' {
						'language': text
						'message': text
					}
				)
			}
		} || throw "dataset could not be decorated"

		walk $'dataset'.'objects' as $ => create (
			'key' = key
			'result' = switch $ .'success' (
				| true => {
					let $'data' = $ .'data' => decorate as union 'object' || throw "object data could not be decorated"

					create 'success' (
						'name' = $'data'.'name'
						'age' = $'data'.'age'
					)
				}
				| false => {
					let $'error' = $ .'data' => decorate as union 'error' || throw "error could not be decorated"

					create 'failure' (
						'language' = $'error'.'language'
						'message' = $'error'.'message'
					)
				}
			)
		)
	}
)
```

```js
consumer ( )

routine 'test' on
do {
	let $'dataset' as collection {
		'success': boolean
		'data': union (
			'object' {
				'name': text
				'age': integer
			}
			'error' {
				'language': text
				'message': text
			}
		)
	} = {
		create ["one"] (
			'success' = true
			'data' = create 'object' (
				'name' = "tester"
				'age' = 42
			)
		)
		create ["two"] (
			'success' = false
			'data' = create 'error' (
				'language' = "English"
				'message' = "This object contains an error message."
			)
		)
	}

	switch $'dataset' => serialize as JSON => is ( "{\"one\":{\"success\":true,\"data\":{\"name\":\"tester\",\"age\":42}},\"two\":{\"success\":false,\"data\":{\"language\":\"English\",\"message\":\"This object contains an error message.\"}}}" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```

```js
consumer ( )

routine 'test' on
do {
	let $'inject' = "<element>Hello world!</element>"
	let $'document' as {
		'root': text
	} = (
		'root' = $'inject'
	)
	let $'text' = $'document' => serialize as XML

	switch $'text' => is ( "<?xml version=\"1.0\"?>
<root>&lt;element&gt;Hello world!&lt;/element&gt;</root>
" ) (
		| true => no-op // Test successful
		| false => throw "produced wrong value"
	)
}
```
