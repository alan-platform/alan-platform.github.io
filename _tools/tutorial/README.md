# Tutorial snippet tools

`snippets.py extract VERSION --write` regenerates committed snippets.
`snippets.py verify VERSION --platform DEVENV` checks models, snippets, and pages.
`snippets.py census VERSION` reports marker inventory.
All three take `--tutorial model|migrations` (default `model`) to select `pages/tutorials/<tutorial>/VERSION`.

A `models/<dir>` is a model project (`application.alan`, compiled with the model language) or a migration
project (`migration.alan` plus `models/source/application.alan`, `models/target/application.alan`,
`configuration.json`, `variables.json`, `interface.alan`; compiled with the datastore migration language).
Markers may appear in `migration.alan` and in the source and target models.

Markers live in `models/*/application.alan`:

- `//@ begin NAME [strip-comments]` and `//@ end NAME [cut="TEXT"]`
- `//@ hide [NAME...]`, `//@ skip [NAME...]`, `//@ show [NAME...]`
- `//@ all NAME`
- `//@ expect error TEXT` or `//@ expect warning TEXT`

Regions may nest, overlap, and repeat. Hidden sections become one indented `...`.
Generated snippets have no trailing newline and markdown fences include them with
`{% include_relative snippets/NAME.alan %}`.

`fetch-toolchain.sh VERSION` obtains a compatible devenv. `upgrade-model.sh` transforms one model dir,
`upgrade-migration.sh` converts one online-ide step migration (legacy layout), `upgrade-migration-project.sh`
upgrades one migration project of the migrations tutorial (source and target models through the model
transform, `migration.alan` through a `from-migration-<datastore>` config when the platform ships one).
`new-version.sh NEW [PREV]` runs the full version-copy workflow for `pages/tutorials/model`,
`pages/tutorials/migrations` and online-ide `docs/tutorials/restaurant1`.

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

## Screenshots

`_tools/tutorial/screenshots/` regenerates the tutorial images from the verified models, so they can be redone
for every platform version. `shoot.mjs VERSION` produces the application screenshots of the model tutorial,
`ide/prepare-workspace.sh VERSION` plus `ide/ide-shoot.mjs VERSION` the IDE screenshots of the migrations
tutorial. Both read their shot lists from `screenshots/VERSION/` (`shots.json`, `ide-shots.json`) and write the
PNGs straight into `pages/tutorials/...`. Scratch output goes to `.toolchains/screenshots/` and `.toolchains/vscode/`.

Prerequisites, one-off per machine:

- A webclient checkout (`WEBCLIENT`, default `../webclient`) with a build that matches its sources:
  `make generator generators src/webclient/dist/client build/javascript/test-server/index.js` in that checkout.
  The client test engine's `--serve` mode from `src/test-server` serves a step locally; `serve-app.sh` is the only
  place that knows this and is the seam to replace when the dev-server gets a local datastore flag.
- `npm install` in `_tools/tutorial/screenshots` (puppeteer, pinned to the version the webclient uses so the cached Chrome is reused).
- The client's font family, "Source Sans Pro", installed for the user (`~/.local/share/fonts`), otherwise Chrome falls back to DejaVu.
- For the IDE shots: the standalone VS Code CLI in `.toolchains/vscode/cli/code` (`https://update.code.visualstudio.com/latest/cli-alpine-x64/stable`),
  one `code serve-web --server-data-dir .toolchains/vscode/server-data --cli-data-dir .toolchains/vscode/cli-data` run that
  downloads the server, and the `Kjerner.alan` extension installed with that server:
  `.toolchains/vscode/cli-data/serve-web/<commit>/bin/code-server --accept-server-license-terms --server-data-dir <abs>/server-data --extensions-dir <abs>/server-data/extensions --install-extension Kjerner.alan`.
  VS Code for the Web keeps user settings in the browser, so the shots use default settings plus a dark theme set as
  a workspace setting, a trusted workspace (the extension is disabled in Restricted Mode) and a closed Chat side bar.
  Nothing of the user's own VS Code configuration is used.

