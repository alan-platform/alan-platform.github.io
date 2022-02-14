---
layout: doc
origin: connector
language: stdlib/network
version: 33.1
type: processor
---

1. TOC
{:toc}

```js
define 'network method' as @API choice ( 'get' 'head' 'post' 'put' 'delete' )
define 'network security' as @API choice ( 'strict' 'preferred' 'none' )
define 'key value list' as @API collection text
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
	'subject': optional text
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
		binds: "d52a897d2b0a358722819b7bd7f01270b9ebee38"
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
		binds: "2b8a7a321aea2baa42819b3fc5c588d55406e7d4"
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
		binds: "348f0ff9ad8a65f8e27ce732530c0b6cf9a47074"
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
		binds: "760fde5a1968de7e7f12886cc4aae328a9e93922"
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
		binds: "6f00f5e9755f27c0253b5b13ae10d807377419f0"
	/* Register webserver handlers.
	 * The handler is used as the path to respond to.
	 * Each handler is triggered by external web requests for the path.
	 */
	hook 'webserver'
		on 'network response'
		(
			$'request': 'network request'
		)
		binds: "c053a7f235c75b7c2e1bf93b7f5e6cd15f86711d"```
