---
layout: doc
origin: project-build-environment
language: deployment
version: 34
type: grammar
---

1. TOC
{:toc}

## Deployment
---
In order to run an Alan application it needs to be deployed by an Alan Application Server.
A `deployment.alan` file contains instructions for the deployment, such as the source of the initial data and configuration.
### Application Servers
The `application-servers` section lists all the Application Servers needed for the deployment.
The Application Server performing the deployment can be referenced with the keyword `local`.

{: #grammar-rule--application-servers }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">application servers</span>': [ <span class="token operator">application-servers</span> ] dictionary {
	'<span class="token string">type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">remote</span>' {
			'<span class="token string">socket</span>': component <a href="#grammar-rule--tcp-socket">'tcp socket'</a>
		}
		'<span class="token string">host</span>' { [ <span class="token operator">local</span> ] }
	)
}
</pre>
</div>
</div>
### External Systems
The `wiring.alan` file declares which external sources your applications require.
In the `deployment.alan`, you need to provide the exact location of these sources.
For specifying a source location, you can use
- a TCP/IP address describing where the source excepts connections, or
- a path on an Alan Application Server, consisting of an `application-servers` name, a *stack* name and a `provided-connections` name, taken from the `wiring.alan` of the other stack.

{: #grammar-rule--external-systems }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">external systems</span>': [ <span class="token operator">external-systems</span> ] dictionary {
	'<span class="token string">mapping type</span>': [ <span class="token operator">:</span> ] stategroup (
		'<span class="token string">static</span>' {
			'<span class="token string">routing</span>': stategroup (
				'<span class="token string">direct</span>' {
					'<span class="token string">socket</span>': component <a href="#grammar-rule--tcp-socket">'tcp socket'</a>
				}
				'<span class="token string">application server</span>' {
					'<span class="token string">server</span>': reference
					'<span class="token string">stack</span>': [ <span class="token operator">/</span> ] text
					'<span class="token string">route</span>': [ <span class="token operator">/</span> ] text
				}
			)
		}
		'<span class="token string">dynamic</span>' {
			'<span class="token string">targets</span>': dictionary {
				'<span class="token string">server</span>': [ <span class="token operator">=</span> ] reference
				'<span class="token string">stack</span>': [ <span class="token operator">/</span> ] text
				'<span class="token string">route</span>': [ <span class="token operator">/</span> ] text
			}
		}
	)
}
</pre>
</div>
</div>
### Systems
The `systems` section provides deployment specific information for each system mentioned in a `wiring.alan` file.
Depending on the System Type, a system may require additional configuration, instance data, or a schedule.

#### Configuration
For systems requiring additional configuration, you can either
- use a template from a list of templates for the System Type, and override specific options, or
- use a `custom` configuration, where all options are set by the deployment.

#### Instance Data
Some systems require data to function (instance data).
To provide data for a system, you can either
- use the keyword `local` for the local file system, or
- use the keyword `from` followed by the name of an Application Server, to download the most recent version of the instance data from another stack.

At deploy time, transformations can be applied to your instance data.
A transformation can be
- a `migration`, transforming data conforming to an older model to instance data conforming to a new model, or
- a `conversion` from a list of predefined conversions for the System Type.

#### Schedule
Some systems require a schedule to perform tasks at specific moments in time.

