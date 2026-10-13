"""Shared palettes, geometry, local icons, motion, and static variants."""
from html import escape
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets'
PROFILE = json.loads((ROOT / 'content/profile.json').read_text())
PALETTES = {
    'dark': dict(bg='#070B17', panel='#0D1426', border='#23314B', text='#EAF2FF',
                 muted='#A6B4D0', cyan='#68E6FF', violet='#A78BFA'),
    'light': dict(bg='#F5F8FF', panel='#FFFFFF', border='#D4DFF0', text='#16243F',
                  muted='#51627D', cyan='#087B92', violet='#7653C4'),
}


def text(x, y, value, size=24, fill='#EAF2FF', weight=400, extra=''):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" {extra}>{escape(str(value))}</text>')


def rect(x, y, w, h, fill, border='none', radius=16, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{border}" {extra}/>'


def path(d, stroke, extra=''):
    return f'<path d="{d}" fill="none" stroke="{stroke}" {extra}/>'


def circle(x, y, r, fill, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'


def svg(w, h, body, title, description):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
            f'<g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>\n')


def surface(p, w, h, grid=False):
    body=f'''<defs>
<linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p['bg']}"/><stop offset="1" stop-color="{p['panel']}"/></linearGradient>
<linearGradient id="spectrum"><stop stop-color="{p['cyan']}"/><stop offset="1" stop-color="{p['violet']}"/></linearGradient>
<radialGradient id="atmosphere"><stop stop-color="{p['violet']}" stop-opacity=".22"/><stop offset="1" stop-color="{p['violet']}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p['border']}" stroke-width=".6"/></pattern>
<clipPath id="panel-clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22"/></clipPath>
</defs>'''
    body+=rect(1,1,w-2,h-2,'url(#surface)',p['border'],22)
    if grid:
        body+=rect(1,1,w-2,h-2,'url(#grid)',radius=22,extra='opacity=".32"')
    body+=path(f'M28 1H{w-28}','url(#spectrum)','stroke-width="2" stroke-opacity=".55"')
    return body


def motion(w=1200):
    # Only geometry animates. Text and metric values never animate.
    return f'''<style>
@keyframes flow{{to{{stroke-dashoffset:-240}}}}
@keyframes orbit{{to{{transform:rotate(360deg)}}}}
@keyframes orbitBack{{to{{transform:rotate(-360deg)}}}}
@keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:.7}}}}
@keyframes halo{{0%,100%{{transform:scale(.95);opacity:.2}}50%{{transform:scale(1.08);opacity:.55}}}}
@keyframes scan{{0%{{transform:translateX(0);opacity:0}}10%,85%{{opacity:.3}}100%{{transform:translateX({w-80}px);opacity:0}}}}
.flow{{animation:flow 14s linear infinite}}
.orbit{{animation:orbit 32s linear infinite;transform-origin:0px 0px}}
.orbit-back{{animation:orbitBack 44s linear infinite;transform-origin:0px 0px}}
.pulse{{animation:pulse 10s ease-in-out infinite}}
.halo{{animation:halo 12s ease-in-out infinite;transform-origin:0px 0px}}
.scan{{animation:scan 20s linear infinite}}
@media(prefers-reduced-motion:reduce){{.flow,.orbit,.orbit-back,.pulse,.halo,.scan{{animation:none!important}}}}
</style>'''


def trace(p, x, y, width, phase=0):
    body=path(f'M{x} {y}H{x+width}',p['border'],'stroke-width="1.5"')
    body+=path(f'M{x} {y}H{x+width}',p['cyan'],f'stroke-width="2" stroke-dasharray="28 212" class="flow" style="animation-delay:-{phase}s" opacity=".65"')
    return body


def arrow(p, x, y, size=15):
    return path(f'M{x} {y+size}L{x+size} {y}M{x} {y}H{x+size}V{y+size}',p['cyan'],'stroke-width="2"')


def icon(name, x, y, size=40, color=None):
    root=ET.parse(ASSETS/'icons'/f'{name}.svg').getroot()
    prefix=f'{name}-{x}-{y}-'
    for node in root.iter():
        for key,value in list(node.attrib.items()):
            if key=='id':node.set(key,prefix+value)
            else:node.set(key,re.sub(r'url\(#([^)]+)\)',lambda m:'url(#'+prefix+m[1]+')',value))
        if color and node.tag.split('}')[-1]=='path':node.set('fill',color)
    children=''.join(ET.tostring(child,encoding='unicode') for child in root)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{root.get("viewBox","0 0 128 128")}">{children}</svg>'


def static_body(body):
    body=re.sub(r'<style>.*?</style>','',body,flags=re.S)
    body=re.sub(r'\sclass="[^"]*"','',body)
    return re.sub(r'\sstyle="animation-delay:[^"]*"','',body)


def save(relative, w, h, body, title, description):
    destination=ASSETS/relative
    destination.parent.mkdir(parents=True,exist_ok=True)
    markup=svg(w,h,body,title,description)
    ET.fromstring(markup)
    destination.write_text(markup,encoding='utf-8')


def variants(stem, builder, title, description, animated=True):
    for theme,palette in PALETTES.items():
        for compact in (False,True):
            suffix='-mobile' if compact else ''
            w,h,body=builder(palette,compact)
            save(f'{stem}{suffix}-{theme}.svg',w,h,body,title,description)
            if animated:
                save(f'{stem}{suffix}-static-{theme}.svg',w,h,static_body(body),title,description+' Static reduced-motion version.')
