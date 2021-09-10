---
layout: page
title: "Application Tutorial:<br>a Restaurant app"
category: docs
version: 89
---

1. TOC
{:toc}

## Introduction
This tutorial aims to give you a basis for working with the application language: the main language for building Alan apps.
Before you get started, make sure that you have completed the [IDE tutorial](/pages/tutorials/ide-tutorial.html).

By means of a story we will take you along several topics and build up the model at the same time. At the end of some topics, a reference to a tutorial folder is provided in case you need extra help to get the expected result. Enjoy!

Imagine you own a restaurant. Business is doing so well you start to feel you need to be more in control of what's going on, before chaos sets in.

Alan to the rescue!

Alan is a platform that provides a language to model your data and processes in a flexible, yet structured way. From the model that you create, the Alan platform generates a fully fledged web application for entering data and reviewing the state of your restaurant.

So, let's dive in!

## Modeling data
A restaurant is nothing without a good menu. So, first, let's take a look at the menu that shows us all the good food and nice drinks you offer.

### Menu
{:.no_toc}

| *Appetizer* | *Price (€)* |
| :- | :-: |
| Shrimp salad | 3,50 |
| Tomato soup | 4,50 |
| Ciabatta with tapenade | 2,50 |

| *Main course* | *Price (€)* |
| :- | :-: |
| Beef stew | 18 |
| Grilled salmon | 16,50 |
| Mashed potato with sauerkraut | 14 |

| *Dessert* | *Price (€)* |
| :- | :-: |
| Chocolate mouse | 4,50 |
| Vanilla ice cream | 3,50 |
| Cherry pie | 4 |

| *Drinks* | *Price (€)* |
| :- | :-: |
| Orange juice | 4,50 |
| Spa rood | 3 |
| Heineken pilsner | 4,20 |
| Cappuccino | 3,50 |
| Mint tea | 3 |
| Mojito | 6,30 |

This menu shows 5 kinds of data:
1. The item that can be ordered (`Item name`)
2. The price per item in Euro (`Selling price`)
3. If it is a dish or a beverage (`Item type`)
4. The type of dish or beverge (`Dish type` / `Beverage type`)
5. And of course, that this collectively is a menu (`Menu`)

If we want to store the menu in Alan application, we can start with this Alan model of a menu:
```js
'Menu': collection ['Item name'] {
	'Item name': text
	'Selling price': number 'euro'
}
```

This small, unfinished model tells us that a `Menu` is a **collection**: a collection of `Menu` items. Each menu item has an `Item name` and a `Selling price`. Each menu item can be uniquely identified by its `Item name`, like 'Chocolate mouse'. `['Item name']` after `collection` expresses that: `Item Name` is the **key attribute**. An `Item Name` such as 'Chocolate mouse' is a **key** of a `Menu` item.

A single `Menu` item consisting of an `Item name` and a `Selling price` is called a **node** (e.g. 'Chocolate mouse', '4,50'). So, a `Menu`-collection stores nodes (menu items). In the model, curly braces ( **{ ... }** ) and everything inbetween define the *type* of a node (`Menu` item).

`Item name` holds a value of type `text`: an `Item name` is a piece of text.

`Selling price` holds a value of type **number**. The meaning of the number is expressed as well: `euro`. A `Selling price` is a number representing a euro amount.

`Menu`, `Item name`, and `Selling Price` are **attributes** of a node. The keywords *collection*, *text* and *number* in a model express the **types** of the attributes. An *attribute type* specifies what kind of data an attribute can hold.

<!-- >Curly braces ( ***{ ... }*** ) describe the start and end of a **node type** definition. A *node type* defines the types of data and its structure in a node. -->

![node](./images_model/000A.png)

![node type](./images_model/000B.png)

## The minimal model
Let's make an app from the `Menu` model.
For that we need the following code in our `./models/model/application.alan` file.
Let's open it up, and put down the following code that describes the main sections of an `application` model:
```js
users
	anonymous

interfaces

root { }

numerical-types
```

This is the ***minimal model*** that is needed for every application that you build on the Alan platform.

The `users` section defines who can access your application and how.
We use `anonymous` for now, which means that anyone can access your app and read and edit the app data.
In the [application language documentation](/pages/docs/model/89/application/grammar.html) you can find more details about the `users` section.

The `interfaces` section defines what other apps and/or databases this app is connected with.
For now we stay 'disconnected' from other apps and databases.

The `root { }` section defines the *root node type*, as you can guess by the curly braces.
This is where you start modeling your application: a single `root` node holds all application data.
Paste the `Menu` model that we created earlier, between the braces.

The `numerical-types` section defines which units are used in your application and how to interpret them.
We use `'euro'` as the unit for the `Selling price` of a `Menu` item, so let's add `'euro'` to the numerical types.

Our model should now look like this:
```js
users
	anonymous

interfaces

root {
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'euro'
	}
}

numerical-types
	'euro'
```

By the way, when you type Alan code, make sure to use **whitespace between keywords**, and **tabs for indentation**!
Otherwise, the compiler will start complaining.

## Deploying the app
How to get this app up and running? The model needs to be processed to produce executable code for a server.
This is done by a ***compiler*** that is part of the Alan platform tools.
You can download the platform tools by clicking `Alan Fetch` in VS Code, or by running `./alan fetch` from the commandline.
`Alan Fetch` uses the `versions.json` file in your project root to determine which versions of the tools are needed.

When `Alan Fetch` is done, you can ***build*** (compile) the application by clicking the button `Alan Build` or running `./alan build` from the commandline.
If everything is correct, the compiler shows no errors.
You can then run `Alan Deploy` to transform your project into an app, ready for you to be used.

When opening the app in a webbrowser (we assume you use a chromium-based browser) it should look like this when clicking `Menu` in the left column:

![first app](./images_model/001.png)

The data from the menu is already there. You can add some data yourself by clicking `Add`. A new window opens.
Fill in the required fields, and click `Save` and `Close` (top right corner) when you're done.
That will bring you back to the `Menu` table, where you can `Add` more data and modify existing `Menu` items.

> <tutorial folder: `./_tutorial/step_01/`>

## Numerical-types
Maybe you've noticed that when you enter a number with decimals, the price is rounded to a whole number:
![wrong numbers](./images_model/002.png)

That is because internally, Alan only stores whole numbers.
You have to use a numerical type that describes the accuracy that you want.
Then you can tweak the GUI such that decimals work as well.

Go back to your model, change `euro` at the `Selling price` to `eurocent`, and make sure your `numerical-types` section looks like this:
```js
numerical-types
	'eurocent'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
```

The `@numerical-type:` part is a GUI annotation; an instruction for the graphical user interface of your app.
We can specify the label that we want to see if we want it to be different from the label of the numerical-type (here `Euro` instead of `eurocent`).
Furthermore, we can specify the number of decimals that the user can enter: 2 as the accuracy is `eurocent`.
There's much more to numerical-types, but we'll leave it at this for now.

## Stategroups
For our `Menu` items, we want our application to store some additional information.
For example, we want to store if an item is a dish or a beverage.
For that, we add an `Item type` to our model:
```js
root {
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'eurocent'
		'Item type': stategroup (
			'Dish' { }
			'Beverage' { }
		)
	}
}
```
An `Item type` is a stategroup atttribute, which holds a choice between states: `Dish` or `Beverage`.
Notice that you can specify attributes specific to `Dish` and `Beverage` in your model between the curly braces.
So, depending on the state that a user chooses, different data will be stored.

For example, a dish can be an appitizer, main course, or dessert.
This again is a choice, so let's make the states available by adding the attribute `Dish type` of type `stategroup` to the state type `Dish`.
In addition, let's do something similar for `Beverages`, such that we can neatly organize menu items in our application:
```js
root {
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'eurocent'
		'Item type': stategroup (
			'Dish' {
				'Dish type': stategroup (
					'Appetizer' { }
					'Main course' { }
					'Dessert' { }
				)
			}
			'Beverage' {
				'Beverage type': stategroup (
					'Juice' { }
					'Soft drink' { }
					'Cocktail' { }
					'Beer' { }
					'Wine' { }
					'Coffee & tea' { }
			}
		)
	}
}
```

Alan `application` models are hierarchical models specifying a hierarchical dataset: the `root` node holds a collection of `Menu` items.
Each `Menu` item (a node) has an `Item type` which can be `Dish` or `Beverage`.
`Dish` and `Beverage` are nodes which hold a `Dish type` and `Beverage type`, respectively.
The value of `Dish type` can be `Appetizer`, `Main course`, `Dessert`.
Similarly the `Beverage type` can be `Juice` or one of the other possible states that the model specifies.

Build the model (`Alan Build`) and find out what stategroups and numerical-types do for your app:

![added states](./images_model/003.png)

The table now has a few more columns.
If you add an item yourself you'll see radio buttons and a drop-down for choosing states for the added stategroup attributes:
![selection boxes](./images_model/004.png)

> You may notice that data you entered yourself in a previous step is gone!
In a real world situation you of course want to keep your data.
For that, you have to migrate it from the running application version to the next.
For this tutorial we provide migration files for each topic, that you can find in the `_tutorial` folder.
You have to copy the `migration.alan` for the step that you are working on, to `migrations\initialization\migration.alan` before deploying your app.
<!-- More information on migrations can be found in the tutorial *Migrations and deployments*. -->

> <tutorial folder: `./_tutorial/step_02/`>

## Built-in attribute types
Our restaurant is more than just a menu. We also have `Tables`; let's express that in our model:
```js
root {
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'eurocent'
		'Item type': stategroup (
			'Dish' {
				'Dish type': stategroup (
					'Appetizer' { }
					'Main course' { }
					'Dessert' { }
				)
			}
			'Beverage' {
				'Beverage type': stategroup (
					'Juice' { }
					'Soft drink' { }
					'Cocktail' { }
					'Beer' { }
					'Wine' { }
					'Coffee & tea' { }
			}
		)
	}

	'Tables': collection ['Table number'] {
		'Table number': text
		'Seatings': number 'chairs'
		'Orders': collection ['Order line'] {
			'Order line': text
			'Item': text -> ^ ^ .'Menu'[]
			'Amount': number 'units'
		}
	}

}
```

