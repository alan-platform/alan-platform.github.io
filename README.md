# Alan website

The homepage is special, all its contents are in the template.

## Markdown

Markdown is converted using [kramdown](https://kramdown.gettalong.org/),
which has a [quick reference guide](https://kramdown.gettalong.org/quickref.html).

## Jekyll

The site is built using [Jekyll](https://jekyllrb.com/docs/home/),
for which there are guides and docs aplenty.

Rendering all generated language documentation takes minutes. For a build in seconds while working on templates and
styles, add the development override: `bundle exec jekyll serve --config _config.yml,_config.dev.yml`.

All commits to the `gh-pages` branch result in an update of the public website.
