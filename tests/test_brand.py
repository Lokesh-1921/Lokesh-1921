"""Regression checks for the reported text overlap and honest visual data."""
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_brand import PALETTES, role, svg
from update_activity import project_languages, dashboard

NS='{http://www.w3.org/2000/svg}'


class BrandTests(unittest.TestCase):
    def test_explicit_static_assets_contain_no_animation_instructions(self):
        files=list((ROOT/'assets').rglob('*static-*.svg'))
        self.assertEqual(len(files),12)
        for file in files:
            with self.subTest(asset=file.name):
                body=file.read_text()
                self.assertNotIn('@keyframes',body)
                self.assertNotIn('animation:',body)
                self.assertNotIn('animation-delay:',body)

    def test_role_has_one_immutable_heading_in_every_variant(self):
        for theme,palette in PALETTES.items():
            for mobile in (False,True):
                with self.subTest(theme=theme,mobile=mobile):
                    w,h,body=role(palette,mobile)
                    root=ET.fromstring(svg(w,h,body,'role','role'))
                    headings=[n for n in root.iter(NS+'text') if n.get('data-role-title')=='true']
                    self.assertEqual(len(headings),1)
                    self.assertEqual(headings[0].text,'ASPIRING AI ENGINEER')
                    parents={child:parent for parent in root.iter() for child in parent}
                    for label in root.iter(NS+'text'):
                        node=label
                        while node is not None:
                            self.assertNotIn('animation',node.get('style',''))
                            self.assertFalse(node.get('class'))
                            node=parents.get(node)
                    self.assertIn('prefers-reduced-motion:reduce',body)

    def test_profile_tooling_and_forks_do_not_skew_project_languages(self):
        data={'owner':'Lokesh-1921','repositories':[
            {'name':'Lokesh-1921','language':'Python','fork':False},
            {'name':'actual-vision','language':'Python','fork':False},
            {'name':'forked-demo','language':'TypeScript','fork':True},
            {'name':'docs-only','language':None,'fork':False}]}
        self.assertEqual(dict(project_languages(data)),{'Python':1})
        compact={'owner':'Lokesh-1921','repositories':[
            {'language':'Python','fork':False,'is_profile':True},
            {'language':'Python','fork':False,'is_profile':False},
            {'language':'TypeScript','fork':True,'is_profile':False}]}
        self.assertEqual(dict(project_languages(compact)),{'Python':1})

    def test_empty_activity_stays_zero_and_never_draws_positive_bars(self):
        data={'owner':'Lokesh-1921','updated_at':'2026-10-13','repositories':[],
              'days':[{'x':i,'count':0} for i in range(53)]}
        body=dashboard(data,'dark')
        self.assertIn('contributions / last year: 0',body)
        self.assertNotIn('Calendar week ',body)


if __name__=='__main__':
    unittest.main()
