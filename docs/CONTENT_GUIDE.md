# Maintaining the portfolio

## Add or update a case study

1. Edit [projects.json](../content/projects.json). Copy an existing entry with a similar project status.
2. Give it a unique lowercase, hyphenated slug. The slug becomes a published URL. Keep existing slugs stable when renaming titles.
3. Write the problem, intended audience, your contribution, the implementation decision and a bounded result. Distinguish professional deployments, public prototypes and learning platforms. Put evaluation scope, denominators and source limitations in the case itself.
4. Add the technology stack, three to five architecture steps, trade-off, reliability considerations, data handling and a proposed next step. Use the architecture steps to document the real flow. For an education platform, describe the learner journey.
5. Use `links` for public evidence and products. Each entry has a descriptive `label` and an HTTPS `url`. The first link is also offered on the project index. Store the evidence revision or date in `evidence`. Empty links on a CV-backed professional case offer the CV download.
6. Order the list by featured priority. The first three cases appear on the home page. Category filters, counts, the collection, case pages and sitemap update together.
7. Regenerate the site and run the checks in [the README](../README.md). When retiring a page, account for links to its former URL. The builder deliberately leaves old files on disk so an editor can supply a redirect or decide how to handle the address.

The renderer escapes authored text. Keep HTML out of JSON fields. Local media paths start with `assets/`. Store public assets in the repository so browser requests work beneath `/Portfolio/`.

## Screenshots, galleries, videos and articles

Use the optional `thumbnail` field for a custom project cover. Supply the repository-relative path to a real screenshot or an architecture illustration. The default illustrations follow the project category. Put evidence and demos in the ordered `media` array. An empty array omits the section and its navigation link.

| Type | Required fields | Result |
| --- | --- | --- |
| `image` | `src`, `alt`, `caption`, `width`, `height` | Responsive lazy-loaded image with intrinsic dimensions and a full-size link. Add multiple entries for a gallery. |
| `mp4` | `src`, `captions` (WebVTT file), `caption` | Native video controls, no autoplay and no video preload. Optional `lang` sets the captions language, defaulting to English. |
| `youtube` | `url`, `caption` | Descriptive link to the hosted walkthrough. Visitors choose when to load the player. |
| `demo` | `url`, `caption` | Link to a public working application. |
| `article` | `url`, `caption` | Link to a technical write-up. |

[BOKRANA’s case](../content/projects.json) includes a working image entry. For a local video, add the actual MP4 and captions before entering their paths. Use an accurate human-readable caption for each item. Keep video clips short and document any mocked inputs. Suggested recording outlines are in [the demo scripts](DEMO_SCRIPTS.md).

## Recognition, teaching and work history

Use [recognition.json](../content/recognition.json) for expandable achievement groups. Each item has a date, name and description. An optional public `url` adds a credential link. An optional `media` array takes the same entries as a project, including certificate images. Use the actual credential name, issuer and issue date available from the evidence.

Use [skills.json](../content/skills.json) for the category, experience level, specific capability and supporting project slug. Use an empty slug for working knowledge where there is no relevant case. Edit the signed-off roles, time periods and teaching narrative in [home.html](../templates/home.html). Review any “present” role when updating the CV.

## Update the portrait, CV or social preview

- Replace the two optimized WebP portrait files, using a common crop and natural proportions at 480 and 900 pixels wide. Update intrinsic dimensions, photo alt text and crop positioning in the homepage template when the subject or proportions change.
- Replace the PDF at its existing filename to preserve downloads and bookmarks. Verify the dates, email and SHA-256 of the actual downloaded file.
- Update the 1200 × 630 image at `assets/og-image.png` when the name, role or portrait changes. The favicon and monogram share the same design. The social image uses the local portrait and DM Sans.

## Before opening a content PR

- [ ] Check each claim against a public source, published evaluation artifact or the latest supplied CV.
- [ ] Name the role, project status and evaluation scope. Distinguish suggestions for future work from shipped functionality.
- [ ] Use approved, public or synthetic material for screenshots and video. Inspect for CRM records, private documents, identifiers, payment data, credentials and voices lacking consent.
- [ ] Check links, image dimensions, alt text, video captions and mobile cropping. Remove controls for unavailable media.
- [ ] Run the builder and static checks. Open the changed case under the Pages subpath in both themes and exercise its controls.
- [ ] Review the generated diff and include updated screenshots when a change affects layout. Check outstanding questions in [the audit](PORTFOLIO_AUDIT.md).
