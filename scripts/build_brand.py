"""Build original, self-contained profile graphics. Python standard library only."""
from pathlib import Path
from html import escape
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PALETTES = {
    "dark": dict(bg="#080f20", panel="#101b30", border="#243249", text="#edf5ff", muted="#9dacc6", cyan="#51e2ed", violet="#ac9bff"),
    "light": dict(bg="#f5f8ff", panel="#ffffff", border="#d7e1ef", text="#13233f", muted="#516681", cyan="#007b89", violet="#7155ca"),
}


def text(x, y, value, size=24, fill="#edf5ff", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def save(name, width, height, content, title, description):
    ASSETS.mkdir(parents=True, exist_ok=True)
    doc = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<g font-family="Arial, Helvetica, sans-serif">{content}</g></svg>'''
    ET.fromstring(doc)
    (ASSETS / name).write_text(doc + "\n", encoding="utf-8")


def hero(p, mobile=False):
    w, h = (600, 440) if mobile else (1200, 350)
    content = f'''<defs>
<linearGradient id="background" x2="1" y2="1"><stop stop-color="{p['bg']}"/><stop offset="1" stop-color="{p['panel']}"/></linearGradient>
<linearGradient id="accent"><stop stop-color="{p['cyan']}"/><stop offset="1" stop-color="{p['violet']}"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p['border']}" stroke-width=".6"/></pattern>
</defs><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="url(#background)" stroke="{p['border']}"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="url(#grid)" opacity=".35"/>
<path d="M40 1H{w-40}" stroke="url(#accent)" stroke-width="2"/>'''
    if mobile:
        content += text(32, 49, "COMPUTER SCIENCE / AI + ML", 19, p["cyan"], 600, 'letter-spacing="2"')
        content += text(28, 159, "LOKESH", 99, p["text"], 700, 'letter-spacing="-5"')
        content += text(32, 213, "Learning to build intelligent systems.", 24, p["muted"])
        content += text(32, 262, "VIT BHOPAL  /  B.TECH CSE", 19, p["text"], 600, 'letter-spacing="1"')
        content += text(32, 294, "Specialization: AI & ML", 20, p["muted"])
        content += '<path d="M32 342H568" stroke="'+p['border']+'"/>'
        content += text(32, 388, "VISION", 17, p["cyan"], 600)
        content += text(190, 388, "RETRIEVAL", 17, p["cyan"], 600)
        content += text(398, 388, "SOFTWARE", 17, p["violet"], 600)
    else:
        content += text(46, 58, "COMPUTER SCIENCE / AI + ML", 17, p["cyan"], 600, 'letter-spacing="3"')
        content += text(39, 190, "LOKESH", 132, p["text"], 700, 'letter-spacing="-6"')
        content += text(46, 241, "Learning to build intelligent systems.", 27, p["muted"])
        content += text(46, 307, "VIT BHOPAL   /   B.TECH CSE   /   AI & ML", 17, p["text"], 600, 'letter-spacing="1.2"')
        # A schematic latent-space lattice, not a project screenshot.
        nodes = []
        for row in range(4):
            for col in range(5):
                x = 797 + col*54 + row*17
                y = 90 + row*44 - col*6
                nodes.append((x, y))
        content += '<g stroke="'+p['cyan']+'" fill="none" stroke-width="1" opacity=".4">'
        for i, (x,y) in enumerate(nodes):
            if i % 5 != 4:
                nx,ny=nodes[i+1]; content += f'<path d="M{x} {y}L{nx} {ny}"/>'
            if i+5<len(nodes):
                nx,ny=nodes[i+5]; content += f'<path d="M{x} {y}L{nx} {ny}"/>'
        content += '</g>'
        for i,(x,y) in enumerate(nodes):
            color = p['violet'] if i % 4 == 0 else p['cyan']
            content += f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>'
        content += f'<ellipse cx="939" cy="161" rx="186" ry="91" transform="rotate(-19 939 161)" fill="none" stroke="{p["violet"]}" stroke-opacity=".3"/>'
        content += text(795, 292, "OBSERVE  →  UNDERSTAND  →  BUILD", 13, p["muted"], 500, 'letter-spacing="1"')
    return w, h, content


def intro(p, mobile=False):
    phrases = ["Computer Science | AI & ML", "Aspiring AI Engineer", "Exploring Machine Learning & Computer Vision", "Building Projects With Python"]
    styles = []
    for i in range(4):
        a, b = i*25, i*25+22
        styles.append(f'@keyframes line{i}{{0%,100%{{opacity:{1 if i==0 else 0}}}' + ('' if i==0 else f'{a-1}%{{opacity:0}}') + f'{a}%,{b}%{{opacity:1}}{b+2}%{{opacity:0}}}}')
    styles += ['.line{opacity:0}', '.line0{opacity:1}', '@media(prefers-reduced-motion:reduce){.line{animation:none!important}.line:not(.line0){display:none}}']
    content = '<style>'+''.join(styles)+'</style>'
    for i, phrase in enumerate(phrases):
        pieces = ['Exploring Machine Learning', '& Computer Vision'] if mobile and i==2 else [phrase]
        for j, piece in enumerate(pieces):
            x, y = (300, 35+j*32 if len(pieces)>1 else 51) if mobile else (600, 39)
            content += text(x, y, piece, 25 if mobile else 28, p['cyan'], 500, f'text-anchor="middle" class="line line{i}" style="animation:line{i} 20s infinite"')
    return content


def icon(name, x, y, size=38):
    file = ASSETS / "icons" / (name + ".svg")
    root = ET.fromstring(file.read_text())
    for element in root.iter():
        for key,value in list(element.attrib.items()):
            if key == 'id':
                element.set(key, name+'-'+value)
            else:
                import re
                element.set(key, re.sub(r'url\(#([^)]+)\)', lambda m: 'url(#'+name+'-'+m[1]+')', value))
    view = root.attrib.get("viewBox", "0 0 128 128")
    body = ''.join(ET.tostring(child, encoding="unicode") for child in root)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{view}">{body}</svg>'


def stack(p, mobile=False):
    w, h = (600, 710) if mobile else (1200, 352)
    content = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{p["panel"]}" stroke="{p["border"]}"/>'
    groups = [("LANGUAGES", [("python","Python"),("typescript","TypeScript"),("javascript","JavaScript"),("java","Java")]), ("VISION + AI", [("opencv","OpenCV"),("numpy","NumPy"),(None,"LangGraph"),(None,"FAISS")]), ("APPLICATIONS", [("react","React"),("fastapi","FastAPI"),("postgresql","PostgreSQL"),("redis","Redis")])]
    for row,(label, tools) in enumerate(groups):
        base = 28+row*(225 if mobile else 110)
        content += text(24, base+13, label, 18 if mobile else 15, p['muted'], 600, 'letter-spacing="1.5"')
        for col,(name, title) in enumerate(tools):
            x = 30+(col%2)*284 if mobile else 230+col*235
            y = base+34+(col//2)*82 if mobile else base-8
            content += f'<rect x="{x-8}" y="{y-5}" width="{264 if mobile else 218}" height="68" rx="12" fill="{p["bg"]}"/>'
            if name:
                content += icon(name,x+5,y+9,40)
            else:
                content += f'<rect x="{x+5}" y="{y+9}" width="40" height="40" rx="9" fill="{p["cyan"]}" fill-opacity=".12"/>'
                content += text(x+25,y+36,"LG" if title=="LangGraph" else "F",17,p['cyan'],700,'text-anchor="middle"')
            content += text(x+60,y+37,title,25 if mobile else 23,p['text'],500)
    return w,h,content


def projects(p, mobile=False):
    w,h=(600,260) if mobile else (1200,168)
    content = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{p["bg"]}" stroke="{p["border"]}"/>'
    for i, (label, subtitle) in enumerate([("01 / VISION", "Depth + motion"),("02 / AI SYSTEMS", "Tools + retrieval"),("03 / PLANNING", "Constraints + clarity"),("04 / EXPERIENCE", "Design + accessibility")]):
        x=28+(i%2)*285 if mobile else 28+i*295
        offset=(i//2)*120 if mobile else 0
        content += text(x,43+offset,label,17 if mobile else 15,p['cyan'] if i%2==0 else p['violet'],600,'letter-spacing="1"')
        content += text(x,78+offset,subtitle,21,p['text'],500)
        for j in range(6):
            y=110+offset-int(13*math.sin(j+i))
            content+=f'<circle cx="{x+15+j*35}" cy="{y}" r="3" fill="{p["cyan"]}"/>'
            if j: content+=f'<path d="M{x+15+(j-1)*35} {110+offset-int(13*math.sin(j-1+i))}L{x+15+j*35} {y}" stroke="{p["border"]}" fill="none"/>'
    return content


def main():
    for theme,p in PALETTES.items():
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            w,h,content=hero(p,mobile)
            save(f'hero{suffix}-{theme}.svg',w,h,content,'Lokesh / AI + ML','Computer science student at VIT Bhopal. Learning to build intelligent systems.')
            save(f'intro{suffix}-{theme}.svg',600 if mobile else 1200,88 if mobile else 64,intro(p,mobile),'Lokesh / introduction','Computer Science | AI & ML. Aspiring AI Engineer. Exploring Machine Learning & Computer Vision. Building Projects With Python. Animation disabled when reduced motion is requested.')
            w,h,content=stack(p,mobile)
            save(f'stack{suffix}-{theme}.svg',w,h,content,'Tools behind the work','Technologies evidenced in Lokesh’s public repositories. LangGraph and FAISS use original letter marks, not official logos.')
            save(f'projects{suffix}-{theme}.svg',600 if mobile else 1200,260 if mobile else 168,projects(p,mobile),'Selected engineering','A schematic introduction to computer vision, AI systems, planning, and interface projects. Decorative diagrams, not application screenshots.')
        footer=f'<rect x="1" y="1" width="1198" height="94" rx="18" fill="{p["bg"]}" stroke="{p["border"]}"/>'+text(32,55,'OBSERVE. UNDERSTAND. BUILD.',26,p['text'],600)+text(1168,55,'LOKESH / ALWAYS LEARNING',16,p['cyan'],500,'text-anchor="end" letter-spacing="1"')
        save(f'footer-{theme}.svg',1200,96,footer,'Observe. Understand. Build.','Lokesh / Always learning.')
        footer_mobile=f'<rect x="1" y="1" width="598" height="138" rx="18" fill="{p["bg"]}" stroke="{p["border"]}"/>'+text(28,57,'OBSERVE. UNDERSTAND. BUILD.',25,p['text'],600)+text(28,105,'LOKESH / ALWAYS LEARNING',20,p['cyan'],500,'letter-spacing="1"')
        save(f'footer-mobile-{theme}.svg',600,140,footer_mobile,'Observe. Understand. Build.','Lokesh / Always learning.')
    for name,label in [('linkedin','LinkedIn / connect'),('github','GitHub / explore')]:
        content='<rect x=".5" y=".5" width="223" height="39" rx="9" fill="#101b30" stroke="#34435e"/>'
        content+=text(14,27,'in' if name=='linkedin' else '⌘',21,'#51e2ed',700)
        content+=text(47,26,label,15,'#edf5ff',500)
        save(name+'.svg',224,40,content,label,label)
    print('Built original brand assets for both themes and mobile layouts.')


if __name__ == '__main__':
    main()
