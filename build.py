#!/usr/bin/env python3
"""
Static site builder for gogo2015.github.io.

Renders index.html from the content below and projects/*.html from the Markdown
sources in projects/*.md. Styles live in assets/css/style.css.

Usage:  python build.py
Then commit the generated index.html and projects/*.html.
"""

import re
import pathlib
import markdown

ROOT = pathlib.Path(__file__).parent

# ---- site content -----------------------------------------------------------

GITHUB = "https://github.com/Gogo2015"
LINKEDIN = "https://linkedin.com/in/mitragaurav"
EMAIL = "mitragaurav10@gmail.com"
PAIR = "https://animesh.garg.tech"

# Add assets/photo.jpg and rebuild to show a photo in the sidebar.
PHOTO = ROOT / "assets" / "photo.jpg"

DESCRIPTION = (
    "Gaurav Mitra is a computer science master's student at Georgia Tech "
    "doing robot learning research in the PAIR Lab."
)

BIO = [
    "I am a master's student in computer science at Georgia Tech, graduating in "
    f'December 2027. I do robot learning research in <a href="{PAIR}">Animesh '
    "Garg's PAIR Lab</a>.",
    "I am interested in post-training foundation models with reinforcement learning.",
]

EXPERIENCE = [
    ("Aug 2026 to present", "Research Assistant, PAIR Lab, Georgia Tech",
     "Sim-to-real robot learning on real hardware."),
    ("Aug 2026 to present", "Graduate Teaching Assistant, Georgia Tech",
     "CS 6601, Artificial Intelligence."),
    ("May to Aug 2026", "Software Engineer Intern, IBM",
     "Shipped 21 production metrics for HashiCorp Vault. Built a proof of concept "
     "for detecting anomalous key usage."),
    ("Jun 2024 to Jan 2025", "Research Assistant, Oden Institute, UT Austin",
     "Quantized convolutional autoencoders for video compression."),
    ("May to Nov 2023", "Software Engineering Intern, Applied Research Laboratories",
     "Backend monitoring services, Docker, and CI/CD to AWS."),
]

EDUCATION = [
    ("2025 to 2027", "MS in Computer Science, Georgia Tech", "AI specialization."),
    ("2022 to 2025", "BS in Aerospace Engineering, UT Austin", "Engineering Honors Program."),
]

