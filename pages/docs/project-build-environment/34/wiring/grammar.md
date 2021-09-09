---
layout: doc
origin: project-build-environment
language: wiring
version: 34
type: grammar
---

1. TOC
{:toc}

## The *basic wiring*
---
Every Alan application needs a [`wiring`](#wiring).
The minimal wiring for a simple server and client is

```js
interfaces

models
	'model'

external-systems

systems
	'server': 'datastore'
		project / (
			'interfaces' / (
				'providing' / ( )
				'consuming' / ( )
			)
			'model' = provide 'model'
		)

	'sessions': 'session-manager'
		project / (
			'model' = bind 'server'::'authenticate'
		)

	'client': 'auto-webclient'
		project / (
			'model' = consume 'server'/'model'
		)

provided-connections
	'auth'   = 'sessions'::'http'
	'client' = 'client'::'http'
```

## Wiring
---
The wiring of an application defines the individual components and how they interact with each other.
### Interfaces
If your application consumes or provides data from internal or external sources, you need to define an Alan `interface` for each source.

{: #grammar-rule--interfaces }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interfaces</span>': [ <span class="token operator">interfaces</span> ] dictionary { }
</pre>
</div>
</div>
### Models
An application usually only has one Alan `model`, but more complex application can have multiple models.

{: #grammar-rule--models }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">models</span>': [ <span class="token operator">models</span> ] dictionary { }
</pre>
</div>
</div>
### External Systems
If your application consumes data from external sources, you need to declare the type of these sources.
The type of an external source must be one of the following:
- `interface` when the data is defined by an Alan `interface`
- `model` when the data is defined by an Alan `model`.
- when a custom protocol is used, this should be the name of the protocol

{: #grammar-rule--external-systems }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">external systems</span>': [ <span class="token operator">external-systems</span> ] dictionary {
	'<span class="token string">is dynamic mapping</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">dynamic</span> ] }
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">library</span>' {
			'<span class="token string">binding</span>': stategroup (
				'<span class="token string">interface</span>' {
					'<span class="token string">interface</span>': [ <span class="token operator">interface</span> ] reference
				}
				'<span class="token string">model</span>' {
					'<span class="token string">model</span>': [ <span class="token operator">model</span> ] reference
				}
			)
		}
		'<span class="token string">protocol</span>' {
			'<span class="token string">type</span>': text
			'<span class="token string">binding</span>': stategroup (
				'<span class="token string">interface</span>' {
					'<span class="token string">interface</span>': [ <span class="token operator">bind</span> <span class="token operator">interface</span> ] reference
				}
				'<span class="token string">model</span>' {
					'<span class="token string">model</span>': [ <span class="token operator">bind</span> <span class="token operator">model</span> ] reference
				}
				'<span class="token string">none</span>' { }
			)
		}
	)
}
</pre>
</div>
</div>
### Internal Systems
The internal `systems` are the active components of an application.
Each system is an instance of a System Type, which defines the structure of the connection mapping.

The mapping of a system is divided into two mappings.
- the `project` mapping, which follows the project structure of the System Type
- the `consume` mapping, which is a list of additional connection of the System Type

Not all System Types have both mappings.

{: #grammar-rule--systems }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">systems</span>': [ <span class="token operator">systems</span> ] dictionary {
	'<span class="token string">has more systems</span>': stategroup = node-switch successor (
		| node = '<span class="token string">yes</span>' { '<span class="token string">next</span>' = successor }
		| none = '<span class="token string">no</span>'
	)
	'<span class="token string">system type</span>': [ <span class="token operator">:</span> ] reference
	/* the libraries mapping */
	'<span class="token string">map libraries</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">project</span> ]
			'<span class="token string">mapping</span>': component <a href="#grammar-rule--library-mapping">'library mapping'</a>
		}
		'<span class="token string">no</span>' { }
	)
	/* the consumed connections mapping */
	'<span class="token string">map connections</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">consume</span> ]
			'<span class="token string">connections</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">target</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--provider-selector">'provider selector'</a>
			}
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
### Provided Connections
The `provided-connections` define all the parts of the application that can be accessed from outside the application.

{: #grammar-rule--provided-connections }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">provided connections</span>': [ <span class="token operator">provided-connections</span> ] dictionary {
	'<span class="token string">system</span>': [ <span class="token operator">=</span> ] reference
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">library</span>' {
			'<span class="token string">library</span>': component <a href="#grammar-rule--library-selector">'library selector'</a>
		}
		'<span class="token string">connection</span>' {
			'<span class="token string">connection</span>': [ <span class="token operator">::</span> ] reference
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--library-mapping }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library mapping</span>' {
	'<span class="token string">step</span>': stategroup (
		'<span class="token string">directory mapping</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">/</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] stategroup (
				'<span class="token string">static mapping</span>' {
					'<span class="token string">children</span>': dictionary {
						'<span class="token string">mapping</span>': component <a href="#grammar-rule--library-mapping">'library mapping'</a>
					}
				}
				'<span class="token string">dynamic mapping</span>' {
					'<span class="token string">entries</span>': dictionary { [ <span class="token operator">[</span> ]
						'<span class="token string">mapping</span>': [ <span class="token operator">]</span> ] component <a href="#grammar-rule--library-mapping">'library mapping'</a>
					}
				}
			)
		}
		'<span class="token string">library mapping</span>' {
			'<span class="token string">type</span>': [ <span class="token operator">=</span> ] stategroup (
				'<span class="token string">provide</span>' { [ <span class="token operator">provide</span> ]
					'<span class="token string">library</span>': reference
				}
				'<span class="token string">consume</span>' { [ <span class="token operator">consume</span> ]
					'<span class="token string">target</span>': component <a href="#grammar-rule--provider-selection">'provider selection'</a>
				}
				'<span class="token string">bind</span>' { [ <span class="token operator">bind</span> ]
					'<span class="token string">target</span>': component <a href="#grammar-rule--provider-selection">'provider selection'</a>
				}
			)
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--library-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">library selector</span>' {
	'<span class="token string">has step</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">step</span>': [ <span class="token operator">/</span> ] reference
			'<span class="token string">tail</span>': component <a href="#grammar-rule--library-selector">'library selector'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--provider-selector }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">provider selector</span>' {
	'<span class="token string">target</span>': stategroup (
		'<span class="token string">external</span>' { [ <span class="token operator">external</span> ]
			'<span class="token string">system</span>': reference
		}
		'<span class="token string">internal connection</span>' {
			'<span class="token string">system</span>': reference
			'<span class="token string">connection</span>': [ <span class="token operator">::</span> ] reference
		}
		'<span class="token string">internal library</span>' {
			'<span class="token string">system</span>': reference
			'<span class="token string">library</span>': component <a href="#grammar-rule--library-selector">'library selector'</a>
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--provider-selection }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">provider selection</span>' {
	'<span class="token string">select</span>': stategroup (
		'<span class="token string">single</span>' {
			'<span class="token string">target</span>': component <a href="#grammar-rule--provider-selector">'provider selector'</a>
		}
		'<span class="token string">multiple</span>' {
			'<span class="token string">system</span>': [ <span class="token operator">dynamic</span> <span class="token operator">external</span> ] reference
		}
	)
}
</pre>
</div>
</div>