Don't forget to add `chairs` and `units` to the `numerical-types`, as these numerical types are new to the model:
```js
numerical-types
	'eurocent'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
```

Deploy and check the app in your browser: click `Tables` in the left menu bar. `Table number`'s and corresponding `Seatings` are already there:

![tables](./images_model/005.png)

In the left column we see that `Tables` is parent to the child `Orders`, just like in our model:
 we have specified a collection attribute `Tables` that nests a collection attribute `Orders`.
This means that in the app, each `Tables` item can have its own collection of `Orders`.

> <tutorial folder: `./_tutorial/step_03/`>

### Overview of attribute types
{:.no_toc}
The application language supports the following built-in attribute types:
>- A ***text*** attribute holds an unbounded string value (eg. *"this is text"*)
>- A ***number*** attribute holds an integer value (eg. *31415927*)
>- A ***file*** attribute holds two unbounded string values representing a file token and a file extension (eg. *"screenshot"* and *"png"*)
>- A ***collection*** attribute holds a map of key-value pairs. Keys are string values that have to be unique such that we can reference them unambiguously. Keys are implicitly defined for collection attributes; values are nodes of an inline defined type (eg. *{"001"; "Eggs"; 6; 'stired', 'fried'; 'omelette.jpg'}*)
>- A ***stategroup*** attribute holds a value indicating a state. States are alternatives to a property that a state group attribute indicates, such as `'Main course'`.
>- A ***group*** attribute holds a node of an inline defined node type. Group attributes add structure by grouping other attributes that belong together or share permission requirements, which we'll discuss later in this tutorial.

## References
There's an interesting line in the model that needs our attention:
```js
'Item': text -> ^ ^ .'Menu'[]
```
This line says that an `Item` on an order from a table refers to a `Menu` item.
First, let's see what this means for our application.

Click on `Tables` on the left hand side.
Click on a table from the list (shown in the previous image) and then click the **Add** button next to `Orders`:

![table number](./images_model/006.png)

Enter an `Order line`, like "01" since its the first order from this table:

![order line](./images_model/007.png)

Now, click the magnifying glass next to the field for `Item` and you'll see this:

![menu items](./images_model/008.png)

Here we see the items from the `Menu` and we can choose an item from the table.
Or, if we start typing in the box `Item name`, the table will be filtered.
We can only choose an item that is in the table.
When we click an item, the `Item name` from the item we clicked will be placed in the text field.

![beef stew](./images_model/009.png)

As explained above, the `Item name` is the key value of the `Menu` item.
It uniquely identifies a `Menu` item, and we can therefore use it to unambiguously reference an item.
With the lock-symbol you can now follow the reference from `Beef stew` to the actual `Menu` item.

Notice that the field for `Item` must contain the `Item name` of a `Menu` item such as `Beef stew`.
Other values are not accepted by your application.
This is because in our model, we have used this arrow keyword `->`, which is for **mandatory** references (also: constraints).

The navigation expression that follows the `->` in the model, expresses how the application can find the collection holding `Menu` items.
The keyword `^` tells the application to go to the parent node.
For an `Orders` item "01" (a node), the parent node is a `Tables` item "T01" (which is also a node).
Then we have another `^`, so the application knows that another parent step is required: from the `Tables` item to the `root` node. The `root` node holds the `Menu` items.
To instruct the application to look in that collection, the expression concludes with `.'Menu'[]`.
Which means: look up the `Item` value in the `Menu` collection.

In a model you can just count opening curly braces (`{`) above an expression to see where a series of `^` leads to, as each curly brace corresponds to a node in your application when navigating from a child node to a parent node:
```js
root {
	'Tables': collection ['Table number'] {   // curly brace 2 (match second ^)
		'Orders': collection ['Order line'] { // curly brace 1 (match first ^)
			'Item': text -> ^ ^ .'Menu'[]
...
```

> **In summary**, the expression states that `Item` is a text value and references a `Menu` item. Therefore, the text value of an item has to equal the `Item name` (key value) of a `Menu` item.

---

Entering an amount and clicking `Save` gives this result:

![first order line](./images_model/010.png)

Sometimes you may want references to be *optional* rather than *mandatory*.
When you import data from other apps this is necessary, as you can typically not force those apps to respect your wishes concerning your text values.
For **optional references**, you use the keyword **~>** (tilde arrow) instead of **->** (dash arrow).

The specification of an attribute with a reference, can be extended with `where`-rules for creating additional references.
This is especially useful when an application combines data from multiple different sources.
For example, suppose for a second that our application imports a menu from two other restaurants: `Blue` and `Red`. We can request a menu `Item` from the other restaurants in case we ever run out of stock:
```js
'Item': text -> .'Menu'[]
	where 'blue' ~> .'Menu from restaurant Blue'[]
	where 'red' ~> .'Menu from restaurant Red'[]
```

`Item` has one *mandatory* reference to our own `Menu` and two *optional* references to the `Menu`'s from restaurant `Blue` and `Red`.

