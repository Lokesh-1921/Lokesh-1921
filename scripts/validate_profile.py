"""Check profile asset references, SVG safety, accessibility, and real-data totals."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
INSTITUTION_PATTERN=re.compile(r'\bvi[t]\b|\bbho[p]al\b|\buniversit[y]\b|\bcolleg[e]\b',re.I)


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
    parents={child:parent for parent in root.iter() for child in parent}
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
        if tag=='text':
            ancestor=node
            while ancestor is not None:
                assert not ancestor.get('class') and 'animation' not in ancestor.get('style',''), f'Text must remain stationary: {file}'
                ancestor=parents.get(ancestor)
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
    checked=0
    for file in ROOT.rglob('*'):
        if not file.is_file() or any(part in ('.git','__pycache__') for part in file.parts):
            continue
        if file.suffix.lower() in ('.svg','.md','.py','.json','.yml','.yaml'):
            assert not INSTITUTION_PATTERN.search(file.read_text()), f'Institution branding remains in {file.relative_to(ROOT)}'
            checked+=1
    for file in (ROOT/'assets/modules').glob('role-strip*.svg'):
        root=ET.parse(file).getroot()
        labels=root.findall('.//{http://www.w3.org/2000/svg}text')
        roles=[node for node in labels if node.get('data-role-title')=='true']
        assert len(roles)==1, f'Role must have exactly one heading: {file}'
        for label in labels:
            assert 'animation' not in label.get('style','') and not label.get('class'), f'Role text must remain immutable: {file}'
    from build_readme import render
    assert readme==render(), 'README differs from its verified modular content source'
    front=readme.split('<h2>')[0]
    assert 'HUMAN // LOKESH' in front
    assert not re.search(r'computer[ -]vision',front,re.I), 'Secondary exploration leaked into front identity'
    for file in (ROOT/'assets/hero').glob('hero*.svg'):
        body=file.read_text()
        assert 'HUMAN // LOKESH' in body and 'GENERATIVE AI' in body
        assert not re.search(r'computer[ -]vision',body,re.I), f'Incorrect primary positioning: {file}'
    for file in (ROOT/'assets').rglob('*static-*.svg'):
        body=file.read_text()
        assert '@keyframes' not in body and 'animation:' not in body, f'Static fallback moves: {file}'
    data=json.loads((ROOT/'assets/generated/activity.json').read_text())
    assert data['owner']=='Lokesh-1921'
    assert len(data['days'])>=350
    total=sum(d['count'] for d in data['days'])
    for file in (ROOT/'assets/generated').glob('stats-summary*.svg'):
        root=ET.parse(file).getroot()
        desc=root.find('{http://www.w3.org/2000/svg}desc').text
        assert f'contributions / last year: {total}' in desc
        assert f'public repositories: {len(data["repositories"])}' in desc
        assert f'active calendar days: {sum(d["count"]>0 for d in data["days"])}' in desc
        assert data['updated_at'][:10] in desc
    print(f'Validated {len(files)} SVGs, {len(parser.references)} README image references, immutable role headings, and {checked} files without institution branding.')


if __name__=='__main__':
    main()