{: #grammar-rule--systems }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">systems</span>': [ <span class="token operator">systems</span> ] dictionary {
	'<span class="token string">configuration</span>': [ <span class="token operator">configuration:</span> ] group {
		'<span class="token string">base</span>': stategroup (
			'<span class="token string">template</span>' {
				'<span class="token string">template</span>': reference
			}
			'<span class="token string">custom</span>' { [ <span class="token operator">custom</span> ] }
		)
		'<span class="token string">options</span>': dictionary {
			'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value-switch">'value switch'</a>
		}
	}
	'<span class="token string">instance data</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">instance-data:</span> ]
			'<span class="token string">source</span>': stategroup (
				'<span class="token string">local</span>' { [ <span class="token operator">local</span> ] }
				'<span class="token string">remote</span>' { [ <span class="token operator">from</span> ]
					'<span class="token string">server</span>': reference
					'<span class="token string">stack name</span>': [ <span class="token operator">/</span> ] text
					'<span class="token string">system name</span>': [ <span class="token operator">/</span> ] text
				}
			)
			'<span class="token string">transformations</span>': group { // TODO: dynamic-order
				'<span class="token string">migrate</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@migrate</span> ] }
					'<span class="token string">no</span>' { }
				)
				'<span class="token string">convert</span>': stategroup (
					'<span class="token string">yes</span>' { [ <span class="token operator">@conversion:</span> ]
						'<span class="token string">conversion</span>': reference
					}
					'<span class="token string">no</span>' { }
				)
			}
		}
		'<span class="token string">no</span>' { }
	)
	'<span class="token string">schedule</span>': stategroup (
		'<span class="token string">yes</span>' { [ <span class="token operator">schedule:</span> ]
			'<span class="token string">schedule</span>': component <a href="#grammar-rule--schedule">'schedule'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
## Component rules

{: #grammar-rule--tcp-socket }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">tcp socket</span>' {
	'<span class="token string">host</span>': text
	'<span class="token string">port</span>': integer
}
</pre>
</div>
</div>

{: #grammar-rule--value }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value</span>' {
	'<span class="token string">data type</span>': stategroup (
		'<span class="token string">choice</span>' {
			'<span class="token string">type</span>': stategroup (
				'<span class="token string">multiple</span>' {
					'<span class="token string">choices</span>': [ <span class="token operator">[</span>, <span class="token operator">]</span> ] dictionary { }
				}
				'<span class="token string">single</span>' {
					'<span class="token string">choice</span>': reference
				}
			)
		}
		'<span class="token string">number</span>' {
			'<span class="token string">value</span>': integer
		}
		'<span class="token string">text</span>' {
			'<span class="token string">value</span>': text
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--value-switch }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">value switch</span>' {
	'<span class="token string">type</span>': stategroup (
		'<span class="token string">singular</span>' {
			'<span class="token string">is set</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">value</span>': component <a href="#grammar-rule--value">'value'</a>
				}
				'<span class="token string">no</span>' { [ <span class="token operator">none</span> ] }
			)
		}
		'<span class="token string">plural</span>' {
			'<span class="token string">values</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] dictionary {
				'<span class="token string">value</span>': [ <span class="token operator">=</span> ] component <a href="#grammar-rule--value">'value'</a>
			}
		}
	)
}
</pre>
</div>
</div>

{: #grammar-rule--schedule }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">schedule</span>' {
	'<span class="token string">trigger</span>': stategroup (
		'<span class="token string">every day</span>' { [ <span class="token operator">every</span> <span class="token operator">day</span> ]
			'<span class="token string">trigger</span>': stategroup (
				'<span class="token string">every hour</span>' { [ <span class="token operator">every</span> <span class="token operator">hour</span> ]
					'<span class="token string">every</span>': component <a href="#grammar-rule--minute-list">'minute list'</a>
				}
				'<span class="token string">select hours</span>' {
					'<span class="token string">every</span>': component <a href="#grammar-rule--hour-list">'hour list'</a>
				}
			)
		}
		'<span class="token string">select days</span>' { [ <span class="token operator">every</span> ]
			'<span class="token string">sunday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Sunday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">monday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Monday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">tuesday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Tuesday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">wednesday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Wednesday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">thursday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Thursday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">friday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Friday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
			'<span class="token string">saturday</span>': stategroup (
				'<span class="token string">yes</span>' {
					'<span class="token string">day</span>': [ <span class="token operator">Saturday</span> ] component <a href="#grammar-rule--day">'day'</a>
				}
				'<span class="token string">no</span>' { }
			)
		}
		'<span class="token string">never</span>' { [ <span class="token operator">never</span> ] }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--day }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">day</span>' {
	'<span class="token string">every</span>': component <a href="#grammar-rule--hour-list">'hour list'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--hour-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">hour list</span>' {
	'<span class="token string">at hour</span>': [ <span class="token operator">at</span> ] integer
	'<span class="token string">at minute</span>': [ <span class="token operator">:</span> ] integer
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--hour-list">'hour list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>

{: #grammar-rule--minute-list }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">minute list</span>' {
	'<span class="token string">at minute</span>': [ <span class="token operator">at</span> ] integer
	'<span class="token string">has tail</span>': stategroup (
		'<span class="token string">yes</span>' {
			'<span class="token string">tail</span>': component <a href="#grammar-rule--minute-list">'minute list'</a>
		}
		'<span class="token string">no</span>' { }
	)
}
</pre>
</div>
</div>
