# Validation record

Validated locally on 13 October 2026, before publication.

| Check | Result |
| --- | --- |
| Public identity and profile repository | `Lokesh-1921/Lokesh-1921` is public; remote `main` remained at the original starter commit during preparation |
| Source audit | Ten repository listings inspected; four featured projects described using source evidence |
| Live statistics collection | GitHub public pages returned ten repositories, 65 annual contributions, and 17 active days; data stored with its timestamp |
| Offline dashboard repeatability | Rendering the committed snapshot reproduced the dashboard SVGs byte for byte |
| SVG validation | 42 files parsed; checks reject scripting, external image references, duplicate IDs, and unsupported embedded HTML |
| README images | All 38 references exist locally; displayed images have alt text |
| Markdown rendering | Parsed with Markdown-it; headings, tables, code, picture sources, and four separate project cards rendered in Chromium |
| Theme and layout | Desktop at 1440 px and mobile at 390 px checked in light/dark; ten images loaded in each case, correct variants selected, no horizontal page overflow |
| Animations | Introduction and snake changed between captured frames in Chromium; reduced-motion/static alternatives included |
| Workflow syntax | Both workflows passed actionlint 1.7.12; binary verified against its official release checksum |
| Action implementation | The pinned official snk Node action ran locally using workflow inputs and an offline GraphQL adapter populated from the real public calendar; both SVG outputs generated |
| Parser safeguards | Five unit tests passed, covering calendar total mismatch, incomplete data, repository pagination/forks, destination restrictions, and escaped labels |
| External README links | Six unique GitHub destinations returned HTTP 200; user-confirmed LinkedIn URL blocked by the cloud egress policy |
| Repository hygiene | `git diff --check` passed; only this profile repository was edited |

These checks do **not** establish live GitHub rendering, a successful hosted Actions run, API token authentication,
push permission, or featured-project application behavior. Those require the publishing step and/or their own runtime setup.
No publication or remote change was performed during preparation.

After approval and push, inspect the profile and both workflows. No extra secret is required.
If repository policy prevents the publisher from committing generated assets, follow that policy;
the committed initial images remain available.
