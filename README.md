# Alan website

The homepage is special, all its contents are in the template.

## Markdown

Markdown is converted using [kramdown](https://kramdown.gettalong.org/),
which has a [quick reference guide](https://kramdown.gettalong.org/quickref.html).

## Jekyll

The site is built using [Jekyll](https://jekyllrb.com/docs/home/),
for which there are guides and docs aplenty.

`_data/dist/<platform version>/versions.json` are copies of the published `versions.json` files; the versions repo
writes them on release (`publish.sh`), do not edit them by hand. `_data/versions.json` is hand-managed: the platform
version, its `alan` script, and the versions of the platform components (model, interface, project-build-environment).
The documentation tables select their pages by front matter (`origin`, `version`) and are rendered once per type and
version with `jekyll-include-cache`.

GitHub Pages builds and deploys every push to `master`.

Rendering all generated language documentation takes minutes. For a build in seconds while working on templates and
styles, add the development override: `bundle exec jekyll serve --config _config.yml,_config.dev.yml`.

