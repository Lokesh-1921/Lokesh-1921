"""Meaningful safeguards for public-data extraction and refresh failures."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from update_activity import Repositories, parse_calendar, fetch, dashboard


def calendar_markup(total=1, missing_tooltip=False):
    cells=[]
    for i in range(350):
        cells.append(f'<td data-date="2026-01-{i:03}" id="contribution-day-component-{i%7}-{i//7}" data-level="{1 if i==0 else 0}"></td>')
        if not missing_tooltip or i!=0:
            value='1 contribution' if i==0 else 'No contributions'
            cells.append(f'<tool-tip for="contribution-day-component-{i%7}-{i//7}">{value} on January 1st.</tool-tip>')
    return f'<h2>{total} contributions in the last year</h2>'+''.join(cells)


class ActivityTests(unittest.TestCase):
    def test_source_and_fork_repositories_and_pagination(self):
        p=Repositories('Lokesh-1921')
        p.feed('<li itemprop="owns" class="public source"><a itemprop="name codeRepository" href="/Lokesh-1921/vision">vision</a><span itemprop="programmingLanguage">Python</span></li><li itemprop="owns" class="public fork"><a itemprop="name codeRepository" href="/Lokesh-1921/fork">fork</a><span itemprop="programmingLanguage">Java</span></li><a class="next_page" href="/Lokesh-1921?tab=repositories&amp;page=2">Next</a>')
        self.assertEqual(len(p.items),2)
        self.assertEqual(p.items[0]['language'],'Python')
        self.assertTrue(p.items[1]['fork'])
        self.assertEqual(p.next_page,'https://github.com/Lokesh-1921?tab=repositories&page=2')

    def test_calendar_counts_match_displayed_total(self):
        days=parse_calendar(calendar_markup())
        self.assertEqual(sum(d['count'] for d in days),1)
        self.assertEqual(len(days),350)

    def test_changed_or_partial_calendar_cannot_replace_snapshot(self):
        for markup in (calendar_markup(total=9),calendar_markup(missing_tooltip=True),'<html>Rate limited</html>'):
            with self.subTest(markup=markup[:60]), self.assertRaises(ValueError):
                parse_calendar(markup)

    def test_unexpected_network_destination_is_rejected_before_request(self):
        with self.assertRaises(ValueError):
            fetch('https://example.com/untrusted-pagination')

    def test_forks_excluded_from_language_shares_and_labels_escape_content(self):
        data={'owner':'Lokesh-1921','updated_at':'2026-01-01','days':[{'count':1}], 'repositories':[{'name':'a','language':'Python','fork':False},{'name':'b','language':'Java','fork':True},{'name':'c','language':None,'fork':False}]}
        image=dashboard(data,'dark')
        self.assertIn('Python · 1/1',image)
        self.assertNotIn('Java ·',image)
        data['repositories'][0]['language']='<script>'
        self.assertIn('&lt;script&gt;',dashboard(data,'light'))


if __name__=='__main__':
    unittest.main()
