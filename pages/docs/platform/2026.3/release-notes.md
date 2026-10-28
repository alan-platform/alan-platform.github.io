---
layout: "doc"
origin: "platform"
language: "release notes"
version: "2026.3"
type: "release notes"
---
## 2026.3

Platform 2026.3 brings model 109, with partitions. A 2026.2 project first runs `./alan fetch`, which
brings the 2026.2 `alan` script that carries the upgrade command.

Run `./alan upgrade platform 2026.3` from the project root. `./alan upgrade` first fetches
the latest builds of the current versions, its own script included, then checks that the project
builds and every deployment packages, writes `versions.json`, fetches the bundles, runs the
transformations the new bundles ship for the old versions (interface, model, system types, in that
order), formats every directory of a changed component with the pretty printer, then builds,
compiles the migrations and packages every deployment. When one of these fails, the upgrade stops
and names the command that failed; every deployment can be checked on its own with `./alan package
dist/project.pkg deployments/<name>`. A stopped upgrade continues with `./alan upgrade`, and
`./alan upgrade --abort` ends it; `./alan upgrade --help` lists both. Its report lists every changed component with the path of its RELEASE.md, and
what is left by hand.

Deployments: a system deployed from a configuration template must now set every option of a plural
type with a static keyset in `deployment.alan`, as a custom system already had to; for such a system
these options used to be optional. For a connector system with `configuration: 'default'` these are
`'texts'` and `'integers'`, with a value for each of their keys. `./alan upgrade` does not fill them
in: choose each value (`instance/values.json` is not read). `./alan package` names every option that
is missing.

Session manager: 2026.3 publishes session-manager 35; 34 is withdrawn, do not deploy it. A 2026.3
project on 34 runs `./alan upgrade system-type session-manager`. Its configuration in every
`deployment.alan` changes by hand, `./alan upgrade` does not do this: delete `'token interval'` (a
session now lasts until its `'token limit'` or logout) and add `'openid authority client secrets'`,
keyed like `'openid authority client ids'`, `( )` when no authority has a secret. An OpenID login
now returns to `<base uri>oidc/resume`: register that address with the client at every provider
before the application moves to 35, or the provider refuses the login.
