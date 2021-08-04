# ALAN TUTORIAL: An introduction to the Model Language

## Introduction
In the range of tutorials concerning the Alan platform this tutorial will focus on the model language and is a good start to learn the ins and outs of the Alan platform. By means of a story we will take you along several topics and build up the model at the same time. At the end of some topics a reference to a tutorial folder is provided in case you need extra help with producing the appropriate result. Enjoy!

Let's imagine you own a restaurant. Business is doing so well you start to feel you need to be more in control of what's going on, before chaos sets in.

Alan to the rescue!

Alan is a platform that provides a language to model your data and processes in a flexible, yet structured way. This same model is also used to generate an application in a web browser, for entering data and reviewing the state of business.

So, let's dive in!

## 1. A data model
A restaurant is nothing without a good menu. So, first, we take a look at the menu that shows us all the good food and nice drinks you offer. 

### Menu

| *appetizer* | *price (€)* |
| --- | --- |
| Shrimp salad | 3,50 |
| Tomato soup | 4,50 |
| Ciabatta with tapenade | 2,50 |

| *main course* | *price (€)* |
| --- | --- |
| Beef stew | 18 |
| Grilled salmon | 16,50 |
| Mashed potato with sauerkraut | 14 |

| *dessert* | *price (€)* |
| --- | --- |
| Chocolate mouse | 4,50 |
| Vanilla ice cream | 3,50 |
| Cherry pie | 4 |

| *drinks* | *price (€)* |
| --- | --- |
| Orange juice | 4,50 |
| Spa rood | 3 |
| Heineken pilsner | 4,20 |
| Cappuccino | 3,50 |
| Mint tea | 3 |
| Mojito | 6,30 |
---
This menu shows 5 kinds of data:
1. The item that can be ordered (`Item name`)
2. The price per item in Euro (`Selling price`)
3. If it is a dish or a beverage (`Item type`)
4. The type of dish or beverge (`Dish type` / `Beverage type`)
5. And of course, that this collectively is a menu (`Menu`)

If we want to organise these data elements in an Alan-model we could start with this:
```
'Menu': collection ['Item name'] {
	'Item name': text
	'Selling price': number 'euro'
}
```
This small, unfinished model tells us that `Menu` is a container that is defined as ***collection***. This means `Menu` is a collection of sets of data, where a set consists of the values for `Item name` and `Selling price`. Each set in the collection is identified by the value of `Item name` (eg. 'Chocolate mouse'). `Item name` defines what is known as the ***key*** for the collection `Menu`. And for example 'Chocolate mouse' is known as the ***key value***.
A set of values is called a ***node*** (eg. 'Chocolate mouse', '4,50'). So the collection `Menu` contains several *nodes* (the sets of data). In the model the containers between curly braces ( ***{ ... }*** ) define what is called the ***node type***. 

`Item name` is a container that is defined as ***text***: the value of `Item name` will be text

`Selling price` is a container that is defined as ***number*** and more specifically as 'euro': the value of `Selling price` will be a number representing euro's.

>The words *collection*, *text* and *number* are called ***types*** and are ***attributes*** of a container. In other words, the type attributed to a container defines what kind of data a container can hold.

>The curly braces ( ***{ ... }*** ) define the start and end of a *node type* definition. The ***node type*** defines the types of data and its structure in a node.

![node](./images_model/000A.png)

![node type](./images_model/000B.png)

## 2. The minimal model
Let's make an app from these few lines of model code.
First, we need to place these lines in a template with a few standard headings, that looks like this:
```
users

interfaces

root { }

numerical-types
```
This is the minimal model that is needed for every application that is build on the Alan platform. 

`Users` defines who can access your application and what their access rights are. Let's use `anonymous` for now, which means anyone can access our app and can read, add and change data within the app. Later we will explain what other options are available and how access rights can be specified for each part of your model.

`Interfaces` defines with which other apps and/or databases this app is connected. For now we are 'disconnected' from other apps and databases.

`Root { }` is a node, as you can guess by the curly braces. It is the fundamental node in all Alan models. In between these curly braces we will place our model.

`Numerical-types` defines how different number units used in a model should be interpreted. In our case `'euro'` will be added here, since we used it in the model as unit for the number of `Selling price`.

