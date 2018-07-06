---
layout: page
title: FAQ
category: main
permalink: /faq/
---


## Do I need to learn programming for Alan
Alan is *low* code, but not *no* code.

Alan looks like code, but it lives on a different level than what you normally think of as programming. Instead of using abstract logic, you create data models that describes aspects of a particular domain as you can observe it. Alan does know decisions (e.g. you can describe that a mountain bike has gears but a fixie doesn't), but it never gets to the point that you're creating algorithms. 

If you're not afraid of a deeply nested `IF` or a crafty `VLOOKUP` in Excel, Alan will definitely not scare you. In fact, I bet you'll find it lot of fun.

It has characteristics that make it really suited for something like a visual application builder, so who knows what the future brings here.


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


## Can I write SQL queries

Alan's datastore is not a relational database (it's graph-based) that you can query using SQL. Don't let that stop you though. Alan can interface with other databases, and you can create queries for Excel reports that you can download straight from the default user interface. 

If you really need SQL, the datastore can expose a data stream that can be used to create an SQL mirror of the data in Alan's datastore.


## Can I connect to another system
Alan datastore systems can talk to each other with interfaces. You can talk with relational databases using the Relational Database Bridge system.

More documentation will follow.

It is possible to connect to other systems using XML Schema or third party API's. This requires additional tooling that isn't available publicly. Please contact us for more information.


## What does that versions.json do?
You'll have noticed the versions.json at the root of your project. It defines a set of packages that should be compatible. Builds of version X are guaranteed to be based on the exact same language and configuration, but may contain bugfixes. We call these "major" versions.

The project.pkg also contains this versions list, to ensure that each next step uses the same major versions as your design.

The package step adds a "minor" version for each system-type. Systems speak a set of protocols amongst each other and that need to match. Builds of system version X.Y are guaranteed to speak the same protocols. We have a mapping that tells the package utility what minor versions are correct for your project.  

Finally there is a "patch" level of versions (in semver-speak), for which we simply use incrementing build numbers. Alan's core tool chain guarantees that at this level compatibility cannot be broken, so it's always safe to use the latest builds.
