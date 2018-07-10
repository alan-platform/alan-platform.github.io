---
layout: doc
origin: datastore
language: deployment
version: 34
type: description
---

Instance data files for the server:
- **instance.json**: Data that matches the model, or migration.
  When migrating from scratch should contain `{}`.
- **config.json**: Datastore runtime options, see example below.
- **timestamp.txt**: The timestamp that is exported when creating a data dump.
- **backup.sh**, **cleanup.sh**: When you've configured a backup schedule,
  it runs the backup script followed by the cleanup script.

The `config.json` contains the runtime options. Option names are case-sensitive. When no options are specified, the system uses the default options as listed below:

```
{
  "DEBUG": false,
  "delay": 60,
  "policy": [ "write", "read_fast" ],
  "poolpolicy": [ "read_fast", "read_slow", "persist" ],
  "poolsize": 1
}
```

Available options:
- `DEBUG`: boolean, enable this flag to write instruction files to disk.
- `delay`: integer, seconds between connection attempts to external systems.
- `poolsize`: integer, number of *additional* datastores to start. Set to zero to run a single datastore process.
- `policy`, `poolpolicy`: a subset of the following flags, indicating the datastore(s) can be used for different types of requests:
  - `write`: mutations (this should **always** be set in `policy` and **never** be set in `poolpolicy`).
  - `read_fast`: small queries.
  - `read_slow`: large queries (e.g. reports).
  - `persist`: subscriptions.

The `policy` option applies to the primary datastore process and the `poolpolicy` option applies to all datastores in the pool.
If a flag is neither listed in the `policy` nor the `poolpolicy` option, no datastore is available to handle those types of requests.
If you choose to run with a `poolsize` of zero, **all** available flags should be listed in the `policy` option.

## support data deployment

```
/'instance.json' ( = required )
/'timestamp.txt' ( = optional )
/'config.json'   ( = required )
/'backup.sh'     ( = optional )
/'cleanup.sh'    ( = optional )
```

## support migration


## support schedule

```
