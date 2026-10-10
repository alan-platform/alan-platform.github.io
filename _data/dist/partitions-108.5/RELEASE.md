# Release Notes

## partitions-108.5 (after before-partitions.1)

Test release of the partitions platform. It upgrades from before-partitions.1, a test platform
with the system-type versions of 2026.2 and an `alan` script that carries the upgrade command;
2026.2 itself follows once its updated `alan` script is published.

Run `./alan upgrade platform partitions-108.5` from the project root. `./alan upgrade` first fetches
the latest builds of the current versions, its own script included, then checks that the project
builds, writes `versions.json`, fetches the bundles, runs the transformations the new bundles ship
for the old versions (interface, model, system types, in that order), formats every directory of a
changed component with the pretty printer, then builds, compiles the migrations and packages every
deployment. A stopped upgrade continues with `./alan upgrade`, and `./alan upgrade --abort` ends
it; `./alan upgrade --help` lists both. Its report lists every changed component with the path of
its RELEASE.md, and what is left by hand.
