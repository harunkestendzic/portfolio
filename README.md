# Harun Kestendžić: portfolio

Static site, English (default) and Bosnian. Built with plain Python and deployed to GitHub Pages.

- `content.py`: text, projects, experience, skills (EN and BS).
- `earlier.py`, `posts*.py`: earlier projects and devlog content.
- `diagrams.py`: inline SVG diagrams.
- `assets/`: images, PDFs and project media.

Build locally: `python3 build2.py` writes the site to `dist/`.
Every push to `main` rebuilds and publishes the site automatically (see `.github/workflows/pages.yml`).
