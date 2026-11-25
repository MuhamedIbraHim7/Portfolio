# Mohamed Ibrahim · Applied AI Engineer

A static portfolio with six engineering case studies, a project index, professional experience, teaching, recognition and a downloadable CV. The site serves complete HTML under the existing GitHub Pages project path. [Live portfolio](https://muhamedibrahim7.github.io/Portfolio/)

## Run locally

Use Python 3.9 or newer. From the repository root, regenerate the pages and serve the parent directory to reproduce the Pages URL structure.

```sh
python3 -B scripts/build.py
python3 -B scripts/check_site.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory ..
```

Open [the local portfolio](http://127.0.0.1:8000/Portfolio/) when the checkout directory is named `Portfolio`. Visitors receive plain HTML, CSS, JavaScript and local assets. Python is an authoring tool. The browser and deployment workflow use the committed files directly.

## Where changes belong

| Change | Source |
| --- | --- |
| Project copy, results, evidence, media and order | [Project data](content/projects.json) |
| Achievement entries and credentials | [Recognition data](content/recognition.json) |
| Skill depth and project references | [Skills data](content/skills.json) |
| Homepage, timeline, teaching and contact | [Homepage template](templates/home.html) |
| Shared navigation and metadata | [Layout](templates/layout.html) and [builder](scripts/build.py) |
| Case study and project index layouts | [Case study](templates/case.html) and [index](templates/projects.html) |
| Responsive layout, themes and interactions | [Stylesheet](assets/styles.css) and [JavaScript](assets/main.js) |
| CV download | [Mohamed-Ibrahim-AI-Engineer.pdf](Mohamed-Ibrahim-AI-Engineer.pdf) |

Run the builder after editing source content. Commit the generated HTML and sitemap alongside the source. The first three project entries appear on the homepage. [Portfolio maintenance and media checklist](docs/CONTENT_GUIDE.md)

## Review and deployment

The checked-in workflow deploys the repository root on a push to `main` or a manual dispatch. At audit time GitHub also reported branch-based Pages publishing from `main` at `/`. A feature branch can be reviewed and tested locally before merging. [Deployment workflow](.github/workflows/deploy.yml)

- [Before-and-after screenshots](docs/COMPARISON.md)
- [Audit, evidence decisions and open content questions](docs/PORTFOLIO_AUDIT.md)
- [Suggested scripts for three project demos](docs/DEMO_SCRIPTS.md)
- [Test methods, measured results and limits](docs/TEST_REPORT.md)

## Assets

The portrait is credited to Mohamed’s BOKRANA instructor profile. The learning-platform image is a capture of BOKRANA’s public landing page. The project thumbnails are original architecture illustrations. DM Sans is self-hosted under the SIL Open Font License. [Instructor profile](https://bokrana.lovable.app/en/about) · [BOKRANA](https://bokrana.lovable.app/) · [Font license](assets/fonts/OFL.txt)
