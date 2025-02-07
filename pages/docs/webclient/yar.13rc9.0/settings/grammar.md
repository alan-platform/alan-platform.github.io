---
layout: "doc"
origin: "webclient"
language: "settings"
version: "yar.13rc9.0"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">settings</span>': [ <span class="token operator">settings</span> ] group {
	'<span class="token string">application creator</span>': [ <span class="token operator">application</span> <span class="token operator">creator</span> <span class="token operator">:</span> ] reference
	'<span class="token string">application name</span>': [ <span class="token operator">application</span> <span class="token operator">name</span> <span class="token operator">:</span> ] reference
	'<span class="token string">default language</span>': [ <span class="token operator">default</span> <span class="token operator">language</span> <span class="token operator">:</span> ] reference
	'<span class="token string">allow anonymous user</span>': [ <span class="token operator">anonymous</span> <span class="token operator">login</span> <span class="token operator">:</span> ] stategroup (
		'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
		'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
	)
	'<span class="token string">reload on unexpected error</span>': [ <span class="token operator">reload</span> <span class="token operator">on</span> <span class="token operator">unexpected</span> <span class="token operator">error</span> <span class="token operator">:</span> ] stategroup (
		'<span class="token string">enabled</span>' { [ <span class="token operator">enabled</span> ] }
		'<span class="token string">disabled</span>' { [ <span class="token operator">disabled</span> ] }
	)
	'<span class="token string">content selection</span>': [ <span class="token operator">content</span> <span class="token operator">selection</span> <span class="token operator">:</span> ] stategroup (
		'<span class="token string">enabled</span>' { [ <span class="token operator">enabled</span> ] }
		'<span class="token string">disabled</span>' { [ <span class="token operator">disabled</span> ] }
	)
	'<span class="token string">report limit</span>': [ <span class="token operator">report</span> <span class="token operator">limit</span> <span class="token operator">:</span> ] integer
	'<span class="token string">announcement title</span>': [ <span class="token operator">announcement</span> <span class="token operator">:</span> ] text
	'<span class="token string">announcements</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] dictionary { }
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">windows</span>': [ <span class="token operator">windows</span> ] dictionary { }
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">allow deeplink</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">deeplink</span> <span class="token operator">to</span> <span class="token operator">:</span> ]
		'<span class="token string">target window</span>': reference
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>
