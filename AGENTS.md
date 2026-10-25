# Agent guidelines

Personal website of Mano Vikash Janardhanan: an [al-folio](https://github.com/alshedivat/al-folio) v1 Jekyll site.
Read [`README.md`](README.md) for the layout of the repository.

## The one rule: content lives only in `content/`

The owner wants every fact stated exactly once. All personal information is in `content/`:

- `profile.yml` (identity and links), `bio.md` (homepage text), `papers.bib` (publications), `cv.yml` (CV sections), `photo.jpg`.
- Never copy any of it into `_config.yml`, `_pages/`, `_data/` or anywhere else. Never add publications to `cv.yml`; its
  `Publications: papers.bib` line pulls them from the `.bib`.
- `_plugins/content.rb` maps `content/` into what al-folio expects (`site.data.socials`, `site.data.cv`, site name, scholar
  names, `\cite{}` -> links) and runs `bin/build-cv`, which fills `cv/template.tex` (moderncv, Jinja2 with `%%` line
  statements and `\VAR{}`) and writes `cv/main.tex`, `cv/main.bib`, `cv/main.pdf`. If you add a field to `content/`, wire it
  through these files rather than duplicating it.
- Everything in `cv/` except `template.tex` and `README.md` is generated and git-ignored.
- `assets/img/prof_pic.jpg` is a symlink to `content/photo.jpg`. Keep it a symlink.

## Building and checking

```bash
bundle install && python3 -m pip install -r requirements.txt   # plus TeX: latexmk, moderncv, biblatex
bundle exec jekyll build      # also builds the CV PDF into _site/assets/pdf/cv.pdf
bin/build-cv                  # just the CV, in cv/
```

- With `CV_PDF_REQUIRED=1` (set in CI) a failed PDF build fails the site build; without it, it is a warning.
- On Ubuntu: `apt-get install latexmk texlive-latex-extra texlive-bibtex-extra texlive-fonts-extra`.
- Deploys push the built site to the `gh-pages` branch. CI sets the baseurl: empty when a root `CNAME` file exists (custom
  domain), `/mano_online` otherwise (mavivi0.github.io/mano_online). Locally the baseurl is empty.

## Theme overrides

Only two gem-owned files are shadowed: `assets/css/main.scss` (accent color `#3873b3`, moderncv's blue, so the site
matches the PDF) and `_includes/cv/publications.liquid`. Prefer configuration over adding more overrides.
