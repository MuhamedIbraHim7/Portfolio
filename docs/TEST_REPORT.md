# Redesign test report

Tested on 25 November 2026 with Chromium 156.0.8078.79, Playwright 1.62.0, axe-core 4.14.1 and Lighthouse 13.6.0. The review build was served from a loopback HTTP test fixture mounted at `/Portfolio/`. The managed visual preview relay timed out during startup. Browser tests, captures and Lighthouse used the same repository files and project subpath as the intended deployment.

## Functional and accessibility results

| Check | Result |
| --- | --- |
| Responsive layout | All 8 pages at 375, 390, 768, 1024 and 1440 CSS pixels passed 40 viewport checks. No document-level horizontal overflow. All images decoded at every width. |
| Runtime health | Zero page exceptions, console errors, failed requests or HTTP error responses during the 40 route/viewport visits. |
| Keyboard navigation | The first Tab reveals the skip link. Enter moves focus to main. Mobile navigation opens with Enter, closes with Escape and restores focus. Selecting a section closes the menu. Desktop navigation returns when resized. |
| Theme | Followed the system preference and its change while the page was open. A manual selection persisted after reload. Switching also worked with local storage unavailable. |
| Project index | All six case studies available without filtering. Every category produced the expected card count and live status. Enter activated filters. Reload, browser Back/Forward and unknown categories behaved correctly. |
| Case studies and media | Index links opened case studies. Section links reached their targets. Architecture diagrams, responsive images and BOKRANA’s gallery loaded. Five renderer types were exercised with synthetic authoring fixtures. Future MP4 and YouTube playback needs testing with the actual supplied media. |
| CV | A real browser download retained the expected filename and matched the supplied PDF byte for byte. SHA-256 was `aec8d77421f9f9091cff90a1e2bf7492dfaaaa57c49621ae54d3fbb8dbe21dec`. |
| Progressive enhancement | With JavaScript disabled, mobile navigation, the project grid and case-study links remained available. Native recognition disclosures opened with the keyboard. Reduced-motion emulation disabled smooth scrolling. |
| Accessibility and contrast | 16 axe scans across 8 pages in desktop light and mobile dark themes reported zero violations in the selected WCAG A/AA and best-practice rules. Achievement groups were expanded for scanning. Corrected a skipped heading level and the mobile brand link’s accessible name during testing. |
| Static integrity | 285 same-site URL and fragment references resolved beneath the project path. Checked the sitemap’s exact URL set, canonical URLs, JSON-LD, heading and ID uniqueness, font, image dimensions, social image and PDF signature. |
| External links | HTTP GET returned 200 for 12 distinct public URLs, including BOKRANA, LinkedIn, GitHub, the published site and evaluation evidence. Two GitHub HTML blob routes returned 503 during initial testing. The final links use the working commit-pinned raw files. |
| Deployment compatibility | The branch uses committed HTML and relative asset paths. The deployed artifact path is the repository root. Compared the workflow with the main baseline and parsed its configuration. The PR awaits review before production deployment. |

## Lighthouse homepage measurements

| Preset | Performance | Accessibility | Best practices | SEO | LCP | TBT | CLS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mobile | 99 | 100 | 100 | 100 | 2.0 s | 0 ms | 0 |
| Desktop | 100 | 100 | 100 | 100 | 0.4 s | 0 ms | 0 |

These are individual local lab runs using Lighthouse’s mobile and desktop configurations. Hosting cache headers, mobile networks and real visitor devices can change the results. WCAG conformance and screen-reader usability require additional human assessment. Safari, Firefox, physical devices and a production deployment of the redesign were outside this run.

## Reproduce

From the repository root, use the local server instructions in [the README](../README.md). For the optional browser suite, install Playwright for Python and Chromium in a development environment. Supply the actual installed Chromium executable and a local copy of axe-core. The website itself has no dependency on these QA tools.

```sh
python3 -B scripts/build.py --check
python3 -B scripts/check_site.py
node --check assets/main.js
python3 -B scripts/browser_check.py http://127.0.0.1:8000/Portfolio/ \
  --chromium /usr/bin/chromium --axe /path/to/axe-core/axe.min.js
```

Lighthouse was run with the `performance,accessibility,best-practices,seo` categories against the homepage, first with the default mobile configuration and then with `--preset=desktop`. The browser suite and static checker can run independently. [Visual comparison](COMPARISON.md)
