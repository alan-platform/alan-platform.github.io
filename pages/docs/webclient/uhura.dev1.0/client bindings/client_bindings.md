---
layout: "doc"
origin: "webclient"
language: "client bindings"
version: "uhura.dev1.0"
type: "client_bindings"
---

1. TOC
{:toc}

```js
initial view binding: 'node'
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
	}
	'is valid': stategroup {
		'yes' { }
		'no' { }
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
}
```
he joined entry is different in order to ensure the correct model
ontext. Otherwise the entry binding could be used incorrectly resulting in
ngine crashes
```js
'joined entry' node joined entry {
	'style': binding 'style' switchable
	'entity': binding 'entity' switchable
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
	'is valid': stategroup {
		'no' { }
		'yes' {
			'insert at': instruction ( text , text )
		}
	}
}
'operation' node operation {
	'reset': instruction
	'parameters': binding 'node' switchable
	'type': stategroup  {
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
		'yes' { }
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
	'version': text
	'status': stategroup {
		'authenticated' {
			'anonymous session': stategroup {
				'yes' {
					'log in': instruction
				}
				'no' {
					'logout': instruction
					'user': binding 'user'
					'username': text
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
}
'entity' node entity {
	'save': instruction
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
	'is busy discarding': stategroup {
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
					'is busy uploading': stategroup {
						'yes' { }
						'no' { }
					}
					'token': text
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
		'no' { }
	}
	'token': text
	'extension': text
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
			'should be positive': stategroup {
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
	'query text column': binding 'query text column'
	'number column': binding 'query number column'
	'columns': collection {
		'name': text
		'column type': stategroup {
			'id' { }
			'content' { }
		}
		'type': stategroup {
			'text' {
				'has filter': stategroup {
					'yes' {
						'remove filter': instruction
						'filter set': stategroup {
							'no' { }
							'yes' { }
						}
						'has default filter': stategroup {
							'no' { }
							'yes' {
								'reset filter': instruction
							// 'value' : text //for representation
							}
						}
						'criteria': stategroup {
							'simple' {
								'set text contains': instruction ( text )
								'set text equals': instruction ( text )
								'set text starts with': instruction ( text )
								'set text ends with': instruction ( text )
								'value': text
							}
							'other' { }
						}
					}
					'no' { }
				}
			}
			'file' { }
			'number' {
				'has filter': stategroup {
					'yes' {
						'remove filter': instruction
						'select smaller than': instruction
						'select smaller than or equal to': instruction
						'select equal to': instruction
						'select greater than or equal to': instruction
						'select greater than': instruction
						'filter number criteria': instruction ( number )
						'has default filter': stategroup {
							'no' { }
							'yes' {
								'reset filter': instruction
							// 'operator' : stategroup {
							// 	'smaller than' { }
							// 	'smaller than or equal to' { }
							// 	'equal to' { }
							// 	'greater than or equal to' { }
							// 	'greater than' { }
							// }
							// 'criteria' : number
							}
						}
						'representation type': stategroup {
							'model' { }
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
						'filter set': stategroup {
							'yes' { }
							'no' { }
						}
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
						'unit': text
						'decimals': number
					}
					'no' { }
				}
			}
			'state group' {
				'has filter': stategroup {
					'yes' {
						'remove filter': instruction
						'has default filter': stategroup {
							'no' { }
							'yes' {
								'reset filter': instruction
							// 'filter' : text //for representation
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
					// TODO: remove this:
					'total amount of entries': number
					'can show all': stategroup {
						'yes' {
							'show all': instruction
						}
						'no' { }
					}
				}
			}
			'entries': collection {
				'open entry': instruction ( view )
				'query file': binding 'query file'
				'number': binding 'query number'
				'text': binding 'query text'
				'stategroup': binding 'query stategroup'
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
								}
								'no' { }
							}
						}
						'number' {
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
			'backend updates are available': stategroup {
				'yes' { }
				'no' { }
			}
		}
	}
}
'query file' query file {
	'is set': stategroup {
		'no' { }
		'yes' {
			'token': text
			'extension': text
		}
	}
}
'query number column' query number column {
	'has filter': stategroup {
		'yes' {
			'remove filter': instruction
			'select smaller than': instruction
			'select smaller than or equal to': instruction
			'select equal to': instruction
			'select greater than or equal to': instruction
			'select greater than': instruction
			'filter number criteria': instruction ( number )
			'has default filter': stategroup {
				'no' { }
				'yes' {
					'reset filter': instruction
				}
			}
			'representation type': stategroup {
				'model' { }
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
			'filter set': stategroup {
				'yes' { }
				'no' { }
			}
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
			'unit': text
			'decimals': number
		}
		'no' { }
	}
}
'query number' query number {
	'column': binding 'query number column' switchable
	'is set': stategroup {
		'no' { }
		'yes' {
			'number': number
		}
	}
	'unit': text
	'decimals': number
}
'query text column' query text column {
	'has filter': stategroup {
		'yes' {
			'remove filter': instruction
			'criteria': stategroup {
				'simple' {
					'set text contains': instruction ( text )
					'set text equals': instruction ( text )
					'set text starts with': instruction ( text )
					'set text ends with': instruction ( text )
					'value': text
				}
				'other' { }
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
'query stategroup' query stategroup {
	'is set': stategroup {
		'yes' {
			'style': binding 'style' switchable
			'state': text
		}
		'no' { }
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
					'pattern': text
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
formatters
	'duration in seconds': number
	'duration in minutes': number
	'duration in hours': number
	'date': number
	'date and time': number
	'HTML date and time': number
	'to color': text
	'url encode': text
transformers
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
