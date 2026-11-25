"""Render the committed GitHub Pages site with the Python standard library."""
import argparse
import json
import re
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://muhamedibrahim7.github.io/Portfolio/"
GITHUB = "https://github.com/MuhamedIbraHim7"
LINKEDIN = "https://linkedin.com/in/mohamedibrahim18"
CV = "Mohamed-Ibrahim-AI-Engineer.pdf"
ART = {"Automation": "automation", "Retrieval": "retrieval", "Voice AI": "voice", "Agent systems": "agents"}

ICON_PATHS = {
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 16v4h16v-4"/>',
    "location": '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/>',
    "github": '<path d="M9 20c-4 1.2-4-2-6-2m12 4v-3.2c0-1 .1-1.7-.6-2.4 3-.3 6.1-1.4 6.1-6.6a5.1 5.1 0 0 0-1.4-3.6 4.8 4.8 0 0 0-.1-3.6s-1.2-.4-3.8 1.4a13 13 0 0 0-7 0C5.6 2.2 4.4 2.6 4.4 2.6a4.8 4.8 0 0 0-.1 3.6A5.1 5.1 0 0 0 3 9.8c0 5.2 3.1 6.3 6.1 6.6-.6.6-.8 1.4-.7 2.2V22"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7.5 10v7m0-10v.2M11.5 17v-7m0 3a3 3 0 0 1 6 0v4"/>',
    "sun": '<circle cx="12" cy="12" r="3.5"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4m0-14.2-1.4 1.4M6.3 17.7l-1.4 1.4"/>',
    "moon": '<path d="M20.5 14A8.5 8.5 0 0 1 10 3.5a8.5 8.5 0 1 0 10.5 10.5Z"/>',
    "menu": '<path d="M3 7h18M3 12h18M3 17h18"/>',
    "close": '<path d="m5 5 14 14M19 5 5 19"/>',
    "plus": '<path d="M5 12h14m-7-7v14"/>',
    "file": '<path d="M6 3h8l4 4v14H6zM14 3v5h4m-9 5h6m-6 3h6"/>',
    "check": '<path d="m4 12 5 5L20 6"/>',
}
SYMBOLS = '<svg xmlns="http://www.w3.org/2000/svg" class="symbol-library" aria-hidden="true"><defs>' + ''.join(
    f'<symbol id="i-{name}" viewBox="0 0 24 24">{path}</symbol>' for name, path in ICON_PATHS.items()
) + '</defs></svg>'
WORDMARK = '<svg class="brand-mark" aria-hidden="true" viewBox="0 0 48 48"><rect width="48" height="48" rx="10"/><path d="M8 33V15h4l7 10 7-10h4v18h-5V23l-6 8-6-8v10Zm27-18h5v18h-5Z"/></svg>'


def icon(name):
    return f'<svg class="icon icon-{name}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def data(name):
    return json.loads((ROOT / "content" / f"{name}.json").read_text())


def template(name, **fields):
    return Template((ROOT / "templates" / f"{name}.html").read_text()).substitute(fields)


