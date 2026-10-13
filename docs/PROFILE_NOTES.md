# Profile maintenance and provenance

This is the public profile repository for [Lokesh-1921](https://github.com/Lokesh-1921).
The profile README is the root `README.md` on `main`. No website hosting or GitHub Pages is needed.

## Content verification

The public profile and all ten public repository listings were inspected on 13 October 2026.
The original profile was GitHub's starter README and contained no Actions workflows.
Education, career goals, Python as the primary language, photography, and gaming were supplied by Lokesh.
Lokesh supplied the LinkedIn URL; its account-view query parameter was removed.

Selected projects were checked against source, not just repository names or README claims:

| Repository | Audited revision | Evidence |
| --- | --- | --- |
| `CV-Project-1` | `5736f74a71eefe1b966ddcf0fc01a4688e3e7d93` | `src/features/`, `src/stereo/`, `src/motion/`, `src/evaluation/`, `tests/`, `requirements.txt` |
| `DigiLocker-For-Hospitals` | `e890d6fab9b7665601ab517e66793e4f85428d3e` | `backend/graph.py`, `backend/rag/`, `backend/models.py`, frontend source and manifests |
| `trip-planner-ai` | `422bff93e4f96897bc4f62fa59f076bd132fdc57` | `src/lib/planner.ts`, `trip.server.ts`, `trip.functions.ts`, trip components, tests, manifest |
| `HealthHACK` | `36dd7ab0bd56ce954fbd15b3b717de47fae61b6c` | Repository tree/README plus raw `src/App.tsx`, `package.json`, and accessibility/motion source |

Additional source snapshots inspected: `NoviCord`, `AMDSlinshotHuman`, and
`AirlinesManagementSystem-24BAI10455`. `Don-t-Press-it` and `oss-audit-24BAI10455`
were inspected through public repository pages. Java is supported by the airline project's Swing source.

The CRM identifies itself as **AI-First CRM HCP**, despite its repository name.
Its README documents integration limitations; the profile describes a development application.
The trip planner uses synthetic reference records and simulated selections. It is presented as a prototype,
not a booking service. Deep learning is a learning direction, rather than a verified implemented stack.
The NoviCord README's proposed blockchain infrastructure was not used as evidence of implemented skills.

No project benchmark values, awards, employment, certifications, or ranks have been inferred.
The source audit did not execute the featured applications or their test suites.

## Graphics and accessibility

- `scripts/build_brand.py` regenerates the original banners, animated introduction, stack panels,
  and social badges using the Python standard library. No font downloads are needed.
- The SVGs contain no JavaScript, external images, or `foreignObject`.
- Desktop/mobile and light/dark hero, introduction, stack, and dashboard variants use GitHub-supported
  `<picture>` sources. Essential information also exists as ordinary Markdown.
- Project entries use native Markdown blockquote cards so their text wraps on mobile.
- The introduction cycles over 20 seconds; CSS respects `prefers-reduced-motion`.
  Its first phrase is the static fallback. Snake animations have a reduced-motion rule and an
  explicit expandable static calendar in the README.
- Technology logos are vendored from **Devicon v2.16.0**. Its license is retained in
  `assets/icons/LICENSE`. LangGraph/FAISS letter marks are original labels, not official logos.
- The four project schematics are decorative original graphics, not project screenshots.

## Public metrics

`scripts/update_activity.py` reads public GitHub repository pages and the public contribution calendar.
It requires no PAT, GraphQL credentials, paid service, or stats-widget host.
It paginates repositories and checks contribution tooltip counts against GitHub's displayed annual total.
If the markup changes or a request fails, it raises an error instead of inventing or publishing partial totals.

The committed `assets/live/activity.json` contains only public repository names/languages and calendar counts,
with a refresh timestamp. The dashboard shows public repositories, last-year contributions, active calendar days,
and primary-language shares across public non-fork repositories with a detected language.
Language shares are repository counts, not byte counts, commit counts, or measures of proficiency.
The date appears in the dashboard. Private repository details are never collected.

Streak/rank/trophy/visitor widgets are intentionally omitted: they add service dependencies and do not
establish engineering experience. Pull-request totals were not independently verified and are not shown.

## Automation

`refresh-profile.yml` runs daily at **04:17 UTC**, can be triggered manually, and runs after changes to
its generation scripts or workflow on `main`. Committing generated assets cannot trigger another refresh.
Actions are pinned to verified full commit SHAs. Platane/snk's SVG-only action is pinned to its v3.5.0 source.

The generation job has `contents: read`, disables persisted checkout credentials, and uses only
`${{ github.token }}` for the snake's public contribution lookup. The publishing job has `contents: write`
and commits only `assets/live/` to `main`, without force pushing. No PAT or additional secret is needed.
Failed refresh steps retain the last successful images and emit explicit warnings in the run summary.
Asset validation must pass before anything is uploaded or committed.

The initial snakes were generated locally from the same verified calendar snapshot with the pinned
Platane/snk action. Its GraphQL fetch was replaced only in the local test by an offline adapter containing
the real public calendar; this validates the official action's runtime and workflow inputs, not live API authentication.
Future refreshes use the official action with GitHub's built-in token. Both files already exist in
the repository, so there is no missing output branch or first-run image dependency.

`validate-profile.yml` checks local image references, SVG structure/safety, accessibility labels,
metrics consistency, and the activity parser's failure safeguards on pushes and pull requests.

Local checks:

```sh
python3 scripts/validate_profile.py
python3 -m unittest discover -s tests -v
python3 scripts/build_brand.py
python3 scripts/update_activity.py
```

The final command accesses public GitHub pages. To reproduce images from the committed snapshot offline:

```sh
python3 scripts/update_activity.py --snapshot assets/live/activity.json --output /tmp/profile-activity-check
```

Use the existing isolated checkout for editing; a Git worktree is unnecessary.

## Publishing and remaining live checks

The changes are prepared locally for review. **Pushing is a separate approval step.**
After approval, push the prepared commit to the profile repository's `main` branch, then inspect the
GitHub-rendered profile and the two Actions runs. The initial push includes the workflow/scripts and
therefore triggers the first refresh automatically. `workflow_dispatch` is available for retries.

GitHub Actions must be enabled. Repository or organization policy must permit the pinned actions
and the refresh publisher's built-in token to write `main`. If branch protection blocks direct bot commits,
adapt the publication job to the repository's review policy rather than bypassing protection.
GitHub may pause schedules in public repositories after 60 days of inactivity; re-enable the schedule if needed.

Before pushing, the updated README cannot be validated on the live GitHub profile, and the workflows
cannot be run in this repository on GitHub. Local browser rendering approximates GitHub's Markdown styling
and verifies the supplied themes and viewport variants; it does not replace that post-push check.

This cloud environment blocks `api.github.com`, LinkedIn, and the two Vercel demo domains inspected.
Public GitHub pages, source files, and the local public-data generator were reachable and tested.
The LinkedIn URL is user-confirmed but its destination could not be live-tested here.
HealthHACK and NoviCord list Vercel homepages; no demo link was placed in the profile without a successful
live check. Published raw-image URLs also require the prepared commit to be pushed first.
