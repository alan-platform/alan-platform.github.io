---
layout: page
title: FAQ
category: main
url: /faq/
class: faq
toc: true
description: >-
  Answers to the questions people ask before their first Alan application: programming background, permissions, SQL, connecting other systems, versions.
---

Answers to the questions people ask before their first Alan application.
Is yours not here? Ask on the [forum](https://forum.alan-platform.com/).
{.lead}

## Getting started

### Do I need to learn programming for Alan?

Alan looks like code, but it lives on a different level than what you normally think of as programming.
Instead of using abstract logic, you create data models that describe aspects of a particular domain as you can observe it.
Alan lets you model decisions (you can describe that a mountain bike has gears but a fixie does not), but you do not have to express them in abstract algorithms.

If you are not afraid of a deeply nested `IF` or a crafty `VLOOKUP` in Excel, Alan will definitely not scare you. In fact, we bet you will find it lots of fun.

It has characteristics that make it really suitable for something like a visual application builder, so who knows what the future brings here.

## Modeling

### Can I change how a property is visualized?

The generated user interface reads the annotations (`@...`) in an `application.alan` file to decide how to render a property.
The [documentation](/pages/docs/model/{{< platform-component "model" >}}/application/grammar.html) covers the possibilities in more detail.

If you want more control over the user interface, for example to create one for a specific workflow, you may want to create a custom client.
Documentation about this is being worked on.

### Can I set required permissions for certain properties?

Permissions are set on nodes: groups, entries and states.
You can set read and update permissions to limit access to specific users, or to users with a specific role.

### Can I create 2-way many-to-many relations?

If you simply want a list of everything that has a reference to a certain object, you do not have to model that explicitly.
The client has a "usages" feature that queries references in the opposite direction automatically.

For computations based on references in the opposite direction, you need to specify [bidirectional references](/pages/docs/model/{{< platform-component "model" >}}/application/grammar.html#bidirectional-references).

## Data and other systems

### Can I write SQL queries?

Alan's datastore is graph-based, not a relational database, so you cannot query it with SQL.
Do not let that stop you, though: Alan can interface with other databases, and you can create queries for Excel reports that you download straight from the default user interface.

If you really need SQL, the datastore can expose a data stream from which you create an SQL mirror of the data in Alan's datastore.

### Can I connect to another system?

Alan `datastore` systems talk to each other through Alan interfaces.
You can communicate with relational databases using the system type [`relational-database-bridge`](/docs/#languages).
You can interact with other systems over HTTP using the system type [`connector`](/docs/#languages).

## Versions and the roadmap

### What does that versions.json do?

You will have noticed the `versions.json` at the root of your project.
It defines a set of packages that should be compatible.
Builds of version X are guaranteed to be based on exactly the same language and configuration, but may contain bug fixes.
We call these "major" versions.

The [project.pkg](/pages/tuts/bottom-up.html#project) contains this versions list as well, so that each next step uses the same major versions as your design.

Finally there is a "patch" level of versions (in semver terms), for which we simply use incrementing build numbers.
Alan's core toolchain guarantees that compatibility cannot break at this level, so it is always safe to use the latest builds.

### What is the roadmap for Alan?

[Kjerner](https://www.kjerner.nl/) and [Applicatiefabriek](https://www.applicatiefabriek.nl/) use Alan to build solutions for their customers.
With the experience from those solutions, we keep extending and improving the Alan platform.

Long-term plans include:

- A generated GUI that leaves even fewer reasons to choose a custom one.
- Custom GUIs on the platform that third-party developers of controls and widgets can extend easily.
- Todo items as the primary driver of the interaction with an application.
- Better querying, reporting and data visualization.
- Better support for creating live dashboard applications.
- A graphical modeler, which makes development more accessible to first-time application developers.
- A marketplace for applications, external connectors, and GUI controls and widgets.

## Still have a question?

<div class="cards cards-small cards-three">
<a class="card" href="https://forum.alan-platform.com/" aria-labelledby="card-forum" aria-describedby="card-forum-text">
<span class="card-kicker">Ask</span>
<span class="card-title" id="card-forum">The forum</span>
<span class="card-text" id="card-forum-text">The place to ask when a model does not behave as you expect. Bring the model.</span>
</a>
<a class="card" href="/learn/" aria-labelledby="card-learn" aria-describedby="card-learn-text">
<span class="card-kicker">Start</span>
<span class="card-title" id="card-learn">Learn Alan</span>
<span class="card-text" id="card-learn-text">Build a first application in your browser, with nothing to install.</span>
</a>
<a class="card" href="/docs/" aria-labelledby="card-docs" aria-describedby="card-docs-text">
<span class="card-kicker">Look up</span>
<span class="card-title" id="card-docs">Documentation</span>
<span class="card-text" id="card-docs-text">The language reference, the guides and the <code>alan</code> script.</span>
</a>
</div>
