---
layout: page
title: "Alan grammar syntax"
category: docs
---


# Syntax

## How to read grammars

### Keywords
- Literals between square brackets indicate required keywords, where a comma indicates if keywords go before or after a property value. For example:

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
<!-- <code> -->
'<span class="token string">name</span>' [ <span class="token operator">&</span> ] text     // means: & <b>before</b> a text value: &"Alice"
'<span class="token string">name</span>' [ <span class="token operator">&</span> , <span class="token operator">*</span> ] text // means: & <b>before</b> and * <b>after</b> a text value: &"Alice"*
'<span class="token string">name</span>' [ , <span class="token operator">*</span> ] text   // means: * <b>after</b> a text value: "Alice"*
<!-- </code> -->
</pre>
</div>
</div>

### Properties

- `text` properties require a double quoted string: **`"Alice"`**
- `reference` properties require a single quoted string: **`'reference to Bob'`**
- `number` properties require a number value: **`10`**
- `stategroup` properties indicate a *choice* between different states, such as allowing or disallowing `anonymous` users
- `collection` properties require *key-value pairs*, where keys are single-quoted strings. For example, a `collection` of `properties` is written like this, depending on the required keywords and properties for the value:

```js
'First Name': text = "Alice"
'Last Name': text = "Ecila"
```

- `component` properties reference a rule in the grammar, to be instantiated at that point: `component 'abc'` references rule `'abc'`
- `group` properties just group properties that belong together

Properties with an `=`-sign like `stategroup = ` do not require your input, as the compiler derives them for you.

## Typical quirks of the Alan compiler

- Keywords should be separated by whitespace, so `()` doesn't work but `( )` does.
- Quotes are recognized as something special, so you *can* write `'type':` and `?'state group'|'state'`.
- Only *tabs* are accepted for indentation.
