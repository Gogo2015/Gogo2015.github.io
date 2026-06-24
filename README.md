# gogo2015.github.io

Personal site for Gaurav Mitra, a small custom static site served by GitHub Pages.

## How it works

- **Content** lives in Markdown, one file per project in `projects/*.md`.
- **`build.py`** holds the site metadata, the homepage copy, and the `PROJECTS`
  registry (card text, tags, repo/paper links). Running it renders the static
  HTML: `index.html` and `projects/*.html`.
- **`assets/css/style.css`** is the design system (light + dark themes).
- **`.nojekyll`** tells GitHub Pages to serve the generated HTML as-is
  (no Jekyll/Ruby build).

## Add or edit a project

1. Edit the relevant `projects/<slug>.md`, or add a new one plus a matching entry
   in the `PROJECTS` list in `build.py`.
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