def external(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname:
        raise ValueError(f"Expected a public HTTPS link: {url}")
    return escape(url, quote=True)


def asset(path, root):
    if not path.startswith("assets/") or ".." in Path(path).parts or not (ROOT / path).is_file():
        raise ValueError(f"Missing or invalid local asset: {path}")
    return escape(root + path, quote=True)


def tags(values):
    return '<ul class="tags">' + ''.join(f'<li>{escape(v)}</li>' for v in values) + '</ul>'


def media(items, root):
    figures = []
    for item in items:
        kind = item["type"]
        caption = escape(item["caption"])
        if kind == "image":
            image = asset(item["src"], root)
            visual = (f'<a href="{image}"><img src="{image}" alt="{escape(item["alt"])}" '
                      f'width="{int(item["width"])}" height="{int(item["height"])}" loading="lazy" decoding="async"></a>')
        elif kind == "mp4":
            video = asset(item["src"], root)
            captions = asset(item["captions"], root)
            lang = escape(item.get("lang", "en"))
            visual = (f'<video controls playsinline preload="none" aria-label="{caption}"><source src="{video}" type="video/mp4">'
                      f'<track kind="captions" src="{captions}" srclang="{lang}" label="{lang}" default></video>')
        elif kind in ("youtube", "demo", "article"):
            label = {"youtube": "Watch on YouTube", "demo": "Open live demo", "article": "Read article"}[kind]
            visual = f'<a class="text-link" href="{external(item["url"])}">{label} · {caption}</a>'
        else:
            raise ValueError(f"Unknown media type: {kind}")
        figures.append(f'<figure class="media-item">{visual}<figcaption>{caption}</figcaption></figure>')
    return ''.join(figures)


def card(project, root):
    p = project
    path = root + "projects/" + p["slug"] + "/"
    if p.get("thumbnail"):
        cover = p["thumbnail"]
    elif p["category"] == "Education" and p["media"] and p["media"][0]["type"] == "image":
        cover = p["media"][0]["src"]
    else:
        cover = "assets/art/" + ART.get(p["category"], "agents") + ".svg"
    heading = "h2" if root else "h3"
    role = ""
    direct = ""
    if root:
        role = f'<p class="card-role"><strong>Role</strong> {escape(p["role"])}</p>'
        if p["links"]:
            link = p["links"][0]
            direct = f'<a class="text-link" href="{external(link["url"])}">{escape(link["label"])}</a>'
    return f'''<article class="project-card" data-category="{escape(p["category"])}">
  <a class="card-cover" href="{path}" tabindex="-1" aria-hidden="true"><img src="{asset(cover, root)}" width="560" height="230" alt="" loading="lazy"></a>
  <div class="card-meta"><span>{escape(p["category"])}</span><span>{escape(p["status"])}</span></div>
  <{heading}><a href="{path}">{escape(p["title"])}</a></{heading}>
  <p>{escape(p["summary"])}</p>{tags(p["stack"][:3])}{role}
  <div class="card-bottom"><span>{escape(p["outcome"])}</span><div class="card-links"><a class="text-link" href="{path}">Case study<span class="sr-only"> — {escape(p["title"])}</span></a>{direct}</div></div>
</article>'''


def skill_list():
    parts = []
    for title, level, detail, slug in data("skills"):
        source = ""
        if slug:
            source = f'<a class="skill-evidence" href="projects/{slug}/">Case study<span class="sr-only"> for {escape(title)}</span></a>'
        parts.append(f'<div class="skill"><div><p class="level">{escape(level)}</p><h3>{escape(title)}</h3><p>{escape(detail)}</p></div>{source}</div>')
    return ''.join(parts)


def recognition_list():
    groups = []
    for index, group in enumerate(data("recognition")):
        entries = []
        for item in group["items"]:
            link = f'<a class="text-link" href="{external(item["url"])}">View credential</a>' if item.get("url") else ""
            entries.append(f'<li><span class="period">{escape(item["date"])}</span><h3>{escape(item["name"])}</h3><p>{escape(item["detail"])}</p>{link}{media(item.get("media", []), "")}</li>')
        groups.append(f'<details{" open" if index == 0 else ""}><summary>{escape(group["title"])}{icon("plus")}</summary><ul>{"".join(entries)}</ul></details>')
    return ''.join(groups)


def case_page(p):
    fields = {k: escape(v) for k, v in p.items() if isinstance(v, str)}
    steps = ''.join(f'<li><strong>{escape(s["title"])}</strong><p>{escape(s["detail"])}</p></li>' for s in p["architecture"])
    links = ''.join(f'<a class="button secondary" href="{external(link["url"])}">{escape(link["label"])}</a>' for link in p["links"])
    if not links:
        links = f'<a class="button secondary" download href="../../{CV}">{icon("download")} Download CV</a>'
    gallery = media(p["media"], "../../")
    return template("case", **fields, steps=steps, stack=tags(p["stack"]), links=links,
                    flow_title="Learner journey" if p["category"] == "Education" else "System flow",
                    evidence=''.join(f'<li>{escape(e)}</li>' for e in p["evidence"]),
                    media_section=f'<section id="media"><h2>Media &amp; walkthroughs</h2>{gallery}</section>' if gallery else "",
                    media_link='<a href="#media">Media</a>' if gallery else "", grid=icon("grid"))


def render_page(path, title, description, main, schema):
    depth = len(Path(path).parts) - 1
    root = "../" * depth
    home = root if depth else ""
    links = [(root + "projects/", "Projects"), (home + "#experience", "Experience"),
             (home + "#skills", "Skills"), (home + "#teaching", "Teaching")]
    nav = ''.join(f'<a href="{href}"' + (' aria-current="page"' if path == "projects/index.html" and label == "Projects" else '') + f'>{label}</a>' for href, label in links)
    return template("layout", title=escape(title), description=escape(description), root=root, home=home,
                    canonical=SITE + path.removesuffix("index.html"), share_image=SITE + "assets/og-image.png",
                    og_type="article" if depth == 2 else "website", nav=nav, main=main, wordmark=WORDMARK,
                    symbols=SYMBOLS, schema=json.dumps(schema, ensure_ascii=False).replace("<", r"\u003c"),
                    **{k: icon(k) for k in ("menu", "close", "moon", "sun")})


def build():
    projects = data("projects")
    slugs = [p["slug"] for p in projects]
    if len(slugs) != len(set(slugs)) or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s) for s in slugs):
        raise ValueError("Every project needs a unique URL-safe slug.")
    home = template("home", count=len(projects), featured=''.join(card(p, "") for p in projects[:3]),
                    skills=skill_list(), recognition=recognition_list(), cv=CV, github=GITHUB, linkedin=LINKEDIN,
                    github_icon=icon("github"), linkedin_icon=icon("linkedin"), grid=icon("grid"),
                    download=icon("download"), location=icon("location"))
    person = {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "#mohamed",
              "name": "Mohamed Ibrahim", "jobTitle": "Applied AI Engineer", "url": SITE,
              "image": SITE + "assets/images/mohamed-900.webp", "sameAs": [GITHUB, LINKEDIN],
              "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"}}
    pages = {"index.html": render_page("index.html", "Mohamed Ibrahim · Applied AI Engineer",
             "Cairo-based AI engineer and generative AI instructor. Explore Arabic document search, real-time voice AI and agent workflows through technical case studies.", home, person)}
    categories = list(dict.fromkeys(p["category"] for p in projects))
    buttons = ['<button type="button" data-filter="" aria-pressed="true">All work</button>']
    for category in categories:
        buttons.append(f'<button type="button" data-filter="{escape(category)}" aria-pressed="false">{escape(category)}</button>')
    listings = template("projects", filters=''.join(buttons), count=len(projects), cards=''.join(card(p, "../") for p in projects))
    collection = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Engineering projects", "url": SITE + "projects/"}
    pages["projects/index.html"] = render_page("projects/index.html", "Engineering projects · Mohamed Ibrahim",
             "Browse case studies in retrieval, voice AI, automation, agent systems and education.", listings, collection)
    for p in projects:
        path = f'projects/{p["slug"]}/index.html'
        schema = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"],
                  "description": p["summary"], "author": {"@type": "Person", "name": "Mohamed Ibrahim", "@id": person["@id"]},
                  "url": SITE + path.removesuffix("index.html")}
        pages[path] = render_page(path, p["title"] + " · Mohamed Ibrahim", p["summary"], case_page(p), schema)
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path in pages:
        ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = SITE + path.removesuffix("index.html")
    ET.indent(sitemap, space="  ")
    pages["sitemap.xml"] = ET.tostring(sitemap, encoding="unicode", xml_declaration=True) + "\n"
    return pages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report stale or missing generated files.")
    options = parser.parse_args()
    outputs = build()
    for relative, contents in outputs.items():
        file = ROOT / relative
        if options.check:
            if not file.is_file() or file.read_text() != contents:
                raise SystemExit(f"Regenerate {relative} with python3 scripts/build.py")
        else:
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(contents)
    print(f'{"Checked" if options.check else "Rendered"} {len(outputs) - 1} pages and the sitemap.')
