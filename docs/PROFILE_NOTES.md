# NEURAL // LOKESH — maintenance and provenance

This is the existing public profile repository for [Lokesh-1921](https://github.com/Lokesh-1921).
The root README is the portfolio. No website hosting, JavaScript application, or Pages setup is required.

## Identity and verified content

The current tree uses professional, skill-focused branding only. Academic institution identification
is excluded from the README, graphics, descriptions, and generation code.

Lokesh supplied his Computer Science/AI & ML background, career interests, Python preference,
photography/gaming interests, and LinkedIn address. The public GitHub account and all ten public
repository listings were checked again on 13 October 2026.

| Featured repository | Verified source revision | Implementation evidence |
| --- | --- | --- |
| CV-Project-1 | 5736f74a71eefe1b966ddcf0fc01a4688e3e7d93 | Feature matching, stereo geometry, optical flow, reconstruction, metrics, CLI, and tests |
| DigiLocker-For-Hospitals | e890d6fab9b7665601ab517e66793e4f85428d3e | FastAPI, active LangGraph workflow, FAISS/BM25 retrieval, PostgreSQL models, React frontend |
| trip-planner-ai | 422bff93e4f96897bc4f62fa59f076bd132fdc57 | Deterministic planner, synthetic catalog, assistant integration, typed interfaces, tests |
| HealthHACK | 36dd7ab0bd56ce954fbd15b3b717de47fae61b6c | React/TypeScript app, typed event content, gallery keyboard controls, reduced-motion hook |

These revisions are unchanged from the earlier source audit. Other public listings were reviewed;
the airline project's Java Swing source supports Java in the toolkit. Dependency declarations alone
were not used to claim proficiency or mastery. Featured application test suites were not executed
as part of this visual redesign.

The CRM's source name is AI-First CRM HCP, despite its repository name. Its runtime/integration
limitations remain acknowledged. The travel project uses synthetic data and simulated selections.
The Intelligence Lab describes learning directions, not finished deep-learning products or professional roles.
No awards, ranks, performance improvements, employment, private project data, or benchmark results are inferred.

## Design and asset generation

The shared palette, typography, layout, diagrams, and motion live in scripts/build_brand.py.
Hero, role, toolkit, four project cards, lab, footer, and social badges are generated with the Python standard library.
Each major graphic has wide/compact and dark/light versions. Compact sources are selected up to 900 px,
including tablets where GitHub's sidebar can narrow the README column. All displayed images are local.
Brand assets live in assets/brand and project graphics in assets/project-cards. The new brand paths also
avoid reusing cached images from the previous hero and role implementation.

The constellation and project schematics are original explanatory artwork, not screenshots,
deployed dashboards, or representations of measured model internals. Logos are vendored from Devicon v2.16.0;
its license is retained in assets/icons/LICENSE. LangGraph and FAISS use original schematic marks with text labels.
The external-link arrows are vector paths, avoiding missing font glyphs.

## Role overlap diagnosis and fix

The old first-title keyframes set opacity to zero at 24% and back to one at 100%.
The browser interpolated across that interval while later titles were visible. At seven seconds,
the first title had opacity 0.174763 while the second had opacity 1: the reported ghosting reproduced.

The replacement has exactly one role heading: ASPIRING AI ENGINEER. Its text never animates.
A separate supporting line stays fixed beneath it. Decorative paths carry the motion.
The social buttons occupy their own paragraph, with consistent widths and spacing.
Regression checks reject animated role text or additional role headings.

The role was sampled at 129 points over 32 seconds in both desktop and mobile versions.
Its text, bounding box, and opacity stayed identical throughout. Geometry was also checked for all generated
graphics, including both color themes.

## Motion, static fallbacks, and accessibility

SVG animation uses only lightweight path signals and slow node accents; no script runs in the profile.
Embedded SVG media queries did not reliably inherit reduced-motion preferences in the test browser.
The README therefore selects explicit, animation-free hero/role/footer assets using native picture sources.
It also substitutes the static calendar for the snake when reduced motion is requested.
This fallback was verified in the browser. The SVG CSS rule remains as an additional direct-view safeguard.

The single role heading is readable even if SVG animation support fails completely.
Essential descriptions, project links, and learning areas are repeated in ordinary Markdown.
Every displayed image has alt text; generated SVGs have accessible titles and descriptions.
Project cards link to their actual source repositories. SVG text bounds and spacing are measured in Chromium,
rather than inferred from character counts.

## Metrics and refresh behavior

scripts/update_activity.py uses public GitHub pages, with no token or stats-service dependency.
It paginates repository listings and checks calendar tooltip counts against GitHub's displayed annual total.
Changed markup, incomplete data, and failed requests fail closed instead of publishing partial metrics.

assets/live/activity.json holds language/fork/profile flags and actual calendar counts, with a timestamp.
Unneeded repository slugs are omitted, including registration-style identifiers in existing project names.
The dashboard presents public repository count, last-year contributions, active calendar days, primary project
languages, and weekly calendar contribution counts. Language shares exclude forks and this profile repository;
they count repositories by primary language rather than bytes, commits, or proficiency. Zero weeks draw no
positive bars. No streak, trophy, visitor, rank, or achievement widget is used.

The daily refresh remains at 09:47 IST (04:17 UTC), with manual execution and script/workflow-change triggers.
Generation has contents: read; the separate publishing job has contents: write and commits only assets/live/.
No PAT is required. The snake uses the maintained, pinned Platane/snk v3.5.0 SVG-only action with the built-in token.
Generation failures retain the last good files and emit warnings. Validation must pass before publication.
Generated commits cannot recursively trigger the refresh workflow.

The Actions were updated to verified Node 24 versions of checkout, upload-artifact, and download-artifact,
using full commit pins and Ubuntu 24.04. This avoids the deprecated-runtime and moving-runner notices observed
in the earlier hosted runs.

The new snake palette and inputs were exercised locally with the pinned official action and an offline
GraphQL adapter populated from the actual collected calendar. This does not claim live API authentication
or a hosted run of the revised workflow. Initial images are already committed, avoiding first-run broken paths.

## Local maintenance

Use the existing isolated checkout; do not create a Git worktree unless explicitly requested.

~~~sh
python3 scripts/build_brand.py
python3 scripts/update_activity.py
python3 scripts/validate_profile.py
python3 -m unittest discover -s tests -v
~~~

The activity command accesses public GitHub pages. For deterministic offline rendering:

~~~sh
python3 scripts/update_activity.py --snapshot assets/live/activity.json --output /tmp/profile-data-check
~~~

The profile viewer requires no Python, Node, framework, font service, or package installation.

## Review and hosted checks

This redesign is prepared as a clean review commit. The previous profile's hosted workflows succeeded;
the revised README and updated workflow pins require post-publication inspection on GitHub.
The visual previews use Chromium and GitHub-like Markdown styling, rather than claiming a hosted render
of an unpublished revision.

The existing automatic publishing job has already demonstrated write access with the built-in token.
No new secret or account-setting change is required. Inspect both Actions runs and the profile after publication,
especially picture source selection, linked project cards, and the revised SVGs. Repository policy still applies.
GitHub may pause schedules after extended inactivity; the manual trigger remains available.

All six unique GitHub README destinations returned HTTP 200. The LinkedIn address is confirmed by Lokesh;
the cloud egress policy prevents checking its response. The verified project homepages on Vercel could not
be reached here, so unverified demo destinations are omitted. No placeholder is presented as a real contact.
