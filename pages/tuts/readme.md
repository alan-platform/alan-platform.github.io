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
2. Run `./alan build -C migrations` to build the migrations.


## Data Migration
Example layout for migrations:

```
migrations/
  └ from_version_x/
      ├ migration.alan
      ├ regexp.alan
      ├ from/
      │   └ application.alan
      └ to/
          └ application.alan(.link)
```

To build the migrations, run `../alan build` from the migrations directory or `./alan build -C migrations` from the root of your project.

This will produce a `from_version_x.migration` package (all output can be found in the "dist" directory) that can be used in a deployment. To do so, copy it to the deployment. In a very basic project the correct location would be `deployments/default/instances/server.migration`:

```sh
cp dist/from_scratch.migration deployments/default/instances/server.migration
```


## Running an image on the server
Once you have a working server, you're ready to run an image on it.

One application server can manage multiple applications (aka "stacks").
Connect to the server and run the `help` command for a list of available commands.

The `--batch replace` command backups old stacks and can be used in scripts:

```
./alan connect 127.0.0.1 12345 --batch replace "demo" image
```
