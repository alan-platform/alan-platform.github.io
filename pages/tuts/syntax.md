---
layout: page
title: "Alan Grammars"
category: docs
---

## How to read grammars

The documentation for the Alan languages describes the syntax of those languages in the form of an Alan grammar,
often accompanied by a description and/or examples.
An Alan grammar describes what you can write in an Alan file:
the keywords to use, values to provide, and options to choose from.

### Keywords
The orange literals between square brackets indicate required keywords.
A comma indicates if keywords go before or after a property value. For example:

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">name</span>' [ <span class="token operator">&</span> ] text     // means: & <b>before</b> a text value: &"Alice"
'<span class="token string">name</span>' [ <span class="token operator">&</span> , <span class="token operator">*</span> ] text // means: & <b>before</b> and * <b>after</b> a text value: &"Alice"*
'<span class="token string">name</span>' [ , <span class="token operator">*</span> ] text   // means: * <b>after</b> a text value: "Alice"*
</pre>
</div>
</div>

### Properties

- `text` properties require a double quoted string: **`"Alice"`**
- `reference` properties require a single quoted string: **`'reference to Bob'`**
- `number` properties require a number value: **`10`**
- `stategroup` properties indicate a *choice* between different states, such as allowing or disallowing `anonymous` users
- `dictionary` properties require *key-value pairs*, where keys are single-quoted strings (`'Alice' 'Bob'`).
- `component` properties reference a rule in the grammar, to be instantiated at that point: `component 'abc'` references rule `'abc'`
- `group` properties just group properties that belong together

For example, suppose that we have the following grammar where an Alan file expects a `dictionary` of `'users'` with user specific fields `'age'` and a choice between a `red` and a `blue` `pill`:

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">users</span>' dictionary { [ <span class="token operator">User</span> ]      // keyword User comes before the user key
	'<span class="token string">age</span>': [ <span class="token operator">:</span> ] number            // keyword : comes before a number value
	'<span class="token string">pill</span>': [ , <span class="token operator">!</span> ] stategroup (   // choose a pill, followed by !
		'<span class="token string">red</span>' { [ <span class="token operator">R</span> ] }            // 'red' requires keyword R
		'<span class="token string">blue</span>' { [ <span class="token operator">B</span> ] }           // 'blue' requires keyword B
	)
}
</pre>
</div>
</div>

then a valid model is:

```js
// your model file (e.g. application.alan)
User 'Alice' : 42 R !
User 'Bob'   : 43 B !
```

Note that properties with an `=`-sign like `stategroup = ` do not require your input, as the compiler derives them for you.

## Typical quirks of the Alan compiler

- Keywords should be separated by whitespace, so `()` doesn't work but `( )` does.
- Quotes are recognized as something special, so you *can* write `'type':` and `?'state group'|'state'`.
- Only *tabs* are accepted for indentation.
