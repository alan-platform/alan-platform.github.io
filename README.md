# Alan website

The site is built with [Hugo](https://gohugo.io/documentation/) and published with GitHub Pages. The homepage is
special, all its contents are in its layout (`layouts/index.html`).

## Build and serve

Needs Hugo 0.167.0 or newer, the standard edition (with an older binary Hugo warns, and the output check fails the build), and Python 3
(standard library only).

```
_tools/hugo/build.sh           # build into public/, then check the output
_tools/hugo/build.sh serve     # hugo server with live reload
```

Nothing adapts the pages before Hugo reads them: the build is Hugo, and the check of its output.

The script changes to the repository root from its own location, so it works from any directory (`hugo.toml` and its
mount sources are relative to the root). `HUGO=/path/to/hugo` names the binary when it is not on the `PATH`; flags
after `serve` go to `hugo server`. The whole build takes seconds.

`serve` renders in memory, so `public/` keeps the last build. An edit of a page, a file beside it (a snippet of the
`file` shortcode, an image), a data file, a template or `src/` shows without a restart.

After Hugo, the build runs `_tools/hugo/check-output.sh` on `public/`, with the output of Hugo in a temporary file.
Hugo exits 0 and writes a smaller site when a mount source is missing, a data glob matches nothing or a layout is
missing, so the check fails the build when: `public/pages/docs` has another number of `.html` files than `pages/docs`
has `.md` files; one of the pages and files that every deployment needs is missing (the home page, 404, the docs, learn,
about, faq and deps pages, `sitemap.xml`, `robots.txt`, `CNAME`, the stylesheet and scripts, a font); a rule block of the
model 109 grammar has lost its id; the sitemap has fewer than 3000 entries; Hugo logged a warning or an error; or the
text `{:`, or a line that starts with `{.` or `{#` outside `<pre>`, is left in a generated page. That last check fails
the build of a generator that writes a form that Hugo does not read.

The tools have tests: `python3 -m unittest discover -s _tools/hugo/tests` (the workflow runs them before the build).

## Markdown

Markdown is converted by Hugo's Goldmark, a CommonMark parser. Its settings in `hugo.toml`: raw HTML is enabled, block
attributes work (`{#id .class}` on the line after a paragraph, `{#id}` after a fence's language), the typographer
writes smart quotes and dashes, a bare URL is not a link, and void elements are written `<br />`. Fenced code and
headings go through render hooks (`layouts/_markup/`): a fence renders as the wrapper that the stylesheet, `src/main.js`
and Prism select on (`div.language-X.highlighter-rouge > div.highlight > pre.highlight > code`), and Prism highlights
it in the browser. Page logic is in shortcodes: `{{< file >}}` includes a file relative to the page, `{{< param >}}` and
`{{< site-version >}}` print versions, `{{< dist-version >}}` and `{{< platform-component >}}` read the version data.
`url:` in the front matter is the page's address.

## Where content comes from

- Hand-written pages: `index.md`, `404.md`, `pages/*.md`, `pages/tutorials/**`, `pages/tuts/**`. The files in
  `pages/tutorials/**` that are not Markdown (models, images, data) are copied as they are.
- Generated documentation: `pages/docs/**` is written by the docs generator of alan-tools and committed. Never edit it
  here. The generator writes the form that Hugo reads, and the build adapts nothing; its contract is below.
- `_data/dist/<platform version>/versions.json` are copies of the published `versions.json` files; the versions repo
  writes them on release (`publish.sh`), do not edit them by hand. `_data/versions.json` is hand-managed: the platform
  version, its `alan` script, and the versions of the platform components (model, interface, project-build-environment).
  The `RELEASE.md` files beside the `versions.json` files are not data: the data mount in `hugo.toml` takes only `.json`,
  `.yml` and `.yaml` files, Hugo would fail to load them. `deps/` (the dependency graph) is written by CI as well.
- Layouts and styles: `layouts/` (partials, shortcodes, render hooks, and the templates of `robots.txt` and
  `sitemap.xml`), `src/`, `assets/`. The documentation tables select their pages by front matter (`origin`,
  `version`) and are rendered once per type and version (`partialCached`).
- `hugo.toml` mounts these directories where Hugo wants them: the Markdown under `pages/`, `pages/docs/` included, as
  content; `index.md` as the home page placeholder and `404.md` as the text of the 404 page; `assets/`, `deps/`,
  `CNAME` and `favicon.ico` as static files; `_data/` as data. Everything else under `pages/` (under `payload/`) and `src/` are assets, which
  `layouts/partials/static-payload.html` publishes at their paths in the repository: a static mount of `pages/` would
  make `hugo server` miss every edit of a page (see `hugo.toml`). `robots.txt` and `sitemap.xml` are not static files
  but templates, and `src/main.css` is built from `src/css/`, so none of the three is in the repository as a file. The
  directories are laid out as the tools that write into them expect (CI writes `pages/docs` and `deps/`, the versions
  repo writes `_data/dist/`), which is why `hugo.toml` mounts them.
- The stylesheet is plain CSS: no Sass, so the build needs only the standard Hugo binary. Its parts are the files in
  `src/css/`, numbered in the order of the cascade: `10-fonts.css` (the font faces), `15-tokens.css` (the design
  tokens: colours, type scale, spacing, widths, radii, shadows, durations and stacking levels, as custom properties
  that the other parts use), `20-theme.css` (the base styles of the elements), `30-main.css` (the page layout),
  `40-home.css` (the home page), `50-header.css` and `60-footer.css` (the site header and footer), `70-docs.css`
  (the language tables, the archive and the document switcher), `80-release-notes.css`, `90-hub.css` (the Learn,
  Documentation, About and FAQ pages) and `95-index.css` (the page index). `layouts/partials/stylesheet.html` concatenates them in the order of their names into `/src/main.css`, as they
  are, comments included: a minifier would rewrite values into equivalent forms, and the server compresses the
  file anyway. A new part gets a number that puts it at its place in that order. The fonts, Instrument Sans and IBM
  Plex Mono, are served from `assets/fonts/` with their licenses; `10-fonts.css` says where the files come from.
- The order of the components in the version tables is configuration, not data: Hugo hands the data files over as maps
  and a range over a map goes in sorted key order, so `[params.order]` in `hugo.toml` lists the platform components and
  the system types in the order that the data files use, and `layouts/partials/ordered-keys.html` follows it. A key that
  a list does not name follows in sorted order.

### The contract of the generator

A page under `pages/docs` is written in the form Hugo reads. What the build relies on:

- The front matter carries `url: "/pages/docs/<path without .md>.html"` (the path keeps the spaces of directory names
  such as `client bindings`) and, when the page has an index, `toc: true`. The layouts and the toolchains' deep links
  rest on both.
- No kramdown attribute lines (`{: ... }`) and no `1. TOC` / `{:toc}` marker. The id of a grammar rule is an `id` on the
  `<div class="language-js highlighter-rouge">` of its block; the id of an example is `{#id}` on the line after the
  paragraph that introduces it.
- Inside a rule block, a `<` that starts no tag the generator writes there (`span`, `a`, `div`, `pre`, `code`) is
  written `&lt;`, so that grammar text such as `<begin>` shows as text. A blank line follows a block when text follows
  it, because Goldmark ends an HTML block at a blank line.
- Prose is written for CommonMark: a fence that opens in a blockquote is prefixed with `>` on every line, a link
  destination with a space is wrapped in `<...>`, the quotes of a quoted word are written as `‘` and `’`.

`check-output.sh` fails a build whose pages still contain `{:` or a line that starts with `{.` or `{#` outside `<pre>`.

## URL contract

Other systems link to the pages, so the addresses must not change. The toolchains ship
`prefix: https://alan-platform.com/pages/docs/` in `platform.json` and the tools deep-link to
`/pages/docs/<origin>/<version>/<language>/grammar.html#grammar-rule--<rule>`; the forum and the `./alan` script link
there too. Therefore the pages under `pages/` keep `.html` (`uglyURLs` for that section; the home page stays at `/`),
`disablePathToLower = true` (directories such as `client bindings` and `images_IDE` keep their space and case), the
hand-written pages whose address differs from their file name set `url:` (`/docs/`, `/learn/`, `/about/`, `/faq/`,
`/docs/archive`), and the ids `grammar-rule--X` and `example--X` stay as they are.

## Deploy

`.github/workflows/pages.yml` has three jobs.

- `build` installs Hugo, runs `_tools/hugo/build.sh` (so the check of the output too) and uploads `public/` as the
  Pages artifact. It runs for a push to `master`, for a pull request to `master` and for a manual run (Actions, Pages,
  Run workflow, on any branch).
- `deploy` publishes the artifact with GitHub Pages and runs only for a push to `master`. The push of the
  documentation CI job publishes too. A pull request or a manual run stops after the build, with the artifact
  `github-pages` (a tar of `public/`) attached to the run: download it from the run page to inspect it. A deployment
  that failed after a push is redeployed by re-running that run; a manual run does not deploy.
- `notify` runs when a push failed, in `build` or in `deploy`. GitHub emails only the person whose action started a
  failed run, and the documentation pushes come from the GitLab CI user, so the job opens an issue titled
  "Site build failed: <job> / <step>" with the commit, its author and the run, assigned to `gjkunst` and labelled
  `site-build`. While an issue with that label is open, a new failure is a comment on it, not a second issue. Close the
  issue when the site builds again.

The Pages source of the repository is "GitHub Actions" (Settings, Pages,
https://github.com/alan-platform/alan-platform.github.io/settings/pages). Hugo is downloaded from its release and
checked against a SHA-256 pinned in the workflow; to update Hugo, change `HUGO_VERSION` and `HUGO_SHA256` together (the
checksum is in the `checksums.txt` of the release).

