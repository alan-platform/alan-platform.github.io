---
layout: "doc"
origin: "webclient"
language: "client bindings"
version: "yar.15rc2.0"
type: "client_bindings"
---

1. TOC
{:toc}

## Client bindings
---

The *client bindings* provide bindings to the available features of the client
engine.

The `client engine` is what makes sure data is synchronized with the server,
keeps track of what the user modifies about that state, and if that is still
valid. This is called the `client state`.

In a widget the client state is used to pass that state to the controls.

### initial view binding

The `initial view binding` indicates the binding that is used at the beginning of
a view in the views. When starting to write views, and the widget is bound to
the model, know that the widget is initialized using this binding. This is
always the `node` binding. Node refers to the concept of a node in the
application model. E.g. the root node, or the node of a collection.

```js
initial view binding: 'node'
```
### Binding properties

Each binding has a set of properties. All properties are read only. Interacting
with the client engine can be done using `instructions`.

Some familiar properties like text, number and stategroup follow the same rules
as the other Alan languages. There are some special properties that are specific
to the client bindings.

The `binding` property references another binding. E.g. The `node` binding has
the `collection` property of the type `binding 'collection'`. In order to use a
binding property it requires additional information about that binding. In the
previous example, it is not know which collection from the model can be
selected. This is usually configured in the widget. Some bindings don't need
this extra information. Without any extra information from the model the widget
can just select that binding and work within that context. These bindings are
marked with the `switchable` keyword. For example:

```
'entry': binding 'entry' switchable
```

The `instruction` property is used to interact with the client engine. The
latter provides function to update texts and numbers, change state etc.

Some instructions take an argument like a file, text or view.

