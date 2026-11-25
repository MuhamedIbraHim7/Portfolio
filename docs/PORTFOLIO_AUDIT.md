# Portfolio audit and editorial decisions

Reviewed on 25 November 2026 from main at `7b8c9c0`. The baseline contained a single HTML page, one stylesheet, one script, a PDF, a README and one deployment workflow. The public URL returned HTTP 200. The baseline desktop and mobile captures are in [review](review/).

| Finding | Change on the redesign branch |
| --- | --- |
| The home page repeated Neqabty responsibilities across the hero, focus panel, biography and experience. The navigation had no Projects destination. | Lead with identity, three selected case studies and a dedicated project index. Keep dates and role descriptions together. |
| The repository CV and HTML described Neqabty and Ayed as ongoing. | Use the newer supplied CV at the existing PDF path. It lists both end dates as November 2026 and adds the DIGITISED contract from October 2026. The contract work is described as in progress. |
| The HTML referenced a missing 1200 × 630 Open Graph image. The favicon lived inside a data URL. | Supply a local share image and favicon, individual canonical URLs and metadata, structured data and a sitemap. |
| The README described a showcase, listed a different CV filename and referenced absent CSS/JS paths. | Document the real source files, regeneration command, review steps and deployment behavior. |
| Mobile navigation and the theme depended on JavaScript. Storage access was unguarded. External font CSS and entrance effects delayed the visible hero. | Render content and links as HTML. Enhance the menu and filters only when scripts are available, use a local font and respect system colors and reduced motion. |
| The workflow uploads the repository root on main pushes and manual dispatches. GitHub also reports legacy Pages publishing from main at /. Both workflows succeeded on the last main push. | Keep the checked-in HTML deployable directly under /Portfolio/. Preserve the workflow and Pages settings. No deployment is needed to review the branch. |

## Evidence decisions

- The supplied CV supports seven or more AI systems at Neqabty, five syndicates using the Arabic document search deployment, two Ayed programs, dates, education, awards and the named training credentials. No public credential IDs were supplied. The new PDF retains the established download filename.
- The sales prototype has a committed ten-scenario offline test log. The proposed 781 tests and 97% coverage could not be tied to that revision. CRM screenshots contain contact or deal information. Use the scenario log and an original diagram.
- The public retrieval repository evaluates general question-answer passages. The supplied CV describes a legal-awareness proof of concept and a separate Arabic document deployment. Evidence for 298 Egyptian labor-law articles and a distinct public case study is outstanding.
- No matching public source for the CV and cover-letter agent was found. A source-cleared walkthrough, repository or redacted project brief would support a future entry.
- Omit precise voice latency until measurement boundaries and a shareable benchmark are available. Professional cases use high-level architecture and the supplied CV. No client voice recordings, identities or documents are published.
- BOKRANA publicly names Mohamed as instructor. The case describes the learner journey. Ownership, student counts, payment volume, community integrations and implementation stack need separate evidence.
- The original PNGs displayed in chat were unavailable as workspace files. Use the credited professional BOKRANA instructor portrait. Its orange background informed the terracotta accent. [Instructor profile](https://bokrana.lovable.app/en/about)
- Additional public work reviewed included a separate AI media-buying prototype. The six selected case studies prioritize distinct responsibilities and evidence. See the source URLs and evidence notes in [projects.json](../content/projects.json).
