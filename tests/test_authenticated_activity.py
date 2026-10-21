"""Check authorized calendar parsing without making network calls."""
from datetime import date, timedelta
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from authenticated_activity import parse_authenticated_calendar


def sample_calendar():
    start = date(2025, 10, 19)
    weeks = []
    for i in range(53):
        entries = []
        for j in range(7):
            d = start + timedelta(days=7 * i + j)
            count = 77 if (i, j) == (1, 0) else 16 if (i, j) == (2, 0) else 0
            entries.append(dict(date=d.isoformat(), contributionCount=count,
                                weekday=j, contributionLevel="FIRST_QUARTILE" if count else "NONE"))
        weeks.append(dict(contributionDays=entries))
    return dict(data=dict(viewer=dict(login="Lokesh-1921"),
        user=dict(contributionsCollection=dict(contributionCalendar=dict(
            totalContributions=93, weeks=weeks)))))


class AuthenticatedActivityTests(unittest.TestCase):
    def test_count_and_metadata(self):
        days = parse_authenticated_calendar(sample_calendar(), "Lokesh-1921")
        self.assertEqual(sum(d["count"] for d in days), 93)
        self.assertEqual(len(days), 371)
        self.assertEqual(set(days[0]), {"date", "count", "level", "x", "y"})

    def test_mismatched_identity_fails(self):
        payload = sample_calendar()
        payload["data"]["viewer"]["login"] = "other"
        with self.assertRaises(ValueError):
            parse_authenticated_calendar(payload, "Lokesh-1921")

    def test_mismatched_total_fails(self):
        payload = sample_calendar()
        payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"] = 100
        with self.assertRaises(ValueError):
            parse_authenticated_calendar(payload, "Lokesh-1921")

    def test_bad_weekday_fails(self):
        payload = sample_calendar()
        payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"][0]["contributionDays"][0]["weekday"] = 5
        with self.assertRaises(ValueError):
            parse_authenticated_calendar(payload, "Lokesh-1921")

    def test_graphql_errors_fail(self):
        with self.assertRaises(ValueError):
            parse_authenticated_calendar({"errors": [{"message": "Denied"}]}, "Lokesh-1921")


if __name__ == "__main__":
    unittest.main()
