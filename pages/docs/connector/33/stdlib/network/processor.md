---
layout: doc
origin: connector
language: stdlib/network
version: 33
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
		binds: "builtin::network::parse"
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
		binds: "builtin::network::http"
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
		binds: "builtin::network::ftp"
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
		binds: "builtin::network::imap"
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
		binds: "builtin::network::smtp"
```
