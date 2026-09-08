---
layout: page
title: Docs
category: main
permalink: /docs/
---

1. TOC
{:toc}

On the Alan platform you do not write an application; you write a **model** of one.
A model states what the data is, how values are computed from it, which processes the data goes through, and who may see and change what.
From that model the platform generates the database, the server, the web application, the login page, the authorization checks, and the migrations that carry your data into the next version of the model.

You do not need a programming background to start — see the [FAQ](/faq/) — and you do not need to install anything: the tutorials below run in a browser.

## Start here

### Step 1 — Get an environment

[**Developing software with Alan**](/pages/tutorials/ide/ide-tutorial.html) sets you up with the online IDE: the project layout, the editor, and the build and deploy buttons that every tutorial after this one uses.

Everything below assumes you have that project open.
To work on your own machine instead, use the [`alan` script](#alan) further down this page — but note that **deploying** a project still goes through the online IDE, so you need an account there either way.
The [version control guide](/pages/tutorials/ide/ide-version-control.html) explains how to keep a project in Git and edit it locally while deploying from the IDE.

### Step 2 — Learn the language

Two tutorials teach the same `application` language at different speeds.
Both end in a complete, working application.
Pick the one that suits how you like to learn — or read the fast one first and the thorough one after.

#### The fast path: [Mission Control](/pages/tutorials/mission/{{ site.data.versions.current }}/mission-control.html)

*One afternoon, seven short acts.* You build the ground software for a lunar cargo flight.

Each act ends in something you watch happen: a total that is never stale, a launch button that cannot exist while the vehicle is overloaded, an assembly that cannot contain itself.
It includes the unit mismatch that cost NASA the Mars Climate Orbiter — caught by the compiler while you type.
The whole language passes by in outline: computations, references, state machines, graph constraints, users, permissions and migrations.

Take this path if you want to see quickly what the platform can do.

#### The detailed path: [a Restaurant app](/pages/tutorials/model/{{ site.data.versions.current }}/application-tutorial.html), in three parts

*Three parts, one sitting each.* You build an app for a restaurant, from the menu to the kitchen.

[Part I](/pages/tutorials/model/{{ site.data.versions.current }}/application-tutorial.html) is about data: collections, nodes, keys, states and references.
[Part II](/pages/tutorials/model/{{ site.data.versions.current }}/application-tutorial2.html) is about computation and interaction: derived values, conditional expressions, reference sets, commands and actions.
[Part III](/pages/tutorials/model/{{ site.data.versions.current }}/application-tutorial3.html) is about processes: state machines, advanced references, and products assembled from other products.

Every construct is explained where it appears, and every topic ends with a folder inside your own project holding the model as it should be at that point, so you can always compare.

Take this path if you want to understand every line before moving on.

**In a hurry?** The [quick start](/pages/tuts/getting-started.html) is one page: from an empty project to a small application with users, passwords and permissions.

### Step 3 — Keep the data you entered

Models change; the data they describe should survive the change.
[**Migrating application data**](/pages/tutorials/migrations/{{ site.data.versions.current }}/migrations.html) shows how a deployment carries an existing dataset into a new version of your model, and how to write the parts the platform cannot work out by itself.
Read it before your application holds data you would mind losing.

## Building something of your own

- [**Users & Authentication**](/pages/tutorials/model/{{ site.data.versions.current }}/application-users.html) — replace anonymous access with real accounts, passwords and sign-up: the basis for permissions.
- [**Spreadsheet data import & export**](/pages/tutorials/data-import-export/data-import-export.html) — every collection exports to Excel and CSV, and takes CSV back in.
- [**Version control & offline editing**](/pages/tutorials/ide/ide-version-control.html) — put your project in Git, work with others, edit locally.
- The [forum](https://forum.alan-platform.com/) is the place to ask when a model does not behave as you expect. Bring the model.

Two habits carry you a long way: **build often**, so that a single change is all you have to inspect when something breaks, and **read the error** — the compiler reports where the problem is, what it expected there, and what it found instead.

## Background

- [**Introducing Alan**](/pages/tuts/introducing.html) — what the platform is and why it works the way it does.
- [**The Alan stack from the bottom up**](/pages/tuts/bottom-up.html) — what actually runs on a server after you deploy.
- [**FAQ**](/faq/) — starting with whether you need to be a programmer for this.
- [**How to read a grammar**](/pages/tuts/syntax.html) — the notation used throughout the language documentation below.

{% comment %}
	The alan script is offered per platform version in _data/versions.json ("alan" field).
	Show the quickstart for the newest version that has one.
{% endcomment %}
{% assign alan_version = nil %}
{% for v in site.data.versions.versions %}
	{% if alan_version == nil and v.alan %}
		{% assign alan_version = v %}
	{% endif %}
{% endfor %}
{% if alan_version %}
<a name="alan"></a>
## The `alan` script ({{ alan_version.name }})

The [`alan`]({{ alan_version.alan }}) script is the command-line entry point to the platform.
It downloads the toolchain for its platform version, sets up an empty project from a template, builds the project, and packages it for deployment.
Deploying that package is a step the online IDE does for you; local deployment is not part of the script.

```sh
curl -O {{ alan_version.alan }}
chmod +x alan
./alan init     # empty project from the default template, fetches the {{ alan_version.name }} toolchain
./alan build
```

Run `./alan --help` for all subcommands.
{% endif %}

<a name="languages"></a>
## Language documentation ({{ site.data.versions.current }})

An Alan project uses several languages, one per kind of file.
The `application` language is for `application.alan` files — the model of your application, and the language both tutorials teach.
The `interface` language describes what one system exchanges with another, in `interface.alan` files.
The `wiring` language connects the systems of a project in `wiring.alan`, the `deployment` language says where a deployment runs in `deployment.alan`, and each system type — datastore, connector, webclient, session manager — documents the files that configure it.

If you cannot find the documentation for a file you are looking at, ask on the [forum](https://forum.alan-platform.com/).

See [versions.json](https://dist.alan-platform.com/share/versions/{{ site.data.versions.current }}/versions.json) for the system type versions that belong with this platform version; your own project pins its versions in its `versions.json`.

{% include doc-index.html %}

[other versions...](/docs/archive)
{: style="text-align: right"}
