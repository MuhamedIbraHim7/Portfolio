"""Check the generated site, including links and assets under the Pages subpath."""
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

from build import ROOT, SITE, build


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.refs = []
        self.canonical = None
        self.h1_count = 0
        self.schema = []
        self.in_schema = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a["href"]
        if tag == "meta" and a.get("property", a.get("name")) in ("og:image", "twitter:image"):
            self.refs.append(a["content"])
        if tag == "img" and ("alt" not in a or not a.get("width") or not a.get("height")):
            raise ValueError(f"Missing img alt or dimensions: {a}")
        self.refs.extend(a[key] for key in ("src", "href") if key in a)
        self.refs.extend(entry.strip().split()[0] for entry in a.get("srcset", "").split(",") if entry.strip())
        if tag == "script":
            self.in_schema = a.get("type") == "application/ld+json"

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_schema = False

    def handle_data(self, text):
        if self.in_schema:
            self.schema.append(json.loads(text))


def verify():
    outputs = build()
    pages = {}
    for relative, expected in outputs.items():
        path = ROOT / relative
        assert path.read_text() == expected, f"Stale generated file: {relative}"
        if path.suffix != ".html":
            continue
        doc = Document(expected)
        assert doc.h1_count == 1 and len(doc.schema) == 1, relative
        duplicates = [key for key, count in Counter(doc.ids).items() if count > 1]
        assert not duplicates, (relative, duplicates)
        assert doc.canonical == SITE + relative.removesuffix("index.html"), relative
        pages[path] = doc

    references = 0
    for path, doc in pages.items():
        for ref in doc.refs:
            url = urlsplit(urljoin(doc.canonical, ref))
            if url.netloc != urlsplit(SITE).netloc:
                continue
            assert url.path.startswith(urlsplit(SITE).path), (path, ref)
            target = ROOT / unquote(url.path.removeprefix(urlsplit(SITE).path))
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), (path, ref)
            if url.fragment:
                assert target in pages and unquote(url.fragment) in pages[target].ids, (path, ref)
            references += 1

    css = ROOT / "assets/styles.css"
    for match in re.findall(r'url\(["\']?([^)"\']+)', css.read_text()):
        assert (css.parent / match).is_file(), match
    locations = ET.parse(ROOT / "sitemap.xml").findall(".//{*}loc")
    assert {node.text for node in locations} == {d.canonical for d in pages.values()}
    assert (ROOT / "Mohamed-Ibrahim-AI-Engineer.pdf").read_bytes().startswith(b"%PDF-")
    print(f"{len(pages)} pages, {references} internal URL/fragment references, sitemap, PDF and font verified.")


if __name__ == "__main__":
    verify()
