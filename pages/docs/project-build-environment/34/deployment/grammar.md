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
In order to run an Alan application it needs to be deployed to the Application Server.
The Alan `deployment` contains instructions for the deployment, such as the source of the initial data and configuration.
### Application Servers
The `application-servers` lists all the Application Servers required for the deployment.
For the Application Server performing the deployment can be referred to with `local`.

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
The Alan `wiring` declared the external sources required by the application.
In the deployment, you need to specify the exact location of the sources.
A source can be specified as either
- a TCP/IP address where the source excepts connections
- a path on an Application Server, the path consists of the `application-servers` name, the stack name and the `provided-connections` name from that stacks wiring.

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
Here we provide deployment specific information for each system in the wiring.

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
#### Configuration
Some System Types require additional configuration.
To configure a system, you can either
- use a template provided by the System Type and override specific options
- use a `custom` configuration, where all options are set by the deployment
#### Instance Data
Some System Types require instance data.
To provide data to a system, you can either
- use `local` for the local file system
- use `from` Application Server to download the most recent version of the instance data of another stack

In addition to the source of the instance data, transformations can be applied at deploy time to the data.
This can be either
- a `migration` to transform data for an older model to the current model
- a `conversion` to apply a predefined transformation to the data, the available conversions are defined by the System Type
### Schedule
Some System Types require a schedule to perform tasks at specific moments in time.

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
