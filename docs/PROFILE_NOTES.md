# HUMAN // LOKESH — modular profile maintenance

This is the existing public profile repository for [Lokesh-1921](https://github.com/Lokesh-1921).
The root README is the portfolio. No separate website, Pages configuration, or application deployment is needed.

## Content and provenance

content/profile.json is the source for identity, confirmed contact destinations, section order, project
descriptions, and audited source revisions. Lokesh supplied his Computer Science/AI & ML background,
Python preference, learning interests, photography/gaming interests, and LinkedIn URL.
Institution identification is absent from current source and graphics.

The primary identity is HUMAN // LOKESH: aspiring AI engineer, Python, machine learning, and generative AI.
Computer vision is deliberately secondary: the fourth featured project and a side exploration in the lab.
No employment, expertise level, award, production status, live demo, or performance result is invented.

All four featured public source revisions were rechecked on 13 October 2026 and remain unchanged:
the healthcare CRM has implemented routing/retrieval and documented integration gaps; the trip planner
uses synthetic data and simulated selections; HealthHACK implements event interfaces and accessibility;
StereoVision supplies geometry, optical-flow tools, evaluation code, and tests. Featured application
test suites were not rerun as part of this visual redesign.

## Modular architecture

- content/profile.json: human-editable, verified content.
- scripts/profile_design/shared.py: palettes, local logos, geometry, motion, and static variants.
- scripts/profile_design/hero.py: orbit illustration and opening/closing composition.
- scripts/profile_design/panels.py: role, six section headers, technical systems, learning lab, and connection buttons.
- scripts/profile_design/projects.py: uniform source-linked project cards and conceptual diagrams.
- scripts/profile_design/dashboard.py: actual metrics, honest language shares, and weekly activity.
- scripts/build_brand.py: deterministic SVG assembly.
- scripts/build_readme.py: deterministic Markdown/HTML composition.
- scripts/update_activity.py: public-data collection and atomic rendering.
- scripts/finalize_snake.py: accessible labels and motion preference guard for the maintained action output.
- scripts/validate_profile.py: references, XML safety, content consistency, positioning, and metric safeguards.

The old generated directories were replaced only after their content, metadata, and initial snake assets
were preserved in the new modules. Unrelated projects and account settings were not modified.

## Motion and rendering

Only geometry animates. The role has exactly one immutable heading and a fixed supporting line.
Focus outlines pulse independently of their labels. Hero rings orbit, particles travel, and signal dashes flow.
Section headers, technical-system accents, project schematics, learning panels, and the closing signature move
at deliberately slow rates. Metric values and chart bars never animate or imply live measurements.

The original ghosting came from interpolating the first title's opacity back to one while another title
was visible. That multi-title implementation stays removed. New role typography, opacity, and bounds are
sampled across 258 frames in wide/compact layouts.

Each animated module has explicit static variants. Reduced-motion picture sources select those images and
the static contribution calendar. Embedded SVG media queries alone were not reliable in earlier testing;
the explicit files are the main fallback. Important information is also present in ordinary Markdown and alt text.

Compact variants are selected at viewport widths up to 900 px to accommodate GitHub's narrow profile column.
The picture, heading, paragraph, link, and details tags are ordinary GitHub-compatible HTML. No README CSS,
script, embedded HTML in SVGs, remote font, image widget, or simulated interaction is required.

## Honest data and secure automation

The existing daily refresh remains at **09:47 IST** (04:17 UTC), with manual and relevant source-change triggers.
The public-page collector paginates repository listings and requires calendar counts to match GitHub's
displayed annual total. Changed markup and partial data fail closed, retaining the last verified images.

The snapshot stores language/fork/profile flags and actual daily counts. Unneeded repository identifiers
are excluded. Primary language shares count non-fork project repositories, excluding the profile; they
are not byte shares, commit shares, or measures of mastery. Empty weeks produce no positive activity bars.
No rank, streak estimate, trophy, visitor count, or achievement widget is used.

The generation job has contents: read and no persisted checkout credential. The separate publishing job
has contents: write and stages only assets/generated/. All actions retain their verified full commit pins,
Node 24 runtime versions, and Ubuntu 24.04 runners. The built-in token is sufficient; no PAT or new secret is needed.
Refresh failures emit warnings. Validated initial assets are committed, preventing first-run broken paths.
Generated changes cannot recursively trigger the refresh workflow.

The read-only validation workflow rebuilds the brand and README and checks for drift before validation/tests.
Keeping the existing two workflows avoids redundant schedules, repeated contribution fetching, and extra publishing jobs.

## Local maintenance

~~~sh
python3 scripts/build_brand.py
python3 scripts/build_readme.py
python3 scripts/update_activity.py
python3 scripts/validate_profile.py
python3 -m unittest discover -s tests -v
~~~

To preserve the existing verified snapshot while regenerating its new design:

~~~sh
python3 scripts/update_activity.py --snapshot assets/generated/activity.json
~~~

The generators use the Python standard library. Chromium, Playwright, Markdown-it, and actionlint were
used only for authoring/QA and are not dependencies of the rendered profile or automated generation.

## Review and publication

This modular revision is prepared for review and is not published yet. The previous hosted validation
and refresh runs succeeded, proving the existing permissions/token arrangement. New directory paths and
the regenerated README still require native GitHub inspection and a hosted run after publication.

No new account setting or secret setup is required. Check GitHub's picture selection, six image headings,
linked project modules, and both workflows after publishing. Extended repository inactivity may pause
scheduled workflows; the manual trigger remains available.

Public repository destinations were rechecked. LinkedIn is the URL supplied by Lokesh; live response checks
are blocked by this cloud network policy. Unverified demo links are omitted.
