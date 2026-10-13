"""Render real public GitHub data without a stats service, token, or dependencies.

Fail closed if GitHub changes its markup; the workflow retains the last good assets.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from build_brand import PALETTES, text

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
    return dict(owner=owner, updated_at=datetime.now(timezone.utc).isoformat(timespec='seconds'), repositories=items, days=days)


def svg(width, height, content, title, description):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc><g font-family="Arial, Helvetica, sans-serif">{content}</g></svg>\n'


def dashboard(data, theme, mobile=False):
    p = PALETTES[theme]
    width, height = (600, 610) if mobile else (1200, 370)
    days = data['days']
    values = [('PUBLIC REPOSITORIES', len(data['repositories'])), ('CONTRIBUTIONS / LAST YEAR', sum(d['count'] for d in days)), ('ACTIVE CALENDAR DAYS', sum(d['count'] > 0 for d in days))]
    languages = Counter(i['language'] for i in data['repositories'] if not i['fork'] and i['language'])
    total = sum(languages.values())
    content = f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="{p["panel"]}" stroke="{p["border"]}"/>'
    content += text(28, 38, 'GITHUB / PUBLIC ACTIVITY', 18, p['cyan'], 600, 'letter-spacing="1.2"')
    for i,(label,value) in enumerate(values):
        x, y = (28, 83+i*100) if mobile else (28+i*395, 90)
        content += text(x,y+35,f'{value:,}',49 if mobile else 52,p['text'],700)
        content += text(x+113 if mobile else x,y+22 if mobile else y+70,label,17 if mobile else 15,p['muted'],500)
    y = 405 if mobile else 220
    content += text(28,y,'PRIMARY LANGUAGES / PUBLIC SOURCE REPOS',18 if mobile else 16,p['muted'],600)
    x = 28
    colors = ['#7295ff','#e6c15c','#51c5cc','#b797eb','#cc8974','#81a984']
    for index,(language,count) in enumerate(languages.most_common()):
        segment = (width-56)*count/total if total else 0
        content += f'<rect x="{x:.2f}" y="{y+20}" width="{segment:.2f}" height="13" fill="{colors[index%len(colors)]}"/>'
        x += segment
        lx = 28+(index%2)*280 if mobile else 28+(index%5)*230
        ly = y+65+(index//2)*32 if mobile else y+67+(index//5)*27
        content += f'<circle cx="{lx+5}" cy="{ly-6}" r="5" fill="{colors[index%len(colors)]}"/>'
        content += text(lx+19,ly,f'{language} · {count}/{total}',20 if mobile else 17,p['text'])
    date = data['updated_at'][:10]
    content += text(28,height-23,f'REFRESHED {date} UTC · github.com/{data["owner"]}',17 if mobile else 14,p['muted'])
    description = '; '.join(f'{label.lower()}: {value}' for label,value in values) + '. Languages count public source repositories, not code volume or skill level. Updated '+date+'.'
    return svg(width,height,content,'Lokesh / GitHub public activity',description)


def calendar_svg(data,theme):
    p=PALETTES[theme]
    days=data['days']; weeks=max(d['x'] for d in days)+1
    width=weeks*20+56; height=238
    colors=[p['border'],'#193c52','#1c6f80','#32b2bd','#51e2ed'] if theme=='dark' else ['#e7ecf5','#bcdee5','#77bac7','#2b8d9c','#007080']
    content=f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="{p["bg"]}" stroke="{p["border"]}"/>'
    content+=text(28,33,'CONTRIBUTION CALENDAR / STATIC VIEW',16,p['muted'],600)
    for d in days:
        content+=f'<rect x="{28+d["x"]*20}" y="{52+d["y"]*20}" width="15" height="15" rx="3" fill="{colors[d["level"]]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>'
    content+=text(28,216,f'{days[0]["date"]} → {days[-1]["date"]} · {sum(d["count"] for d in days):,} contributions',14,p['muted'])
    return svg(width,height,content,'Lokesh / static contribution calendar','Actual GitHub contribution calendar. Updated '+data['updated_at'][:10]+'.')


def render(data,out):
    out.mkdir(parents=True,exist_ok=True)
    files={}
    for theme in PALETTES:
        files[f'dashboard-{theme}.svg']=dashboard(data,theme)
        files[f'dashboard-mobile-{theme}.svg']=dashboard(data,theme,True)
        files[f'contributions-{theme}.svg']=calendar_svg(data,theme)
    files['activity.json']=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
    # Render everything before replacing a previously successful snapshot.
    for name,body in files.items():
        temp=out/(name+'.tmp');temp.write_text(body,encoding='utf-8');temp.replace(out/name)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--owner',default='Lokesh-1921')
    parser.add_argument('--output',type=Path,default=ROOT/'assets/live')
    parser.add_argument('--snapshot',type=Path,help='Render an existing verified public-data snapshot without network access')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}',args.owner):
        parser.error('Invalid GitHub username')
    data=json.loads(args.snapshot.read_text()) if args.snapshot else collect(args.owner)
    render(data,args.output)
    print(f'Rendered {len(data["repositories"])} public repositories and {sum(d["count"] for d in data["days"])} contributions. Snapshot: {data["updated_at"]}')


if __name__=='__main__':
    main()
