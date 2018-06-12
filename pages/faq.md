---
layout: page
title: FAQ
category: main
permalink: /faq/
---


## Can I split application.alan into multiple files
No, this is currently not possible.


## Can I change how a property is visualized
The generated user interface reads the annotations in an application.alan to decide how to render a property. The Docs cover the possibilities in more detail:
https://github.com/M-industries/Docs/blob/master/docs/model/29/application/grammar.md

If you want more control over the user interface, e.g. to create one for a specific work flow, you may want to create a custom client. Documentation about this is being worked on.


## Can I limit permissions on certain properties
Permissions use role based access control. The Hours application sets `#writer` and `#reader` access on several nodes to limit their permissions where necessary:
https://github.com/M-industries/Hours/blob/master/shared/models/hours/application.alan


## Can I create 2-way many-to-many relations
If you want to simply get a list of everything that has a reference to a certain entry, you don’t have to model that explicitly. The client has a “usages” feature that automatically queries references in the opposite direction. 

To make derivations and calculations based on this relation, you need to define an inverse reference. The Hours application has an example of this:
https://github.com/M-industries/Hours/blob/cfc59c310134a0be174369b3ecf58363107c472d/shared/models/hours/application.alan#L51


## Can I connect to another system
Alan datastore systems can talk to each other with interfaces. You can talk with relational databases using the Relational Database Bridge system.

More documentation will follow.

It is possible to connect to other systems using XML Schema or third party API's. This requires additional tooling that isn't available publicly. Please contact us for more information.