Now, our model looks like this:
```
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
This model needs to be stored in the file ***application.alan*** and located in the file tree at ***[app name]/interfaces/model/***

By the way, when you retype the different lines of code from this tutorial, make sure the individual spaces are correct! For the model to be understood these spaces are important.

## 3. Build the app
How to get this app up and running? The model needs to be processed to produce executable code for a server. This is done by a ***compiler*** that is part of the Alan development environment integrated in VS Code (we use VS Code as our Integrated Development Environment). Before the compiler can translate our model we have to let the compiler know which elements and versions of the Alan platform it needs to properly translate the model. This is done by simply clicking the button `Alan Fetch` in the bottom line of the VS Code window. VS Code will download the correct files needed. This is necessary only once. 

Now we can ***build*** (compile) the model by clicking the button `Alan Build` (next to `Alan Fetch`). If everything is correct the compiler should show no errors and the model is built into an executable app, ready for you to be used.

When opening the app in a webbrowser (we assume you use a chromium-based browser) it looks like this, after you clicked `Menu` in the left column:

![first app](./images_model/001.png)

The data from the menu card is already there, but you can add some data yourself by clicking `Add`. A new window opens. Fill in the required fields, click `Save` and `Close` (top right corner) when you're done. We return to the table `Menu`. Repeat to add more data.

Maybe you've noticed that when you enter a number with decimals, the price is rounded to a whole number:
![wrong numbers](./images_model/002.png)

<tutorial folder: ./_tutorial/step_01/>

## 4. Numerical-types
Of course, we want to correct this. Go back to your model and make sure your `numerical-types` looks like this:
```
numerical-types
	'euro'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
