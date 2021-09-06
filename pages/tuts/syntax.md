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

For example, take the following extract from the grammar of the application language:

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">node</span>' { [ <span class="token operator">{</span> , <span class="token operator">}</span> ]                       // curly braces wrap a node type
	'<span class="token string">attributes</span>' dictionary {            // an attribute starts with a key, followed by
		'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (       // a chosen type, preceded by keyword :
			'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }          // 'text' requires keyword text
			'<span class="token string">number</span>' { [ <span class="token operator">number</span> ] }      // 'number' requires keyword number
		)
	}
}
</pre>
</div>
</div>

then a valid model is:

```js
// application.alan (your model file)
{
	'A': text
	'B': number
}
```

Note that properties with an `=`-sign like `stategroup = ` do not require your input, as the compiler derives them for you.

## Typical quirks of the Alan compiler

- Keywords should be separated by whitespace, so `()` doesn't work but `( )` does.
- Quotes are recognized as something special, so you *can* write `'type':` and `?'state group'|'state'`.
- Only *tabs* are accepted for indentation.
