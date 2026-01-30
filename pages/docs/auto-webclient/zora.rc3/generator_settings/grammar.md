---
layout: "doc"
origin: "auto-webclient"
language: "generator_settings"
version: "zora.rc3"
type: "grammar"
---

1. TOC
{:toc}

### Settings
Global settings for the user interface:

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application creator</span>': [ <span class="token operator">application</span> <span class="token operator">creator:</span> ] text
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">allow anonymous user</span>': [ <span class="token operator">anonymous</span> <span class="token operator">login:</span> ] stategroup (
	'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
	'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">enable csv actions</span>': [ <span class="token operator">csv</span> <span class="token operator">actions:</span> ] stategroup (
	'<span class="token string">no</span>' { [ <span class="token operator">disabled</span> ] }
	'<span class="token string">yes</span>' { [ <span class="token operator">enabled</span> ] }
)
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">report limit</span>': [ <span class="token operator">report</span> <span class="token operator">limit:</span> ] integer
</pre>
</div>
</div>

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
'<span class="token string">generator</span>': [ <span class="token operator">generator:</span> ] reference
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">has landing page</span>': stategroup (
	'<span class="token string">yes</span>' { [ <span class="token operator">landing-page:</span> ]
		'<span class="token string">from</span>': stategroup (
			'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
			'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
		)
		'<span class="token string">expression</span>': component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
	}
	'<span class="token string">no</span>' { }
)
</pre>
</div>
</div>

{: #grammar-rule--ancestor-node-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor node path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--landing-page-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">landing page path</span>' {
	'<span class="token string">from</span>': stategroup (
		'<span class="token string">current</span>' {
			'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
		}
		'<span class="token string">user</span>' { [ <span class="token operator">user</span> ] }
		'<span class="token string">root</span>' { [ <span class="token operator">root</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--landing-page-branches }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">landing page branches</span>' {
	'<span class="token string">branch</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
	'<span class="token string">has alternative</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">alternative</span>': component <a href="#grammar-rule--landing-page-branches">'landing page branches'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--landing-page-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">landing page selector</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">group step</span>' {
			'<span class="token string">group</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		}
		'<span class="token string">state switch</span>' { [ <span class="token operator">switch</span> ]
			'<span class="token string">stategroup</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">cases</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary { [ <span class="token operator">|</span> ]
				'<span class="token string">path</span>': [ <span class="token operator">=></span> ] component <a href="#grammar-rule--ancestor-node-path">'ancestor node path'</a>
				'<span class="token string">tail</span>': component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
			}
		}
		'<span class="token string">reference step</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">reference</span>' {
					'<span class="token string">reference</span>': [ <span class="token operator">></span> ] reference
				}
				'<span class="token string">property rule</span>' {
					'<span class="token string">property</span>': [ <span class="token operator">.</span> ] reference
					'<span class="token string">rule</span>': [ <span class="token operator">&</span> ] reference
				}
				'<span class="token string">context rule</span>' {
					'<span class="token string">rule</span>': [ <span class="token operator">.&</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		}
		'<span class="token string">collection lookup</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">tail</span>': [ <span class="token operator">[</span> <span class="token operator">user</span> <span class="token operator">]</span> ] component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		}
		'<span class="token string">branches</span>' {
			'<span class="token string">list</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--landing-page-branches">'landing page branches'</a>
		}
		'<span class="token string">page select</span>' { [ <span class="token operator">open</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">reports</span>' { [ <span class="token operator">reports</span> ] }
				'<span class="token string">todos</span>' { [ <span class="token operator">todos</span> ] }
				'<span class="token string">entity view</span>' { [ <span class="token operator">entity</span> ]
					'<span class="token string">entity</span>': component <a href="#grammar-rule--landing-page-path">'landing page path'</a>
				}
				'<span class="token string">collection view</span>' { [ <span class="token operator">collection</span> ]
					'<span class="token string">attribute</span>': reference
				}
				'<span class="token string">global feature</span>' { [ <span class="token operator">global-feature</span> ]
					'<span class="token string">feature</span>': reference
				}
			)
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
	)
}
</pre>
</div>
</div>
