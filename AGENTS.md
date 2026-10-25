# Agent guidelines

Personal website of Mano Vikash Janardhanan: an [al-folio](https://github.com/alshedivat/al-folio) v1 Jekyll site.
Read [`README.md`](README.md) for the layout of the repository.

## The one rule: content lives only in `content/`

The owner wants every fact stated exactly once. All personal information is in `content/`:

- `profile.yml` (identity and links), `bio.md` (homepage text), `papers.bib` (publications), `cv.yml` (CV sections), `photo.jpg`.
- Never copy any of it into `_config.yml`, `_pages/`, `_data/` or anywhere else. Never add publications to `cv.yml`; its
  `Publications: papers.bib` line pulls them from the `.bib`.
- `_plugins/content.rb` maps `content/` into what al-folio expects (`site.data.socials`, `site.data.cv`, site name, scholar
  names) and builds the PDF. `bin/build-cv` maps the same files into RenderCV. If you add a field to `content/`, wire it
  through these two files rather than duplicating it.
- `assets/img/prof_pic.jpg` is a symlink to `content/photo.jpg`. Keep it a symlink.

## Building and checking

```bash
bundle install && python3 -m pip install -r requirements.txt
bundle exec jekyll build      # also builds the CV PDF into _site/assets/pdf/cv.pdf
bin/build-cv --out /tmp/cv.pdf   # just the PDF
```

- With `CV_PDF_REQUIRED=1` (set in CI) a failed PDF build fails the site build; without it, it is a warning.
- RenderCV's Typst template downloads packages from packages.typst.org on first use.
- The site's baseurl is empty (custom domain www.manovikash.com).

## Theme overrides

Only two gem-owned files are shadowed: `assets/css/main.scss` (accent color `#004f90`, shared with
`_rendercv/design.yaml`) and `_includes/cv/publications.liquid`. Prefer configuration over adding more overrides.
