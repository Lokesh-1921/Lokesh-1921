# HUMAN // LOKESH assets

The profile is assembled from original, repository-hosted SVG modules. The viewer needs no framework,
JavaScript, font service, package installation, or third-party statistics host.

| Folder | Purpose |
| --- | --- |
| hero/ | Layered orbit identity and wide/compact variants |
| modules/ | Fixed role card, six animated section headers, connection buttons, learning lab, and closing signature |
| dashboards/ | Categorized technical-system panel |
| projects/ | Four verified project cards with original conceptual schematics |
| generated/ | Real activity snapshot, statistics, static calendars, and contribution snakes |
| icons/ | Retained Devicon source logos and license |

scripts/build_brand.py assembles the design from scripts/profile_design/. scripts/build_readme.py composes
the README from content/profile.json. Shared colors, typography, motion, geometry, and icon embedding live
in profile_design/shared.py. Never edit generated SVGs or README text independently of their source.

Animated modules have explicit animation-free variants for both themes and sizes. Native README picture
sources select them under reduced motion. Normal motion uses stationary text with slow geometry animation.

Vendored logos come from [Devicon v2.16.0](https://github.com/devicons/devicon/tree/v2.16.0/icons).
The license is retained in icons/LICENSE; marks belong to their owners. Toolkit labels describe tools used
in public code, not proficiency levels. Project diagrams are concepts, not screenshots or measured telemetry.

The snakes use [Platane/snk](https://github.com/Platane/snk) pinned to
d8f6715049803e982ee5ff501b6b9b7d5deeb09b (v3.5.0), retaining its embedded attribution.
The initial animations were moved from the previous successful hosted refresh without inventing activity.
