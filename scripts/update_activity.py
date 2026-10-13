"""Render real public GitHub data without a stats service, token, or dependencies.

Fail closed if GitHub changes its markup; the workflow retains the last good assets.
"""
import argparse
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from profile_design.shared import PALETTES, text, surface, static_body
from profile_design.dashboard import dashboard, project_languages

ROOT = Path(__file__).resolve().parents[1]


class Repositories(HTMLParser):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.items = []
        self.current = None
        self.language = False
        self.next_page = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'li' and a.get('itemprop') == 'owns':
            self.current = {'name': None, 'language': None, 'fork': 'fork' in a.get('class', '').split()}
        if tag == 'a' and 'next_page' in a.get('class', '').split() and a.get('href'):
            self.next_page = urljoin('https://github.com', a['href'])
        if self.current is not None:
            if tag == 'a' and a.get('itemprop') == 'name codeRepository':
                parts = a.get('href', '').strip('/').split('/')
                if len(parts) != 2 or parts[0].lower() != self.owner.lower():
                    raise ValueError('Unexpected repository identity')
                self.current['name'] = parts[1]
            if tag == 'span' and a.get('itemprop') == 'programmingLanguage':
                self.language = True

    def handle_data(self, data):
        if self.language and self.current is not None and data.strip():
            self.current['language'] = data.strip()

    def handle_endtag(self, tag):
        if tag == 'span':
            self.language = False
        if tag == 'li' and self.current is not None:
            if not self.current['name']:
                raise ValueError('Repository markup has changed')
            self.items.append(self.current)
            self.current = None


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}
        self.tooltip = None
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and a.get('data-date'):
            match = re.fullmatch(r'contribution-day-component-(\d+)-(\d+)', a.get('id', ''))
            if not match:
                raise ValueError('Contribution grid identity has changed')
            y, x = map(int, match.groups())
            self.days[a['id']] = dict(date=a['data-date'], level=int(a['data-level']), x=x, y=y)
        if tag == 'tool-tip' and a.get('for') in self.days:
            self.tooltip = a['for']
            self.buffer = []

    def handle_data(self, data):
        if self.tooltip:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tooltip:
            match = re.match(r'\s*(No|[\d,]+) contributions? on ', ''.join(self.buffer))
            if not match:
                raise ValueError('Contribution tooltip has changed')
            self.days[self.tooltip]['count'] = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
            self.tooltip = None


def parse_calendar(body):
    parser = Calendar()
    parser.feed(body)
    days = sorted(parser.days.values(), key=lambda d: d['date'])
    if len(days) < 350 or any('count' not in d for d in days):
        raise ValueError('Incomplete contribution calendar; refusing to publish partial metrics')
    if any(d['count'] < 0 or not 0 <= d['level'] <= 4 or not 0 <= d['y'] <= 6 for d in days):
        raise ValueError('Invalid contribution data')
    total = re.search(r'([\d,]+)\s+contributions\s+in the last year', body)
    if not total or int(total[1].replace(',', '')) != sum(d['count'] for d in days):
        raise ValueError('Calendar total does not match GitHub’s displayed total')
    return days


def fetch(url):
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.hostname != 'github.com':
        raise ValueError('Only public HTTPS GitHub pages are supported')
    req = Request(url, headers={'User-Agent': 'Lokesh-profile-activity', 'Accept-Language': 'en-US,en;q=0.9'})
    with urlopen(req, timeout=45) as response:
        return response.read().decode('utf-8')


def collect(owner):
    items, seen = [], set()
    url = f'https://github.com/{owner}?tab=repositories&type=public'
    while url:
        if url in seen or len(seen) >= 100:
            raise ValueError('Unexpected repository pagination')
        seen.add(url)
        parser = Repositories(owner)
        parser.feed(fetch(url))
        items.extend(parser.items)
        url = parser.next_page
    if not items or len({i['name'] for i in items}) != len(items):
        raise ValueError('Empty or duplicated repository discovery')
    days = parse_calendar(fetch(f'https://github.com/users/{owner}/contributions'))
    # The dashboard needs language/fork/profile flags, not identifying project slugs.
    metadata=[dict(language=item['language'],fork=item['fork'],
                   is_profile=item['name'].lower()==owner.lower()) for item in items]
    return dict(owner=owner, updated_at=datetime.now(timezone.utc).isoformat(timespec='seconds'), repositories=metadata, days=days)


def svg(width, height, content, title, description):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc><g font-family="Arial, Helvetica, sans-serif">{content}</g></svg>\n'



def calendar_svg(data,theme,mobile=False):
    p=PALETTES[theme]
    days=data['days']; weeks=max(d['x'] for d in days)+1
    width,height=(600,838) if mobile else (weeks*20+56,262)
    colors=[p['border'],'#1C3B53','#22647C','#359BB5',p['cyan']] if theme=='dark' else ['#E5EDF8','#C3DFE8','#80BECF','#328CA3',p['cyan']]
    content=surface(p,width,height)
    content+=text(28,40,'CONTRIBUTION CALENDAR',23 if mobile else 20,p['muted'],600)
    if mobile:
        for window in range((weeks+13)//14):
            subset=[d for d in days if d['x']//14==window]
            if not subset:
                continue
            start,end=subset[0]['date'],subset[-1]['date']
            content+=text(28,80+window*184,f'{start} → {end}',22,p['muted'])
    for d in days:
        x=76+(d['x']%14)*32 if mobile else 28+d['x']*20
        y=96+(d['x']//14)*184+d['y']*19 if mobile else 66+d['y']*20
        content+=f'<rect x="{x}" y="{y}" width="{25 if mobile else 15}" height="15" rx="3" fill="{colors[d["level"]]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>'
    label=f'{sum(d["count"] for d in days):,} contributions · {data["updated_at"][:10]} UTC' if mobile else f'{days[0]["date"]} → {days[-1]["date"]} · {sum(d["count"] for d in days):,} contributions'
    content+=text(28,height-24,label,22,p['muted'])
    return svg(width,height,content,'Lokesh / static contribution calendar','Actual GitHub contribution calendar. Updated '+data['updated_at'][:10]+'.')


def render(data,out):
    out.mkdir(parents=True,exist_ok=True)
    files={}
    for theme in PALETTES:
        for compact in (False,True):
            suffix='-mobile' if compact else ''
            body=dashboard(data,theme,compact)
            files[f'stats-summary{suffix}-{theme}.svg']=body
            files[f'stats-summary{suffix}-static-{theme}.svg']=static_body(body)
            files[f'activity-calendar{suffix}-{theme}.svg']=calendar_svg(data,theme,compact)
    files['activity.json']=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
    # Render everything before replacing a previously successful snapshot.
    for name,body in files.items():
        temp=out/(name+'.tmp');temp.write_text(body,encoding='utf-8');temp.replace(out/name)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--owner',default='Lokesh-1921')
    parser.add_argument('--output',type=Path,default=ROOT/'assets/generated')
    parser.add_argument('--snapshot',type=Path,help='Render an existing verified public-data snapshot without network access')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}',args.owner):
        parser.error('Invalid GitHub username')
    data=json.loads(args.snapshot.read_text()) if args.snapshot else collect(args.owner)
    render(data,args.output)
    print(f'Rendered {len(data["repositories"])} public repositories and {sum(d["count"] for d in data["days"])} contributions. Snapshot: {data["updated_at"]}')


if __name__=='__main__':
    main()