```

Here we define the label it should show if it should differ from the label of the numerical-type (here `Euro` instead of `euro`) and the number of decimals that can be entered by the user (in this case 2 so we can also set euro cents).
There's much more to numerical-types, but we'll leave it at this for now.

## 5. Stategroup
Let's extend the root by making sure we can define whether an item is a dish or a beverage:
```
root { 
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'euro'
		'Item type': stategroup (
			'Dish' { }
			'Beverage' { }
		)
	}
}
```
The container `Item type` is added and is defined as ***stategroup***. This means the container `Item type` can only hold predefined ***states***, in this case either `Dish` or `Beverage`. Notice that `Dish` and `Beverage` have the ability to hold more containers and that these containers can be different for each state. So depending on the state different data can be stored.
Our dishes can be an appitizer, main course or dessert, so let's make these states available by adding the container `Dish type` of type ***stategroup*** to the state `Dish`. This adds more nuance to the model by making it possible to know what kind of dish we're talking about. The same counts for `Beverages`:
```
root { 
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'euro'
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
It shows that states of a stategroup can in itself have other stategroups with states and that the number of states is not limited to two. We also get to see a glimps of the hierarchical form all data models have: `Root` contains `Menu` collections and each `Menu` collection can have state `Dish` or `Beverage` that itself can have states like `Appetizer` or `Cocktail` on even more detailed level.

Build the model (`Alan Build`) and find out what stategroups and numerical-types do for your app:
<tutorial folder: ./_tutorial/step_02/>

![added states](./images_model/003.png)

The table has a few more columns, but the data you might have entered yourself in previous steps is gone! In a real world situation that would be catastrophic and now it's maybe a little annoying. To solve this issue you need to migrate your data from one model version to the other. This topic is described in the tutorial 'Migrations and deployments'.

If you add an item yourself you'll see we have some selection boxes available to determine the states of our added stategroups:
![selection boxes](./images_model/004.png)

## 6. Expand the model
We continue with our model. Add the additional containers to the `root` below `Menu`:
```
root { 
	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'euro'
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
		'Seatsings': number 'chairs'
		'Orders': collection ['Order line'] {
			'Order line': text
			'Item': text -> ^ ^ .'Menu'[]
			'Amount': number 'units'
		}
	}

}
```
First of all, don't forget to add `chairs` and `units` to the `numerical-types` because these numerical types are new to the model:
```
numerical-types
	'euro'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
```

Build and check the app in your browser, selecting `Tables` from the left menu bar. `Table number`'s and corresponding `Seatings` were already added:

![tables](./images_model/005.png)

In the left column we see that `Tables` is parent to the child `Orders`, just like in our model: We have a container of type *collection* within another container of type *collection*. This means that several `Order lines` can be added to `Orders` that is part of one single `Table`. And `Tables` can have several `Table number`'s. This is in line with the business process: In our restaurant with `Tables` a particular `Table number` could have multiple `Order lines` for example for two different dishes and some beers.

As we can see from this model, *stategroups* and *collections* can contain other types, not necessarily of their own type. *Collections* can contain *stategroups*, *collections*, *texts*, etc. The same counts for *stategroups* and *groups*. With these types we can build more complex models that describe the contents of and relations between data and that suit the desired business processes.

<tutorial folder: ./_tutorial/step_03/>

### Built-in types
>We've seen some ***types*** in the previous part, but the Alan platform has several built-in data types available. Time for a complete overview with definitions:
>- A ***text*** attribute holds an unbounded string value (eg. *"this is text"*)
>- A ***number*** attribute holds an integer value (eg. *31415927*)
>- A ***file*** attribute holds two unbounded string values representing a file token and a file extension (eg. *"screenshot"* and *"png"*)
>- A ***collection*** attribute holds a map of key-value pairs. Keys are string values that have to be unique such that we can reference them unambiguously. Keys are implicitly defined for collection attributes; values are nodes of an inline defined type (eg. *{"001"; "Eggs"; 6; 'stired', 'fried'; 'omelette.jpg'}*)
>- A ***stategroup*** attribute holds a value indicating a state. States are alternatives to a property that a state group attribute indicates (eg. *'open'*)
>- A ***group*** attribute holds a node of an inline defined type. Group attributes add structure by grouping other attributes that belong together or share permission requirements, which we'll discuss later in this tutorial.
>- The ***root*** type is a complex type that nests other (complex) types

## 7. References
There's an interesting line in the model that needs our attention: 
```
'Item': text -> ^ ^ .'Menu'[]
```
What's going on here? This line seems to somehow relate the container `Item` (within the collection `Tables`) with the collection `Menu`. `Menu` and `Tables` are collections on the same level, both contained within `Root`. Let's explain by going to the application first. Select a table from the list (as shown in the previous image) and click `Add` in the line `Orders`:

![table number](./images_model/006.png)

Enter an `Order line` ("01" since its the first order from this table):

![order line](./images_model/007.png)

Now select the magnifying glass on the right of `Item` and you'll see this:

![menu items](./images_model/008.png)

Here we see the items of `Menu` and we can select an item from the table. Or, if we start typing in the box `Item name` the table will be filtered. We can only choose an item that is in the table, specifically in the column `Item name`. This is the result of that line in the model: An `Item` is constraint to the entries in the referenced collection `Menu`. Formally, this is known as a (mandatory) ***reference (constraint)*** and is used in the model by typing this arrow **`->`**. 
A *reference (constraint)* always references a *node type* by supplying a *path* to the *node type*. A ***node type path*** uniquely identifies every *node type* in the model from the `root` (eg. `.'Menu'` which is short for `root .'Menu'`). The *reference* can only be applied to a container with type *text* (eg. `Item`). It can't be applied to the types *number*, *file*, *collection*, *stategroup* and *group*.
Also notice the square brackets `[` and `]` behind `.'Menu'`. This implies that we refer to one unspecified set of values (a *node*) in the collection `Menu` which is identified by the value of the *key* `Item name` of the collection `Menu`. This value is known as the ***key value*** of the selected node: `Item` has the value 'Beef stew' after selecting it, as presented in this image:

![beef stew](./images_model/009.png)

Once models get more complex this construction is very powerful, because by knowing the *key value* we can get information from within the *node* that is identified by this key value. In our case, by knowing table 'T01' ordered 2 'Beef stews' and by definition of the collection `Menu` knowing that a 'Beef stew' has a price of '18 Euro' we could calculate that this table needs to pay 36 Euro at this point in time.

>Next to `Item` being defined as of type *text* it is additionally being defined by its (mandatory) reference to `Menu`: Values of `Item` can only consist of *key values* from `Menu`. 
This extention of the definition of `Item` is also an important concept of the Alan platform.

Entering an amount and selecting `Save` get this result:

![first order line](./images_model/010.png)

Not all references can be made mandatory. When a text container references a collection that is defined outside the scope of the current model, for example in another app or in an external database, we can't technically make sure that the reference constraint is always met, but we do want to keep our apps and models close knit. So we make these references optional by using the symbol **~>** (curly arrow, not to be confused with **->** ) and call these ***links***.

The definition of a text, like we've seen above, can be extended with what is called a ***reference rule***. We can use the word `where` to apply one or more *reference rules* to a text. An example, apart from our current model:
```
'Car': text -> .'Electric vehicles'[]
	where 'blue' ~> .'Blue objects'[]
	where 'american' ~> .'American products'[]
```
`Car` in this example has one *reference* and two *links* which all define `Car`:
- `Car` can have key values from the collection `Electric vehicles`
- `Car` can have key values from the collection `Blue objects`, by definition of the rule `blue`
- `Car` can have key values from the collection `American products`, by definition of the rule `american`
This way `Car` is much more specified. The rule names `blue` and `american` can be used as references themselves in subsequent parts of the model, which can come in handy.

By the way, *links* are used in this example because it is not technically possible yet and it has not been neccesary to make mandatory references to several collections (although within the same model).

`Where` is not restricted to be used with text containers, it can also be used with states of a stategroup. More on this in the topic *Advanced references*.

## 8. Hierarchy
We explained this: **->**, but why do we need this: **^ ^**? As mentioned earlier, there are parent and child relations between different parts of the model, thus between different data. These parts, or this data, exists on different levels, created by the node types (the containers between curly braces **{** and **}** ). For explanatory purposes, let's say `root` is on level 0. Then collection `Menu` is on level 1, while text `Item` is on level 3:

| 0 | 1 | 2 | 3 | ... | 2 | 1 |
|---|---|---|---|---|---|---|
|`root` | `{ Menu` | `{ ... }` | | | | `}` |
|`root` | `{ Tables` | `{ Orders` | `{ Item }` | | `}` | `}` |

So, to reference `Menu` we have to 'jump up' two levels relative to `Item`, therefore the two 'arrows' up: **^ ^** . This makes it clear to the compiler where it can find `Menu`.
Additionally, for the compiler to understand this jump up, the referenced collection also needs to be positioned above the reference constraint, i.e. `Menu` needs to be defined before `Item` can reference it, reading the model from top to bottom.

To summarize, `'Item': text -> ^ ^ .'Menu'[]` is:
- a container with the name 'Item'
- that is of type *text* 
- that is constrained by a *reference constraint* 
- which is defined by a *relative node type path* 
- that points to a *node type*.

## 9. Modify the model
Hopefully by now you can 'read' this model and understand its components and structure. Meanwhile our restaurant is in full swing, so no time to waste!

You might have experienced in your restaurant that having a static set of beverage types might not be very practical. Let's change the model accordingly and make a dynamic set of beverage types, which means the *stategroup* `Beverage type` is removed and replaced with a *collection* `Beverages types`. 

Since we still want to be able to select a beverage type when we compose our menu, we need to be able to reference `Beverages types` from `Beverage type` within the state `Beverage` in our model. Therefore it needs to be above `Menu`. Modify your model according to this new one:
```
users
	anonymous

interfaces

root {
	'Beverages types': collection ['Beverage type'] {
		'Beverage type': text
	}

	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'euro'
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
	'euro'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
```

Again, build and check your app, selecting `Beverages types` from the left menu bar:
<tutorial folder: ./_tutorial/step_04/>

![beverages types collection](./images_model/011.png)

Now you are free to add or adjust the types of beverages you have in your restaurant and still be able to use those in your menu setup:

![similar menu layout](./images_model/012.png)

Select 'Mojito', then `Edit` (top right):

![mojito](./images_model/013.png)

And finally the magnifying glass on the right of `Beverage type`:

![edit beverage type](./images_model/014.png)

Here, we can edit the `Beverage type` of 'Mojito'. The collection `Beverages types` is shown just like before with `Orders`. This *graphical user interface* ***(GUI)*** is also automatically updated just by changing our model.

## 10. Reference set
You decided that your restaurant will also provide a take-away service. This means adjusting the model accordingly. Let's see what is needed.

`Orders` will no longer be a child to the parent `Tables`, which makes more sense anyway: If we consider these entities more accurately, `Orders` and `Tables` don't have a parent-child relation, since they are of different order. For example the relation between `Tables` and `Seatings` is more natural, like wheels to a car or zebra to mammals.
`Orders` need to be defined as either takeaway or in-house. And if in-house, it can be linked to a table.
We will change this part of the model:
```
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
```
'Tables': collection ['Table number'] {
	'Table number': text
	'Seatings': number 'chairs'
	'Orders': reference-set -> .'Orders'* .'Order type'?'In-house' = inverse >'Table'
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
- Since we don't want a long list of `Order line`'s, we organized the `Order line`'s in a subcollection `Order lines` . Now each `Order` can have multiple `Order line`'s (previously each `Table number` could have multiple `Order line`'s)
- We've added a stategroup `Order type` to indicate the kind of order: state `Takeaway` or state `In-house`
- If the state of an orde is `In-house` we also like to know which `Table` it belongs to, so we added a text `Table` that references the collection `Tables` inside the node of state `In-house`

And now for the interestingly new parts: 
We would also like to know for each `Table` which `Orders` it has. So far we could only know for each `Order` which `Table` it has, by means of the *reference constraint* on `Table` (by the way, did you check if two ^ are correct here?). The ***reference set*** makes it possible to know which `Orders` are pointing to each `Table`, so for each `Table` we can have insight into its `Orders`. 
We achieve this by adding `Orders` to the collection `Tables` and define it as type *reference set*. Then we have to make the reference to the desired location by supplying the path: `-> .'Orders'* .'Order type'?'In-house'` This is called an *absolute node type path*:
- Absolute since it starts from the root and no `^` are used
- Node type path since it descibes a path in several node types: `.'Order type'?'In-house'` within `.'Orders'*`

Here we use * instead of [ ] behind `.'Orders'` because we want to reference *all* the nodes (not a single node) of `Orders` that have the state `In-house`.
Finally we say 'follow the reference of `Table`', written like this: `>'Table'` (more on the symbol > in the topic Navigate), but do it 'backwards' (`inverse`). If we 'jump' to `Table` we see a kind of inverse reference `-<` (instead of `->`) at the end of the line with label `Orders`. This links `Table` from collection `Orders` to `Orders` from collection `Tables`.

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

## 11. Command

Instead of going to `Orders`, clicking `Add`, providing an order number, then clicking `Add` again to provide `Order lines` and finally being able to select a menu item, you would like to make it easier on your service personnel by providing one form for placing a new order. This is achieved by adding a ***command*** to our model and it looks like this:
```
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
		|'At the restaurant' => create 'In-house' (
			'Table' = @ .'Where is the customer seated?'
		)
	)
	'Order lines' = walk @ .'Order lines' (
		create (
			'Order line' = @ .'Provide an order line number'
			'Item' = @ .'Item to be consumed'
			'Amount' = @ .'Amount of this item'
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

Let's review the added *command* in the model. The first part of the *command* looks a lot like familiar model language and actually is similar:
```
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
It defines the command by providing containers in between curly braces (just like with for example a *collection*) that can hold specific data types. Some containers also have reference constraints to control the allowable values. These containers are called the ***parameters*** of the command.
Although the labels are different, the structure of the command is the same as the collection `Orders`. In this case we want to manipulate this collection with the command and often the command definition is identical to the definition of that collection.
The *parameters* (containers within the command) correspond with the fields in the GUI-form to be filled in and thus hold the inserted values after submitting the form.

Then the start of the second part of the *command*: 
```
... => update .'Orders' ...
```
It consists of a double arrow ( ***=>*** ), the word ***update*** and a *(absolute) node type path*. The double arrow can be read as 'do this'. *Update* means we want to update a collection or stategroup. And the path points to the collection or stategroup we want to update with the provided data, in this case collection `Orders`.
Instead of *update* we can also use these key words: *switch*, *match*, *ignore*, *walk*, *execute* and *external*, each with their own definition and required structure that should follow the key word. Let's stick with *update* for now, since we want to update the specified collection.

The end of the second part: 
```
			... = create ( ... )
```
This tells us what the update should be about: 'the update is ( ***=*** ) the creation (***create***) of a node.
The key word *create* can be replaced by only the key word ***ensure***. *Create* will check if an entry in the target collection already exists (if there is a node that is similar to the values the user filled in). If so, an error will be thrown and the command will be aborted. Otherwise, the new node is created. *Ensure* will also create the node, but if it already existed it will overwrite its data.

And lastly, the part between the parentheses of the key word *create*:
```
'Order' = @ .'Provide an order number'
'Order type' = switch @ .'Where is the meal consumed?' (
	|'Outside of restaurant' => create 'Takeaway' ( )
	|'At the restaurant' => create 'In-house' (
		'Table' = @ .'Where is the customer seated?'
	)
)
'Order lines' = walk @ .'Order lines' (
	create (
		'Order line' = @ .'Provide an order line number'
		'Item' = @ .'Item to be consumed'
		'Amount' = @ .'Amount of this item'
	)
)
```
Each container within the collection `Orders` is equated with the parameter defined in the *command*, much like this:
```
'container in collection' = @ .'parameter of command'
```
This means the values inserted in the form are copied to a node that is being created within the collection `Orders`. The symbol ***@*** is used to tell the compiler a given path is within the command definition. Otherwise the compiler will consider these paths as within `root`. 
As an experiment to show you how the compiler responds without this symbol, remove the @ in this line: `'Order' = @ .'Provide an order number'` and build the model. The compiler will throw an error telling you it can't find `Provide an order numer` in `root` and will show what it does find in `root`.

Additionally, we see two new key words: ***switch*** and ***walk***. Let's discuss *switch*:
```
'Order type' = switch @ .'Where is the meal consumed?' (
	|'Outside of restaurant' => create 'Takeaway' ( )
	|'At the restaurant' => create 'In-house' ( ...	)
)
```
Since we don't know which selection the user is going to make we need a way to link al possible states of the input (parameter) stategroup with all possible states of the output stategroup. The statement *switch* expresses that we want to switch between possible states of `Order type`, depending on the state of the stategroup `Where is the meal consumed?`.
You can read it like this: 
'If the state of `Where is the meal consumed?` is `Outside of restaurant`, then 'do this': create the state `Takeaway` for stategroup `Order type`. If the state of `Where is the meal consumed?` is `At the restaurant`, then 'do this': create the state `In-house` with a node that contains a value for `Table` for stategroup `Order type`.'

Let's look at *walk*:
```
'Order lines' = walk @ .'Order lines' (
	create ( ... )
)
```
The statement *walk*, followed by the node type path, expresses that we want to 'walk along' all entries in the collection `Order lines`. The statements between the parentheses are evaluated for each of the entries in the collection. In this case for each entry in the parameter `Order lines` a node is created in the collection `Order lines` according to the supplied structure and values.

Finally, *command*s can also be used to transmit data from one app to another through an interface. More on this in the tutorial 'Interfaces'.

>Before we continu with the next topic it is good to know that *reference-set* and *command* are also considered possible *attributes* for a container. The previously mentioned types *text*, *number*, *file*, *collection*, *stategroup* and *group* are more specifically *property attributes*, in short ***properties***, of the container. This in contrast to the *attributes* *reference-set* and *command*. 

## 12 Derivations: numbers
Whenever you want to derive a value from other values, we use derivations. Derivations can be recognized in the model by the symbol **=**. This means we've already seen some derivations in the previous topic on *command*s. 
We've seen for example a state of a stategroup being derived from the state of another stategroup by using = and the statement *switch*. Such a ***state derivation*** can also be used  outside of a *command* attribute, more generally in a model. More on this in the topic *Derivations: conditional expressions*.

Here we focus on number derivations. Let's make the also previously mentioned example (in the topic *References*) of calculating a subtotal per order line. Add these lines below `Amount` to your model:
```
'Order lines': collection ['Order line'] {
	'Order line': text
	'Item': text -> ^ ^ .'Menu'[]
	'Amount': number 'units'
	'Line total': number 'euro' = product (
		>'Item'.'Selling price' as 'euro' ,
		.'Amount'
	)
}
```
A property `Line total` of type *number* with numerical-type 'euro' is added. The value of `Line total` is derived by multiplying the selling price with the amount. The ***product*** statement takes two terms: the two numbers to be multiplied.

>An important concept arises when we focus on the symbol ***>*** in front of `Item` (the first term in the *product* statement for calculating `Line total`). This line of code means:
'With the current value of `Item` (a key value of `Menu`) of this specific `Order line` follow its reference and from the resulting node in that referenced collection provide the value of property `Selling price`.' 
>So, from a specific node of `Order lines`, that has a specific value for `Item`, a reference is made to another specific node of `Menu` from which the value of the property `Selling price` is provided.
>In short, *>* makes sure that during runtime the current value of `Item` is used to reference the appropriate node of the referenced collection.

Now we want to focus on the ***as*** statement followed by `'euro'`.
To explain what this means and for the health of our model we need to add this line:
`= 'euro' * 'units'` below `euro` so our numerical-types now looks like this:
```
numerical-types
	'euro'
	= 'euro' * 'units'
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
`'Dollar selling price': number 'dollar' = from 'euro' .'Selling price'`
And a ***singular conversion rule***: 
`= 'num-typ' * constant`, according to the example:
```
numerical-types
	'dollar'
	= 'euro' * 1176 * 10 ^ -3	// 1 euro = 1.176 dollar (20-7-2021)
```

Let's add another useful line to the model:
```
'Total': number 'euro' = sum .'Order lines'* .'Line total'
```

Can you determine where it needs to go? Spoiler alert: answer ahead...

So now our whole model looks like this:
```
users
	anonymous

interfaces

root {
	'Beverages types': collection ['Beverage type'] {
		'Beverage type': text
	}

	'Menu': collection ['Item name'] {
		'Item name': text
		'Selling price': number 'euro'
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
		'Orders': reference-set -> .'Orders'* .'Order type'?'In-house' = inverse >'Table'
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
			'Line total': number 'euro' = product (
				>'Item'.'Selling price' as 'euro' ,
				.'Amount'
			)
		}
		'Total': number 'euro' = sum .'Order lines'* .'Line total' // <-- ;-)
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
			|'At the restaurant' => create 'In-house' (
				'Table' = @ .'Where is the customer seated?'
			)
		)
		'Order lines' = walk @ .'Order lines' (
			create (
				'Order line' = @ .'Provide an order line number'
				'Item' = @ .'Item to be consumed'
				'Amount' = @ .'Amount of this item'
			)
		)
	)
}

numerical-types
	'euro'
	= 'euro' * 'units'
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
***min***: determines the minimum of a set of values
***max***: determines the maximumof a set of values
***std***: determines the standard deviation of a set of values
***count***: counts the number of values in a set 
***remainder***: calculates the remainder of a division (10 mod 3 = 1)
***division***: calculates the division of two numbers  
***add***: calculates the addition of two numbers
***diff***: calculates the difference of two (relative!) numbers, for example the difference between two dates or two degrees Celcius 

Examples of absolute and relative numbers:
(number of) days: absolute, "28 days"
date: relative, "28-7-2021"
years: absolute, "5 years"
year: relative, "2021"
degrees: absolute, "21 degrees"
degrees Celcius: relative, "21˚C"
seconds, minutes, hours: absolute, "2 hours, 35 minutes and 8 seconds" (duration)
time of day or 'the time': relative "14:35:08"

So far we've seen numerical derivation, but we can also derive other types of data.

## 13 Another model expansion
To show examples of other types of derivation we need to create a more intricate model.
Let's create a group `Management` at the top of the model that contains a new collection `Discount peroids`, a number `VAT percentage` and the existing collection `Beverages types` (because this is a more suitable place):
```
'Management': group {
	'Discount periods': collection ['Period'] {
		'Period': text
		'Percentage' : number 'percent'
		'Minimal spendings': number 'euro'
	}

	'VAT percentage': number 'percent' = 21

	'Beverages types': collection ['Beverage type'] {
		'Beverage type': text
	}
}
```
And since we've added a new numerical type, we need to add this to our `numerical-types` in the model:
```
'percent'
```
We will use the collection `Discount periods` for selecting a certain discount percentage (`Percentage`), depending on the amount of money spend (`Minimal spendings`). `VAT percentage` will be used to calculate value added tax (VAT).
Change the number property `Total` within collection `Orders` into `Subtotal`, because the new `Total` will take into account the appropriate discount:
```
'Subtotal': number 'euro' = sum .'Order lines'* .'Line total'
```

## 14 Derivations: conditional expressions

Now let's add a stategroup `Discount applicable`, also within `Orders`. These lines of code also show some more examples of the symbol **>** :
```
'Discount applicable': stategroup (
	'Yes' {
		'Discount period': text -> ^ ^ .'Management' .'Discount periods'[]
		'Discount': number 'euro' = switch ^ .'Subtotal' compare ( >'Discount period' .'Minimal spendings' ) (
			| < => 0
			| >= => product (
				from 'percent' >'Discount period' .'Percentage' as 'percent-fraction',
				^ .'Subtotal'
			)
		)
		'Total': number 'euro' = sum ( ^ .'Subtotal' , - .'Discount' )
	}
	'No' {
		'Discount': number 'euro' = 0
		'Total': number 'euro' = ^ .'Subtotal'
	}
)
```
Add the numercial type `percent-fraction`, the *product conversion rule* and the *singular conversion rule* to the numerical types. It should now look like this:
```
numerical-types
	'euro'
	= 'units' * 'euro'
	= 'percent-fraction' * 'euro'
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

Because we `switch` on a `compare` we can provide the desired states with operators like 'greater than', 'equal', 'less than' and combinations of these.
Finally, the `Total` is calculated by adding `Subtotal` to the negative of `Discount` (subtraction).
If discount is not applicable (state`No`) `Discount` is equal to 0 and `Total` is equal to `Subtotal`.

Although the inputs and outcome are numbers, we also call this a ***state derivation*** because the result is determined from which state is true.

We also have to adjust the command `Place new order`, since this comand updates collection `Orders` and this collection has changed. Can you find out where these seperate parts of code should go and what they mean?:
```
'Apply discount?': stategroup (
	'Yes' {
		'Discount period': text -> .'Management' .'Discount periods'[]
	}
	'No' { }
)
```
And:
```
'Discount applicable' = switch @ .'Apply discount?' (
	|'Yes' => create 'Yes' (
		'Discount period' = @ .'Discount period'
	)
	|'No' => create 'No' ( )
)
```
Let's take a look at the app and enter an order:
![discount](./images_model/023.png)
An order with a subtotal of €40,20 receives during the summer holiday a discount of 3%  when spending €35 or over.

It's time to calculate the VAT. To do this we need to know the `Total` and calculate a percentage of it. But we have two kinds of `Total` depending on whether a discount was applied or not. This means our calculation should depend on which state that specific `Total` is in. Again we can use the `switch` statement for this:
```
'VAT': number 'euro' = switch .'Discount applicable' (
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
We define `VAT` as a `number` of numerical type `euro` and derive (=) it depending on (switch) the states of stategroup `Discount applicable`: either `Yes` or `No`. In both cases we end up using the product statement and supply this with the appropriate terms. The interesting parts are where the ***\$*** symbols are used. If we look back at our definition of the stategroup `Discount applicable` (at the start of this topic) we see that each state has a node type definition by providing properties and derivations within the curly braces: `'Yes' { ... }` and `'No' { ... }`. When `as $'...'` is used a specific node (all the values of that particular node of the specified state within a node of collection `Order`) is pinpointed and can be referenced as `$'...'`. In our case that pinpointed node is given the temporary name `discount` for nodes in the state `Yes` and `no discount` for nodes in the state `No`. So, when we say `$'discount' .'Total'` we mean the value of `Total` within a node of state `Yes`. And similar for `$'no discount'`.
`$'discount'` and `$'no discount'` are called ***named objects***.

<tutorial folder: ./_tutorial/step_05/>

Derivations come in several forms and are powerful tools. We've shown you some examples, but want to provide an in depth overview in the *Derivations tutorial*.

## 15 Upstream and downstream

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

To create an example without the need for building a very intricate model, let's change the model slightly. Move the `Tables` collection below the `Orders` collection. This disobeys the previously mentioned rule (in the topic *Hierarchy*) that collections referenced at some point in the model need to be above that point.
Build the model and the compiler will throw an error:
>order constraint violation. `Tables` needs to be a 'predecessors' entry in 'attributes'. Available 'predecessors':
	- `Menu`
	- `Management`

The error refers to this line, within the collection `Orders`:
```
'Table': text -> ^ ^ .'Tables'[] -< 'Orders'
```
The compiler expected to find the referenced collection `Tables` above this point in the model. As we've learned just now we can bypass this error by adding the statement `downstream` like this:
```
'Table': text -> downstream ^ ^ .'Tables'[] -< 'Orders'
```
Build the model again and you'll notice that the compiler is at ease with this. We've told the compiler to look for `Tables` further down in the model, in the second phase of calculations.

Please revert your model to the previous state, because this is not good practice (although in exceptional cases unavoidable): For good readability of your model it is best to stick to the rule that whatever you would like to reference has to come first in your model.
