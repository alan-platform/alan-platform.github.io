---
layout: "doc"
origin: "solver"
language: "interface-to-rcmpsp"
version: "0.3"
type: "grammar"
---

1. TOC
{:toc}


<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">trigger</span>': [ <span class="token operator">trigger</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--stategroup-attribute">'stategroup attribute'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">trigger options</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
	'<span class="token string">Start</span>': [ <span class="token operator">|</span> <span class="token operator">start</span> <span class="token operator">=></span> ] reference
	'<span class="token string">Stop</span>': [ <span class="token operator">|</span> <span class="token operator">stop</span> <span class="token operator">=></span> ] reference
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">timeout</span>': [ <span class="token operator">timeout</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--positive-number-attribute">'positive number attribute'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">resources</span>': [ <span class="token operator">resources</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">resource mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
	'<span class="token string">time slots</span>': [ <span class="token operator">time-slots</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
	'<span class="token string">time slots ordering</span>': [ <span class="token operator">in</span> ] reference
	'<span class="token string">time slot mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { }
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">worker pools</span>': [ <span class="token operator">worker-pools</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">worker pool mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
	'<span class="token string">weight</span>': [ <span class="token operator">weight</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--number-attribute">'number attribute'</a>
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">jobs</span>': [ <span class="token operator">jobs</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">job mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
	'<span class="token string">resource</span>': [ <span class="token operator">resource</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--reference-attribute">'reference attribute'</a>
	'<span class="token string">tasks</span>': [ <span class="token operator">tasks</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
	'<span class="token string">task mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
		'<span class="token string">dependencies</span>': [ <span class="token operator">dependencies</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
		'<span class="token string">dependency mapping</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group { }
		'<span class="token string">duration</span>': [ <span class="token operator">duration</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--positive-number-attribute">'positive number attribute'</a>
		'<span class="token string">worker pool</span>': [ <span class="token operator">worker-pool</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--reference-attribute">'reference attribute'</a>
		'<span class="token string">demand</span>': [ <span class="token operator">demand</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--positive-number-attribute">'positive number attribute'</a>
		'<span class="token string">scheduling</span>': [ <span class="token operator">scheduling</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--stategroup-attribute">'stategroup attribute'</a>
		'<span class="token string">scheduling options</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
			'<span class="token string">locked</span>': [ <span class="token operator">|</span> <span class="token operator">locked</span> <span class="token operator">=></span> ] reference
			'<span class="token string">locked parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
				'<span class="token string">start</span>': [ <span class="token operator">start</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--reference-attribute">'reference attribute'</a>
			}
			'<span class="token string">unlocked</span>': [ <span class="token operator">|</span> <span class="token operator">unlocked</span> <span class="token operator">=></span> ] reference
		}
	}
}
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command</span>': [ <span class="token operator">command</span> ] component <a href="#grammar-rule--command-attribute">'command attribute'</a>
</pre>
</div>
</div>

<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
	'<span class="token string">progress</span>': [ <span class="token operator">progress</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--stategroup-attribute">'stategroup attribute'</a>
	'<span class="token string">progress options</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
		'<span class="token string">running</span>': [ <span class="token operator">|</span> <span class="token operator">running</span> <span class="token operator">=></span> ] reference
		'<span class="token string">finished</span>': [ <span class="token operator">|</span> <span class="token operator">finished</span> <span class="token operator">=></span> ] reference
	}
	'<span class="token string">status</span>': [ <span class="token operator">status</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--stategroup-attribute">'stategroup attribute'</a>
	'<span class="token string">status options</span>': group {
		'<span class="token string">unsolved</span>': [ <span class="token operator">|</span> <span class="token operator">unsolved</span> <span class="token operator">=></span> ] reference
		'<span class="token string">unsolved parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
			'<span class="token string">unsolved cause</span>': [ <span class="token operator">unsolved-cause</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--stategroup-attribute">'stategroup attribute'</a>
			'<span class="token string">unsolved cause options</span>': group {
				'<span class="token string">unknown</span>': [ <span class="token operator">|</span> <span class="token operator">unknown</span> <span class="token operator">=></span> ] reference
				'<span class="token string">infeasible</span>': [ <span class="token operator">|</span> <span class="token operator">infeasible</span> <span class="token operator">=></span> ] reference
				'<span class="token string">model invalid</span>': [ <span class="token operator">|</span> <span class="token operator">model-invalid</span> <span class="token operator">=></span> ] reference
			}
		}
		'<span class="token string">solved</span>': [ <span class="token operator">|</span> <span class="token operator">solved</span> <span class="token operator">=></span> ] reference
		'<span class="token string">solved parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
			'<span class="token string">solution quality</span>': [ <span class="token operator">solution-quality</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--stategroup-attribute">'stategroup attribute'</a>
			'<span class="token string">solution quality options</span>': group {
				'<span class="token string">optimal</span>': [ <span class="token operator">|</span> <span class="token operator">optimal</span> <span class="token operator">=></span> ] reference
				'<span class="token string">feasible</span>': [ <span class="token operator">|</span> <span class="token operator">feasible</span> <span class="token operator">=></span> ] reference
			}
			'<span class="token string">jobs</span>': [ <span class="token operator">jobs</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
			'<span class="token string">job parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
				'<span class="token string">tasks</span>': [ <span class="token operator">tasks</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--collection-attribute">'collection attribute'</a>
				'<span class="token string">task parameters</span>': [ <span class="token operator">(</span>, <span class="token operator">)</span> ] group {
					'<span class="token string">start</span>': [ <span class="token operator">start</span> <span class="token operator">=</span> ] component <a href="#grammar-rule--reference-attribute">'reference attribute'</a>
				}
			}
		}
	}
}
</pre>
</div>
</div>

{: #grammar-rule--collection-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">collection attribute</span>' {
	'<span class="token string">attribute</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--number-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">number attribute</span>' {
	'<span class="token string">attribute</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--zero-or-positive-number-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">zero or positive number attribute</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--number-attribute">'number attribute'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--positive-number-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">positive number attribute</span>' {
	'<span class="token string">expression</span>': component <a href="#grammar-rule--zero-or-positive-number-attribute">'zero or positive number attribute'</a>
}
</pre>
</div>
</div>

{: #grammar-rule--reference-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">reference attribute</span>' {
	'<span class="token string">attribute</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--command-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">command attribute</span>' {
	'<span class="token string">attribute</span>': reference
}
</pre>
</div>
</div>

{: #grammar-rule--stategroup-attribute }
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
'<span class="token string">stategroup attribute</span>' {
	'<span class="token string">attribute</span>': reference
}
</pre>
</div>
</div>
