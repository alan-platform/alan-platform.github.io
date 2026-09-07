---
layout: page
head: "Application data migration"
title: "Migrating Alan application data"
category: docs
platform_version: 2026.2
---
{% comment %}
	The migration language is the connector's processor language. Its version for this platform version
	comes from _data/dist/<platform version>/versions.json (Jekyll drops the dot from that directory name).
{% endcomment %}
{% assign dist_key = page.platform_version | remove: '.' %}
{% assign dist = site.data.dist[dist_key].versions %}
{% assign connector_version = dist["system types"].connector.version %}

1. TOC
{:toc}

## Introduction

For deploying an Alan application with a `datastore` (`systems/server` in the Alan IDE), you either need to provide an initial dataset or *migrate* an existing dataset from a(n) (older) running Alan application.
That dataset needs to conform to the data structure that your `application` model (`application.alan` file) specifies.
This guide explains how you construct an initial dataset or *migrate* an existing dataset with the online Alan IDE.

Since platform version 2026.1, a migration is written in the processor language of the Alan `connector`.
If you have written migrations for an older platform version, note that the language changed completely: there are no typed declarations and no `map` anymore, and error annotations between `<!` and `!>` no longer exist.
The [migration language](#the-migration-language) section below covers everything you need for a typical application.

## Initial dataset
When clicking the button `Alan Deploy`, you get a list from which you can choose a data source for the deployment.
For your first deployment, you have to choose the **empty** option from the list.
This will initialize your application with an empty dataset.

![](images/deploy1.png)

Choosing the **empty** option creates a folder `migrations/from_empty`:

![](images/empty.png)

This folder is a complete migration project:

- `migration.alan` specifies how data should be migrated **from** the source application **to** the target application that you have built.
- `models/source/application.alan` is the model of the source dataset. For `from_empty` it is an empty model (`root { }`).
- `models/target/application.alan.link` points to your own `models/model/application.alan` file, the target model.
- `configuration.json`, `variables.json` and `interface.alan` are fixed configuration files; you never have to edit them.
- `data/` is an empty folder for auxiliary data files.

For an empty dataset, the generated `migration.alan` sets every collection of your model to `none`, the empty set:
```js
{% include_relative snippets/from-empty-generated.alan %}
```

If you want your application to start with some data instead, replace the `none` expressions with `create` entries.
For example, this migration initializes the `Menu` collection of the first step of the [restaurant tutorial](/pages/tutorials/model/{{ page.platform_version }}/application-tutorial.html) with three items:
```js
{% include_relative snippets/from-empty.alan %}
```

Be aware that `migrations/from_empty` is generated again every time you deploy with the **empty** option, so keep a copy of a `migration.alan` that you edited by hand.
The restaurant tutorial does exactly that: every step comes with a ready-made `migration.alan` in the `_docs` folder that you copy into your project.

## Existing dataset migration

After completing at least one successful deployment, you can make changes to your application model and choose to **migrate** from the current (running version) of your application, which enables you to keep application data that application users added:

![](images/deploy2.png)

The first time you choose this option, the IDE generates a migration in the `migrations/from_release` folder.
Unlike `from_empty`, this folder is generated only once: the `migration.alan` file in it is yours to maintain, and it is kept between deployments.

The `models/source/application.alan` file in this folder is the deployed version of your `application.alan` file.
It is updated automatically at every deployment with the **migrate** option. When using the online Alan IDE: do not modify `models/source/application.alan` manually for this migration!*

<sup>
*Sometimes it is useful to specify derived properties in the source model for use in your `migration.alan`. In that case, you can copy the `migrations/from_release` folder to a folder with a different name and modify the copied source model.
</sup>

## The migration language

A `migration.alan` file describes, for every base data property of the target model, where its value comes from.
The file is written in the processor language of the Alan `connector`; the [grammar of the processor language](/pages/docs/connector/{{ connector_version }}/processor/grammar.html) describes all operations that are available.
This section shows the operations that you need for migrating a typical application.

As an example, we migrate from the model of the first step of the restaurant tutorial, where `Menu` items have a `Selling price` in whole euros, to the model of the second step, where the price is in eurocents and every item has an `Item type` stategroup.
The complete migration looks like this:
```js
{% include_relative snippets/from-release.alan %}
```

**Root and nodes.** A migration always starts with `root = root as $ {`. The `$` is the *source* dataset: the data of the running application, conforming to `models/source/application.alan`.
Between parentheses you list the properties of a node of the *target* model, each followed by `=` and an expression that determines its value.
Derived values are not migrated; only base data properties are listed.

**Copying values.** The expression `$ .'Item name'` reads the property `Item name` of the current source node. Text and number values can be copied this way when their type did not change.
References are migrated as the text of the key that they refer to, so `'Item' = $ .'Item'` also works for a reference.

**Collections.** A collection is migrated by walking over the source collection and creating one target entry for each source entry:
```js
{% include_relative snippets/walk-create.alan %}
```
Inside the `walk`, the `$` is rebound to the current source entry, so `$ .'Item name'` now refers to a property of that entry.
To initialize a collection without a source, use a block with one `create` per entry, as in the `from_empty` example above, or `none` for an empty collection.

**Stategroups.** A stategroup is migrated with a `switch` on the source stategroup, creating the corresponding target state in each case: `switch $ .'Item type' ( |'Dish' as $ => { create 'Dish' ( ... ) } |'Beverage' as $ => { create 'Beverage' ( ... ) } )`.
When the stategroup is new in the target model, there is nothing to switch on, and you create a fixed state:
```js
{% include_relative snippets/new-stategroup.alan %}
```
Between the parentheses of `create 'Dish' ( ... )` you list the properties of the state, again with an expression for each.

**Groups.** A group in the target model is written as a block with a node in it: `'Management' = { ( ... ) }`, where the parentheses hold the properties of the group.

**Numbers.** Numbers are migrated as integers in the unit of the *target* numerical type. When a numerical type changes, convert the value with `product ( ... )` or `division ( ... )`; the migration language has no `*` or `/` operators. From euros to eurocents:
```js
{% include_relative snippets/number-conversion.alan %}
```

**Literals.** A text is written between double quotes (`"Example"`), a number as a plain integer (`2042`), and `none` is the empty collection.

**Navigating back.** Inside nested `walk` and `switch` statements the `$` only refers to the innermost source node. To reach data higher up, store a node under a name with `let $'root' = $` at the beginning of a block and refer to it as `$'root'`; from a deeper block, prefix the name with one `^` for every block in between, for example `^ $'root'`.

## Migration maintenance
The `from_release/migration.alan` file is a migration that you have to keep up-to-date such that it describes a source for every base data property that your `application.alan` file specifies.
When you change your model and deploy with the **migrate** option, the migration is compiled against the new target model and the deployment fails until every new or changed property has a valid expression.

The migration that the IDE generates (see [Generating a migration](#generating-a-migration) below) is a starting point, not a finished migration: it assumes that the source model has the same structure as the target model, and copies every property.
For the model change of the example above, the generated migration looks like this:
```js
{% include_relative snippets/from-release-generated.alan %}
```
Compiling it fails, because the source model has no `Item type` yet:

>'property' `Item type` was not found in 'attributes'. Existing 'attributes': `Item name`, `Selling price`

The `switch` on `$ .'Item type'` has to be replaced by a `create` of a fixed state, and the `Selling price` needs its conversion to eurocents, as shown in the complete migration in the previous section.

As another example, if you have an `application.alan` file with
```js
{% include_relative snippets/maintenance-model.alan %}
```

a valid migration from a model that only had an `Original App Name` property is:
```js
{% include_relative snippets/maintenance-migration.alan %}
```

**Missing source data.** Some expressions can fail: looking up an entry in a collection with `[ ... ]` fails when the key does not exist, and following a reference can fail as well.
Suppose the target model turns the `Administrator` text of a model into a reference to the `Users` collection, and adds the name of the administrator as a property:
```js
{% include_relative snippets/error-handling-model.alan %}
```
You can abort the migration with a message when the lookup fails, using `|| throw`:
```js
{% include_relative snippets/throw-alternative.alan %}
```
The message is displayed in the `Output` window when the migration fails while deploying your app.
Alternatively, you can handle both outcomes of a failing expression with a `switch` that distinguishes `value` from `none`:
```js
{% include_relative snippets/switch-value-none.alan %}
```

## Generating a migration
After a successful deployment, it is often useful to generate a migration based on the just deployed application model. This way, you do not have to manually specify that values should be kept for base data properties that you added in the last development iteration.
For that, run the command `Alan: Generate Migration` from the [Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette).

The command asks for:

- a *migration name*, which becomes the folder name under `migrations/`;
- the *migration target model*, which is your `models/model` (this question is skipped when your project has a single model);
- the *migration type*: `mapping from target conformant dataset` generates a migration that copies every property from a source with the same structure, and `initialization from empty dataset` generates a migration that sets every collection to `none`.

Generate a migration under a new name, or move the existing folder away first, to avoid overwriting a `migration.alan` that you edited by hand.
Sometimes it is also useful to run the command after making changes to your `application` model. Doing so gives you the mapping for newly added base properties, which you then copy into your `from_release/migration.alan`. You only have to provide valid expressions for determining their initial values.

The same generator is available from the [Terminal](https://code.visualstudio.com/docs/terminal/basics):

```
.alan/devenv/system-types/datastore/scripts/generate_migration.sh migrations/from_release models/model
.alan/devenv/system-types/datastore/scripts/generate_migration.sh migrations/from_empty models/model --strategy bootstrap
```

To check your migrations manually without deploying, run `./alan build -C migrations` from the Terminal; it compiles every migration project in the `migrations` folder.
