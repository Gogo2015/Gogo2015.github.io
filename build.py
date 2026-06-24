#!/usr/bin/env python3
"""
Static site builder for gogo2015.github.io.

Converts the Markdown sources in projects/*.md into styled static HTML using a
shared shell (nav + footer) and the design system in assets/css/style.css, and
generates index.html from the PROJECTS registry below.

Usage:  python build.py
Then commit the generated index.html and projects/*.html (served as-is by
GitHub Pages via the .nojekyll marker, so no Ruby/Jekyll needed).
"""

import re
import pathlib
import markdown

ROOT = pathlib.Path(__file__).parent

# ---- site content -----------------------------------------------------------

GITHUB = "https://github.com/Gogo2015"
LINKEDIN = "https://linkedin.com/in/mitragaurav"
EMAIL = "mitragaurav10@gmail.com"

HERO_EYEBROW = "Machine Learning · Computer Vision · Robotics"
HERO_INTRO = (
    "I work on machine learning for computer vision, "
    "motion forecasting, and vision-language-action models for robotics."
)

CURRENTLY = [
    "<strong>Incoming SWE Intern @ IBM</strong> (Summer 2026)",
    "Pursuing an ML research position in robotics (VLAMs / home robotics)",
]
PREVIOUSLY = [
    "Neural video compression autoencoders (variable-rate) at the Oden Institute, UT Austin",
    "Cloud infrastructure, containerization, and CI/CD at Applied Research Laboratories",
]

# Ordered: featured / newest first. `meta` rows render under the page title;
# `repo` / `paper` become header buttons.
PROJECTS = [
    {
        "slug": "vlatune",
        "title": "VLATune",
        "desc": "Reward-weighted filtered behavior cloning for flow-matching VLAs on "
                "LIBERO. A study of whether lightweight RL can improve SmolVLA, with a "
                "negative result.",
        "tags": ["Robotics", "VLA", "Reinforcement Learning", "Flow Matching"],
        "highlight": "🤖 SmolVLA · LIBERO · a negative result",
        "featured": True,
        "badge": "New",
        "meta": ["<b>Model:</b> SmolVLA (450M) &nbsp;·&nbsp; <b>Benchmark:</b> LIBERO"],
        "repo": f"{GITHUB}/VLATune",
        "paper": f"{GITHUB}/VLATune/blob/main/paper/main.pdf",
    },
    {
        "slug": "liver-transplant",
        "title": "Liver Transplant Outcome Prediction",
        "desc": "A full ML pipeline on the OPTN/SRTR national registry predicting graft "
                "failure with classification and survival analysis across ~87k transplants.",
        "tags": ["Machine Learning", "Survival Analysis", "Healthcare"],
        "highlight": "🏆 Best Project Award in CS 7641",
        "badge": "Award",
        "meta": [
            "<b>Course:</b> CS 7641, Machine Learning (Georgia Tech)",
            "<b>Team:</b> Anushka Bajpai · Madhavan Balasubramaniam · Sanjay Gorur · Ameel Jani · Gaurav Mitra",
            "<b>Clinical Advisor:</b> Dr. Marwan Kazimi",
        ],
        "repo": f"{GITHUB}/liver-transplant-ml",
    },
    {
        "slug": "waymo",
        "title": "Waymo Motion Forecasting",
        "desc": "Trajectory prediction on the Waymo Open Motion Dataset, with a Conv-MLP "
                "baseline and a multi-modal extension predicting six futures with confidence.",
        "tags": ["Computer Vision", "Motion Forecasting", "TensorFlow"],
        "highlight": "📉 73% ADE reduction with multi-modal prediction",
        "repo": f"{GITHUB}/WaymoMotionEstimator",
        "paper": f"{GITHUB}/WaymoMotionEstimator/blob/main/ConvMLPPaper.pdf",
    },
    {
        "slug": "gnn-homo-lumo",
        "title": "GNN Molecular Property Prediction",
        "desc": "Predicting the HOMO-LUMO gap from 2D molecular graphs with a deep "
                "edge-aware GINE network, and testing whether a Virtual Node helps.",
        "tags": ["Graph Neural Nets", "PyTorch Geometric", "Chemistry"],
        "highlight": "⚛️ 0.142 eV MAE on 3.38M molecules (PCQM4Mv2)",
        "meta": [
            "<b>Course:</b> CS 7643, Deep Learning (Georgia Tech) · Final Project",
            "<b>Team:</b> Net-Runners (Kapil Meena, Gaurav Mitra, Archith K. Iyer)",
        ],
        "repo": f"{GITHUB}/GNN-HOMO-LUMO",
        "mathjax": True,
    },
    {
        "slug": "llm-eval",
        "title": "LLM Semantic Syntax Evaluation",
        "desc": "An automated pipeline testing whether LLMs can generate semantically "
                "correct pygame board games, checking syntax, semantics, and game logic.",
        "tags": ["LLMs", "Evaluation", "Programming Languages"],
        "highlight": "🎮 3 models · 5 games · headless logic tests",
        "meta": ["<b>Course:</b> CS 6390, Programming Languages · Final Project"],
        "repo": f"{GITHUB}/llm-semantic-syntax",
    },
    {
        "slug": "earthquake",
        "title": "Earthquake Analysis Web App",
        "desc": "A containerized Flask REST API over USGS earthquake data with Redis "
                "storage, async job processing, and server-side charting, deployed to Kubernetes.",
        "tags": ["Backend", "Flask", "Redis", "Kubernetes"],
        "highlight": "☁️ Dockerized · async workers · K8s deploy",
        "repo": f"{GITHUB}/EarthquakeAnalyzer",
    },
    {
        "slug": "autoencoder",
        "title": "Video Compression Autoencoder",
        "desc": "A quantized 3D-convolutional autoencoder for video compression, with "
                "tunable codebook sizes controlling the rate-distortion tradeoff on Moving MNIST.",
        "tags": ["Computer Vision", "Compression", "PyTorch"],
        "highlight": "🎞️ Tunable rate-distortion via codebook size",
        "repo": f"{GITHUB}/ae_compressed_vision",
        "paper": f"{GITHUB}/ae_compressed_vision/blob/main/AutoencoderPaper.pdf",
    },
]

