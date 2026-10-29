---
layout: page
title: Learn Alan
category: learn
url: /learn/
description: >-
  Get started with Alan: set up the online IDE, build a first application with the Mission Control or restaurant tutorial, and keep your data with migrations.
toc: true
---

Build a working application in your browser, with nothing to install and no programming background needed.
On the Alan platform you do not write the application; you write a **model** of it, and the platform generates the rest.
{.lead}

## Get started

### 1. Set up the online IDE

[**Developing software with Alan**](/pages/tutorials/ide/ide-tutorial.html) sets you up with the online IDE: the project layout, the editor, and the build and deploy buttons that every tutorial after it uses.
The tutorials assume you have that project open, and use platform version {{< site-version >}}.

Prefer your own machine? The [`alan` script](/docs/#alan) builds a project locally, and the [version control guide](/pages/tutorials/ide/ide-version-control.html) shows how to edit in Git; deploying always goes through the online IDE.

### 2. Build your first application

Two tutorials teach the same `application` language at different speeds, and both end in a complete, working application.
Pick the one that suits how you learn, or take the fast one first and the detailed one after.

<div class="cards">
<a class="card" href="/pages/tutorials/mission/{{< site-version >}}/mission-control.html" aria-labelledby="card-mission" aria-describedby="card-mission-text">
<span class="card-kicker">Fast path · one afternoon</span>
<span class="card-title" id="card-mission">Mission Control</span>
<span class="card-text" id="card-mission-text">Build the ground software for a lunar cargo flight in seven short acts. A total that is never stale, a launch button that cannot exist while the vehicle is overloaded, and the unit mismatch that cost NASA the Mars Climate Orbiter, caught while you type.</span>
</a>
<a class="card" href="/pages/tutorials/model/{{< site-version >}}/application-tutorial.html" aria-labelledby="card-restaurant" aria-describedby="card-restaurant-text">
<span class="card-kicker">Detailed path · three parts</span>
<span class="card-title" id="card-restaurant">A restaurant app</span>
<span class="card-text" id="card-restaurant-text">From the menu to the kitchen, one part per sitting. Every construct is explained where it appears, and every topic ends with a folder in your project holding the model as it should be, so you can always compare.</span>
</a>
</div>

Back for the next part of the restaurant tutorial?
[I.&nbsp;Data](/pages/tutorials/model/{{< site-version >}}/application-tutorial.html) ·
[II.&nbsp;Computation](/pages/tutorials/model/{{< site-version >}}/application-tutorial2.html) ·
[III.&nbsp;Processes](/pages/tutorials/model/{{< site-version >}}/application-tutorial3.html)

### 3. Keep the data you entered

Models change, and the data they describe should survive the change.
[**Migrating application data**](/pages/tutorials/migrations/{{< site-version >}}/migrations.html) shows how a deployment carries a dataset into the next version of your model, and how to write the parts the platform cannot work out by itself.
Read it before your application holds data you would mind losing.

## Next steps

<div class="cards cards-small">
<a class="card" href="/pages/tutorials/model/{{< site-version >}}/application-users.html" aria-labelledby="card-users" aria-describedby="card-users-text">
<span class="card-title" id="card-users">Users and passwords</span>
<span class="card-text" id="card-users-text">Replace anonymous access with accounts, passwords and sign-up: the basis for permissions.</span>
</a>
<a class="card" href="/pages/tuts/getting-started.html" aria-labelledby="card-example" aria-describedby="card-example-text">
<span class="card-title" id="card-example">A one-page example</span>
<span class="card-text" id="card-example-text">A small application with users, passwords and permissions, from an empty project, on a single page.</span>
</a>
<a class="card" href="/pages/tutorials/data-import-export/data-import-export.html" aria-labelledby="card-spreadsheet" aria-describedby="card-spreadsheet-text">
<span class="card-title" id="card-spreadsheet">Spreadsheet import and export</span>
<span class="card-text" id="card-spreadsheet-text">Every collection exports to Excel and CSV, and takes CSV back in.</span>
</a>
<a class="card" href="/pages/tutorials/ide/ide-version-control.html" aria-labelledby="card-git" aria-describedby="card-git-text">
<span class="card-title" id="card-git">Version control</span>
<span class="card-text" id="card-git-text">Put a project in Git, work with others, and edit on your own machine.</span>
</a>
</div>

To look something up, go to the [documentation](/docs/): the language reference, the `alan` script, more guides, and the release notes.

Stuck on a model? Ask on the [forum](https://forum.alan-platform.com/), and bring the model.

## Understand the platform

A model states what the data is, how values are computed from it, which processes the data goes through, and who may see and change what.
From that model the platform generates the database, the server, the web application, the login page, the authorization checks, and the migrations that carry your data into the next version of the model.

- [**Introducing Alan**](/pages/tuts/introducing.html): what the platform is, and why it works the way it does.
- [**The Alan stack from the bottom up**](/pages/tuts/bottom-up.html): what actually runs on a server after you deploy.
- [**FAQ**](/faq/): from whether you need to be a programmer to how Alan relates to SQL.
{.link-list}
