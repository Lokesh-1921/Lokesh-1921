"""Uniform source-linked project modules with conceptual animated schematics."""
from .shared import text, rect, path, circle, surface, motion, trace, arrow


def schematic(p, key):
    c,v,b=p['cyan'],p['violet'],p['border']
    body='<g transform="translate(963 143)">'
    if key=='crm':
        for i,label in enumerate(('ROUTE','CONTEXT','ANSWER')):
            x=-152+i*109
            body+=rect(x,-30,88,60,p['panel'],b,12)
            body+=text(x+44,6,label,16,p['text'],500,'text-anchor="middle"')
            if i<2:body+=path(f'M{x+88} 0H{x+109}',c,'stroke-width="2"')
        body+=path('M-108 32V68H110V32',b,'stroke-dasharray="4 7"')
        body+=path('M-152 47H152',c,'stroke-width="1.5" stroke-dasharray="12 228" class="flow" opacity=".5"')
        body+=text(0,104,'ROUTING + RETRIEVAL',18,p['muted'],400,'text-anchor="middle"')
    elif key=='trip':
        d='M-148 50C-79-91-18 100 38 14S117-91 150-31'
        body+=path(d,b,'stroke-width="2"')
        body+=path(d,c,'stroke-width="2" stroke-dasharray="28 212" class="flow"')
        for x,y in ((-148,50),(-47,18),(38,14),(150,-31)):
            body+=circle(x,y,7,p['bg'],f'stroke="{c}"')+circle(x,y,2.5,v)
        body+=text(0,103,'BUDGET / FILTER / RANK',18,p['muted'],400,'text-anchor="middle"')
    elif key=='health':
        body+=rect(-146,-74,292,165,'none',b,12)
        body+=path('M-146-45H146',b)
        for i in range(3):body+=circle(-126+i*14,-59,3,c if i==0 else b)
        body+=rect(-123,-21,107,90,c,radius=8,extra='fill-opacity=".06"')
        for y in (-20,14,48):body+=rect(5,y,116,20,v,radius=4,extra='fill-opacity=".1"')
        body+=path('M-123 76H122',c,'stroke-width="2" stroke-dasharray="26 214" class="flow"')
        body+=text(0,121,'CONTENT / ACCESSIBILITY',18,p['muted'],400,'text-anchor="middle"')
    else:
        for layer in range(3):
            for row in range(4):
                for col in range(5):
                    body+=circle(-104+col*39+layer*13,-47+row*29-layer*12+col*4,2.8,c if layer%2==0 else v,f'opacity="{.3+layer*.25}"')
        body+=path('M-144-80L-4-102L144-37L8-16ZM-144-80V46L8 105V-16M8 105L144 75V-37',b)
        body+=path('M-144-80L8-16L144-37',c,'stroke-width="1.5" stroke-dasharray="20 220" class="flow" opacity=".65"')
    return body+'</g>'


def project_card(p, compact, project, number):
    w,h=(600,466) if compact else (1200,318)
    body=surface(p,w,h)+motion(w)
    body+=rect(1,36,3,h-72,'url(#spectrum)',radius=1)
    x=32
    body+=text(x,43,f'{number:02} / '+project['status'],21,p['cyan'],600,'letter-spacing="1"')
    body+=text(x,111,project['title'],40,p['text'],700,'letter-spacing="-.7"')
    if compact:
        for i,line in enumerate(project['mobile_subtitle']):body+=text(x,151+i*31,line,24,p['muted'])
        for i,line in enumerate(project['lines']):body+=text(x,238+i*35,line,26,p['text'])
        for i,tag in enumerate(project['tags']):
            tx=32+(i%2)*280;ty=309+(i//2)*49
            body+=rect(tx,ty,256,37,p['panel'],p['border'],8)
            body+=text(tx+14,ty+26,tag,23,p['muted'],500)
        body+=trace(p,32,420,536,number*3)
        body+=text(538,451,'VIEW SOURCE',21,p['cyan'],600,'text-anchor="end" letter-spacing="1"')
        body+=arrow(p,550,434)
    else:
        body+=text(x,151,project['subtitle'],24,p['muted'])
        body+=text(x,202,' '.join(project['lines']),24,p['text'])
        tx=x
        for tag in project['tags']:
            tw=28+len(tag)*13
            body+=rect(tx,240,tw,38,p['panel'],p['border'],8)
            body+=text(tx+14,266,tag,22,p['muted'],500)
            tx+=tw+12
        body+=schematic(p,project['key'])
        body+=trace(p,32,300,1136,number*3)
        body+=text(1125,285,'VIEW SOURCE',19,p['cyan'],600,'text-anchor="end" letter-spacing="1"')
        body+=arrow(p,1140,270)
    return w,h,body