### Bindings
```js
'collection' node collection {
	'sort property': binding 'sort property'
	'can download files': stategroup {
		'yes' {
			'download all files': instruction
		}
		'no' { }
	}
	'is editable': stategroup {
		'no' { }
		'yes' {
			'edit mode': stategroup {
				'on' {
					'switch off': instruction
				}
				'off' {
					'switch on': instruction
				}
			}
		}
	}
	'can create entry': stategroup {
		'yes' {
			'add entry': instruction
			'add entry with key': instruction ( text )
		}
		'no' { }
	}
	'last created entry': stategroup {
		'entry' {
			'entry': binding 'entry' switchable
			'entry': reference 'collection'.'entries'
		}
		'none' { }
	}
	'amount of entries': number
	'is empty': stategroup {
		'yes' { }
		'no' {
			'size': stategroup {
				'single' { }
				'multiple' { }
			}
		}
	}
	'entries': collection {
		'entry': binding 'entry' switchable
		'node': binding 'node' switchable
	}
	'is valid': stategroup {
		'yes' { }
		'no' {
			'entries are invalid': stategroup {
				'no' { }
				'yes' { }
			}
			'cardinality constraint violation': stategroup {
				'no' { }
				'yes' { }
			}
		}
	}
	'modified': stategroup {
		'yes' { }
		'no' { }
	}
	'has ordered graphs': stategroup {
		'no' { }
		'yes' {
			'ordered graph': binding 'ordered graph'
		}
	}
}
'entry' node collection entry {
	'style': binding 'style' switchable
	'entity': binding 'entity' switchable
	'node': binding 'node' switchable
}
```
The joined entry is different in order to ensure the correct model
context. Otherwise the entry binding could be used incorrectly resulting in
engine crashes
```js
'joined entry' node joined entry {
	'style': binding 'style' switchable
	'entity': binding 'entity' switchable
	'node': binding 'node' switchable
}
'join' node join {
	'collection': binding 'collection' switchable
	'joined collection': stategroup {
		'unresolved' { }
		'resolved' {
			'collection': binding 'collection' switchable
		}
	}
	'amount of entries': number
	'is empty': stategroup {
		'yes' { }
		'no' {
			'size': stategroup {
				'single' { }
				'multiple' { }
			}
		}
	}
	'entries': collection {
		'collection entry': stategroup {
			'entry' {
				'entry': binding 'entry' switchable
				'node': binding 'node' switchable
			}
			'none' { }
		}
		'referenced entry': stategroup {
			'entry' {
				'entry': binding 'joined entry'
				'can create entry': stategroup {
					'yes' {
						'add entry to collection': instruction
					}
					'no' { }
				}
			}
			'none' { }
		}
	}
}
'sort property' node sort property { sortable }
'ordered graph' node ordered graph { sortable
	'insert before': instruction ( text , text )
	'insert after': instruction ( text , text )
	'move forward': instruction ( text )
	'move backward': instruction ( text )
	'move to sink': instruction ( text )
	'move to source': instruction ( text )
	'is valid': stategroup {
		'no' { }
		'yes' { }
	}
}
'operation' node operation {
	'reset': instruction
	'parameters': binding 'node' switchable
	'type': stategroup {
		'action' { }
		'command' {
			'execute permitted': stategroup {
				'yes' { }
				'no' { }
			}
		}
	}
	'is valid': stategroup {
		'no' { }
		'yes' { }
	}
	'executing': stategroup {
		'yes' {
			'can continue': stategroup {
				'yes' {
					'continue': instruction
				}
				'no' { }
			}
		}
		'no' {
			'last result': stategroup {
				'not invoked' { }
				'failure' { }
				'success' { }
			}
		}
	}
	'executable': stategroup {
		'yes' {
			'execute': instruction
		}
		'no' { }
	}
}
'user' user {
	'node': binding 'node' switchable
}
'engine state' unconstrained engine {
	'send feedback': instruction ( text )
	'on synchronized': instruction
	'add error message': instruction ( text , text )
	'add warning message': instruction ( text , text )
	'add success message': instruction ( text , text )
	'version': text
	'status': stategroup {
		'authenticated' {
			'anonymous session': stategroup {
				'yes' {
					'log in': instruction
				}
				'no' {
					'logout': instruction
					'username': text
					'user found': stategroup {
						'no' { }
						'yes' {
							'user': binding 'user'
						}
					}
				}
			}
		}
		'not authenticated' {
			'log in': instruction
		}
	}
	'report types': collection {
		'upload template': instruction ( file )
	}
	'reports': collection {
		'definition': stategroup {
			'known' {
				'of type': reference
			}
			'unknown' { }
		}
		'permissions': stategroup {
			'read only' { }
			'writable' {
				'delete template': instruction
			}
		}
	}
	'selected language': reference
	'languages': collection {
		'select language': instruction
		'label': text
	}
	'modules': collection {
		'name': text
		'has logo': stategroup {
			'yes' {
				'url': text
			}
			'no' { }
		}
	}
	'has landing page': stategroup {
		'yes' {
			'open landing page': instruction
		}
		'no' { }
	}
	'messages': collection {
		'remove message': instruction
		'type': stategroup {
			'error' { }
			'warning' { }
			'success' { }
			'waiting' { }
		}
		'title': text
		'has body': stategroup {
			'no' { }
			'yes' {
				'body': text
			}
		}
	}
	'server connection status': stategroup {
		'alive' { }
		'dead' { }
	}
	'network connection status': stategroup {
		'alive' { }
		'dead' { }
	}
	'platform family': stategroup {
		'Android' { }
		'macOS' { }
		'iOS' { }
		'Linux' { }
		'Windows' { }
		'undetermined' { }
	}
	'browser family': stategroup {
		'Edge' { }
		'Safari' { }
		'Chromium' { }
		'undetermined' { }
	}
	'alt key pressed': stategroup {
		'yes' { }
		'no' { }
	}
	'ctrl key pressed': stategroup {
		'yes' { }
		'no' { }
	}
	'shift key pressed': stategroup {
		'yes' { }
		'no' { }
	}
	'meta key pressed': stategroup {
		'yes' { }
		'no' { }
	}
	'toggle key pressed': stategroup {
		'yes' { }
		'no' { }
	}
	'logo url': text
	'logo-sideways url': text
	'custom application color': stategroup {
		'no' { }
		'yes' {
			'color': text
		}
	}
	'custom application name': stategroup {
		'no' { }
		'yes' {
			'name': text
		}
	}
	'busy': stategroup {
		'no' { }
		'yes' { }
	}
}
'entity' node entity {
```
'save all' includes all the collection entries that are part of this
entity. 'save' only saves the properties and collections that are
annotated with @small.
```js
	'save': instruction
	'save all': instruction
	'duplicate': instruction ( view )
	'add entry': instruction ( view )
	'cancel': instruction
	'discard': instruction
	'open view': instruction ( view )
	'node': binding 'node' switchable
	'is busy saving': stategroup {
		'yes' { }
		'no' { }
	}
	'location': stategroup {
		'local' {
			'parent location': stategroup {
				'local' { }
				'remote' { }
			}
		}
		'remote' { }
	}
	'modified': stategroup {
		'yes' { }
		'no' { }
	}
	'is valid': stategroup {
		'yes' { }
		'no' { }
	}
	'is editable': stategroup {
		'yes' { }
		'no' { }
	}
	'can be deleted': stategroup {
		'yes' {
			'delete': instruction
		}
		'no' { }
	}
}
'file' node file {
	'add single file': instruction ( file )
	'download file': instruction
	'is editable': stategroup {
		'yes' {
			'delete file': instruction
			'modified': stategroup {
				'yes' {
					'upload status': stategroup {
						'not uploaded' { }
						'uploading' { }
						'done' {
							'token': text
						}
					}
					'extension': text
				}
				'no' { }
			}
			'edit mode': stategroup {
				'on' {
					'switch off': instruction
				}
				'off' {
					'switch on': instruction
				}
			}
		}
		'no' { }
	}
	'backend known': stategroup {
		'yes' {
			'is readable': stategroup {
				'yes' {
					'revert': instruction
					'token': text
					'extension': text
				}
				'no' { }
			}
		}
		'no' { }
	}
	'is valid': stategroup {
		'yes' { }
		'no' {
			'not set': stategroup {
				'yes' { }
				'no' { }
			}
			'extension not valid': stategroup {
				'yes' {
					'pattern': text
				}
				'no' { }
			}
		}
	}
	'is set': stategroup {
		'yes' {
			'token': text
			'extension': text
		}
		'no' { }
	}
}
'window' unconstrained window {
	'close all views': instruction
	'close all but active view': instruction
	'open views': collection {
		'activate': instruction
		'close view': instruction
		'entity': binding 'entity' switchable
		'is entry view': stategroup {
			'yes' {
				'entry path': text
				'entry key': text
			}
			'no' {
				'title': text
			}
		}
		'is active view': stategroup {
			'yes' { }
			'no' { }
		}
	}
}
'group' node group {
	'node': binding 'node' switchable
	'style': binding 'style' switchable
}
'node' node {
	'open view': instruction ( view )
	'refresh queries': instruction
	'node': binding 'node'
	'entity': binding 'entity' switchable
	'operation': binding 'operation'
	'text': binding 'text'
	'file': binding 'file'
	'number': binding 'number'
	'state group': binding 'state group'
	'collection': binding 'collection'
	'join': binding 'join'
	'group': binding 'group'
	'query': binding 'query'
	'view': binding 'view' switchable
	'report': binding 'report'
	'todo': stategroup {
		'yes' {
			'for': stategroup {
				'current user' {
					'and': stategroup {
						'no one else' { }
						'others' { }
					}
				}
				'someone else' { }
			}
		}
		'no' { }
	}
	'location': stategroup {
		'local' { }
		'remote' {
			'edit mode': stategroup {
				'on' {
					'switch off': instruction
				}
				'off' {
					'switch on': instruction
					'switch off properties': instruction
				}
			}
		}
	}
	'read permitted': stategroup {
		'yes' { }
		'no' { }
	}
	'modified': stategroup {
		'yes' { }
		'no' { }
	}
	'is valid': stategroup {
		'yes' { }
		'no' { }
	}
}
'report' report {
	'report number parameter': binding 'report number parameter'
	'report text parameter': binding 'report text parameter'
	'is valid': stategroup {
		'yes' { }
		'no' { }
	}
	'templates': collection {
		'download': instruction
	}
}
'report number parameter' report number {
	'set number': instruction ( number )
	'is valid': stategroup {
		'yes' { }
		'no' { }
	}
	'is set': stategroup {
		'yes' {
			'value': number
		}
		'no' { }
	}
	'unit': text
	'decimals': number
}
'report text parameter' report text {
	'update text': instruction ( text )
	'is valid': stategroup {
		'yes' { }
		'no' { }
	}
	'is set': stategroup {
		'no' { }
		'yes' {
			'value': text
		}
	}
}
'number' node number {
	'set number': instruction ( number )
	'style': binding 'style' switchable
	'is editable': stategroup {
		'no' { }
		'yes' {
			'modified': stategroup {
				'no' { }
				'yes' {
					'number': number
				}
			}
			'edit mode': stategroup {
				'on' {
					'switch off': instruction
				}
				'off' {
					'switch on': instruction
				}
			}
		}
	}
	'backend known': stategroup {
		'no' { }
		'yes' {
			'is readable': stategroup {
				'no' { }
				'yes' {
					'revert': instruction
					'number': number
				}
			}
		}
	}
	'is set': stategroup {
		'yes' {
			'number': number
		}
		'no' { }
	}
	'unit': text
	'decimals': number
	'has maximum': stategroup {
		'yes' {
			'maximum': number
		}
		'no' { }
	}
	'has minimum': stategroup {
		'yes' {
			'minimum': number
		}
		'no' { }
	}
	'should be positive': stategroup {
		'yes' { }
		'no' { }
	}
	'is valid': stategroup {
		'yes' { }
		'no' {
			'not set': stategroup {
				'yes' { }
				'no' { }
			}
			'exceeds maximum': stategroup {
				'yes' {
					'maximum': number
				}
				'no' { }
			}
			'exceeds minimum': stategroup {
				'yes' {
					'minimum': number
				}
				'no' { }
			}
			'is negative': stategroup {
				'yes' { }
				'no' { }
			}
			'not a number': stategroup {
				'yes' { }
				'no' { }
			}
		}
	}
}
'query' node query {
	'reset all filters': instruction
	'remove all filters': instruction
	'refresh': instruction
	'download as Excel': instruction
	'download as Excel template': instruction
	'text column': binding 'query text column'
	'number column': binding 'query number column'
	'stategroup column': binding 'query stategroup column'
	'filter': binding 'query filter'
```
The context node is the node where the query is located. That is the starting
point of the query. Note that for candidate queries this is the location of the
reference and not the referenced node.
```js
	'context node': binding 'node' switchable
	'columns': collection {
		'name': text
		'column type': stategroup {
			'id' { }
			'content' { }
		}
		'type': stategroup {
			'text' {
				'text column': binding 'query text column' switchable
			}
			'file' { }
			'number' {
				'number column': binding 'query number column' switchable
			}
			'state group' {
				'stategroup column': binding 'query stategroup column' switchable
			}
			'reference' {
				'has filter': stategroup {
					'yes' { }
					'no' { }
				}
			}
			'widget' { }
		}
	}
	'can download files': stategroup {
		'yes' {
			'download all files': instruction
		}
		'no' { }
	}
	'is busy querying': stategroup {
		'yes' {
			'requery needed': stategroup {
				'no' { }
				'yes' { }
			}
		}
		'no' {
			'request status': stategroup {
				'success' { }
				'failure' { }
			}
		}
	}
	'entries are editable': stategroup {
		'yes' {
			'import csv': instruction ( file )
			'can create entry': stategroup {
				'yes' {
					'add entry': instruction ( view )
					'add entry with key': instruction ( view , text )
				}
				'no' { }
			}
			'is importing': stategroup {
				'yes' { }
				'no' { }
			}
		}
		'no' { }
	}
	'has selected entries': stategroup {
		'yes' {
			'save deletions': instruction
			'selected entries': collection {
				'deselect': instruction
				'delete': instruction
				'node': binding 'node' switchable
			}
			'number of selected entries': number
			'number of editable selected entries': number
		}
		'no' { }
	}
	'has result': stategroup {
		'no' { }
		'yes' {
			'clear': instruction
			'amount of entries visible': number
			'total amount of entries': number
			'is empty': stategroup {
				'yes' { }
				'no' {
					'result size': stategroup {
						'one' { }
						'multiple' { }
					}
				}
			}
			'selected entries': stategroup {
				'all' { }
				'some' { }
				'none' { }
			}
			'has more entries than maximum': stategroup {
				'no' { }
				'yes' {
					'can show all': stategroup {
						'yes' {
							'show all': instruction
						}
						'no' { }
					}
				}
			}
			'entries': collection {
				'entry': binding 'query entry' switchable
			}
			'backend updates are available': stategroup {
				'yes' { }
				'no' { }
			}
		}
	}
}
'query entry' query entry {
	'open entry': instruction ( view )
	'query file': binding 'query file'
	'number': binding 'query number'
	'text': binding 'query text'
	'stategroup': binding 'query stategroup'
	'collection': binding 'query collection'
	'node': binding 'node' switchable
	'style': binding 'style' switchable
	'is selected': stategroup {
		'yes' {
			'deselect': instruction
		}
		'no' {
			'select': instruction
		}
	}
	'is valid': stategroup {
		'yes' { }
		'no' { }
	}
	'is modified': stategroup {
		'yes' { }
		'no' { }
	}
	'use for': stategroup {
		'query' { }
		'candidates' {
			'select candidate': instruction
		}
	}
	'is editable': stategroup {
		'yes' {
			'delete dictionary entry': instruction
		}
		'no' { }
	}
	'cells': collection {
		'column type': stategroup {
			'id' { }
			'content' { }
		}
		'column': reference 'query'.'columns'
		'type': stategroup {
			'text' {
				'is set': stategroup {
					'yes' {
						'text': text
					}
					'no' { }
				}
			}
			'file' {
				'is set': stategroup {
					'yes' {
						'download file': instruction
						'token': text
						'extension': text
					}
					'no' { }
				}
			}
			'number' {
				'column': binding 'query number column' switchable
				'is set': stategroup {
					'yes' {
						'textual representation': text
						'number': number
					}
					'no' { }
				}
				'unit': text
				'decimals': number
			}
			'state group' {
				'is set': stategroup {
					'yes' {
						'style': binding 'style' switchable
						'state': text
					}
					'no' { }
				}
			}
			'reference' {
				'is set': stategroup {
					'yes' {
						'reference': text
					}
					'no' { }
				}
			}
			'widget' { has-widget }
		}
	}
}
'query file' query file {
	'is set': stategroup {
		'no' { }
		'yes' {
			'download file': instruction
			'token': text
			'extension': text
		}
	}
}
'query number column' query number column { sortable
	'has filter': stategroup {
		'yes' {
			'remove filter': instruction
			'select smaller than': instruction
			'select smaller than or equal to': instruction
			'select equal to': instruction
			'select greater than or equal to': instruction
			'select greater than': instruction
			'filter number criteria': instruction ( number )
			'operator selected': stategroup {
				'yes' {
					'operator': stategroup {
						'smaller than' { }
						'smaller than or equal to' { }
						'equal to' { }
						'greater than or equal to' { }
						'greater than' { }
					}
				}
				'no' { }
			}
			'criteria is valid': stategroup {
				'yes' {
					'criteria': number
				}
				'no' { }
			}
			'filter range': stategroup {
				'not available' { }
				'no' {
					'enable range': instruction
				}
				'yes' {
					'disable range': instruction
					'filter number criteria': instruction ( number )
					'operator': stategroup {
						'smaller than' {
							'or equal to': stategroup {
								'no' {
									'set': instruction
								}
								'yes' {
									'unset': instruction
								}
							}
						}
						'greater than' {
							'or equal to': stategroup {
								'no' {
									'set': instruction
								}
								'yes' {
									'unset': instruction
								}
							}
						}
					}
					'criteria is valid': stategroup {
						'yes' {
							'criteria': number
						}
						'no' { }
					}
				}
			}
			'has default filter': stategroup {
				'no' { }
				'yes' {
					'reset filter': instruction
				}
			}
			'filter set': stategroup {
				'yes' { }
				'no' { }
			}
			'unit': text
			'decimals': number
		}
		'no' { }
	}
	'representation type': stategroup {
		'model' {
			'style': stategroup {
				'decimal' { }
				'currency' { }
				'scientific' { }
				'engineering' { }
			}
		}
		'date' { }
		'date and time' { }
		'duration' {
			'unit': stategroup {
				'hours' { }
				'minutes' { }
				'seconds' { }
			}
		}
	}
	'show aggregate': stategroup {
		'no' { }
		'yes' {
			'type': stategroup {
				'sum' { }
				'average' { }
				'min' { }
				'max' { }
			}
		}
	}
}
'query number' query number {
	'column': binding 'query number column' switchable
	'is set': stategroup {
		'no' { }
		'yes' {
			'textual representation': text
			'number': number
		}
	}
	'unit': text
	'decimals': number
}
'query text column' query text column { sortable
	'query': binding 'query' switchable
	'has filter': stategroup {
		'yes' {
			'remove filter': instruction
			'set text contains': instruction ( text )
			'set text equals': instruction ( text )
			'set text starts with': instruction ( text )
			'set text ends with': instruction ( text )
			'operation': stategroup {
				'contains' { }
				'starts with' { }
				'ends with' { }
				'equals' { }
				'containment' {
					'operator': stategroup {
						'in' { }
						'not in' { }
					}
				}
			}
			'value': text
			'filter set': stategroup {
				'no' { }
				'yes' { }
			}
			'has containment filter': stategroup {
				'yes' {
					'set reference in': instruction
					'set reference not in': instruction
					'query': binding 'query' switchable
				}
				'no' { }
			}
			'has default filter': stategroup {
				'no' { }
				'yes' {
					'reset filter': instruction
				}
			}
		}
		'no' { }
	}
}
'query text' query text {
	'query text column': binding 'query text column' switchable
	'is set': stategroup {
		'no' { }
		'yes' {
			'text': text
		}
	}
}
'query stategroup column' query stategroup column { sortable
	'has filter': stategroup {
		'yes' {
			'remove filter': instruction
			'has default filter': stategroup {
				'no' { }
				'yes' {
					'reset filter': instruction
				}
			}
			'filter enabled': stategroup {
				'yes' {
					'disable state group filter': instruction
				}
				'no' {
					'enable state group filter': instruction
				}
			}
			'states': collection {
				'name': text
				'is selected': stategroup {
					'yes' {
						'unset state filter': instruction
					}
					'no' {
						'set state filter': instruction
					}
				}
			}
		}
		'no' { }
	}
}
'query stategroup' query stategroup {
	'column': binding 'query stategroup column' switchable
	'is set': stategroup {
		'yes' {
			'style': binding 'style' switchable
			'state': text
		}
		'no' { }
	}
}
'query collection column' query collection column { sortable
	'has filter': stategroup {
		'yes' {
			'remove filter': instruction
			'add key': instruction ( text )
			'has default filter': stategroup {
				'no' { }
				'yes' {
					'reset filter': instruction
				}
			}
			'operation': stategroup {
				'in' { }
				'not in' { }
			}
			'keys': collection {
				'remove key': instruction
				'value': text
			}
		}
		'no' { }
	}
}
'query collection' query collection {
	'column': binding 'query collection column' switchable
	'entries': collection {
		'style': binding 'style' switchable
		'entry': binding 'query entry' switchable
	}
}
'query filter' query filter {
	'enabled': stategroup {
		'yes' {
			'disable': instruction
		}
		'no' {
			'enable': instruction
		}
	}
}
'rule' node rule {
	'is valid': stategroup {
		'no' { }
		'yes' { }
	}
	'status': stategroup {
		'unresolved' { }
		'failed to resolve' { }
		'is busy resolving' { }
		'resolved' {
			'open entity': instruction ( view )
			'node': binding 'node' switchable
		}
	}
}
'state group' node stategroup {
	'reset': instruction
	'state': binding 'state'
	'initialized': stategroup {
		'no' { }
		'yes' {
			'revert': instruction
			'state in backend': reference
		}
	}
	'is modified': stategroup {
		'no' { }
		'yes' { }
	}
	'is set': stategroup {
		'no' { }
		'yes' {
			'state': binding 'state' switchable
		}
	}
	'is editable': stategroup {
		'no' { }
		'yes' {
			'edit mode': stategroup {
				'on' {
					'switch off': instruction
				}
				'off' {
					'switch on': instruction
				}
			}
		}
	}
	'is valid': stategroup {
		'no' {
			'no state selected': stategroup {
				'yes' { }
				'no' { }
			}
			'invalid rules': stategroup {
				'yes' { }
				'no' { }
			}
		}
		'yes' { }
	}
}
'state' node state {
	'node': binding 'node' switchable
	'rule': binding 'rule'
	'style': binding 'style' switchable
	'is selected': stategroup {
		'yes' { }
		'no' { }
	}
	'create permitted': stategroup {
		'yes' {
			'set state': instruction
		}
		'no' { }
	}
}
'text' node text {
	'update text': instruction ( text )
	'reset': instruction
	'style': binding 'style' switchable
	'is editable': stategroup {
		'no' { }
		'yes' {
			'reset password': instruction
			'modified': stategroup {
				'no' { }
				'yes' {
					'value': text
				}
			}
			'edit mode': stategroup {
				'on' {
					'switch off': instruction
				}
				'off' {
					'switch on': instruction
				}
			}
		}
	}
	'is valid': stategroup {
		'yes' { }
		'no' {
			'text does not match pattern': stategroup {
				'yes' {
					'reason': text
				}
				'no' { }
			}
			'key is not unique': stategroup {
				'yes' { }
				'no' { }
			}
			'reference not resolved': stategroup {
				'yes' { }
				'no' { }
			}
			'referenced node not valid': stategroup {
				'yes' { }
				'no' { }
			}
			'invalid rules': stategroup {
				'yes' { }
				'no' { }
			}
		}
	}
	'backend known': stategroup {
		'no' { }
		'yes' {
			'mail password': instruction
			'copy password to clipboard': instruction
			'revert': instruction
			'value': text
		}
	}
	'is set': stategroup {
		'no' { }
		'yes' {
			'text': text
		}
	}
	'navigable': stategroup {
		'yes' {
			'query': binding 'query'
			'rule': binding 'rule'
			'status': stategroup {
				'unresolved' { }
				'failed to resolve' { }
				'is busy resolving' { }
				'resolved' {
					'open reference': instruction ( view )
					'node': binding 'node' switchable
				}
			}
		}
		'no' { }
	}
	'is key': stategroup {
		'yes' {
			'key unique': stategroup {
				'no' { }
				'yes' { }
			}
		}
		'no' { }
	}
	'validation result': stategroup {
		'success' { }
		'failure' { }
	}
}
'view' view {
	'close view': instruction
	'open in new window': instruction
	'copy link to clipboard': instruction
	'node': binding 'node' switchable
	'entity': binding 'entity' switchable
	'is active view': stategroup {
		'yes' { }
		'no' { }
	}
	'action active': stategroup {
		'yes' {
			'cancel action': instruction
			'can finish step': stategroup {
				'yes' {
					'finish current step': instruction
				}
				'no' { }
			}
			'last step': stategroup {
				'yes' { }
				'no' { }
			}
		}
		'no' { }
	}
}
'style' node {
	'has style': stategroup {
		'no' { }
		'yes' {
			'type': stategroup {
				'fixed' {
					'style': stategroup {
						'foreground' { }
						'background' { }
						'brand' { }
						'link' { }
						'accent' { }
						'success' { }
						'warning' { }
						'error' { }
					}
				}
				'color' {
					'value': text
				}
			}
		}
	}
}
```
### Formatters and transformers

