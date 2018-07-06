---
layout: page
title: Basic README
category: docs
---


## How to use Alan
Basic steps to build your project:

1. `./alan bootstrap`
2. `./alan build`
3. `./alan package dist/project.pkg deployments/default`

Also make sure you build any necessary [migrations](#data-migration), and copy the migration package to the deployment.


## Modifying applications

1. Edit the application.alan.
2. Run `./alan build`.
3. Update a migration to define the initial data.


## Data Migration
Example layout for a migrations ("dataenv") environment:

```
migrations/
  ├ versions.json
  └ from_version_x/
      ├ build.json
      ├ migration.alan
      ├ regexp.alan
      ├ from/
      │   └ application.alan
      └ to/
          └ application.alan(.link)
```

> The versions.json would be the same as the one in your project, but with only the "datastore" system type and the platform version.

To build the migrations, run this from the "migrations" directory:

1. `./alan bootstrap`
2. `./alan build`

This will produce a `from_version_x.migration` package that can be used in a deployment. To do so, copy it to the deployment. In a very basic project the correct location would be `deployments/default/instances/server.migration`.


## Running an image on the server
Once you have a working server, you're ready to run an image on it.

One application server can manage multiple applications (aka "stacks").
Connect to the server ask for `--help` for a list of available commands.

The `--batch replace` command backups old stacks and can be used in scripts:

```
alan connect 127.0.0.1 12345 --batch replace "demo" image
```
