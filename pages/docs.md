---
layout: page
title: Documentation
category: docs
url: /docs/
description: >-
  Reference for the Alan platform: the documentation of every language per platform version, guides, the alan script, and release notes.
toc: true
---

This page covers platform version {{< site-version >}}: the documentation of every Alan language, the `alan` script, and guides for common tasks.
New to Alan? [**Learn Alan**](/learn/) takes you from an empty project to a working application first.
{.lead}

{{< docs-whats-new >}}

<a name="languages"></a>
## Language reference ({{% site-version %}})

<div class="cards cards-small">
{{< application-card >}}
<a class="card" href="/pages/tuts/syntax.html" aria-labelledby="card-grammar" aria-describedby="card-grammar-text">
<span class="card-kicker">First time here</span>
<span class="card-title" id="card-grammar">How to read a grammar</span>
<span class="card-text" id="card-grammar-text">The notation of every language page below, and the quirks of the compiler worth knowing.</span>
</a>
</div>

An Alan project uses several languages, one per kind of file:

- `application`, in `application.alan`: the model of your application, and the language the tutorials teach.
- `interface`, in `interface.alan`: what one system exchanges with another.
- `wiring` and `deployment`, in `wiring.alan` and `deployment.alan`: how the systems of a project connect, and where a deployment runs.
- One language per configuration file of a system type: datastore, connector, webclient, session manager.

The documentation of each language is its grammar, with explanations and examples.
A version number in the table links the release notes of that version.
Your project pins its versions in its `versions.json`; [this versions.json](https://dist.alan-platform.com/share/versions/{{< site-version >}}/versions.json) lists the ones that belong to platform version {{< site-version >}}.

{{< doc-index >}}

[All versions](/docs/archive)
{.more}

## Guides

- [**Migrating application data**](/pages/tutorials/migrations/{{< site-version >}}/migrations.html): carry a dataset into a new version of the model, and write the parts the platform cannot work out by itself.
- [**Users and passwords**](/pages/tutorials/model/{{< site-version >}}/application-users.html): accounts, passwords and sign-up instead of anonymous access.
- [**Spreadsheet import and export**](/pages/tutorials/data-import-export/data-import-export.html): Excel and CSV out of every collection, CSV back in.
- [**Version control and offline editing**](/pages/tutorials/ide/ide-version-control.html): a project in Git, edited on your own machine and deployed from the IDE.
- [**Upgrading a project**](/pages/tuts/upgrading.html): move a project to a newer platform version.
{.link-list}

{{% alan-script %}}

## Get help

- The [**forum**](https://forum.alan-platform.com/) is the place to ask when a model does not behave as you expect. Bring the model.
- The [**FAQ**](/faq/) answers the questions people ask before their first application.
- Cannot find the documentation of a file? Ask on the forum as well.
{.link-list}
