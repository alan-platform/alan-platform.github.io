---
layout: page
head: "Creating a webclient system"
title: "Creating a webclient system"
category: docs
version: voyager.2.0
---

## Introduction

There are two way to create a user interface with the Alan-platform. The first
and recommended is to use an automatically generated user interface using the
`auto-webclient` system. It requires minimal configuration and it provides all
the elements to let the user interact with the application model.

For some use cases it is however necessary to have more control over user
interaction and styling. For example when creating a customer portal or creating
visualisations specific for the problem domain.

*NB!* Creating a webclient system is not for the faint of heart. It is far more
 complex than using the auto-webclient system. The tools and languages used are
 intended for (frontend) developers.
 
## Main concepts: views, widgets and controls

A webclient consists of three
parts. [Views](/pages/docs/webclient/{{page.version}}/views/grammar.md),
[widgets](/pages/docs/webclient/{{page.version}}/widget/grammar.md) and
controls. All the parts combined is called a gui definition. A each parts plays
a specific role in the gui definition. 

Starting bottom up, the smallest part of the gui definition is a control. A
control is responsible for visualizing data on the screen and handling user
interaction. Each control has a contract (the `control.alan` file) and an
implementation file (index.ts). 

A control.alan example:
```js
{ 
	'text': text
}
```

One or more controls can be used (composed) in a widget. The widget determines
the data that is bound to the control and how user interaction results in
actions in the client. Widgets use controls by implementing their contract
(`control.alan`).

Widgets are agnostic of the application model. So when there is a collection
called 'Users' in the model, it can't be directly accessed in the widget. A more
abstract mechanism is used called
[client bindings](/pages/docs/webclient/{{page.version}}/client%20bindings/client_bindings.md). Using
the client bindings data and instructions of the binding type can be
accessed. E.g. if a collection property is valid or not or an instruction to add
a new entry to a collection.

A widget example:
```js
binding 'node' {
	'text': binding 'text' {
		'empty label': text
	}
}

switch ::'text'.'is set' (
	|'no' as $ => control 'text' {
		'text' = $ . ::'empty label'
	}
	|'yes' as $'text value' => control 'text' {
		'text' = $'text value'.'text'
	}
)
```

A widget is only one file and not a contract and implementation file, since both
are written in Alan. The top part of a widget is the contract and is used by
views when using the widget. That brings us to the last and most generic part of
the webclient, the views. The responsibility is fairly simple, i.e. compose
widgets and bind specific model properties to the bindings.

A view example:
```js
'table number view' ( .'Tables' )
	'simple text widget.alan' {
		'text':: text 'Table number' {
			'empty label': "No table number set"
		}
	}
```
