# Authenticated GitHub contribution totals

This profile intentionally displays the **public** GitHub contribution calendar unless the owner configures an authenticated source. A signed-in owner can see more contributions than anonymous visitors. The dashboard previously displayed the anonymous total, so the image can legitimately differ from GitHub's signed-in graph.

## Enable owner-visible calendar totals

1. Sign in as \`Lokesh-1921\` and open https://github.com/settings/tokens .
2. Create a personal access token **(classic)** with the **read:user** scope only and a reasonable expiration date. Do not select \`repo\`, \`workflow\`, or write permissions.
3. Open https://github.com/Lokesh-1921/Lokesh-1921/settings/secrets/actions and choose **New repository secret**.
4. Set the name to \`PROFILE_STATS_TOKEN\` and paste the token in the **secret value** field. Do not put the token in source code, an issue, a commit, or this README.
5. Go to https://github.com/Lokesh-1921/Lokesh-1921/actions/workflows/refresh-profile.yml and run **Run workflow** on the \`main\` branch.
6. Confirm the **Refresh verified contribution calendar** and **publish-assets** steps succeeded. The dashboard should say **ACCOUNT ACTIVITY / VERIFIED SNAPSHOT**, include a UTC refresh time, and show the authenticated contribution total reported by GitHub's API.

The code queries GitHub's authenticated GraphQL \`contributionsCollection.contributionCalendar\` field and verifies that the token is for this profile's owner. The persisted snapshot contains **only daily aggregate counts and levels**, never private repository titles, commits, issue content, private URLs, or credentials. The token only reaches the first-party GitHub API inside the data-fetch step. The contribution snake is powered by its separate action and can still reflect publicly available data rather than owner-only counts.

If no token is configured, the dashboard will continue showing **PUBLIC GITHUB / DAILY SNAPSHOT**. A missing token never produces a guessed private count. Invalid or expired credentials fail the refresh, and the last verified images are preserved with an error shown in Actions.

## Refresh behavior and privacy

The workflow requests an update hourly (at :17 UTC); GitHub may delay scheduled workflow execution. A manual workflow run is also available. GitHub may cache rendered SVG files for a short time. The image displays its last successful **UTC** refresh time rather than claiming to be real time.

A read:user classic token grants account-profile reading access and must be protected as a credential. Revoke it immediately if exposed, and replace it in the repository secret before expiry. An authenticated count may still differ from a browser graph because GitHub's API and site may use different visibility, cache, or calendar-time windows; verify the API result instead of manually entering a target number.
