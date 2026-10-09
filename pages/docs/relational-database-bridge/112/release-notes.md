---
layout: "doc"
origin: "relational-database-bridge"
language: "release notes"
version: "112"
type: "release notes"
---
## 112 (after 111)

- The command gateway is gone: a relational-database-bridge system no longer has a `config.alan` (its `command-gateway` section configured the protocol for commands), and the bundle no longer ships the WSDL generator.
- `generate-queries.sh` and `map-results.sh` no longer build the system first. Build it with `./alan b` before you run them.

### After the upgrade
- Remove `config.alan` from every relational-database-bridge system directory.
