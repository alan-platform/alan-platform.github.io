---
layout: "doc"
origin: "project-build-environment"
language: "release notes"
version: "45"
type: "release notes"
---
## 45

- Deployment language: a system deployed from a template must set its configuration options of a plural type with a static keyset, as a custom system already had to.
- System-type contract: a system type can provide a static interface. A wiring connects it with `= provide static`; `= provide '<library>'` is unchanged.
- Wiring language: the compatibility of interface and model types between provider and consumer is enforced as a constraint.
- Platforms: darwin-arm64 replaces darwin-x64; the linux-aarch64 build is no longer published.
- The package ships an agent guide (AGENTS.md).

Upgrade: a system deployed from a template requires every configuration option of a plural type with a static
keyset, such as the `'integers'` and `'texts'` options of a connector system. `./alan upgrade` does not add them;
packaging the deployment reports each missing one, for example ``missing entry `integers` in 'options'``. Add each
option to `deployment.alan`: `( )` when its keyset in `wiring.alan` is empty, otherwise an entry for every key, with
the value that system needs:

```
'pdf-generator'
	configuration: 'default'
		'slow speed' = 30
		'slow time'  = 60
		'integers'   = ( )
		'texts'      = (
			'pdf_generator_url' = "http://127.0.0.1:5044/v1/generate"
		)
```
