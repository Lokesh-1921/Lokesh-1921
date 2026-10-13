"""Generate NEURAL // LOKESH graphics with the Python standard library."""
from html import escape
from pathlib import Path
import math
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PALETTES = {
    "dark": dict(bg="#070B17", panel="#0D1426", border="#23314B",
                 text="#EAF2FF", muted="#A6B4D0", cyan="#68E6FF", violet="#A78BFA"),
    "light": dict(bg="#F5F8FF", panel="#FFFFFF", border="#D4DFF0",
                  text="#16243F", muted="#51627D", cyan="#087B92", violet="#7653C4"),
}
FONT = "Arial, Helvetica, sans-serif"
PROJECTS = {
    "vision": dict(number="01", title="STEREOVISION", subtitle="3D & Motion Analysis",
                   status="ACADEMIC PROJECT", lines=["From stereo images to depth,", "3D geometry, and motion."],
                   tags=["Python", "OpenCV", "NumPy", "pytest"]),
    "crm": dict(number="02", title="AI-FIRST CRM", subtitle="Healthcare Professional Interactions",
                status="DEVELOPMENT APP", lines=["Record HCP interactions and", "retrieve context from local PDFs."],
                tags=["FastAPI", "LangGraph", "FAISS", "React"]),
    "trip": dict(number="03", title="TRIP PLANNER AI", subtitle="Constraints before recommendations",
                 status="SYNTHETIC PROTOTYPE", lines=["Compare short trips within", "explicit budgets. Synthetic data."],
                 tags=["TypeScript", "React", "TanStack", "Vitest"]),
    "health": dict(number="04", title="HEALTHHACK", subtitle="Health Hackathon 3.0",
                   status="EVENT WEBSITE", lines=["A responsive healthcare-event", "experience built for clarity."],
                   tags=["TypeScript", "React", "Vite", "Tailwind"]),
}


def text(x, y, value, size=24, fill="#EAF2FF", weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" {extra}>{escape(str(value))}</text>')


def svg(width, height, content, title, description):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
            f'<g font-family="{FONT}">{content}</g></svg>\n')


def save(name, width, height, content, title, description):
    destination = ASSETS / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    body = svg(width, height, content, title, description)
    ET.fromstring(body)
    destination.write_text(body, encoding="utf-8")


def surface(p, w, h, grid=False):
    content = f'''<defs>
<linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p['bg']}"/><stop offset="1" stop-color="{p['panel']}"/></linearGradient>
<linearGradient id="spectrum"><stop stop-color="{p['cyan']}"/><stop offset="1" stop-color="{p['violet']}"/></linearGradient>
<radialGradient id="atmosphere"><stop stop-color="{p['violet']}" stop-opacity=".12"/><stop offset="1" stop-color="{p['violet']}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{p['border']}" stroke-width=".6"/></pattern>
</defs><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#surface)" stroke="{p['border']}"/>
<path d="M32 1H{w-32}" stroke="url(#spectrum)" stroke-opacity=".65" stroke-width="2"/>'''
    if grid:
        content += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#grid)" opacity=".35"/>'
    return content


def motion():
    # Text is never animated. The entire design is readable without this style.
    return '''<style>
@keyframes signal{to{stroke-dashoffset:-200}}
@keyframes breathe{0%,100%{opacity:.45}50%{opacity:.8}}
.signal{animation:signal 16s linear infinite}
.breathe{animation:breathe 10s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.signal,.breathe{animation:none!important}}
</style>'''


