---
layout: doc
origin: auto-webclient
language: generator_settings
version: q.handheld.1
type: grammar
---

1. TOC
{:toc}

### Settings
Global settings for the user interface:

{: #grammar-rule--application-creator }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application creator</span>': [ <span class="token operator">application</span> <span class="token operator">creator:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--application-name }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application name</span>': [ <span class="token operator">application</span> <span class="token operator">name:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--allow-anonymous-user }
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

{: #grammar-rule--enable-csv-actions }
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

{: #grammar-rule--report-limit }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">report limit</span>': [ <span class="token operator">report</span> <span class="token operator">limit:</span> ] integer
</pre>
</div>
</div>

{: #grammar-rule--announcement-title }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">announcement title</span>': [ <span class="token operator">announcement:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--announcements }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">announcements</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] dictionary { @block indent }
</pre>
</div>
</div>

{: #grammar-rule--custom-color-theme }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">custom color theme</span>': stategroup (
	'<span class="token string">no</span>' { }
	'<span class="token string">yes</span>' { [ <span class="token operator">color</span> <span class="token operator">theme:</span> ]
		'<span class="token string">foreground</span>': [ <span class="token operator">foreground:</span> ] text
		'<span class="token string">background</span>': [ <span class="token operator">background:</span> ] text
		'<span class="token string">brand</span>': [ <span class="token operator">brand:</span> ] text
		'<span class="token string">link</span>': [ <span class="token operator">link:</span> ] text
		'<span class="token string">accent</span>': [ <span class="token operator">accent:</span> ] text
		'<span class="token string">success</span>': [ <span class="token operator">success:</span> ] text
		'<span class="token string">warning</span>': [ <span class="token operator">warning:</span> ] text
		'<span class="token string">error</span>': [ <span class="token operator">error:</span> ] text
		'<span class="token string">blue</span>': [ <span class="token operator">blue:</span> ] text
		'<span class="token string">orange</span>': [ <span class="token operator">orange:</span> ] text
		'<span class="token string">green</span>': [ <span class="token operator">green:</span> ] text
		'<span class="token string">red</span>': [ <span class="token operator">red:</span> ] text
		'<span class="token string">purple</span>': [ <span class="token operator">purple:</span> ] text
		'<span class="token string">teal</span>': [ <span class="token operator">teal:</span> ] text
	}
)
</pre>
</div>
</div>

{: #grammar-rule--language }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">language</span>': [ <span class="token operator">language:</span> ] text
</pre>
</div>
</div>

{: #grammar-rule--engine-language }
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

{: #grammar-rule--generator }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">generator</span>': stategroup (
	'<span class="token string">default</span>' { }
	'<span class="token string">handheld</span>' { [ <span class="token operator">generator:</span> <span class="token operator">handheld</span> ] }
)
</pre>
</div>
</div>

{: #grammar-rule--has-landing-page }
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

{: #grammar-rule--ancestor-entity-path }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">ancestor entity path</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">^</span> ]
			'<span class="token string">tail</span>': component <a href="#grammar-rule--ancestor-entity-path">'ancestor entity path'</a>
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
			'<span class="token string">path</span>': component <a href="#grammar-rule--ancestor-entity-path">'ancestor entity path'</a>
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
				'<span class="token string">tail</span>': component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
			}
		}
		'<span class="token string">reference step</span>' {
			'<span class="token string">text</span>': [ <span class="token operator">></span> ] reference
			'<span class="token string">output</span>': stategroup (
				'<span class="token string">node</span>' { }
				'<span class="token string">parameter</span>' {
					'<span class="token string">parameter</span>': [ <span class="token operator">$</span> ] reference
				}
			)
			'<span class="token string">tail</span>': component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		}
		'<span class="token string">collection lookup</span>' {
			'<span class="token string">collection</span>': [ <span class="token operator">.</span> ] reference
			'<span class="token string">require</span>': [ <span class="token operator">[</span> <span class="token operator">user</span> ] stategroup (
				'<span class="token string">key constraint</span>' { [ <span class="token operator">></span> ] }
				'<span class="token string">key hint</span>' { [ <span class="token operator">:></span> ] }
			)
			'<span class="token string">tail</span>': [ <span class="token operator">]</span> ] component <a href="#grammar-rule--landing-page-selector">'landing page selector'</a>
		}
		'<span class="token string">branches</span>' {
			'<span class="token string">list</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] component <a href="#grammar-rule--landing-page-branches">'landing page branches'</a>
		}
		'<span class="token string">page select</span>' { [ <span class="token operator">open</span> ]
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">reports</span>' { [ <span class="token operator">reports</span> ] }
				'<span class="token string">todos</span>' { [ <span class="token operator">todos</span> ] }
				'<span class="token string">dashboard</span>' { [ <span class="token operator">dashboard</span> ] }
				'<span class="token string">entity view</span>' { [ <span class="token operator">entity</span> ]
					'<span class="token string">entity</span>': component <a href="#grammar-rule--landing-page-path">'landing page path'</a>
				}
				'<span class="token string">collection view</span>' { [ <span class="token operator">collection</span> ]
					'<span class="token string">attribute</span>': reference
				}
			)
		}
		'<span class="token string">none</span>' { [ <span class="token operator">none</span> ] }
	)
}
</pre>
</div>
</div>
