---
layout: page
title: Documentation
category: docs
permalink: /docs/
description: >-
  Reference for the Alan platform: the documentation of every language per platform version, guides, the alan script, and release notes.
---

1. TOC
{:toc}

This page covers platform version {{ site.data.versions.current }}: the documentation of every Alan language, the `alan` script, and guides for common tasks.
New to Alan? [**Learn Alan**](/learn/) takes you from an empty project to a working application first.

{% comment %}
	A notice for the newest platform version that has release notes. The list in _data/versions.json is newest first, so a
	version met before the current one is newer than it; the reference below stays at the current version, the one the
	tutorials are written for, until that moves on.
{% endcomment %}
{% assign newest_notes = nil %}
{% assign notes_newer = false %}
{% for v in site.data.versions.versions %}
	{% if newest_notes == nil %}
		{% assign newest_notes = site.pages | where: 'origin', 'platform' | where: 'version', v.name | where: 'type', 'release notes' | first %}
		{% if newest_notes and v.name != site.data.versions.current %}{% assign notes_newer = true %}{% endif %}
	{% endif %}
	{% if v.name == site.data.versions.current %}{% break %}{% endif %}
{% endfor %}
{% if newest_notes %}
<p class="notice">
	<strong>Alan {{ newest_notes.version }}</strong>{% if notes_newer %} is out{% endif %}:
	<a href="{{ newest_notes.url | relative_url }}">release notes</a> ·
	<a href="/pages/tuts/upgrading.html">upgrading a project</a>{% if notes_newer %} ·
	<a href="/docs/archive">its language reference</a>{% endif %}
</p>
{% endif %}

<a name="languages"></a>
## Language reference ({{ site.data.versions.current }})

{% assign current_release = site.data.versions.versions | where: 'name', site.data.versions.current | first %}
<div class="cards cards-small">
{% if current_release.platform.model %}
<a class="card" href="/pages/docs/model/{{ current_release.platform.model }}/application/grammar.html" aria-labelledby="card-application" aria-describedby="card-application-text">
<span class="card-kicker">Most used · model {{ current_release.platform.model }}</span>
<span class="card-title" id="card-application">The application language</span>
<span class="card-text" id="card-application-text">Everything an <code>application.alan</code> can say: data, derivations, references, commands, users and permissions.</span>
</a>
{% endif %}
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
Your project pins its versions in its `versions.json`; [this versions.json](https://dist.alan-platform.com/share/versions/{{ site.data.versions.current }}/versions.json) lists the ones that belong to platform version {{ site.data.versions.current }}.

{% include doc-index.html %}

[All versions](/docs/archive)
{: .more}

## Guides

- [**Migrating application data**](/pages/tutorials/migrations/{{ site.data.versions.current }}/migrations.html): carry a dataset into a new version of the model, and write the parts the platform cannot work out by itself.
- [**Users and passwords**](/pages/tutorials/model/{{ site.data.versions.current }}/application-users.html): accounts, passwords and sign-up instead of anonymous access.
- [**Spreadsheet import and export**](/pages/tutorials/data-import-export/data-import-export.html): Excel and CSV out of every collection, CSV back in.
- [**Version control and offline editing**](/pages/tutorials/ide/ide-version-control.html): a project in Git, edited on your own machine and deployed from the IDE.
- [**Upgrading a project**](/pages/tuts/upgrading.html): move a project to a newer platform version.

{% comment %}
	The alan script is offered per platform version in _data/versions.json ("alan" field).
	Show the quickstart for the current version, the one the tutorials are written for; a newer version can be listed
	(with its script) on the versions page before the tutorials move to it.
{% endcomment %}
{% assign alan_version = site.data.versions.versions | where: 'name', site.data.versions.current | first %}
{% if alan_version.alan %}
<a name="alan"></a>
## The `alan` script ({{ alan_version.name }})

The [`alan`]({{ alan_version.alan }}) script is the command-line entry point to the platform.
It downloads the toolchain of its platform version, sets up a project from a template, builds the project, and packages it for deployment.
Deploying a package is what the [online IDE](/pages/tutorials/ide/ide-tutorial.html) does; the script does not deploy.
To move a project to a newer platform version, see [Upgrading a project](/pages/tuts/upgrading.html).

```sh
curl -O {{ alan_version.alan }}
chmod +x alan
./alan init     # a project from the default template, with the {{ alan_version.name }} toolchain
./alan build
```

`./alan --help` lists every subcommand.
{% endif %}

## Get help

- The [**forum**](https://forum.alan-platform.com/) is the place to ask when a model does not behave as you expect. Bring the model.
- The [**FAQ**](/faq/) answers the questions people ask before their first application.
- Cannot find the documentation of a file? Ask on the forum as well.