def constellation(p, cx, cy, scale=1):
    points = [(-132,-57),(-94,-115),(-12,-139),(94,-103),(146,-18),
              (113,73),(31,127),(-71,103),(-145,34),(0,0),(-36,-49),(51,45)]
    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,0),
             (0,9),(2,10),(3,9),(4,11),(5,9),(6,11),(7,9),(8,10),
             (9,10),(9,11),(10,11),(1,10),(6,9)]
    content = f'<g transform="translate({cx} {cy}) scale({scale})">'
    content += '<circle r="205" fill="url(#atmosphere)"/>'
    content += f'<ellipse rx="179" ry="149" transform="rotate(-28)" fill="none" stroke="{p["border"]}"/>'
    content += f'<ellipse rx="167" ry="103" transform="rotate(37)" fill="none" stroke="{p["cyan"]}" stroke-opacity=".19" stroke-dasharray="3 9"/>'
    content += f'<path d="M-183 0H183M0-166V166" stroke="{p["border"]}" stroke-dasharray="2 8"/>'
    for i, (a, b) in enumerate(edges):
        x1,y1=points[a]; x2,y2=points[b]
        content += f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{p["cyan"] if i%3 else p["violet"]}" stroke-opacity=".24" stroke-width="1.2"/>'
    content += f'<path d="M-132-57L0 0L94-103L146-18L51 45L31 127" fill="none" stroke="{p["cyan"]}" stroke-width="2" stroke-dasharray="7 193" class="signal"/>'
    content += f'<path d="M-145 34L-36-49L-12-139L94-103" fill="none" stroke="{p["violet"]}" stroke-width="2" stroke-dasharray="5 195" class="signal" style="animation-delay:-7s"/>'
    for i,(x,y) in enumerate(points):
        color=p["cyan"] if i%3 else p["violet"]
        content += f'<circle cx="{x}" cy="{y}" r="{5 if i==9 else 3.5}" fill="{color}"/>'
        if i in (2,6,9):
            content += f'<circle cx="{x}" cy="{y}" r="12" fill="none" stroke="{color}" stroke-opacity=".3" class="breathe"/>'
    content += f'<circle r="24" fill="{p["bg"]}" stroke="url(#spectrum)"/>'
    content += f'<path d="M-10 7V-7L10 7V-7" fill="none" stroke="{p["text"]}" stroke-width="2"/>'
    return content+'</g>'


def hero(p, mobile):
    w,h=(600,650) if mobile else (1200,480)
    content=surface(p,w,h,True)+motion()
    content += text(32 if mobile else 48,48,"NEURAL // LOKESH",22,p["cyan"],700,'letter-spacing="3"')
    if mobile:
        content += text(28,173,"LOKESH",125,p["text"],700,'letter-spacing="-5"')
        content += text(32,225,"Turning curiosity into",28,p["text"],400)
        content += text(32,262,"intelligent systems.",28,p["muted"])
        content += text(32,320,"AI ENGINEERING / MACHINE LEARNING",22,p["cyan"],600)
        content += text(32,354,"COMPUTER VISION",22,p["cyan"],600)
        content += constellation(p,300,482,.60)
        content += text(300,616,"INTELLIGENCE IN MOTION",22,p["muted"],500,'text-anchor="middle" letter-spacing="2"')
    else:
        content += text(1152,48,"INTELLIGENCE IN MOTION",22,p["muted"],500,'text-anchor="end" letter-spacing="2"')
        content += text(42,219,"LOKESH",145,p["text"],700,'letter-spacing="-6"')
        content += text(48,285,"Turning curiosity into intelligent systems.",30,p["muted"])
        content += text(48,351,"AI ENGINEERING / MACHINE LEARNING",22,p["cyan"],600,'letter-spacing=".6"')
        content += text(48,387,"COMPUTER VISION",22,p["cyan"],600,'letter-spacing=".6"')
        content += constellation(p,971,247,1)
        content += f'<path d="M48 426H1152" stroke="{p["border"]}"/>'
        content += text(48,455,"PERCEPTION / RETRIEVAL / USEFUL SOFTWARE",22,p["muted"],500,'letter-spacing="1"')
        content += text(1152,455,"PYTHON AT THE CORE",22,p["muted"],500,'text-anchor="end" letter-spacing="1"')
    return w,h,content


def role(p,mobile):
    w,h=(600,144) if mobile else (1200,116)
    # A single immutable role heading makes simultaneous titles impossible.
    content=motion()
    content += text(w/2,55 if mobile else 48,"ASPIRING AI ENGINEER",32,p["text"],600,'text-anchor="middle" letter-spacing="1.2" data-role-title="true"')
    content += text(w/2,91 if mobile else 79,"Python · Computer Vision · Machine Learning",23 if mobile else 22,p["muted"],400,'text-anchor="middle"')
    y=122 if mobile else 103
    content += f'<path d="M{w/2-88} {y}H{w/2+88}" stroke="{p["border"]}"/>'
    content += f'<path d="M{w/2-88} {y}H{w/2+88}" stroke="{p["cyan"]}" stroke-width="2" stroke-dasharray="6 170" class="signal"/>'
    for x in (-88,0,88):
        content += f'<circle cx="{w/2+x}" cy="{y}" r="3" fill="{p["cyan"]}" fill-opacity=".65"/>'
    return w,h,content