# ---- shell ------------------------------------------------------------------

MATHJAX = """<script>
window.MathJax = {
  tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>"""


def nav(prefix):
    return f"""<header class="nav"><div class="nav-inner">
  <a class="nav-brand" href="{prefix}index.html">Gaurav Mitra</a>
  <nav class="nav-links">
    <a href="{prefix}index.html#projects">Projects</a>
    <a class="hide-sm" href="{prefix}resume.pdf">Resume</a>
    <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
    <a class="hide-sm" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    <a href="mailto:{EMAIL}">Email</a>
  </nav>
</div></header>"""


def footer(prefix):
    return f"""<footer class="footer"><div class="container"><div class="footer-inner">
  <span class="muted">© 2026 Gaurav Mitra</span>
  <div class="footer-links">
    <a href="mailto:{EMAIL}">Email</a>
    <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
    <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    <a href="{prefix}resume.pdf">Resume</a>
  </div>
</div></div></footer>"""


def shell(prefix, title, description, body, mathjax=False):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{MATHJAX if mathjax else ""}
</head>
<body>
{nav(prefix)}
{body}
{footer(prefix)}
</body>
</html>
"""

# ---- markdown conversion ----------------------------------------------------

def convert_markdown(text, mathjax):
    blocks = []

    def protect(m):
        blocks.append(m.group(0))
        return f"\x00M{len(blocks) - 1}\x00"

    if mathjax:
        text = re.sub(r"\$\$.*?\$\$", protect, text, flags=re.S)
        text = re.sub(r"(?<!\\)\$(?!\s)(.+?)(?<!\s)\$", protect, text)

    html = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])

    for i, b in enumerate(blocks):
        html = html.replace(f"\x00M{i}\x00", b)

    # responsive table wrapper
    html = html.replace("<table>", '<div class="table-wrap"><table>')
    html = html.replace("</table>", "</table></div>")

    # image + italic caption -> <figure><figcaption>
    html = re.sub(
        r"<p><img([^>]*?)\s*/?></p>\s*<p><em>(.*?)</em></p>",
        r"<figure><img\1><figcaption>\2</figcaption></figure>",
        html, flags=re.S,
    )
    # bare image -> <figure>
    html = re.sub(r"<p><img([^>]*?)\s*/?></p>", r"<figure><img\1></figure>", html, flags=re.S)
    return html


def strip_front_matter(md):
    if md.lstrip().startswith("---"):
        parts = md.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return md


def split_title_and_body(md):
    """Return (h1, content_md). h1 from the first '# ' line; content starts at
    the first '## ' section, dropping the source's title/meta block and any
    trailing 'Link:' / 'Repository:' footer."""
    h1_match = re.search(r"^#\s+(.+)$", md, flags=re.M)
    h1 = h1_match.group(1).strip() if h1_match else ""

    idx = md.find("\n## ")
    content = md[idx + 1:] if idx != -1 else md

    content = content.rstrip()
    for _ in range(4):
        content = re.sub(r"\*\*(?:Link|Repository)\*\*:[^\n]*\Z", "", content, flags=re.S).rstrip()
        content = re.sub(r"-{3,}\s*\Z", "", content).rstrip()
    return h1, content

# ---- page builders ----------------------------------------------------------

def project_card(p):
    classes = "card featured" if p.get("featured") else "card"
    badge = f'<span class="badge">{p["badge"]}</span>' if p.get("badge") else ""
    highlight = f'<p class="card-highlight">{p["highlight"]}</p>' if p.get("highlight") else ""
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    return f"""<a class="{classes}" href="projects/{p['slug']}.html">
  <div class="card-top">
    <h3 class="card-title">{p['title']}</h3>
    {badge}
  </div>
  <p class="card-desc">{p['desc']}</p>
  {highlight}
  <div class="card-tags">{tags}</div>
  <span class="card-cta">View project <span class="arrow">→</span></span>
