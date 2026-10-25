# manovikash.com

Personal website of Mano Vikash Janardhanan, built with [al-folio](https://github.com/alshedivat/al-folio) (Jekyll) and hosted on GitHub Pages.

**To change anything on the site or CV, edit the files in [`content/`](content/README.md).** Nothing is typed twice:
one BibTeX file feeds the publications page and both CVs, and one YAML file feeds the CV web page and the LaTeX CV.

```
content/            what you edit (see content/README.md)
  profile.yml         name, headline, contact details, profile links
  bio.md              homepage text
  papers.bib          all publications
  cv.yml              CV sections
  photo.jpg           profile photo
cv/template.tex     look of the LaTeX CV (moderncv); see cv/README.md
_pages/             the three pages (home, publications, cv) - wiring only
_plugins/content.rb hands content/ to al-folio and runs bin/build-cv
bin/build-cv        content/ -> cv/main.tex + cv/main.bib -> cv/main.pdf
_config.yml         site settings
```

## How it updates

Pushing to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which builds the site and the LaTeX CV
from `content/` and pushes the result to the `gh-pages` branch, which GitHub Pages serves (the PDF at `/assets/pdf/cv.pdf`).
Nothing generated is committed to `main`; each run also keeps `cv/main.tex`, `cv/main.bib` and `cv/main.pdf` as a downloadable
artifact.

Until the custom domain is set up, the site is at https://mavivi0.github.io/mano_online/. To move it to www.manovikash.com,
point the domain's DNS at GitHub Pages, then add a file named `CNAME` to the repository root containing `www.manovikash.com`.
The next deploy publishes it and builds the site for the root of that domain. (Setting the domain only in Settings → Pages
would be undone by the next deploy, which replaces the whole `gh-pages` branch.)

## Previewing on your Mac

One-time setup (Homebrew):

```bash
brew install ruby imagemagick python
brew install --cask mactex-no-gui        # LaTeX for the CV (skip if you already have MacTeX)
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
http://localhost:4000/assets/pdf/cv.pdf. To build only the CV: `bin/build-cv` (writes `cv/main.tex`, `cv/main.bib`, `cv/main.pdf`).

## Upgrading al-folio

Layouts and styles come from al-folio's versioned gems (pinned in `Gemfile` and listed under `plugins:` in `_config.yml`).
This site overrides only two theme files: `assets/css/main.scss` (accent color) and
`_includes/cv/publications.liquid` (CV publications come from `papers.bib`). Re-check both after an upgrade.
