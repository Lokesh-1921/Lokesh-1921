"""Layered orbit artwork and the HUMAN opening/closing signatures."""
import math
from .shared import PROFILE, text, rect, path, circle, surface, motion, trace


def orbit_system(p, cx, cy, scale=1):
    c,v,b=p['cyan'],p['violet'],p['border']
    body=f'<g transform="translate({cx} {cy}) scale({scale})">'
    body+=circle(0,0,216,'url(#atmosphere)')
    for radius in (76,130,181):
        body+=circle(0,0,radius,'none',f'stroke="{b}" stroke-width=".8"')
    body+=path('M-195 0H195M0-195V195',b,'stroke-dasharray="2 9"')
    body+='<g class="orbit">'
    body+=circle(0,0,192,'none',f'stroke="{c}" stroke-opacity=".4" stroke-dasharray="48 112 4 112"')
    body+=circle(192,0,5,c)+circle(-192,0,3,v)
    body+='</g><g class="orbit-back">'
    body+=path('M-148-63A161 161 0 1 1 148 63',v,'stroke-width="1.2" stroke-dasharray="8 20" stroke-opacity=".45"')
    body+=circle(-148,-63,4,v)
    body+='</g>'
    points=[(-130,-59),(-74,-123),(28,-140),(123,-76),(148,29),(78,127),(-30,148),(-135,75),(-45,-27),(49,41),(25,-68)]
    edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),
           (0,8),(1,8),(2,10),(3,10),(4,9),(5,9),(6,8),(7,8),(8,9),(8,10),(9,10)]
    for i,(a,z) in enumerate(edges):
        x,y=points[a];xx,yy=points[z]
        body+=path(f'M{x} {y}L{xx} {yy}',c if i%3 else v,'stroke-opacity=".25" stroke-width="1.2"')
    body+=path('M-130-59L-45-27L49 41L148 29L123-76L25-68',c,'stroke-width="2" stroke-dasharray="32 208" class="flow" opacity=".8"')
    body+=path('M-74-123L28-140L25-68L-45-27L-30 148L78 127',v,'stroke-width="2" stroke-dasharray="24 216" class="flow" style="animation-delay:-6s" opacity=".7"')
    for i,(x,y) in enumerate(points):
        color=c if i%3 else v
        body+=circle(x,y,3.5,color)
        if i in (1,4,6):
            body+=circle(x,y,10,'none',f'stroke="{color}" stroke-opacity=".25" class="pulse" style="animation-delay:-{i}s"')
    for i in range(24):
        a=i*math.pi/12
        body+=path(f'M{201*math.cos(a):.2f} {201*math.sin(a):.2f}L{(208 if i%3==0 else 204)*math.cos(a):.2f} {(208 if i%3==0 else 204)*math.sin(a):.2f}',b)
    body+='<g class="halo">'+circle(0,0,51,'none',f'stroke="{c}" stroke-width="1" opacity=".3"')+'</g>'
    body+=circle(0,0,35,p['bg'],'stroke="url(#spectrum)" stroke-width="1.5"')
    body+=path('M-11-12V12M11-12V12M-11 0H11',p['text'],'stroke-width="2.4" stroke-linecap="round"')
    return body+'</g>'


def hero(p, compact):
    w,h=(600,776) if compact else (1200,530)
    body=surface(p,w,h,True)+motion(w)
    body+='<g clip-path="url(#panel-clip)">'+rect(30,76,20,h-120,p['cyan'],radius=0,extra='opacity=".035" class="scan"')+'</g>'
    x=32 if compact else 48
    body+=text(x,49,PROFILE['identity'],22,p['cyan'],700,'letter-spacing="2.8"')
    if compact:
        body+=text(26,178,'LOKESH',125,p['text'],700,'letter-spacing="-5"')
        body+=text(32,236,'Turning curiosity into',28,p['text'])
        body+=text(32,274,'intelligent systems.',28,p['muted'])
        body+=text(32,326,'AI ENGINEERING / MACHINE LEARNING',22,p['cyan'],600)
        body+=text(32,361,'GENERATIVE AI',22,p['cyan'],600,'letter-spacing="1"')
        body+=orbit_system(p,300,522,.62)
        body+=trace(p,32,706,536,4)
        body+=text(32,743,'PYTHON AT THE CORE',21,p['muted'],500,'letter-spacing=".8"')
        body+=text(568,743,'BUILD / LEARN / REFINE',18,p['muted'],500,'text-anchor="end"')
        body+=text(300,681,'INTELLIGENCE IN MOTION',20,p['muted'],500,'text-anchor="middle" letter-spacing="2"')
    else:
        body+=text(1152,49,'INTELLIGENCE IN MOTION',20,p['muted'],500,'text-anchor="end" letter-spacing="2"')
        body+=text(40,225,'LOKESH',151,p['text'],700,'letter-spacing="-6"')
        body+=text(48,289,PROFILE['tagline'],29,p['muted'])
        body+=text(48,359,'AI ENGINEERING / MACHINE LEARNING',23,p['cyan'],600,'letter-spacing=".5"')
        body+=text(48,396,'GENERATIVE AI',23,p['cyan'],600,'letter-spacing="1"')
        body+=orbit_system(p,967,264,.96)
        body+=trace(p,48,463,1104,5)
        body+=text(48,501,'GENERATION / RETRIEVAL / USEFUL SOFTWARE',20,p['muted'],500,'letter-spacing=".8"')
        body+=text(1152,501,'PYTHON AT THE CORE',20,p['muted'],500,'text-anchor="end" letter-spacing="1"')
    return w,h,body


def closing(p, compact):
    w,h=(600,350) if compact else (1200,300)
    body=surface(p,w,h,True)+motion(w)
    x=32 if compact else 44
    body+=text(x,49,PROFILE['identity'],22,p['cyan'],600,'letter-spacing="2"')
    body+=text(x,127,'Curiosity drives the code.',38 if compact else 45,p['text'],600,'letter-spacing="-1"')
    body+=text(x,187,'Impact shapes the system.',38 if compact else 45,p['text'],600,'letter-spacing="-1"')
    body+=trace(p,x,235,536 if compact else 684,8)
    body+=text(x,290 if compact else 274,"LET'S BUILD SOMETHING USEFUL.",22,p['muted'],500,'letter-spacing="1"')
    if not compact:body+=orbit_system(p,1030,158,.55)
    else:
        body+=text(x,322,'PYTHON / AI / PURPOSEFUL SOFTWARE',19,p['muted'],500)
    return w,h,body
