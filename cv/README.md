# cv/: the LaTeX CV

`template.tex` is the only file here you edit, and only to change the CV's *look* (moderncv
style, colors, spacing, section layout). What the CV *says* lives in [`content/`](../content/README.md).

`bin/build-cv` (run automatically by every site build) creates the rest of this folder:

| File       | Built from                                                       |
| ---------- | ---------------------------------------------------------------- |
| `main.tex` | `template.tex` filled in with `content/profile.yml` and `content/cv.yml` |
| `main.bib` | `content/papers.bib`, minus the website-only fields               |
| `main.pdf` | `main.tex` + `main.bib`, compiled with latexmk (pdflatex + biblatex) |

They are not committed; a fresh build recreates them. The website publishes the PDF at
`/assets/pdf/cv.pdf`, and each deploy run on GitHub keeps `main.tex`, `main.bib` and `main.pdf`
as a downloadable "cv" artifact (Actions tab, open the latest run).

`main.tex` and `main.bib` are self-contained, so you can also compile them yourself
(`latexmk -pdf main.tex`) or upload both to Overleaf.
