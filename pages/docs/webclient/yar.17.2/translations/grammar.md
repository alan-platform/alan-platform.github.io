---
layout: "doc"
origin: "webclient"
language: "translations"
version: "yar.17.2"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">language</span>': [ <span class="token operator">language:</span> ] text
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">engine language</span>': [ <span class="token operator">engine</span> <span class="token operator">language:</span> ] stategroup (
	'<span class="token string">english</span>' { [ <span class="token operator">english</span> ] }
	'<span class="token string">dutch</span>' { [ <span class="token operator">dutch</span> ] }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">translations</span>': dictionary {
	'<span class="token string">translation</span>': [ <span class="token operator">:</span> ] text
}
</pre>
</div>
</div>
