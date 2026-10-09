---
layout: "doc"
origin: "session-manager"
language: "interface"
version: "partitions-108.5"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">enable password authentication</span>': [ <span class="token operator">password-authentication:</span> ] stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
	'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">enable user creation</span>': [ <span class="token operator">user-creation:</span> ] stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
	'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">enable user linking</span>': [ <span class="token operator">user-linking:</span> ] stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
	'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
)
</pre>
</div>
</div>
