---
layout: page
head: "Application Guide: Users & Authentication"
title: "Application Guide: <br>Users & Authentication"
category: docs
version: 89
---

1. TOC
{:toc}

## Introduction
This guide explains how to **add users** and basic password **authentication** to your Alan application.
The guide assumes familiarity with the Alan project structure from the online Alan IDE.

For enabling application users and authentication, the following steps are required:
- updating your `application.alan` file
- updating the `session-manager` (`systems/sessions`) configuration
- deploying your app with an initial username and password for bootstrapping authentication


## Updating your `application.alan`
Read the section on **Application users** from the [application language docs](/pages/docs/model/{{ page.version }}/application/grammar.html#application-users).
From the example model that you find there, copy the parts that you need for a `'Users'` and `'Passwords'` collection, and copy the contents of the `users` section.
For basic password authentication, you can ignore the parts about *authorities*.

Build your app, and fix any errors that you get.
Note that if you removed `anonymous` from the `users` section, the compiler will complain about your client settings (`systems/client/settings.alan`).
Fix the error by setting `anonymous login:` to `disabled`, as your app no longer supports `anonymous` users.


## Updating your *session-manager*
An Alan *session-manager* is responsible for showing the login page, handling authentication, and storing and revoking user sessions.
Open the file `systems/sessions/config.alan` and set `password-authentication:` to `enabled`.

In the `config.alan` file, you can also enable user creation for supporting user sign-up via the login page.
For user sign-up, make sure that you have the required `user-initializer:` section in your `application` model.

## Deploying your changes
You can now run **Alan: Deploy** with the **'empty'** option. \*

After a succesfull deployment, open your app and sign in with these credentials:

> | **username:** | `root` |
> | **password:** | `welcome` |

When asked, choose your own password for the `root` user.
You have now succesfully bootstrapped authentication.
You can add `Users` in your app, and send them urls for signing in.

<br>
\* If you wish to use your own `migration.alan` file, follow these steps:
- Run the [command](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) `Alan: Generate Migration` from VS Code, hit Enter twice, and select *'initialization from empty dataset'* as the *'migration type'*.
- The generated file `migrations/from_empty/migration.alan` will provide you with initial username/password data for bootstrapping authentication. Copy the parts for the `Users` and `Passwords` collection to your own `migration.alan` file.
***Do not change the username (or password hash) in your migration file!***