<sup>NOTE: in `application` language `where`-rules that require a lookup in a collection can currently not be mandatory; only the main reference (expressed by `-> .'Menu'[]` can be mandatory. Support may be added in future versions.</sup>

The `where`-rules can also be used for states of a `stategroup` attribute. More on this in the topic [Advanced references](#advanced-references).


## Rewrite 1: states versus references
Hopefully by now you can 'read' this model and understand its components and structure.
Meanwhile our restaurant is in full swing, so no time to waste!

You may have noticed in your restaurant that having a fixed set of beverage types is not practical.
Let's change the model accordingly and make a dynamic set of beverage types, which means the stategroup `Beverage type` is removed and replaced with a collection `Beverages types`.

Since we still want to be able to select a beverage type when we compose our menu, we need to be able to reference `Beverages types` from `Beverage type` within the state `Beverage` in our model. Therefore it needs to be above `Menu`. Modify your model according to this new one:
```js
users
	anonymous

interfaces

root {
	'Beverages types': collection ['Beverage type'] {
		'Beverage type': text
	}

	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'eurocent'
		'Item type': stategroup (
			'Dish' {
				'Dish type': stategroup (
					'Appetizer' { }
					'Main course' { }
					'Dessert' { }
				)
			}
			'Beverage' {
				'Beverage type': text -> ^ ^ .'Beverages types'[]
			}
		)
	}

	'Tables': collection ['Table number'] {
		'Table number': text
		'Seatings': number 'chairs'
		'Orders': collection ['Order line'] {
			'Order line': text
			'Item': text -> ^ ^ .'Menu'[]
			'Amount': number 'units'
		}
	}
}

numerical-types
	'eurocent'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
```

Again, build and check your app, selecting `Beverages types` from the left menu bar:
![beverages types collection](./images_model/011.png)

Now you are free to add or adjust the types of beverages you have in your restaurant and still be able to use those in your menu setup:

![similar menu layout](./images_model/012.png)

Select 'Mojito', then `Edit` (top right):

![mojito](./images_model/013.png)

And finally the magnifying glass on the right of `Beverage type`:

![edit beverage type](./images_model/014.png)

Here, we can edit the `Beverage type` of 'Mojito'. The collection `Beverages types` is shown just like before with `Orders`. This *graphical user interface* ***(GUI)*** is also automatically updated just by changing our model.

> <tutorial folder: `./_tutorial/step_04/`>

## Reference sets
You decided that your restaurant will also provide a take-away service. This means adjusting the model accordingly. Let's see what is needed.

`Orders` will no longer be a child to the parent `Tables`, which makes more sense anyway: If we consider these entities more accurately, `Orders` and `Tables` don't have a parent-child relation, since they are of different order. For example the relation between `Tables` and `Seatings` is more natural, like wheels to a car or zebras to mammals.
`Orders` need to be defined as either takeaway or in-house. And if in-house, it can be linked to a table.
We will change this part of the model:
```js
'Tables': collection ['Table number'] {
	'Table number': text
	'Seatings': number 'chairs'
	'Orders': collection ['Order line'] {
		'Order line': text
		'Item': text -> ^ ^ .'Menu'[]
		'Amount': number 'units'
	}
}
```

Into this:
```js
'Tables': collection ['Table number'] {
	'Table number': text
	'Seatings': number 'chairs'
	'Orders': reference-set -> downstream ^ .'Orders'* .'Order type'?'In-house' = inverse >'Table'
}

'Orders': collection ['Order'] {
	'Order': text
	'Order type': stategroup (
		'Takeaway' { }
		'In-house' {
			'Table': text -> ^ ^ .'Tables'[] -< 'Orders'
		}
	)
	'Order lines': collection ['Order line'] {
		'Order line': text
		'Item': text -> ^ ^ .'Menu'[]
		'Amount': number 'units'
	}
}
```

What changed?
- We moved `Orders` one level up, alongside `Tables`
- Since we don't want a long list of `Order lines`, we organized the `Order lines` in a subcollection `Order lines` . Now each `Order` can have multiple `Order lines` (previously each `Table number` could have multiple `Order lines`)
- We've added a stategroup `Order type` to indicate the kind of order: state `Takeaway` or state `In-house`
- If the state of an orde is `In-house` we also like to know which `Table` it belongs to, so we added a text `Table` that references the collection `Tables` inside the node of state `In-house`

And now for the interestingly new parts:
We would also like to know for each `Table` which `Orders` it has. So far we could only know for each `Order` which `Table` it is for, by means of the reference on `Table` (by the way, did you check if two ^ are correct here?). The ***reference set*** makes it possible to know which `Orders` are pointing to each `Table`, so for each `Table` we can have insight into its `Orders`.
We achieve this by adding `Orders` to the collection `Tables` and define it as type reference set. Then we have to make the reference to the desired location by supplying the path: `-> downstream ^ .'Orders'* .'Order type'?'In-house'` This is called a *relative node type path*:
- It's relative since we start from our current position and first have to jump up one level (`^`) and then follow the node types
- It's a node type path since it descibes a path of consecutive node types on ever deeper levels: `.'Order type'?'In-house'` within `.'Orders'*`

`Downstream` tells us the node type the compiler needs to find is further down in the model. More on `downstream` in the topic 'Upstream and downstream'.
Here we use * instead of [ ] behind `.'Orders'` because we want to reference *all* the nodes (not a single node) of `Orders` that have the state `In-house`.
Finally we say 'follow the reference of `Table`', written like this: `>'Table'` (more on the symbol > in the topic 'Navigation'), but do it 'backwards' (`inverse`). If we 'jump' to `Table` we see a kind of inverse reference `-<` (instead of `->`) at the end of the line with label `Orders`. This links `Table` from collection `Orders` to `Orders` from collection `Tables`.

Make the changes to your model, build it and take a look at the app.
Select `Order` in the left column and click `Add`:

![order](./images_model/015.png)

Insert '001' as order number, select 'In-house' and select a table. Add some order lines:

![order lines](./images_model/016.png)

Hit `Save`!
Now go to `Tables`, select the table you selected when placing the order and click `Usages`:

![usages](./images_model/017.png)

We can see that `Order` '001' is using table 'T03':

![table used](./images_model/018.png)

If we click the order, we jump to the order with its order lines.

> <tutorial folder: `./_tutorial/step_04a/`>

## Commands

At this point in the tutorial we would like to show you the ***command*** statement. The model however doesn't necessarily need a command, therefore the example presented here is not the best usecase. Nevertheless it will give a glimpse into the structure of a command.
With a command we can for example create nodes in a collection, provided the data is available to create the node. Having this data is achieved by deriving it from other data (more on derivations later), receiving data through an interface or ask the user to enter data. Although commonly an ***action*** is used in the later case (an action takes into account the access rights a user has, while a command does not), we will use this scenario here.

In short, in our model we will add a command to gather data for placing a new order by means of a user form and then use this data to update the collection `Orders`:

```js
'Place new order': command {
	'Provide an order number': text
	'Where is the meal consumed?': stategroup (
		'Outside of restaurant' { }
		'At the restaurant' {
			'Where is the customer seated?': text -> .'Tables'[]
		}
	)
	'Order lines': collection ['Provide an order line number'] {
		'Provide an order line number': text
		'Item to be consumed': text -> .'Menu'[]
		'Amount of this item': number 'units'
	}
} => update .'Orders' = create (
	'Order' = @ .'Provide an order number'
	'Order type' = switch @ .'Where is the meal consumed?' (
		|'Outside of restaurant' => create 'Takeaway' ( )
		|'At the restaurant' as $ => create 'In-house' (
			'Table' = $ .'Where is the customer seated?'
		)
	)
	'Order lines' = walk @ .'Order lines' as $ (
		create (
			'Order line' = $ .'Provide an order line number'
			'Item' = $ .'Item to be consumed'
			'Amount' = $ .'Amount of this item'
		)
	)
)
```

That's a lot to take in! Let's take a look at the result in the webbrowser. So, add this to the model, below `Orders`, but within `root`. Build the app and go to your browser. In the left column a button 'Place new order...' appeared:

![command](./images_model/019.png)

This button's title corresponds with the label of our command: `Place new order`
Click it and fill in the fields, for example like this:

![form filled](./images_model/020.png)

Now click `Place new order` below the form en `Close` (top right). Then go to `Orders` and select your order:

![added order](./images_model/021.png)

We have successfully added an entry to the collection `Order` by providing the data in the form.
On closer inspection of this example we can see that the selection `At the restaurant` for the question `Where is the meal consumed?` is translated into the state `In-house` of stategroup `Order type`.

Let's review the added command in the model. The first part of the command looks a lot like familiar model language and actually is similar:
```js
'Place new order': command {
	'Provide an order number': text
	'Where is the meal consumed?': stategroup (
		'Outside of restaurant' { }
		'At the restaurant' {
			'Where is the customer seated?': text -> .'Tables'[]
		}
	)
	'Order lines': collection ['Provide an order line number'] {
		'Provide an order line number': text
		'Item to be consumed': text -> .'Menu'[]
		'Amount of this item': number 'units'
	}
} ...
```
It defines the command by providing containers in between curly braces (just like when defining a collection) that can hold specific data types. Some containers also have reference constraints to control the allowable values. These references have paths starting at the node type where the command is placed, in this case `root`. So the reference constraint of `'Where is the customer seated?'` starts at `root`. Don't be fooled by this: It still is a relative node type path, but from the node type that contains the command!
To illustrate this more clearly, let's temporarily add the command to a group `Temporary` and see how this effects the paths:
```js
'Temporary': group {
	'Place new order': command {
		'Provide an order number': text
		'Where is the meal consumed?': stategroup (
			'Outside of restaurant' { }
			'At the restaurant' {
				'Where is the customer seated?': text -> ^ .'Management' .'Tables'[]  // ^ added!!
			}
		)
		'Order lines': collection ['Provide an order line number'] {
			'Provide an order line number': text
			'Item to be consumed': text -> ^ .'Menu'[]             // ^ added!!
			'Amount of this item': number 'units'
		}
		'Apply discount?': stategroup (
			'Yes' {
				'Discount period': text -> ^ .'Management' .'Discount periods'[]  // ^ added!!
			}
			'No' { }
		)
	} => update ^ .'Orders' = create (                // ^ added!!
		'Order' = @ .'Provide an order number'
		'Order type' = switch @ .'Where is the meal consumed?' (
			|'Outside of restaurant' => create 'Takeaway' ( )
			|'At the restaurant' as $ => create 'In-house' (
				'Table' = $ .'Where is the customer seated?'
			)
		)
		'Order lines' = walk @ .'Order lines' as $ (
			create (
				'Order line' = $ .'Provide an order line number'
				'Item' = $ .'Item to be consumed'
				'Amount' = $ .'Amount of this item'
				'Line status' = create 'Placed' ( )
			)
		)
		'Order status' = create 'Open' ( )
		'Discount applicable' = switch @ .'Apply discount?' (
			|'Yes' as $ => create 'Yes' (
				'Discount period' = $ .'Discount period'
			)
			|'No' => create 'No' ( )
		)
	)
}
```
This change makes it necessary to add `^` to the paths, as indicated in the four comment lines, and shows that the paths are relative, but from the node type where the command is defined, in this case the node type `Temporary`.
Please revert the model to the original state to undo this example.

All these containers are called the ***parameters*** of the command.
Although the labels are different, the structure of the command definition is the same as the collection `Orders`. In this case we want to manipulate this collection with the command and often the command definition is identical to the definition of that collection.
The parameters (containers within the command definition) correspond with the fields in the GUI-form to be filled in and thus hold the inserted values after submitting the form.
The values of the parameters together form a ***parameter node*** that can be accessed.

Then the second part of the command, the *command implementation* starts with:
```js
... => update .'Orders' ...
```
It consists of a double arrow ( ***=>*** ), the word ***update*** and a (relative!) node type path. The double arrow can be read as 'do this'. Update means we want to update a collection or stategroup. And the path points to the collection or stategroup we want to update with the provided data, in this case collection `Orders`.
Instead of update we can also use these key words: *switch*, *ignore*, *walk*, *execute* and *external*, each with their own definition and required structure that should follow the key word. Let's stick with update for now, since we want to update the specified collection with the provided data, but just so you know there are many more possibilities.

The command implementation ends with:
```js
			... = create ( ... )
```
This tells us what the update should be about: 'the update is ( ***=*** ) the creation (***create***) of a node.
The key word *create* can be replaced by only the key word ***ensure***. Create will check if an entry in the target collection already exists (if there is a node that is similar to the values the user filled in). If so, an error will be thrown and the command will be aborted. Otherwise, the new node is created.
Ensure will also create the node, but if it already existed it will overwrite its data.

And lastly, the part between the parentheses of the key word *create*:
```js
'Order' = @ .'Provide an order number'
'Order type' = switch @ .'Where is the meal consumed?' (
	|'Outside of restaurant' => create 'Takeaway' ( )
	|'At the restaurant' as $ => create 'In-house' (
		'Table' = $ .'Where is the customer seated?'
	)
)
'Order lines' = walk @ .'Order lines' as $ (
	create (
		'Order line' = $ .'Provide an order line number'
		'Item' = $ .'Item to be consumed'
		'Amount' = $ .'Amount of this item'
	)
)
```
The containers `Order`, `Order type` and `Order lines` within the collection `Orders` are equated with a parameter defined in the command, much like this:
```js
'container in collection' = @ .'parameter of command'
```
This means access the parameter node, lookup the specified value (inserted in the form by the user) and copy it to the container of the collection. The symbol ***@*** is used here to tell the compiler a given path is within the command definition. Otherwise the compiler will consider these paths as within `root`.
As an experiment to show you how the compiler responds without this symbol, remove the @ in this line: `'Order' = @ .'Provide an order number'` and build the model. The compiler will throw an error telling you it can't find `Provide an order numer` in 'attributes' and will show what it does find in 'attributes', in this case `root`.

Additionally, we see two new key words: ***switch*** and ***walk***. Let's discuss switch:
```js
'Order type' = switch @ .'Where is the meal consumed?' (
	|'Outside of restaurant' => create 'Takeaway' ( )
	|'At the restaurant' as $ => create 'In-house' ( ... )
)
```
Since we don't know which selection the user has made we need a way to link al possible states of the input (parameter) stategroup with all possible states of the output stategroup. The statement switch expresses that, depending on the state of the stategroup `Where is the meal consumed?`, we want to switch between possible states of `Order type`.
You can read it like this:
***"*** If the state of `Where is the meal consumed?` is `Outside of restaurant`, then 'do this': create the state `Takeaway` for stategroup `Order type`. If the state of `Where is the meal consumed?` is `At the restaurant`, then 'do this': create the state `In-house` for stategroup `Order type`. ***"***

It doesn't end there, because if the customer wants to eat at the restaurant we need to know at what table the customer is seated. The meaning of:
```js
	|'At the restaurant' as $ ...
```
is to say: Temporarily store the contents of the parameter node of the state 'At the restaurant' as $. The ***\$-symbol*** is like a sticky note with all the values within the node written down on it. The node type of this state ({...}) is defined in the command definition as:
```js
'At the restaurant' {
	'Where is the customer seated?': text -> .'Management' .'Tables'[]
}
```
With `$` we thus have access to the value of `Where is the customer seated?`.

Then when the state `In-house` is created we have to fill the node by providing the value for `Table`:
```js
=> create 'In-house' (
		'Table' = $ .'Where is the customer seated?'
	)
```
Here we refer to the temporarily stored node of state `At the restaurant` as `$` and of that node we refer to the (one and only) container `Where is the customer seated?` (Look at the sticky note and provide the value of `Where is the customer seated?`).
Next time we use the command to create a new order, these values can be different, therefore we only need to store these values temporarily. The goal of our command is to permanently store these values in a new node in the collection `Orders`.

Let's look at walk:
```js
'Order lines' = walk @ .'Order lines' as $ (
	create ( ... )
)
```
The statement walk, followed by the node type path, expresses that we want to 'walk along' all entries in the parameter collection `Order lines`. The statements between the parentheses are evaluated for each of the entries in the collection. In this case for each entry in the parameter collection `Order lines` a node is created in the collection `Order lines` according to the supplied structure and values.
Again, the $-symbol is used to temporarily store each node within the collection `Order lines`.
So once we start to create the node in the collection `Order lines`, we derive the values for each container within the node by refering to \$ and from this \$ we want a specific container.
```js
		'Order line' = $ .'Provide an order line number'
		'Item' = $ .'Item to be consumed'
		'Amount' = $ .'Amount of this item'
```

The use of the $-symbol is not restricted to commands and can be applied throughout a model to refer to temporarily stored nodes or states.

As mentioned before, this is only an example of a command. Commands are commonly used to automatically create or change nodes or states without bothering the user with this or to transmit data from one app to another through an interface. More on the use of commands in interfaces in the tutorial 'Interfaces'.

> <tutorial folder: `./_tutorial/step_04b/`>

>Before we continu with the next topic it is good to know that *reference-set* and *command* are also considered possible *attributes* for a container. The previously mentioned types *text*, *number*, *file*, *collection*, *stategroup* and *group* are more specifically *property attributes*, in short ***properties***, of the container. This in contrast to the *attributes* *reference-set* and *command*.

## Derivations: numbers
Our customers in the restaurant have to pay us, and for that we need to compute the cost of their orders.
Let's start with the `Line total`: the cost of a single `Order line`:
```js
'Order lines': collection ['Order line'] {
	'Order line': text
	'Item': text -> ^ ^ .'Menu'[]
	'Amount': number 'units'
	'Line total': number 'eurocent' = product (
		>'Item'.'Selling price' as 'eurocent' ,
		.'Amount'
	)
}
```
Notice that after `eurocent` for the `Line total` we have have written a formula for deriving the value.
A derived value (derivation) `Line total` is computed by multiplying the `Selling price` with the `Amount`.

>An important concept arises when we focus on the symbol ***>*** in front of `Item` (the first term in the *product* statement for calculating `Line total`). This line of code means:
'With the current value of `Item` (a key value of `Menu`) of this specific `Order line` follow its reference and from the resulting node in that referenced collection provide the value of property `Selling price`.'
>So, from a specific node of `Order lines`, that has a specific value for `Item`, a reference is made to another specific node of `Menu` from which the value of the property `Selling price` is provided.
>In short, *>* makes sure that during runtime the current value of `Item` is used to reference the appropriate node of the referenced collection.

Now we want to focus on the ***as*** statement followed by `'eurocent'`.
To explain what this means and for the health of our model we need to add this line:
`= 'eurocent' * 'units'` below `euro` so our numerical-types now looks like this:
```js
numerical-types
	'eurocent'
	= 'eurocent' * 'units'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
```
The *as* statement is followed by what is called a ***product conversion rule***, that describes how the numerical-types of the two properties are multiplied, in this case `euro` and `unit`. So the general format of a *product conversion rule* is `= 'num-type1' * 'num-type2'`.

Another possible calculation is for example a division:
`= division ( 'property1' as 'division conversion rule' , 'property2' )`
that uses a ***division conversion rule***:
`= 'num-type1' / 'num-type2'`

And we can do conversion of units by a constant factor, using the ***from*** statement, for example:
`'Circle circumference': number 'circum' = from 'diameter' .'Circle diameter'`
And a ***singular conversion rule***:
`= 'num-typ' * constant`, according to the example:
```js
numerical-types
	'circum'
	= 'diameter' * 314159265 * 10 ^ -8	// = diameter * pi
```

Let's add another useful line to the model:
```js
'Total': number 'eurocent' = sum .'Order lines'* .'Line total'
```

Can you determine where it needs to go? Spoiler alert: answer ahead...

So now our whole model looks like this:
```js
users
	anonymous

interfaces

root {
	'Beverages types': collection ['Beverage type'] {
		'Beverage type': text
	}

	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'eurocent'
		'Item type': stategroup (
			'Dish' {
				'Dish type': stategroup (
					'Appetizer' { }
					'Main course' { }
					'Dessert' { }
				)
			}
			'Beverage' {
				'Beverage type': text -> ^ ^ .'Beverages types'[]
			}
		)
	}

	'Tables': collection ['Table number'] {
		'Table number': text
		'Seatings': number 'chairs'
		'Orders': reference-set -> downstream ^ .'Orders'* .'Order type'?'In-house' = inverse >'Table'
	}

	'Orders': collection ['Order'] {
		'Order': text
		'Order type': stategroup (
			'Takeaway' { }
			'In-house' {
				'Table': text -> ^ ^ .'Tables'[] -< 'Orders'
			}
		)
		'Order lines': collection ['Order line'] {
			'Order line': text
			'Item': text -> ^ ^ .'Menu'[]
			'Amount': number 'units'
			'Line total': number 'eurocent' = product (
				>'Item'.'Selling price' as 'eurocent' ,
				.'Amount'
			)
		}
		'Total': number 'eurocent' = sum .'Order lines'* .'Line total' // <-- ;-)
	}

	'Place new order': command {
		'Provide an order number': text
		'Where is the meal consumed?': stategroup (
			'Outside of restaurant' { }
			'At the restaurant' {
				'Where is the customer seated?': text -> .'Tables'[]
			}
		)
		'Order lines': collection ['Provide an order line number'] {
			'Provide an order line number': text
			'Item to be consumed': text -> .'Menu'[]
			'Amount of this item': number 'units'
		}
	} => update .'Orders' = create (
		'Order' = @ .'Provide an order number'
		'Order type' = switch @ .'Where is the meal consumed?' (
			|'Outside of restaurant' => create 'Takeaway' ( )
			|'At the restaurant' as $ => create 'In-house' (
				'Table' = $ .'Where is the customer seated?'
			)
		)
		'Order lines' = walk @ .'Order lines' as $ (
			create (
				'Order line' = $ .'Provide an order line number'
				'Item' = $ .'Item to be consumed'
				'Amount' = $ .'Amount of this item'
			)
		)
	)
}

numerical-types
	'eurocent'
	= 'eurocent' * 'units'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
```

And at runtime (in the webbrowser) it looks like this:
![(line totals and total](./images_model/022.png)

Other possible calculations that can be used in ***number derivations*** are:
`min`: determines the minimum of a set of values
`max`: determines the maximum of a set of values
`std`: determines the standard deviation of a set of values
`count`: counts the number of values in a set
`remainder`: calculates the remainder of a division (10 mod 3 = 1)
`division`: calculates the division of two numbers
`add`: calculates the addition of two numbers
`diff`: calculates the difference of two (relative!) numbers, for example the difference between two dates or two temperatures

Examples of absolute and relative numbers:
- (number of) days: absolute, "28 days"
- date: relative, "28-7-2021"
- years: absolute, "5 years"
- year: relative, "2021"
- degrees: absolute, "21 degrees"
- temperature: relative, "21˚C"
- seconds, minutes, hours: absolute, "2 hours, 35 minutes and 8 seconds" (duration)
- time of day or 'the time': relative "14:35:08"

So far we've seen number derivations, but we can also derive other types of data.

> <tutorial folder: `./_tutorial/step_04c/`>

## Rewrite 2: more derivations
To show examples of other types of derivation we need to create a more intricate model.
Let's create a group `Management` at the top of the model for more permanent data, while still being able to adjust it. This group contains a new collection `Discount periods`, a number `VAT percentage` and the existing collections `Beverages types` and `Tables` (we're not going to change this data on a daily basis):
```js
'Management': group {
	'Discount periods': collection ['Period'] {
		'Period': text
		'Percentage' : number 'percent'
		'Minimal spendings': number 'eurocent'
	}

	'VAT percentage': number 'percent'

	'Beverages types': collection ['Beverage type'] {
		'Beverage type': text
	}

	'Tables': collection ['Table number'] {
		'Table number': text
		'Seatings': number 'chairs'
		'Orders': reference-set -> downstream ^ ^ .'Orders'* .'Order type'?'In-house' = inverse >'Table'
	}
}
```
When you moved `Beverages types` and `Tables` to the group `Management` rebuild your app. You'll get some errors saying the compiler can't find these properties. Correct the errors according to the changes made.

And since we use a new numerical type, we need to add this to our `numerical-types` section in the model:
```js
'percent'
```
We will use the collection `Discount periods` for discounts during different time periods, where the discount depends on the amount of money spent at the restaurant.
`VAT percentage` will be used for calculating the value added tax (VAT).

Rename the number property `Total` for `Orders` to `Subtotal`, because the new `Total` will take the appropriate discount into account:
```js
'Subtotal': number 'eurocent' = sum .'Order lines'* .'Line total'
```

> <tutorial folder: `./_tutorial/step_05/`>

## Derivations: conditional expressions

Now let's add a stategroup `Discount applicable`, also within `Orders`. These lines of code also show some more examples of the symbol **>** :
```js
'Discount applicable': stategroup (
	'Yes' {
		'Discount period': text -> ^ ^ .'Management' .'Discount periods'[]
		'Discount': number 'eurocent' = switch ^ .'Subtotal' compare ( >'Discount period' .'Minimal spendings' ) (
			| < => 0
			| >= => product (
				from 'percent' >'Discount period' .'Percentage' as 'percent-fraction',
				^ .'Subtotal'
			)
		)
		'Total': number 'eurocent' = sum ( ^ .'Subtotal' , - .'Discount' )
	}
	'No' {
		'Discount': number 'eurocent' = 0
		'Total': number 'eurocent' = ^ .'Subtotal'
	}
)
```
Add the numercial type `percent-fraction`, the product conversion rule and the singular conversion rule to the numerical types. It should now look like this:
```js
numerical-types
	'eurocent'
	= 'units' * 'eurocent'
	= 'percent-fraction' * 'eurocent'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
	'percent'
	'percent-fraction'
	= 'percent' / 1 * 10 ^ 2
```

In short, this model extension makes it possible to apply a discount by selecting a `Discount period` from the previously added collection `Discount periods`; for example 'Summer holiday' that will give 3% discount on spendings over €35.
If discount is applicable (state `Yes`) and a discount period is selected, the `Discount` will be calculated:
- Compare the `Subtotal` with the `Minimal spendings` that belong to the selected `Discount period`
- If `Subtotal` is smaller than `Minimal spendings` then `Discount` will be equal to 0
- If `Subtotal` is bigger than or equal to `Minimal spendings` then `Discount` will be equal to the product of the appropriate `Percentage` and `Subtotal`. The value of `Percentage` is first transformed from `percent` to `percent-fraction` (from 3% to 0,03). The value of `Subtotal` is this number of `percent-fraction` times number of `euro`. Its unit is equal to `euro`

Because we `switch` on a `compare` we can provide the desired states with operators like 'greater than', 'equal to', 'less than' and combinations of these.
Finally, the `Total` is calculated by adding `Subtotal` to the negative of `Discount` (subtraction).
If discount is not applicable (state`No`) `Discount` is equal to 0 and `Total` is equal to `Subtotal`.

Although the inputs and outcome are numbers, we also call this a ***state derivation*** because the result is determined from which state is true.

We also have to adjust the command `Place new order`, since this comand updates collection `Orders` and this collection has changed. Can you find out where these seperate parts of code should go and what they mean?:
```js
'Apply discount?': stategroup (
	'Yes' {
		'Discount period': text -> .'Management' .'Discount periods'[]
	}
	'No' { }
)
```

And:
```js
'Discount applicable' = switch @ .'Apply discount?' (
	|'Yes' as $ => create 'Yes' (
		'Discount period' = $ .'Discount period'
	)
	|'No' => create 'No' ( )
)
```
Let's take a look at the app and enter an order:
![discount](./images_model/023.png)
An order with a subtotal of €40,20 receives during the summer holiday a discount of 3%  when spending €35 or over.

It's time to calculate the VAT. To do this we need to know the `Total` and calculate a percentage of it. But we have two kinds of `Total` depending on whether a discount was applied or not. This means our calculation should depend on which state that specific `Total` is in. Again we can use the `switch` statement for this:
```js
'VAT': number 'eurocent' = switch .'Discount applicable' (
	|'Yes' as $'discount' => product (
		from 'percent' ^ .'Management' .'VAT percentage' as 'percent-fraction' ,
		$'discount' .'Total'
	)
	|'No' as $'no discount' => product (
		from 'percent' ^ .'Management' .'VAT percentage' as 'percent-fraction' ,
		$'no discount' .'Total'
	)
)
```

We define `VAT` as a `number` of numerical type `euro` and derive it (=) depending on the states of stategroup `Discount applicable` (switch): either `Yes` or `No`. In both cases we end up using the product statement and supply this with the appropriate terms. The interesting parts are where the \$-symbols are used. If we look back at our definition of the stategroup `Discount applicable` (at the start of this topic) we see that each state has a node type definition by providing properties and derivations within the curly braces: `'Yes' { ... }` and `'No' { ... }`.
As explained previously, when `as $` is used a specific node (all the values of that particular node of the specified state within a node of collection `Order`) is temporarily marked as `$`. Here we added a name to each specific temporary node and can reference these with \$'name'. We could have added names in the previous example as well, or leave them out here. It can be convenient to apply these names to differentiate them when several temporary nodes are needed and a model gets cluttered with \$'s. Although not necessary for the compiler, it is more readable for humans.
Here we've given the marked node the temporary name `discount` for nodes in the state `Yes` and `no discount` for nodes in the state `No`. So, when we write `$'discount' .'Total'` we point at the value of `Total` within a temporarily marked node of state `Yes`. And similar for `$'no discount'`.
`$'discount'` and `$'no discount'` are called ***named objects***.

Here's the result of our work:
![VAT](./images_model/024.png)

Derivations come in several forms and are powerful tools. We've shown you some examples, but want to provide an in depth overview in the *Derivations tutorial*.

> <tutorial folder: `./_tutorial/step_06/`>

## Upstream and downstream

As mentioned before, when we click `Alan Build` the compiler will compile the model into code that is executable for a computer. When models get really intricate, with lots of references and all kinds of derivations, the compiler builds code that supports calculations in an order that not neccesarily corresponds with the order in which we built our model.
At runtime applications perform calculations in four phases:
1. determining constraints while calculating top-to-bottom
2. determining constraints while calculating bottom-to-top
3. determining derivations while calculating top-to-bottom
4. determining derivations while calculating bottom-to-top

If at runtime a reference constraint can't be determined in the first phase because the referenced collection is below the point of reference, the compiler will throw an error during the build. We can bypass this by telling the compiler it will be possible to determine the reference in the second phase of calculations at runtime, when calculations are performed bottom-to-top. We use the statement ***downstream*** for this, since in our readable model the reference constraint points to a collection further down. From the perspective of the calculation it is as if the referenced collection is still 'before' the point of reference, since its calculating bottom-to-top.
The model can make use of either the statement ***upstream*** or downstream for each calculation phase:
- determining constraints phase 1: upstream
- determining constraints phase 2: downstream
- determining derivations phase 3: upstream
- determining derivations phase 4: downstream

To create an example without the need for building a very intricate model, let's change the model slightly. Move the `Menu` collection below the `Orders` collection. This disobeys the previously mentioned rule (in the topic 'Hierarchy') that collections referenced at some point in the model need to be above that point.
Build the model and the compiler will throw an error:
>order constraint violation. `Menu` needs to be a 'predecessors' entry in 'attributes'. Available 'predecessors':
	- `Management`

The error refers to this line, within the collection `Orders`:
```js
'Item': text -> ^ ^ .'Menu'[]
```

The compiler expected to find the referenced collection `Menu` above this point in the model. As we've learned just now we can bypass this error by adding the statement `downstream` like this:
```js
'Item': text -> downstream ^ ^ .'Menu'[]
```

Build the model again and you'll notice that the compiler is at ease with this. We've told the compiler to look for `Menu` further down in the model, in the second phase of calculations.

Please revert your model to the previous state, because this example is not good practice: For good readability of your model it is best to stick to the rule that whatever you would like to reference has to come first in your model.

In some situations we can't avoid needing `downstream`, for example as we've seen with the reference-set `Orders` in collection `Tables` (discusse in the topic 'Reference set'). There we need to add `downstream` to this reference-set to make the compiler find the referenced property `Table`, because `Table` needs to be below collection `Tables` to be able to reference it.

## Extensions and GUI annotations

In the topic 'Derivations: conditional expressions' we've calculated the number `Total` as part of the stategroup `Discount applicable`. In our app it is therefore shown inside a box along `Discount period` and `Discount`. Both visually and model-wise it's more appropriate to show and calculate `Total` outside of `Discount applicable`. Let's adjust the model accordingly. The last part for the `Orders` collection should look like this:
```js
'Orders': collection ['Order'] {
	...

	'Discount applicable': stategroup (
		'Yes' {
			'Discount period': text -> ^ ^ .'Management' .'Discount periods'[]
			'Discount': number 'eurocent' = switch ^ .'Subtotal' compare ( >'Discount period' .'Minimal spendings' ) (
				| < => 0
				| >= => product (
					from 'percent' >'Discount period' .'Percentage' as 'percent-fraction',
					^ .'Subtotal'
				)
			)
		}
		'No' {
			'Discount': number 'eurocent' = 0
		}
	)

	'Total': number 'eurocent' = switch .'Discount applicable' (
		|'Yes' as $'discount' => sum ( $'discount' ^ .'Subtotal' , - $'discount' .'Discount' )
		|'No' as $'no discount' => $'no discount' ^ .'Subtotal'
	)

	'VAT': number 'eurocent' = product (
		from 'percent' ^ .'Management' .'VAT percentage' as 'percent-fraction' ,
		.'Total'
	)
}
```
Instead of `VAT` using a state switch now `Total` switches on the state of `Discount applicable`.

Working towards the processes of order preparation and service let's take this opportunity to also add the stategroups `Line status` and `Order status` within the collections `Order lines` and `Orders` respectively. The top part of collection `Orders` now is this:
```js
'Orders': collection ['Order'] {
	'Order': text
	'Order type': stategroup (
		'Takeaway' { }
		'In-house' {
			'Table': text -> ^ ^ .'Tables'[] -< 'Orders'
		}
	)
	'Order lines': collection ['Order line'] {
		'Order line': text
		'Item': text -> ^ ^ .'Menu'[]
		'Amount': number 'units'
		'Line total': number 'eurocent' = product (
			.'Amount' as 'units',
			>'Item'.'Selling price'
		)
		'Line status': stategroup (
			'On hold' { }
			'Placed' { }
			'Service' { }
			'Served' { }
		)
	}
	'Order status': stategroup (
		'Open' { }
		'Closed' { }
	)
	'Subtotal': number 'eurocent' = sum .'Order lines'* .'Line total'
	...
}
```

Customers sometimes change their mind while ordering, so we don't want to place evey order line immediately, but place all lines once everybody is happy. To support this process we've added `Line status`. It has these states:
- state `On hold` for when an order line is inserted but the customer might change his/her mind
- state `Placed` for an order line that is 'approved' and ready to be prepared
- state `Service` for when the order line is prepared and can be served to the customer
- state `Served` for an order line that is served to the customer

`Order status` has states `Open` after placing the first order, and `Closed` after payment of the bill. This brings us to the next adjustment: the command `Place new order`. We need to add the states corresponding to these stategroups when placing an new order:
```js
'Place new order': command {
	...
} => update .'Orders' = create (
	'Order' = @ .'Provide an order number'
	'Order type' = switch @ .'Where is the meal consumed?' (
		|'Outside of restaurant' => create 'Takeaway' ( )
		|'At the restaurant' as $ => create 'In-house' (
			'Table' = $ .'Where is the customer seated?'
		)
	)
	'Order lines' = walk @ .'Order lines' as $ (
		create (
			'Order line' = $ .'Provide an order line number'
			'Item' = $ .'Item to be consumed'
			'Amount' = $ .'Amount of this item'
			'Line status' = create 'Placed' ( )
		)
	)
	'Order status' = create 'Open' ( )
	'Discount applicable' = switch @ .'Apply discount?' (
		|'Yes' as $ => create 'Yes' (
			'Discount period' = $ .'Discount period'
		)
		|'No' => create 'No' ( )
	)
)
```

No new parameters need to be added to the command, but we have to create the states `Placed` and `Open` when executing this command. Both are not determined by input from the user (therefore not depending on a parameter), since the purpose of the command implies these states and can be statically determined.
Let's take a look at our app:
![Order and line status](./images_model/025.png)

Also add `@default: auto-increment` this to the existing lines within collection `Orders` and `Order lines` repectively:
```js
'Order': text @default: auto-increment

'Order line': text @default: auto-increment
```
This is called a ***GUI annotation*** and makes sure that when you add an order or order line it automatically creates a followup number for those keys. GUI annotations always have the symbol ***@*** as prefix. GUI annotations need a seperate topic to be described in full, so we won't elaborate on this right now. This just makes it easier to add orders and order lines for now.

Finally, let's create a group `Service` and add `Menu`, `Orders` and `Place new order` in it, to further streamline the model.

As you might have noticed it is easy to make adjustments to your model: Moving a block of code, adding a derivation or property, changing the layout and applying a GUI annotation. Finetuning your model is quite easy without losing the integrity of your data.

> <tutorial folder: `./_tutorial/step_07/`>


## State machines
In the previous topic we've added `Line status` but the different states do not have any effect yet. The order line status needs to change according to the process in our restaurant. In short the process looks like this: Service goes to a table, customers order their drinks and/or dishes and might change their minds, orders are placed to be prepared and finally, the orders are delivered to the table.
So, we want to change the state without accidentilly skip a state. Let's implement this:
```js
'Line status': stategroup (
	'On hold' {
		'Ready for preparation': command { } => update ^ .'Line status' = create 'Placed' ( )
	}
	'Placed' {
		'Ready for service': command { } => update ^ .'Line status' = create 'Service' ( )
	}
	'Service' {
		'Served': command { } => update ^ .'Line status' = create 'Served' ( )
	}
	'Served' { }
)
```
Each state got a command that can change the current state to the next one. Notice that these commands do not have a command definition, only a command implementation, because all we need here is a button.
Build the model and view it in your browser by going to 'Orders' and selecting order 001 (or input an order first):
![Place order line commands](./images_model/026.png)
Set the view to `Full`. This will reveil some extra columns with in the first column a button `Place order line` (if you inserted an order yourself you must have selected `On hold` as line state).
Click the button of an order line to place it and refresh the table `Order lines`. As you can see the button disappears from the column `Place order line` and a new one appears in the column `Ready for service`. Repeat for this button and see what happens.
If you can imagine that different people with different roles within the restaurant have access to specific parts of the model, you could organise who gets to push which button. This is possible by implementing `users` and their access rights, which will be discussed in another topic.
Now clicking each line individually can become a hassle, so let's create a command that can set all lines with state `On hold` within one order to `Placed`:
```js
'Place order lines': command { } => walk .'Order lines' as $'line' (
	switch $'line' .'Line status' (
		|'On hold' => update $'line' (
			'Line status' = create 'Placed' ( )
		)
		|'Placed' => ignore
		|'Service' => ignore
		|'Served' => ignore
	)
)
```

This command (again only a command implementation) is placed below `Order lines` within `Orders`. We see familiar and new words.
The command implementation shows a 'do this' (`=>`), followed this time by `walk` and a node type path to the collection `Order lines`, which means 'walk' along all the nodes of this collection. Each node in the collection is temporarily stored as `$'line'`. We want the app to check for each of these nodes the property `Line status` and perform a 'do this' depending on the state. If the state is `On hold` then we want to update that node by creating the state `Placed` for its property `Line status`. In any other case we want to ignore it and do nothing.
In short: Walk along all the nodes of collection `Order lines` and if the property `Line status` of a particular node is set to `On hold` update the node by changing the `Line status` to state `Placed`.
Build the model and view the result, again in `Orders` and selecting `001`:
![Place order lines command](./images_model/027.png)
Click the button and refresh `Order lines`. This command only affects lines with state `On hold`.

Then there is another process we want to support: When the customer leaves we want to make sure all order lines are served and the bill is paid, so we can close the order.
Add these new lines in the state `Open` of stategroup `Order status` and take a look at it:
```js
'Order status': stategroup (
	'Open' {
		'All served': stategroup = switch ^ .'Order lines'* .'Line status'?'On hold' (
			| nodes => 'No' ( )
			| none => switch ^ .'Order lines'* .'Line status'?'Placed' (
				| nodes => 'No' ( )
				| none => switch ^ .'Order lines'* .'Line status'?'Service' (
					| nodes => 'No' ( )
					| none => 'Yes' ( )
				)
			)
		) (
			'No' { }
			'Yes' {
				'Paid': command { } => update ^ ^ .'Order status' = create 'Closed' ( )
			}
		)
	}
	'Closed' { }
)
```
When the `Order status` is `Open` we want to check if all order lines are `Served` but we don't know how many order lines an order contains. By checking if any nodes within `Line status` exist with the states `On hold`, `Placed` or `Service` we can either confirm or deny that all order lines are served.
Important to notice that this line would switch on the state of `Line status`:
```js
switch .'Line status' ( ... )
```
While this line switches on whether nodes with status `On hold` exist or not:
```js
switch .'Order lines'* .'Line status'?'On hold' ( ... )
```
<sup>(For the purpose of comparison `^` is left out in this line)</sup>

This line says: Check all nodes (`*`) of `Order lines` for the state `On hold` of stategroup `Line status`. The result is either there are nodes with this state (`nodes`) or there are no nodes with this state (`none`). If the result is `none` we still want to check for the other states in the same way. Only if there are no nodes with the last state we can be sure all nodes are `Served`, because order lines can only have and must have at least one of these four states.
Once it is confirmed that all order lines are served (state `Yes`) we provide a button that can be clicked when the customer has paid the bill. This will change the state of `Order status` to `Closed`.
Check out the app:
![All served?](./images_model/028.png)
![All served!](./images_model/029.png)

> <tutorial folder: `./_tutorial/step_08/`>

## Advanced references
Before we get to the advaced part we add some more common lines to the model.
When food and drinks are prepared and ready for service, we would like to provide service with additional information, for example the priority of service (when food is hot it needs to be served asap) and the table to serve to. We will add this information in steps. Take a look at the overview Order lines, with the view set to `Full`:
![Overview order lines!](./images_model/030.png)
Add `Priority` to the state `Service` of stategroup `Line status`:
```js
'Service' {
	'Priority': stategroup = switch ^ >'Item' .'Item type' (
		|'Beverage' => 'Low' ( )
		|'Dish' as $'dish' => switch $'dish' .'Dish type' (
			|'Appetizer' => 'Medium' ( )
			|'Main course' => 'High' ( )
			|'Dessert' => 'Low' ( )
		)
	) (
		'Low' { }
		'Medium' { }
		'High' { }
	)
	'Served': command { } => update ^ .'Line status' = create 'Served' ( )
}
```
This looks similar to the previously defined state derivation of stategroup `All served` (within state `Open` of stategroup `Order status`), exept here we switch on the state of the stategroup, not whether a collection has nodes or not.
To not make the model too complicated at this point we simply say that desserts have a low priority (mainly cold food), appetizers a medium priority (could be warm food) and main courses a high priority (mainly warm food). Check out the extra column:
![Priority](./images_model/031.png)

Only if an order is of order type `In-house` we would like to show the table to serve to when it's ready to be served. To achieve this we have to look at the states of both stategroups `Order type` and `Line status`:
```js
'To serve': stategroup = switch ^ . 'Order type' (
	| 'Takeaway' => 'No' ( )
	| 'In-house' as $'in-house' => switch . 'Line status' (
		|'On hold' => 'No' ( )
		|'Placed' => 'No' ( )
		|'Service' => 'Yes' ( 'Table' = $'in-house' >'Table' )
		|'Served' => 'No' ( )
	)
) (
		'No' { }
		'Yes' {
			'Table': text -> ^ ^ ^ ^ .'Management' .'Tables'[] = parameter
		}
	)
```
This shows the table if `To serve` is `Yes`:
![To serve table](./images_model/032.png)
The main part again looks like structures we've seen before: The code has a state switches that switch on stategroups. The addition is between parenthesis. This is also known as a ***state parameter*** (similar to the command parameter) and with it we can supply a state with an additional piece of information from a node, in this case `Table`.
We temporarily stored the node of state `In-house` as `$'in-house'` and a few lines down in the model we want to follow the reference of `Table` within that node to appoint it to the state parameter `Table`. Then when we get to the state `Yes` we can derive the value of text property `Table` from the parameter, but first have to tell that this property is related to the collection `Tables` in group `Management` by providing a reference to it.
By providing this reference, as part of the definition of `Table`, we 'close the loop' and make sure that the value of the derivation can only be of the same collection `Tables` as the text property `Table`. The compiler will check this 'reference loop' during compilation and if we by accident referenced for example another collection `Tables` it will throw an error. This makes the Alan platform very stable, since we have to be very clear about what data we expect at which part in the model.

Let's say we would also like to show the priority when stategroup `To serve` has state `Yes`. We do this for explanatory purposes, because the model it creates is not clean and it will show the priority in the table twice, but the structure it will show is interesting and important.
To achieve this it is required to have access to the node of state `Service` of stategroup `Line status`. Therfore add `$'service'` to the state `Service` in the state switch of stategroup `To serve`:
```js
'To serve': stategroup = switch ^ . 'Order type' (
	| 'Takeaway' => 'No' ( )
	| 'In-house' as $'in-house' => switch . 'Line status' (
		|'On hold' => 'No' ( )
		|'Placed' => 'No' ( )
		|'Service' as $'service' => 'Yes' ( 'Table' = $'in-house' >'Table' )
		|'Served' => 'No' ( )
	)
) ( ... )
```
If we build the model like this the compiler will throw an error saying it can't find the named object `in-house`. We created another 'sticky note' `$'service'` on a lower level than the previous 'sticky note' `$'in-house'`. On this lower level the only reachable 'sticky note' is `$'service'`. It's like the 'sticky notes' are stacked and only the last one is visible. To get to a 'sticky note' defined on higher levels we need to jump up thos levels, but not like using the regular `^`, but by using `$^`. The temporarily stored nodes create a hierachy in itself.
Another thing to notice is that the names we gave to these temporarily stored nodes are only for human readability and have no meaning to the compiler. We could just as easily have used only `$`.
Applying this new knowledge creates this:
```js
'To serve': stategroup = switch ^ . 'Order type' (
	| 'Takeaway' => 'No' ( )
	| 'In-house' as $'in-house' => switch . 'Line status' (
		|'On hold' => 'No' ( )
		|'Placed' => 'No' ( )
		|'Service' as $'service' => 'Yes' ( 'Table' = $^ $'in-house' >'Table' ) // <--- !! $^
		|'Served' => 'No' ( )
	)
) ( ... )
```
Building the model now will show a problem, but it's only a warning, saying we didn't use `service`, so let's use it:
```js
'To serve': stategroup = switch ^ . 'Order type' (
	| 'Takeaway' => 'No' ( )
	| 'In-house' as $'in-house' => switch . 'Line status' (
		|'On hold' => 'No' ( )
		|'Placed' => 'No' ( )
		|'Service' as $'service' => 'Yes' where 'Service' = $'service' ( 'Table' = $^ $'in-house' >'Table' ) // <--- !! where ...
		|'Served' => 'No' ( )
	)
) (
		'No' { }
		'Yes' where 'Service' -> .'Line status'?'Service' {						// <--- !! where ...
			'Table': text -> ^ ^ ^ ^ .'Management' .'Tables'[] = parameter
		}
)
```
We've seen `where` being used before, but then applied to a text property and now applied to a state. It serves as a *reference rule* here as well and further defines the state `Yes` by adding the reference to a node of state `Service`.

If we 'zoom out' and look at the structure:
```js
'To serve': stategroup = switch ... (
	| ...
	| ... => switch ... (
		| ...
		| ...
		|'Service' as $'service' => 'Yes' where 'Service' = $'service' ( ... )
		...
	)
) (
		...
		'Yes' where 'Service' -> .'Line status'?'Service' {
			...
		}
)
```
We see:
- a state derivation within a state derivation (two times `switch`)
- in case of state `Service` temporarily store the node and 'do this': Initialize the state `Yes`
- state `Yes` with where rule and reference (to 'close the loop') and a node type definition ({ ... })

Now the node of state `Service` of stategroup `Line status` is available from within the state `Yes` of stategroup `To serve`. With a state switch we can determine the property `Priority` by deriving it from `Priority` within the node of this state `Service`:
```js
'Yes' where 'Service' -> .'Line status'?'Service'
{
	'Table': text -> ^ ^ ^ ^ .'Management' .'Tables'[] = parameter
	'Priority': stategroup = switch .&'Service' .'Priority' (
		|'Low' => 'Low' ( )
		|'Medium' => 'Medium' ( )
		|'High' => 'High' ( )
	) (
		'Low' { }
		'Medium' { }
		'High' { }
	)
}
```
For referencing the reference rule (`where`) the ***&-symbol*** is used.
In our model we access the stategroup `Priority` of node `Service` by writing `.&'Service' .'Priority'`. The rest is a common state derivation.

By revisiting the Car example from the topic 'References', where we explained the where rule applied to a text property, we can show you why the notation `.&'where'` is used:
```js
'Electric vehicles': collection ['Vehicle'] {
	'Vehicle': text
	'Color': text
	'Is': stategroup (
		'Fast' {
			'Top speed': number 'km/h'
		}
		'Slow' { }
	)
}

'Car': text -> .'Electric vehicles'[] // as $ (this is implicit)
	where 'fast' -> $ .'Is'?'Fast'

'Top speed': number 'km/h' = .'Car'&'fast' .'Top speed'
```
Here we used property `Car` with reference rule `fast` (this means `Car` can only have values of `Electric vehicles` that also have state `Fast`) to derive `Top speed` by using the notation `.'property'&'where'`.
Back to our model, since a state is not a property there is no property to refer to and therefore the notation becomes `.&'where'`.

Here is the result of ouw efforts in the app:
![Table and priority](./images_model/033.png)

The example is a bit far fetched but it gives a preview into how intricate models can become.

> <tutorial folder: `./_tutorial/step_09/`>

## More advanced references
We haven't even touched on the subject 'kitchen' yet. The kitchen is where ingredients are turned into dishes. Basic ingredients need to be in stock, prices of products need to be monitored, etc. Let's start easy and create a seperate group `Kitchen` (between `Management` and `Service`), a collection `Products` and a stategroup that show if a product is a basic ingredient or a composed product (for example a dish):
```js
'Kitchen': group {
	'Products': collection ['Product'] {
		'Product': text
		'Product type': stategroup (
			'Basic ingredient' { }
			'Composed product' { }
		)
	}
}
```
If it's a basic ingredient (state `Basic ingredient`) we would like to register the purchase price and the amount this price refers to, for example 1000 grams of potato's cost 5 euro:
```js
'Basic ingredient' {
	'Amount': number positive 'units'
	'Purchase price': number 'thousandth eurocent'
}
```
Also add the new numerical-type `thousandth eurocent`:
```js
'thousandth eurocent'
	@numerical-type: (
		label: "Euro"
		decimals: 5
	)
```
This means a number like 500.000 will be represented as "Euro 5,00000". If later on the purchase cost of for example potato per unit is calculated, by dividing 500.000 by 1.000, the result ("Euro 0,00500") is accurate enough for further calculations.
A composed product consists of other composed products and/or basic ingredients, for example mashed potato with suaerkraut consists of a composed product potato mash and a basic ingredient sauerkraut. Potato mash consists of the basic ingredients potato, milk and butter in certain quantities. These products all exist as nodes on the same level within our collection `Products`:
- Mashed potato with sauerkraut (composed product)
- Sauerkraut (basic ingredient)
- Potato mash (composed product)
- Potato (basic ingredient)
- Milk (basic ingredient)
- Butter (basic ingredient)

If a products has state `Composed product` we want to know a cost price by adding the prices of the ingredients proportionally to the required amount. Let's first describe that composed products consist of products from the same collection:
```js
'Composed product' {
	'Composed amount': number positive 'units'
	'Ingredients': collection ['Product'] {
		'Product': text -> ^ ^ ^ .'Products'[]
		'Amount': number 'units'
	}
}
```
Build your model and an error occurs:
>'property' `Products` is a self-reference, but a reference to a sibling is required.

What this means is exactly what we try to accomplish ( a self-reference), but the compiler doesn't comply and needs 'a reference to a sibling'. To understand this you first need to know that all nodes in the same collection are siblings: They all 'live' on the same level.
To refer to a node from within another node in the same collection we need to apply the word `sibling`:
```js
'Composed product' {
	'Composed amount': number positive 'units'
	'Ingredients': collection ['Product'] {
		'Product': text -> ^ ^ sibling
		'Amount': number 'units'
	}
}
```
Be aware that we jump up two levels instead of the three (in the previous reference)! If we want to refer to a sibling a reference is needed to the level of the key of a collection, not to the level of the collection itself.
Next up is the calculation of a price, without taking into account the amount for now, to create the model step by step. Shown below is the group `Kitchen` we build sofar, including the cost price calculations:
```js
'Kitchen': group {
	'Products': collection ['Product'] {
		'Product': text
		'Product type': stategroup (
			'Basic ingredient' {
				'Amount': number positive 'units'
				'Purchase price': number 'thousandth eurocent'
			}
			'Composed product' {
				'Composed amount': number positive 'units'
				'Ingredients': collection ['Product'] {
					'Product': text -> ^ ^ sibling
					'Amount': number 'units'
					'Price': number 'thousandth eurocent' = ( sibling ) >'Product' .'Cost price'
				}
			}
		)
		'Cost price': number 'thousandth eurocent' = ( sibling ) switch .'Product type' (
			|'Basic ingredient' as $'basic' => $'basic' .'Purchase price'
			|'Composed product' as $'composed' => sum $'composed' .'Ingredients'* .'Price'
		)
	}
}
```

The price of an ingredient of a composed product is determined by the price that is listed under that product's cost price. So: `'Price' ... = ... >'Product' .'Cost price'` points here:
```js
'Products': collection ['Product'] {
	'Product': text
	'Product type': stategroup (
		'Basic ingredient' { ... }
		'Composed product' {
			...
			'Ingredients': collection ['Product'] {
				...
				'Price': number 'thousandth eurocent' = ( sibling ) >'Product' .'Cost price'	// ----> !!
			}
		}
	)
	'Cost price': number 'thousandth eurocent' = ( sibling ) switch .'Product type' (			// <---- !!
		...
	)
}
```

And the cost price per product is derived from whether it's a `Basic ingredient` or a `Composed product`. Either we can simply use the `Purchase price` or we need to sum the prices of all the ingredients that make up the composed product: `sum $'composed' .'Ingredients'* .'Price'`.

So, in the example of mashed potato with sauerkraut (composed product) the cost price structure looks like this:
- Mashed potato with sauerkraut (composed product)
	- Sauerkraut (basic ingredient)
	- Potato mash (composed product)
		- Potato (basic ingredient)
		- Milk (basic ingredient)
		- Butter (basic ingredient)

And is detemined like this:
€<sub>mashed potato with sauerkraut</sub> = €<sub>sauerkraut</sub> + €<sub>potato mash</sub> = €<sub>sauerkraut</sub> + ( €<sub>potato</sub> + €<sub>milk</sub> + €<sub>butter</sub> )

Every time a derivation uses information from a sibling we need to tell the compiler it should look for a sibling by adding `( sibling )` (make sure you add the space before and after the word `sibling`!).
Let's build the model and find out another error occurs:
>no valid 'dependency location' found for 'property'. Unexpected 'relative object location':
	- expected:  'non sibling entity'
	- but found: 'sibling entity'

And the error points to `Cost price` in this line:
```js
'Price': number 'thousandth eurocent' = ( sibling ) >'Product' .'Cost price'
```

Keyword `sibling` in this line `'Product': text -> ^ ^ sibling` solves the problem of not being able to point at a node within the same collection (a user can now say potato mash consists of potato, milk and butter), but also creates a new problem: A user could potentially say that potato mash consists of potato which consists of potato mash, or even worse, that potato mash consists of potato mash itself! Without getting philosophical about whether this is correct or not on an existential level, if a computer would try to calculate the price of potato mash it would end up in an eternal calculation.
The kinds of calculations that use the result of the same calculation are called ***recursive computations***. Like a printer that prints on the back side of its just printed page. It's convenient, but not if it keeps doing that with the same sheet of paper. We'll end up with black pages and unreadable text. The printer needs to know when to stop turning the same sheet of paper and load a new sheet for the next printing step.
To avoid never ending calculations and still make use of the strength of these recursive calculations the Alan platform uses ***graph constraints***, a type of constraints that limits the kind of relations (***edges***) between nodes in a graph (a graph being for example a collection of nodes).
Two graph constraints are implemented on the Alan platform: The ***acyclic-graph*** and the ***ordered-graph***. The next image shows a visual representation of the definitions of these graph constraints:
<img src="./images_model/graph constraints.svg">

An acyclic-graph constraint constrains nodes from forming a cycle: Every node can have links to (multiple) other nodes, but it's not allowed to be referenced back to itself. Any loop is forbidden.
An ordered-graph constraint is even more strict and constrains all nodes to one single chain, like a train with a locomotive (***source***) and a final wagon (***sink***). Obvious examples for an ordered-graph are the days in a month or months in a year: There is a first and a last and in between a consecutive order.

To be very explicit, these constraints do not prevent a user from entering or manipulating data like this:
- In a collection with acyclic-graph constraint:"Potatos consist of eggs and grapefruit, and eggs consist of potato mash and chicken soup"
- In a collection with ordered-graph constraint:"The year starts with month October and ends with month April"

It's the relations between the nodes in a collection that is constrained, not the content. Most computers have no concept of potato, grapefruit or chicken soup.

Continuing with our model, we need to add an acyclic-graph constraint. This is achieved like this:
```js
'Kitchen': group {
	'Products': collection ['Product']
		'Assembly': acyclic-graph
	{ ... }
```
And the reference to a sibling needs to be added to this graph `Assembly`:
```js
'Product': text -> ^ ^ sibling in ('Assembly')
```
The graph `Assembly` stores the relations (edges) between all the nodes and makes sure these remain acyclic. In the app either a user can't select the product that would create a cyclic graph or the app throws an error telling the user it can't save the selected settings.
Finally the derivations need to be aware of this acyclic-graph constraint and know which graph to consult when performing calculations (so it won't end up in a never ending loop):
```js
'Price': number 'thousandth eurocent' = ( sibling in ^ ^ 'Assembly' ) >'Product' .'Cost price'
```
And:
```js
'Cost price': number 'thousandth eurocent' = ( sibling in 'Assembly' ) switch .'Product type' (
	|'Basic ingredient' as $'basic' => $'basic' .'Purchase price'
	|'Composed product' as $'composed' => sum $'composed' .'Ingredients'* .'Price'
)
```

The app now looks like this:
![Kitchen Products](./images_model/034.png)

Let's take a look at `Potato mash`:
![Potato mash](./images_model/035.png)
It consists of butter, milk and potato, each products that can also be found in the same collection `Products`. As expected there's something off with the price: It does not yet take into account the amounts.
For each ingredient we would like to calculate the price for the amount that is used in the composed product. So we change the calculation of `Price` and add a calculation for `Price per unit` in collection `Ingredients`:
```js
'Ingredients': collection ['Product'] {
	'Product': text -> ^ ^ sibling in ('Assembly')
	'Amount': number 'units'
	'Price per unit': number 'thousandth eurocent' = ( sibling in ^ ^ 'Assembly' ) division ( >'Product'.'Cost price' as 'thousandth eurocent' , >'Product'.'Amount' )
	'Price': number 'thousandth eurocent' = ( sibling in ^ ^ 'Assembly' ) product ( .'Price per unit' as 'thousandth eurocent' , .'Amount' )
}
```
The calculation `Price per unit` refers to `Amount` in the node type of the collection `Products`. This needs to be added and has a similar structure as the derivation of `Cost price`:
```js
'Amount': number positive 'units' = ( sibling in 'Assembly' ) switch .'Product type' (
	|'Basic ingredient' as $'basic' => $'basic' .'Amount'
	|'Composed product' as $'composed' => $'composed' .'Composed amount'
)
```
`Price per unit` is determined by dividing the cost price of the ingredient by the (purchased) amount. `Price` is then the product of this `Price per unit` and the amount required in the composed product. The `Cost price` remains the same: `Purchased price` for basic ingredients and `Price` for composed products.
Amounts all have `units` for unit. This can be kilogram, gram, liter, pieces, etc. Deriving the amount of a composed product from its ingredients (similar to the derivation of the price) would require us to know specific volumes or masses of all the ingredients. Then we would be able to calculate how they add up to the weight or volume of the composed product. We won't get into this part in this tutorial. The units of a composed product need to be added by the user.

Be aware to also add to numerical-type `thousandth eurocent` the product and division conversion rules (in that order):
```js
'thousandth eurocent'
	= 'thousandth eurocent' * 'units'
	= 'thousandth eurocent' / 'units'
	@numerical-type: (
		label: "Euro"
		decimals: 5
	)
```

Our potato mash now costs less, because the ingredients cost less:
![Potato mash price](./images_model/036.png)

To end this topic, we can add a stategroup `To be put on menu` in the collection `Products`, to specify for each product if it can be ordered by a customer:
```js
'To be put on menu': stategroup (
	'Yes' { }
	'No' { }
)
```

In the collection `Menu` within group `Service` the key `Item name` now can refer to this collection `Products` and specifically to the state `Yes` of stategroup `To be put on menu`:
```js
'Item name': text -> ^ ^ .'Kitchen' .'Products'[]
	where 'menu item' -> $ .'To be put on menu'?'Yes'
```
<sup>(NOTE: `as $` is implicit, after the reference constraint in the first line)</sup>

The definition of `Item name` is extended with a reference to the collection `Products` and a where rule that more specifically states that only products with the state `Yes` can be used as `Item name`.
If you want to add an item to the menu, you can now select from a list:
![Menu items](./images_model/037.png)

> <tutorial folder: `./_tutorial/step_10/`>

## The End
This concludes the introductory tutorial into the `application` language, and hopefully begins your journey in the world of Alan.
There is still a lot to discover. And "practice makes perfect" (in Dutch:"Oefening baart kunst").

To learn more about the `application` language, we recommend you [read the docs](/pages/docs/model/89/application/grammar.html).
The documentation gives an overview of *all* features that the `application` language supports.

<!--
## (... Permissions and) Todo's
has todo

(
...
can read
can create
can update
can delete
can execute (command)
)

## (... Actions)
...


## (... GUI annotations)
(verwijzing naar documentatie)


## A. Other tutorials
1. Migrations and deployments
2. Interfaces
3. Users
4. Derivations
5. The import module (?)
6. Wiring
7. The stack (?; system types)
8. ... -->