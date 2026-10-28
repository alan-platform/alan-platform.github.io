---
layout: "doc"
origin: "auto-webclient"
language: "parameters"
version: "zora.rc6"
type: "grammar"
url: "/pages/docs/auto-webclient/zora.rc6/parameters/grammar.html"
toc: true
---



<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">context type</span>': component <a href="#grammar-rule--plural-type-selector">'plural type selector'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">parameters</span>': [ <span class="token operator">parameters:</span> ] dictionary {
	'<span class="token string">has successor</span>': stategroup = node-switch successor (
		| node = '<span class="token string">yes</span>' { '<span class="token string">successor</span>' = successor }
		| none = '<span class="token string">no</span>'
	)
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">number</span>' { [ <span class="token operator">number</span> ]
			'<span class="token string">numerical type</span>': reference
		}
		'<span class="token string">text</span>' { [ <span class="token operator">text</span> ] }
	)
}
</pre>
</div>
</div>

<div id="grammar-rule--singular-type-selector" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">singular type selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--singular-type-selector">'singular type selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

<div id="grammar-rule--conditional-type-selector" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">conditional type selector</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--singular-type-selector">'singular type selector'</a>
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">state</span>': [ <span class="token operator">?</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--conditional-type-selector">'conditional type selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

<div id="grammar-rule--plural-type-selector" class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">plural type selector</span>' {
	'<span class="token string">head</span>': component <a href="#grammar-rule--conditional-type-selector">'conditional type selector'</a>
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': [ <span class="token operator">.</span>, <span class="token operator">*</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--plural-type-selector">'plural type selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
