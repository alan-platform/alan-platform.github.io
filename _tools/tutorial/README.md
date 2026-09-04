# Tutorial snippet tools

`snippets.py extract VERSION --write` regenerates committed snippets.
`snippets.py verify VERSION --platform DEVENV` checks models, snippets, and pages.
`snippets.py census VERSION` reports marker inventory.

Markers live in `models/*/application.alan`:

- `//@ begin NAME [strip-comments]` and `//@ end NAME [cut="TEXT"]`
- `//@ hide [NAME...]`, `//@ skip [NAME...]`, `//@ show [NAME...]`
- `//@ all NAME`
- `//@ expect error TEXT` or `//@ expect warning TEXT`

Regions may nest, overlap, and repeat. Hidden sections become one indented `...`.
Generated snippets have no trailing newline and markdown fences include them with
`{% include_relative snippets/NAME.alan %}`.

`fetch-toolchain.sh VERSION` obtains a compatible devenv. `upgrade-model.sh` and
`upgrade-migration.sh` update copied tutorial material. `new-version.sh NEW [PREV]`
runs full version-copy workflow.

Never pretty-print `pages/tutorials/model/*/models/` in place: marker positions and
tutorial prose depend on source layout.

## Upgrading to a new platform version

`new-version.sh NEW PREV` copies both tutorial trees, runs the platform's model transform and migration
upgrade, regenerates snippets, verifies, runs online-ide `test.sh`, and prints a report. Models that carry
`//@ expect error` cannot be transformed (the transform needs a model that compiles under the old language):
apply the syntax change to them by hand and rerun `snippets.py verify NEW --platform DEVENV`. The transform
re-emits the models it touches in canonical formatting, so hand-wrapped lines in those models are lost.
Promoting `_data/versions.json` `current` is a separate, manual commit. A version entry there may carry an `alan`
field with the URL of that platform version's `alan` script (`https://dist.alan-platform.com/share/versions/VERSION/alan`);
`pages/docs.md` shows a quickstart for the newest version that has one, and `_includes/doc-archive.html` links it per version.
