---
layout: page
title: "Hello World"
category: docs
---


> Take a look at the [Reference Guide](reference.html) for an overview of the bits, pieces and commands used throughout this tutorial. 

In this tutorial we'll take you through the steps going from a blank model to a little "Hello World" application. 

To get you up and running we've created a project template. The build system we're going to use expects a layout with files and folders in a particular structure, and this template sets you right on track for anything but the more complicated things you can build with Alan (like connecting to external databases).

You'll notice some top level directories here, from the top:

- deployments
  Contains environment specific configuration like IP addresses, in addition to stuff that will be different from one deployment to another like your datasets.
- interfaces
  In Alan systems talk to each other over interfaces. For instance, the client talks to the server over an interface defined by the application model. 
- migrations
  Data needs to match the application model specification. Unlike relational databases, the model drives the entire application and will often change between versions of your application. Migrations help you move your data from one version to another. 
- systems
  Contains the configuration of each system that will be running for your project. Most projects have a server, a client and a reporter. 
- wiring
  Defines how the systems and interfaces are wired together. For most projects the default here already defines everything you need, but if you want to add custom clients or external databases this is where you describe how they're connected.

For now, you can forget about deployments, migrations, systems and wiring. We've got defaults set up there that will work and some tools to generate files where needed. We'll touch on them later.

Firstly, lets take a look at the application model. As we said earlier, it drives everything and this file is the one you'll spend most time editing.

Open the application.alan file in an editor. We'll be using Sublime Text in the screenshots, but [you can use whatever you like](https://github.com/M-industries?utf8=✓&q=AlanFor). 

The template already has a little model set up that covers some basics. Let's walk through it before we wipe it clean and start our own.

The model is a nested data structure not unlike [JSON](https://json.org). At the first level you'll see some keywords:
- [users](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L1)
  There is some boiler plate here that currently allows anonymous users (you can use the application without logging in). To use user accounts, uncomment the other lines that point to a "Users" collection and the "Password" property in it.
- [roles](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L6)
  Permissions are currently (we're working a completely revised system) set using roles. Users are assigned to roles to give them read and/or write access to parts of the data.
- [root](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L12)
  This is where your model really starts. Note the basic read and write permissions that are set here.
- [numerical-types](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L55)
  Numbers have types, like "date" or units like "kg". Number types can be converted between for calculations (e.g. to get "meters per second") etc. We'll get to that later.

So, in "root", you describe the data model of your application. The base of that is describing your data types. Essentially there are 4 of those in Alan:
- number
  Numbers are things you can count, or do math with. [Dates and date-time values](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L42) are numbers too.
- text
  Text is mostly just text, e.g. "Name", or any other value that doesn't adhere to any rules. So [phone numbers](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L33) are `text`, not `number`.
  You *can* put some [input rules](/pages/docs/model/33/application/grammar.html#node) on text for the user interface, e.g. minimum length or a specific pattern.
  Text can also refer to an [entry in another collection](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L49) (like a "foreign key").
- collection
  You could (but [shouldn't](https://en.wikipedia.org/wiki/Graph_database) ;) ) think of these as your tables. If you want to describe a bunch of "things" that are mostly the same, e.g. "Contacts", that's a collection.
  Keys in a collection are just like a text property, but they're implicit. So, keys can also refer to keys in another collection. 
- stategroup
  [State groups](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L39) are where it gets really interesting: they represent a choice. With this things in one state have slightly different properties from things in another state. E.g. road bikes and fixies are both bikes, but one has gears and shifters, whereas the other doesn't.

There is a fifth type called "group", which is just a construct to create (visual) grouping and name spaces: groups don't actually hold any data by themselves.

