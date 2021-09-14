---
layout: page
title: "Application Tutorial:<br>a Restaurant app<br>Part II"
category: docs
version: 89
---


1. TOC
{:toc}

## Introduction
This is the second part of the application language tutorial where we build a restaurant app.
Make sure that you have completed [the first part](/pages/tutorials/application-tutorial.html) before continuing.

Let's recap: in the first part, we wrote a small data model for our restaurant.
From that data model, we generated a web application for entering a menu, tables, and orders.
In this second part you will learn about [derived values](#derived-values), more [advanced references](#advanced-references), [evaluation phases](#upstream-and-downstream), and [commands](#commands).

## Take-away
You decided that your restaurant will also provide a take-away service.
For that, we have to make so adjustments to the model.
Let's see what is needed.

`Orders` will no longer be part of `Tables`: we can have `Orders` without `Tables`.
But, for an `Order`, we do want to know if it is a `Takeaway` order, or if it is an `In-house` order for a table.
For that, we add an `Order type`.

So, we rewrite this piece of code:
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

to this:
```js
'Tables': collection ['Table number'] {
	'Table number': text
	'Seatings': number 'chairs'
}

'Orders': collection ['Order'] {
	'Order': text
	'Order type': stategroup (
		'Takeaway' { }
		'In-house' {
			'Table': text -> ^ ^ .'Tables'[]
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
- We moved `Orders` one level up, to the `root`.
- Previously, we had a list of `Order lines` per table.
That is inconvenient, because we want to know which `Order lines` belong to the same order.
Therefore, we updated our model to express that `Orders` have a collection of `Order lines`.
- We've added a stategroup `Order type` with two possible states: `Takeaway` or `In-house`
- For `In-house` `Orders`, we also want to know for which `Table` they are. Therefore, `In-house` orders now have a `Table` attribute, that references a `Tables` item.

## Derived values
Our customers have to pay us, and for that we need to compute the cost of their orders.
Let's start with a `Line total`: the cost of a single `Order line`:
The `Line total` of an `Order line` is a derived value, computed from the (base values) `Selling price` and the `Amount`:
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
After `eurocent` for the `Line total` we have have written a formula for deriving the `Line total` of an `Order line`.
The formula (derivation expression) expresses that the `Line total` is computed by multiplying (taking the `product` of) the `Selling price` and `Amount`.

For retrieving the `Selling price` of the `Item` we use the notation `>'Item'`.
That means, starting at the `Order lines` node, follow the `Item` reference (expressed by `-> ^ ^ .'Menu'[]`).
So, at runtime, `>'Item'` gives us the `Menu` item that corresponding to an `Order line`.

After `Selling price`, there is some special code: `as 'eurocent'`.
To explain what this means and for the health of our model we need to add this line:
`= 'eurocent' * 'units'` below `euro` so our `numerical-types` section now looks like this:
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
The *as* statement is followed by what is called a ***product conversion rule***.
Such a rule describes how `numerical-types` of the two properties are multiplied, like `euro` and `unit`.
So the general format of a *product conversion rule* is `= 'num-type1' * 'num-type2'`.
The first part (`num-type1`) is wat we mention after the keyword `as`.

For a `division`, we see something similar:
`= division ( 'property1' as 'division conversion rule' , 'property2' )`
The `division` uses a ***division conversion rule***:
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

Conversion rules ensure that `numerical-types` for derived values are correct.
They also let you reuse (singular) conversions.

---

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
	}

	'Orders': collection ['Order'] {
		'Order': text
		'Order type': stategroup (
			'Takeaway' { }
			'In-house' {
				'Table': text -> ^ ^ .'Tables'[]
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

And at runtime (in your app) it looks like this:
![(line totals and total](./images_model/022.png)

The possible operations that can be used for deriving number values can be found [here](/pages/docs/model/89/application/grammar.html#derived-numbers).
- `min`: determines the minimum of a set of values
- `max`: determines the maximum of a set of values
- `std`: determines the standard deviation of a set of values
- `count`: counts the number of values in a set
- `remainder`: calculates the remainder of a division (10 mod 3 = 1)
- `division`: calculates the division of two numbers
- `add`: calculates the addition of two numbers
- `diff 'date'`: calculates the difference of two (relative!) numbers, for example the difference between two dates or two temperatures

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


> <tutorial folder: `./_docs/tutorials/restaurant1/step_04a/`>

## Growing our business
Our restaurant business is growing.
Many people are now working with our app, and its time for some reorganizations.
We have more permanent data that only `Management` should touch, and we want to show that in our application.
For that, we express a group called `Management` at the top of the model.
This group captures a new collection `Discount periods`, a `VAT percentage`, and the existing collections `Beverages types` and `Tables`:
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
	}
}
```
When you have moved `Beverages types` and `Tables` to the group `Management`, rebuild your app.
You'll get some errors saying the compiler can't find certain properties.
Correct the errors according to the changes made, by adding missing navigation steps such as `.'Management'`.

The `VAT percentage` will be used for calculating the value added tax (VAT).
For the `VAT percentage`, we also have to add a numerical type to the `numerical-types` section in the model:
```js
'percent'
```

The `Discount periods` are for discounts during different time periods, where the discount depends on the amount of money spent at the restaurant.

Rename the attribute `Total` for `Orders` to `Subtotal`:
```js
'Subtotal': number 'eurocent' = sum .'Order lines'* .'Line total'
```
The actual `Total` cost will depend on a discount when applicable.

> <tutorial folder: `./_docs/tutorials/restaurant1/step_05/`>

## Conditional expressions
Now let's add a stategroup `Discount applicable` to `Orders`:
```js
'Discount applicable': stategroup (
	'Yes' {
		'Discount period': text -> ^ ^ .'Management' .'Discount periods'[]
		'Discount': number 'eurocent' = switch ^ .'Subtotal' compare ( >'Discount period' .'Minimal spendings' ) (
			| < => 0
			| >= => product (
				from 'percent' >'Discount period' .'Percentage' as 'fraction',
				^ .'Subtotal'
			)
		)
		'Total': number 'eurocent' = sum ( ^ .'Subtotal' , - .'Discount' )
	}
	'No' { }
)
```

Now, add the required numerical type `fraction`, the product conversion rule, and the singular conversion rule to the `numerical-types` section:
```js
numerical-types
	'eurocent'
		= 'units' * 'eurocent'
		= 'fraction' * 'eurocent'
		@numerical-type: (
			label: "Euro"
			decimals: 2
		)
	'chairs'
	'units'
	'percent'
	'fraction'
		= 'percent' / 1 * 10 ^ 2
```

With this model extension, you can apply a discount by selecting a `Discount period` from the previously added collection `Discount periods`.
For example, selecting 'Summer holiday' will give 3% discount on spendings over €35.
If a discount is applicable (state `Yes`) and a `Discount period` is selected, the `Discount` will be computed after saving your changes:
- Compare the `Subtotal` with the `Minimal spendings` that belong to the selected `Discount period`
- If `Subtotal` is smaller than `Minimal spendings` then `Discount` will be equal to 0
- If `Subtotal` is bigger than or equal to `Minimal spendings` then the `Discount` will be computed using the corresponding `Percentage`.
The `Percentage` is first converted from `percent` to `fraction` (from 3% to 0.03).
The `Total` is then computed as the product of the computed `fraction` and the `Subtotal`.

With the expression, we `switch` on the comparison (`compare`) result of two numbers.
We can match against the following possible results for the comparison:
- 'greater than' (`>`)
- 'greater than or equal to' (`>=`)
- 'less than' (`<`)
- 'less than or equal to' (`<=`)
- 'equal to' (`==`)
- 'less than or greater than' (`<>`)
Cases may not overlap, so you cannot match against `<` as well as `<=`.

Finally, the `Total` is calculated by subtracting `Discount` from the `Subtotal` using the `sum` operation and a sign inversion (`-`).
If discount is not applicable (state `No`), then the `Total` is identical to `Subtotal`.

Let's take a look at the app and enter an order:
![discount](./images_model/023.png)
An order with a subtotal of €40,20 receives a discount of 3% when spending €35 or more during the summer holiday.

Now, let's calculate the tax (`VAT`).
To do this we need to know the `Total` cost and take a percentage of it.
But, the actual `Total` cost of an `Orders` item depends on whether a discount was applied or not.
For that purpose, we use a `switch` statement for switching on the state of a stategroup attribute, after which we can compute the `VAT` from the `Total` of the order:
```js
'Total': number 'eurocent' = switch .'Discount applicable' (
	|'Yes' as $'discount' => $'discount'.'Total'
	|'No' => .'Subtotal'
)
'VAT': number 'eurocent' = product (
	from 'percent' ^ .'Management' .'VAT percentage' as 'fraction' ,
	.'Total'
)
```

For computing the `Total`, we `switch` on the state of `Discount applicable`.
In case of state `Yes` we use a special instruction `as $'discount'`.
This stores the `Yes` node under the name `$'discount'`.
Because of that, we can refer to it in the remaining part of the expression (and only there): `$'discount'.'Total'`.
We call this a **named object** (or constant variable).

Here's the result of our work:
![VAT](./images_model/024.png)

For each property type that the `application` language supports, the language also supports expressing for deriving such values.
So, you can derive text values, file values, references, stategroup states, and even collections.
You can find many examples in the `application` language [documentation](/pages/docs/model/89/application/grammar.html#derived-values).

> <tutorial folder: `./_docs/tutorials/restaurant1/step_06/`>


## Usages and Reference sets
References are by default unidirectional.
However, it is often useful to 'invert' those references: for `Tables` we may want to know which `Orders` it has placed.

You may have noticed the `Usages` button in your app, when viewing a `Tables` item.
Clicking on `Usages`, gives you a screen with exactly that information: which `Orders` exist for `Tables`.

Let's try that with a new order.
Select `Orders` in the left column and click `Add`:

![order](./images_model/015.png)

Insert '001' as the order number, choose `In-house` and select a table.
Just for fun, add some order lines as well:

![order lines](./images_model/016.png)

Now, hit `Save`!
Go to `Tables`, pick the table you selected when placing the order and click `Usages`:

![usages](./images_model/017.png)

We can see that in our version `Order` '001' is using table 'T03':

![table used](./images_model/018.png)

If we click the order, we jump to the order with its order lines.

---
In the web app, we have this nice 'Usages' screen.
The web app computes these screens for us.
However, we cannot use these 'Usages' in computations.
For that, we need bidirectional references.

You can turn unidirectional references into bidirectional references with a **reference set**.
A *reference set* holds inverse references, which are identical to the usages that we just saw.
Let's add that reference set, and some derivations that use it:
```js
'Tables': collection ['Table number'] {
	'Table number': text
	'Seatings': number 'chairs'
	'Orders': reference-set -> downstream ^ ^ .'Orders'* .'Order type'?'In-house' = inverse >'Table'
	'Number of orders': number 'units' = count <'Orders'*
	'Total order value': number 'eurocent' = downstream sum <'Orders'* ^ .'Total'
}
```
Also, add `-<'Orders'` at the `Table` reference below `'In-house'` in your model.
```js
'Table': text -> ^ ^ ^ .'Management' .'Tables'[] -<'Orders'
```

Now, build it and take a look at the app.
For each `Tables` node we can now see how many `Orders` have been placed at that table.
Furthermore, we can see the `Total order value` for the `Orders` placed at a specific table.
Nice stats that may enable us to optimize the placement of our `Tables`.

For expressing the reference set, we use a special keyword `downstream` followed by a navigation path.
The keyword `downstream` indicates in which computation phase the reference set is available.
You can read more about that in the [next section](#upstream-and-downstream).

The navigation path contains the keyword `*` instead of `[]` that we saw for unidirectional references.
That is because multiple `Orders` can reference the same table; the `reference-set` for a specific table will hold *all* `Orders` that refer to that specific table.
Finally we say: take the `inverse` of the `Table` reference that you find under `In-house`.

For the `Table`, we expressed that for the reference, its inverse (`-<` instead of `->`) should be stored in the reference set `Orders` of the `Tables` item.

> <tutorial folder: `./_docs/tutorials/restaurant1/step_06a/`>


## Upstream and downstream
Computations for Alan applications are divided over multiple different phases to guarantee that derivations can always be evaluated.


In the [documentation](/pages/docs/model/89/application/grammar.html#upstream-downstream-and-sibling-dependence) we computation phases this in more detail.

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
			'Where is the customer seated?': text -> .'Management'.'Tables'[]
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
	'Discount applicable' = create 'No' ( )
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
This means access the parameter node, lookup the specified value (inserted in the form by the user) and copy it to the container of the collection. The keyword ***@*** is used here to tell the compiler a given path is within the command definition. Otherwise the compiler will consider these paths as within `root`.
As an experiment to show you how the compiler responds without this keyword, remove the @ in this line: `'Order' = @ .'Provide an order number'` and build the model. The compiler will throw an error telling you it can't find `Provide an order numer` in 'attributes' and will show what it does find in 'attributes', in this case `root`.

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
is to say: Temporarily store the contents of the parameter node of the state 'At the restaurant' as `$`. The ***`$`-keyword*** is like a sticky note with all the values within the node written down on it. The node type of this state ({...}) is defined in the command definition as:
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
Again, the `$`-keyword is used to temporarily store each node within the collection `Order lines`.
So once we start to create the node in the collection `Order lines`, we derive the values for each container within the node by refering to `$` and from this `$` we want a specific container.
```js
		'Order line' = $ .'Provide an order line number'
		'Item' = $ .'Item to be consumed'
		'Amount' = $ .'Amount of this item'
```

The use of the `$`-keyword is not restricted to commands and can be applied throughout a model to refer to temporarily stored nodes or states.

As mentioned before, this is only an example of a command. Commands are commonly used to automatically create or change nodes or states without bothering the user with this or to transmit data from one app to another through an interface. More on the use of commands in interfaces in the tutorial 'Interfaces'.

> <tutorial folder: `./_docs/tutorials/restaurant1/step_06b/`>

>Before we continu with the next topic it is good to know that *reference-set* and *command* are also considered possible *attributes* for a container. The previously mentioned types *text*, *number*, *file*, *collection*, *stategroup* and *group* are more specifically *property attributes*, in short ***properties***, of the container. This in contrast to the *attributes* *reference-set* and *command*.

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
					from 'percent' >'Discount period' .'Percentage' as 'fraction',
					^ .'Subtotal'
				)
			)
		}
		'No' { }
	)

	'Total': number 'eurocent' = switch .'Discount applicable' (
		|'Yes' as $'discount' => sum ( $'discount' ^ .'Subtotal' , - $'discount' .'Discount' )
		|'No' => .'Subtotal'
	)

	'VAT': number 'eurocent' = product (
		from 'percent' ^ .'Management' .'VAT percentage' as 'fraction' ,
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

> <tutorial folder: `./_docs/tutorials/restaurant1/step_07/`>


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

> <tutorial folder: `./_docs/tutorials/restaurant1/step_08/`>

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

> <tutorial folder: `./_docs/tutorials/restaurant1/step_09/`>

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

> <tutorial folder: `./_docs/tutorials/restaurant1/step_10/`>

## The End
This concludes the tutorial into the `application` language.
You can now start building your own application, if you haven't done so already.

To learn more about the `application` language, we recommend you [read the docs](/pages/docs/model/89/application/grammar.html).
The documentation gives an overview of *all* features that the `application` language supports.
It also provides many useful examples that you can use while building your own application.

If you have questions, suggestions, or if you want to discuss the Alan platform, please go the [forum](https://forum.alan-platform.com/) that we have just set up for you.
