---
layout: page
head: "Application Guide: Users & Authentication"
title: "Application Guide: <br>Users & Authentication"
category: docs
model_version: 108
platform_version: 2026.2
---

1. TOC
{:toc}

## Introduction
Every app in the tutorials so far used `anonymous` users: anyone who opens the app can read and change everything.
This guide replaces that with real users and password **authentication**, which is the basis for permissions — deciding who may see and change which part of the data.

It assumes the project structure of the online Alan IDE, as described in the [IDE tutorial](/pages/tutorials/ide/ide-tutorial.html), and a model you can build, such as the one from the [application tutorial](/pages/tutorials/model/{{ page.platform_version }}/application-tutorial.html).

Three things need to change:
- the `application.alan` model, which gains a users administration,
- the `session-manager` configuration in `systems/sessions`, which handles logging in,
- the deployment, which needs an initial username and password to bootstrap authentication.

## Updating your `application.alan`
Read the section on **Application users** in the [application language documentation](/pages/docs/model/{{ page.model_version }}/application/grammar.html#application-users).
From the example model there, copy the parts you need for a `'Users'` and a `'Passwords'` collection, and the contents of the `users` section.
The parts about *authorities* can be ignored for basic password authentication.

Build the app and fix the errors that appear.
Removing `anonymous` from the `users` section makes the compiler complain about the client settings in `systems/client/settings.alan`: set `anonymous login:` to `disabled` there, because the app no longer has anonymous users.

## Updating your *session-manager*
An Alan *session-manager* shows the login page, checks credentials, and stores and revokes user sessions.
Open `systems/sessions/config.alan` and set `password-authentication:` to `enabled`.

The same file can enable user creation, which lets people sign up from the login page.
Sign-up requires a `user-initializer:` section in the `application` model, which the documentation section above describes.

## Deploying your changes
Run `Alan Deploy` and choose the **empty** option. \*

Open the app after the deployment succeeds and sign in with:

> | **username:** | `root` |
> | **password:** | `welcome` |

Choose your own password for the `root` user when the app asks for it.
Authentication is now bootstrapped: you can add `Users` in the app and send them the URL to sign in.

<br>
\* The **empty** option deletes the data of the running app, which is what the first deployment with authentication needs.
To keep your data, use your own `migration.alan` file instead:
- Run the command `Alan: Generate Migration` from the [command palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) in VS Code. It asks for the migration directory and the model to migrate to — accept the defaults with Enter — and then for the *'migration type'*: choose *'initialization from empty dataset'*.
- The generated file `migrations/from_empty/migration.alan` contains initial username and password data. Copy the parts for the `Users` and `Passwords` collections into your own `migration.alan` file.

***Do not change the username or the password hash in your migration file***: the hash is what makes `welcome` work as the initial password, and a changed hash locks you out of your own app.
