"""Read the account owner's GitHub contribution calendar without publishing private details.

Uses only daily counts and levels. Never stores a token, repository name, or private URL.
"""
from datetime import date
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ENDPOINT = "https://api.github.com/graphql"
LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}
QUERY = """
query ProfileContributionCalendar($login: String!) {
  viewer { login }
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
            weekday
          }
        }
      }
    }
  }
}
"""


def parse_authenticated_calendar(payload, owner):
    """Validate every daily count, date, level and the API-provided total."""
    if payload.get("errors"):
        raise ValueError("GitHub GraphQL rejected the contribution query")
    result = payload.get("data")
    if not isinstance(result, dict):
        raise ValueError("No GitHub GraphQL data returned")
    viewer = result.get("viewer") or {}
    if viewer.get("login", "").lower() != owner.lower():
        raise ValueError("PROFILE_STATS_TOKEN must belong to the profile owner")
    user = result.get("user") or {}
    calendar = (user.get("contributionsCollection") or {}).get("contributionCalendar") or {}
    total = calendar.get("totalContributions")
    weeks = calendar.get("weeks")
    if type(total) is not int or total < 0 or not isinstance(weeks, list):
        raise ValueError("Incomplete authenticated contribution calendar")
    days = []
    seen = set()
    for x, week in enumerate(weeks):
        entries = week.get("contributionDays") if isinstance(week, dict) else None
        if not isinstance(entries, list):
            raise ValueError("Missing contribution week")
        for item in entries:
            if not isinstance(item, dict):
                raise ValueError("Invalid contribution day")
            raw_date = item.get("date")
            try:
                day = date.fromisoformat(raw_date)
            except (TypeError, ValueError):
                raise ValueError("Invalid contribution date") from None
            count = item.get("contributionCount")
            weekday = item.get("weekday")
            level = LEVELS.get(item.get("contributionLevel"))
            if (type(count) is not int or count < 0 or
                    type(weekday) is not int or weekday != (day.weekday() + 1) % 7 or
                    level is None or raw_date in seen):
                raise ValueError("Invalid or duplicate contribution-calendar entry")
            seen.add(raw_date)
            days.append({"date": raw_date, "count": count, "level": level, "x": x, "y": weekday})
    if not 350 <= len(days) <= 380:
        raise ValueError("Incomplete authenticated contribution calendar")
    if days != sorted(days, key=lambda item: item["date"]):
        raise ValueError("Contribution dates are out of order")
    if sum(item["count"] for item in days) != total:
        raise ValueError("Authenticated calendar total does not match daily counts")
    return days


def fetch_authenticated_calendar(owner, token):
    """Query as the account owner using a read:user personal access token."""
    if not token:
        raise ValueError("Missing PROFILE_STATS_TOKEN")
    body = json.dumps({"query": QUERY, "variables": {"login": owner}}).encode("utf-8")
    req = Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "profile-contribution-refresh",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=35) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise ValueError("Authenticated GitHub query failed (HTTP %s)" % exc.code) from None
    except URLError:
        raise ValueError("Authenticated GitHub query could not reach GitHub") from None
    except (ValueError, UnicodeError):
        raise ValueError("Authenticated GitHub returned an invalid response") from None
    return parse_authenticated_calendar(payload, owner)
