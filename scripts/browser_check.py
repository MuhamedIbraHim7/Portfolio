"""Exercise a locally served GitHub Pages tree using Playwright Chromium."""
import argparse
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / "content/projects.json").read_text())
ROUTES = ["", "projects/"] + [f'projects/{p["slug"]}/' for p in PROJECTS]
VIEWPORTS = [(375, 812), (390, 844), (768, 1024), (1024, 768), (1440, 900)]
CV = ROOT / "Mohamed-Ibrahim-AI-Engineer.pdf"


def check_layout(page, url):
    assert page.goto(url).status == 200, url
    page.evaluate("document.fonts.ready")
    assert page.locator("h1").count() == 1, url
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), url
    images = page.locator("img")
    for image in images.all():
        image.scroll_into_view_if_needed()
        image.evaluate("img => img.decode()")
        assert image.evaluate("img => img.naturalWidth > 0"), url


def check_interactions(browser, base):
    page = browser.new_page(viewport={"width": 390, "height": 844}, color_scheme="light", reduced_motion="reduce")
    page.goto(base)
    page.keyboard.press("Tab")
    assert page.locator(".skip").evaluate("el => document.activeElement === el")
    page.keyboard.press("Enter")
    assert page.locator("main").evaluate("el => document.activeElement === el")
    assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"

    nav = page.locator("#primary-nav")
    menu = page.locator("#menu-toggle")
    assert not nav.is_visible()
    menu.focus()
    page.keyboard.press("Enter")
    assert nav.is_visible()
    page.keyboard.press("Escape")
    assert not nav.is_visible() and menu.evaluate("e => document.activeElement === e")
    menu.click()
    nav.get_by_role("link", name="Experience").click()
    assert page.url.endswith("#experience") and not nav.is_visible()
    page.set_viewport_size({"width": 1440, "height": 900})
    assert nav.is_visible() and not menu.is_visible()

    theme = page.locator("#theme-toggle")
    assert theme.get_attribute("data-current") == "light"
    page.emulate_media(color_scheme="dark")
    page.wait_for_function("document.querySelector('#theme-toggle').dataset.current === 'dark'")
    theme.click()
    page.reload()
    assert theme.get_attribute("data-current") == "light"

    page.goto(base)
    with page.expect_download() as capture:
        page.locator(".hero [download]").click()
    download = capture.value
    assert download.suggested_filename == CV.name
    assert sha256(Path(download.path()).read_bytes()).digest() == sha256(CV.read_bytes()).digest()
    for detail in page.locator(".recognition-list details").all():
        if detail.get_attribute("open") is None:
            summary = detail.locator("summary")
            summary.focus()
            page.keyboard.press("Enter")
        assert detail.locator("li").first.is_visible()
    page.locator(".hero .primary").click()
    assert page.url.endswith("projects/")
    active_cards = page.locator(".catalog .project-card:visible")
    assert active_cards.count() == len(PROJECTS)
    counts = Counter(p["category"] for p in PROJECTS)
    for category, count in counts.items():
        control = page.get_by_role("button", name=category, exact=True)
        control.focus()
        page.keyboard.press("Enter")
        assert control.get_attribute("aria-pressed") == "true"
        assert active_cards.count() == count
        assert page.get_by_role("status").inner_text() == f'{count} {"project" if count == 1 else "projects"}'
    page.reload()
    last_category = list(counts)[-1]
    assert page.get_by_role("button", name=last_category, exact=True).get_attribute("aria-pressed") == "true"
    page.get_by_role("button", name="All work").click()
    assert active_cards.count() == len(PROJECTS)
    page.go_back()
    assert active_cards.count() == counts[last_category]
    page.go_forward()
    page.goto(urljoin(base, "projects/?category=unknown"))
    assert active_cards.count() == len(PROJECTS)
    page.locator(".card-links").first.get_by_role("link", name="Case study", exact=False).click()
    assert page.locator(".flow li").count() >= 3
    page.get_by_role("link", name="System design", exact=True).click()
    assert page.url.endswith("#architecture")
    page.close()

    plain = browser.new_context(java_script_enabled=False, viewport={"width": 375, "height": 812})
    pg = plain.new_page()
    pg.goto(base)
    assert pg.locator("#primary-nav").is_visible()
    assert pg.get_by_role("link", name="Explore projects").is_visible()
    pg.locator(".hero .primary").click()
    assert pg.locator(".project-card:visible").count() == len(PROJECTS)
    assert not pg.locator(".filter-bar").is_visible()
    plain.close()

    restricted = browser.new_context()
    restricted.add_init_script("Object.defineProperty(window, 'localStorage', { get() { throw new Error('storage unavailable') } })")
    pg = restricted.new_page()
    pg.goto(base)
    before = pg.locator("#theme-toggle").get_attribute("data-current")
    pg.locator("#theme-toggle").click()
    assert pg.locator("#theme-toggle").get_attribute("data-current") != before
    restricted.close()


def run(args):
    errors = []
    audits = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=args.chromium)
        for w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("response", lambda r: errors.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            page.on("requestfailed", lambda r: errors.append(f"{r.failure} {r.url}"))
            for route in ROUTES:
                check_layout(page, urljoin(args.url, route))
            page.close()
        check_interactions(browser, args.url)
        if args.axe:
            for mode, width in (("light", 1440), ("dark", 390)):
                page = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=mode)
                for route in ROUTES:
                    page.goto(urljoin(args.url, route))
                    page.evaluate("document.fonts.ready")
                    if route == "":
                        page.locator(".recognition-list details").evaluate_all("els => els.forEach(e => e.open = true)")
                    page.add_script_tag(path=args.axe)
                    violations = page.evaluate("""async () => (await axe.run(document, {
                      runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']
                    })).violations.map(v => ({id:v.id, targets:v.nodes.map(n=>n.target)}))""")
                    if violations:
                        audits.append((route, mode, violations))
                page.close()
        print("Chromium", browser.version)
        browser.close()
    print(f"{len(ROUTES) * len(VIEWPORTS)} layout checks. Browser and resource errors: {len(errors)}.")
    if args.axe:
        print(f"{2 * len(ROUTES)} axe scans. Scans with violations: {len(audits)}.")
    assert not errors, errors
    assert not audits, audits
    print("Navigation, theme, filters, history, PDF download, disclosures, keyboard, reduced motion and no-JS checks passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Local server URL ending in /Portfolio/")
    parser.add_argument("--chromium", help="Installed Chromium executable")
    parser.add_argument("--axe", help="Path to an optional local axe.min.js")
    options = parser.parse_args()
    if not options.url.endswith("/"):
        parser.error("Pass the directory URL with its trailing slash.")
    run(options)