Formatters and transformers can be applied when binding text or number to
controls.

A formatter takes a number or text and formats it as a text. Depending on the
engine-language, the output might differ. E.g. when applying `duration in
hours`, the output might be **12h**, but in Dutch this would become: **12u**.
#### Formatters
```js
formatters
```
##### Duration

- seconds: Formats a number as: `<hours>`h`<minutes>`m`<seconds>`s e.g. **12h30m12s**
- minutes: Formats a number as: `<hours>`h`<minutes>`m e.g. **12h30m**
- hours: Formats a number as: `<hours>`h e.g. **12.5h**
```js
	'short duration in seconds': number
	'duration in seconds': number
	'duration in minutes': number
	'duration in hours': number
```
##### Date
Date formatters assume that the number is a Julian date or a Julian date time.

- `date`: formats it canonically. E.g. **2022-02-22**
- `date and time`: formats it canonically  E.g. **2022-02-22 13:34:56**

The `html date and time` formatter, formats the input so that it is valid for a
[date input element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date). If
no valid date can be determined, returns "out of range".
```js
	'date': number
	'date and time': number
	'HTML date and time': number
```
##### Miscellaneous

- `to color` Calculates a valid RGB color in hex format. E.g. **#9de318**.
- `url encode` makes the string save to use in URLs.
```js
	'to color': text
	'url encode': text
transformers
```
#### Transfomers

Takes a number input and tries to transform it. When a transformation can not be
applied, the number becomes invalid.
```js
	'julian date to JS date': number
	'julian date time to JS date': number
	'JS date to julian date': number
	'JS date to julian date and time': number
	'HTML date to julian date': text
	'HTML date time to julian date time': text
	'duration in seconds': text
	'duration in minutes': text
	'duration in hours': text
```