# Ordered as shown on the homepage. `meta` rows render under the page title.
PROJECTS = [
    {
        "slug": "vlatune",
        "title": "VLATune",
        "desc": "Reward-weighted filtered behavior cloning for flow-matching VLAs on "
                "LIBERO. A study of whether lightweight RL can improve SmolVLA, with a "
                "negative result.",
        "meta": ["<b>Model:</b> SmolVLA (450M)", "<b>Benchmark:</b> LIBERO"],
        "repo": f"{GITHUB}/VLATune",
        "paper": f"{GITHUB}/VLATune/blob/main/paper/main.pdf",
    },
    {
        "slug": "liver-transplant",
        "title": "Liver Transplant Outcome Prediction",
        "desc": "A full ML pipeline on the OPTN/SRTR national registry predicting graft "
                "failure with classification and survival analysis across ~87k "
                "transplants. Best Project Award in CS 7641.",
        "meta": [
            "<b>Course:</b> CS 7641, Machine Learning (Georgia Tech)",
            "<b>Award:</b> Best Project Award",
            "<b>Team:</b> Anushka Bajpai, Madhavan Balasubramaniam, Sanjay Gorur, Ameel Jani, Gaurav Mitra",
            "<b>Clinical advisor:</b> Dr. Marwan Kazimi",
        ],
        "repo": f"{GITHUB}/liver-transplant-ml",
    },
    {
        "slug": "waymo",
        "title": "Waymo Motion Forecasting",
        "desc": "Trajectory prediction on the Waymo Open Motion Dataset, with a Conv-MLP "
                "baseline and a multi-modal extension predicting six futures with "
                "confidence. 73% ADE reduction with multi-modal prediction.",
        "repo": f"{GITHUB}/WaymoMotionEstimator",
        "paper": f"{GITHUB}/WaymoMotionEstimator/blob/main/ConvMLPPaper.pdf",
    },
    {
        "slug": "gnn-homo-lumo",
        "title": "GNN Molecular Property Prediction",
        "desc": "Predicting the HOMO-LUMO gap from 2D molecular graphs with a deep "
                "edge-aware GINE network, and testing whether a Virtual Node helps. "
                "0.142 eV MAE on 3.38M molecules (PCQM4Mv2).",
        "meta": [
            "<b>Course:</b> CS 7643, Deep Learning (Georgia Tech), final project",
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
        "meta": ["<b>Course:</b> CS 6390, Programming Languages, final project"],
        "repo": f"{GITHUB}/llm-semantic-syntax",
    },
    {
        "slug": "earthquake",
        "title": "Earthquake Analysis Web App",
        "desc": "A containerized Flask REST API over USGS earthquake data with Redis "
                "storage, async job processing, and server-side charting, deployed to Kubernetes.",
        "repo": f"{GITHUB}/EarthquakeAnalyzer",
    },
    {
        "slug": "autoencoder",
        "title": "Video Compression Autoencoder",
        "desc": "A quantized 3D-convolutional autoencoder for video compression, with "
                "tunable codebook sizes controlling the rate-distortion tradeoff on Moving MNIST.",
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


def shell(prefix, title, description, body, mathjax=False):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{MATHJAX if mathjax else ""}
</head>
<body>
{body}
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
        content = re.sub(r"\*\*(?:Link|Repository):?\*\*:?[^\n]*\Z", "", content, flags=re.S).rstrip()
        content = re.sub(r"-{3,}\s*\Z", "", content).rstrip()
    return h1, content

# ---- page builders ----------------------------------------------------------

def timeline(rows):
    return "\n".join(
        f"""<div class="entry">
  <p class="when">{when}</p>
  <div><p class="what">{what}</p><p class="detail">{detail}</p></div>
</div>"""
        for when, what, detail in rows
    )


def project_links(p):
    links = [f'<a href="{p["repo"]}">Code</a>']
    if p.get("paper"):
        links.append(f'<a href="{p["paper"]}">Paper</a>')
    return "".join(links)


def project_row(p):
    return f"""<div class="project">
  <h3><a href="projects/{p['slug']}.html">{p['title']}</a></h3>
  <p class="detail">{p['desc']}</p>
  <p class="links">{project_links(p)}</p>
</div>"""


def build_home():
    photo = '<img class="photo" src="assets/photo.jpg" alt="Gaurav Mitra">' if PHOTO.exists() else ""
    bio = "\n".join(f"<p>{x}</p>" for x in BIO)
    projects = "\n".join(project_row(p) for p in PROJECTS)

    body = f"""<div class="home">
<aside class="side">
  {photo}
  <h1>Gaurav Mitra</h1>
  <p class="role">Computer science master's student<br>Georgia Tech</p>
  <ul class="contact">
    <li><a href="resume.pdf">Resume</a></li>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><a href="{GITHUB}">GitHub</a></li>
    <li><a href="{LINKEDIN}">LinkedIn</a></li>
  </ul>
</aside>
<main>
{bio}
<h2>Experience</h2>
{timeline(EXPERIENCE)}
<h2>Projects</h2>
{projects}
<h2>Education</h2>
{timeline(EDUCATION)}
</main>
</div>"""

    (ROOT / "index.html").write_text(shell("", "Gaurav Mitra", DESCRIPTION, body), encoding="utf-8")
    print("built index.html")


def build_project(p):
    src = ROOT / "projects" / f"{p['slug']}.md"
    md = strip_front_matter(src.read_text(encoding="utf-8"))
    h1, content_md = split_title_and_body(md)
    content_html = convert_markdown(content_md, p.get("mathjax", False))

    meta = "".join(f"<p>{r}</p>" for r in p.get("meta", []))
    meta_html = f'<div class="meta">{meta}</div>' if meta else ""

    body = f"""<div class="project-page">
<p class="home-link"><a href="../index.html">Gaurav Mitra</a></p>
<main>
  <h1>{h1}</h1>
  {meta_html}
  <p class="links">{project_links(p)}</p>
  <article class="prose">
{content_html}
  </article>
</main>
</div>"""

    html = shell("../", f"{p['title']} | Gaurav Mitra", p["desc"], body, mathjax=p.get("mathjax", False))
    (ROOT / "projects" / f"{p['slug']}.html").write_text(html, encoding="utf-8")
    print(f"built projects/{p['slug']}.html")


def main():
    build_home()
    for p in PROJECTS:
        build_project(p)
    print(f"\nDone: {len(PROJECTS)} project pages + index.html")


if __name__ == "__main__":
    main()