</a>"""


def build_home():
    cards = "\n".join(project_card(p) for p in PROJECTS)
    currently = "".join(f"<li>{x}</li>" for x in CURRENTLY)
    previously = "".join(f"<li>{x}</li>" for x in PREVIOUSLY)

    body = f"""<main>
<section class="hero"><div class="container">
  <p class="eyebrow">{HERO_EYEBROW}</p>
  <h1>Gaurav Mitra</h1>
  <p class="role">MSCS @ Georgia Tech <span class="sep">·</span> AI / ML <span class="sep">·</span> graduating May 2027</p>
  <p class="intro">{HERO_INTRO}</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="resume.pdf">Resume</a>
    <a class="btn" href="{GITHUB}" target="_blank" rel="noopener">GitHub ↗</a>
    <a class="btn" href="mailto:{EMAIL}">Email</a>
  </div>
</div></section>

<section><div class="container narrow">
  <div class="facts">
    <div class="fact"><h3>Currently</h3><ul>{currently}</ul></div>
    <div class="fact"><h3>Previously</h3><ul>{previously}</ul></div>
  </div>
</div></section>

<section id="projects"><div class="container">
  <div class="section-head"><h2>Projects</h2></div>
  <div class="projects-grid">
{cards}
  </div>
</div></section>
</main>"""

    html = shell("", "Gaurav Mitra · ML & Computer Vision", HERO_INTRO, body)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("built index.html")


def build_project(p):
    src = ROOT / "projects" / f"{p['slug']}.md"
    md = strip_front_matter(src.read_text(encoding="utf-8"))
    h1, content_md = split_title_and_body(md)
    content_html = convert_markdown(content_md, p.get("mathjax", False))

    meta_html = ""
    if p.get("meta"):
        rows = "".join(f'<div class="row">{r}</div>' for r in p["meta"])
        meta_html = f'<div class="proj-meta">{rows}</div>'

    buttons = [f'<a class="btn btn-primary" href="{p["repo"]}" target="_blank" rel="noopener">GitHub ↗</a>']
    if p.get("paper"):
        buttons.append(f'<a class="btn" href="{p["paper"]}" target="_blank" rel="noopener">Paper (PDF) ↗</a>')
    actions = "\n      ".join(buttons)

    body = f"""<main><div class="container narrow">
  <div class="proj-header">
    <a class="back-link" href="../index.html">← All projects</a>
    <h1>{h1}</h1>
    {meta_html}
    <div class="proj-actions">
      {actions}
    </div>
  </div>
  <article class="prose">
{content_html}
  </article>
</div></main>"""

    html = shell("../", f"{p['title']} · Gaurav Mitra", p["desc"], body, mathjax=p.get("mathjax", False))
    (ROOT / "projects" / f"{p['slug']}.html").write_text(html, encoding="utf-8")
    print(f"built projects/{p['slug']}.html")


def main():
    build_home()
    for p in PROJECTS:
        build_project(p)
    print(f"\nDone: {len(PROJECTS)} project pages + index.html")


if __name__ == "__main__":
    main()