def icon(name,x,y,size=40,color=None):
    root=ET.fromstring((ASSETS/"icons"/(name+".svg")).read_text())
    for node in root.iter():
        for key,value in list(node.attrib.items()):
            if key=="id":
                node.set(key,name+"-"+value)
            else:
                node.set(key,re.sub(r'url\(#([^)]+)\)',lambda m:'url(#'+name+'-'+m[1]+')',value))
        if color and node.tag.split("}")[-1]=="path":
            node.set("fill",color)
    view=root.get("viewBox","0 0 128 128")
    children="".join(ET.tostring(child,encoding="unicode") for child in root)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{view}">{children}</svg>'


def stack(p,mobile):
    w,h=(600,740) if mobile else (1200,406)
    content=surface(p,w,h)
    groups=[
        ("CORE LANGUAGES",[("python","Python"),("typescript","TypeScript"),("javascript","JavaScript"),("java","Java")]),
        ("VISION + RETRIEVAL",[("opencv","OpenCV"),("numpy","NumPy"),(None,"LangGraph"),(None,"FAISS")]),
        ("APIs + APPLICATIONS",[("fastapi","FastAPI"),("react","React"),("postgresql","PostgreSQL"),("redis","Redis")]),
    ]
    for row,(label,tools) in enumerate(groups):
        base=32+row*(238 if mobile else 124)
        if mobile:
            content+=text(28,base+12,label,22,p["muted"],600,'letter-spacing="1.2"')
        else:
            pieces=label.rsplit(' ',1)
            for j,piece in enumerate(pieces):
                content+=text(28,base+12+j*29,piece,22,p["muted"],600,'letter-spacing="1"')
        for col,(name,label) in enumerate(tools):
            x=28+(col%2)*286 if mobile else 237+col*232
            y=base+36+(col//2)*82 if mobile else base-7
            content+=f'<rect x="{x}" y="{y}" width="{258 if mobile else 219}" height="70" rx="12" fill="{p["panel"]}" stroke="{p["border"]}"/>'
            if name:
                content+=icon(name,x+14,y+15,40)
            else:
                content+=f'<path d="M{x+23} {y+19}L{x+42} {y+36}L{x+23} {y+52}M{x+23} {y+19}V{y+52}" fill="none" stroke="{p["cyan"]}" stroke-width="2"/>'
                content+=f'<circle cx="{x+42}" cy="{y+36}" r="4" fill="{p["violet"]}"/>'
            content+=text(x+68,y+44,label,24 if mobile else 23,p["text"],500)
    return w,h,content


def project_art(p,kind):
    c=p["cyan"]; v=p["violet"]; border=p["border"]
    content='<g transform="translate(944 145)">'
    if kind=="vision":
        for layer in range(3):
            for row in range(4):
                for col in range(5):
                    x=-93+col*31+layer*12
                    y=-46+row*27-layer*13+col*3
                    content+=f'<circle cx="{x}" cy="{y}" r="2.5" fill="{c if layer!=1 else v}" opacity="{.35+layer*.25}"/>'
        content+=f'<path d="M-132-71L-7-91L132-38L7-17ZM-132-71V45L7 95V-17M7 95L132 73V-38" stroke="{border}" fill="none"/>'
    elif kind=="crm":
        for i,label in enumerate(["QUERY","RETRIEVE","TOOLS"]):
            x=-135+i*96
            content+=f'<rect x="{x}" y="-26" width="78" height="48" rx="9" stroke="{border}" fill="{p["panel"]}"/>'
            content+=text(x+39,6,label[0],26,c,600,'text-anchor="middle"')
            if i<2:content+=f'<path d="M{x+78}-2H{x+96}" stroke="{v}"/>'
        content+=f'<path d="M-96 24V57H96V24" stroke="{c}" stroke-opacity=".4" fill="none" stroke-dasharray="3 5"/>'
    elif kind=="trip":
        content+=f'<path d="M-135 39C-74-95 32 110 126-45" fill="none" stroke="{border}" stroke-width="2"/>'
        for x,y in [(-135,39),(-47,-6),(38,21),(126,-45)]:
            content+=f'<circle cx="{x}" cy="{y}" r="8" fill="{p["bg"]}" stroke="{c}"/><circle cx="{x}" cy="{y}" r="3" fill="{v}"/>'
    else:
        content+=f'<rect x="-124" y="-73" width="248" height="164" rx="13" stroke="{border}" fill="none"/><path d="M-124-42H124" stroke="{border}"/>'
        for i in range(3):content+=f'<circle cx="{-106+i*12}" cy="-57" r="3" fill="{c if i==0 else border}"/>'
        content+=f'<rect x="-103" y="-24" width="92" height="88" rx="6" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".3"/>'
        for y in (-21,13,47):
            content+=f'<rect x="10" y="{y}" width="92" height="22" rx="4" fill="{v}" fill-opacity=".13"/>'
    return content+'</g>'


def project_card(p,key,mobile):
    data=PROJECTS[key]
    w,h=(600,422) if mobile else (1200,300)
    content=surface(p,w,h)
    content+=f'<path d="M1 42V{h-42}" stroke="url(#spectrum)" stroke-width="2"/>'
    if mobile:
        content+=text(30,42,data["number"]+" / "+data["status"],22,p["cyan"],600,'letter-spacing="1"')
        content+=text(30,108,data["title"],39,p["text"],700,'letter-spacing="-1"')
        subtitle=data["subtitle"]
        # Long labels wrap into two fixed lines, leaving description space intact.
        if key=="crm":
            content+=text(30,148,"Healthcare Professional",24,p["muted"])
            content+=text(30,179,"Interactions",24,p["muted"])
        else:
            content+=text(30,153,subtitle,24,p["muted"])
        for i,line in enumerate(data["lines"]):
            content+=text(30,232+i*35,line,26,p["text"])
        for i,tag in enumerate(data["tags"]):
            x=30+(i%2)*274; y=300+(i//2)*48
            content+=f'<rect x="{x}" y="{y}" width="244" height="36" rx="8" fill="{p["cyan"]}" fill-opacity=".06" stroke="{p["border"]}"/>'
            content+=text(x+14,y+25,tag,22,p["muted"],500)
        content+=text(538,403,"VIEW SOURCE",22,p["cyan"],600,'text-anchor="end" letter-spacing="1"')
        content+=f'<path d="M551 399L566 384M551 384H566V399" fill="none" stroke="{p["cyan"]}" stroke-width="2"/>'
    else:
        content+=text(36,40,data["number"]+" / "+data["status"],22,p["cyan"],600,'letter-spacing="1.5"')
        content+=text(36,100,data["title"],40,p["text"],700,'letter-spacing="-1"')
        content+=text(36,139,data["subtitle"],23,p["muted"])
        content+=text(36,189," ".join(data["lines"]),23,p["text"])
        x=36
        for tag in data["tags"]:
            width=24+len(tag)*13
            content+=f'<rect x="{x}" y="222" width="{width}" height="38" rx="8" fill="{p["cyan"]}" fill-opacity=".06" stroke="{p["border"]}"/>'
            content+=text(x+12,248,tag,22,p["muted"],500)
            x+=width+12
        content+=project_art(p,key)
        content+=text(1127,275,"VIEW SOURCE",22,p["cyan"],600,'text-anchor="end" letter-spacing="1"')
        content+=f'<path d="M1140 271L1155 256M1140 256H1155V271" fill="none" stroke="{p["cyan"]}" stroke-width="2"/>'
    return w,h,content


def lab(p,mobile):
    w,h=(600,740) if mobile else (1200,344)
    content=surface(p,w,h,True)
    content+=text(30,46,"THE INTELLIGENCE LAB",24,p["text"],600,'letter-spacing="1.5"')
    topics=[
        ("01 / PERCEPTION","Learning to see",["Deep learning for","visual understanding."]),
        ("02 / GROUNDING","Learning to reason",["Retrieval for grounded","generative systems."]),
        ("03 / AGENCY","Learning to act",["Tools, explicit context,","and bounded workflows."]),
    ]
    if mobile:
        content+=text(30,78,"LEARNING DIRECTIONS",22,p["cyan"],600,'letter-spacing="1.5"')
    else:
        content+=text(1170,45,"LEARNING DIRECTIONS",22,p["cyan"],600,'text-anchor="end" letter-spacing="1.5"')
    for i,(label,title,lines) in enumerate(topics):
        x,y=(30,110+i*205) if mobile else (30+i*390,82)
        width=540 if mobile else 360
        content+=f'<rect x="{x}" y="{y}" width="{width}" height="{185 if mobile else 228}" rx="16" fill="{p["panel"]}" stroke="{p["border"]}"/>'
        content+=text(x+22,y+36,label,22,p["cyan"] if i!=1 else p["violet"],600,'letter-spacing="1"')
        content+=text(x+22,y+80,title,30 if mobile else 27,p["text"],600)
        for j,line in enumerate(lines):
            content+=text(x+22,y+123+j*32,line,24 if mobile else 22,p["muted"])
        if not mobile:
            for k in range(7):
                content+=f'<circle cx="{x+25+k*47}" cy="{y+199-int(4*math.sin(k+i))}" r="2" fill="{p["cyan"]}" fill-opacity=".45"/>'
    return w,h,content


def footer(p,mobile):
    w,h=(600,300) if mobile else (1200,234)
    content=surface(p,w,h,True)+motion()
    x=30 if mobile else 42
    content+=text(x,46,"NEURAL // LOKESH",22,p["cyan"],600,'letter-spacing="2"')
    content+=text(x,114 if mobile else 115,"Curiosity drives the code.",38 if mobile else 44,p["text"],600,'letter-spacing="-1"')
    content+=text(x,171 if mobile else 176,"Impact defines the work.",38 if mobile else 44,p["text"],600,'letter-spacing="-1"')
    content+=text(x,253 if mobile else 210,"LET'S BUILD SOMETHING USEFUL.",23 if mobile else 22,p["muted"],500,'letter-spacing="1"')
    if not mobile:
        content+=constellation(p,1030,135,.42)
    else:
        content+=f'<path d="M30 211H570" stroke="{p["border"]}"/><path d="M30 211H570" class="signal" stroke="{p["cyan"]}" stroke-dasharray="5 195"/>'
    return w,h,content


def main():
    for theme,p in PALETTES.items():
        for mobile in (False,True):
            suffix="-mobile" if mobile else ""
            for name,build,title,description in [
                ("hero",hero,"NEURAL // LOKESH — Intelligence in Motion","Lokesh. AI engineering, machine learning, computer vision. Turning curiosity into intelligent systems."),
                ("intro",role,"Aspiring AI Engineer","One static role heading with decorative animated signals. Python, computer vision, machine learning. No animated or stacked role text."),
                ("stack",stack,"Tools used in the work","Core languages, vision and retrieval, APIs and applications. Used tools are not claims of mastery."),
                ("lab",lab,"The Intelligence Lab","Learning directions: visual deep learning, grounded generation, and tool-based workflows."),
                ("footer",footer,"Curiosity drives the code. Impact defines the work.","NEURAL // LOKESH. An invitation to build something useful together."),
            ]:
                w,h,content=build(p,mobile)
                save(f"brand/{name}{suffix}-{theme}.svg",w,h,content,title,description)
                if name in ("hero","intro","footer"):
                    static=re.sub(r'<style>.*?</style>','',content,flags=re.S)
                    static=static.replace('class="breathe"','opacity=".45"')
                    static=static.replace('class="signal"','').replace('style="animation-delay:-7s"','')
                    save(f"brand/{name}{suffix}-static-{theme}.svg",w,h,static,title,description+" Static version for reduced motion.")
            for key in PROJECTS:
                w,h,content=project_card(p,key,mobile)
                save(f"project-cards/{key}{suffix}-{theme}.svg",w,h,content,PROJECTS[key]["title"]," ".join(PROJECTS[key]["lines"])+" Original conceptual schematic; not an application screenshot.")
    for name,label in [("linkedin","LinkedIn"),("github","GitHub")]:
        p=PALETTES["dark"]
        content=surface(p,210,48)
        content+=icon(name,16,12,24,color=p["text"] if name=="github" else None)
        content+=text(52,31,label,18,p["text"],500)
        content+=f'<path d="M165 31L177 19M165 19H177V31" fill="none" stroke="{p["muted"]}" stroke-width="1.5"/>'
        save("brand/"+name+".svg",210,48,content,label,"Connect with Lokesh on "+name+".")
    print("Built NEURAL brand, immutable role, project cards, and learning lab.")


if __name__=="__main__":
    main()
