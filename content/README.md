# content/: everything you edit

This folder is the only place your information lives. Change a file here, push to `main`,
and the website and the CV PDF are rebuilt from it within a couple of minutes.

| File          | What it holds                                                      | Where it shows up                                              |
| ------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- |
| `profile.yml` | Name, headline, location, email, website, profile links            | Homepage, browser tab, link previews, CV header (web + PDF)    |
| `bio.md`      | The paragraphs on your homepage (Markdown)                          | Homepage                                                       |
| `papers.bib`  | Every publication, in BibTeX                                        | Publications page, homepage "selected", CV publications (web + PDF) |
| `cv.yml`      | CV sections: experience, education, talks, service, ...             | CV page (`/cv/`) and the PDF (`/assets/pdf/cv.pdf`)            |
| `photo.jpg`   | Profile photo                                                      | Homepage                                                       |

## Common edits

- **New paper:** add a BibTeX entry to `papers.bib`. Add `selected = {true}` to also show it on the
  homepage. It appears on the publications page and in both CVs automatically.
- **New job or talk:** add an entry under the right section of `cv.yml`.
- **New photo:** replace `photo.jpg`, keeping the file name.
- **Reorder CV sections:** move them around in `cv.yml`. The `Publications: papers.bib` line marks
  where the publications go.

You can edit these files directly on github.com (open the file, click the pencil icon, commit).

## What not to do

Don't type papers into `cv.yml`, and don't type your name, email or links anywhere but
`profile.yml`. Everything else reads from these files.
