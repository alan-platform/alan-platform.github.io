---
layout: doc
origin: auto-webclient
language: deployment
version: neo.2rc2
type: description
---

Images to be supplied to the client to customize its appearance:
- **favicon.ico**:         bookmark icon (required)
- **logo.png**:            94x94 logo to be displayed at login
- **logo-sideways.png**:   38x76 logo for the application sidebar

Note that logo's are resized to fit and should be supplied at 2x the specified
resolution or larger to be crsip on high dpi displays.

- **config.json**          Configuration options for the client.
 An example:

{
	"include data in error log": true // include (potentially sensitive) data in error reports.
}
<div class="language-js highlighter-rouge">
<div class="highlight">
<pre class="highlight language-js code-custom">
/'<span class="token string">logo.png</span>'   ( = optional )
/'<span class="token string">logo-sideways.png</span>' ( = optional )
/'<span class="token string">favicon.ico</span>'   ( = required )
/'<span class="token string">config.json</span>' ( = optional )
</pre>
</div>
</div>
</pre>
</div>
</div>
