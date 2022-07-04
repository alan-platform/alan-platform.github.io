---
layout: doc
origin: connector
language: variables
version: 34.dev.1
type: grammar
---

1. TOC
{:toc}

#### Instance Data
Every `connector` has a `variables.alan` file where a set of key value-type pairs is specified.
The connector requires a `values.json` instance data file, this provides the value (of the correct type) for each of these keys.
The `values.json` file is required and must also be provided when no keys are specified.
During deployments the runtime validates the provided values and fails when either:

* a value is missing
* a value is of the wrong type
* a superfluous value is present

To help with ensuring a correct `values.json` file before deployments, the `values-helper` tool is provided.
This can be run from any project with the follow command:

```
./.alan/dataenv/system-types/connector/scripts/generate_values.sh <Path-To-System> <Path-To-Deployment>

Example: ./.alan/dataenv/system-types/connector/scripts/generate_values.sh systems/currency-importer ./deployment/demo
```

The tool is interactive and always prompts the user before deleting any data from an existing `values.json`.
Once a new version of `values.json` has been written, which is guaranteed to be accepted by the server, the following message is printed:

```
Values successfully updated
```
#### Variables
The variables.
Each has a type of `integer` or `text`.
The values of each variable is specified in the deployment, see Instance Data.

{: #grammar-rule--variables }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">variables</span>': dictionary { [ <span class="token operator">var</span> ]
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">integer</span>' { [ <span class="token operator">integer</span> ] }
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
}
</pre>
</div>
</div>
