# gogo2015.github.io

Personal site for Gaurav Mitra, a small static site served by GitHub Pages.

## How it works

- **Content** lives in Markdown, one file per project in `projects/*.md`.
- **`build.py`** holds the homepage copy and the `PROJECTS` list. Running it
  renders `index.html` and `projects/*.html`.
- **`assets/css/style.css`** has the styles. Fonts are in `assets/fonts/`.
- **`.nojekyll`** tells GitHub Pages to serve the generated HTML as-is.

## Add or edit a project

1. Edit `projects/<slug>.md`, or add a new one plus an entry in `PROJECTS` in
   `build.py`.
2. Rebuild:
   ```bash
   pip install markdown      # one time
   python build.py
   ```
3. Commit the regenerated `index.html` and `projects/*.html`.

## Local preview

```bash
python -m http.server 4173
```

Then open <http://localhost:4173>.
