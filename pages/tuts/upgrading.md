---
layout: page
title: "Upgrading a project"
category: docs
description: >-
  Move a project to a newer platform version with ./alan upgrade, or let an AI coding agent do it.
---

`./alan upgrade` moves a project to a newer platform version.
It writes the new versions into `versions.json`, fetches them, converts the files for which the new versions ship a conversion, formats them, builds the project, packages every deployment, and ends with a report of what is left to do by hand.
The project must build with its current versions before you start.
The upgrade changes the files of the project in place, so commit or back up the project first.

The details are in the `AGENTS.md` that `./alan fetch` puts in the project, and in `./alan upgrade --help`.

## With an AI coding agent

Open the project in your editor and give the agent this prompt:

``` {.copy}
Run ./alan f to update AGENTS.md, then upgrade this project to platform 2026.3.
```

The agent runs the upgrade, fixes what the build reports with the release notes at hand, and goes through the report.
Use a strong model at a high thinking effort: in our tests, Claude Opus at effort xhigh did best (max was not tested).
Review its changes before you deploy.

## By hand

```sh
./alan upgrade platform 2026.3
```

When the upgrade stops, fix the cause and run `./alan upgrade` again; `./alan upgrade --prompt` says what is left.
`./alan upgrade --abort` abandons an upgrade that has not finished.

On Windows, run `./alan` in Git Bash.

## From 2026.2

A 2026.2 project gets the upgrade command with `./alan fetch`: the first step of the prompt above, or run it by hand.
Then upgrade as above; nothing else changes.
