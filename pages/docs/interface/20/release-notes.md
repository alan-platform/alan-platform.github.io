---
layout: "doc"
origin: "interface"
language: "release notes"
version: "20"
type: "release notes"
---
## 20 (after 19)

- Interface subscription language: the `no-init` option is gone; a subscription always receives the initialization data. Remove `no-init` from subscriptions.
- The builds of version 20 since platform 2026.2 change only the library behind the language (an event-driven API) and ship an agent guide (AGENTS.md). A project already on interface 20 has nothing to upgrade.
