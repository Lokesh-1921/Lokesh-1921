# HUMAN // LOKESH — modular redesign validation

Checked on 13 October 2026. This record describes the review revision before publication.

| Check | Actual result |
| --- | --- |
| SVG safety | 148 SVGs parsed; no scripting, external image dependencies, embedded HTML, or duplicate IDs |
| Asset references | All 158 README image/source references resolve locally; all images have meaningful alt text |
| Source consistency | README exactly matches scripts/build_readme.py and content/profile.json |
| Primary positioning | All eight hero/role variants preserve HUMAN, aspiring AI engineer, Python, AI/ML/GenAI; no primary computer vision identity |
| Institution identification | Zero matches in 169 current text/source files, including descriptions, generators, JSON content, and documentation |
| Verified projects | All four GitHub source revisions rechecked; identical to the code audit. AI/retrieval and application projects lead; vision is fourth and secondary |
| Real metrics | Preserves the previous successful public snapshot: ten repositories, 69 last-year contributions, timestamp 2026-10-13T17:42:26+00:00 |
| Honest language chart | Profile and forks excluded; nine project repositories counted by primary language, not code volume or proficiency |
| Text geometry | 136 display/generated SVGs checked in Chromium at natural coordinates; zero clipped or overlapping text bounding boxes |
| Responsive rendering | 375, 768, and 1280 px in both themes; 20 image assets load in every layout; no page overflow |
| Role and social layout | Two equal-height social buttons share one aligned row and remain below the independently spaced role module |
| Heading composition | Six accessible image headings retain their section order and wide/compact layouts |
| Mobile code panel | No horizontal scrolling required for the introductory Python block |
| Project links | Four graphical modules retain their correct source anchors and order |
| Motion inside images | Frame changes observed in 17 embedded SVG images: hero, role, six headers, toolkit, four projects, dashboard, snake, lab, closing |
| Role stability | All role text sampled at 129 times per size over 32 seconds, 258 total; text, bounds, and opacity remain constant |
| Reduced motion | 64 explicit static SVG variants; the entire reduced-motion profile remains pixel-identical between screenshot frames; snake replaced by static calendar |
| Regression safeguards | Nine unit tests pass: parsing, fail-closed data refresh, fork/profile exclusion, honest zero activity, singleton role, complete static fallbacks |
| Workflow syntax | Both updated workflows pass actionlint 1.7.12; downloaded tool verified against its official artifact checksum |
| Runtime dependencies | Generation uses only the Python standard library; profile rendering has no runtime package dependency |
| Footprint | All assets total approximately 854 KiB; normal desktop fallback images total 158 KiB, including the collapsed calendar |
| Repository scope | Only the existing profile repository is changed; unrelated projects/settings untouched |

The first browser pass detected a five-pixel name/tagline bounding-box intersection in the compact hero.
Spacing was corrected, the constellation was repositioned, and the full visual checks passed afterward.
Hero and role now sit in separate paragraphs so GitHub's native margins separate the panels and connection row.

The generators are deterministic. The validation workflow rebuilds the visual modules and README, rejects
tracked drift or missing committed outputs, then validates XML, references, real-data labels, and tests.
Graphics are self-contained, use standard system-font fallbacks, and animate geometry only.
Project sketches are explicitly conceptual; no application screenshots, deployments, benchmarks, or licensing
claims are fabricated.

## Verification limits and publication

This modular revision is prepared as a local review commit, not a published change.
Browser previews approximate GitHub's Markdown styling. Native GitHub sanitization, six picture headings,
media selection, card anchors, and the new generated-asset workflow paths need inspection after publication.

The previous hosted [validation run 38440802881](https://github.com/Lokesh-1921/Lokesh-1921/actions/runs/38440802881)
and [refresh run 38440800997](https://github.com/Lokesh-1921/Lokesh-1921/actions/runs/38440800997)
succeeded. The action pins and permissions remain the same; those runs do not prove the revised asset paths.

No PAT, secret, Pages setup, website deployment, or account-setting change is required.
LinkedIn remains the user-confirmed address; its HTTP response cannot be checked under this environment's
network policy. No unverified demo is linked. Featured application runtime tests were outside this visual task.

After review and publication, inspect the profile in both themes at narrow and wide widths and confirm
both workflows complete. The scheduled refresh remains at 09:47 IST, with a manual trigger available.
