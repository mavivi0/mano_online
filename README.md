# manovikash.com

Personal website of Mano Vikash Janardhanan, built with [al-folio](https://github.com/alshedivat/al-folio) (Jekyll) and hosted on GitHub Pages.

**To change anything on the site or CV, edit the files in [`content/`](content/README.md).** Nothing is typed twice:
one BibTeX file feeds the publications page and both CVs, and one YAML file feeds the CV web page and the CV PDF.

```
content/            what you edit (see content/README.md)
  profile.yml         name, headline, contact details, profile links
  bio.md              homepage text
  papers.bib          all publications
  cv.yml              CV sections
  photo.jpg           profile photo
_pages/             the three pages (home, publications, cv) - wiring only
_plugins/content.rb hands content/ to al-folio and builds the CV PDF
bin/build-cv        content/ -> CV PDF, via RenderCV
_rendercv/          look of the PDF (theme, colors, fonts)
_config.yml         site settings
```

## How it updates

Pushing to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which builds the site, builds the CV PDF
from `content/`, and publishes both to GitHub Pages. Nothing generated is committed to the repository.

## Previewing on your Mac

One-time setup (Homebrew):

```bash
brew install ruby imagemagick python
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
bundle install
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Then, each time:

```bash
source .venv/bin/activate
bundle exec jekyll serve      # open http://localhost:4000
```

Edits in `content/` show up in the browser after a refresh, including the PDF at
http://localhost:4000/assets/pdf/cv.pdf. To produce only the PDF: `bin/build-cv` (writes `cv.pdf`).

## Upgrading al-folio

Layouts and styles come from al-folio's versioned gems (pinned in `Gemfile` and listed under `plugins:` in `_config.yml`).
This site overrides only two theme files: `assets/css/main.scss` (accent color) and
`_includes/cv/publications.liquid` (CV publications come from `papers.bib`). Re-check both after an upgrade.
