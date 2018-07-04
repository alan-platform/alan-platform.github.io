---
layout: page
title: Basic README
category: docs
---


## How to use Alan
Basic steps to build your project:

1. `./alan bootstrap`
2. `./alan build`
3. `./alan package devenv/output/project.definition deployments/default`

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


## Getting Alan
If you start your project from the [template](https://github.com/M-industries/AlanProjectTemplate), it already has the `alan` utility in the root directory.

In some cases it's easier to install `alan` globally and make it available everywhere via `$PATH`. 
You can download the `alan` utility, and the tools it uses, here:

- [macOS](https://alan-platform.com/utils/latest/darwin-x64/utils.tar.gz)
- [Linux](https://alan-platform.com/utils/latest/linux-x64/utils.tar.gz)
- [Windows](https://alan-platform.com/utils/latest/windows-x64/utils.tar.gz)


## Getting an Alan Application Server
Get a server by running a one-liner in a Unix-like shell. 

> Tip: run this in a directory dedicated to the server as it will download additional utilities and create directories.

macOs:
```sh
bash -c "mkdir -p data runenv/image && curl -s https://alan-platform.com/utils/latest/darwin-x64/application-server.tar.gz | tar xzf - -C runenv/image && ln -s runenv/image/application-server serve"
```
Linux:
```sh
bash -c "mkdir -p data runenv/image && curl -s https://alan-platform.com/utils/latest/linux-x64/application-server.tar.gz | tar xzf - -C runenv/image && ln -s runenv/image/application-server serve"
```

You can start the server by running:
```sh
./serve 127.0.0.1 12345
```


## Running an image on the server
Once you have a working server, you're ready to run an image on it.

One application server can manage multiple applications (aka "stacks").
Connect to the server ask for `--help` for a list of available commands.

The `--batch replace` command backups old stacks and can be used in scripts:

```
alan connect 127.0.0.1 12345 --batch replace "demo" image
```
