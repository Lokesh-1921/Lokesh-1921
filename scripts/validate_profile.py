"""Check profile asset references, SVG safety, accessibility, and real-data totals."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references=[]

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='img':
            assert a.get('alt','').strip(), 'Image has no meaningful alt text'
            self.references.append(a['src'])
        if tag=='source':
            self.references.append(a['srcset'])
        assert tag not in ('script','iframe','style'), f'Unsupported README tag: {tag}'
        assert not any(k.startswith('on') for k in a), 'Event handler in README'


def validate_svg(file):
    root=ET.fromstring(file.read_text())
    assert root.tag.endswith('}svg') and root.get('viewBox'), f'Invalid SVG: {file}'
    ids=set()
    for node in root.iter():
        tag=node.tag.split('}')[-1]
        assert tag not in ('script','foreignObject','image'), f'Non-self-contained SVG: {file}'
        if node.get('id'):
            assert node.get('id') not in ids, f'Duplicate SVG ID in {file}'
            ids.add(node.get('id'))
        for key,value in node.attrib.items():
            assert not key.lower().startswith('on'), f'SVG event handler: {file}'
            if key.endswith('href'):
                assert value.startswith('#'), f'External SVG reference: {file}'
    if file.parent.name!='icons':
        assert root.find('{http://www.w3.org/2000/svg}title') is not None, f'Missing SVG title: {file}'


def main():
    readme=(ROOT/'README.md').read_text()
    parser=Images();parser.feed(readme)
    for source in parser.references:
        assert not source.startswith(('http:','https:')), f'Unnecessary remote image dependency: {source}'
        file=(ROOT/source).resolve()
        assert file.is_relative_to(ROOT) and file.is_file(), f'Missing image: {source}'
    for destination in re.findall(r'\]\(([^)]+)\)',readme):
        assert destination.startswith('https://'), f'Invalid project/social destination: {destination}'
    files=list((ROOT/'assets').rglob('*.svg'))
    for file in files:
        validate_svg(file)
    data=json.loads((ROOT/'assets/live/activity.json').read_text())
    assert data['owner']=='Lokesh-1921'
    assert len(data['days'])>=350
    total=sum(d['count'] for d in data['days'])
    for theme in ('dark','light'):
        root=ET.parse(ROOT/'assets/live'/f'dashboard-{theme}.svg').getroot()
        desc=root.find('{http://www.w3.org/2000/svg}desc').text
        assert f'contributions / last year: {total}' in desc
        assert f'public repositories: {len(data["repositories"])}' in desc
    print(f'Validated {len(files)} SVGs, {len(parser.references)} README image references, alt text, local hosting, and dashboard totals.')


if __name__=='__main__':
    main()
