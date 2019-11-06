---
layout: page
title: "Getting Started"
category: docs
---


In this tutorial we'll take you through the steps of going from a blank model to a small application.

- [Project Layout](#project-layout)
- [Application Model](#application-model)
- [Build It & Run It](#run-it)
- [Your own application model](#your-own-application-model)
  - [Add users](#add-users)
  - [Add some collections](#add-some-collections)
  - [Numbers](#numbers)
  - [References](#references)
- [Next steps](#next-steps)


<hr>

## Project Layout

To get you up and running we've set up a project template in your online ide. The build system we're going to use expects a layout with files and folders in a particular structure, and this template sets you right on track for anything but the most complicated things you can build with Alan (like connecting to external databases).

You'll notice some top level directories here.

![](helloworld1.png)

- **.alan**
  Contains downloaded alan executables
- **.vscode**
  Contains project specific vscode settings
- **deployments**
	Contains environment specific configuration like IP addresses, in addition to stuff that will be different from one deployment to another like your datasets.
- **interfaces**
	Systems talk to each other over interfaces. For instance, the client talks to the server over an interface defined by the application model.
- **migrations**
	Data needs to match the application model specification. Migrations help you move your data from one version of that specification to another.
- **systems**
	Contains the configuration of each system that will be running for your project. Most projects have a server, a client and a reporter.
- **wiring**
	Defines how the systems and interfaces are wired together. For most projects the default here already defines everything you need, but if you want to add custom clients or external databases this is where you describe how they're connected.

For now, you can ignore .alan, .vscode, deployments, migrations, systems and wiring. We'll touch on some of those later, but we've got defaults set up there that will work for most basic projects.

First, lets take a look at the application model, as for most projects you'll spend most time editing this file.


## Application Model

Open the **interfaces/model/application.alan** file in an editor. We'll be using Visual Studio Code in the screenshots, but [you can use whatever you like](https://github.com/alan-platform?utf8=✓&q=AlanFor).

![](helloworld2.png)

The template already has a little model set up that covers some basics. Let's walk through it before we wipe it clean and start our own.

The model is a nested structure not unlike [JSON](https://json.org). At the first level you'll see some keywords:
- [users](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L1)
	There is some boiler plate here that currently allows anonymous users, so you can use the application without logging in.
- [interfaces](https://github.com/M-industries/AlanProjectTemplate/blob/e12c45306d10461c47218ec11ed872002fbce1f5/interfaces/model/application.alan#L6)
	Interfaces are declared here so that they can be assigned permissions to access parts of the application model.
- [root](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L12)
	This is where your model really starts.
- [numerical-types](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L55)
	Numbers have types, like "date" or units like "kg". Number types can be converted between for calculations (e.g. to get "meters per second") etc.

So, in **root**, you describe the data model of your application. You do so by combining properties of certain types. Essentially there are 5 data types in Alan:
- **number** (integer or natural)
	Numbers are things you can count, or do math with. [Dates and date-time values](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L42) are numbers too. Numbers are usually an integer, or a [natural](https://en.wikipedia.org/wiki/Natural_number) when they can't be zero or negative. Alan doesn't have floats, but uses conversions to maintain a specific accuracy.
- **text**
	Text is mostly just text, e.g. a "Name", or any other value that doesn't adhere to any rules. So [phone numbers](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L33) are `text`, not `number`.
	You *can* put some [input rules](/pages/docs/model/33/application/grammar.html#node) on text for the user interface, e.g. minimum length or a specific pattern.
	Text can also refer to an [entry in another collection](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L49) (like a [foreign key](https://en.wikipedia.org/wiki/Foreign_key)).
- **file**
	When you connect file storage to your server (documentation about this will follow), you can store files as well. They can be viewed in the client, or downloaded.
- **collection**
	You could (but [shouldn't](https://en.wikipedia.org/wiki/Graph_database) 😉 ) think of these as your tables. If you want to describe a bunch of "things" that are mostly the same, e.g. "Contacts", that's a collection.
	Keys in a collection are just like a text property, but you don't have to define it explicitly. Like text properties, keys can also refer to keys in another collection.
- **stategroup**
	[State groups](https://github.com/M-industries/AlanProjectTemplate/blob/bb862edd3be27df167400cbbc405aa3509d47da4/interfaces/model/application.alan#L39) represent a choice. With state groups things in one state have different properties from things in another state. E.g. road bikes and fixies are both bikes, but one has gears and shifters, whereas the other doesn't. Or finished processes have and end time, unfinished processes don't.

There is a fifth type called **group**, which is just a construct to create  grouping and name spaces: groups don't actually hold any data by themselves.


## Build It & Run It

Let's quickly try to actually boot up this example project, before we go back to making our own application.

This should be fairly easy:
- Use the button 'Alan Build' at the bottom left to run a build go over the problems with F8
- If it builds, you should be able to deploy it, by using the 'Alan Deploy' button at the bottom


## Your own application model

While getting an application for free is nice, it's even nicer to build your own. For that, lets start by wiping the **application.alan** file and then start over with this:

```
users
	dynamic : . 'Users'
	password : + 'User Data' . 'Password'
	password-status : ?'Login Status'
		active : 'Active' ( )
		reset  : 'Password Reset' ( )

interfaces

root {

}

numerical-types
```

This clean slate for an application that has "users" and requires logging in.

### Add users
Now let's add those users to the model:

```
root {
	'Users': collection ['Username'] {
		'Username': text
	}
}
```

We specified that for each user we store their password in the `'Password'`property and the Login Status in a 'Login Status' stategroup.
And we would like to have this personal data protected from updating by other users. Finally, you would want to tell Alan who has read and update right of the root type. This will be inherited until overridden.

This is how it would look like:

```
root {
	can-read: user
	can-update: user

	'Users': collection ['Username'] {
		'Username': text
		'User Data': group { can-update: equal ( user , $ ^ )
			'Login Status': stategroup @default: 'Suspended' (
				'Active'-> { }
				'Password Reset'-> { }
				'Suspended'-> { }
			)
			'Password': text
		}
	}
}
```

So, we've defined a 'Users' collection, where each key in the collection will serve as the "username" and there is a password they'll need to provide to log in. The default user interface will pick this up and present the login form next time you run the application. In this demo setup, it will inject a user 'root' with passworde 'welcome' by default, so you can login and add other users.

### Add some collections
That should work, but our app lacks purpose right now. Why not build a little multi-user todo app (when not sure what to do, make a todo app right?). So, let's say our users are involved in projects and each project has stuff that needs to be done.

```
root {
	can-read: user
	can-update: user

	'Users': collection ['Username'] {
		'Username': text
		'User Data': group { can-update: equal ( user , $ ^ )
			'Login Status': stategroup @default: 'Suspended' (
				'Active'-> { }
				'Password Reset'-> { }
				'Suspended'-> { }
			)
			'Password': text
		}
	}
	'Projects': collection ['Project Name'] {
	'Project Name': text
		'Todos': collection ['Todo'] {
			'Todo': text
		}
	}
}
```

We should probably have a little more information for each todo, like when it was created, or to which user it was assigned. It probably doesn't hurt to be able to write down some details about the todo either.

```
'Todos': collection ['Todo'] {
	'Todo': text
	'Created': natural 'date and time'
	'Description': text
	'Assignee': text -> ^ ^ .'Users'
}
```

Now we've already done some things I need to explain. Let's take them one by one.


### Numbers
```
'Created': natural 'date and time'
```

This creates a number property, typically a "natural": meaning it can't be zero or negative, which won't make sense for a timestamp. We also give it the type of 'date and time'. Properties that are the same kind of number (a "date", or "kilograms", or "minutes") all have the same numerical type. This makes sure that when you're making calculations, you also end up with the correct numerical type for the result value. More on that later, right now you need to register that numerical type:

```
numerical-types
	'date and time'
```

To help the user interface interpret this and serve up a nice date-time picker, we need to annotate this.

```
numerical-types
	'date and time' @date-time
```

### References
The other thing that's special here is the 'Assignee'.

```
'Assignee': text -> ^ ^ .'Users'
```

It's a text property, but we want it to refer to one of the users of the application. Let's break down the syntax here:

- `->`: says "hey, this should refer to something"
- `^`: this is the first step in what we call the **path** to the thing we want to refer to. It tells the program to step "up" (`^`) out of the current collection.
- `^`: the first step took us from 'Todos' to 'Project', so we take another step up.
- `.'Users'`: now that we've arrived at the root of the model, we can simply point to the 'Users' collection.

If you would like to check your addition, build the project again. And if all is well, just deploy it to see how it works in practice.

## Next steps

The project template has a model filled with examples that cover what we call **derivations**: ways to do math with numbers or derive state groups from other data.

You can [annotate your model](/pages/docs/model/45/application/grammar.html#node) to set default values and [number formats](/pages/docs/model/45/application/grammar.html#numerical-types). Check the [model language docs](/pages/docs/model/45/application/grammar.html) for more details.

Migrations can be edited by hand, for instance to bootstrap your application with more data than is automatically generated. Learn more about it in the [migrations tutorial](migration.html).

If you want to learn more, check our [documentation](/docs) or ask us directly!
