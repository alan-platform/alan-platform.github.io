---
layout: page
head: "Application data migration"
title: "Migrating Alan application data"
category: docs
version: 97
---

1. TOC
{:toc}

## Introduction

For deploying an Alan application with a `datastore` (`systems/server` in the Alan IDE), you either need to provide an initial dataset or *migrate* an existing dataset from a(n) (older) running Alan application.
That dataset needs to conform to the data structure that your `application` model (`application.alan` file) specifies.
This guide explains how you construct an initial dataset or *migrate* an existing dataset with the online Alan IDE.

## Initial dataset
When clicking the button `Alan Deploy`, you get a list from which you can choose a deployment type.
For your first deployment, you have choose the **empty** option from the list.
This will initialize your application with an empty dataset.

![](images/deploy1.png)

Choosing the **empty** option creates a folder `migrations/from_empty`:

![](images/empty.png)

This folder describes the migration from an empty dataset conforming to the `application` model in the `from/` folder, to a dataset that conforms to the `application` model in the `to/` folder. Note that the `to/` folder does not contain your actual `application.alan` file, but an `application.alan.link` file with a path to your `models/model/application.alan` file.

The `migration.alan` file specifies how data should be migrated **from** the source application (the empty `from` application) **to** the target application that you have built. The `migration.alan` file requires a listing of all base data properties from the target (`to/`) model, followed by an expression that determines their value. This expression can be as simple as a constant string value for a text property, as the above figure depicts. The [grammar of the migration language](/pages/docs/datastore/99/migration_mapping/grammar.html) describes all possible operations that are available.

## Existing dataset migration

After completing at least one successful deployment, you can make changes to your application model and choose to **migrate** from the current (running version) of your application, which enables you to keep application data that application users added:

![](images/deploy2.png)

This automatically generates a migration in the `migrations/from_release` folder. The `to/` folder contains the deployed version of your `application.alan` file. It is updated automatically when you deploy your app. When using the online Alan IDE: do not modify `to/application.alan` manually for this migration!*

<sup>
*Sometimes it is useful to specify derived properties in the `from/` model for use in your `migration.alan`. In that case, you can copy the `migrations/from_release` folder and modify the copied `from` model.
</sup>


## Migration maintenance
The `from_release/migration.alan` file is a migration that you have to keep up-to-date such that it describes a source for every base data property that your `application.alan` file specifies. For example, if you have have an `application.alan` file with

```js
root {
	'App Name': text
	'Users': collection ['User'] {
		'User': text
	}
	'Year': number ''
}
```

A valid migration is:
```js
root = root as $ { /* root of dataset specified by ./from/application.alan */
	'App Name': text = $ .'Original App Name' /* property in ./from/application.alan' */
	'Users': collection = <!"Error while processing Users."!> none
	'App description': text = "Example app for migrations."
	'Year': number = 2042
}
```

Between the `<! !>` you can provide an optional error message, which will be displayed in the `Output` window when the migration fails while deploying your app. With the above migration, this would happen when the `Users` collection cannot be empty:
```js
'Users': collection ['User'] non-empty { ...
```

After a succesfull deployment, it is often useful to generate a migration based on the just deployed application model. This way, you do not have to manually specify that values should be kept for base data properties that you added in the last development iteration. For that, run the command `Alan: Generate Migration` from the [Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) or use the `alan` script from the [Terminal](https://code.visualstudio.com/docs/terminal/basics).

Type `from_release` as the migration name, choose `server/model.lib` as the target model and a `mapping from target conformant dataset` to generate the migration. Sometimes it is also useful to run the command after making changes to your `application` model. Doing so will add newly added base properties to the `migration.alan` file. You then only have to provide valid expressions for determining their initial values.
