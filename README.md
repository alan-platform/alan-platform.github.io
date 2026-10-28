# Alan website

The site is built with [Hugo](https://gohugo.io/documentation/) and published with GitHub Pages. The homepage is
special, all its contents are in its layout (`layouts/index.html`).

## Build and serve

Needs Hugo 0.167.0 extended (the extended edition carries the Sass compiler; `hugo.toml` makes an older or plain binary
stop with a message) and Python 3 (standard library only).

```
_tools/hugo/build.sh           # rewrite the generated pages, build into public/
_tools/hugo/build.sh serve     # the same, then hugo server with live reload
```

The script changes to the repository root from its own location, so it works from any directory (`hugo.toml`, its
mount sources and the output of `prepare.py` are relative to the root). `HUGO=/path/to/hugo` names the binary when it
is not on the `PATH`; flags after `serve` go to `hugo server`. The whole build takes seconds.

`serve` renders in memory, so `public/` keeps the last build. It runs `prepare.py` once, when it starts: restart it
after `pages/docs` or `_data` changed, or the rewritten documentation pages in `.build/content` and the key order of
the data files in `.build/data/key_order.json` are stale. An edit of a hand-written page, a file beside it (a snippet
of the `file` shortcode, an image), a template, `src/` or `_sass/` shows without a restart.

After Hugo, the build runs `_tools/hugo/check-output.sh` on `public/`, with the output of Hugo in `.build/hugo.log`.
Hugo exits 0 and writes a smaller site when a mount source is missing, a data glob matches nothing or a layout is
missing, so the check fails the build when: `public/pages/docs` has another number of `.html` files than `pages/docs`
has `.md` files; one of the pages and files that every deployment needs is missing (the home page, 404, the docs, learn,
about, faq and deps pages, `sitemap.xml`, `robots.txt`, `CNAME`, the stylesheet and scripts, a font); a rule block of the
model 109 grammar has lost its id; the sitemap has fewer than 3000 entries; or Hugo logged a warning or an error other
than the deprecation of LibSass; or the text `{:`, or a line that starts with `{.` or `{#` outside `<pre>`, is left in
a generated page (a sign that the generator started a form that `prepare.py` does not know).

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
- Generated documentation: `pages/docs/**` is written by the GitLab CI job "Update the docs", in kramdown syntax, and
  committed. Never edit it here. `_tools/hugo/prepare.py` rewrites it at build time, see below.
- `_data/dist/<platform version>/versions.json` are copies of the published `versions.json` files; the versions repo
  writes them on release (`publish.sh`), do not edit them by hand. `_data/versions.json` is hand-managed: the platform
  version, its `alan` script, and the versions of the platform components (model, interface, project-build-environment).
  The `RELEASE.md` files beside the `versions.json` files are not data: the data mount in `hugo.toml` takes only `.json`,
  `.yml` and `.yaml` files, Hugo would fail to load them. `deps/` (the dependency graph) is written by CI as well.
- Layouts and styles: `layouts/` (partials, shortcodes, render hooks, and the templates of `robots.txt` and
  `sitemap.xml`), `_sass/` with `src/main.scss`, `src/`, `assets/`. The documentation tables select their pages by
  front matter (`origin`, `version`) and are rendered once per type and version (`partialCached`). `src/main.css` is
  compiled from `src/main.scss` by `layouts/partials/stylesheet.html`, through Hugo's LibSass.
- `hugo.toml` mounts these directories where Hugo wants them: the Markdown under `pages/` as content, except
  `pages/docs/`, which comes from `.build/content/pages/docs`; `index.md` as the home page placeholder and `404.md` as
  the text of the 404 page; `assets/`, `deps/`, `CNAME` and `favicon.ico` as static files; `_data/` and `.build/data`
  as data. Everything else under `pages/` (under `payload/`) and `src/` are assets, which
  `layouts/partials/static-payload.html` publishes at their paths in the repository: a static mount of `pages/` would
  make `hugo server` miss every edit of a page (see `hugo.toml`). `_sass/` is mounted beside `src/main.scss`.
  `robots.txt` and `sitemap.xml` are not static files but templates, and `src/main.css` is compiled, so none of the
  three is in the repository as a file. The directories are laid out as the tools that write into them expect (CI writes
  `pages/docs` and `deps/`, the versions repo writes `_data/dist/`), which is why `hugo.toml` mounts them.

## prepare.py

`_tools/hugo/prepare.py` reads `pages/docs/**` and writes a rewritten copy to `.build/content/pages/docs`, which
`hugo.toml` mounts over the content. The source stays untouched because CI rewrites it on every documentation update.
The generator writes kramdown syntax, and kramdown and Goldmark read some of it differently. The script:

- removes the `1. TOC` and `{:toc}` lines and puts `toc: true` in the front matter; the layout builds the index of the
  page (the rail) from the headings of pages that have it;
- turns the `{: #grammar-rule--X }` line before a rule block into an `id` on its `<div>` (27921 times), and the
  `{: #example--X }` line after a paragraph into `{#example--X}`;
- adds `url: "/pages/docs/<path>.html"` to the front matter, the address the toolchains deep-link to;
- repairs what Goldmark would render differently: a blank line after a rule block that text follows directly (a heading
  there would be swallowed by the HTML block), a `>` prefix on a fence that opens in a blockquote, a stray backtick
  after a fence language, `<!`, `<!--` and `</` that a browser would read as markup in rule blocks (written `&lt;`), and
  link destinations with a space (wrapped in `<...>`);
- writes the quotes of a quoted word in prose as `‘` and `’`: Goldmark's typographer renders `'empty'` with two right
  quotes, where kramdown's smart quotes open and close it. Apostrophes inside words, code and raw HTML are left alone;
- stops with the file and line when it meets a `{:` line of a kind it does not know, or a line outside fences and raw
  HTML that starts with `{.` or `{#` (Goldmark would take it for a block attribute and not show it), so a new form of
  the generator is noticed and not published as text.

Beside the pages it writes `.build/data/key_order.json`: the order of the keys of the `platform` object of each version
in `_data/versions.json` and of the `system types` object of each `_data/dist/<version>/versions.json`. Hugo loads a JSON
object as a map and templates range over a map in sorted order, while the tables list components in file order; the
layout reads the order from this file. The data mount of `hugo.toml` takes `.build/data` as well.

It prints a counter for each rewrite. `python3 _tools/hugo/prepare.py --check` runs the rewrite in memory and prints
the counters only. The output depends only on the input, so running it twice gives the same tree.

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
  `github-pages` (a tar of `public/`) attached to the run: download it from the run page to inspect it. A deployment that failed after a push is redeployed by re-running
  that run; a manual run does not deploy.
- `notify` runs when a push failed, in `build` or in `deploy`. GitHub emails only the person whose action started a
  failed run, and the documentation pushes come from the GitLab CI user, so the job opens an issue titled
  "Site build failed: <job> / <step>" with the commit, its author and the run, assigned to `gjkunst` and labelled
  `site-build`. While an issue with that label is open, a new failure is a comment on it, not a second issue. Close the
  issue when the site builds again.

The Pages source of the repository is "GitHub Actions" (Settings, Pages,
https://github.com/alan-platform/alan-platform.github.io/settings/pages). Hugo is downloaded from its release and
checked against a SHA-256 pinned in the workflow; to update Hugo, change `HUGO_VERSION` and `HUGO_SHA256` together (the
checksum is in the `checksums.txt` of the release).

Cutover order: set the Pages source to "GitHub Actions" first, while `master` still holds the previous tree, and push
the Hugo tree to `master` afterwards. With the source on a branch, GitHub builds the pushed tree with its own builder,
which cannot build it, and the workflow cannot deploy. A pull request from the branch that holds the Hugo tree to
`master` builds and checks it on a runner before that, without deploying. The cutover runbook has the steps.
