#!/usr/bin/env python3
"""Generate latex-cv/main.tex from the CV's single sources of truth.

Content sources (never edit main.tex by hand -- it is generated):
  - assets/json/resume.json   CV content (name, work, education, talks, service)
  - _bibliography/papers.bib  publications (also used by the website's /publications/ page)

Usage: python3 bin/generate_cv.py [--build]
  --build  also run pdflatex/bibtex and copy the result to assets/pdf/cv.pdf
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = REPO_ROOT / "latex-cv"
RESUME_JSON = REPO_ROOT / "assets" / "json" / "resume.json"
OUTPUT_TEX = LATEX_DIR / "main.tex"
OUTPUT_PDF = REPO_ROOT / "assets" / "pdf" / "cv.pdf"

LATEX_SPECIAL_CHARS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}
LATEX_SPECIAL_RE = re.compile("|".join(re.escape(c) for c in LATEX_SPECIAL_CHARS))


def escape(value):
    if not isinstance(value, str):
        return value
    return LATEX_SPECIAL_RE.sub(lambda m: LATEX_SPECIAL_CHARS[m.group()], value)


def year_of(date_str):
    return date_str[:4] if date_str else ""


def period_of(start, end):
    start_year, end_year = year_of(start), year_of(end)
    if not end:
        return f"{start_year} - present"
    if start_year == end_year:
        return start_year
    return f"{start_year} - {end_year}"


def entry_body(highlights, cites=None):
    """Dash-bulleted body used for Employment/Experience entries, e.g. `- text \\cite{key}`."""
    cites = cites or {}
    lines = []
    for i, h in enumerate(highlights):
        line = f"- {escape(h)}"
        keys = cites.get(str(i))
        if keys:
            line += " \\cite{" + ",".join(keys) + "}"
        lines.append(line)
    return "\\newline{}".join(lines)


def entry_body_plain(highlights):
    """Plain (non-bulleted) body used for Education entries, matching the original template."""
    return "\\newline{}".join(escape(h) for h in highlights)


def build_employment_summary(raw_entries):
    entries = []
    for entry in raw_entries:
        entries.append(
            {
                "name": escape(entry["name"]),
                "position": escape(entry["position"]),
                "location": escape(entry.get("location", "")),
                "period": period_of(entry.get("startDate", ""), entry.get("endDate", "")),
            }
        )
    return entries


def build_work(raw_work):
    jobs = []
    for job in raw_work:
        jobs.append(
            {
                "name": escape(job["name"]),
                "position": escape(job["position"]),
                "location": escape(job.get("location", "")),
                "period": period_of(job.get("startDate", ""), job.get("endDate", "")),
                "body": entry_body(job.get("highlights", []), job.get("highlight_cites")),
            }
        )
    return jobs


def build_education(raw_education):
    entries = []
    for edu in raw_education:
        entries.append(
            {
                "institution": escape(edu["institution"]),
                "location": escape(edu.get("location", "")),
                "degree_line": f"{escape(edu.get('studyType', ''))}, {escape(edu.get('area', ''))}",
                "period": period_of(edu.get("startDate", ""), edu.get("endDate", "")),
                "body": entry_body_plain(edu.get("highlights", [])),
            }
        )
    return entries


def build_academic_research(raw_entries):
    return build_work(raw_entries)


def build_talks(raw_talks):
    talks = []
    for talk in raw_talks:
        talks.append(
            {
                "title": escape(talk["title"]),
                "event": escape(talk["event"]),
                "location": escape(talk.get("location", "")),
                "year": year_of(talk.get("date", "")),
            }
        )
    return talks


def build_service(raw_service):
    entries = []
    for entry in raw_service:
        entries.append(
            {
                "role": escape(entry["role"]),
                "venues": escape(", ".join(entry.get("venues", []))),
            }
        )
    return entries


def main():
    do_build = "--build" in sys.argv

    resume = json.loads(RESUME_JSON.read_text())
    basics = resume["basics"]

    env = Environment(
        loader=FileSystemLoader(str(LATEX_DIR)),
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("template.tex.j2")

    rendered = template.render(
        basics={
            "first_name": escape(basics["first_name"]),
            "last_name": escape(basics["last_name"]),
            "email": escape(basics["email"]),
            "homepage": basics["homepage"],
        },
        employment_summary=build_employment_summary(resume.get("employment_summary", [])),
        work=build_work(resume.get("work", [])),
        academic_research=build_academic_research(resume.get("academic_research", [])),
        education=build_education(resume.get("education", [])),
        talks=build_talks(resume.get("talks", [])),
        service=build_service(resume.get("service", [])),
    )
    OUTPUT_TEX.write_text(rendered)
    print(f"Wrote {OUTPUT_TEX.relative_to(REPO_ROOT)}")

    if not do_build:
        return

    def run_latex(cmd):
        subprocess.run(cmd, cwd=LATEX_DIR, check=True)

    run_latex(["pdflatex", "-interaction=nonstopmode", "main.tex"])
    run_latex(["bibtex", "main"])
    run_latex(["pdflatex", "-interaction=nonstopmode", "main.tex"])
    run_latex(["pdflatex", "-interaction=nonstopmode", "main.tex"])

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PDF.write_bytes((LATEX_DIR / "main.pdf").read_bytes())
    print(f"Wrote {OUTPUT_PDF.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