Shot list (`shots.json`): `datasets` map a name to a website model dir and a data migration, either
`online-ide:<step>` (the step migrations of the online-ide docs, which only `create` and therefore compile against
an empty source model) or `data/<file>.alan` for a state the tutorial needs but no step provides. Every shot names
its dataset, output file, `actions`, and optionally `clip`, `clipTo`, `annotate` (red boxes, arrows, labels drawn
as an SVG overlay), `viewport`, `settleMs`; `code` shots render a code fragment instead of the app. Selectors:
CSS, `text=` (substring), `exact=` (exact leaf text), `button=` (button label, icon names stripped), `row=` (table
row containing a cell with that text), `field=` (the control next to a property label), `chevron=` (the expand
icon of a navigation entry), `widget=`; append `[n]` to pick the n-th match. Actions: `click`, `dblclick`, `hover`,
`type`, `press`, `clickAt`, `mouse`, `waitFor`, `wait`, `select`, `view` (`Full`/`Compact`), `goto` (hash deep
link). Shots of one dataset share one datastore instance, so a shot that saves data changes what later shots see;
`--only ID,ID` reruns single shots, `--keep` leaves the last server running for inspection, `--headful` shows the browser.
Annotation and action selectors: `exact=<text>`/`button=<text>`/`chevron=<text>` (deepest visible element with that
text, buttons only for the last two), `row=<cell text>` (the table row holding it), `field=<label>` (the input of a
property), `prop=<label>` (the whole property line, label and value) and `value=<label>` (only its value part),
`text=`/`aria=`/`widget=` and plain css (first visible match). All of them take `[n]` to pick the n-th match. When
writing a new shot, the `dump` (elements matching a css selector) and `dumpUp` (`{"text": ..., "up": n}`: the HTML n
levels above a text) actions print what the page offers.

`dataDir` names a directory (default `assets/`) whose `logo.png` (and optionally `logo-sideways.png`, app icons) the
served client shows as application logo, exactly as the `data/` files of a deployment. A project keeps its icon as
`favicon.ico`, and the server serves such a file under the name the client asks for, so `assets/` holds nothing but a
copy of the template project's own icon and the screenshots carry the logo of a freshly created project:

```sh
cp <online-ide>/templates/default/project/deployments/default/systems/client/instance/favicon.ico assets/favicon.ico
```

No conversion: browsers decode an image from its content, not from its name or content type. Every capture is framed
afterwards (`lib/frame.mjs`: rounded corners, thin border, drop shadow on a transparent margin); `frame` on the
config or a shot overrides `margin`, `radius`, `border`, `shadow`, and `"frame": false` disables it.

The models in `pages/tutorials/model/VERSION/models/` that exist only for a screenshot (`step_09-priority`) carry no
snippet markers; they are still compiled by `snippets.py verify`.

The Mission Control tutorial (`pages/tutorials/mission/VERSION/`) is a second tutorial in the same infrastructure:
`snippets.py <cmd> VERSION --tutorial mission` for its models and snippets, `2026.2/shots-mission.json` for its
application screenshots (`shoot.mjs VERSION --list ...`; the list's `tutorial` field makes `build-step.sh` read models
from `pages/tutorials/mission` and its `docs` field points `online-ide:<step>` migrations at the tutorial's own
online-ide directory; `TUTORIAL=<name>` and `DOCS=<name>` do the same on the command line), and `ide/mission-shots.json`
for the language-server screenshot, taken from a workspace whose model is `step_02-units` with the markers stripped.
`step_02-units` carries `//@ expect error`: it is meant not to compile, and the reference check skips it.

Its step models and example data live in online-ide `docs/tutorials/mission-control/VERSION/step_NN/{to_model,migration}`,
exactly as `restaurant1` holds them for the model tutorial: `./test.sh mission-control/VERSION` in online-ide compiles
every step model and every step migration against the previous step, `snippets.py verify VERSION --tutorial mission
--reference <online-ide>` checks that the website models and those step models are the same model (`REFERENCE_DOCS` in
`snippets.py` maps a tutorial to its online-ide directory), the screenshot datasets read their data from those step
migrations, and the tutorial page points readers at the folders for the data of each act.

`pages/tuts/getting-started.md` has its own four images in `ide/getting-started-shots.json`, taken from a workspace
built by hand: copy `templates/default/project`, put the model of that page in `models/model/application.alan`, set
`anonymous login: disabled`, `./alan build`, and generate a `migrations/from_release` (as `prepare-workspace.sh
--from-release` does) into `.toolchains/vscode/workspace-gs/project`.

The IDE tutorial (`pages/tutorials/ide/`) is not versioned; its six images come from `ide/tutorial-shots.json`:
`ide/prepare-workspace.sh VERSION step_01 --from-release --dir workspace-ide` (a workspace with a `from_release`
migration, as after a first deployment) and `node ide/ide-shoot.mjs VERSION --list ide/tutorial-shots.json`. Shot
steps there are `open`, `command` (palette title), `click`/`hover` (css, `explorer=<row>`, `statusbar=<text>`,
`text=<exact>`), `key`, `type`, `waitFor`, `wait`, `dump` (prints matching elements, for writing new shots);
`clip`/`clipTo`/`annotate` work as in `shots.json`. Captures go through a plain CDP screenshot because puppeteer's
own screenshot resizes the page, which makes VS Code close menus and hovers.
