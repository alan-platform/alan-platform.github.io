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

Upgrade: a deployment whose template-based system leaves out such an option no longer builds; add the option to `deployment.alan`.
