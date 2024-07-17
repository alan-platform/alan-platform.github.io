---
layout: "doc"
origin: "project-build-environment"
language: "project_wiring"
version: "43"
type: "grammar"
---

1. TOC
{:toc}

## The *minimal wiring*
---
Every Alan project needs a [`wiring`](#wiring).
The *minimal wiring* for a single Alan application with client, server, and authentication is

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
The wiring describes which components make up the Alan project, and how they interact with each other.
### Interfaces
If your application consumes data from, or provide data to another application, you need an Alan `interface`.
In the `interfaces` section of the wiring, you list the names of the `interface`s.
For each item in the list, you need a file `interfaces/<name>/interface.alan` in your project, which specifies the interface.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">interfaces</span>': [ <span class="token operator">interfaces</span> ] dictionary { }
</pre>
</div>
</div>
### Models
An Alan project typically has one Alan `application` model, but projects can have multiple `application` models.
For each item in the `models` section, you need a corresponding file `models/<name>/application.alan` in your project.

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">models</span>': [ <span class="token operator">models</span> ] dictionary { }
</pre>
</div>
</div>
### External Systems
If your application consumes data from external sources, you need to specify the types of these sources.
The type of an external source must be one of:
- `interface` when the data conforms to an Alan `interface`,
- `model` when the data conforms to an Alan `application` model, or
- when a custom protocol is used: the name of the protocol.

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
The internal `systems` are the active components of your Alan project.
Each system is an instance of a System Type, which defines the structure of the connection mapping.

The mapping of a system is divided into two mappings.
- the `project` mapping, which follows the project structure of the System Type
- the `consume` mapping, which is a list of additional connection of the System Type

Whether a mapping is required, depends on the System Type.
The compiler can tell you which one(s) you need.

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
	/* the configuration mapping */
	'<span class="token string">static keysets</span>': dictionary { [ <span class="token operator">keyset</span> ]
		'<span class="token string">keys</span>': [ <span class="token operator">=</span> <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
			'<span class="token string">secret</span>': stategroup (
				'<span class="token string">yes</span>' { [ <span class="token operator">secret</span> ] }
				'<span class="token string">no</span>' { }
			)
		}
	}
}
</pre>
</div>
</div>
### Provided Connections
The `provided-connections` section describes which parts of your systems can be accessed from the outside world.

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
## Components

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
